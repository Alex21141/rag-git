#!/usr/bin/env python3
"""Alpha sweep: find optimal alpha for BM25 + Semantic hybrid search."""
import argparse, json, os, re, sys
import faiss, numpy as np
from rank_bm25 import BM25Okapi
from sentence_transformers import SentenceTransformer

CHUNKS_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "processed", "chunks.jsonl")
INDEX_DIR = os.path.join(os.path.dirname(__file__), "..", "index")
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "outputs")
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

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

ALPHA_VALUES = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]


def load_chunks():
    chunks = []
    with open(CHUNKS_FILE) as f:
        for line in f:
            chunks.append(json.loads(line))
    return chunks


def load_index():
    import pickle
    index = faiss.read_index(os.path.join(INDEX_DIR, "faiss.index"))
    with open(os.path.join(INDEX_DIR, "metadata.pkl"), "rb") as f:
        meta = pickle.load(f)
    model = SentenceTransformer(MODEL_NAME)
    return index, meta["chunks"], model


def build_bm25(chunks):
    tokenized = [c["text"].lower().split() for c in chunks]
    return BM25Okapi(tokenized)


def hybrid_search(query, index, chunks, model, bm25, top_k=5, alpha=0.5):
    q_emb = model.encode([query], normalize_embeddings=True)
    q_emb = np.array(q_emb, dtype="float32")
    k = min(top_k * 4, index.ntotal)
    sem_scores, ids = index.search(q_emb, k)

    q_tokens = query.lower().split()
    bm25_scores = np.array([bm25.get_scores(q_tokens)[int(i)] if i >= 0 else 0.0
                            for i in ids[0]])

    max_sem = sem_scores[0].max() if sem_scores[0].max() > 0 else 1.0
    max_bm25 = bm25_scores.max() if bm25_scores.max() > 0 else 1.0
    norm_sem = sem_scores[0] / max_sem
    norm_bm25 = bm25_scores / max_bm25

    hybrid = alpha * norm_sem + (1 - alpha) * norm_bm25

    results = []
    for i in range(len(ids[0])):
        idx = int(ids[0][i])
        if idx < 0:
            break
        chunk = chunks[idx]
        results.append({
            "chunk_id": chunk["chunk_id"],
            "score": round(float(hybrid[i]), 4),
            "semantic_score": round(float(sem_scores[0][i]), 4),
            "bm25_score": round(float(bm25_scores[i]), 4),
            "text_preview": chunk["text"][:200],
        })

    results.sort(key=lambda r: r["score"], reverse=True)
    return results[:top_k]


def generate_alpha_sweep():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_path = os.path.join(OUTPUT_DIR, "alpha_sweep.md")

    index, chunks, model = load_index()
    bm25 = build_bm25(chunks)

    print(f"Loaded {len(chunks)} chunks, testing {len(ALPHA_VALUES)} alpha values\n")

    # For each query + alpha: get top-1 chunk_id and score
    results = {}  # {query: {alpha: {"chunk_id": ..., "score": ..., "sem": ..., "bm25": ...}}}

    for qi, query in enumerate(TEST_QUERIES, 1):
        print(f"Query {qi}/{len(TEST_QUERIES)}")
        results[query] = {}
        for alpha in ALPHA_VALUES:
            top5 = hybrid_search(query, index, chunks, model, bm25, top_k=1, alpha=alpha)
            if top5:
                r = top5[0]
                results[query][alpha] = {
                    "chunk_id": r["chunk_id"],
                    "score": r["score"],
                    "sem": r["semantic_score"],
                    "bm25": r["bm25_score"],
                }
            else:
                results[query][alpha] = {"chunk_id": "N/A", "score": 0, "sem": 0, "bm25": 0}

    # Write report
    lines = [
        "# Alpha Sweep — BM25 + Semantic Hybrid",
        "",
        "**Tested**: α = 0.0 (BM25 only) → 1.0 (Semantic only)",
        "",
        "## Top-1 chunk per alpha",
        "",
    ]

    for query in TEST_QUERIES:
        lines.append(f"### {query}")
        lines.append("")
        lines.append("| α | Top-1 chunk | Hybrid | Semantic | BM25 |")
        lines.append("|---|-------------|--------|----------|------|")
        for alpha in ALPHA_VALUES:
            r = results[query][alpha]
            lines.append(f"| {alpha:.1f} | {r['chunk_id']} | {r['score']:.4f} | {r['sem']:.4f} | {r['bm25']:.4f} |")
        lines.append("")

    # Summary: which alpha gives best avg score
    lines.append("## Summary — Average top-1 score by alpha")
    lines.append("")
    lines.append("| α | Avg Score |")
    lines.append("|---|----------|")
    for alpha in ALPHA_VALUES:
        scores = [results[q][alpha]["score"] for q in TEST_QUERIES]
        avg = sum(scores) / len(scores)
        lines.append(f"| {alpha:.1f} | {avg:.4f} |")
    lines.append("")

    best_alpha = max(ALPHA_VALUES, key=lambda a: sum(results[q][a]["score"] for q in TEST_QUERIES) / len(TEST_QUERIES))
    best_avg = sum(results[q][best_alpha]["score"] for q in TEST_QUERIES) / len(TEST_QUERIES)
    lines.append(f"**Best α = {best_alpha:.1f}** with average score {best_avg:.4f}")
    lines.append("")

    # Compare current (α=0.5) vs best
    current_avg = sum(results[q][0.5]["score"] for q in TEST_QUERIES) / len(TEST_QUERIES)
    lines.append(f"Current α=0.5: avg {current_avg:.4f}")
    if best_alpha != 0.5:
        lines.append(f"Best α={best_alpha:.1f}: avg {best_avg:.4f} (improvement: {best_avg - current_avg:+.4f})")
    else:
        lines.append("α=0.5 is already optimal for this query set")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"\nSaved to {output_path}")


if __name__ == "__main__":
    generate_alpha_sweep()