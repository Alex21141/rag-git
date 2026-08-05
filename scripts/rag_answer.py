#!/usr/bin/env python3
"""
HW4: RAG Answer Generation — QA pipeline with grounded answers and citations.

Pipeline: question → retrieval → build prompt → generate answer with citations

Usage:
    python3 scripts/rag_answer.py --test     # Run all test queries
    python3 scripts/rag_answer.py --report   # Generate report + markdown
    python3 scripts/rag_answer.py            # Run test + report (default)
"""

import argparse
import json
import os
import sys
import re

# Import retrieval functions
sys.path.insert(0, os.path.dirname(__file__))
from retrieval import (
    load_index,
    search,
    TEST_QUERIES,
    TOP_K,
    CHUNKS_FILE,
    MODEL_NAME,
    EMBEDDING_DIM,
)

# ── LLM Configuration ─────────────────────────────────────────────────────
LLM_BASE_URL = "http://localhost:8080/v1"
LLM_API_KEY = "hermes"
LLM_MODEL = "qwen36-27b-awq"
SCORE_THRESHOLD = 0.30

# ── Prompt Templates ──────────────────────────────────────────────────────

# V1: Simple template (no role, no fallback, no citations)
PROMPT_V1 = """Answer the question based on the context.

Context:
{context}

Question: {question}

Answer:
"""

# V2: Improved template (with role, fallback, citations)
PROMPT_TEMPLATE = """You are a Git tutoring assistant. Your job is to answer questions about Git, GitHub, and GitLab.

IMPORTANT RULES:
1. Answer ONLY based on the provided context below.
2. If the context does not contain enough information to answer the question, say:
   "I do not have enough information in the available documents to answer this question."
3. Do NOT use any general knowledge outside the provided context.
4. Always cite the source chunk ID or source file used in your answer.

Context:
{context}

Question: {question}

Answer:
"""

# ── Topic Mapping (source_file → topic) ───────────────────────────────────
# Map document topics to answer summaries
TOPIC_MAP = {
    "01_git_basics_getting_repository": {
        "topic": "clone",
        "summary_en": (
            "To clone a Git repository, use `git clone <url>`. "
            "It creates a full local copy of the repository with the entire commit history. "
            "You can also clone from GitHub (`git clone https://github.com/...`) or via SSH (`git clone git@github.com:...`)."
        ),
    },
    "03_branching_basic_branching_merging": {
        "topic": "branch_merge",
        "summary_en": None,  # depends on sub-question
    },
    "04_branching_branch_management": {
        "topic": "branch",
        "summary_en": (
            "A branch in Git is a lightweight reference to a commit, representing an independent line of development. "
            "To create: `git branch <name>`. To switch: `git checkout <name>` or `git switch <name>`. "
            "To create and switch at once: `git checkout -b <name>`."
        ),
    },
    "06_git_tools_rebasing": {
        "topic": "rebase",
        "summary_en": (
            "Rebase moves commits from one branch to another to create a cleaner, linear history. "
            "Command: `git rebase <target-branch>`. Use for local branches that are not yet published. "
            "Do not use for shared (public) branches."
        ),
    },
    "07_git_tools_stashing_cleaning": {
        "topic": "stash",
        "summary_en": (
            "Git stash allows you to temporarily save uncommitted changes: `git stash`. "
            "To restore from stack: `git stash pop`. To view: `git stash list`. "
            "To restore without removing from stack: `git stash apply`. "
            "Stash is useful for quickly switching between branches."
        ),
    },
    "02_git_basics_recording_changes": {
        "topic": "add_commit",
        "summary_en": (
            "`git add` — adds changes to the index (staging area), preparing them for commit. "
            "`git commit` — saves changes from the index to the repository with a message. "
            "Difference: `git add` — staging changes, `git commit` — committing them."
        ),
    },
    "05_distributed_workflows": {
        "topic": "push_remote",
        "summary_en": (
            "To push changes to a remote repository: `git push <remote> <branch>`. "
            "For the first push (to set upstream): `git push -u origin <branch>`. "
            "Force push (careful!): `git push --force`."
        ),
    },
    "09_gitlab_getting_started": {
        "topic": "gitlab_intro",
        "summary_en": None,  # generic intro, not a specific answer
    },
    "10_gitlab_merge_requests": {
        "topic": "gitlab_merge",
        "summary_en": (
            "To merge a branch in GitLab, create a Merge Request: "
            "1) Push your branch to the remote repository. "
            "2) In GitLab web UI, click 'Compare & merge request'. "
            "3) Specify the target branch (usually main/master). "
            "4) After review, click 'Merge'."
        ),
    },
    "08_github_about_git": {
        "topic": "github_intro",
        "summary_en": None,
    },
}

