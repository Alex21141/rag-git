# A/B(/C) Embedding Benchmark — real KB data (Final branch)

## Setup

- KB: `145 chunks`, 7 GitLab docs (the HW2/HW3 collection)
- Queries: the 10 test queries from `scripts/retrieval.py` (HW2 set)
- A: `sentence-transformers/all-MiniLM-L6-v2` (384d) — production model from HW2/HW3
- B: `BAAI/bge-small-en-v1.5` (384d) — technical-domain candidate, drop-in (same dimension)
- C: `nomic-ai/nomic-embed-text-v1.5` (768d) — strong tech model, instruction-tuned (query prefix applied), NOT drop-in (index size changes)
- Cosine on normalized vectors, CPU, deterministic. **Cosine values are not comparable across models** (each model has its own space calibration) — read the top-1 chunk choice, not the raw number.

## Top-1 retrieval per query

| # | Query | A top-1 (score) | B top-1 (score) | C top-1 (score) |
|---|---|----|----|----|
| 1 | How do I clone a Git repository? | `git_basics_getting_repository_chunk_002` (0.709) | `gitlab_getting_started_chunk_006` (0.819) | `git_basics_getting_repository_chunk_006` (0.751) |
| 2 | What is a Git branch and how do I create one? | `gitlab_getting_started_chunk_001` (0.634) | `branching_branch_management_chunk_001` (0.812) | `branching_branch_management_chunk_001` (0.738) |
| 3 | How to resolve merge conflicts in Git? | `gitlab_getting_started_chunk_005` (0.721) | `branching_basic_branching_merging_chunk_014` (0.863) | `gitlab_getting_started_chunk_005` (0.747) |
| 4 | What is the difference between git add and git commit? | `github_about_git_chunk_008` (0.660) | `git_basics_recording_changes_chunk_007` (0.829) | `git_basics_recording_changes_chunk_028` (0.764) |
| 5 | How do I stash my changes temporarily? | `git_tools_stashing_cleaning_chunk_001` (0.620) | `git_tools_stashing_cleaning_chunk_012` (0.769) | `git_tools_stashing_cleaning_chunk_001` (0.664) |
| 6 | How do I merge a branch in GitLab? | `gitlab_getting_started_chunk_004` (0.715) | `gitlab_getting_started_chunk_004` (0.819) | `gitlab_getting_started_chunk_004` (0.809) |
| 7 | How do I view the commit history? | `github_about_git_chunk_004` (0.593) | `git_basics_recording_changes_chunk_023` (0.754) | `git_tools_rebasing_chunk_016` (0.644) |
| 8 | How to set up SSH keys for GitLab? | `gitlab_getting_started_chunk_010` (0.743) | `gitlab_getting_started_chunk_010` (0.865) | `gitlab_getting_started_chunk_010` (0.783) |
| 9 | What is rebasing and when should I use it? | `git_tools_rebasing_chunk_001` (0.545) | `git_tools_rebasing_chunk_015` (0.777) | `git_tools_rebasing_chunk_001` (0.648) |
| 10 | How do I push changes to a remote repository? | `github_about_git_chunk_010` (0.701) | `github_about_git_chunk_010` (0.819) | `github_about_git_chunk_010` (0.707) |

## Score separation (top-1 score, margin top1-top2)

| # | Query | A top-1 | A margin | B top-1 | B margin | C top-1 | C margin |
|---|---|----|----|----|----|----|----|
| 1 | How do I clone a Git repository? | 0.709 | 0.000 | 0.819 | 0.012 | 0.751 | 0.007 |
| 2 | What is a Git branch and how do I create one? | 0.634 | 0.026 | 0.812 | 0.010 | 0.738 | 0.020 |
| 3 | How to resolve merge conflicts in Git? | 0.721 | 0.001 | 0.863 | 0.032 | 0.747 | 0.017 |
| 4 | What is the difference between git add and git commit? | 0.660 | 0.045 | 0.829 | 0.009 | 0.764 | 0.002 |
| 5 | How do I stash my changes temporarily? | 0.620 | 0.053 | 0.769 | 0.018 | 0.664 | 0.014 |
| 6 | How do I merge a branch in GitLab? | 0.715 | 0.115 | 0.819 | 0.068 | 0.809 | 0.048 |
| 7 | How do I view the commit history? | 0.593 | 0.007 | 0.754 | 0.003 | 0.644 | 0.001 |
| 8 | How to set up SSH keys for GitLab? | 0.743 | 0.068 | 0.865 | 0.146 | 0.783 | 0.079 |
| 9 | What is rebasing and when should I use it? | 0.545 | 0.033 | 0.777 | 0.036 | 0.648 | 0.005 |
| 10 | How do I push changes to a remote repository? | 0.701 | 0.039 | 0.819 | 0.042 | 0.707 | 0.016 |

