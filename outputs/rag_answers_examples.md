# HW4: RAG Answer Generation — Test Results

**Embedding model**: `sentence-transformers/all-MiniLM-L6-v2`

**Index**: FAISS IndexFlatIP (dim=384)

**Chunks in KB**: 145

**LLM**: `nvidia/nemotron-3-nano-30b-a3b:free` via `https://openrouter.ai/api/v1`

**Relevance threshold**: 0.3


## Summary Table

| # | Question | Top-1 score | Result |
|---|----------|-------------|--------|
| 1 | How do I clone a Git repository? | 0.68 | ✅ Grounded |
| 2 | What is a Git branch and how do I create one? | 0.63 | ❌ Fallback |
| 3 | How to resolve merge conflicts in Git? | 0.74 | ✅ Grounded |
| 4 | What is the difference between git add and git commit? | 0.63 | ✅ Grounded |
| 5 | How do I stash my changes temporarily? | 0.63 | ✅ Grounded |
| 6 | How do I merge a branch in GitLab? | 0.69 | ✅ Grounded |
| 7 | How do I view the commit history? | 0.58 | ❌ Fallback |
| 8 | How to set up SSH keys for GitLab? | 0.74 | ✅ Grounded |
| 9 | What is rebasing and when should I use it? | 0.54 | ✅ Grounded |
| 10 | How do I push changes to a remote repository? | 0.71 | ✅ Grounded |

## Question 1: How do I clone a Git repository?

**Retrieved chunks**: git_basics_getting_repository_chunk_006 (score: 0.68), gitlab_getting_started_chunk_003 (score: 0.64), git_basics_getting_repository_chunk_002 (score: 0.63)

**Answer**: To clone a repository you run `git clone <url>` which creates a new directory, initializes a `.git` folder inside it, pulls down all of the repository’s data, and checks out a working copy of the latest version. This description is given in chunk [1].

**Source**: data/raw/01_git_basics_getting_repository.md

**Comment**: Grounded — answer based on relevant chunk


## Question 2: What is a Git branch and how do I create one?

**Retrieved chunks**: gitlab_getting_started_chunk_001 (score: 0.63), github_about_git_chunk_007 (score: 0.61), github_about_git_chunk_004 (score: 0.61)

**Answer**: I do not have enough information in the available documents to answer this question.

**Source**: data/raw/09_gitlab_getting_started.md

**Comment**: Fallback — insufficient relevant context


## Question 3: How to resolve merge conflicts in Git?

**Retrieved chunks**: branching_basic_branching_merging_chunk_016 (score: 0.74), branching_basic_branching_merging_chunk_013 (score: 0.73), branching_basic_branching_merging_chunk_011 (score: 0.72)

**Answer**: To resolve a merge conflict you first look at the conflicted files (Git will mark them as “both modified”).  
Edit each file to keep the desired version of the content, then **stage the resolved file** with `git add`.  
After all conflicts are staged, finish the merge by committing the result (`git commit` or `git commit` to conclude the merge).  
If you prefer a visual aid, you can run `git mergetool` to launch a merge‑tool that helps you resolve the conflicts.  

**Sources:**  
- [1] Chunk branching_basic_branching_merging_chunk_016 – “verify that all conflicts have been resolved… use “git commit” to conclude merge”  
- [4] Chunk branching_basic_branching_merging_chunk_014 – “Staging the file marks it as resolved in Git… you can run `git mergetool`”  
- [13] Chunk branching_basic_branching_merging_chunk_013 – describes the conflict and the need to resolve it before proceeding.

**Source**: data/raw/03_branching_basic_branching_merging.md

**Comment**: Grounded — answer based on relevant chunk


## Question 4: What is the difference between git add and git commit?

**Retrieved chunks**: github_about_git_chunk_009 (score: 0.63), gitlab_getting_started_chunk_002 (score: 0.62), github_about_git_chunk_008 (score: 0.61)

**Answer**: **Answer**

- **`git add`** – This command stages the changes you have made to files. It moves the modified files from the working directory into the *index* (the staging area) so that those specific changes are prepared to be included in the next commit. [4]

- **`git commit`** – This command takes the staged changes and records them as a new commit in the repository’s history. It creates a permanent snapshot of the project at that point, using the files that were staged by `git add`. [1]

**Citations**

- The description of `git commit` as creating a snapshot comes from Chunk [1] (github_about_git_chunk_009).  
- The relationship between staging with `git add` and then committing is explained in Chunk [4] (git_basics_recording_changes_chunk_007).

**Source**: data/raw/08_github_about_git.md

**Comment**: Grounded — answer based on relevant chunk


## Question 5: How do I stash my changes temporarily?

**Retrieved chunks**: git_tools_stashing_cleaning_chunk_002 (score: 0.63), git_tools_stashing_cleaning_chunk_001 (score: 0.62), git_tools_stashing_cleaning_chunk_004 (score: 0.55)