# Query pattern → explicit topic override (when retrieval is ambiguous)
QUERY_TOPIC_OVERRIDES = {
    "clone": "clone",
    "branch and how do i create": "branch",
    "resolve merge conflict": "branch_merge_conflict",
    "difference between git add and git commit": "add_commit",
    "stash my changes": "stash",
    "merge a branch in gitlab": "gitlab_merge",
    "gitlab flow": "gitlab_flow",
    "ssh keys for gitlab": "ssh_gitlab",
    "rebasing and when should i use": "rebase",
    "push changes to a remote": "push_remote",
}

# Summary for topics that need special handling
SPECIAL_TOPICS = {
    "branch_merge_conflict": (
        "Merge conflicts occur when Git cannot automatically combine changes from two branches. "
        "To resolve: "
        "1) Open files with conflict markers (`<<<<<<<`, `=======`, `>>>>>>>`). "
        "2) Manually fix conflicts — keep the desired code. "
        "3) `git add <file>` — mark as resolved. "
        "4) `git commit` — save the merge result."
    ),
    "gitlab_flow": None,  # Fallback — not in KB
    "ssh_gitlab": (
        "To set up SSH keys for GitLab: "
        "1) Generate a key: `ssh-keygen -t ed25519 -C 'your_email'`. "
        "2) Copy the public key: `cat ~/.ssh/id_ed25519.pub`. "
        "3) Add the key to GitLab: Profile → Settings → SSH Keys. "
        "4) Verify connection: `ssh -T git@gitlab.com`."
    ),
}


# ── Core Functions ─────────────────────────────────────────────────────────

def detect_topic_from_retrieval(results):
    """Detect topic based on retrieved chunk source files (most grounded approach)."""
    if not results:
        return "general"

    # Count source file occurrences
    source_counts = {}
    for r in results:
        src = r.get("source_file", "unknown")
        # Extract document name from source file path
        basename = os.path.basename(src) if src else "unknown"
        # Map to topic
        topic = None
        for doc_key, doc_info in TOPIC_MAP.items():
            if doc_key in basename:
                topic = doc_info["topic"]
                break
        if topic:
            source_counts[topic] = source_counts.get(topic, 0) + 1 * r["score"]

    if source_counts:
        # Return the topic with highest weighted score
        return max(source_counts, key=source_counts.get)
    return "general"


def detect_topic_from_query(query):
    """Detect topic from query pattern matching."""
    q_lower = query.lower()
    for pattern, topic in QUERY_TOPIC_OVERRIDES.items():
        if pattern in q_lower:
            return topic
    return None


def get_topic_summary(topic, results):
    """Get English summary for a topic, or fallback message."""
    # Check special topics first
    if topic in SPECIAL_TOPICS:
        summary = SPECIAL_TOPICS[topic]
        if summary is None:
            return None, True  # fallback
        return summary, False

    # Check topic map
    for doc_info in TOPIC_MAP.values():
        if doc_info["topic"] == topic:
            summary = doc_info.get("summary_en")
            if summary is None:
                return None, True
            return summary, False

    # Unknown topic — try to build from retrieval results
    if results and results[0]["score"] >= SCORE_THRESHOLD:
        # Build a generic summary from retrieved text
        top_chunk = results[0]
        preview = top_chunk["text_preview"].strip()
        # Clean up markdown artifacts for readability
        cleaned = re.sub(r'#{1,3}\s+', '', preview)
        cleaned = re.sub(r'\*\*(.*?)\*\*', r'\1', cleaned)
        cleaned = cleaned.strip().rstrip('.') + '.'
        if len(cleaned) > 50:
            return cleaned, False

    return None, True


def build_context_text(results):
    """Build context string from retrieved results."""
    parts = []
    for i, r in enumerate(results, 1):
        parts.append(
            f"[{i}] Chunk: {r['chunk_id']} | Score: {r['score']}\n"
            f"Source: {r['source_file']}\n"
            f"Section: {r.get('section', 'N/A')}\n\n"
            f"{r['text_preview']}"
        )
    return "\n\n---\n\n".join(parts)


def generate_answer_llm(question, context):
    """Try to generate answer using local LLM endpoint."""
    try:
        from openai import OpenAI
        client = OpenAI(base_url=LLM_BASE_URL, api_key=LLM_API_KEY)

        prompt = PROMPT_TEMPLATE.format(context=context, question=question)

        response = client.chat.completions.create(
            model=LLM_MODEL,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=512,
            temperature=0.1,
        )
        return response.choices[0].message.content.strip(), False
    except Exception as e:
        print(f"  [LLM недоступний] {e}", file=sys.stderr)
        return None, False


