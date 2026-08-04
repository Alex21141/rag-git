# HW2: Semantic Retrieval — Test Results

**Model**: sentence-transformers/all-MiniLM-L6-v2

**Chunks**: 158

**Index**: FAISS (IndexFlatIP, dim=384)

**Top-k**: 5

## Summary

| Metric | Value |
|--------|-------|
| Total chunks indexed | 158 |
| Embedding model | sentence-transformers/all-MiniLM-L6-v2 |
| Embedding dimension | 384 |
| Vector storage | FAISS IndexFlatIP |
| Test queries | 10 |
| Top-k | 5 |

## Query 1: How do I clone a Git repository?

Top-1: git_basics_getting_repository_chunk_007 | score: 0.7135
  Text: 'Clone the Git linkable library called `libgit2`, you can do so like this:\n\n    $ git clone\n\nThat creates a directory named `libgit2`, initializes a `. git` directory inside it, pulls down all the data'
  Source: data/raw/01_git_basics_getting_repository.md
  Domain: git


Top-2: git_basics_getting_repository_chunk_006 | score: 0.6633
  Text: 'Y\n\nIf you want to get a copy of an existing Git repository — for example, a project you’d like to contribute to — the command you need is `git clone`. If you’re familiar with other VCSs such as Subver'
  Source: data/raw/01_git_basics_getting_repository.md
  Domain: git


Top-3: github_about_git_chunk_009 | score: 0.6385
  Text: 'Copy, create, change, and combine code. These commands can be executed directly from the command line or by using an application like GitHub Desktop. Here are some common commands for using Git:\n\n* `g'
  Source: data/raw/08_github_about_git.md
  Domain: github


Top-4: github_about_git_chunk_012 | score: 0.6288
  Text: 'Ository\n\n```bash\n# download a repository on GitHub to our machine\n# Replace `owner/repo` with the owner and name of the repository to clone\ngit clone nges to github\ngit push --set-upstream origin my-b'
  Source: data/raw/08_github_about_git.md
  Domain: github


Top-5: git_basics_getting_repository_chunk_005 | score: 0.5993
  Text: "$ Git commit -m 'Initial project version'\n\nWe’ll go over what these commands do in just a minute. At this point, you have a Git repository with tra cked files and an initial commit.\n\n### Cloning an Ex"
  Source: data/raw/01_git_basics_getting_repository.md
  Domain: git



## Query 2: What is a Git branch and how do I create one?

Top-1: distributed_workflows_chunk_013 | score: 0.6231
  Text: 'De Branches". This guide covers all the common Git workflows, and explains how/when to use them. There’s also a section comparing high and low integra tion frequencies. <>\n\n### Workflows Summary\n\nThes'
  Source: data/raw/05_distributed_workflows.md
  Domain: git


Top-2: gitlab_getting_started_chunk_011 | score: 0.6182
  Text: 'Ow.\nA standard Git workflow includes the following steps:\n\n1. Clone a repository: Create a local copy of the repository by cloning it to your machine. You can work on the project without affecting the'
  Source: data/raw/09_gitlab_getting_started.md
  Domain: gitlab


Top-3: github_about_git_chunk_004 | score: 0.6137
  Text: 'On barriers between teams and keep them focused on doing their best work. Plus, Git makes it possible to align experts across a business to collaborat e on major projects.\n\n## About repositories\n\nA re'
  Source: data/raw/08_github_about_git.md
  Domain: github


Top-4: git_about_version_control_chunk_001 | score: 0.6126
  Text: '# Getting Started — About Version Control\n\n# 1.1 Getting Started - About Version Control\n\nThis chapter will be about getting started with Git. We will begin by explaining some background on version co'
  Source: data/raw/00_git_about_version_control.md
  Domain: git


Top-5: gitlab_getting_started_chunk_015 | score: 0.6083
  Text: 'The installation process varies depending on your operating system.\nFor example, Windows, macOS, or Linux.\nFor information on how to install Git, se ## Git commands\n\nTo interact with Git from the comm'
  Source: data/raw/09_gitlab_getting_started.md
  Domain: gitlab



## Query 3: How to resolve merge conflicts in Git?

Top-1: branching_basic_branching_merging_chunk_014 | score: 0.7729
  Text: 'Olving tricky merge conflicts, we cover more on merging in Advanced Merging.\n\nAfter you exit the merge tool, Git asks you if the merge was successful. If you tell the script that it was, it stages the'
  Source: data/raw/03_branching_basic_branching_merging.md
  Domain: git


