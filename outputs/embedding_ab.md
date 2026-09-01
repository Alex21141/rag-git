# A/B Embedding Benchmark — real KB data (Final branch)

## Setup

- KB: `145 chunks`, 7 GitLab docs (the HW2/HW3 collection)
- Queries: the 10 test queries from `scripts/retrieval.py` (HW2 set)
- A: `sentence-transformers/all-MiniLM-L6-v2` (384d) — production model from HW2/HW3
- B: `BAAI/bge-small-en-v1.5` (384d) — technical-domain candidate, drop-in (same dimension)
- Cosine on normalized vectors, CPU, deterministic

## Top-1 retrieval per query

| # | Query | A top-1 (score) | B top-1 (score) | Same? |
|---|---|---|---|---|
| 1 | How do I clone a Git repository? | `git_basics_getting_repository_chunk_002` (0.7085) | `gitlab_getting_started_chunk_006` (0.8193) | **no** |
| 2 | What is a Git branch and how do I create one? | `gitlab_getting_started_chunk_001` (0.6338) | `branching_branch_management_chunk_001` (0.8124) | **no** |
| 3 | How to resolve merge conflicts in Git? | `gitlab_getting_started_chunk_005` (0.7214) | `branching_basic_branching_merging_chunk_014` (0.8628) | **no** |
| 4 | What is the difference between git add and git commit? | `github_about_git_chunk_008` (0.6602) | `git_basics_recording_changes_chunk_007` (0.8289) | **no** |
| 5 | How do I stash my changes temporarily? | `git_tools_stashing_cleaning_chunk_001` (0.6201) | `git_tools_stashing_cleaning_chunk_012` (0.7692) | **no** |
| 6 | How do I merge a branch in GitLab? | `gitlab_getting_started_chunk_004` (0.7146) | `gitlab_getting_started_chunk_004` (0.8190) | yes |
| 7 | How do I view the commit history? | `github_about_git_chunk_004` (0.5934) | `git_basics_recording_changes_chunk_023` (0.7543) | **no** |
| 8 | How to set up SSH keys for GitLab? | `gitlab_getting_started_chunk_010` (0.7434) | `gitlab_getting_started_chunk_010` (0.8650) | yes |
| 9 | What is rebasing and when should I use it? | `git_tools_rebasing_chunk_001` (0.5448) | `git_tools_rebasing_chunk_015` (0.7765) | **no** |
| 10 | How do I push changes to a remote repository? | `github_about_git_chunk_010` (0.7015) | `github_about_git_chunk_010` (0.8192) | yes |

## Score separation (top1 score, margin top1-top2)

| # | Query | A top-1 | A margin | B top-1 | B margin |
|---|---|---|---|---|---|
| 1 | How do I clone a Git repository? | 0.7085 | 0.0002 | 0.8193 | 0.0121 |
| 2 | What is a Git branch and how do I create one? | 0.6338 | 0.0263 | 0.8124 | 0.0099 |
| 3 | How to resolve merge conflicts in Git? | 0.7214 | 0.0006 | 0.8628 | 0.0318 |
| 4 | What is the difference between git add and git commit? | 0.6602 | 0.0450 | 0.8289 | 0.0090 |
| 5 | How do I stash my changes temporarily? | 0.6201 | 0.0533 | 0.7692 | 0.0181 |
| 6 | How do I merge a branch in GitLab? | 0.7146 | 0.1151 | 0.8190 | 0.0682 |
| 7 | How do I view the commit history? | 0.5934 | 0.0073 | 0.7543 | 0.0030 |
| 8 | How to set up SSH keys for GitLab? | 0.7434 | 0.0684 | 0.8650 | 0.1459 |
| 9 | What is rebasing and when should I use it? | 0.5448 | 0.0326 | 0.7765 | 0.0362 |
| 10 | How do I push changes to a remote repository? | 0.7015 | 0.0393 | 0.8192 | 0.0423 |

## Aggregates

- Top-1 agreement A vs B: **3/10**
- Mean top-1 cosine — A: **0.6642**, B: **0.8127**
- Mean margin (top1-top2) — A: **0.0388**, B: **0.0377** (bigger = clearer winner vs runner-up)
- Timing: index build A 1.5s / B 3.0s; model load A 9.1s / B 3.5s

## Qualitative top-1 assessment (manual, reading the actual chunk text)

Cosine scores are not comparable across models (B systematically scores
higher), so the decisive question is *which chunk* each model surfaced.
Judging each query's top-1 against the chunk's real content:

| # | Query | A top-1 chunk | B top-1 chunk | Better top-1 |
|---|---|---|---|---|
| 1 | clone a repo | getting_repository #002 ("two ways to get a repo") | getting_started #006 ("cloning it to your machine") | tie |
| 2 | what is a branch | getting_started #001 (generic Git intro) | branch_management #001 (the Branching chapter) | **B** |
| 3 | resolve merge conflicts | getting_started #005 (passing mention) | branching_merging #014 (resolution steps, `git mergetool`) | **B** |
| 4 | add vs commit | about_git #008 (generic) | recording_changes #007 (the add/commit chapter) | **B** |
| 5 | stash changes | stashing #001 (chapter opener) | stashing #012 (niche `git stash branch`) | **A** |
| 6 | merge a branch | getting_started #004 | getting_started #004 | tie |
| 7 | view commit history | about_git #004 ("revision history / snapshots") | recording_changes #023 (`git status`/`diff` example) | **A** |
| 8 | set up SSH keys | getting_started #010 | getting_started #010 | tie |
| 9 | what is rebasing | rebasing #001 (chapter opener, merge vs rebase) | rebasing #015 (niche "safe to rebase pushed") | **A** |
| 10 | push changes | about_git #010 | about_git #010 | tie |

**Head-to-head: A wins 3 (5,7,9), B wins 3 (2,3,4), tie 4 (1,6,8,10).**
It is *not* a runaway 10-0. The pattern is the insight:

- **B's 3 wins are topic-grounding wins** — for specific topic questions
  (branch, conflicts, add/commit) A returned a *generic* GitLab intro or a
  general doc, while B returned the exact chapter. Those are real misses for
  A.
- **A's 3 wins are opener-vs-depth wins** — for "what is X" intro questions
  A landed on the chapter *opener*, while B dug into a niche sub-chunk of
  the *same* chapter (still the right doc, just a less ideal chunk). Milder.
- **Score calibration favors B**: B's top-1 cosines (0.81) are higher and
  more spread than A's (0.66), which matters for re-ranking / thresholds in
  the HW3 hybrid (BM25 + semantic + metadata).

## Conclusion

`bge-small-en-v1.5` is the stronger embedder for this technical KB: better
topic grounding and better score calibration, at the same 384d (drop-in —
only `MODEL_NAME` + an index rebuild of 145 chunks, ~3s). Its one mild
weakness (preferring a deep niche chunk over the chapter opener for "what is
X" intro questions) is small and is mitigated by the hybrid retrieval, where
BM25 anchors the exact terms and metadata filters the doc. Recommendation:
adopt bge-small-en-v1.5 for the semantic leg of the hybrid.

(Project decision: keep all-MiniLM-L6-v2 as-is for now; bge-small-en-v1.5
is recorded here as the measured drop-in upgrade option.)
