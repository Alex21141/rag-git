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

**Answer**: Based on the provided context, I do not have enough information to answer this question. The available chunks mention concepts related to obtaining a Git repository (e.g., "creates a directory named `libgit2`, initializes a `.git` directory inside it, pulls down all the data for that repository, and checks out a working copy of the latest version" [1], and "you create a local copy of the repository in your working directory" [2]), but they do not specify the actual `git clone` command or its usage.

**Source**: data/raw/01_git_basics_getting_repository.md

**Comment**: Grounded — answer based on relevant chunk


## Question 2: What is a Git branch and how do I create one?

**Retrieved chunks**: gitlab_getting_started_chunk_001 (score: 0.63), github_about_git_chunk_007 (score: 0.61), github_about_git_chunk_004 (score: 0.61)

**Answer**: I do not have enough information in the available documents to answer this question.

The provided context mentions Git branching in [Chunk 4](branching_branch_management_chunk_001) which discusses "Branch Management" and references creating, merging, and deleting branches, but it does not define what a Git branch is or provide the specific commands to create one. Other chunks ([1], [2], [3], [5]) discuss Git basics, commands, and repositories but do not cover branch creation.

**Source**: data/raw/09_gitlab_getting_started.md

**Comment**: Grounded — answer based on relevant chunk


## Question 3: How to resolve merge conflicts in Git?

**Retrieved chunks**: branching_basic_branching_merging_chunk_016 (score: 0.74), branching_basic_branching_merging_chunk_013 (score: 0.73), branching_basic_branching_merging_chunk_011 (score: 0.72)

**Answer**: Based on the provided context, here's how to resolve merge conflicts in Git:

1. **Identify the conflict**: When merging, Git will indicate conflicts with messages like `CONFLICT (content): Merge conflict in index.html` [11].

2. **Examine the conflict markers**: The conflicted file will contain conflict markers showing both versions:
   - The top part (above `=======`) represents one version
   - The bottom part (below `=======`) represents the other version (e.g., from `iss53` branch) [13].

3. **Resolve the conflict**: Edit the file to choose which changes to keep (or combine them manually).

4. **Mark as resolved**: Stage the resolved file using `git add` to mark it as resolved in Git [14].

5. **Optional graphical tool**: You can use `git mergetool` to launch a visual merge tool for easier resolution [14].

6. **Complete the merge**: After all conflicts are fixed, run `git status` to verify ("All conflicts fixed but you are still merging"), then run `git commit` to conclude the merge [16].

**Sources**: [11], [13], [14], [16]

**Source**: data/raw/03_branching_basic_branching_merging.md

**Comment**: Grounded — answer based on relevant chunk


## Question 4: What is the difference between git add and git commit?

**Retrieved chunks**: github_about_git_chunk_009 (score: 0.63), gitlab_getting_started_chunk_002 (score: 0.62), github_about_git_chunk_008 (score: 0.61)

**Answer**: Based on the provided context, the difference between `git add` and `git commit` is:

- **`git add`** stages changes, placing them under the "Changes to be committed" heading. It prepares the current version of a file to be included in the next snapshot. As noted in the Git Basics documentation: "the version of the file at the time you ran `git add` is what will be in the subsequent historical snapshot" [4].

- **`git commit`** takes a snapshot of the staged changes and records them permanently in the project's history. The About Git documentation describes this as a two-step process: "it's necessary to stage and take a snapshot of the changes to include them in the project's history. This command performs staging, the first part of that two-st[ep process]" [3], with `git commit` being the second step that creates the snapshot.

In summary, `git add` prepares (stages) changes, while `git commit` finalizes them into a historical snapshot.

Sources: [3], [4]

**Source**: data/raw/08_github_about_git.md

**Comment**: Grounded — answer based on relevant chunk


## Question 5: How do I stash my changes temporarily?

**Retrieved chunks**: git_tools_stashing_cleaning_chunk_002 (score: 0.63), git_tools_stashing_cleaning_chunk_001 (score: 0.62), git_tools_stashing_cleaning_chunk_004 (score: 0.55)

**Answer**: Based on the provided context, you can stash your changes temporarily using the command `git stash push`. The context indicates that `git stash save` is being deprecated in favor of `git stash push` [1].

