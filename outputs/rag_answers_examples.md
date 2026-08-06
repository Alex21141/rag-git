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

**Answer**: I do not have enough information in the available documents to answer this question. The provided context mentions that obtaining a repository involves pulling down all the data and checking out a working copy [1], and creating a local copy in your working directory [2], but it does not provide the specific commands or steps to clone a repository. [1] [2]

**Source**: data/raw/01_git_basics_getting_repository.md

**Comment**: Grounded — answer based on relevant chunk


## Question 2: What is a Git branch and how do I create one?

**Retrieved chunks**: gitlab_getting_started_chunk_001 (score: 0.63), github_about_git_chunk_007 (score: 0.61), github_about_git_chunk_004 (score: 0.61)

**Answer**: I do not have enough information in the available documents to answer this question. (Source: [4] Chunk: branching_branch_management_chunk_001)

**Source**: data/raw/09_gitlab_getting_started.md

**Comment**: Grounded — answer based on relevant chunk


## Question 3: How to resolve merge conflicts in Git?

**Retrieved chunks**: branching_basic_branching_merging_chunk_016 (score: 0.74), branching_basic_branching_merging_chunk_013 (score: 0.73), branching_basic_branching_merging_chunk_011 (score: 0.72)

**Answer**: Based on the provided documents, you can resolve merge conflicts in Git by following these steps:

1. **Edit the conflicting sections**: Merge conflicts appear as blocks separated by `=======`, showing the different versions of the code. You must manually edit the file to fix these sections [2].
2. **Mark the file as resolved**: After editing, stage the file. Staging the file marks it as resolved in Git [4]. Alternatively, you can use a graphical interface to resolve the issues by running `git mergetool` [4].
3. **Verify resolution**: Run `git status` to confirm that all conflicts have been resolved [1].
4. **Conclude the merge**: Once verified, finish the merge process by running `git commit` [1].

*Sources: [1], [2], [4]*

**Source**: data/raw/03_branching_basic_branching_merging.md

**Comment**: Grounded — answer based on relevant chunk


## Question 4: What is the difference between git add and git commit?

**Retrieved chunks**: github_about_git_chunk_009 (score: 0.63), gitlab_getting_started_chunk_002 (score: 0.62), github_about_git_chunk_008 (score: 0.61)

**Answer**: Based on the provided context, `git add` is used to stage changes, which is the first step in preparing them to be included in the project's history. `git commit` then takes a snapshot of those staged changes to record them in the project's history. Specifically, the version of the file that gets committed is exactly the version that was staged when `git add` was run [3, 4].

**Source**: data/raw/08_github_about_git.md

**Comment**: Grounded — answer based on relevant chunk


## Question 5: How do I stash my changes temporarily?

**Retrieved chunks**: git_tools_stashing_cleaning_chunk_002 (score: 0.63), git_tools_stashing_cleaning_chunk_001 (score: 0.62), git_tools_stashing_cleaning_chunk_004 (score: 0.55)

**Answer**: Based on the provided context, you can temporarily shelve your changes using the `git stash push` command. The context notes that `git stash save` is being deprecated in favor of `git stash push` [1]. This is useful when your working directory is in a messy state and you need to switch branches temporarily to work on something else [2].

**Source**: data/raw/07_git_tools_stashing_cleaning.md

**Comment**: Grounded — answer based on relevant chunk


## Question 6: How do I merge a branch in GitLab?

**Retrieved chunks**: gitlab_getting_started_chunk_005 (score: 0.69), gitlab_getting_started_chunk_004 (score: 0.69), gitlab_getting_started_chunk_009 (score: 0.58)

**Answer**: I do not have enough information in the available documents to answer this question. (Sources: [1], [5])

**Source**: data/raw/09_gitlab_getting_started.md

**Comment**: Grounded — answer based on relevant chunk


## Question 7: How do I view the commit history?

**Retrieved chunks**: github_about_git_chunk_001 (score: 0.58), git_basics_recording_changes_chunk_027 (score: 0.55), git_basics_recording_changes_chunk_028 (score: 0.54)

**Answer**: I do not have enough information in the available documents to answer this question.

**Source**: data/raw/08_github_about_git.md

**Comment**: Partial — context partially relevant


## Question 8: How to set up SSH keys for GitLab?

**Retrieved chunks**: gitlab_getting_started_chunk_010 (score: 0.74), gitlab_getting_started_chunk_009 (score: 0.61), gitlab_getting_started_chunk_001 (score: 0.52)

**Answer**: Based on the provided context, to set up SSH keys for GitLab, you must:
1. Generate an SSH key pair on your local system.
2. Add your SSH key to your Git... (Note: The provided context cuts off at this step).

**Source:** Chunk [1] (`gitlab_getting_started_chunk_010`), `data/raw/09_gitlab_getting_started.md`

**Source**: data/raw/09_gitlab_getting_started.md

**Comment**: Grounded — answer based on relevant chunk


## Question 9: What is rebasing and when should I use it?

**Retrieved chunks**: git_tools_rebasing_chunk_001 (score: 0.54), git_tools_rebasing_chunk_018 (score: 0.54), git_tools_rebasing_chunk_009 (score: 0.54)

**Answer**: Based on the provided context:

**What is rebasing?**
Rebasing is one of the two main methods for integrating changes from one branch into another (the other being `merge`). It works by replaying changes from one branch onto another. When you examine the log of a rebased branch, it displays a linear history, making it appear as though all the work happened in series, even if it originally occurred in parallel [1], [4], [5].

**When should I use it?**
You can use rebasing to create a cleaner, linear project history [4]. However, there is an important guideline: you should avoid rebasing commits that exist outside your repository or that others may have already based their work on [3]. Ultimately, whether to use rebasing or merging depends on your specific team and project requirements [2].

*Citations: [1], [2], [3], [4], [5]*

**Source**: data/raw/06_git_tools_rebasing.md

**Comment**: Partial — context partially relevant


## Question 10: How do I push changes to a remote repository?

**Retrieved chunks**: github_about_git_chunk_010 (score: 0.71), git_basics_getting_repository_chunk_002 (score: 0.70), github_about_git_chunk_012 (score: 0.66)

**Answer**: Based on the provided context, you can push changes to a remote repository using the `git push` command. This command updates the remote repository with any commits made locally to a branch [1] Chunk: github_about_git_chunk_010 | Source: data/raw/08_github_about_git.md.

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

