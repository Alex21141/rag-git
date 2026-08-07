# HW4: Генерація відповіді RAG — Результати тесту

| Параметр | Значення |
|----------|----------|
| **Embedding модель** | all-MiniLM-L6-v2 |
| **LLM модель** | nvidia/nemotron-3-nano-30b-a3b:free (OpenRouter) |
| **Індекс** | FAISS, 145 чанків, dim=384 |
| **Score threshold** | 0.30 |
| **TOP_K** | 5 |
| **LLM mode** | **Real LLM** (не template) |

## Запит 1: How do I clone a Git repository?

**Отримані чанки:** git_basics_getting_repository_chunk_006 (score: 0.68), gitlab_getting_started_chunk_003 (score: 0.64), git_basics_getting_repository_chunk_002 (score: 0.63), github_about_git_chunk_007 (score: 0.62), github_about_git_chunk_010 (score: 0.61)

**Відповідь**: To clone a Git repository you use the `git clone` command followed by the repository’s URL (and optionally a directory name).  
For example:

```bash
git clone https://github.com/owner/repo.git          # clones into a folder named “repo”
git clone https://github.com/owner/repo.git mylibgit # clones into a folder named “mylibgit”
```

The command creates a local copy of the remote repository, including all files, history, and branches, and checks out a working copy ready for you to work on [1][4][5].

**Джерело:** data/raw/01_git_basics_getting_repository.md

**Коментар:** Grounded — answer based on relevant chunk


## Запит 2: What is a Git branch and how do I create one?

**Отримані чанки:** gitlab_getting_started_chunk_001 (score: 0.63), github_about_git_chunk_007 (score: 0.61), github_about_git_chunk_004 (score: 0.61), branching_branch_management_chunk_001 (score: 0.59), gitlab_getting_started_chunk_002 (score: 0.59)

**Відповідь**: A Git branch is a separate line of development that lets you work on different versions of a project without affecting other branches. You create a new branch with the `git branch` command (e.g., `git branch feature‑x`). The branch you are currently working on is marked with an asterisk (`*`) in the output of `git branch`.  

**Source:** Chunk [4] – *branching_branch_management_chunk_001* (data/raw/04_branching_branch_management.md)

**Джерело:** data/raw/09_gitlab_getting_started.md

**Коментар:** Grounded — answer based on relevant chunk


## Запит 3: How to resolve merge conflicts in Git?

**Отримані чанки:** branching_basic_branching_merging_chunk_016 (score: 0.74), branching_basic_branching_merging_chunk_013 (score: 0.73), branching_basic_branching_merging_chunk_011 (score: 0.72), branching_basic_branching_merging_chunk_014 (score: 0.72), branching_basic_branching_merging_chunk_010 (score: 0.68)

**Відповідь**: To resolve a merge conflict you must:

1. **Identify the conflicted files** – after a failed merge run `git status` to see which files are listed under “Unmerged paths”.  
   *Source: [3] – “Git hasn’t automatically created a new merge commit. It has paused the process while you resolve the conflict… you can run `git status` … Unmerged paths …”*

2. **Open each conflicted file and edit the conflict markers** – the file will contain the conflict markers `<<<<<<<`, `=======`, and `>>>>>>>`.  
   *Source: [2] – “In order to resolve the conflict, you have to either choose one side or the other or merge the contents yourself… After you’ve resolved each of these sections in each conflicted file, run `git add` on each file to mark …”*

3. **Remove the conflict markers and keep the desired combined content** – replace the marker block with the version you want (it can contain parts from both sides).  
   *Source: [2] – “…replace the entire block with this: `<div id="footer">…</div>` … The `<<<<<<<`, `=======`, and `>>>>>>>` lines have been completely removed.”*

4. **Mark the file as resolved** – stage the edited file with `git add`.  
   *Source: [3] – “…run `git add` on each file to mark resolution.”*  
   *Source: [4] – “Staging the file marks it as resolved in Git.”*

5. **Complete the merge** – once all conflicted files are staged, finish the merge commit.  
   *Source: [1] – “If you’re happy with that, and you verify that everything that had conflicts has been staged, you can type `git commit` to finalize the merge commit.”*  
   *Source: [4] – “If you want to use a graphical tool to resolve these issues, you can run `git mergetool` …”*

**Summary of commands**

```bash
# after a merge conflict
git status                     # see unmerged paths
# edit each conflicted file, remove <<<<<<<, =======, >>>>>>> markers
git add <file>                 # mark the file as resolved
git commit                     # finish the merge (or use a message with -m)
# optional graphical aid
git mergetool                  # launch a merge‑tool to help resolve conflicts
```

These steps—detecting conflicts, editing the conflict markers, staging the resolved files, and committing—are the standard way to resolve merge conflicts in Git.

**Джерело:** data/raw/03_branching_basic_branching_merging.md

**Коментар:** Grounded — answer based on relevant chunk


## Запит 4: What is the difference between git add and git commit?

**Отримані чанки:** github_about_git_chunk_009 (score: 0.63), gitlab_getting_started_chunk_002 (score: 0.62), github_about_git_chunk_008 (score: 0.61), git_basics_recording_changes_chunk_007 (score: 0.57), github_about_git_chunk_007 (score: 0.56)

**Відповідь**: `git add` stages the changes you have made, moving them from the working directory into the staging area so they are included in the next snapshot.  
`git commit` then takes that staged snapshot and records it permanently in the repository’s history.  

**Sources:** [3] and [4]

**Джерело:** data/raw/08_github_about_git.md

**Коментар:** Grounded — answer based on relevant chunk


## Запит 5: How do I stash my changes temporarily?

