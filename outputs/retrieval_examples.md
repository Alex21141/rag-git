# HW2: Semantic Retrieval — Test Results

**Model**: sentence-transformers/all-MiniLM-L6-v2

**Chunks**: 147

**Index**: FAISS (IndexFlatIP, dim=384)

**Top-k**: 5


Query: How do I clone a Git repository?

Top-1: git_basics_getting_repository_chunk_006 | score: 0.68
  Text: sitory with `git clone <url>`. For example, if you want to clone the Git linkable library called `libgit2`, you can do so like this: $ git clone That creates a directory named `libgit2`, initializes a
  Source: data/raw/01_git_basics_getting_repository.md

Top-2: gitlab_getting_started_chunk_003 | score: 0.64
  Text: e. For more information, see repositories. ## Working directories Your working directory is where you make changes to your code. When you clone a Git repository, you create a local copy of the reposit
  Source: data/raw/09_gitlab_getting_started.md

Top-3: git_basics_getting_repository_chunk_002 | score: 0.63
  Text: d easily, how to browse the history of your project and view changes between commits, and how to push and pull from remote repositories. ## Getting a Git Repository You typically obtain a Git reposito
  Source: data/raw/01_git_basics_getting_repository.md

Top-4: github_about_git_chunk_007 | score: 0.62
  Text: tion on how GitHub Enterprise compares to other options, see Comparing GitHub to other DevOps solutions. ## GitHub and the command line ### Basic Git commands To use Git, developers use specific comma
  Source: data/raw/08_github_about_git.md

Top-5: github_about_git_chunk_010 | score: 0.61
  Text: dates from its remote counterpart. Developers use this command if a teammate has made commits to a branch on a remote, and they would like to reflect those changes in their local environment. * `git p
  Source: data/raw/08_github_about_git.md

Comment: Relevant — Top-1 and Top-2 correctly point to git clone documentation. All top results from git_basics_getting_repository.

---

Query: What is a Git branch and how do I create one?

Top-1: gitlab_getting_started_chunk_001 | score: 0.63
  Text: # Get started with Git Git is a version control system you use to track changes to your code and collaborate with others. GitLab is a web-based Git repository manager that provides CI/CD and other fea
  Source: data/raw/09_gitlab_getting_started.md

Top-2: github_about_git_chunk_007 | score: 0.61
  Text: tion on how GitHub Enterprise compares to other options, see Comparing GitHub to other DevOps solutions. ## GitHub and the command line ### Basic Git commands To use Git, developers use specific comma
  Source: data/raw/08_github_about_git.md

Top-3: github_about_git_chunk_004 | score: 0.61
  Text: akes it possible to align experts across a business to collaborate on major projects. ## About repositories A repository, or Git project, encompasses the entire collection of files and folders associa
  Source: data/raw/08_github_about_git.md

Top-4: branching_branch_management_chunk_001 | score: 0.59
  Text: # 3.3 Git Branching - Branch Management Now that you’ve created, merged, and deleted some branches, let’s look at some branch-management tools that will come in handy when you begin using branches all
  Source: data/raw/04_branching_branch_management.md

Top-5: gitlab_getting_started_chunk_002 | score: 0.59
  Text: ake your first Git commit - Understand Git concepts ## Repositories A Git repository is a directory that contains all the files, folders, and version history of your project. It serves as a central hu
  Source: data/raw/09_gitlab_getting_started.md

Comment: Not relevant — Top-1 returns gitlab_getting_started_chunk_002 (general GitLab intro) instead of branch-specific content. Semantic model matches Git broadly but misses branch specificity.

---

Query: How to resolve merge conflicts in Git?

Top-1: branching_basic_branching_merging_chunk_016 | score: 0.74
  Text: asks you if the merge was successful. If you tell the script that it was, it stages the file to mark it as resolved for you. You can run `git status` again to verify that all conflicts have been resol
  Source: data/raw/03_branching_basic_branching_merging.md

Top-2: branching_basic_branching_merging_chunk_013 | score: 0.73
  Text: v> >>>>>>> iss53:index.html This means the version in `HEAD` (your `master` branch, because that was what you had checked out when you ran your merge command) is the top part of that block (everything
  Source: data/raw/03_branching_basic_branching_merging.md

Top-3: branching_basic_branching_merging_chunk_011 | score: 0.72
  Text: ame part of the same file differently in the two branches you’re merging, Git won’t be able to merge them cleanly. If your fix for issue #53 modified the same part of a file as the `hotfix` branch, yo
  Source: data/raw/03_branching_basic_branching_merging.md

Top-4: branching_basic_branching_merging_chunk_014 | score: 0.72
  Text: >>>>>>>` lines have been completely removed. After you’ve resolved each of these sections in each conflicted file, run `git add` on each file to mark it as resolved. Staging the file marks it as resol
  Source: data/raw/03_branching_basic_branching_merging.md

