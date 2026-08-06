# HW2: Semantic Retrieval — Test Results

**Model**: sentence-transformers/all-MiniLM-L6-v2

**Chunks**: 145

**Index**: FAISS (IndexFlatIP, dim=384)

**Top-k**: 5

## Summary

| Metric | Value |
|--------|-------|
| Total chunks indexed | 145 |
| Embedding model | sentence-transformers/all-MiniLM-L6-v2 |
| Embedding dimension | 384 |
| Vector storage | FAISS IndexFlatIP |
| Test queries | 10 |
| Top-k | 5 |

## Query 1: How do I clone a Git repository?

Top-1: git_basics_getting_repository_chunk_002 | score: 0.7085
  Text: 'Git Repository\nYou typically obtain a Git repository in one of two ways:\n1. You can take a local directory that is currently not under version control, and turn it into a Git repository, or\n2. You can'
  Source: data/raw/01_git_basics_getting_repository.md
  Domain: git


Top-2: git_basics_getting_repository_chunk_006 | score: 0.7084
  Text: 'creates a directory named `libgit2`, initializes a `.git` directory inside it, pulls down all the data for that repository, and checks out a working copy of the latest version. If you go into the new '
  Source: data/raw/01_git_basics_getting_repository.md
  Domain: git


Top-3: git_basics_getting_repository_chunk_005 | score: 0.6878
  Text: 'working copy, Git receives a full copy of nearly all data that the server has. Every version of every file for the history of the project is pulled down by default when you run `git clone`. In fact, i'
  Source: data/raw/01_git_basics_getting_repository.md
  Domain: git


Top-4: gitlab_getting_started_chunk_006 | score: 0.6345
  Text: 'repository: Create a local copy of the repository by cloning it to your machine.\nYou can work on the project without affecting the original repository.\n1. Create a new branch: Before you make any chan'
  Source: data/raw/09_gitlab_getting_started.md
  Domain: gitlab


Top-5: github_about_git_chunk_007 | score: 0.6219
  Text: 'commands\nTo use Git, developers use specific commands to copy, create, change, and combine code. These commands can be executed directly from the command line or by using an application like GitHub De'
  Source: data/raw/08_github_about_git.md
  Domain: github



## Query 2: What is a Git branch and how do I create one?

Top-1: gitlab_getting_started_chunk_001 | score: 0.6338
  Text: '# Get started with Git\nGit is a version control system you use to track changes to your code and collaborate with others.\nGitLab is a web-based Git repository manager that provides CI/CD and other fea'
  Source: data/raw/09_gitlab_getting_started.md
  Domain: gitlab


Top-2: github_about_git_chunk_004 | score: 0.6076
  Text: "the entire collection of files and folders associated with a project, along with each file's revision history. The file history appears as snapshots in time called commits. The commits can be organize"
  Source: data/raw/08_github_about_git.md
  Domain: github


Top-3: github_about_git_chunk_007 | score: 0.6008
  Text: 'commands\nTo use Git, developers use specific commands to copy, create, change, and combine code. These commands can be executed directly from the command line or by using an application like GitHub De'
  Source: data/raw/08_github_about_git.md
  Domain: github


Top-4: branching_branch_management_chunk_001 | score: 0.5925
  Text: '# 3.3 Git Branching - Branch Management\nNow that you’ve created, merged, and deleted some branches, let’s look at some branch-management tools that will come in handy when you begin using branches all'
  Source: data/raw/04_branching_branch_management.md
  Domain: git


Top-5: github_about_git_chunk_009 | score: 0.583
  Text: 'become a part of the snapshot with `git commit`.\n* `git status` shows the status of changes as untracked, modified, or staged.\n* `git branch` shows the branches being worked on locally.\n* `git merge` '
  Source: data/raw/08_github_about_git.md
  Domain: github



## Query 3: How to resolve merge conflicts in Git?

Top-1: gitlab_getting_started_chunk_005 | score: 0.7214
  Text: 'these as merge conflicts.\nThese must be resolved manually by reviewing and editing the code.\n### Delete a branch\nAfter a successful merge, you can delete the branch if it is no longer needed.\nDeleting'
  Source: data/raw/09_gitlab_getting_started.md
  Domain: gitlab


