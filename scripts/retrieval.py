#!/usr/bin/env python3
"""
HW2: Semantic Retrieval Layer

Pipeline: chunks.jsonl → embeddings → FAISS index → top-k semantic search → retrieved chunks

Usage:
    python3 scripts/retrieval.py --rebuild          # Build index from scratch
    python3 scripts/retrieval.py --query "..."      # Search a single query
    python3 scripts/retrieval.py --test              # Run all test queries
    python3 scripts/retrieval.py --report            # Generate outputs/retrieval_examples.md
"""

import argparse
import json
import os
import pickle
import sys

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# ── Configuration ──────────────────────────────────────────────────────────
CHUNKS_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "processed", "chunks.jsonl")
INDEX_DIR = os.path.join(os.path.dirname(__file__), "..", "index")
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
EMBEDDING_DIM = 384  # all-MiniLM-L6-v2 output dimension
TOP_K = 5

# ── Test Queries ──────────────────────────────────────────────────────────
TEST_QUERIES = [
    "How do I clone a Git repository?",
    "What is a Git branch and how do I create one?",
    "How to resolve merge conflicts in Git?",
    "What is the difference between git add and git commit?",
    "How do I stash my changes temporarily?",
    "How do I merge a branch in GitLab?",
    "How do I view the commit history?",
    "How to set up SSH keys for GitLab?",
    "What is rebasing and when should I use it?",
    "How do I push changes to a remote repository?",
]


def load_chunks():
    """Load chunks from JSONL file."""
    chunks = []
    with open(CHUNKS_FILE, "r", encoding="utf-8") as f:
        for line in f:
            chunks.append(json.loads(line))
    return chunks


def build_index(chunks):
    """Build FAISS index + store chunk metadata."""
    os.makedirs(INDEX_DIR, exist_ok=True)

    model = SentenceTransformer(MODEL_NAME)

    # Extract texts and encode
    texts = [c["text"] for c in chunks]
    embeddings = model.encode(texts, show_progress_bar=True, normalize_embeddings=True)
    embeddings = np.array(embeddings, dtype="float32")

    # Build FAISS index (Inner Product for cosine similarity on normalized vectors)
    index = faiss.IndexFlatIP(EMBEDDING_DIM)
    index.add(embeddings)

    # Save index + metadata
    index_path = os.path.join(INDEX_DIR, "faiss.index")
    meta_path = os.path.join(INDEX_DIR, "metadata.pkl")

    faiss.write_index(index, index_path)
    with open(meta_path, "wb") as f:
        pickle.dump({
            "chunks": chunks,
            "model": MODEL_NAME,
            "embedding_dim": EMBEDDING_DIM,
            "chunk_count": len(chunks),
        }, f)

    return index, chunks, model


def load_index():
    """Load FAISS index + metadata."""
    index_path = os.path.join(INDEX_DIR, "faiss.index")
    meta_path = os.path.join(INDEX_DIR, "metadata.pkl")

    if not os.path.exists(index_path):
        print("ERROR: Index not found. Run with --rebuild first.", file=sys.stderr)
        sys.exit(1)

    index = faiss.read_index(index_path)
    with open(meta_path, "rb") as f:
        meta = pickle.load(f)

    model = SentenceTransformer(MODEL_NAME)
    return index, meta["chunks"], model


def search(query, index, chunks, model, top_k=TOP_K):
    """Search for top-k chunks by semantic similarity."""
    # Encode query (same model as chunks)
    query_embedding = model.encode([query], normalize_embeddings=True)
    query_embedding = np.array(query_embedding, dtype="float32")

    # Search
    k = min(top_k, index.ntotal)
    scores, ids = index.search(query_embedding, k)

    results = []
    for score, idx in zip(scores[0], ids[0]):
        if idx >= 0:  # valid index
            chunk = chunks[idx]
            results.append({
                "chunk_id": chunk["chunk_id"],
                "score": round(float(score), 4),
                "text_preview": chunk["text"][:200],
                "source_file": chunk["metadata"]["source_file"],
                "document_id": chunk["metadata"]["document_id"],
                "domain": chunk["metadata"]["domain"],
                "section": chunk["metadata"]["section"],
            })

    return results


def format_result(result, rank):
    """Format a single search result — HW2 spec format."""
    text_preview = result["text_preview"].strip()
    # Clean up repr-style quotes and newlines
    text_preview = text_preview.replace("\n", " ")
    return (
        f"Top-{rank}: {result['chunk_id']} | score: {result['score']:.2f}\n"
        f"  Text: {text_preview}\n"
        f"  Source: {result['source_file']}\n"
    )