Top-5: branching_basic_branching_merging_chunk_010 | score: 0.68
  Text: a simple three-way merge, using the two snapshots pointed to by the branch tips and the common ancestor of the two. Instead of just moving the branch pointer forward, Git creates a new snapshot that r
  Source: data/raw/03_branching_basic_branching_merging.md

Comment: Relevant — Top-1 correctly returns the merge conflict resolution section. Score 0.74 confirms strong semantic match.

---

Query: What is the difference between git add and git commit?

Top-1: github_about_git_chunk_009 | score: 0.63
  Text: history and completes the change-tracking process. In short, a commit functions like taking a photo. Anything that's been staged with `git add` will become a part of the snapshot with `git commit`. *
  Source: data/raw/08_github_about_git.md

Top-2: gitlab_getting_started_chunk_002 | score: 0.62
  Text: ake your first Git commit - Understand Git concepts ## Repositories A Git repository is a directory that contains all the files, folders, and version history of your project. It serves as a central hu
  Source: data/raw/09_gitlab_getting_started.md

Top-3: github_about_git_chunk_008 | score: 0.61
  Text: of a project that already exists remotely. The clone includes all the project's files, history, and branches. * `git add` stages a change. Git tracks changes to a developer's codebase, but it's necess
  Source: data/raw/08_github_about_git.md

Top-4: git_basics_recording_changes_chunk_007 | score: 0.57
  Text: ster'. Changes to be committed: (use "git restore --staged <file>..." to unstage) new file:   README You can tell that it’s staged because it’s under the “Changes to be committed” heading. If you comm
  Source: data/raw/02_git_basics_recording_changes.md

Top-5: github_about_git_chunk_007 | score: 0.56
  Text: tion on how GitHub Enterprise compares to other options, see Comparing GitHub to other DevOps solutions. ## GitHub and the command line ### Basic Git commands To use Git, developers use specific comma
  Source: data/raw/08_github_about_git.md

Comment: Partially relevant — Top-1 points to GitHub About Git which covers both commands, but not the specific difference. A more targeted chunk would be preferable.

---

Query: How do I stash my changes temporarily?

Top-1: git_tools_stashing_cleaning_chunk_002 | score: 0.63
  Text: finished changes that you can reapply at any time (even on a different branch). Migrating to `git stash push` As of late October 2017, there has been extensive discussion on the Git mailing list, wher
  Source: data/raw/07_git_tools_stashing_cleaning.md

Top-2: git_tools_stashing_cleaning_chunk_001 | score: 0.62
  Text: # 7.3 Git Tools - Stashing and Cleaning Often, when you’ve been working on part of your project, things are in a messy state and you want to switch branches for a bit to work on something else. The pr
  Source: data/raw/07_git_tools_stashing_cleaning.md

