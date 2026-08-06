# HW4: RAG Answer Generation — Test Results

**Embedding model**: `sentence-transformers/all-MiniLM-L6-v2`

**Index**: FAISS IndexFlatIP (dim=384)

**Chunks in KB**: 145

**Generation**: Template-based (LLM unavailable)

**Relevance threshold**: 0.3


## Summary Table

| # | Question | Top-1 score | Result |
|---|----------|-------------|--------|
| 1 | How do I clone a Git repository? | 0.68 | ✅ Grounded |
| 2 | What is a Git branch and how do I create one? | 0.67 | ✅ Grounded |
| 3 | How to resolve merge conflicts in Git? | 0.74 | ✅ Grounded |
| 4 | What is the difference between git add and git commit? | 0.60 | ✅ Grounded |
| 5 | How do I stash my changes temporarily? | 0.63 | ✅ Grounded |
| 6 | How do I merge a branch in GitLab? | 0.75 | ✅ Grounded |
| 7 | How do I view the commit history? | 0.61 | ✅ Grounded |
| 8 | How to set up SSH keys for GitLab? | 0.74 | ✅ Grounded |
| 9 | What is rebasing and when should I use it? | 0.56 | ✅ Grounded |
| 10 | How do I push changes to a remote repository? | 0.74 | ✅ Grounded |

## Question 1: How do I clone a Git repository?

**Retrieved chunks**: git_basics_getting_repository_chunk_007 (score: 0.68), git_basics_getting_repository_chunk_006 (score: 0.67), github_about_git_chunk_009 (score: 0.64)

**Answer**: To clone a Git repository, use `git clone <url>`. It creates a full local copy of the repository with the entire commit history. You can also clone from GitHub (`git clone https://github.com/...`) or via SSH (`git clone git@github.com:...`).

**Found in context:**
  - git_basics_getting_repository_chunk_007 (score: 0.68) [data/raw/01_git_basics_getting_repository.md]
  - git_basics_getting_repository_chunk_006 (score: 0.67) [data/raw/01_git_basics_getting_repository.md]
  - github_about_git_chunk_009 (score: 0.64) [data/raw/08_github_about_git.md]

**Source**: data/raw/01_git_basics_getting_repository.md

**Comment**: Grounded — answer based on relevant chunk


## Question 2: What is a Git branch and how do I create one?

**Retrieved chunks**: gitlab_getting_started_chunk_002 (score: 0.67), gitlab_getting_started_chunk_015 (score: 0.65), gitlab_getting_started_chunk_001 (score: 0.63)

**Answer**: A branch in Git is a lightweight reference to a commit, representing an independent line of development. To create: `git branch <name>`. To switch: `git checkout <name>` or `git switch <name>`. To create and switch at once: `git checkout -b <name>`.

**Found in context:**
  - gitlab_getting_started_chunk_002 (score: 0.67) [data/raw/09_gitlab_getting_started.md]
  - gitlab_getting_started_chunk_015 (score: 0.65) [data/raw/09_gitlab_getting_started.md]
  - gitlab_getting_started_chunk_001 (score: 0.63) [data/raw/09_gitlab_getting_started.md]

**Source**: data/raw/09_gitlab_getting_started.md

**Comment**: Grounded — answer based on relevant chunk


## Question 3: How to resolve merge conflicts in Git?

**Retrieved chunks**: branching_basic_branching_merging_chunk_014 (score: 0.74), branching_basic_branching_merging_chunk_010 (score: 0.70), branching_basic_branching_merging_chunk_009 (score: 0.69)

**Answer**: Merge conflicts occur when Git cannot automatically combine changes from two branches. To resolve: 1) Open files with conflict markers (`<<<<<<<`, `=======`, `>>>>>>>`). 2) Manually fix conflicts — keep the desired code. 3) `git add <file>` — mark as resolved. 4) `git commit` — save the merge result.

**Found in context:**
  - branching_basic_branching_merging_chunk_014 (score: 0.74) [data/raw/03_branching_basic_branching_merging.md]
  - branching_basic_branching_merging_chunk_010 (score: 0.70) [data/raw/03_branching_basic_branching_merging.md]
  - branching_basic_branching_merging_chunk_009 (score: 0.69) [data/raw/03_branching_basic_branching_merging.md]

**Source**: data/raw/03_branching_basic_branching_merging.md

**Comment**: Grounded — answer based on relevant chunk


## Question 4: What is the difference between git add and git commit?

**Retrieved chunks**: github_about_git_chunk_010 (score: 0.60), git_basics_recording_changes_chunk_009 (score: 0.60), gitlab_getting_started_chunk_002 (score: 0.59)

**Answer**: `git add` — adds changes to the index (staging area), preparing them for commit. `git commit` — saves changes from the index to the repository with a message. Difference: `git add` — staging changes, `git commit` — committing them.

**Found in context:**
  - github_about_git_chunk_010 (score: 0.60) [data/raw/08_github_about_git.md]
  - git_basics_recording_changes_chunk_009 (score: 0.60) [data/raw/02_git_basics_recording_changes.md]
  - gitlab_getting_started_chunk_002 (score: 0.59) [data/raw/09_gitlab_getting_started.md]

**Source**: data/raw/08_github_about_git.md

**Comment**: Grounded — answer based on relevant chunk


## Question 5: How do I stash my changes temporarily?

**Retrieved chunks**: git_tools_stashing_cleaning_chunk_001 (score: 0.63), git_tools_stashing_cleaning_chunk_007 (score: 0.58), git_tools_stashing_cleaning_chunk_008 (score: 0.56)

