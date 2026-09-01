#!/usr/bin/env python3
"""
Final — A/B(/C) embedding benchmark on OUR real data.

  KB:      data/processed/chunks.jsonl (145 chunks, 7 GitLab docs — the same
           collection used in HW2/HW3 retrieval work).
  Queries: TEST_QUERIES from scripts/retrieval.py (the 10 queries from HW2).
  Models:
    A = all-MiniLM-L6-v2   (384d) — what HW2/HW3 used (production)
    B = bge-small-en-v1.5  (384d) — technical-domain candidate, drop-in
    C = nomic-embed-text   (768d) — strong tech model, different dimension
               (NOT drop-in: FAISS index size changes).

For every query we compare top-1/top-3 chunk ids + cosine scores and the
top1-top2 margin (how clearly the model separates the best from runner-up).
Cosine scores are NOT comparable ACROSS models (each model has its own
embedding-space calibration) — read the ranking/chunk choice, not the raw
number.

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

# name -> (huggingface id, dim, query_prefix or None, doc_prefix or None)
# nomic-embed-text is instruction-tuned: it expects a specific query prefix.
MODELS = {
    "A": ("sentence-transformers/all-MiniLM-L6-v2", 384, None, None),
    "B": ("BAAI/bge-small-en-v1.5", 384, None, None),
    "C": ("nomic-ai/nomic-embed-text-v1.5", 768,
          "Represent this sentence for searching relevant passages: ", None),
}

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


def embed(model, texts, prefix=None, batch_size=32):
    if prefix:
        texts = [prefix + t for t in texts]
    vecs = []
    for i in range(0, len(texts), batch_size):
        vecs.append(model.encode(texts[i:i + batch_size],
                                 normalize_embeddings=True,
                                 show_progress_bar=False))
    return np.vstack(vecs)


def topk(qvec, mat, k=3):
    sims = mat @ qvec  # both normalized => cosine
    order = np.argsort(-sims)[:k]
    return [int(i) for i in order], [float(sims[i]) for i in order]


def chunk_label(chunk):
    return chunk.get("chunk_id", "?")


def main():
    from sentence_transformers import SentenceTransformer
    chunks = load_chunks()
    texts = [c["text"] for c in chunks]
    print(f"KB: {len(chunks)} chunks")

    # per-model index matrices + timings
    mats, qmats, timings = {}, {}, {}
    for name, (model_name, dim, qpre, dpre) in MODELS.items():
        t0 = time.time()
        model = SentenceTransformer(model_name, device="cpu")
        timings[name + "_load_s"] = round(time.time() - t0, 1)
        t0 = time.time()
        mats[name] = embed(model, texts, prefix=dpre)
        timings[name + "_index_s"] = round(time.time() - t0, 1)
        qmats[name] = embed(model, TEST_QUERIES, prefix=qpre)
        got_dim = mats[name].shape[1]
        print(f"[{name}] {model_name}: indexed {len(texts)} chunks "
              f"({got_dim}d, {timings[name + '_index_s']}s)")
        del model

    names = list(MODELS.keys())
    by_q = {}
    for qi, q in enumerate(TEST_QUERIES):
        by_q[qi] = {}
        for name in names:
            ids, sc = topk(qmats[name][qi], mats[name])
            by_q[qi][name] = {
                "top1_id": ids[0], "top1_score": sc[0],
                "top2_id": ids[1], "top2_score": sc[1],
                "top3_id": ids[2], "top3_score": sc[2],
                "margin": sc[0] - sc[1],
            }

    # CSV
    with open(OUT_CSV, "w", encoding="utf-8") as f:
        f.write("model,model_name,query,top1_id,top1_score,"
                "top2_id,top2_score,top3_id,top3_score,margin\n")
        for qi, q in enumerate(TEST_QUERIES):
            for name in names:
                r = by_q[qi][name]
                f.write(",".join([
                    name, MODELS[name][0], q,
                    str(r["top1_id"]), f"{r['top1_score']:.4f}",
                    str(r["top2_id"]), f"{r['top2_score']:.4f}",
                    str(r["top3_id"]), f"{r['top3_score']:.4f}",
                    f"{r['margin']:.4f}"]) + "\n")

    # Report
    md = ["# A/B(/C) Embedding Benchmark — real KB data (Final branch)", "",
          "## Setup", "",
          f"- KB: `{len(chunks)} chunks`, 7 GitLab docs (the HW2/HW3 "
          "collection)",
          "- Queries: the 10 test queries from `scripts/retrieval.py` "
          "(HW2 set)",
          f"- A: `{MODELS['A'][0]}` ({MODELS['A'][1]}d) — production model "
          "from HW2/HW3",
          f"- B: `{MODELS['B'][0]}` ({MODELS['B'][1]}d) — technical-domain "
          "candidate, drop-in (same dimension)",
          f"- C: `{MODELS['C'][0]}` ({MODELS['C'][1]}d) — strong tech "
          "model, instruction-tuned (query prefix applied), NOT drop-in "
          "(index size changes)",
          "- Cosine on normalized vectors, CPU, deterministic. "
          "**Cosine values are not comparable across models** (each model "
          "has its own space calibration) — read the top-1 chunk choice, "
          "not the raw number.", ""]

    # Top-1 retrieval per query (one column per model)
    header = "| # | Query |"
    sep = "|---|---|"
    for name in names:
        header += f" {name} top-1 (score) |"
        sep += "----|"
    md += ["## Top-1 retrieval per query", "", header, sep]
    for qi, q in enumerate(TEST_QUERIES):
        row = f"| {qi + 1} | {q} |"
        for name in names:
            r = by_q[qi][name]
            row += (f" `{chunk_label(chunks[r['top1_id']])}` "
                    f"({r['top1_score']:.3f}) |")
        md.append(row)
    md += ["",
           "## Score separation (top-1 score, margin top1-top2)", "",
           "| # | Query |" + "".join(f" {n} top-1 | {n} margin |" for n in names),
           "|---|---|" + "----|" * (2 * len(names))]
    for qi, q in enumerate(TEST_QUERIES):
        row = f"| {qi + 1} | {q} |"
        for name in names:
            r = by_q[qi][name]
            row += f" {r['top1_score']:.3f} | {r['margin']:.3f} |"
        md.append(row)

    md += ["", "## Aggregates", ""]
    # pairwise top-1 agreement
    for i, a in enumerate(names):
        for b in names[i + 1:]:
            agree = sum(1 for qi in range(len(TEST_QUERIES))
                        if by_q[qi][a]["top1_id"] == by_q[qi][b]["top1_id"])
            md.append(f"- Top-1 agreement {a} vs {b}: "
                      f"**{agree}/{len(TEST_QUERIES)}**")
    for name in names:
        sc = [by_q[qi][name]["top1_score"] for qi in range(len(TEST_QUERIES))]
        mg = [by_q[qi][name]["margin"] for qi in range(len(TEST_QUERIES))]
        md.append(f"- Mean top-1 cosine {name}: **{np.mean(sc):.4f}** | "
                  f"mean margin {name}: **{np.mean(mg):.4f}** "
                  f"(bigger margin = clearer winner vs runner-up)")
    md.append("- Timing (index build / model load): "
              + "; ".join(f"{n} {timings[n+'_index_s']}s / "
                          f"{timings[n+'_load_s']}s" for n in names))
    md.append("")

    with open(OUT_MD, "w", encoding="utf-8") as f:
        f.write("\n".join(md))
    print(f"report -> {OUT_MD}")
    print(f"csv    -> {OUT_CSV}")


if __name__ == "__main__":
    main()