## Aggregates

- Top-1 agreement A vs B: **3/10**
- Top-1 agreement A vs C: **6/10**
- Top-1 agreement B vs C: **4/10**
- Mean top-1 cosine A: **0.6642** | mean margin A: **0.0388** (bigger margin = clearer winner vs runner-up)
- Mean top-1 cosine B: **0.8126** | mean margin B: **0.0377** (bigger margin = clearer winner vs runner-up)
- Mean top-1 cosine C: **0.7256** | mean margin C: **0.0209** (bigger margin = clearer winner vs runner-up)
- Timing (index build / model load): A 1.5s / 3.9s; B 2.8s / 3.7s; C 11.8s / 3.7s

## Qualitative top-1 assessment (manual, reading the actual chunk text)

Cosine scores are not comparable across models — what matters is *which*
chunk each model lands on. Each top-1 was read manually:

| Query | A: MiniLM | B: bge-small | C: nomic |
|---|---|---|---|
| 1 clone | opener «обери спосіб отримати репо» (ok) | GitLab-інтро про клонування (weak) | **саме `git clone` туторіал** (libgit2) |
| 2 branch | GitLab-інтро (weak) | **opener глави Branch Management** | **opener глави Branch Management** |
| 3 merge conflict | GitLab-секція про conflicts (ok) | **глубина глави branching/merging (mergeconflict tutorial)** | GitLab-секція (ok) |
| 4 add vs commit | github_about_git (generic) | **глава Recording Changes (add/commit workflow)** | та сама глава, глибший суб-чанк |
| 5 stash | **opener глави Stashing** | та сама глава, суб-чанк | **opener глави Stashing** |
| 6 merge in GitLab | **gitlab_getting_started ✓** | **✓** | **✓** |
| 7 view history | «history = snapshots called commits» (generic) | diff-чанк Recording Changes (weak) | концепція «what history means» (rebase chapter) — тематично найточніший текст про history |
| 8 SSH keys | **gitlab_getting_started ✓** | **✓** | **✓** |
| 9 rebase | **opener глави Rebasing** | та сама глава, суб-чанк | **opener глави Rebasing** |
| 10 push | **github_about_git ✓** | **✓** | **✓** |

Document-level: A 9/10 acceptable, B 9/10 acceptable, **C 10/10 correct
document** (Q7 — closest on topic but not the `git log` chunk; no model
picked a dedicated `git log` tutorial).

### How nomic (C) compares to bge (B) specifically

- **C's wins over B:** Q1 (actual `git clone` tutorial vs GitLab intro),
  Q7 (topical "what history means" vs an off-target diff chunk).
- **B's wins over C:** Q2/Q3 (bge's chunk choices are more precise
  tutorials; C is ok there), and C is never *better* where B is already
  at the exact tutorial.
- **Margin (separation signal):** B 0.0377 ≈ A 0.0388 ≫ **C 0.0209** —
  nomic clusters similar chunks tightly, which is the *weakest* reranking
  signal of the three for a hybrid (BM25 + semantic).
- **Cost:** 768d (2x index size), index build 11.8s vs 1.5s/2.8s, no
  drop-in (FAISS index size changes, `prepare_knowledge_base.py` +
  `retrieval.py` must both move to the new dimension).
- **Agreement:** C agrees with A (MiniLM) on 6/10 top-1 — nomic's
  "prefer chapter openers" behaviour is closest to MiniLM's, while B
  (deep-subchunk behaviour) is the most different (3/10 with A).

### Conclusion

For *our* small GitLab KB the three models are close at document level
(9–10/10); the differences are in chunk precision and score calibration.
- **bge-small** stays the strongest single-model pick here: best
  calibration (0.81, wide spread), good margins, and the most precise
  chunk choices on tutorial-style queries — *and* it is a 384d drop-in.
- **nomic-embed-text-v1.5** is genuinely strong (best Q1, best Q7) but
  brings no net win for this KB: it does not beat bge anywhere bge is
  already exact, has the weakest margin, doubles index size, and needs
  code changes. Its documented strengths (8K context, multilingual,
  long-doc handling) do not matter for 145 short GitLab chunks.
- MiniLM-L6-v2's real weakness (generic intro chunks instead of the
  exact tutorial) is visible on Q1/Q2/Q7 and is exactly what bge fixes.

BM25 anchors the exact terms and metadata filters the doc. Recommendation:
adopt bge-small-en-v1.5 for the semantic leg of the hybrid; nomic is a
reasonable alternative if index size / dimension are not a constraint, but
on this data it is not the best pick.

(Project decision: keep all-MiniLM-L6-v2 as-is for now; bge-small
recorded as the measured drop-in upgrade, nomic measured as well.)