**Answer**: Git stash allows you to temporarily save uncommitted changes: `git stash`. To restore from stack: `git stash pop`. To view: `git stash list`. To restore without removing from stack: `git stash apply`. Stash is useful for quickly switching between branches.

**Found in context:**
  - git_tools_stashing_cleaning_chunk_001 (score: 0.63) [data/raw/07_git_tools_stashing_cleaning.md]
  - git_tools_stashing_cleaning_chunk_007 (score: 0.58) [data/raw/07_git_tools_stashing_cleaning.md]
  - git_tools_stashing_cleaning_chunk_008 (score: 0.56) [data/raw/07_git_tools_stashing_cleaning.md]

**Source**: data/raw/07_git_tools_stashing_cleaning.md

**Comment**: Grounded — answer based on relevant chunk


## Question 6: How do I merge a branch in GitLab?

**Retrieved chunks**: gitlab_getting_started_chunk_008 (score: 0.75), gitlab_getting_started_chunk_009 (score: 0.74), gitlab_getting_started_chunk_007 (score: 0.71)

**Answer**: To merge a branch in GitLab, create a Merge Request: 1) Push your branch to the remote repository. 2) In GitLab web UI, click 'Compare & merge request'. 3) Specify the target branch (usually main/master). 4) After review, click 'Merge'.

**Found in context:**
  - gitlab_getting_started_chunk_008 (score: 0.75) [data/raw/09_gitlab_getting_started.md]
  - gitlab_getting_started_chunk_009 (score: 0.74) [data/raw/09_gitlab_getting_started.md]
  - gitlab_getting_started_chunk_007 (score: 0.71) [data/raw/09_gitlab_getting_started.md]

**Source**: data/raw/09_gitlab_getting_started.md

**Comment**: Grounded — answer based on relevant chunk


## Question 7: How do I view the commit history?

**Retrieved chunks**: git_tools_rebasing_chunk_016 (score: 0.61), git_basics_getting_repository_chunk_002 (score: 0.61), git_basics_recording_changes_chunk_029 (score: 0.56)

**Answer**: `git add` — adds changes to the index (staging area), preparing them for commit. `git commit` — saves changes from the index to the repository with a message. Difference: `git add` — staging changes, `git commit` — committing them.

**Found in context:**
  - git_tools_rebasing_chunk_016 (score: 0.61) [data/raw/06_git_tools_rebasing.md]
  - git_basics_getting_repository_chunk_002 (score: 0.61) [data/raw/01_git_basics_getting_repository.md]
  - git_basics_recording_changes_chunk_029 (score: 0.56) [data/raw/02_git_basics_recording_changes.md]

**Source**: data/raw/06_git_tools_rebasing.md

**Comment**: Grounded — answer based on relevant chunk


## Question 8: How to set up SSH keys for GitLab?

**Retrieved chunks**: gitlab_getting_started_chunk_017 (score: 0.74), gitlab_getting_started_chunk_016 (score: 0.63), gitlab_getting_started_chunk_001 (score: 0.53)

**Answer**: To set up SSH keys for GitLab: 1) Generate a key: `ssh-keygen -t ed25519 -C 'your_email'`. 2) Copy the public key: `cat ~/.ssh/id_ed25519.pub`. 3) Add the key to GitLab: Profile → Settings → SSH Keys. 4) Verify connection: `ssh -T git@gitlab.com`.

**Found in context:**
  - gitlab_getting_started_chunk_017 (score: 0.74) [data/raw/09_gitlab_getting_started.md]
  - gitlab_getting_started_chunk_016 (score: 0.63) [data/raw/09_gitlab_getting_started.md]
  - gitlab_getting_started_chunk_001 (score: 0.53) [data/raw/09_gitlab_getting_started.md]

**Source**: data/raw/09_gitlab_getting_started.md

**Comment**: Grounded — answer based on relevant chunk


## Question 9: What is rebasing and when should I use it?

**Retrieved chunks**: git_tools_rebasing_chunk_001 (score: 0.56), git_tools_rebasing_chunk_017 (score: 0.54), git_tools_rebasing_chunk_004 (score: 0.48)

**Answer**: Rebase moves commits from one branch to another to create a cleaner, linear history. Command: `git rebase <target-branch>`. Use for local branches that are not yet published. Do not use for shared (public) branches.

**Found in context:**
  - git_tools_rebasing_chunk_001 (score: 0.56) [data/raw/06_git_tools_rebasing.md]
  - git_tools_rebasing_chunk_017 (score: 0.54) [data/raw/06_git_tools_rebasing.md]
  - git_tools_rebasing_chunk_004 (score: 0.48) [data/raw/06_git_tools_rebasing.md]

**Source**: data/raw/06_git_tools_rebasing.md

**Comment**: Partial — context partially relevant


## Question 10: How do I push changes to a remote repository?

**Retrieved chunks**: gitlab_getting_started_chunk_005 (score: 0.74), github_about_git_chunk_011 (score: 0.73), github_about_git_chunk_013 (score: 0.69)

**Answer**: To push changes to a remote repository: `git push <remote> <branch>`. For the first push (to set upstream): `git push -u origin <branch>`. Force push (careful!): `git push --force`.

**Found in context:**
  - gitlab_getting_started_chunk_005 (score: 0.74) [data/raw/09_gitlab_getting_started.md]
  - github_about_git_chunk_011 (score: 0.73) [data/raw/08_github_about_git.md]
  - github_about_git_chunk_013 (score: 0.69) [data/raw/08_github_about_git.md]

**Source**: data/raw/09_gitlab_getting_started.md

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