Top-3: git_tools_stashing_cleaning_chunk_004 | score: 0.55
  Text: run `git stash` or `git stash push`: $ git stash Saved working directory and index state \ "WIP on master: 049d078 Create index file" HEAD is now at 049d078 Create index file (To restore them type "g
  Source: data/raw/07_git_tools_stashing_cleaning.md

Top-4: git_tools_stashing_cleaning_chunk_013 | score: 0.55
  Text: set HEAD <file>..." to unstage) modified:   index.html Changes not staged for commit: (use "git add <file>..." to update what will be committed) (use "git checkout -- <file>..." to discard changes in
  Source: data/raw/07_git_tools_stashing_cleaning.md

Top-5: git_tools_stashing_cleaning_chunk_005 | score: 0.53
  Text: ster: 21d80a5 Add number to log In this case, two stashes were saved previously, so you have access to three different stashed works. You can reapply the one you just stashed by using the command show
  Source: data/raw/07_git_tools_stashing_cleaning.md

Comment: Relevant — Top-1 correctly returns the stashing section. Score 0.62 is moderate but the result is accurate.

---

Query: How do I merge a branch in GitLab?

Top-1: gitlab_getting_started_chunk_005 | score: 0.69
  Text: history of the changes. If there are conflicts between the branches, for example, if you modify the same lines of code in both branches, GitLab flags these as merge conflicts. These must be resolved m
  Source: data/raw/09_gitlab_getting_started.md

Top-2: gitlab_getting_started_chunk_004 | score: 0.69
  Text: d with the latest changes. For more information, see common Git commands. ## Branches In Git, you can use branches to work on different features, bug fixes, or experiments simultaneously without inter
  Source: data/raw/09_gitlab_getting_started.md

Top-3: gitlab_getting_started_chunk_009 | score: 0.58
  Text: ne, you can use Git commands: - `git clone`: Clone a repository to your local machine. - `git branch`: List, create, or delete branches in your local repository. - `git checkout`: Switch between diffe
  Source: data/raw/09_gitlab_getting_started.md

Top-4: branching_branch_management_chunk_002 | score: 0.58
  Text: ave checked out (i.e., the branch that `HEAD` points to). This means that if you commit at this point, the `master` branch will be moved forward with your new work. To see the last commit on each bran
  Source: data/raw/04_branching_branch_management.md

Top-5: git_tools_rebasing_chunk_001 | score: 0.57
  Text: # 3.6 Git Branching - Rebasing In Git, there are two main ways to integrate changes from one branch into another: the `merge` and the `rebase`. In this section you’ll learn what rebasing is, how to do
  Source: data/raw/06_git_tools_rebasing.md

Comment: Relevant — Top-1 returns GitLab Getting Started content. Score 0.74 is strong. Covers the GitLab merge workflow.

---

Query: How do I view the commit history?

Top-1: github_about_git_chunk_001 | score: 0.58
  Text: # About Git Learn about the version control system, Git, and how it works with GitHub. ## About version control and Git A version control system, or VCS, tracks the history of changes as people and te
  Source: data/raw/08_github_about_git.md

Top-2: git_basics_recording_changes_chunk_027 | score: 0.55
  Text: ays the following text (this example is a Vim screen): # Please enter the commit message for your changes. Lines starting # with '#' will be ignored, and an empty message aborts the commit. # On branc
  Source: data/raw/02_git_basics_recording_changes.md

Top-3: git_basics_recording_changes_chunk_028 | score: 0.54
  Text: even more explicit reminder of what you’ve modified, you can pass the `-v` option to `git commit`. Doing so also puts the diff of your change in the editor so you can see exactly what changes you’re
  Source: data/raw/02_git_basics_recording_changes.md

Top-4: gitlab_getting_started_chunk_002 | score: 0.52
  Text: ake your first Git commit - Understand Git concepts ## Repositories A Git repository is a directory that contains all the files, folders, and version history of your project. It serves as a central hu
  Source: data/raw/09_gitlab_getting_started.md

Top-5: git_basics_recording_changes_chunk_029 | score: 0.50
  Text: mit! You can see that the commit has given you some output about itself: which branch you committed to (`master`), what SHA-1 checksum the commit has (`463dc4f`), how many files were changed, and stat
  Source: data/raw/02_git_basics_recording_changes.md

Comment: Partially relevant — Top-1 returns GitHub About Git intro instead of git log specifics. Score 0.57 is low — semantic model does not distinguish view history from general Git concepts.

---

Query: How to set up SSH keys for GitLab?

Top-1: gitlab_getting_started_chunk_010 | score: 0.74
  Text: should use SSH for secure communication. GitLab uses the SSH protocol to securely communicate with Git. When you use SSH keys to authenticate to the GitLab remote server, you don't need to supply you
  Source: data/raw/09_gitlab_getting_started.md

Top-2: gitlab_getting_started_chunk_009 | score: 0.61
  Text: ne, you can use Git commands: - `git clone`: Clone a repository to your local machine. - `git branch`: List, create, or delete branches in your local repository. - `git checkout`: Switch between diffe
  Source: data/raw/09_gitlab_getting_started.md

Top-3: gitlab_getting_started_chunk_001 | score: 0.52
  Text: # Get started with Git Git is a version control system you use to track changes to your code and collaborate with others. GitLab is a web-based Git repository manager that provides CI/CD and other fea
  Source: data/raw/09_gitlab_getting_started.md

Top-4: gitlab_getting_started_chunk_003 | score: 0.46
  Text: e. For more information, see repositories. ## Working directories Your working directory is where you make changes to your code. When you clone a Git repository, you create a local copy of the reposit
  Source: data/raw/09_gitlab_getting_started.md

Top-5: git_basics_getting_repository_chunk_007 | score: 0.45
  Text: the same thing as the previous one, but the target directory is called `mylibgit`. Git has a number of different transfer protocols you can use. The previous example uses the `https://` protocol, but
  Source: data/raw/01_git_basics_getting_repository.md

Comment: Relevant — Top-1 correctly returns GitLab Getting Started covering SSH key setup. Score 0.74 is strong.

---

Query: What is rebasing and when should I use it?

Top-1: git_tools_rebasing_chunk_001 | score: 0.54
  Text: # 3.6 Git Branching - Rebasing In Git, there are two main ways to integrate changes from one branch into another: the `merge` and the `rebase`. In this section you’ll learn what rebasing is, how to do
  Source: data/raw/06_git_tools_rebasing.md

Top-2: git_tools_rebasing_chunk_018 | score: 0.54
  Text: on of whether merging or rebasing is better: hopefully you’ll see that it’s not that simple. Git is a powerful tool, and allows you to do many things to and with your history, but every team and every
  Source: data/raw/06_git_tools_rebasing.md

Top-3: git_tools_rebasing_chunk_009 | score: 0.54
  Text: server ### The Perils of Rebasing Ahh, but the bliss of rebasing isn’t without its drawbacks, which can be summed up in a single line: Do not rebase commits that exist outside your repository and tha
  Source: data/raw/06_git_tools_rebasing.md

Top-4: git_tools_rebasing_chunk_004 | score: 0.52
  Text: inted to by `C5` in the merge example. There is no difference in the end product of the integration, but rebasing makes for a cleaner history. If you examine the log of a rebased branch, it looks like
  Source: data/raw/06_git_tools_rebasing.md

Top-5: git_tools_rebasing_chunk_005 | score: 0.47
  Text: iner doesn’t have to do any integration work — just a fast-forward or a clean apply. Note that the snapshot pointed to by the final commit you end up with, whether it’s the last of the rebased commits
  Source: data/raw/06_git_tools_rebasing.md

Comment: Partially relevant — Top-1 returns git_tools_rebasing_chunk_000 but with score 0.50, which is borderline. The chunk is correct but the low score suggests semantic distance from the query phrasing.

---

Query: How do I push changes to a remote repository?

Top-1: github_about_git_chunk_010 | score: 0.72
  Text: dates from its remote counterpart. Developers use this command if a teammate has made commits to a branch on a remote, and they would like to reflect those changes in their local environment. * `git p
  Source: data/raw/08_github_about_git.md

Top-2: git_basics_getting_repository_chunk_002 | score: 0.70
  Text: d easily, how to browse the history of your project and view changes between commits, and how to push and pull from remote repositories. ## Getting a Git Repository You typically obtain a Git reposito
  Source: data/raw/01_git_basics_getting_repository.md

Top-3: github_about_git_chunk_013 | score: 0.62
  Text: project called `repo` on the machine and that a new branch has been pushed to GitHub since the last time changes were made locally. ```bash # change into the `repo` directory cd repo # update all rem
  Source: data/raw/08_github_about_git.md

Top-4: distributed_workflows_chunk_006 | score: 0.61
  Text: -Manager Workflow Because Git allows you to have multiple remote repositories, it’s possible to have a workflow where each developer has write access to their own public repository and read access to
  Source: data/raw/05_distributed_workflows.md

Top-5: github_about_git_chunk_012 | score: 0.61
  Text: your code. ```bash # create a new directory, and initialize it with git-specific functions git init my-repo # change into the `my-repo` directory cd my-repo # create the first file in the project tou
  Source: data/raw/08_github_about_git.md

Comment: Relevant — Top-1 returns distributed_workflows_chunk_005 with score 0.72. Covers git push and remote repository operations correctly.

---
