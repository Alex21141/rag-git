# Alpha Sweep — BM25 + Semantic Hybrid

**Tested**: α = 0.0 (BM25 only) → 1.0 (Semantic only)

## Top-1 chunk per alpha

### How do I clone a Git repository?

| α | Top-1 chunk | Hybrid | Semantic | BM25 |
|---|-------------|--------|----------|------|
| 0.0 | git_basics_getting_repository_chunk_006 | 0.4194 | 0.6758 | 0.4194 |
| 0.1 | git_basics_getting_repository_chunk_006 | 0.4451 | 0.6758 | 0.4194 |
| 0.2 | git_basics_getting_repository_chunk_006 | 0.4707 | 0.6758 | 0.4194 |
| 0.3 | git_basics_getting_repository_chunk_006 | 0.4963 | 0.6758 | 0.4194 |
| 0.4 | git_basics_getting_repository_chunk_006 | 0.5220 | 0.6758 | 0.4194 |
| 0.5 | git_basics_getting_repository_chunk_006 | 0.5476 | 0.6758 | 0.4194 |
| 0.6 | git_basics_getting_repository_chunk_006 | 0.5733 | 0.6758 | 0.4194 |
| 0.7 | git_basics_getting_repository_chunk_006 | 0.5989 | 0.6758 | 0.4194 |
| 0.8 | git_basics_getting_repository_chunk_006 | 0.6245 | 0.6758 | 0.4194 |
| 0.9 | git_basics_getting_repository_chunk_006 | 0.6502 | 0.6758 | 0.4194 |
| 1.0 | git_basics_getting_repository_chunk_006 | 0.6758 | 0.6758 | 0.4194 |

### What is a Git branch and how do I create one?

| α | Top-1 chunk | Hybrid | Semantic | BM25 |
|---|-------------|--------|----------|------|
| 0.0 | gitlab_getting_started_chunk_001 | 0.4888 | 0.6338 | 0.4888 |
| 0.1 | gitlab_getting_started_chunk_001 | 0.5033 | 0.6338 | 0.4888 |
| 0.2 | gitlab_getting_started_chunk_001 | 0.5178 | 0.6338 | 0.4888 |
| 0.3 | gitlab_getting_started_chunk_001 | 0.5323 | 0.6338 | 0.4888 |
| 0.4 | gitlab_getting_started_chunk_001 | 0.5468 | 0.6338 | 0.4888 |
| 0.5 | gitlab_getting_started_chunk_001 | 0.5613 | 0.6338 | 0.4888 |
| 0.6 | gitlab_getting_started_chunk_001 | 0.5758 | 0.6338 | 0.4888 |
| 0.7 | gitlab_getting_started_chunk_001 | 0.5903 | 0.6338 | 0.4888 |
| 0.8 | gitlab_getting_started_chunk_001 | 0.6048 | 0.6338 | 0.4888 |
| 0.9 | gitlab_getting_started_chunk_001 | 0.6193 | 0.6338 | 0.4888 |
| 1.0 | gitlab_getting_started_chunk_001 | 0.6338 | 0.6338 | 0.4888 |

### How to resolve merge conflicts in Git?

| α | Top-1 chunk | Hybrid | Semantic | BM25 |
|---|-------------|--------|----------|------|
| 0.0 | branching_basic_branching_merging_chunk_011 | 0.7515 | 0.7244 | 0.7515 |
| 0.1 | branching_basic_branching_merging_chunk_011 | 0.7488 | 0.7244 | 0.7515 |
| 0.2 | branching_basic_branching_merging_chunk_011 | 0.7461 | 0.7244 | 0.7515 |
| 0.3 | branching_basic_branching_merging_chunk_011 | 0.7433 | 0.7244 | 0.7515 |
| 0.4 | branching_basic_branching_merging_chunk_011 | 0.7406 | 0.7244 | 0.7515 |
| 0.5 | branching_basic_branching_merging_chunk_011 | 0.7379 | 0.7244 | 0.7515 |
| 0.6 | branching_basic_branching_merging_chunk_011 | 0.7352 | 0.7244 | 0.7515 |
| 0.7 | branching_basic_branching_merging_chunk_011 | 0.7325 | 0.7244 | 0.7515 |
| 0.8 | branching_basic_branching_merging_chunk_011 | 0.7298 | 0.7244 | 0.7515 |
| 0.9 | branching_basic_branching_merging_chunk_011 | 0.7271 | 0.7244 | 0.7515 |
| 1.0 | branching_basic_branching_merging_chunk_016 | 0.7409 | 0.7409 | 0.5090 |

### What is the difference between git add and git commit?

