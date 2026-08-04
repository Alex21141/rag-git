# HW2: Semantic Retrieval — Test Results

**Model**: sentence-transformers/all-MiniLM-L6-v2

**Chunks**: 164

**Index**: FAISS (IndexFlatIP, dim=384)

**Top-k**: 5

## Summary

| Metric | Value |
|--------|-------|
| Total chunks indexed | 164 |
| Embedding model | sentence-transformers/all-MiniLM-L6-v2 |
| Embedding dimension | 384 |
| Vector storage | FAISS IndexFlatIP |
| Test queries | 10 |
| Top-k | 5 |

## Query 1: How do I clone a Git repository?

Top-1: git_basics_getting_repository_chunk_005 | score: 0.7031
  Text: '`libgit2`, initializes a `.git` directory inside it, pulls down all the data for that repository, and checks out a working copy of the latest version.If you go into the new `libgit2` directory that wa'
  Source: data/raw/01_git_basics_getting_repository.md
  Domain: git


Top-2: github_about_git_chunk_006 | score: 0.6456
  Text: 'copy, create, change, and combine code. These commands can be executed directly from the command line or by using an application like GitHub Desktop.Here are some common commands for using Git:\n\n  * `'
  Source: data/raw/08_github_about_git.md
  Domain: github


Top-3: git_basics_getting_repository_chunk_004 | score: 0.6193
  Text: 'of nearly all data that the server has. Every version of every file for the history of the project is pulled down by default when you run `git clone`.In fact, if your server disk gets corrupted, you c'
  Source: data/raw/01_git_basics_getting_repository.md
  Domain: git


Top-4: git_basics_getting_repository_chunk_001 | score: 0.6169
  Text: 'mits, and how to push and pull from remote repositories.\n\n## Getting a Git Repository\n\nYou typically obtain a Git repository in one of two ways:\n\n  1.You can take a local directory that is currently n'
  Source: data/raw/01_git_basics_getting_repository.md
  Domain: git


Top-5: gitlab_getting_started_chunk_001 | score: 0.6153
  Text: '- Understand Git concepts\n## Repositories\n\nA Git repository is a directory that contains all the files, folders, and version\nhistory of your project.It serves as a central hub where Git manages and tr'
  Source: data/raw/09_gitlab_getting_started.md
  Domain: gitlab



## Query 2: What is a Git branch and how do I create one?

Top-1: gitlab_getting_started_chunk_000 | score: 0.6283
  Text: '# Get started with Git\n\nGit is a version control system you use to track changes to your code and collaborate with others.\nGitLab is a web-based Git repository manager that provides CI/CD and other fe'
  Source: data/raw/09_gitlab_getting_started.md
  Domain: gitlab


Top-2: git_basics_getting_repository_chunk_000 | score: 0.6198
  Text: '# Git Basics — Getting a Git Repository\n\nIf you can read only one chapter to get going with Git, this is it. This chapter covers every basic command you need to do the vast majority of the things you’'
  Source: data/raw/01_git_basics_getting_repository.md
  Domain: git


Top-3: github_about_git_chunk_009 | score: 0.608
  Text: 'it push` updates the remote repository with any commits made locally to a branch.\n\nFor more information, see the full reference guide to Git commands.### Example: Contribute to an existing repository\n'
  Source: data/raw/08_github_about_git.md
  Domain: github


Top-4: github_about_git_chunk_005 | score: 0.6045
  Text: 'development process. Work is organized into repositories where developers can outline requirements or direction and set expectations for team members.Then, using the GitHub flow, developers simply cre'
  Source: data/raw/08_github_about_git.md
  Domain: github


Top-5: branching_branch_management_chunk_000 | score: 0.6006
  Text: '# Git Branching — Branch Management\n\n## Branch Management\n\nNow that you’ve created, merged, and deleted some branches, let’s look at some branch-management tools that will come in handy when you begin'
  Source: data/raw/04_branching_branch_management.md
  Domain: git



## Query 3: How to resolve merge conflicts in Git?

Top-1: branching_basic_branching_merging_chunk_013 | score: 0.7773
  Text: 't@github.com\n    </div>\n\nThis resolution has a little of each section, and the `<<<<<<<`, `=======`, and `>>>>>>>` lines have been completely removed.After you’ve resolved each of these sections in ea'
  Source: data/raw/03_branching_basic_branching_merging.md
  Domain: git