Top-2: branching_basic_branching_merging_chunk_016 | score: 0.7208
  Text: 'again to verify that all conflicts have been resolved:\n$ git status\nOn branch master\nAll conflicts fixed but you are still merging.\n(use "git commit" to conclude merge)\nChanges to be committed:\nmodifi'
  Source: data/raw/03_branching_basic_branching_merging.md
  Domain: git


Top-3: branching_basic_branching_merging_chunk_010 | score: 0.6859
  Text: 'pointer forward, Git creates a new snapshot that results from this three-way merge and automatically creates a new commit that points to it. This is referred to as a merge commit, and is special in th'
  Source: data/raw/03_branching_basic_branching_merging.md
  Domain: git


Top-4: branching_basic_branching_merging_chunk_011 | score: 0.6841
  Text: 'the same part of a file as the `hotfix` branch, you’ll get a merge conflict that looks something like this:\n$ git merge iss53\nAuto-merging index.html\nCONFLICT (content): Merge conflict in index.html\nA'
  Source: data/raw/03_branching_basic_branching_merging.md
  Domain: git


Top-5: branching_basic_branching_merging_chunk_015 | score: 0.6728
  Text: 'modified file\n{remote}: modified file\nHit return to start merge resolution tool (opendiff):\nIf you want to use a merge tool other than the default (Git chose `opendiff` in this case because the comman'
  Source: data/raw/03_branching_basic_branching_merging.md
  Domain: git



## Query 4: What is the difference between git add and git commit?

Top-1: github_about_git_chunk_008 | score: 0.6602
  Text: "changes to a developer's codebase, but it's necessary to stage and take a snapshot of the changes to include them in the project's history. This command performs staging, the first part of that two-st"
  Source: data/raw/08_github_about_git.md
  Domain: github


Top-2: git_basics_recording_changes_chunk_007 | score: 0.6152
  Text: 'the “Changes to be committed” heading. If you commit at this point, the version of the file at the time you ran `git add` is what will be in the subsequent historical snapshot. You may recall that whe'
  Source: data/raw/02_git_basics_recording_changes.md
  Domain: git


Top-3: github_about_git_chunk_007 | score: 0.562
  Text: 'commands\nTo use Git, developers use specific commands to copy, create, change, and combine code. These commands can be executed directly from the command line or by using an application like GitHub De'
  Source: data/raw/08_github_about_git.md
  Domain: github


Top-4: github_about_git_chunk_004 | score: 0.5474
  Text: "the entire collection of files and folders associated with a project, along with each file's revision history. The file history appears as snapshots in time called commits. The commits can be organize"
  Source: data/raw/08_github_about_git.md
  Domain: github


Top-5: git_basics_recording_changes_chunk_030 | score: 0.5427
  Text: 'a simple shortcut. Adding the `-a` option to the `git commit` command makes Git automatically stage every file that is already tracked before doing the commit, letting you skip the `git add` part:\n$ g'
  Source: data/raw/02_git_basics_recording_changes.md
  Domain: git



## Query 5: How do I stash my changes temporarily?

Top-1: git_tools_stashing_cleaning_chunk_001 | score: 0.6201
  Text: '# 7.3 Git Tools - Stashing and Cleaning\nOften, when you’ve been working on part of your project, things are in a messy state and you want to switch branches for a bit to work on something else. The pr'
  Source: data/raw/07_git_tools_stashing_cleaning.md
  Domain: git


Top-2: git_tools_stashing_cleaning_chunk_005 | score: 0.5668
  Text: 'the one you just stashed by using the command shown in the help output of the original stash command: `git stash apply`. If you want to apply one of the older stashes, you can specify it by naming it,'
  Source: data/raw/07_git_tools_stashing_cleaning.md
  Domain: git


Top-3: git_tools_stashing_cleaning_chunk_002 | score: 0.547
  Text: 'extensive discussion on the Git mailing list, wherein the command `git stash save` is being deprecated in favour of the existing alternative `git stash push`. The main reason for this is that `git sta'
  Source: data/raw/07_git_tools_stashing_cleaning.md
  Domain: git


Top-4: git_tools_stashing_cleaning_chunk_004 | score: 0.5308
  Text: '049d078 Create index file\n(To restore them type "git stash apply")\nYou can now see that your working directory is clean:\n$ git status\n# On branch master\nnothing to commit, working directory clean\nAt t'
  Source: data/raw/07_git_tools_stashing_cleaning.md
  Domain: git


