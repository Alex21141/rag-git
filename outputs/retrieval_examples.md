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

Top-1: git_basics_getting_repository_chunk_005 | score: 0.7268
  Text: 'clone the Git linkable library called `libgit2`, you can do so like this:\n\n    $ git clone\n\nThat creates a directory named `libgit2`, initializes a `.git` directory inside it, pulls down all the data '
  Source: data/raw/01_git_basics_getting_repository.md
  Domain: git


Top-2: git_basics_getting_repository_chunk_004 | score: 0.6847
  Text: 'checkout". This is an important distinction — instead of getting just a working copy, Git receives a full copy of nearly all data that the server has.Every version of every file for the history of the'
  Source: data/raw/01_git_basics_getting_repository.md
  Domain: git


Top-3: github_about_git_chunk_009 | score: 0.6473
  Text: 'For more information, see the full reference guide to Git commands.\n\n### Example: Contribute to an existing repository\n\n```bash\n# download a repository on GitHub to our machine\n# Replace `owner/repo` '
  Source: data/raw/08_github_about_git.md
  Domain: github


Top-4: github_about_git_chunk_006 | score: 0.6456
  Text: 'copy, create, change, and combine code. These commands can be executed directly from the command line or by using an application like GitHub Desktop.Here are some common commands for using Git:\n\n* `gi'
  Source: data/raw/08_github_about_git.md
  Domain: github


Top-5: git_basics_getting_repository_chunk_001 | score: 0.6419
  Text: 'kes quickly and easily, how to browse the history of your project and view changes between commits, and how to push and pull from remote repositories.## Getting a Git Repository\n\nYou typically obtain '
  Source: data/raw/01_git_basics_getting_repository.md
  Domain: git



## Query 2: What is a Git branch and how do I create one?

Top-1: branching_branch_management_chunk_000 | score: 0.631
  Text: '# Git Branching — Branch Management\n\n# 3.3 Git Branching - Branch Management\n\n## Branch Management\n\nNow that you’ve created, merged, and deleted some branches, let’s look at some branch-management too'
  Source: data/raw/04_branching_branch_management.md
  Domain: git


Top-2: github_about_git_chunk_002 | score: 0.6179
  Text: 'iduals, teams and businesses.\n\n* Git lets developers see the entire timeline of their changes, decisions, and progression of any project in one place.From the moment they access the history of a proje'
  Source: data/raw/08_github_about_git.md
  Domain: github


Top-3: github_about_git_chunk_005 | score: 0.6045
  Text: 'development process. Work is organized into repositories where developers can outline requirements or direction and set expectations for team members.Then, using the GitHub flow, developers simply cre'
  Source: data/raw/08_github_about_git.md
  Domain: github


Top-4: gitlab_getting_started_chunk_000 | score: 0.5982
  Text: '# GitLab — Getting started with Git\n\n# Get started with Git\n\nGit is a version control system you use to track changes to your code and collaborate with others.\nGitLab is a web-based Git repository man'
  Source: data/raw/09_gitlab_getting_started.md
  Domain: gitlab


Top-5: github_about_git_chunk_006 | score: 0.5974
  Text: 'copy, create, change, and combine code. These commands can be executed directly from the command line or by using an application like GitHub Desktop.Here are some common commands for using Git:\n\n* `gi'
  Source: data/raw/08_github_about_git.md
  Domain: github



## Query 3: How to resolve merge conflicts in Git?

Top-1: branching_basic_branching_merging_chunk_010 | score: 0.7285
  Text: 'Auto-merging index.html\n    CONFLICT (content): Merge conflict in index.html\n    Automatic merge failed; fix conflicts and then commit the result.Git hasn’t automatically created a new merge commit. I'
  Source: data/raw/03_branching_basic_branching_merging.md
  Domain: git


Top-2: branching_basic_branching_merging_chunk_014 | score: 0.7132
  Text: 'opendiff` in this case because the command was run on macOS), you can see all the supported tools listed at the top after “one of the following tools.” Just type the name of the tool you’d rather use.'
  Source: data/raw/03_branching_basic_branching_merging.md
  Domain: git


Top-3: branching_basic_branching_merging_chunk_011 | score: 0.7093
  Text: 's unmerged. Git adds standard conflict-resolution markers to the files that have conflicts, so you can open them manually and resolve those conflicts.Your file contains a section that looks something '
  Source: data/raw/03_branching_basic_branching_merging.md
  Domain: git


Top-4: branching_basic_branching_merging_chunk_015 | score: 0.7073
  Text: 'If you’re happy with that, and you verify that everything that had conflicts has been staged, you can type `git commit` to finalize the merge commit.The commit message by default looks something like '
  Source: data/raw/03_branching_basic_branching_merging.md
  Domain: git


Top-5: branching_basic_branching_merging_chunk_009 | score: 0.6714
  Text: 'e and automatically creates a new commit that points to it. This is referred to as a merge commit, and is special in that it has more than one parent.Now that your work is merged in, you have no furth'
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