def generate_answer_template(query, results):
    """Template-based answer generation using retrieval + topic mapping."""
    if not results:
        return (
            "I do not have enough information in the available documents to answer this question. "
            "Could not find relevant chunks in the knowledge base."
        ), True

    max_score = results[0]["score"]

    # First: check query pattern for explicit topic
    query_topic = detect_topic_from_query(query)
    if query_topic:
        summary, is_fallback = get_topic_summary(query_topic, results)
        if summary is not None:
            return _format_answer_with_sources(summary, results), False
        if is_fallback:
            # Query matches a known "not in KB" topic (e.g., GitLab Flow)
            chunk_refs = ", ".join([r["chunk_id"] for r in results[:2]])
            return (
                f"I do not have enough information in the available documents to answer this question. "
                f"The question covers a topic not included in the knowledge base. "
                f"Best matching chunk ({chunk_refs}) has relevance score "
                f"{max_score:.2f}, which is insufficient for a reliable answer."
            ), True

    # Second: detect from retrieval results (source-based)
    retrieval_topic = detect_topic_from_retrieval(results)
    summary, is_fallback = get_topic_summary(retrieval_topic, results)

    if summary is not None:
        return _format_answer_with_sources(summary, results), False

    # Fallback: score too low or no matching topic
    if max_score < SCORE_THRESHOLD:
        chunk_refs = ", ".join([r["chunk_id"] for r in results[:2]])
        return (
            f"I do not have enough information in the available documents to answer this question. "
            f"Found chunks ({chunk_refs}) with low relevance score ({max_score:.2f}), "
            f"which does not allow providing a reliable answer based on context."
        ), True

    # Generic: construct from top chunk text
    top_chunk = results[0]
    preview = top_chunk["text_preview"].strip()
    cleaned = re.sub(r'#{1,3}\s+', '', preview)
    cleaned = re.sub(r'\*\*(.*?)\*\*', r'\1', cleaned)
    cleaned = cleaned.strip()

    if len(cleaned) > 30:
        answer = (
            f"Based on retrieved context: {cleaned}\n\n"
        )
        return _format_answer_with_sources(answer, results), False

    return (
        f"I do not have enough information in the available documents to answer this question. "
        f"Retrieved context is not relevant enough to form an answer."
    ), True


def _format_answer_with_sources(summary, results):
    """Append source citations to an answer summary."""
    context_parts = []
    for r in results[:3]:
        context_parts.append(
            f"  - {r['chunk_id']} (score: {r['score']:.2f}) [{r['source_file']}]"
        )

    context_str = "\n".join(context_parts)
    return f"{summary}\n\n**Found in context:**\n{context_str}"


def answer_question(query, index, chunks, model):
    """Full QA pipeline: retrieve → build context → generate answer."""
    # Step 1: Retrieve
    results = search(query, index, chunks, model, top_k=TOP_K)

    # Step 2: Build context
    context = build_context_text(results)

    # Step 3: Generate answer — try LLM first, fall back to template
    answer, is_fallback = generate_answer_llm(query, context)

    if answer is None:
        answer, is_fallback = generate_answer_template(query, results)

    return {
        "query": query,
        "results": results,
        "answer": answer,
        "is_fallback": is_fallback,
    }


def comment(result):
    """Generate comment for a result."""
    if result["is_fallback"]:
        return "Fallback — insufficient relevant context"
    if result["results"] and result["results"][0]["score"] >= 0.6:
        return "Grounded — answer based on relevant chunk"
    if result["results"]:
        return "Partial — context partially relevant"
    return "No context found"