Top-5: git_tools_stashing_cleaning_chunk_012 | score: 0.5158
  Text: 'have to try to resolve it. If you want an easier way to test the stashed changes again, you can run `git stash branch <new branchname>`, which creates a new branch for you with your selected branch na'
  Source: data/raw/07_git_tools_stashing_cleaning.md
  Domain: git



## Query 6: How do I merge a branch in GitLab?

Top-1: gitlab_getting_started_chunk_004 | score: 0.7146
  Text: "fixes, or experiments\nsimultaneously without interfering with each other's work.\nBranching enables you to create an isolated environment where you can make and test\nchanges without affecting the defau"
  Source: data/raw/09_gitlab_getting_started.md
  Domain: gitlab


Top-2: github_about_git_chunk_009 | score: 0.5995
  Text: 'become a part of the snapshot with `git commit`.\n* `git status` shows the status of changes as untracked, modified, or staged.\n* `git branch` shows the branches being worked on locally.\n* `git merge` '
  Source: data/raw/08_github_about_git.md
  Domain: github


Top-3: gitlab_getting_started_chunk_009 | score: 0.5947
  Text: 'repository.\n- `git checkout`: Switch between different branches in your local repository.\n- `git add`: Stage changes for commit.\n- `git commit`: Commit staged changes to your local repository.\n- `git '
  Source: data/raw/09_gitlab_getting_started.md
  Domain: gitlab


Top-4: git_tools_rebasing_chunk_001 | score: 0.5734
  Text: '# 3.6 Git Branching - Rebasing\nIn Git, there are two main ways to integrate changes from one branch into another: the `merge` and the `rebase`. In this section you’ll learn what rebasing is, how to do'
  Source: data/raw/06_git_tools_rebasing.md
  Domain: git


Top-5: branching_branch_management_chunk_002 | score: 0.5659
  Text: "your new work. To see the last commit on each branch, you can run `git branch -v`:\n$ git branch -v\niss53   93b412c Fix javascript issue\n* master  7a98805 Merge branch 'iss53'\ntesting 782fd34 Add scott"
  Source: data/raw/04_branching_branch_management.md
  Domain: git



## Query 7: How do I view the commit history?

Top-1: github_about_git_chunk_004 | score: 0.5934
  Text: "the entire collection of files and folders associated with a project, along with each file's revision history. The file history appears as snapshots in time called commits. The commits can be organize"
  Source: data/raw/08_github_about_git.md
  Domain: github


Top-2: git_basics_recording_changes_chunk_028 | score: 0.5861
  Text: 'editor so you can see exactly what changes you’re committing.\nWhen you exit the editor, Git creates your commit with that commit message (with the comments and diff stripped out).\nAlternatively, you c'
  Source: data/raw/02_git_basics_recording_changes.md
  Domain: git


Top-3: github_about_git_chunk_001 | score: 0.5813
  Text: '# About Git\nLearn about the version control system, Git, and how it works with GitHub.\n## About version control and Git\nA version control system, or VCS, tracks the history of changes as people and te'
  Source: data/raw/08_github_about_git.md
  Domain: github


Top-4: git_basics_recording_changes_chunk_022 | score: 0.5479
  Text: 'made since your last commit — only changes that are still unstaged. If you’ve staged all of your changes, `git diff` will give you no output.\nFor another example, if you stage the `CONTRIBUTING.md` fi'
  Source: data/raw/02_git_basics_recording_changes.md
  Domain: git


Top-5: git_tools_rebasing_chunk_011 | score: 0.5355
  Text: 'commit which includes both lines of history, and your repository will look like this:\nIf you run a `git log` when your history looks like this, you’ll see two commits that have the same author, date, '
  Source: data/raw/06_git_tools_rebasing.md
  Domain: git



## Query 8: How to set up SSH keys for GitLab?

Top-1: gitlab_getting_started_chunk_010 | score: 0.7434
  Text: "GitLab remote server,\nyou don't need to supply your username and password each time.\nTo use SSH with GitLab, you must:\n1. Generate an SSH key pair on your local system.\n1. Add your SSH key to your Git"
  Source: data/raw/09_gitlab_getting_started.md
  Domain: gitlab


Top-2: gitlab_getting_started_chunk_009 | score: 0.6751
  Text: 'repository.\n- `git checkout`: Switch between different branches in your local repository.\n- `git add`: Stage changes for commit.\n- `git commit`: Commit staged changes to your local repository.\n- `git '
  Source: data/raw/09_gitlab_getting_started.md
  Domain: gitlab


