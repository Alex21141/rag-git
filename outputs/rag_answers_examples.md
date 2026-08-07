# HW4: RAG Answer Generation — Test Results

**Embedding model**: `sentence-transformers/all-MiniLM-L6-v2`

**Index**: FAISS IndexFlatIP (dim=384)

**Chunks in KB**: 145

**LLM**: `nvidia/nemotron-3-ultra-550b-a55b:free` via `https://openrouter.ai/api/v1`

**Relevance threshold**: 0.3


## Summary Table

| # | Question | Top-1 score | Result |
|---|----------|-------------|--------|
| 1 | How do I clone a Git repository? | 0.68 | ❌ Fallback |
| 2 | What is a Git branch and how do I create one? | 0.63 | ❌ Fallback |
| 3 | How to resolve merge conflicts in Git? | 0.74 | ✅ Grounded |
| 4 | What is the difference between git add and git commit? | 0.63 | ✅ Grounded |
| 5 | How do I stash my changes temporarily? | 0.63 | ✅ Grounded |
| 6 | How do I merge a branch in GitLab? | 0.69 | ❌ Fallback |
| 7 | How do I view the commit history? | 0.58 | ❌ Fallback |
| 8 | How to set up SSH keys for GitLab? | 0.74 | ❌ Fallback |
| 9 | What is rebasing and when should I use it? | 0.54 | ✅ Grounded |
| 10 | How do I push changes to a remote repository? | 0.71 | ✅ Grounded |

## Question 1: How do I clone a Git repository?

**Retrieved chunks**: git_basics_getting_repository_chunk_006 (score: 0.68), gitlab_getting_started_chunk_003 (score: 0.64), git_basics_getting_repository_chunk_002 (score: 0.63)

**Answer**: I do not have enough information in the available documents to answer this question. The provided context describes what happens when you clone a repository (creates a directory, initializes `.git`, pulls data, checks out a working copy) but does not specify the actual `git clone` command or its syntax.

**Source**: data/raw/01_git_basics_getting_repository.md

**Comment**: Fallback — insufficient relevant context


## Question 2: What is a Git branch and how do I create one?

**Retrieved chunks**: gitlab_getting_started_chunk_001 (score: 0.63), github_about_git_chunk_007 (score: 0.61), github_about_git_chunk_004 (score: 0.61)

**Answer**: I do not have enough information in the available documents to answer this question.

**Source**: data/raw/09_gitlab_getting_started.md

**Comment**: Fallback — insufficient relevant context


## Question 3: How to resolve merge conflicts in Git?

**Retrieved chunks**: branching_basic_branching_merging_chunk_016 (score: 0.74), branching_basic_branching_merging_chunk_013 (score: 0.73), branching_basic_branching_merging_chunk_011 (score: 0.72)

**Answer**: Based on the provided context, here's how to resolve merge conflicts in Git:

1. **Identify the conflict**: When merging, Git will report conflicts like `CONFLICT (content): Merge conflict in index.html` [11].

2. **Examine the conflict markers**: Git marks conflicted areas in files with `<<<<<<<`, `=======`, and `>>>>>>>`. The version in `HEAD` (your current branch) appears above the `=======`, while the version from the merging branch appears below [13].

3. **Resolve the conflict**: Edit the file to choose which changes to keep (or combine them manually).

4. **Mark as resolved**: Stage the resolved file using `git add` to mark it as resolved in Git [14].

5. **Optional graphical tool**: You can use `git mergetool` to launch a visual merge tool for assistance [14].

6. **Complete the merge**: After all conflicts are resolved and staged, run `git commit` to conclude the merge [16].

**Sources**: 
- Conflict detection and markers: [11], [13]
- Staging to mark resolved and mergetool: [14]
- Final commit to conclude merge: [16]

**Source**: data/raw/03_branching_basic_branching_merging.md

**Comment**: Grounded — answer based on relevant chunk


## Question 4: What is the difference between git add and git commit?

**Retrieved chunks**: github_about_git_chunk_009 (score: 0.63), gitlab_getting_started_chunk_002 (score: 0.62), github_about_git_chunk_008 (score: 0.61)

**Answer**: Based on the provided context, the difference between `git add` and `git commit` is:

- **`git add`** performs **staging**, which is the first part of a two-step process to include changes in the project's history. It prepares changes (e.g., modified files) to be included in the next snapshot. [3]
- **`git commit`** takes a **snapshot** of the staged changes and records them permanently in the repository's history. The version of the file at the time you ran `git add` is what becomes part of that historical snapshot. [4][1]

In short, `git add` stages changes, and `git commit` saves those staged changes as a commit in the project history.

**Source**: data/raw/08_github_about_git.md

**Comment**: Grounded — answer based on relevant chunk


## Question 5: How do I stash my changes temporarily?

**Retrieved chunks**: git_tools_stashing_cleaning_chunk_002 (score: 0.63), git_tools_stashing_cleaning_chunk_001 (score: 0.62), git_tools_stashing_cleaning_chunk_004 (score: 0.55)

