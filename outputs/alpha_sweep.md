# Alpha Sweep — BM25 + Semantic Hybrid

**Tested**: α = 0.0 (BM25 only) → 1.0 (Semantic only)

## Top-1 chunk per alpha

### How do I clone a Git repository?

| α | Top-1 chunk | Hybrid | Semantic | BM25 |
|---|-------------|--------|----------|------|
| 0.0 | git_basics_getting_repository_chunk_006 | 1.0000 | 0.6758 | 6.7084 |
| 0.1 | git_basics_getting_repository_chunk_006 | 1.0000 | 0.6758 | 6.7084 |
| 0.2 | git_basics_getting_repository_chunk_006 | 1.0000 | 0.6758 | 6.7084 |
| 0.3 | git_basics_getting_repository_chunk_006 | 1.0000 | 0.6758 | 6.7084 |
| 0.4 | git_basics_getting_repository_chunk_006 | 1.0000 | 0.6758 | 6.7084 |
| 0.5 | git_basics_getting_repository_chunk_006 | 1.0000 | 0.6758 | 6.7084 |
| 0.6 | git_basics_getting_repository_chunk_006 | 1.0000 | 0.6758 | 6.7084 |
| 0.7 | git_basics_getting_repository_chunk_006 | 1.0000 | 0.6758 | 6.7084 |
| 0.8 | git_basics_getting_repository_chunk_006 | 1.0000 | 0.6758 | 6.7084 |
| 0.9 | git_basics_getting_repository_chunk_006 | 1.0000 | 0.6758 | 6.7084 |
| 1.0 | git_basics_getting_repository_chunk_006 | 1.0000 | 0.6758 | 6.7084 |

### What is a Git branch and how do I create one?

| α | Top-1 chunk | Hybrid | Semantic | BM25 |
|---|-------------|--------|----------|------|
| 0.0 | gitlab_getting_started_chunk_001 | 1.0000 | 0.6338 | 7.8186 |
| 0.1 | gitlab_getting_started_chunk_001 | 1.0000 | 0.6338 | 7.8186 |
| 0.2 | gitlab_getting_started_chunk_001 | 1.0000 | 0.6338 | 7.8186 |
| 0.3 | gitlab_getting_started_chunk_001 | 1.0000 | 0.6338 | 7.8186 |
| 0.4 | gitlab_getting_started_chunk_001 | 1.0000 | 0.6338 | 7.8186 |
| 0.5 | gitlab_getting_started_chunk_001 | 1.0000 | 0.6338 | 7.8186 |
| 0.6 | gitlab_getting_started_chunk_001 | 1.0000 | 0.6338 | 7.8186 |
| 0.7 | gitlab_getting_started_chunk_001 | 1.0000 | 0.6338 | 7.8186 |
| 0.8 | gitlab_getting_started_chunk_001 | 1.0000 | 0.6338 | 7.8186 |
| 0.9 | gitlab_getting_started_chunk_001 | 1.0000 | 0.6338 | 7.8186 |
| 1.0 | gitlab_getting_started_chunk_001 | 1.0000 | 0.6338 | 7.8186 |

### How to resolve merge conflicts in Git?

| α | Top-1 chunk | Hybrid | Semantic | BM25 |
|---|-------------|--------|----------|------|
| 0.0 | branching_basic_branching_merging_chunk_011 | 1.0000 | 0.7244 | 12.0196 |
| 0.1 | branching_basic_branching_merging_chunk_011 | 0.9978 | 0.7244 | 12.0196 |
| 0.2 | branching_basic_branching_merging_chunk_011 | 0.9955 | 0.7244 | 12.0196 |
| 0.3 | branching_basic_branching_merging_chunk_011 | 0.9933 | 0.7244 | 12.0196 |
| 0.4 | branching_basic_branching_merging_chunk_011 | 0.9911 | 0.7244 | 12.0196 |
| 0.5 | branching_basic_branching_merging_chunk_011 | 0.9888 | 0.7244 | 12.0196 |
| 0.6 | branching_basic_branching_merging_chunk_011 | 0.9866 | 0.7244 | 12.0196 |
| 0.7 | branching_basic_branching_merging_chunk_011 | 0.9844 | 0.7244 | 12.0196 |
| 0.8 | branching_basic_branching_merging_chunk_011 | 0.9821 | 0.7244 | 12.0196 |
| 0.9 | branching_basic_branching_merging_chunk_011 | 0.9799 | 0.7244 | 12.0196 |
| 1.0 | branching_basic_branching_merging_chunk_016 | 1.0000 | 0.7409 | 8.1411 |

### What is the difference between git add and git commit?