**Source:** [1] Chunk: git_tools_stashing_cleaning_chunk_002

**Source**: data/raw/07_git_tools_stashing_cleaning.md

**Comment**: Grounded — answer based on relevant chunk


## Question 6: How do I merge a branch in GitLab?

**Retrieved chunks**: gitlab_getting_started_chunk_005 (score: 0.69), gitlab_getting_started_chunk_004 (score: 0.69), gitlab_getting_started_chunk_009 (score: 0.58)

**Answer**: I do not have enough information in the available documents to answer this question. The provided context mentions merge conflicts and deleting branches after a successful merge (Chunk 1), and discusses branching concepts (Chunk 2) and general Git commands (Chunk 3), but does not contain specific instructions on how to perform a merge in GitLab.

**Source**: data/raw/09_gitlab_getting_started.md

**Comment**: Grounded — answer based on relevant chunk


## Question 7: How do I view the commit history?

**Retrieved chunks**: github_about_git_chunk_001 (score: 0.58), git_basics_recording_changes_chunk_027 (score: 0.55), git_basics_recording_changes_chunk_028 (score: 0.54)

**Answer**: I do not have enough information in the available documents to answer this question.

**Source**: data/raw/08_github_about_git.md

**Comment**: Partial — context partially relevant


## Question 8: How to set up SSH keys for GitLab?

**Retrieved chunks**: gitlab_getting_started_chunk_010 (score: 0.74), gitlab_getting_started_chunk_009 (score: 0.61), gitlab_getting_started_chunk_001 (score: 0.52)

**Answer**: Based on the provided context, to set up SSH keys for GitLab you must:

1. Generate an SSH key pair on your local system.
2. Add your SSH key to your GitLab account (the text cuts off at "Add your SSH key to your Git").

Source: [1] Chunk: gitlab_getting_started_chunk_010

**Source**: data/raw/09_gitlab_getting_started.md

**Comment**: Grounded — answer based on relevant chunk


## Question 9: What is rebasing and when should I use it?

**Retrieved chunks**: git_tools_rebasing_chunk_001 (score: 0.54), git_tools_rebasing_chunk_018 (score: 0.54), git_tools_rebasing_chunk_009 (score: 0.54)

**Answer**: Based on the provided context, here's what I can tell you about rebasing:

**What is rebasing?**
- Rebasing is one of two main ways to integrate changes from one branch into another (the other being `merge`) [1].
- When you examine the log of a rebased branch, it looks like a linear history: it appears that all the work happened in series, even when it originally happened in parallel [4].
- Rebasing replays changes from one branch onto another; the final snapshot is the same as with a merge, but the history is different [5].

**When should you use it?**
- The context suggests that "it's up to you to decide which one is best for your particular situation" after understanding how both merge and rebase work [2].
- There's an important guideline: you should not rebase commits that exist outside your repository and that people may have based work on. If you follow this guideline, "you'll be fine. If you don't, people will hate you, and you'll be scorned by friends and..." [3].
- Often, rebasing is done "to make sure y..." (the text cuts off) [4].

The provided context doesn't contain a complete explanation of all scenarios where rebasing is recommended versus merging. For more detailed guidance on when to choose rebase over merge, additional context would be needed.

**Source**: data/raw/06_git_tools_rebasing.md

**Comment**: Partial — context partially relevant


## Question 10: How do I push changes to a remote repository?

**Retrieved chunks**: github_about_git_chunk_010 (score: 0.71), git_basics_getting_repository_chunk_002 (score: 0.70), github_about_git_chunk_012 (score: 0.66)

**Answer**: To push changes to a remote repository: `git push <remote> <branch>`. For the first push (to set upstream): `git push -u origin <branch>`. Force push (careful!): `git push --force`.

**Found in context:**
  - github_about_git_chunk_010 (score: 0.71) [data/raw/08_github_about_git.md]
  - git_basics_getting_repository_chunk_002 (score: 0.70) [data/raw/01_git_basics_getting_repository.md]
  - github_about_git_chunk_012 (score: 0.66) [data/raw/08_github_about_git.md]

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