**Answer**: Git stash allows you to temporarily save uncommitted changes: `git stash`. To restore from stack: `git stash pop`. To view: `git stash list`. To restore without removing from stack: `git stash apply`. Stash is useful for quickly switching between branches.

**Found in context:**
  - git_tools_stashing_cleaning_chunk_002 (score: 0.63) [data/raw/07_git_tools_stashing_cleaning.md]
  - git_tools_stashing_cleaning_chunk_001 (score: 0.62) [data/raw/07_git_tools_stashing_cleaning.md]
  - git_tools_stashing_cleaning_chunk_004 (score: 0.55) [data/raw/07_git_tools_stashing_cleaning.md]

**Source**: data/raw/07_git_tools_stashing_cleaning.md

**Comment**: Grounded — answer based on relevant chunk


## Question 6: How do I merge a branch in GitLab?

**Retrieved chunks**: gitlab_getting_started_chunk_005 (score: 0.69), gitlab_getting_started_chunk_004 (score: 0.69), gitlab_getting_started_chunk_009 (score: 0.58)

**Answer**: I do not have enough information in the available documents to answer this question. The provided context chunks mention merge conflicts and branch deletion after a successful merge (Chunk 1), and general branching concepts (Chunk 2), but do not contain specific instructions on how to perform a merge in GitLab.

**Source**: data/raw/09_gitlab_getting_started.md

**Comment**: Fallback — insufficient relevant context


## Question 7: How do I view the commit history?

**Retrieved chunks**: github_about_git_chunk_001 (score: 0.58), git_basics_recording_changes_chunk_027 (score: 0.55), git_basics_recording_changes_chunk_028 (score: 0.54)

**Answer**: I do not have enough information in the available documents to answer this question.

**Source**: data/raw/08_github_about_git.md

**Comment**: Fallback — insufficient relevant context


## Question 8: How to set up SSH keys for GitLab?

**Retrieved chunks**: gitlab_getting_started_chunk_010 (score: 0.74), gitlab_getting_started_chunk_009 (score: 0.61), gitlab_getting_started_chunk_001 (score: 0.52)

**Answer**: I do not have enough information in the available documents to answer this question. The provided context only mentions that to use SSH with GitLab you must "Generate an SSH key pair on your local system" and "Add your SSH key to your Git" (chunk gitlab_getting_started_chunk_010), but the instructions are incomplete and don't explain the actual steps for generating keys or adding them to GitLab.

**Source**: data/raw/09_gitlab_getting_started.md

**Comment**: Fallback — insufficient relevant context


## Question 9: What is rebasing and when should I use it?

**Retrieved chunks**: git_tools_rebasing_chunk_001 (score: 0.54), git_tools_rebasing_chunk_018 (score: 0.54), git_tools_rebasing_chunk_009 (score: 0.54)

**Answer**: Rebase moves commits from one branch to another to create a cleaner, linear history. Command: `git rebase <target-branch>`. Use for local branches that are not yet published. Do not use for shared (public) branches.

**Found in context:**
  - git_tools_rebasing_chunk_001 (score: 0.54) [data/raw/06_git_tools_rebasing.md]
  - git_tools_rebasing_chunk_018 (score: 0.54) [data/raw/06_git_tools_rebasing.md]
  - git_tools_rebasing_chunk_009 (score: 0.54) [data/raw/06_git_tools_rebasing.md]

**Source**: data/raw/06_git_tools_rebasing.md

**Comment**: Partial — context partially relevant


## Question 10: How do I push changes to a remote repository?

**Retrieved chunks**: github_about_git_chunk_010 (score: 0.71), git_basics_getting_repository_chunk_002 (score: 0.70), github_about_git_chunk_012 (score: 0.66)

**Answer**: Based on the provided context, you can push changes to a remote repository using the `git push` command. According to the documentation, "`git push` updates the remote repository with any commits made locally to a branch." [1]

[1] Chunk: github_about_git_chunk_010 | Source: data/raw/08_github_about_git.md | Section: About Git

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

Context:
{context}

Question: {question}

Answer:
```


**Problem**: For the 'How do I view the commit history?' query, the model tried to guess an answer because the topic was not well covered in the knowledge base. This led to hallucinated answers that were not based on facts.


**Result analysis**: A clear fallback rule allows the model to honestly admit missing information. For uncovered topics, the model now returns 'I do not have enough information' instead of making up an answer.


### Example 3: Mandatory source citations


#### Original prompt (v1)

```

You are a Git tutoring assistant. Your job is to answer questions about Git, GitHub, and GitLab.

IMPORTANT RULES:
1. Answer ONLY based on the provided context below.
2. If the context does not contain enough information to answer the question, say:
   "I do not have enough information in the available documents to answer this question."
3. Do NOT use any general knowledge outside the provided context.

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


**Problem**: Answers did not include source references, making it difficult to verify correctness and traceability of answers.


**Result analysis**: Requiring chunk_id and source_file citations makes answers verifiable. Every statement can be traced back to a specific part of the document.