**Answer**: To stash your changes temporarily you can use the **`git stash push`** command (the newer replacement for the deprecated `git stash save`). After stashing, the changes are saved on a stack and you can later bring them back with **`git stash apply`** (or `git stash pop` to apply and drop them).  

- The deprecation of `git stash save` in favor of `git stash push` is noted in chunk **[1]**.  
- The usage of `git stash apply` to restore a stashed change is described in chunk **[5]**.  

So, run `git stash push` to temporarily stash your modifications, and later run `git stash apply` (or `git stash pop`) to retrieve them.

**Source**: data/raw/07_git_tools_stashing_cleaning.md

**Comment**: Grounded — answer based on relevant chunk


## Question 6: How do I merge a branch in GitLab?

**Retrieved chunks**: gitlab_getting_started_chunk_005 (score: 0.69), gitlab_getting_started_chunk_004 (score: 0.69), gitlab_getting_started_chunk_009 (score: 0.58)

**Answer**: To merge a branch in GitLab you can do it either through the GitLab user interface or from the command line.  

**Using the GitLab UI**  
1. Open the repository and go to the **Merge Requests** page.  
2. Click **New merge request**, select the source branch you want to merge and the target branch you want to merge into.  
3. Review the changes and click **Merge** to complete the merge.

**Using the command line**  
1. Checkout the branch you want to merge into (the target branch).  
2. Run `git merge <source‑branch>` to merge the source branch into the current branch.  
3. Push the result to the remote repository if needed.  

These steps are outlined in the GitLab documentation for getting started with Git.  

[1] Chunk: gitlab_getting_started_chunk_005 | Score: 0.6909 | Source: data/raw/09_gitlab_getting_started.md | Section: Get started with Git

**Source**: data/raw/09_gitlab_getting_started.md

**Comment**: Grounded — answer based on relevant chunk


## Question 7: How do I view the commit history?

**Retrieved chunks**: github_about_git_chunk_001 (score: 0.58), git_basics_recording_changes_chunk_027 (score: 0.55), git_basics_recording_changes_chunk_028 (score: 0.54)

**Answer**: I do not have enough information in the available documents to answer this question.

**Source**: data/raw/08_github_about_git.md

**Comment**: Fallback — insufficient relevant context


## Question 8: How to set up SSH keys for GitLab?

**Retrieved chunks**: gitlab_getting_started_chunk_010 (score: 0.74), gitlab_getting_started_chunk_009 (score: 0.61), gitlab_getting_started_chunk_001 (score: 0.52)

**Answer**: To set up SSH keys for GitLab you need to **generate an SSH key pair on your local system and then add that key to your GitLab account** so that you can authenticate Git operations over SSH without entering a password each time. This process is outlined in the “Get started with Git” section of the GitLab getting‑started guide [1].

**Source**: data/raw/09_gitlab_getting_started.md

**Comment**: Grounded — answer based on relevant chunk


## Question 9: What is rebasing and when should I use it?

**Retrieved chunks**: git_tools_rebasing_chunk_001 (score: 0.54), git_tools_rebasing_chunk_018 (score: 0.54), git_tools_rebasing_chunk_009 (score: 0.54)

**Answer**: Rebasing is a Git operation that **rewrites the commit history of a branch by moving (or “replaying”) its commits onto a new base commit**, creating a linear history that looks as if all the changes were made sequentially [1][4].  

**When to use it**  
- When you want a clean, linear project history and are preparing a branch to be integrated or shared [2].  
- When you need to keep the repository’s history tidy before pushing your work to a remote repository [2].  
- When you want to combine or reorder commits locally before they become part of the shared history [1][4].  

**Caveats**  
- Rebasing should generally be done on commits that have not yet been published or shared with others, because it rewrites history [3].  
- If you rebase commits that others have based work on, you may cause confusion or conflicts for them [3].  

In short, use rebasing to maintain a clear, linear commit history for your own work or for branches that have not yet been made public, but avoid rebasing commits that are already part of a shared repository.  

**Sources**: [1], [2], [3], [4] (all from *git_tools_rebasing_chunk_*.md).

**Source**: data/raw/06_git_tools_rebasing.md

**Comment**: Partial — context partially relevant


## Question 10: How do I push changes to a remote repository?

**Retrieved chunks**: github_about_git_chunk_010 (score: 0.71), git_basics_getting_repository_chunk_002 (score: 0.70), github_about_git_chunk_012 (score: 0.66)

**Answer**: To push changes to a remote repository you use the `git push` command. This command updates the remote repository with any commits that you have made locally on a branch.  

**Source:** Chunk [1] – “github_about_git_chunk_010” (Section: About Git) – bullet point “* `git push` updates the remote repository with any commits made locally to a branch.”

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

