#!/usr/bin/env python3
"""
Final — A/B embedding benchmark on OUR real data.

  KB:      data/processed/chunks.jsonl (145 chunks, 7 GitLab docs — the same
           collection used in HW2/HW3 retrieval work).
  Queries: TEST_QUERIES from scripts/retrieval.py (the 10 queries from HW2).
  Models:  A = all-MiniLM-L6-v2  (384d) — what HW2/HW3 used
           B = bge-small-en-v1.5 (384d) — technical-domain candidate,
               same dimensionality => drop-in, index rebuild only.

For every query we compare:
  - top-1 / top-3 chunk ids + cosine scores (retrieval agreement)
  - score margins (does the model separate relevant vs irrelevant better?)

Outputs:
  outputs/embedding_ab.md    — report
  outputs/embedding_ab.csv   — per-query, per-model rows

Deterministic: batch embeddings, fixed seed, CPU.
"""
import json
import os
import time

import numpy as np

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHUNKS_FILE = os.path.join(REPO, "data/processed/chunks.jsonl")
OUT_MD = os.path.join(REPO, "outputs/embedding_ab.md")
OUT_CSV = os.path.join(REPO, "outputs/embedding_ab.csv")

MODEL_A = "sentence-transformers/all-MiniLM-L6-v2"
MODEL_B = "BAAI/bge-small-en-v1.5"

# Same 10 queries as scripts/retrieval.py (HW2 test set).
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
    chunks = []
    with open(CHUNKS_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                chunks.append(json.loads(line))
    return chunks


def embed(model, texts, batch_size=32):
    vecs = []
    for i in range(0, len(texts), batch_size):
        vecs.append(model.encode(texts[i:i + batch_size],
                                 normalize_embeddings=True,
                                 show_progress_bar=False))
    return np.vstack(vecs)


def topk(qvec, mat, ids, k=3):
    sims = mat @ qvec  # both normalized => cosine
    order = np.argsort(-sims)[:k]
    return [(ids[i], float(sims[i])) for i in order]


def chunk_label(chunk):
    return chunk.get("chunk_id", "?")


def main():
    chunks = load_chunks()
    texts = [c["text"] for c in chunks]
    print(f"KB: {len(chunks)} chunks")

    rows = []
    timings = {}
    for name, model_name in (("A", MODEL_A), ("B", MODEL_B)):
        t0 = time.time()
        from sentence_transformers import SentenceTransformer
        model = SentenceTransformer(model_name, device="cpu")
        timings[name + "_load_s"] = round(time.time() - t0, 1)
        t0 = time.time()
        mat = embed(model, texts)
        timings[name + "_index_s"] = round(time.time() - t0, 1)
        print(f"[{name}] {model_name}: indexed {len(texts)} chunks "
              f"({timings[name + '_index_s']}s)")
        qvecs = embed(model, TEST_QUERIES)
        for qi, q in enumerate(TEST_QUERIES):
            top = topk(qvecs[qi], mat, list(range(len(chunks))))
            rows.append({
                "model": name,
                "model_name": model_name,
                "query": q,
                "top1_id": top[0][0],
                "top1_score": f"{top[0][1]:.4f}",
                "top2_id": top[1][0],
                "top2_score": f"{top[1][1]:.4f}",
                "top3_id": top[2][0],
                "top3_score": f"{top[2][1]:.4f}",
                "margin": f"{top[0][1] - top[1][1]:.4f}",
            })

    # CSV
    with open(OUT_CSV, "w", encoding="utf-8") as f:
        f.write("model,model_name,query,top1_id,top1_score,"
                "top2_id,top2_score,top3_id,top3_score,margin\n")
        for r in rows:
            f.write(",".join(str(r[k]) for k in (
                "model", "model_name", "query", "top1_id", "top1_score",
                "top2_id", "top2_score", "top3_id", "top3_score",
                "margin")) + "\n")

    # Report
    by_q = {}
    for r in rows:
        by_q.setdefault(r["query"], {})[r["model"]] = r
    agree = sum(1 for q in by_q
                if by_q[q]["A"]["top1_id"] == by_q[q]["B"]["top1_id"])
    md = ["# A/B Embedding Benchmark — real KB data (Final branch)", "",
          "## Setup", "",
          f"- KB: `{len(chunks)} chunks`, 7 GitLab docs (the HW2/HW3 collection)",
          f"- Queries: the 10 test queries from `scripts/retrieval.py` (HW2 set)",
          f"- A: `{MODEL_A}` (384d) — production model from HW2/HW3",
          f"- B: `{MODEL_B}` (384d) — technical-domain candidate, "
          "drop-in (same dimension)",
          f"- Cosine on normalized vectors, CPU, deterministic", "",
          "## Top-1 retrieval per query", "",
          "| # | Query | A top-1 (score) | B top-1 (score) | Same? |",
          "|---|---|---|---|---|"]
    for qi, q in enumerate(TEST_QUERIES, 1):
        a = by_q[q]["A"]
        b = by_q[q]["B"]
        same = "yes" if a["top1_id"] == b["top1_id"] else "**no**"
        md.append(f"| {qi} | {q} | `{chunk_label(chunks[a['top1_id']])}` "
                  f"({a['top1_score']}) | `{chunk_label(chunks[b['top1_id']])}` "
                  f"({b['top1_score']}) | {same} |")
    md += ["",
           "## Score separation (top1 score, margin top1-top2)", "",
           "| # | Query | A top-1 | A margin | B top-1 | B margin |",
           "|---|---|---|---|---|---|"]
    for qi, q in enumerate(TEST_QUERIES, 1):
        a = by_q[q]["A"]
        b = by_q[q]["B"]
        md.append(f"| {qi} | {q} | {a['top1_score']} | {a['margin']} "
                  f"| {b['top1_score']} | {b['margin']} |")
    a_scores = [float(by_q[q]["A"]["top1_score"]) for q in TEST_QUERIES]
    b_scores = [float(by_q[q]["B"]["top1_score"]) for q in TEST_QUERIES]
    a_margins = [float(by_q[q]["A"]["margin"]) for q in TEST_QUERIES]
    b_margins = [float(by_q[q]["B"]["margin"]) for q in TEST_QUERIES]
    md += ["", "## Aggregates", "",
           f"- Top-1 agreement A vs B: **{agree}/{len(TEST_QUERIES)}**",
           f"- Mean top-1 cosine — A: **{np.mean(a_scores):.4f}**, "
           f"B: **{np.mean(b_scores):.4f}**",
           f"- Mean margin (top1-top2) — A: **{np.mean(a_margins):.4f}**, "
           f"B: **{np.mean(b_margins):.4f}** (bigger = clearer winner vs "
           f"runner-up)",
           f"- Timing: index build A {timings['A_index_s']}s / B "
           f"{timings['B_index_s']}s; model load A "
           f"{timings['A_load_s']}s / B {timings['B_load_s']}s",
           ""]
    with open(OUT_MD, "w", encoding="utf-8") as f:
        f.write("\n".join(md))
    print(f"report -> {OUT_MD}")
    print(f"csv    -> {OUT_CSV}")
    print(f"top-1 agreement: {agree}/{len(TEST_QUERIES)}")
    print(f"mean top1 A={np.mean(a_scores):.4f} B={np.mean(b_scores):.4f}")


if __name__ == "__main__":
    main()