Top-2: branching_basic_branching_merging_chunk_010 | score: 0.707
  Text: '’T go smoothly. If you changed the same part of the same file differently in the two branches you’re merging, Git won’t be able to merge them cleanly. If your fix for issue #53 modified the same part '
  Source: data/raw/03_branching_basic_branching_merging.md
  Domain: git


Top-3: branching_basic_branching_merging_chunk_012 | score: 0.6924
  Text: 'Like everything in the bottom part. In order to resolve the conflict, you have to either choose one side or the other or merge the contents yourself. For instance, you might resolve this conflict by r'
  Source: data/raw/03_branching_basic_branching_merging.md
  Domain: git


Top-4: branching_basic_branching_merging_chunk_011 | score: 0.6594
  Text: '"Git add <file>..." to mark resolution)\n\n        both modified:      index.html\n\n    no changes added to commit (use "git add" and/or "git commit -a") Anything that has merge conflicts and hasn’t been'
  Source: data/raw/03_branching_basic_branching_merging.md
  Domain: git


Top-5: gitlab_getting_started_chunk_009 | score: 0.6456
  Text: 'Xample, if you modify the same lines of code\nin both branches, GitLab flags these as merge conflicts.\nThese must be resolved manually by reviewing and editing the code.\n\n### Delete a branch\n\nAfter a s'
  Source: data/raw/09_gitlab_getting_started.md
  Domain: gitlab



## Query 4: What is the difference between git add and git commit?

Top-1: github_about_git_chunk_010 | score: 0.5952
  Text: 'Istory. Staging and committing separately gives developers complete control over the history of their project without changing how they code and work. * `git commit` saves the snapshot to the project '
  Source: data/raw/08_github_about_git.md
  Domain: github


Top-2: git_basics_recording_changes_chunk_009 | score: 0.559
  Text: 'In your directory. The `git add` command takes a path name for either a file or a directory; if it’s a directory, the command adds all the files in th at directory recursively.\n\n### Staging Modified F'
  Source: data/raw/02_git_basics_recording_changes.md
  Domain: git


Top-3: git_basics_recording_changes_chunk_010 | score: 0.5533
  Text: 'On branch master\n    Your branch is up-to-date with \'origin/master\'.\n    Changes to be committed:\n      (use "git reset HEAD <file>..." to unstage) new file:   README\n\n    Changes not staged for commi'
  Source: data/raw/02_git_basics_recording_changes.md
  Domain: git


Top-4: git_basics_recording_changes_chunk_031 | score: 0.55
  Text: 'Fore doing the commit, letting you skip the `git add` part:\n\n    $ git status\n    On branch master\n    Your branch is up-to-date with \'origin/master\'. Changes not staged for commit:\n      (use "git ad'
  Source: data/raw/02_git_basics_recording_changes.md
  Domain: git


Top-5: git_basics_recording_changes_chunk_012 | score: 0.543
  Text: '/Master\'.\n    Changes to be committed:\n      (use "git reset HEAD <file>..." to unstage)\n\n        new file:   README\n        modified:   CONTRIBUTING. md\n\n    Changes not staged for commit:\n      (use'
  Source: data/raw/02_git_basics_recording_changes.md
  Domain: git



## Query 5: How do I stash my changes temporarily?

Top-1: git_tools_stashing_cleaning_chunk_001 | score: 0.6401
  Text: '- Stashing and Cleaning\n\n## Stashing and Cleaning\n\nOften, when you’ve been working on part of your project, things are in a messy state and you want to switch branches for a bit to work on something e'
  Source: data/raw/07_git_tools_stashing_cleaning.md
  Domain: git


Top-2: git_tools_stashing_cleaning_chunk_007 | score: 0.6112
  Text: 'To discard changes in working directory)\n\n    \tmodified:   index.html\n    \tmodified:   lib/simplegit.rb\n\n    no changes added to commit (use "git add" and/or "git commit -a")\n\nYou can see that Git re-'
  Source: data/raw/07_git_tools_stashing_cleaning.md
  Domain: git


Top-3: git_tools_stashing_cleaning_chunk_008 | score: 0.5624
  Text: 'N’t restaged. To do that, you must run the `git stash apply` command with a `--index` option to tell the command to try to reapply the staged changes. If you had run that instead, you’d have gotten ba'
  Source: data/raw/07_git_tools_stashing_cleaning.md
  Domain: git


Top-4: git_tools_stashing_cleaning_chunk_003 | score: 0.5612
  Text: 'Ot going away any time soon, so don’t worry about it suddenly disappearing. But you might want to start migrating over to the `push` alternative for t he new functionality.\n\n### Stashing Your Work\n\nTo'
  Source: data/raw/07_git_tools_stashing_cleaning.md
  Domain: git


