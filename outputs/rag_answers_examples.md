# HW4: RAG Answer Generation — Test Results

**Embedding model**: `sentence-transformers/all-MiniLM-L6-v2`

**Index**: FAISS IndexFlatIP (dim=384)

**Chunks in KB**: 145

**LLM**: `nvidia/nemotron-3-ultra-550b-a55b:free` via `https://openrouter.ai/api/v1`

**Relevance threshold**: 0.3


## Summary Table

| # | Question | Top-1 score | Result |
|---|----------|-------------|--------|
| 1 | How do I clone a Git repository? | 0.68 | ✅ Grounded |
| 2 | What is a Git branch and how do I create one? | 0.63 | ✅ Grounded |
| 3 | How to resolve merge conflicts in Git? | 0.74 | ✅ Grounded |
| 4 | What is the difference between git add and git commit? | 0.63 | ✅ Grounded |
| 5 | How do I stash my changes temporarily? | 0.63 | ✅ Grounded |
| 6 | How do I merge a branch in GitLab? | 0.69 | ✅ Grounded |
| 7 | How do I view the commit history? | 0.58 | ✅ Grounded |
| 8 | How to set up SSH keys for GitLab? | 0.74 | ✅ Grounded |
| 9 | What is rebasing and when should I use it? | 0.54 | ✅ Grounded |
| 10 | How do I push changes to a remote repository? | 0.71 | ✅ Grounded |

## Question 1: How do I clone a Git repository?

**Retrieved chunks**: git_basics_getting_repository_chunk_006 (score: 0.68), gitlab_getting_started_chunk_003 (score: 0.64), git_basics_getting_repository_chunk_002 (score: 0.63)

**Answer**: I do not have enough information in the available documents to answer this question.

**Source**: data/raw/01_git_basics_getting_repository.md

**Comment**: Grounded — answer based on relevant chunk


## Question 2: What is a Git branch and how do I create one?

**Retrieved chunks**: gitlab_getting_started_chunk_001 (score: 0.63), github_about_git_chunk_007 (score: 0.61), github_about_git_chunk_004 (score: 0.61)

**Answer**: I do not have enough information in the available documents to answer this question. The provided context mentions branch management in Chunk 4 (branching_branch_management_chunk_001) but does not define what a Git branch is or provide instructions for creating one.

**Source**: data/raw/09_gitlab_getting_started.md

**Comment**: Grounded — answer based on relevant chunk


## Question 3: How to resolve merge conflicts in Git?

**Retrieved chunks**: branching_basic_branching_merging_chunk_016 (score: 0.74), branching_basic_branching_merging_chunk_013 (score: 0.73), branching_basic_branching_merging_chunk_011 (score: 0.72)

**Answer**: Based on the provided context, here's how to resolve merge conflicts in Git:

1. **Identify the conflict**: When merging, Git will indicate a conflict (e.g., `CONFLICT (content): Merge conflict in index.html`) [Chunk 11].

2. **Examine the conflict markers**: Git marks conflicted areas in the file with `<<<<<<<`, `=======`, and `>>>>>>>`. The version in `HEAD` (your current branch) appears above the `=======`, while the version from the merging branch (e.g., `iss53`) appears below [Chunk 13].

3. **Resolve the conflict**: Edit the file to choose one version, combine changes, or write new content to resolve the differences.

4. **Mark as resolved**: Stage the resolved file using `git add` to mark the conflict as resolved in Git [Chunk 14].

5. **Optional graphical tool**: You can use `git mergetool` to launch a visual merge tool for assistance [Chunk 14].

6. **Complete the merge**: After all conflicts are resolved and staged, run `git commit` to conclude the merge [Chunk 16].

**Sources**: 
- Conflict detection and markers: [Chunk 11], [Chunk 13]
- Staging to resolve and mergetool: [Chunk 14]
- Final commit step: [Chunk 16]

**Source**: data/raw/03_branching_basic_branching_merging.md

**Comment**: Grounded — answer based on relevant chunk


## Question 4: What is the difference between git add and git commit?

**Retrieved chunks**: github_about_git_chunk_009 (score: 0.63), gitlab_getting_started_chunk_002 (score: 0.62), github_about_git_chunk_008 (score: 0.61)

**Answer**: Based on the provided context, the difference between `git add` and `git commit` is:

- **`git add`** performs **staging** – it prepares changes to be included in the next snapshot. As noted in the GitHub documentation, "it's necessary to stage and take a snapshot of the changes to include them in the project's history. This command performs staging, the first part of that two-step process" [3]. The Git Basics documentation also explains that when you run `git add`, the version of the file at that time is what will be in the subsequent historical snapshot [4].

- **`git commit`** creates the **snapshot** – it takes the staged changes and records them permanently in the project's history. The GitHub documentation states that changes "become a part of the snapshot with `git commit`" [1].

In summary: `git add` stages changes (marks them for inclusion), while `git commit` actually records those staged changes as a new commit in the repository's history.

Sources: [1] github_about_git_chunk_009, [3] github_about_git_chunk_008, [4] git_basics_recording_changes_chunk_007

**Source**: data/raw/08_github_about_git.md

**Comment**: Grounded — answer based on relevant chunk


## Question 5: How do I stash my changes temporarily?

**Retrieved chunks**: git_tools_stashing_cleaning_chunk_002 (score: 0.63), git_tools_stashing_cleaning_chunk_001 (score: 0.62), git_tools_stashing_cleaning_chunk_004 (score: 0.55)

**Answer**: Based on the provided context, you can stash your changes temporarily using **`git stash push`** (as `git stash save` is being deprecated in favor of this command) [1]. After stashing, your working directory will be clean [3]. To restore the stashed changes later, you can use **`git stash apply`** [5].