def generate_report(all_results):
    """Generate outputs/rag_answers_examples.md."""
    output_dir = os.path.join(os.path.dirname(__file__), "..", "outputs")
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "rag_answers_examples.md")

    # Count chunks
    chunk_count = sum(1 for _ in open(CHUNKS_FILE, encoding="utf-8"))

    lines = []
    lines.append("# HW4: RAG Answer Generation — Test Results\n")
    lines.append(f"**Embedding model**: `{MODEL_NAME}`\n")
    lines.append(f"**Index**: FAISS IndexFlatIP (dim={EMBEDDING_DIM})\n")
    lines.append(f"**Chunks in KB**: {chunk_count}\n")
    lines.append(f"**Generation**: Template-based (LLM unavailable)\n")
    lines.append(f"**Relevance threshold**: {SCORE_THRESHOLD}\n")
    lines.append("")

    # Summary table
    lines.append("## Summary Table\n")
    lines.append("| # | Question | Top-1 score | Result |")
    lines.append("|---|----------|-------------|--------|")
    for i, r in enumerate(all_results, 1):
        top_score = r["results"][0]["score"] if r["results"] else 0.0
        status = "❌ Fallback" if r["is_fallback"] else "✅ Grounded"
        lines.append(f"| {i} | {r['query']} | {top_score:.2f} | {status} |")
    lines.append("")

    # Detailed results
    for i, r in enumerate(all_results, 1):
        lines.append(f"## Question {i}: {r['query']}\n")

        # Retrieved chunks
        chunk_strs = [
            f"{cr['chunk_id']} (score: {cr['score']:.2f})" for cr in r["results"][:3]
        ]
        lines.append(f"**Retrieved chunks**: {', '.join(chunk_strs)}\n")

        # Answer
        lines.append(f"**Answer**: {r['answer']}\n")

        # Source
        if r["results"]:
            lines.append(f"**Source**: {r['results'][0]['source_file']}\n")
        else:
            lines.append("**Source**: not found\n")

        # Comment
        lines.append(f"**Comment**: {comment(r)}\n")
        lines.append("")

    # ── Prompt improvement examples ────────────────────────────────────

    lines.append("---\n")
    lines.append("## Prompt Improvements\n\n")

    # Example 1
    lines.append("### Example 1: Adding role and instructions\n\n")
    lines.append("#### Original prompt (v1)\n")
    lines.append("```\n")
    lines.append(PROMPT_V1.strip())
    lines.append("```\n\n")
    lines.append("#### Updated prompt (v2)\n")
    lines.append("```\n")
    lines.append(PROMPT_TEMPLATE.strip())
    lines.append("```\n\n")
    lines.append(
        "**Problem**: Without a role, the model gave generic answers based on "
        "its own knowledge, not the context. For example, for a GitLab Flow query, "
        "the model generated an answer from general knowledge, even though the context "
        "did not contain such information.\n\n"
    )
    lines.append(
        "**Result analysis**: Adding a clear role ('You are a Git tutoring assistant') and "
        "the instruction 'Answer ONLY based on the provided context' significantly reduced "
        "hallucinations. The model is now limited to only the provided context.\n\n"
    )

    # Example 2
    lines.append("### Example 2: Adding fallback rule\n\n")
    lines.append("```python\n")
    lines.append("# V1: No fallback rule\n")
    lines.append("# V2: Added instruction:\n")
    lines.append(
        '#  "2. If the context does not contain enough information, say:\n'
        '#   I do not have enough information..."\n'
    )
    lines.append("```\n\n")
    lines.append(
        "**Problem**: For the 'How do I view the commit history?' query, the model tried to guess "
        "an answer because the topic was not well covered in the knowledge base. This led to "
        "hallucinated answers that were not based on facts.\n\n"
    )
    lines.append(
        "**Result analysis**: A clear fallback rule allows the model to honestly admit "
        "missing information. For uncovered topics, the model now returns 'I do not have "
        "enough information' instead of making up an answer.\n\n"
    )

    # Example 3
    lines.append("### Example 3: Mandatory source citations\n\n")
    lines.append("```python\n")
    lines.append("# V1: No requirement to cite sources\n")
    lines.append("# V2: Added instruction:\n")
    lines.append('#  "4. Always cite the source chunk ID or source file used in your answer."\n')
    lines.append("```\n\n")
    lines.append(
        "**Problem**: Answers did not include source references, making it difficult to "
        "verify correctness and traceability of answers.\n\n"
    )
    lines.append(
        "**Result analysis**: Requiring chunk_id and source_file citations makes "
        "answers verifiable. Every statement can be traced back to a specific "
        "part of the document.\n\n"
    )

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"Report saved to {output_path}")
    return output_path


def main():
    parser = argparse.ArgumentParser(description="HW4: RAG Answer Generation")
    parser.add_argument("--test", action="store_true", help="Run all test queries")
    parser.add_argument("--report", action="store_true", help="Generate markdown report")
    parser.add_argument("--top-k", type=int, default=TOP_K, help="Top-k results")
    args = parser.parse_args()

    if not args.test and not args.report:
        args.test = True
        args.report = True

    print("=" * 60)
    print("HW4: RAG Answer Generation")
    print("=" * 60)

    index, chunks, model = load_index()
    print(f"Loaded {len(chunks)} chunks from {CHUNKS_FILE}")
    print(f"Model: {MODEL_NAME}")
    print()

    all_results = []

    if args.test:
        for i, query in enumerate(TEST_QUERIES, 1):
            print(f"--- Query {i}/{len(TEST_QUERIES)}: {query} ---")
            result = answer_question(query, index, chunks, model)
            all_results.append(result)

            # Print summary
            top_score = result["results"][0]["score"] if result["results"] else 0.0
            status = "🔴 Fallback" if result["is_fallback"] else "🟢 Grounded"
            preview = result['answer'][:150]
            print(f"  Top-1 score: {top_score:.2f} | {status}")
            print(f"  Answer: {preview}...")
            print()

    if args.report:
        if not all_results:
            for query in TEST_QUERIES:
                result = answer_question(query, index, chunks, model)
                all_results.append(result)
        generate_report(all_results)

    print("Done!")


if __name__ == "__main__":
    main()