Top-5: git_tools_stashing_cleaning_chunk_006 | score: 0.5239
  Text: 'Can use `git stash list`:\n\n    $ git stash list\n    stash@{0}: WIP on master: 049d078 Create index file\n    stash@{1}: WIP on master: c264051 Revert " Add file_size"\n    stash@{2}: WIP on master: 21d8'
  Source: data/raw/07_git_tools_stashing_cleaning.md
  Domain: git



## Query 6: How do I merge a branch in GitLab?

Top-1: gitlab_getting_started_chunk_008 | score: 0.7459
  Text: '.\nYou can do this in a merge request.\nMerging is a safe way to bring changes from one branch into another while preserving the\nhistory of the changes. If there are conflicts between the branches, for '
  Source: data/raw/09_gitlab_getting_started.md
  Domain: gitlab


Top-2: gitlab_getting_started_chunk_007 | score: 0.6944
  Text: 'You to create an isolated environment where you can make and test\nchanges without affecting the default branch.\nIn GitLab, the default branch is usual ly called `main`.\n\n### Merge a branch\n\nAfter a fe'
  Source: data/raw/09_gitlab_getting_started.md
  Domain: gitlab


Top-3: gitlab_getting_started_chunk_009 | score: 0.6897
  Text: 'Xample, if you modify the same lines of code\nin both branches, GitLab flags these as merge conflicts.\nThese must be resolved manually by reviewing and editing the code.\n\n### Delete a branch\n\nAfter a s'
  Source: data/raw/09_gitlab_getting_started.md
  Domain: gitlab


Top-4: gitlab_getting_started_chunk_016 | score: 0.6518
  Text: 'Anges from the remote repository and merge them into your local branch.\n\nFor more comprehensive information and detailed explanations,\nsee the common Git commands guide.\n\n### Use SSH with Git\n\nWhen yo'
  Source: data/raw/09_gitlab_getting_started.md
  Domain: gitlab


Top-5: branching_branch_management_chunk_004 | score: 0.6447
  Text: 'Ut the merge state with respect to some other branch without checking that other branch out first, as in, what is not merged into the `master` branch? topicA\n      featureB\n\n### Changing a branch name'
  Source: data/raw/04_branching_branch_management.md
  Domain: git



## Query 7: How do I view the commit history?

Top-1: git_tools_rebasing_chunk_016 | score: 0.5551
  Text: 'Ository’s commit history is a record of what actually happened. It’s a historical document, valuable in its own right, and shouldn’t be tampered with. From this angle, changing the commit history is a'
  Source: data/raw/06_git_tools_rebasing.md
  Domain: git


Top-2: git_tools_rebasing_chunk_010 | score: 0.539
  Text: 'Eate a merge commit which includes both lines of history, and your repository will look like this:\n\nIf you run a `git log` when your history looks lik e this, you’ll see two commits that have the same'
  Source: data/raw/06_git_tools_rebasing.md
  Domain: git


Top-3: git_basics_recording_changes_chunk_029 | score: 0.5388
  Text: 'O (`master`), what SHA-1 checksum the commit has (`463dc4f`), how many files were changed, and statistics about lines added and removed in the commit. Remember that the commit records the snapshot you'
  Source: data/raw/02_git_basics_recording_changes.md
  Domain: git


Top-4: git_basics_getting_repository_chunk_002 | score: 0.5218
  Text: 'Atterns, how to undo mistakes quickly and easily, how to browse the history of your project and view changes between commits, and how to push and pull from remote repositories.\n\n## Getting a Git Repos'
  Source: data/raw/01_git_basics_getting_repository.md
  Domain: git


Top-5: git_basics_recording_changes_chunk_027 | score: 0.5213
  Text: 'Hell’s `EDITOR` environment variable — usually vim or emacs, although you can configure it with whatever you want using the `git config --global core. mmitted:\n    #\tnew file:   README\n    #\tmodified:'
  Source: data/raw/02_git_basics_recording_changes.md
  Domain: git



## Query 8: How to set up SSH keys for GitLab?

Top-1: gitlab_getting_started_chunk_017 | score: 0.7501
  Text: 'When you work with remote repositories, you should use SSH for secure communication.\n\nGitLab uses the SSH protocol to securely communicate with Git. When you use SSH keys to authenticate to the GitLab'
  Source: data/raw/09_gitlab_getting_started.md
  Domain: gitlab