| α | Top-1 chunk | Hybrid | Semantic | BM25 |
|---|-------------|--------|----------|------|
| 0.0 | gitlab_getting_started_chunk_002 | 1.0000 | 0.6164 | 8.5754 |
| 0.1 | gitlab_getting_started_chunk_002 | 0.9977 | 0.6164 | 8.5754 |
| 0.2 | gitlab_getting_started_chunk_002 | 0.9955 | 0.6164 | 8.5754 |
| 0.3 | gitlab_getting_started_chunk_002 | 0.9932 | 0.6164 | 8.5754 |
| 0.4 | gitlab_getting_started_chunk_002 | 0.9910 | 0.6164 | 8.5754 |
| 0.5 | gitlab_getting_started_chunk_002 | 0.9887 | 0.6164 | 8.5754 |
| 0.6 | gitlab_getting_started_chunk_002 | 0.9864 | 0.6164 | 8.5754 |
| 0.7 | gitlab_getting_started_chunk_002 | 0.9842 | 0.6164 | 8.5754 |
| 0.8 | gitlab_getting_started_chunk_002 | 0.9819 | 0.6164 | 8.5754 |
| 0.9 | gitlab_getting_started_chunk_002 | 0.9796 | 0.6164 | 8.5754 |
| 1.0 | github_about_git_chunk_009 | 1.0000 | 0.6306 | 3.9383 |

### How do I stash my changes temporarily?

| α | Top-1 chunk | Hybrid | Semantic | BM25 |
|---|-------------|--------|----------|------|
| 0.0 | git_tools_stashing_cleaning_chunk_004 | 1.0000 | 0.5509 | 4.5569 |
| 0.1 | git_tools_stashing_cleaning_chunk_004 | 0.9875 | 0.5509 | 4.5569 |
| 0.2 | git_tools_stashing_cleaning_chunk_004 | 0.9750 | 0.5509 | 4.5569 |
| 0.3 | git_tools_stashing_cleaning_chunk_004 | 0.9625 | 0.5509 | 4.5569 |
| 0.4 | git_tools_stashing_cleaning_chunk_002 | 0.9584 | 0.6295 | 4.2413 |
| 0.5 | git_tools_stashing_cleaning_chunk_002 | 0.9654 | 0.6295 | 4.2413 |
| 0.6 | git_tools_stashing_cleaning_chunk_002 | 0.9723 | 0.6295 | 4.2413 |
| 0.7 | git_tools_stashing_cleaning_chunk_002 | 0.9792 | 0.6295 | 4.2413 |
| 0.8 | git_tools_stashing_cleaning_chunk_002 | 0.9861 | 0.6295 | 4.2413 |
| 0.9 | git_tools_stashing_cleaning_chunk_002 | 0.9931 | 0.6295 | 4.2413 |
| 1.0 | git_tools_stashing_cleaning_chunk_002 | 1.0000 | 0.6295 | 4.2413 |

### How do I merge a branch in GitLab?

| α | Top-1 chunk | Hybrid | Semantic | BM25 |
|---|-------------|--------|----------|------|
| 0.0 | gitlab_getting_started_chunk_004 | 1.0000 | 0.6885 | 6.6265 |
| 0.1 | gitlab_getting_started_chunk_004 | 0.9997 | 0.6885 | 6.6265 |
| 0.2 | gitlab_getting_started_chunk_004 | 0.9993 | 0.6885 | 6.6265 |
| 0.3 | gitlab_getting_started_chunk_004 | 0.9990 | 0.6885 | 6.6265 |
| 0.4 | gitlab_getting_started_chunk_004 | 0.9986 | 0.6885 | 6.6265 |
| 0.5 | gitlab_getting_started_chunk_004 | 0.9983 | 0.6885 | 6.6265 |
| 0.6 | gitlab_getting_started_chunk_004 | 0.9979 | 0.6885 | 6.6265 |
| 0.7 | gitlab_getting_started_chunk_004 | 0.9976 | 0.6885 | 6.6265 |
| 0.8 | gitlab_getting_started_chunk_004 | 0.9972 | 0.6885 | 6.6265 |
| 0.9 | gitlab_getting_started_chunk_004 | 0.9969 | 0.6885 | 6.6265 |
| 1.0 | gitlab_getting_started_chunk_005 | 1.0000 | 0.6909 | 3.3941 |

### How do I view the commit history?

| α | Top-1 chunk | Hybrid | Semantic | BM25 |
|---|-------------|--------|----------|------|
| 0.0 | github_about_git_chunk_001 | 1.0000 | 0.5813 | 6.7947 |
| 0.1 | github_about_git_chunk_001 | 1.0000 | 0.5813 | 6.7947 |
| 0.2 | github_about_git_chunk_001 | 1.0000 | 0.5813 | 6.7947 |
| 0.3 | github_about_git_chunk_001 | 1.0000 | 0.5813 | 6.7947 |
| 0.4 | github_about_git_chunk_001 | 1.0000 | 0.5813 | 6.7947 |
| 0.5 | github_about_git_chunk_001 | 1.0000 | 0.5813 | 6.7947 |
| 0.6 | github_about_git_chunk_001 | 1.0000 | 0.5813 | 6.7947 |
| 0.7 | github_about_git_chunk_001 | 1.0000 | 0.5813 | 6.7947 |
| 0.8 | github_about_git_chunk_001 | 1.0000 | 0.5813 | 6.7947 |
| 0.9 | github_about_git_chunk_001 | 1.0000 | 0.5813 | 6.7947 |
| 1.0 | github_about_git_chunk_001 | 1.0000 | 0.5813 | 6.7947 |