| α | Top-1 chunk | Hybrid | Semantic | BM25 |
|---|-------------|--------|----------|------|
| 0.0 | gitlab_getting_started_chunk_002 | 0.5361 | 0.6164 | 0.5361 |
| 0.1 | gitlab_getting_started_chunk_002 | 0.5442 | 0.6164 | 0.5361 |
| 0.2 | gitlab_getting_started_chunk_002 | 0.5522 | 0.6164 | 0.5361 |
| 0.3 | gitlab_getting_started_chunk_002 | 0.5602 | 0.6164 | 0.5361 |
| 0.4 | gitlab_getting_started_chunk_002 | 0.5682 | 0.6164 | 0.5361 |
| 0.5 | gitlab_getting_started_chunk_002 | 0.5763 | 0.6164 | 0.5361 |
| 0.6 | gitlab_getting_started_chunk_002 | 0.5843 | 0.6164 | 0.5361 |
| 0.7 | gitlab_getting_started_chunk_002 | 0.5923 | 0.6164 | 0.5361 |
| 0.8 | gitlab_getting_started_chunk_002 | 0.6003 | 0.6164 | 0.5361 |
| 0.9 | gitlab_getting_started_chunk_002 | 0.6084 | 0.6164 | 0.5361 |
| 1.0 | github_about_git_chunk_009 | 0.6306 | 0.6306 | 0.2462 |

### How do I stash my changes temporarily?

| α | Top-1 chunk | Hybrid | Semantic | BM25 |
|---|-------------|--------|----------|------|
| 0.0 | git_tools_stashing_cleaning_chunk_004 | 0.2849 | 0.5509 | 0.2849 |
| 0.1 | git_tools_stashing_cleaning_chunk_004 | 0.3115 | 0.5509 | 0.2849 |
| 0.2 | git_tools_stashing_cleaning_chunk_004 | 0.3381 | 0.5509 | 0.2849 |
| 0.3 | git_tools_stashing_cleaning_chunk_002 | 0.3745 | 0.6295 | 0.2652 |
| 0.4 | git_tools_stashing_cleaning_chunk_002 | 0.4109 | 0.6295 | 0.2652 |
| 0.5 | git_tools_stashing_cleaning_chunk_002 | 0.4473 | 0.6295 | 0.2652 |
| 0.6 | git_tools_stashing_cleaning_chunk_002 | 0.4838 | 0.6295 | 0.2652 |
| 0.7 | git_tools_stashing_cleaning_chunk_002 | 0.5202 | 0.6295 | 0.2652 |
| 0.8 | git_tools_stashing_cleaning_chunk_002 | 0.5566 | 0.6295 | 0.2652 |
| 0.9 | git_tools_stashing_cleaning_chunk_002 | 0.5931 | 0.6295 | 0.2652 |
| 1.0 | git_tools_stashing_cleaning_chunk_002 | 0.6295 | 0.6295 | 0.2652 |

### How do I merge a branch in GitLab?

| α | Top-1 chunk | Hybrid | Semantic | BM25 |
|---|-------------|--------|----------|------|
| 0.0 | gitlab_getting_started_chunk_004 | 0.4143 | 0.6885 | 0.4143 |
| 0.1 | gitlab_getting_started_chunk_004 | 0.4417 | 0.6885 | 0.4143 |
| 0.2 | gitlab_getting_started_chunk_004 | 0.4691 | 0.6885 | 0.4143 |
| 0.3 | gitlab_getting_started_chunk_004 | 0.4966 | 0.6885 | 0.4143 |
| 0.4 | gitlab_getting_started_chunk_004 | 0.5240 | 0.6885 | 0.4143 |
| 0.5 | gitlab_getting_started_chunk_004 | 0.5514 | 0.6885 | 0.4143 |
| 0.6 | gitlab_getting_started_chunk_004 | 0.5788 | 0.6885 | 0.4143 |
| 0.7 | gitlab_getting_started_chunk_004 | 0.6063 | 0.6885 | 0.4143 |
| 0.8 | gitlab_getting_started_chunk_004 | 0.6337 | 0.6885 | 0.4143 |
| 0.9 | gitlab_getting_started_chunk_004 | 0.6611 | 0.6885 | 0.4143 |
| 1.0 | gitlab_getting_started_chunk_005 | 0.6909 | 0.6909 | 0.2122 |

### How do I view the commit history?

| α | Top-1 chunk | Hybrid | Semantic | BM25 |
|---|-------------|--------|----------|------|
| 0.0 | github_about_git_chunk_001 | 0.4248 | 0.5813 | 0.4248 |
| 0.1 | github_about_git_chunk_001 | 0.4405 | 0.5813 | 0.4248 |
| 0.2 | github_about_git_chunk_001 | 0.4561 | 0.5813 | 0.4248 |
| 0.3 | github_about_git_chunk_001 | 0.4718 | 0.5813 | 0.4248 |
| 0.4 | github_about_git_chunk_001 | 0.4874 | 0.5813 | 0.4248 |
| 0.5 | github_about_git_chunk_001 | 0.5030 | 0.5813 | 0.4248 |
| 0.6 | github_about_git_chunk_001 | 0.5187 | 0.5813 | 0.4248 |
| 0.7 | github_about_git_chunk_001 | 0.5343 | 0.5813 | 0.4248 |
| 0.8 | github_about_git_chunk_001 | 0.5500 | 0.5813 | 0.4248 |
| 0.9 | github_about_git_chunk_001 | 0.5656 | 0.5813 | 0.4248 |
| 1.0 | github_about_git_chunk_001 | 0.5813 | 0.5813 | 0.4248 |