Top-2: branching_basic_branching_merging_chunk_015 | score: 0.7655
  Text: 'exit the merge tool, Git asks you if the merge was successful. If you tell the script that it was, it stages the file to mark it as resolved for you.You can run `git status` again to verify that all c'
  Source: data/raw/03_branching_basic_branching_merging.md
  Domain: git


Top-3: branching_basic_branching_merging_chunk_010 | score: 0.7012
  Text: 'r issue-tracking system, and delete the branch:\n\n    $ git branch -d iss53\n\n### Basic Merge Conflicts\n\nOccasionally, this process doesn’t go smoothly.If you changed the same part of the same file diff'
  Source: data/raw/03_branching_basic_branching_merging.md
  Domain: git


Top-4: branching_basic_branching_merging_chunk_011 | score: 0.6813
  Text: 'files are unmerged at any point after a merge conflict, you can run `git status`:\n\n    $ git status\n    On branch master\n    You have unmerged paths.(fix conflicts and run "git commit")\n\n    Unmerged '
  Source: data/raw/03_branching_basic_branching_merging.md
  Domain: git


Top-5: branching_basic_branching_merging_chunk_009 | score: 0.6707
  Text: 'ed from some older point. Because the commit on the branch you’re on isn’t a direct ancestor of the branch you’re merging in, Git has to do some work.In this case, Git does a simple three-way merge, u'
  Source: data/raw/03_branching_basic_branching_merging.md
  Domain: git



## Query 4: What is the difference between git add and git commit?

Top-1: github_about_git_chunk_007 | score: 0.6224
  Text: "e and take a snapshot of the changes to include them in the project's history. This command performs staging, the first part of that two-step process.Any changes that are staged will become a part of "
  Source: data/raw/08_github_about_git.md
  Domain: github


Top-2: git_basics_recording_changes_chunk_029 | score: 0.5995
  Text: 'it provides a simple shortcut. Adding the `-a` option to the `git commit` command makes Git automatically stage every file that is already tracked before doing the commit, letting you skip the `git ad'
  Source: data/raw/02_git_basics_recording_changes.md
  Domain: git


Top-3: github_about_git_chunk_009 | score: 0.58
  Text: 'it push` updates the remote repository with any commits made locally to a branch.\n\nFor more information, see the full reference guide to Git commands.### Example: Contribute to an existing repository\n'
  Source: data/raw/08_github_about_git.md
  Domain: github


Top-4: gitlab_getting_started_chunk_001 | score: 0.5745
  Text: '- Understand Git concepts\n## Repositories\n\nA Git repository is a directory that contains all the files, folders, and version\nhistory of your project.It serves as a central hub where Git manages and tr'
  Source: data/raw/09_gitlab_getting_started.md
  Domain: gitlab


Top-5: git_basics_recording_changes_chunk_008 | score: 0.5647
  Text: 'section named “Changes not staged for commit” — which means that a file that is tracked has been modified in the working directory but not yet staged.To stage it, you run the `git add` command. `git a'
  Source: data/raw/02_git_basics_recording_changes.md
  Domain: git



## Query 5: How do I stash my changes temporarily?

Top-1: git_tools_stashing_cleaning_chunk_000 | score: 0.6238
  Text: '# Git Tools — Stashing and Cleaning\n\n## Stashing and Cleaning\n\nOften, when you’ve been working on part of your project, things are in a messy state and you want to switch branches for a bit to work on'
  Source: data/raw/07_git_tools_stashing_cleaning.md
  Domain: git


Top-2: git_tools_stashing_cleaning_chunk_004 | score: 0.6061
  Text: 'tashed works. You can reapply the one you just stashed by using the command shown in the help output of the original stash command: `git stash apply`.If you want to apply one of the older stashes, you'
  Source: data/raw/07_git_tools_stashing_cleaning.md
  Domain: git


Top-3: git_tools_stashing_cleaning_chunk_001 | score: 0.569
  Text: 'ou can reapply at any time (even on a different branch).\n\nMigrating to `git stash push` As of late October 2017, there has been extensive discussion on the Git mailing list, wherein the command `git s'
  Source: data/raw/07_git_tools_stashing_cleaning.md
  Domain: git


Top-4: git_tools_stashing_cleaning_chunk_006 | score: 0.5624
  Text: 'n’t restaged. To do that, you must run the `git stash apply` command with a `--index` option to tell the command to try to reapply the staged changes.If you had run that instead, you’d have gotten bac'
  Source: data/raw/07_git_tools_stashing_cleaning.md
  Domain: git