Top-3: gitlab_getting_started_chunk_008 | score: 0.524
  Text: 'repository that exists in your own namespace.\nUse this workflow when contributing to open-source projects or when your team uses a\ncentralized repository.\n## Install Git\nTo use Git commands and contri'
  Source: data/raw/09_gitlab_getting_started.md
  Domain: gitlab


Top-4: gitlab_getting_started_chunk_001 | score: 0.5177
  Text: '# Get started with Git\nGit is a version control system you use to track changes to your code and collaborate with others.\nGitLab is a web-based Git repository manager that provides CI/CD and other fea'
  Source: data/raw/09_gitlab_getting_started.md
  Domain: gitlab


Top-5: gitlab_getting_started_chunk_003 | score: 0.4583
  Text: 'repository, you create a local copy of the repository in your working directory.\nYou can edit files, add new ones, and test your code.\nTo collaborate, you can:\n- Commit: After you make changes in your'
  Source: data/raw/09_gitlab_getting_started.md
  Domain: gitlab



## Query 9: What is rebasing and when should I use it?

Top-1: git_tools_rebasing_chunk_001 | score: 0.5448
  Text: '# 3.6 Git Branching - Rebasing\nIn Git, there are two main ways to integrate changes from one branch into another: the `merge` and the `rebase`. In this section you’ll learn what rebasing is, how to do'
  Source: data/raw/06_git_tools_rebasing.md
  Domain: git


Top-2: git_tools_rebasing_chunk_005 | score: 0.5123
  Text: 'with, whether it’s the last of the rebased commits for a rebase or the final merge commit after a merge, is the same snapshot — it’s only the history that is different. Rebasing replays changes from o'
  Source: data/raw/06_git_tools_rebasing.md
  Domain: git


Top-3: git_tools_rebasing_chunk_017 | score: 0.5048
  Text: 'why show your messy work? When you’re working on a project, you may need a record of all your missteps and dead-end paths, but when it’s time to show your work to the world, you may want to tell a mor'
  Source: data/raw/06_git_tools_rebasing.md
  Domain: git


Top-4: git_tools_rebasing_chunk_008 | score: 0.4864
  Text: '(`master`):\n$ git rebase master server\nThis replays your `server` work on top of your `master` work, as shown in Rebasing your `server` branch on top of your `master` branch.\nThen, you can fast-forwar'
  Source: data/raw/06_git_tools_rebasing.md
  Domain: git


Top-5: git_tools_rebasing_chunk_015 | score: 0.4819
  Text: 'never left your own computer, you’ll be just fine. If you rebase commits that have been pushed, but that no one else has based commits from, you’ll also be fine. If you rebase commits that have alread'
  Source: data/raw/06_git_tools_rebasing.md
  Domain: git



## Query 10: How do I push changes to a remote repository?

Top-1: github_about_git_chunk_010 | score: 0.7015
  Text: 'those changes in their local environment.\n* `git push` updates the remote repository with any commits made locally to a branch.\nFor more information, see the full reference guide to Git commands.\n### '
  Source: data/raw/08_github_about_git.md
  Domain: github


Top-2: github_about_git_chunk_012 | score: 0.6622
  Text: '### Example: contribute to an existing branch on GitHub\nThis example assumes that you already have a project called `repo` on the machine and that a new branch has been pushed to GitHub since the last'
  Source: data/raw/08_github_about_git.md
  Domain: github


Top-3: distributed_workflows_chunk_006 | score: 0.657
  Text: 'to their own public repository and read access to everyone else’s. This scenario often includes a canonical repository that represents the “official” project. To contribute to that project, you create'
  Source: data/raw/05_distributed_workflows.md
  Domain: git


Top-4: gitlab_getting_started_chunk_006 | score: 0.6518
  Text: 'repository: Create a local copy of the repository by cloning it to your machine.\nYou can work on the project without affecting the original repository.\n1. Create a new branch: Before you make any chan'
  Source: data/raw/09_gitlab_getting_started.md
  Domain: gitlab


Top-5: distributed_workflows_chunk_007 | score: 0.6182
  Text: 'that repository and makes changes.\n3. The contributor pushes to their own public copy.\n4. The contributor sends the maintainer an email asking them to pull changes.\n5. The maintainer adds the contribu'
  Source: data/raw/05_distributed_workflows.md
  Domain: git