**Отримані чанки:** git_tools_stashing_cleaning_chunk_002 (score: 0.63), git_tools_stashing_cleaning_chunk_001 (score: 0.62), git_tools_stashing_cleaning_chunk_004 (score: 0.55), git_tools_stashing_cleaning_chunk_013 (score: 0.55), git_tools_stashing_cleaning_chunk_005 (score: 0.53)

**Відповідь**: You can temporarily store (stash) your changes with the **`git stash`** command – the newer **`git stash push`** form is recommended because it also lets you stash selected paths, but the classic `git stash` (or `git stash save`) still works. After stashing, the changes are kept on a stack and can be re‑applied later using **`git stash apply`** (or `git stash apply stash@{n}` to target a specific stash).  

*See the discussion of stashing in chunk [2] and the example of applying a stash in chunk [5].*

**Джерело:** data/raw/07_git_tools_stashing_cleaning.md

**Коментар:** Grounded — answer based on relevant chunk


## Запит 6: How do I merge a branch in GitLab?

**Отримані чанки:** gitlab_getting_started_chunk_005 (score: 0.69), gitlab_getting_started_chunk_004 (score: 0.69), gitlab_getting_started_chunk_009 (score: 0.58), branching_branch_management_chunk_002 (score: 0.58), git_tools_rebasing_chunk_001 (score: 0.57)

**Відповідь**: To merge a branch in GitLab you create a **merge request** that targets the repository’s default branch (typically `main`). After opening the request, GitLab will try to merge the changes; if there are conflicts you must resolve them manually, then click **Merge** to integrate the branch. This process safely brings the changes into the default branch while preserving the commit history.  

[2] Chunk: gitlab_getting_started_chunk_004 – describes merging a branch via a merge request and handling conflicts.

**Джерело:** data/raw/09_gitlab_getting_started.md

**Коментар:** Grounded — answer based on relevant chunk


## Запит 7: How do I view the commit history?

**Отримані чанки:** github_about_git_chunk_001 (score: 0.58), git_basics_recording_changes_chunk_027 (score: 0.55), git_basics_recording_changes_chunk_028 (score: 0.54), gitlab_getting_started_chunk_002 (score: 0.52), git_basics_recording_changes_chunk_029 (score: 0.50)

**Відповідь**: I do not have enough information in the available documents to answer this question.

**Джерело:** data/raw/08_github_about_git.md

**Коментар:** Fallback — insufficient relevant context


## Запит 8: How to set up SSH keys for GitLab?

**Отримані чанки:** gitlab_getting_started_chunk_010 (score: 0.74), gitlab_getting_started_chunk_009 (score: 0.61), gitlab_getting_started_chunk_001 (score: 0.52), gitlab_getting_started_chunk_003 (score: 0.46), git_basics_getting_repository_chunk_007 (score: 0.45)

**Відповідь**: To set up SSH keys for GitLab you need to:

1. **Generate an SSH key pair on your local system** – this creates the public‑private key pair that will be used for authentication.  
2. **Add your SSH key to your GitLab account** – upload the public key so GitLab can recognize your machine.  
3. **Verify your SSH connection to GitLab** – test that the key works by attempting an SSH connection (e.g., `ssh -T git@gitlab.com`).

These steps are outlined in **Chunk [1]** of the provided documentation.

**Джерело:** data/raw/09_gitlab_getting_started.md

**Коментар:** Grounded — answer based on relevant chunk


## Запит 9: What is rebasing and when should I use it?

**Отримані чанки:** git_tools_rebasing_chunk_001 (score: 0.54), git_tools_rebasing_chunk_018 (score: 0.54), git_tools_rebasing_chunk_009 (score: 0.54), git_tools_rebasing_chunk_004 (score: 0.52), git_tools_rebasing_chunk_005 (score: 0.47)

**Відповідь**: **What is rebasing?**  
Rebasing is a way of integrating changes by *re‑playing a series of commits onto a new base commit*, which rewrites the branch’s history so that the commits appear as if they were introduced sequentially on top of the new base. [1]  

**When should you use it?**  
- **Clean up local work before you share it.** You can rebase your local commits to tidy the history, then push the cleaned‑up branch. [2]  
- **Make sure your changes apply cleanly onto another branch** (for example, onto `origin/master` when contributing to a project you don’t maintain). This gives the maintainer a linear, easy‑to‑apply series of patches. [4]  
- **Keep a linear project history** when you want the log to show a straight line of commits rather than a merge‑generated fork. [5]  

**When should you avoid it?**  
- **Never rebase commits that have already been pushed and shared** with others, because rewriting those commits forces everyone else to re‑merge and can cause confusion. [3]  

In short, use rebasing to maintain a clean, linear history for private or freshly‑pushed work, but refrain from rebasing any history that has already been published.

**Джерело:** data/raw/06_git_tools_rebasing.md

**Коментар:** Grounded — answer based on relevant chunk


## Запит 10: How do I push changes to a remote repository?

**Отримані чанки:** github_about_git_chunk_010 (score: 0.71), git_basics_getting_repository_chunk_002 (score: 0.70), github_about_git_chunk_012 (score: 0.66), distributed_workflows_chunk_006 (score: 0.61), gitlab_getting_started_chunk_007 (score: 0.59)

**Відповідь**: To push your local commits to a remote repository you first commit the changes and then run the **`git push`** command.  
For the first push of a new branch you can also set the upstream in one step with:

```bash
git push --set-upstream origin <branch-name>
```

These steps are shown in the examples that explain pushing to GitHub [1] and illustrate the basic workflow of pushing after a commit [3].  

**Source:** [1] and [3] (chunks github_about_git_chunk_010 and git_basics_getting_repository_chunk_002).

**Джерело:** data/raw/08_github_about_git.md

**Коментар:** Grounded — answer based on relevant chunk