Top-5: git_tools_stashing_cleaning_chunk_005 | score: 0.5593
  Text: 'no changes added to commit (use "git add" and/or "git commit -a")\n\nYou can see that Git re-modifies the files you reverted when you saved the stash.In this case, you had a clean working directory when'
  Source: data/raw/07_git_tools_stashing_cleaning.md
  Domain: git



## Query 6: How do I merge a branch in GitLab?

Top-1: gitlab_getting_started_chunk_004 | score: 0.7394
  Text: 'ify the same lines of code\nin both branches, GitLab flags these as merge conflicts.\nThese must be resolved manually by reviewing and editing the code.### Delete a branch\n\nAfter a successful merge, you'
  Source: data/raw/09_gitlab_getting_started.md
  Domain: gitlab


Top-2: gitlab_merge_requests_chunk_014 | score: 0.7366
  Text: 'lose a merge request without merging, by selecting Delete source branch.\n\nAn administrator can make this option the default in the project’s settings.For merge requests from forks, GitLab reads the De'
  Source: data/raw/10_gitlab_merge_requests.md
  Domain: gitlab


Top-3: gitlab_merge_requests_chunk_016 | score: 0.7201
  Text: '2 merges into `feature-alpha`. The updated merge request 1, which now contains the contents of `feature-alpha` and `feature-beta`, merges into `main`.This feature works only when a merge request is me'
  Source: data/raw/10_gitlab_merge_requests.md
  Domain: gitlab


Top-4: gitlab_merge_requests_chunk_012 | score: 0.7173
  Text: '* Only Maintainers and higher roles can merge into the default branch.\n  * Developers can merge any merge request that targets a non-protected branch.To determine if you have permission to merge a spe'
  Source: data/raw/10_gitlab_merge_requests.md
  Domain: gitlab


Top-5: gitlab_merge_requests_chunk_002 | score: 0.7002
  Text: 'For more information, see assign an assignee and request a reviewer.\n\n## Create a merge request\n\nLearn the different ways to create a merge request.### Use merge request templates\n\nWhen you create a m'
  Source: data/raw/10_gitlab_merge_requests.md
  Domain: gitlab



## Query 7: How do I view the commit history?

Top-1: github_about_git_chunk_000 | score: 0.5679
  Text: '# GitHub — About Git\n\nLearn about the version control system, Git, and how it works with GitHub.\n\n## About version control and Git\n\nA version control system, or VCS, tracks the history of changes as p'
  Source: data/raw/08_github_about_git.md
  Domain: github


Top-2: git_basics_recording_changes_chunk_027 | score: 0.5479
  Text: 'pass the `-v` option to `git commit`. Doing so also puts the diff of your change in the editor so you can see exactly what changes you’re committing.When you exit the editor, Git creates your commit w'
  Source: data/raw/02_git_basics_recording_changes.md
  Domain: git


Top-3: git_tools_rebasing_chunk_016 | score: 0.5321
  Text: 'ht, and shouldn’t be tampered with. From this angle, changing the commit history is almost blasphemous; you’re _lying_ about what actually transpired.So what if there was a messy series of merge commi'
  Source: data/raw/06_git_tools_rebasing.md
  Domain: git


Top-4: git_basics_recording_changes_chunk_021 | score: 0.5159
  Text: 'changes made since your last commit — only changes that are still unstaged. If you’ve staged all of your changes, `git diff` will give you no output.For another example, if you stage the `CONTRIBUTING'
  Source: data/raw/02_git_basics_recording_changes.md
  Domain: git


Top-5: git_basics_recording_changes_chunk_026 | score: 0.5108
  Text: "reen):\n\n    # Please enter the commit message for your changes. Lines starting\n    # with '#' will be ignored, and an empty message aborts the commit.# On branch master\n    # Your branch is up-to-date"
  Source: data/raw/02_git_basics_recording_changes.md
  Domain: git



## Query 8: How to set up SSH keys for GitLab?

Top-1: gitlab_getting_started_chunk_009 | score: 0.7398
  Text: 'ssword each time.\n\nTo use SSH with GitLab, you must:\n\n1. Generate an SSH key pair on your local system.\n1. Add your SSH key to your GitLab account.\n1.Verify your SSH connection to GitLab.\n\nFor more in'
  Source: data/raw/09_gitlab_getting_started.md
  Domain: gitlab


Top-2: gitlab_getting_started_chunk_008 | score: 0.738
  Text: 'en different branches in your local repository.\n- `git add`: Stage changes for commit.\n- `git commit`: Commit staged changes to your local repository.- `git push`: Push local commits to the remote rep'
  Source: data/raw/09_gitlab_getting_started.md
  Domain: gitlab