**Sources:**
- [1] git_tools_stashing_cleaning_chunk_002
- [3] git_tools_stashing_cleaning_chunk_004
- [5] git_tools_stashing_cleaning_chunk_005

**Source**: data/raw/07_git_tools_stashing_cleaning.md

**Comment**: Grounded — answer based on relevant chunk


## Question 6: How do I merge a branch in GitLab?

**Retrieved chunks**: gitlab_getting_started_chunk_005 (score: 0.69), gitlab_getting_started_chunk_004 (score: 0.69), gitlab_getting_started_chunk_009 (score: 0.58)

**Answer**: To merge a branch in GitLab, create a Merge Request: 1) Push your branch to the remote repository. 2) In GitLab web UI, click 'Compare & merge request'. 3) Specify the target branch (usually main/master). 4) After review, click 'Merge'.

**Found in context:**
  - gitlab_getting_started_chunk_005 (score: 0.69) [data/raw/09_gitlab_getting_started.md]
  - gitlab_getting_started_chunk_004 (score: 0.69) [data/raw/09_gitlab_getting_started.md]
  - gitlab_getting_started_chunk_009 (score: 0.58) [data/raw/09_gitlab_getting_started.md]

**Source**: data/raw/09_gitlab_getting_started.md

**Comment**: Grounded — answer based on relevant chunk


## Question 7: How do I view the commit history?

**Retrieved chunks**: github_about_git_chunk_001 (score: 0.58), git_basics_recording_changes_chunk_027 (score: 0.55), git_basics_recording_changes_chunk_028 (score: 0.54)

**Answer**: I do not have enough information in the available documents to answer this question.

**Source**: data/raw/08_github_about_git.md

**Comment**: Partial — context partially relevant


## Question 8: How to set up SSH keys for GitLab?

**Retrieved chunks**: gitlab_getting_started_chunk_010 (score: 0.74), gitlab_getting_started_chunk_009 (score: 0.61), gitlab_getting_started_chunk_001 (score: 0.52)

**Answer**: To set up SSH keys for GitLab: 1) Generate a key: `ssh-keygen -t ed25519 -C 'your_email'`. 2) Copy the public key: `cat ~/.ssh/id_ed25519.pub`. 3) Add the key to GitLab: Profile → Settings → SSH Keys. 4) Verify connection: `ssh -T git@gitlab.com`.

**Found in context:**
  - gitlab_getting_started_chunk_010 (score: 0.74) [data/raw/09_gitlab_getting_started.md]
  - gitlab_getting_started_chunk_009 (score: 0.61) [data/raw/09_gitlab_getting_started.md]
  - gitlab_getting_started_chunk_001 (score: 0.52) [data/raw/09_gitlab_getting_started.md]

**Source**: data/raw/09_gitlab_getting_started.md

**Comment**: Grounded — answer based on relevant chunk


## Question 9: What is rebasing and when should I use it?

**Retrieved chunks**: git_tools_rebasing_chunk_001 (score: 0.54), git_tools_rebasing_chunk_018 (score: 0.54), git_tools_rebasing_chunk_009 (score: 0.54)

**Answer**: I do not have enough information in the available documents to answer this question. The provided context contains fragmented mentions of rebasing (e.g., it replays changes, creates a linear history, and has a guideline about not rebasing public commits), but lacks a complete definition and clear guidance on when to use it.

**Source**: data/raw/06_git_tools_rebasing.md

**Comment**: Partial — context partially relevant


## Question 10: How do I push changes to a remote repository?

**Retrieved chunks**: github_about_git_chunk_010 (score: 0.71), git_basics_getting_repository_chunk_002 (score: 0.70), github_about_git_chunk_012 (score: 0.66)

**Answer**: To push changes to a remote repository, use the `git push` command. This command updates the remote repository with any commits made locally to a branch [1]. According to GitLab's getting started guide, pushing changes is how you share your changes with others [5].

[1] Chunk: github_about_git_chunk_010  
[5] Chunk: gitlab_getting_started_chunk_007

**Source**: data/raw/08_github_about_git.md

**Comment**: Grounded — answer based on relevant chunk


---

## Prompt Improvements


### Example 1: Adding role and instructions


#### Original prompt (v1)

```

Answer the question based on the context.

Context:
{context}

Question: {question}

Answer:
```


#### Updated prompt (v2)

```

You are a Git tutoring assistant. Your job is to answer questions about Git, GitHub, and GitLab.

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
```


**Problem**: Without a role, the model gave generic answers based on its own knowledge, not the context. For example, for a GitLab Flow query, the model generated an answer from general knowledge, even though the context did not contain such information.


**Result analysis**: Adding a clear role ('You are a Git tutoring assistant') and the instruction 'Answer ONLY based on the provided context' significantly reduced hallucinations. The model is now limited to only the provided context.


### Example 2: Adding fallback rule


```python

# V1: No fallback rule

# V2: Added instruction:

#  "2. If the context does not contain enough information, say:
#   I do not have enough information..."

```


**Problem**: For the 'How do I view the commit history?' query, the model tried to guess an answer because the topic was not well covered in the knowledge base. This led to hallucinated answers that were not based on facts.


**Result analysis**: A clear fallback rule allows the model to honestly admit missing information. For uncovered topics, the model now returns 'I do not have enough information' instead of making up an answer.


### Example 3: Mandatory source citations


```python

# V1: No requirement to cite sources

# V2: Added instruction:

#  "4. Always cite the source chunk ID or source file used in your answer."

```


**Problem**: Answers did not include source references, making it difficult to verify correctness and traceability of answers.


**Result analysis**: Requiring chunk_id and source_file citations makes answers verifiable. Every statement can be traced back to a specific part of the document.