def run_test_queries():
    """Run all test queries and print results."""
    print("=" * 70)
    print("HW2: Semantic Retrieval — Test Queries")
    print("=" * 70)

    index, chunks, model = load_index()
    print(f"\nLoaded {len(chunks)} chunks from {CHUNKS_FILE}")
    print(f"Model: {MODEL_NAME}\n")

    results_by_query = []

    for i, query in enumerate(TEST_QUERIES, 1):
        results = search(query, index, chunks, model)

        print(f"--- Query {i}/{len(TEST_QUERIES)} ---")
        print(f"Query: {query}")
        print()

        for j, result in enumerate(results, 1):
            print(format_result(result, j))
            print()

        results_by_query.append({
            "query": query,
            "results": results,
        })

    return results_by_query


def generate_report(results_by_query=None):
    """Generate outputs/retrieval_examples.md from test queries — HW2 spec format."""
    if results_by_query is None:
        results_by_query = run_test_queries()

    output_dir = os.path.join(os.path.dirname(__file__), "..", "outputs")
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "retrieval_examples.md")

    # Comments for each query
    COMMENTS = [
        "Relevant — Top-1 and Top-2 correctly point to git clone documentation. All top results from git_basics_getting_repository.",
        "Not relevant — Top-1 returns gitlab_getting_started_chunk_002 (general GitLab intro) instead of branch-specific content. Semantic model matches Git broadly but misses branch specificity.",
        "Relevant — Top-1 correctly returns the merge conflict resolution section. Score 0.74 confirms strong semantic match.",
        "Partially relevant — Top-1 points to GitHub About Git which covers both commands, but not the specific difference. A more targeted chunk would be preferable.",
        "Relevant — Top-1 correctly returns the stashing section. Score 0.62 is moderate but the result is accurate.",
        "Relevant — Top-1 returns GitLab Getting Started content. Score 0.74 is strong. Covers the GitLab merge workflow.",
        "Partially relevant — Top-1 returns GitHub About Git intro instead of git log specifics. Score 0.57 is low — semantic model does not distinguish view history from general Git concepts.",
        "Relevant — Top-1 correctly returns GitLab Getting Started covering SSH key setup. Score 0.74 is strong.",
        "Partially relevant — Top-1 returns git_tools_rebasing_chunk_000 but with score 0.50, which is borderline. The chunk is correct but the low score suggests semantic distance from the query phrasing.",
        "Relevant — Top-1 returns distributed_workflows_chunk_005 with score 0.72. Covers git push and remote repository operations correctly.",
    ]

    lines = []
    lines.append("# HW2: Semantic Retrieval — Test Results\n")
    lines.append(f"**Model**: {MODEL_NAME}\n")
    lines.append(f"**Chunks**: {len(load_chunks())}\n")
    lines.append(f"**Index**: FAISS (IndexFlatIP, dim={EMBEDDING_DIM})\n")
    lines.append(f"**Top-k**: {TOP_K}\n")
    lines.append("")

    for i, entry in enumerate(results_by_query, 1):
        lines.append(f"Query: {entry['query']}\n")
        for j, result in enumerate(entry["results"], 1):
            text_preview = result["text_preview"].strip().replace("\n", " ")
            lines.append(f"Top-{j}: {result['chunk_id']} | score: {result['score']:.2f}")
            lines.append(f"  Text: {text_preview}")
            lines.append(f"  Source: {result['source_file']}")
            lines.append("")

        comment = COMMENTS[i - 1] if i - 1 < len(COMMENTS) else "No comment available."
        lines.append(f"Comment: {comment}\n")
        lines.append("---\n")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"\nReport saved to {output_path}")
    return output_path


def main():
    parser = argparse.ArgumentParser(description="HW2: Semantic Retrieval")
    parser.add_argument("--rebuild", action="store_true",
                        help="Build index from scratch")
    parser.add_argument("--query", type=str, default=None,
                        help="Search a single query")
    parser.add_argument("--test", action="store_true",
                        help="Run all test queries")
    parser.add_argument("--report", action="store_true",
                        help="Generate retrieval_examples.md report")
    parser.add_argument("--top-k", type=int, default=TOP_K,
                        help="Number of results to return (default: 5)")
    args = parser.parse_args()

    if not args.rebuild and not args.query and not args.test and not args.report:
        parser.print_help()
        sys.exit(1)

    if args.rebuild:
        print(f"Building index with model: {MODEL_NAME}")
        chunks = load_chunks()
        print(f"Loaded {len(chunks)} chunks")
        index, chunks, model = build_index(chunks)
        print(f"Index saved to {INDEX_DIR}/")
        print(f"Total chunks indexed: {index.ntotal}")
        # Run test queries and generate report after rebuild
        results_by_query = run_test_queries()
        generate_report(results_by_query)

    if args.query:
        index, chunks, model = load_index()
        results = search(args.query, index, chunks, model, top_k=args.top_k)
        print(f"Query: {args.query}\n")
        for j, result in enumerate(results, 1):
            print(format_result(result, j))
            print()

    if args.test:
        run_test_queries()

    if args.report:
        index, chunks, model = load_index()
        results_by_query = []
        for query in TEST_QUERIES:
            results = search(query, index, chunks, model)
            results_by_query.append({"query": query, "results": results})
        generate_report(results_by_query)


if __name__ == "__main__":
    main()