Top-3: gitlab_getting_started_chunk_000 | score: 0.5195
  Text: '# Get started with Git\n\nGit is a version control system you use to track changes to your code and collaborate with others.\nGitLab is a web-based Git repository manager that provides CI/CD and other fe'
  Source: data/raw/09_gitlab_getting_started.md
  Domain: gitlab


Top-4: gitlab_merge_requests_chunk_017 | score: 0.51
  Text: 'that are not compatible with your project, with license approval policies.\n  6. You request the approval from your manager.\n  7. Your manager:\n     1.Pushes a commit with their final review.\n     2. A'
  Source: data/raw/10_gitlab_merge_requests.md
  Domain: gitlab


Top-5: gitlab_merge_requests_chunk_010 | score: 0.506
  Text: 'DK). To use Ona, you must turn on Ona in your user account.\n  * Push changes from the command line, if you are familiar with Git and the command line.## Assign a user to a merge request\n\nTo assign the'
  Source: data/raw/10_gitlab_merge_requests.md
  Domain: gitlab



## Query 9: What is rebasing and when should I use it?

Top-1: git_tools_rebasing_chunk_009 | score: 0.5023
  Text: '’ll be scorned by friends and family.\n\nWhen you rebase stuff, you’re abandoning existing commits and creating new ones that are similar but different.If you push commits somewhere and others pull them'
  Source: data/raw/06_git_tools_rebasing.md
  Domain: git


Top-2: git_tools_rebasing_chunk_017 | score: 0.4847
  Text: 'from A to B. People in this camp use tools like `rebase` and `filter-branch` to rewrite their commits before they’re merged into the mainline branch.They use tools like `rebase` and `filter-branch`, t'
  Source: data/raw/06_git_tools_rebasing.md
  Domain: git


Top-3: git_tools_rebasing_chunk_008 | score: 0.4676
  Text: 'h (`master`):\n\n    $ git checkout master\n    $ git merge server\n\nYou can remove the `client` and `server` branches because all the work is integrated and you don’t need them anymore, leaving your hist'
  Source: data/raw/06_git_tools_rebasing.md
  Domain: git


Top-4: git_tools_rebasing_chunk_000 | score: 0.4583
  Text: '# Git Tools — Rebasing\n\n## Rebasing\n\nIn Git, there are two main ways to integrate changes from one branch into another: the `merge` and the `rebase`. In this section you’ll learn what rebasing is, how'
  Source: data/raw/06_git_tools_rebasing.md
  Domain: git


Top-5: git_tools_rebasing_chunk_004 | score: 0.4502
  Text: 'is case, you’d do your work in a branch and then rebase your work onto `origin/master` when you were ready to submit your patches to the main project.That way, the maintainer doesn’t have to do any in'
  Source: data/raw/06_git_tools_rebasing.md
  Domain: git



## Query 10: How do I push changes to a remote repository?

Top-1: distributed_workflows_chunk_005 | score: 0.7182
  Text: 'n public clone of the project and push your changes to it. Then, you can send a request to the maintainer of the main project to pull in your changes.The maintainer can then add your repository as a r'
  Source: data/raw/05_distributed_workflows.md
  Domain: git


Top-2: github_about_git_chunk_009 | score: 0.7134
  Text: 'it push` updates the remote repository with any commits made locally to a branch.\n\nFor more information, see the full reference guide to Git commands.### Example: Contribute to an existing repository\n'
  Source: data/raw/08_github_about_git.md
  Domain: github


Top-3: github_about_git_chunk_011 | score: 0.6608
  Text: 'touch README.md\n\n    # git isn\'t aware of the file, stage it\n    git add README.md\n\n    # take a snapshot of the staging area\n    git commit -m "add README to initial commit"\n\n    # provide the path f'
  Source: data/raw/08_github_about_git.md
  Domain: github


Top-4: gitlab_getting_started_chunk_006 | score: 0.6361
  Text: 'Commit your staged changes to your local repository.\n   A commit saves a snapshot of your work and creates a history of the changes to your files.\n1.Push changes: To share your changes with others, pu'
  Source: data/raw/09_gitlab_getting_started.md
  Domain: gitlab


Top-5: gitlab_getting_started_chunk_005 | score: 0.6358
  Text: 'sitory: Create a local copy of the repository by cloning it to your machine.\n   You can work on the project without affecting the original repository.1. Create a new branch: Before you make any change'
  Source: data/raw/09_gitlab_getting_started.md
  Domain: gitlab