Top-3: gitlab_getting_started_chunk_001 | score: 0.5745
  Text: '- Understand Git concepts\n## Repositories\n\nA Git repository is a directory that contains all the files, folders, and version\nhistory of your project.It serves as a central hub where Git manages and tr'
  Source: data/raw/09_gitlab_getting_started.md
  Domain: gitlab


Top-4: git_basics_recording_changes_chunk_008 | score: 0.5647
  Text: 'section named “Changes not staged for commit” — which means that a file that is tracked has been modified in the working directory but not yet staged.To stage it, you run the `git add` command. `git a'
  Source: data/raw/02_git_basics_recording_changes.md
  Domain: git


Top-5: git_basics_recording_changes_chunk_025 | score: 0.557
  Text: 'reated or modified that you haven’t run `git add` on since you edited them — won’t go into this commit. They will stay as modified files on your disk.In this case, let’s say that the last time you ran'
  Source: data/raw/02_git_basics_recording_changes.md
  Domain: git



## Query 5: How do I stash my changes temporarily?

Top-1: git_tools_stashing_cleaning_chunk_000 | score: 0.6159
  Text: '# Git Tools — Stashing and Cleaning\n\n# 7.3 Git Tools - Stashing and Cleaning\n\n## Stashing and Cleaning\n\nOften, when you’ve been working on part of your project, things are in a messy state and you wan'
  Source: data/raw/07_git_tools_stashing_cleaning.md
  Domain: git


Top-2: git_tools_stashing_cleaning_chunk_001 | score: 0.595
  Text: 'dified tracked files and staged changes — and saves it on a stack of unfinished changes that you can reapply at any time (even on a different branch).Migrating to `git stash push` As of late October 2'
  Source: data/raw/07_git_tools_stashing_cleaning.md
  Domain: git


Top-3: git_tools_stashing_cleaning_chunk_004 | score: 0.545
  Text: 'h@{2}: WIP on master: 21d80a5 Add number to log\n\nIn this case, two stashes were saved previously, so you have access to three different stashed works.You can reapply the one you just stashed by using '
  Source: data/raw/07_git_tools_stashing_cleaning.md
  Domain: git


Top-4: git_tools_stashing_cleaning_chunk_003 | score: 0.5418
  Text: ', run `git stash` or `git stash push`:\n\n    $ git stash\n    Saved working directory and index state \\\n      "WIP on master: 049d078 Create index file"HEAD is now at 049d078 Create index file\n    (To r'
  Source: data/raw/07_git_tools_stashing_cleaning.md
  Domain: git


Top-5: git_tools_stashing_cleaning_chunk_012 | score: 0.541
  Text: 'branch \'testchanges\'\n    On branch testchanges\n    Changes to be committed:\n      (use "git reset HEAD <file>..." to unstage)\n\n    \tmodified:   index.html\n\n    Changes not staged for commit:\n      (us'
  Source: data/raw/07_git_tools_stashing_cleaning.md
  Domain: git



## Query 6: How do I merge a branch in GitLab?

Top-1: gitlab_getting_started_chunk_004 | score: 0.7394
  Text: 'ify the same lines of code\nin both branches, GitLab flags these as merge conflicts.\nThese must be resolved manually by reviewing and editing the code.### Delete a branch\n\nAfter a successful merge, you'
  Source: data/raw/09_gitlab_getting_started.md
  Domain: gitlab


Top-2: gitlab_getting_started_chunk_003 | score: 0.6844
  Text: "ches\n\nIn Git, you can use branches to work on different features, bug fixes, or experiments\nsimultaneously without interfering with each other's work.Branching enables you to create an isolated enviro"
  Source: data/raw/09_gitlab_getting_started.md
  Domain: gitlab


Top-3: gitlab_getting_started_chunk_008 | score: 0.63
  Text: 'en different branches in your local repository.\n- `git add`: Stage changes for commit.\n- `git commit`: Commit staged changes to your local repository.- `git push`: Push local commits to the remote rep'
  Source: data/raw/09_gitlab_getting_started.md
  Domain: gitlab


Top-4: git_tools_rebasing_chunk_000 | score: 0.6086
  Text: '# Git Tools — Rebasing\n\n# 3.6 Git Branching - Rebasing\n\n## Rebasing\n\nIn Git, there are two main ways to integrate changes from one branch into another: the `merge` and the `rebase`. In this section yo'
  Source: data/raw/06_git_tools_rebasing.md
  Domain: git


Top-5: branching_branch_management_chunk_001 | score: 0.5715
  Text: '`*` character that prefixes the `master` branch: it indicates the branch that you currently have checked out (i.e., the branch that `HEAD` points to).This means that if you commit at this point, the `'
  Source: data/raw/04_branching_branch_management.md
  Domain: git



## Query 7: How do I view the commit history?

Top-1: github_about_git_chunk_000 | score: 0.5686
  Text: '# GitHub — About Git\n\n# About Git\n\nLearn about the version control system, Git, and how it works with GitHub.\n\n## About version control and Git\n\nA version control system, or VCS, tracks the history of'
  Source: data/raw/08_github_about_git.md
  Domain: github


