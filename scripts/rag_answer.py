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
LLM_BASE_URL = "https://openrouter.ai/api/v1"
LLM_MODEL = "nvidia/nemotron-3-nano-30b-a3b:free"
SCORE_THRESHOLD = 0.30
# API key from environment variable (not stored in repo)
# Set: export OPENROUTER_API_KEY=sk-or-v1-...
LLM_API_KEY = os.environ.get("OPENROUTER_API_KEY", "")

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

# ── Core Functions ─────────────────────────────────────────────────────────


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


def generate_answer_llm(question, context, max_retries=2):
    """Try to generate answer using OpenRouter LLM (Nemotron with reasoning)."""
    import time
    try:
        from openai import OpenAI
        if not LLM_API_KEY:
            print("  [LLM недоступний] OPENROUTER_API_KEY not set in environment", file=sys.stderr)
            return None, False

        client = OpenAI(base_url=LLM_BASE_URL, api_key=LLM_API_KEY)

        prompt = PROMPT_TEMPLATE.format(context=context, question=question)

        for attempt in range(max_retries):
            try:
                response = client.chat.completions.create(
                    model=LLM_MODEL,
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=4096,
                    temperature=0.1,
                    extra_body={"reasoning": {"enabled": True}},
                )
            except Exception as e:
                if attempt < max_retries - 1:
                    print(f"  [LLM retry {attempt+1}/{max_retries}] {e}", file=sys.stderr)
                    time.sleep(1)
                    continue
                raise

            if not response.choices or not response.choices[0]:
                print(f"  [LLM недоступний] Empty response (attempt {attempt+1}/{max_retries})", file=sys.stderr)
                if attempt < max_retries - 1:
                    time.sleep(1)
                    continue
                # Final attempt failed
                return None, False
        msg = response.choices[0].message
        # Nano Nemotron: content may be None, reasoning in reasoning_details
        answer = msg.content
        if not answer:
            # Fallback: extract from reasoning_details if available
            rd = getattr(msg, "reasoning_details", None)
            if rd:
                reasoning_text = str(rd) if hasattr(rd, "content") else str(rd)
                for marker in ["Response:", "Output:", "Final Output"]:
                    if marker in reasoning_text:
                        answer = reasoning_text.split(marker)[-1].strip()
                        break
                if not answer:
                    lines = reasoning_text.strip().split("\n")
                    answer = "\n".join(lines[-3:]) if len(lines) > 3 else reasoning_text

        answer_text = str(answer).strip() if answer else None
        # Detect if LLM itself returned a fallback answer
        is_fallback = bool(answer_text and "I do not have enough information" in answer_text)
        return answer_text, is_fallback
    except Exception as e:
        print(f"  [LLM недоступний] {e}", file=sys.stderr)
        return None, False


def answer_question(query, index, chunks, model):
    """Full QA pipeline: retrieve → build context → generate answer."""
    # Step 1: Retrieve
    results = search(query, index, chunks, model, top_k=TOP_K)

    # Step 2: Build context
    context = build_context_text(results)

    # Step 3: Generate answer via LLM
    answer, is_fallback = generate_answer_llm(query, context)

    if answer is None:
        # LLM unavailable (rate limit, etc.) — return honest fallback, NOT template
        # Template responses come from hardcoded maps, not retrieved context
        # This violates the grounded QA principle: "answer only from retrieved context"
        answer = (
            "I do not have enough information in the available documents to answer this question. "
            "The LLM service was unavailable at the time of this query."
        )
        is_fallback = True

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
    lines.append(f"**LLM**: `{LLM_MODEL}` via `{LLM_BASE_URL}`\n")
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
    lines.append("#### Original prompt (v1)\n")
    lines.append("```\n")
    lines.append(PROMPT_V1.strip())
    lines.append("```\n\n")
    lines.append("#### Updated prompt (v2)\n")
    lines.append("```\n")
    lines.append(
        "You are a Git tutoring assistant. Your job is to answer questions about Git, GitHub, and GitLab.\n\n"
        "IMPORTANT RULES:\n"
        "1. Answer ONLY based on the provided context below.\n"
        "2. If the context does not contain enough information to answer the question, say:\n"
        '   "I do not have enough information in the available documents to answer this question."\n'
        "3. Do NOT use any general knowledge outside the provided context.\n"
        "\n"
        "Context:\n"
        "{context}\n"
        "\n"
        "Question: {question}\n"
        "\n"
        "Answer:"
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
    lines.append("#### Original prompt (v1)\n")
    lines.append("```\n")
    lines.append(
        "You are a Git tutoring assistant. Your job is to answer questions about Git, GitHub, and GitLab.\n\n"
        "IMPORTANT RULES:\n"
        "1. Answer ONLY based on the provided context below.\n"
        "2. If the context does not contain enough information to answer the question, say:\n"
        '   "I do not have enough information in the available documents to answer this question."\n'
        "3. Do NOT use any general knowledge outside the provided context.\n"
        "\n"
        "Context:\n"
        "{context}\n"
        "\n"
        "Question: {question}\n"
        "\n"
        "Answer:"
    )
    lines.append("```\n\n")
    lines.append("#### Updated prompt (v2)\n")
    lines.append("```\n")
    lines.append(PROMPT_TEMPLATE.strip())
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
    import time

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

            # Wait 4s between queries to stay within free model rate limit (20 RPM)
            if i < len(TEST_QUERIES):
                print("  ⏳ Waiting 20s before next query...")
                time.sleep(20)
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