### How to set up SSH keys for GitLab?

| α | Top-1 chunk | Hybrid | Semantic | BM25 |
|---|-------------|--------|----------|------|
| 0.0 | gitlab_getting_started_chunk_010 | 1.0000 | 0.7385 | 15.9945 |
| 0.1 | gitlab_getting_started_chunk_010 | 1.0000 | 0.7385 | 15.9945 |
| 0.2 | gitlab_getting_started_chunk_010 | 1.0000 | 0.7385 | 15.9945 |
| 0.3 | gitlab_getting_started_chunk_010 | 1.0000 | 0.7385 | 15.9945 |
| 0.4 | gitlab_getting_started_chunk_010 | 1.0000 | 0.7385 | 15.9945 |
| 0.5 | gitlab_getting_started_chunk_010 | 1.0000 | 0.7385 | 15.9945 |
| 0.6 | gitlab_getting_started_chunk_010 | 1.0000 | 0.7385 | 15.9945 |
| 0.7 | gitlab_getting_started_chunk_010 | 1.0000 | 0.7385 | 15.9945 |
| 0.8 | gitlab_getting_started_chunk_010 | 1.0000 | 0.7385 | 15.9945 |
| 0.9 | gitlab_getting_started_chunk_010 | 1.0000 | 0.7385 | 15.9945 |
| 1.0 | gitlab_getting_started_chunk_010 | 1.0000 | 0.7385 | 15.9945 |

### What is rebasing and when should I use it?

| α | Top-1 chunk | Hybrid | Semantic | BM25 |
|---|-------------|--------|----------|------|
| 0.0 | git_tools_rebasing_chunk_001 | 1.0000 | 0.5448 | 9.6568 |
| 0.1 | git_tools_rebasing_chunk_001 | 1.0000 | 0.5448 | 9.6568 |
| 0.2 | git_tools_rebasing_chunk_001 | 1.0000 | 0.5448 | 9.6568 |
| 0.3 | git_tools_rebasing_chunk_001 | 1.0000 | 0.5448 | 9.6568 |
| 0.4 | git_tools_rebasing_chunk_001 | 1.0000 | 0.5448 | 9.6568 |
| 0.5 | git_tools_rebasing_chunk_001 | 1.0000 | 0.5448 | 9.6568 |
| 0.6 | git_tools_rebasing_chunk_001 | 1.0000 | 0.5448 | 9.6568 |
| 0.7 | git_tools_rebasing_chunk_001 | 1.0000 | 0.5448 | 9.6568 |
| 0.8 | git_tools_rebasing_chunk_001 | 1.0000 | 0.5448 | 9.6568 |
| 0.9 | git_tools_rebasing_chunk_001 | 1.0000 | 0.5448 | 9.6568 |
| 1.0 | git_tools_rebasing_chunk_001 | 1.0000 | 0.5448 | 9.6568 |

### How do I push changes to a remote repository?

| α | Top-1 chunk | Hybrid | Semantic | BM25 |
|---|-------------|--------|----------|------|
| 0.0 | github_about_git_chunk_010 | 1.0000 | 0.7104 | 7.8509 |
| 0.1 | github_about_git_chunk_010 | 1.0000 | 0.7104 | 7.8509 |
| 0.2 | github_about_git_chunk_010 | 1.0000 | 0.7104 | 7.8509 |
| 0.3 | github_about_git_chunk_010 | 1.0000 | 0.7104 | 7.8509 |
| 0.4 | github_about_git_chunk_010 | 1.0000 | 0.7104 | 7.8509 |
| 0.5 | github_about_git_chunk_010 | 1.0000 | 0.7104 | 7.8509 |
| 0.6 | github_about_git_chunk_010 | 1.0000 | 0.7104 | 7.8509 |
| 0.7 | github_about_git_chunk_010 | 1.0000 | 0.7104 | 7.8509 |
| 0.8 | github_about_git_chunk_010 | 1.0000 | 0.7104 | 7.8509 |
| 0.9 | github_about_git_chunk_010 | 1.0000 | 0.7104 | 7.8509 |
| 1.0 | github_about_git_chunk_010 | 1.0000 | 0.7104 | 7.8509 |

## Summary — Average top-1 score by alpha

| α | Avg Score |
|---|----------|
| 0.0 | 1.0000 |
| 0.1 | 0.9983 |
| 0.2 | 0.9965 |
| 0.3 | 0.9948 |
| 0.4 | 0.9939 |
| 0.5 | 0.9941 |
| 0.6 | 0.9943 |
| 0.7 | 0.9945 |
| 0.8 | 0.9947 |
| 0.9 | 0.9950 |
| 1.0 | 1.0000 |

**Best α = 0.0** with average score 1.0000

Current α=0.5: avg 0.9941
Best α=0.0: avg 1.0000 (improvement: +0.0059)