Top-2: git_basics_recording_changes_chunk_027 | score: 0.5311
  Text: 'pass the `-v` option to `git commit`. Doing so also puts the diff of your change in the editor so you can see exactly what changes you’re committing.---|---\n\nWhen you exit the editor, Git creates your'
  Source: data/raw/02_git_basics_recording_changes.md
  Domain: git


Top-3: git_tools_rebasing_chunk_009 | score: 0.5262
  Text: 'rk off that. Your commit history looks like this:\n\nNow, someone else does more work that includes a merge, and pushes that work to the central server.You fetch it and merge the new remote branch into '
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


Top-3: gitlab_getting_started_chunk_000 | score: 0.5125
  Text: '# GitLab — Getting started with Git\n\n# Get started with Git\n\nGit is a version control system you use to track changes to your code and collaborate with others.\nGitLab is a web-based Git repository man'
  Source: data/raw/09_gitlab_getting_started.md
  Domain: gitlab


Top-4: gitlab_getting_started_chunk_007 | score: 0.4949
  Text: 'sitory that exists in your own namespace.\nUse this workflow when contributing to open-source projects or when your team uses a\ncentralized repository.## Install Git\n\nTo use Git commands and contribute'
  Source: data/raw/09_gitlab_getting_started.md
  Domain: gitlab


Top-5: gitlab_getting_started_chunk_004 | score: 0.4493
  Text: 'ify the same lines of code\nin both branches, GitLab flags these as merge conflicts.\nThese must be resolved manually by reviewing and editing the code.### Delete a branch\n\nAfter a successful merge, you'
  Source: data/raw/09_gitlab_getting_started.md
  Domain: gitlab



## Query 9: What is rebasing and when should I use it?

Top-1: git_tools_rebasing_chunk_016 | score: 0.564
  Text: 'he way that’s best for future readers.\n\nNow, to the question of whether merging or rebasing is better: hopefully you’ll see that it’s not that simple.Git is a powerful tool, and allows you to do many '
  Source: data/raw/06_git_tools_rebasing.md
  Domain: git


Top-2: git_tools_rebasing_chunk_004 | score: 0.5231
  Text: 'the last of the rebased commits for a rebase or the final merge commit after a merge, is the same snapshot — it’s only the history that is different.Rebasing replays changes from one line of work onto'
  Source: data/raw/06_git_tools_rebasing.md
  Domain: git


Top-3: git_tools_rebasing_chunk_000 | score: 0.5096
  Text: '# Git Tools — Rebasing\n\n# 3.6 Git Branching - Rebasing\n\n## Rebasing\n\nIn Git, there are two main ways to integrate changes from one branch into another: the `merge` and the `rebase`. In this section yo'
  Source: data/raw/06_git_tools_rebasing.md
  Domain: git


Top-4: git_tools_rebasing_chunk_007 | score: 0.4688
  Text: 'master server\n\nThis replays your `server` work on top of your `master` work, as shown in Rebasing your `server` branch on top of your `master` branch.Then, you can fast-forward the base branch (`maste'
  Source: data/raw/06_git_tools_rebasing.md
  Domain: git


Top-5: git_tools_rebasing_chunk_002 | score: 0.4379
  Text: 'g: added staged command\n\nThis operation works by going to the common ancestor of the two branches (the one you’re on and the one you’re rebasing onto), getting the diff introduced by each commit of th'
  Source: data/raw/06_git_tools_rebasing.md
  Domain: git



## Query 10: How do I push changes to a remote repository?

Top-1: git_basics_getting_repository_chunk_001 | score: 0.7058
  Text: 'kes quickly and easily, how to browse the history of your project and view changes between commits, and how to push and pull from remote repositories.## Getting a Git Repository\n\nYou typically obtain '
  Source: data/raw/01_git_basics_getting_repository.md
  Domain: git


Top-2: github_about_git_chunk_011 | score: 0.6612
  Text: 'tial commit"\n\n# provide the path for the repository you created on github\ngit remote add origin https://github.com/YOUR-USERNAME/YOUR-REPOSITORY-NAME.git\n\n# push changes to github\ngit push --set-upstr'
  Source: data/raw/08_github_about_git.md
  Domain: github


Top-3: gitlab_getting_started_chunk_006 | score: 0.6361
  Text: 'Commit your staged changes to your local repository.\n   A commit saves a snapshot of your work and creates a history of the changes to your files.\n1.Push changes: To share your changes with others, pu'
  Source: data/raw/09_gitlab_getting_started.md
  Domain: gitlab


Top-4: gitlab_getting_started_chunk_005 | score: 0.6358
  Text: 'sitory: Create a local copy of the repository by cloning it to your machine.\n   You can work on the project without affecting the original repository.1. Create a new branch: Before you make any change'
  Source: data/raw/09_gitlab_getting_started.md
  Domain: gitlab


Top-5: distributed_workflows_chunk_006 | score: 0.6224
  Text: 'to their public repository.\n\n  2. A contributor clones that repository and makes changes.\n\n  3. The contributor pushes to their own public copy.\n\n  4.The contributor sends the maintainer an email aski'
  Source: data/raw/05_distributed_workflows.md
  Domain: git