### How to set up SSH keys for GitLab?

| α | Top-1 chunk | Hybrid | Semantic | BM25 |
|---|-------------|--------|----------|------|
| 0.0 | gitlab_getting_started_chunk_010 | 1.0000 | 0.7385 | 1.0000 |
| 0.1 | gitlab_getting_started_chunk_010 | 0.9738 | 0.7385 | 1.0000 |
| 0.2 | gitlab_getting_started_chunk_010 | 0.9477 | 0.7385 | 1.0000 |
| 0.3 | gitlab_getting_started_chunk_010 | 0.9215 | 0.7385 | 1.0000 |
| 0.4 | gitlab_getting_started_chunk_010 | 0.8954 | 0.7385 | 1.0000 |
| 0.5 | gitlab_getting_started_chunk_010 | 0.8692 | 0.7385 | 1.0000 |
| 0.6 | gitlab_getting_started_chunk_010 | 0.8431 | 0.7385 | 1.0000 |
| 0.7 | gitlab_getting_started_chunk_010 | 0.8169 | 0.7385 | 1.0000 |
| 0.8 | gitlab_getting_started_chunk_010 | 0.7908 | 0.7385 | 1.0000 |
| 0.9 | gitlab_getting_started_chunk_010 | 0.7646 | 0.7385 | 1.0000 |
| 1.0 | gitlab_getting_started_chunk_010 | 0.7385 | 0.7385 | 1.0000 |

### What is rebasing and when should I use it?

| α | Top-1 chunk | Hybrid | Semantic | BM25 |
|---|-------------|--------|----------|------|
| 0.0 | git_tools_rebasing_chunk_001 | 0.6038 | 0.5448 | 0.6038 |
| 0.1 | git_tools_rebasing_chunk_001 | 0.5979 | 0.5448 | 0.6038 |
| 0.2 | git_tools_rebasing_chunk_001 | 0.5920 | 0.5448 | 0.6038 |
| 0.3 | git_tools_rebasing_chunk_001 | 0.5861 | 0.5448 | 0.6038 |
| 0.4 | git_tools_rebasing_chunk_001 | 0.5802 | 0.5448 | 0.6038 |
| 0.5 | git_tools_rebasing_chunk_001 | 0.5743 | 0.5448 | 0.6038 |
| 0.6 | git_tools_rebasing_chunk_001 | 0.5684 | 0.5448 | 0.6038 |
| 0.7 | git_tools_rebasing_chunk_001 | 0.5625 | 0.5448 | 0.6038 |
| 0.8 | git_tools_rebasing_chunk_001 | 0.5566 | 0.5448 | 0.6038 |
| 0.9 | git_tools_rebasing_chunk_001 | 0.5507 | 0.5448 | 0.6038 |
| 1.0 | git_tools_rebasing_chunk_001 | 0.5448 | 0.5448 | 0.6038 |

### How do I push changes to a remote repository?

| α | Top-1 chunk | Hybrid | Semantic | BM25 |
|---|-------------|--------|----------|------|
| 0.0 | github_about_git_chunk_010 | 0.4908 | 0.7104 | 0.4908 |
| 0.1 | github_about_git_chunk_010 | 0.5128 | 0.7104 | 0.4908 |
| 0.2 | github_about_git_chunk_010 | 0.5348 | 0.7104 | 0.4908 |
| 0.3 | github_about_git_chunk_010 | 0.5567 | 0.7104 | 0.4908 |
| 0.4 | github_about_git_chunk_010 | 0.5787 | 0.7104 | 0.4908 |
| 0.5 | github_about_git_chunk_010 | 0.6006 | 0.7104 | 0.4908 |
| 0.6 | github_about_git_chunk_010 | 0.6226 | 0.7104 | 0.4908 |
| 0.7 | github_about_git_chunk_010 | 0.6445 | 0.7104 | 0.4908 |
| 0.8 | github_about_git_chunk_010 | 0.6665 | 0.7104 | 0.4908 |
| 0.9 | github_about_git_chunk_010 | 0.6885 | 0.7104 | 0.4908 |
| 1.0 | github_about_git_chunk_010 | 0.7104 | 0.7104 | 0.4908 |

## Summary — Average top-1 score by alpha

| α | Avg Score |
|---|----------|
| 0.0 | 0.5414 |
| 0.1 | 0.5520 |
| 0.2 | 0.5625 |
| 0.3 | 0.5739 |
| 0.4 | 0.5854 |
| 0.5 | 0.5969 |
| 0.6 | 0.6084 |
| 0.7 | 0.6199 |
| 0.8 | 0.6314 |
| 0.9 | 0.6429 |
| 1.0 | 0.6577 |

**Best α = 1.0** with average score 0.6577

Current α=0.5: avg 0.5969
Best α=1.0: avg 0.6577 (improvement: +0.0608)