Top-2: gitlab_getting_started_chunk_016 | score: 0.6254
  Text: 'Anges from the remote repository and merge them into your local branch.\n\nFor more comprehensive information and detailed explanations,\nsee the common Git commands guide.\n\n### Use SSH with Git\n\nWhen yo'
  Source: data/raw/09_gitlab_getting_started.md
  Domain: gitlab


Top-3: gitlab_getting_started_chunk_005 | score: 0.5034
  Text: 'Your local repository.\n- Push: Push your changes to a remote Git repository hosted on GitLab. This makes your changes available to other team members. - Pull: Pull changes made by others from the remo'
  Source: data/raw/09_gitlab_getting_started.md
  Domain: gitlab


Top-4: gitlab_getting_started_chunk_014 | score: 0.4859
  Text: 'Y of the repository that exists in your own namespace.\nUse this workflow when contributing to open-source projects or when your team uses a\ncentralize d repository.\n\n## Install Git\n\nTo use Git command'
  Source: data/raw/09_gitlab_getting_started.md
  Domain: gitlab


Top-5: gitlab_getting_started_chunk_006 | score: 0.4516
  Text: 'By others from the remote repository, and ensure that your local repository is updated with the latest changes.\n\nFor more information, see common Git commands.\n\n## Branches\n\nIn Git, you can use branch'
  Source: data/raw/09_gitlab_getting_started.md
  Domain: gitlab



## Query 9: What is rebasing and when should I use it?

Top-1: git_tools_rebasing_chunk_008 | score: 0.5893
  Text: 'Nches because all the work is integrated and you don’t need them anymore, leaving your history for this entire process looking like Final commit histo $ git branch -d server\n\n### The Perils of Rebasin'
  Source: data/raw/06_git_tools_rebasing.md
  Domain: git


Top-2: git_tools_rebasing_chunk_001 | score: 0.5705
  Text: '- Rebasing\n\n## Rebasing\n\nIn Git, there are two main ways to integrate changes from one branch into another: the `merge` and the `rebase`. In this section you’ll learn what rebasing is, how to do it, w'
  Source: data/raw/06_git_tools_rebasing.md
  Domain: git


Top-3: git_tools_rebasing_chunk_017 | score: 0.5583
  Text: 'Hey’re merged into the mainline branch. They use tools like `rebase` and `filter-branch`, to tell the story in the way that’s best for future readers. Now, to the question of whether merging or rebasi'
  Source: data/raw/06_git_tools_rebasing.md
  Domain: git


Top-4: git_tools_rebasing_chunk_005 | score: 0.5578
  Text: 'Y that is different. Rebasing replays changes from one line of work onto another in the order they were introduced, whereas merging takes the endpoint s and merges them together.\n\n### More Interesting'
  Source: data/raw/06_git_tools_rebasing.md
  Domain: git


Top-5: git_tools_rebasing_chunk_004 | score: 0.4891
  Text: 'Y to submit your patches to the main project. That way, the maintainer doesn’t have to do any integration work — just a fast-forward or a clean apply. Note that the snapshot pointed to by the final co'
  Source: data/raw/06_git_tools_rebasing.md
  Domain: git



## Query 10: How do I push changes to a remote repository?

Top-1: gitlab_getting_started_chunk_012 | score: 0.7247
  Text: 'Your work and creates a history of the changes to your files.\n1. Push changes: To share your changes with others, push them to the remote repository. This makes your changes available to other collabo'
  Source: data/raw/09_gitlab_getting_started.md
  Domain: gitlab


Top-2: gitlab_getting_started_chunk_005 | score: 0.7041
  Text: 'Your local repository.\n- Push: Push your changes to a remote Git repository hosted on GitLab. This makes your changes available to other team members. - Pull: Pull changes made by others from the remo'
  Source: data/raw/09_gitlab_getting_started.md
  Domain: gitlab


Top-3: distributed_workflows_chunk_008 | score: 0.6683
  Text: 'Own public repository and read access to everyone else’s. This scenario often includes a canonical repository that represents the “official” project. To contribute to that project, you create your own'
  Source: data/raw/05_distributed_workflows.md
  Domain: git


Top-4: github_about_git_chunk_011 | score: 0.6236
  Text: 'Pers use this command if a teammate has made commits to a branch on a remote, and they would like to reflect those changes in their local environment. ting repository\n\n```bash\n# download a repository '
  Source: data/raw/08_github_about_git.md
  Domain: github


Top-5: git_basics_getting_repository_chunk_002 | score: 0.5637
  Text: 'Atterns, how to undo mistakes quickly and easily, how to browse the history of your project and view changes between commits, and how to push and pull from remote repositories.\n\n## Getting a Git Repos'
  Source: data/raw/01_git_basics_getting_repository.md
  Domain: git

