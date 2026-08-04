# HW2: Semantic Retrieval — Test Results

**Model**: sentence-transformers/all-MiniLM-L6-v2

**Chunks**: 159

**Index**: FAISS (IndexFlatIP, dim=384)

**Top-k**: 5

## Summary

| Metric | Value |
|--------|-------|
| Total chunks indexed | 159 |
| Embedding model | sentence-transformers/all-MiniLM-L6-v2 |
| Embedding dimension | 384 |
| Vector storage | FAISS IndexFlatIP |
| Test queries | 10 |
| Top-k | 5 |

## Query 1: How do I clone a Git repository?

Top-1: git_basics_getting_repository_chunk_006 | score: 0.7135
  Text: 'clone the Git linkable library called `libgit2`, you can do so like this:\n\n    $ git clone\n\nThat creates a directory named `libgit2`, initializes a `.git` directory inside it, pulls down all the data '
  Source: data/raw/01_git_basics_getting_repository.md
  Domain: git


Top-2: git_basics_getting_repository_chunk_005 | score: 0.6633
  Text: 'y\n\nIf you want to get a copy of an existing Git repository — for example, a project you’d like to contribute to — the command you need is `git clone`.If you’re familiar with other VCSs such as Subvers'
  Source: data/raw/01_git_basics_getting_repository.md
  Domain: git


Top-3: github_about_git_chunk_008 | score: 0.6385
  Text: 'copy, create, change, and combine code. These commands can be executed directly from the command line or by using an application like GitHub Desktop.Here are some common commands for using Git:\n\n* `gi'
  Source: data/raw/08_github_about_git.md
  Domain: github


Top-4: github_about_git_chunk_011 | score: 0.6288
  Text: 'ository\n\n```bash\n# download a repository on GitHub to our machine\n# Replace `owner/repo` with the owner and name of the repository to clone\ngit clone nges to github\ngit push --set-upstream origin my-b'
  Source: data/raw/08_github_about_git.md
  Domain: github


Top-5: git_basics_getting_repository_chunk_004 | score: 0.622
  Text: "$ git commit -m 'Initial project version'\n\nWe’ll go over what these commands do in just a minute. At this point, you have a Git repository with tracked files and an initial commit.\n\n### Cloning an Exi"
  Source: data/raw/01_git_basics_getting_repository.md
  Domain: git



## Query 2: What is a Git branch and how do I create one?

Top-1: github_about_git_chunk_003 | score: 0.6234
  Text: 'on barriers between teams and keep them focused on doing their best work. Plus, Git makes it possible to align experts across a business to collaborate on major projects.\n\n## About repositories\n\nA rep'
  Source: data/raw/08_github_about_git.md
  Domain: github


Top-2: gitlab_getting_started_chunk_010 | score: 0.6182
  Text: 'ow.\nA standard Git workflow includes the following steps:\n\n1. Clone a repository: Create a local copy of the repository by cloning it to your machine.You can work on the project without affecting the '
  Source: data/raw/09_gitlab_getting_started.md
  Domain: gitlab


Top-3: gitlab_getting_started_chunk_001 | score: 0.6121
  Text: 'and control.\n\nLearning Git is part of a larger workflow:\n\nChoose your learning path:\n\n- Install Git\n- Tutorial: Make your first Git commit\n- Understand Git concepts\n## Repositories\n\nA Git repository i'
  Source: data/raw/09_gitlab_getting_started.md
  Domain: gitlab


Top-4: gitlab_getting_started_chunk_014 | score: 0.6083
  Text: 'The installation process varies depending on your operating system.\nFor example, Windows, macOS, or Linux.\nFor information on how to install Git, se## Git commands\n\nTo interact with Git from the comma'
  Source: data/raw/09_gitlab_getting_started.md
  Domain: gitlab


Top-5: git_about_version_control_chunk_001 | score: 0.5965
  Text: 'how to get it set up to start working with. At the end of this chapter you should understand why Git is around, why you should use it and you should be all set up to do so.\n\n## About Version Control\n\n'
  Source: data/raw/00_git_about_version_control.md
  Domain: git



## Query 3: How to resolve merge conflicts in Git?

Top-1: branching_basic_branching_merging_chunk_013 | score: 0.7696
  Text: 'ricky merge conflicts, we cover more on merging in Advanced Merging.\n---|---\n\nAfter you exit the merge tool, Git asks you if the merge was successful.If you tell the script that it was, it stages the '
  Source: data/raw/03_branching_basic_branching_merging.md
  Domain: git


Top-2: branching_basic_branching_merging_chunk_009 | score: 0.707
  Text: '’t go smoothly. If you changed the same part of the same file differently in the two branches you’re merging, Git won’t be able to merge them cleanly.If your fix for issue #53 modified the same part o'
  Source: data/raw/03_branching_basic_branching_merging.md
  Domain: git


Top-3: branching_basic_branching_merging_chunk_011 | score: 0.6924
  Text: 'like everything in the bottom part. In order to resolve the conflict, you have to either choose one side or the other or merge the contents yourself.For instance, you might resolve this conflict by re'
  Source: data/raw/03_branching_basic_branching_merging.md
  Domain: git


Top-4: branching_basic_branching_merging_chunk_010 | score: 0.6594
  Text: '"git add <file>..." to mark resolution)\n\n        both modified:      index.html\n\n    no changes added to commit (use "git add" and/or "git commit -a")Anything that has merge conflicts and hasn’t been '
  Source: data/raw/03_branching_basic_branching_merging.md
  Domain: git


Top-5: gitlab_getting_started_chunk_008 | score: 0.6458
  Text: 'xample, if you modify the same lines of code\nin both branches, GitLab flags these as merge conflicts.\nThese must be resolved manually by reviewing andediting the code.\n\n### Delete a branch\n\nAfter a su'
  Source: data/raw/09_gitlab_getting_started.md
  Domain: gitlab



## Query 4: What is the difference between git add and git commit?

Top-1: github_about_git_chunk_009 | score: 0.5952
  Text: 'istory. Staging and committing separately gives developers complete control over the history of their project without changing how they code and work.* `git commit` saves the snapshot to the project h'
  Source: data/raw/08_github_about_git.md
  Domain: github


Top-2: git_basics_recording_changes_chunk_008 | score: 0.5608
  Text: 'in your directory. The `git add` command takes a path name for either a file or a directory; if it’s a directory, the command adds all the files in that directory recursively.\n\n### Staging Modified Fi'
  Source: data/raw/02_git_basics_recording_changes.md
  Domain: git


Top-3: git_basics_getting_repository_chunk_004 | score: 0.5546
  Text: "$ git commit -m 'Initial project version'\n\nWe’ll go over what these commands do in just a minute. At this point, you have a Git repository with tracked files and an initial commit.\n\n### Cloning an Exi"
  Source: data/raw/01_git_basics_getting_repository.md
  Domain: git


Top-4: git_basics_recording_changes_chunk_009 | score: 0.5533
  Text: 'On branch master\n    Your branch is up-to-date with \'origin/master\'.\n    Changes to be committed:\n      (use "git reset HEAD <file>..." to unstage)new file:   README\n\n    Changes not staged for commit'
  Source: data/raw/02_git_basics_recording_changes.md
  Domain: git


Top-5: github_about_git_chunk_003 | score: 0.5525
  Text: 'on barriers between teams and keep them focused on doing their best work. Plus, Git makes it possible to align experts across a business to collaborate on major projects.\n\n## About repositories\n\nA rep'
  Source: data/raw/08_github_about_git.md
  Domain: github



## Query 5: How do I stash my changes temporarily?

Top-1: git_tools_stashing_cleaning_chunk_000 | score: 0.6401
  Text: '- Stashing and Cleaning\n\n## Stashing and Cleaning\n\nOften, when you’ve been working on part of your project, things are in a messy state and you want to switch branches for a bit to work on something e'
  Source: data/raw/07_git_tools_stashing_cleaning.md
  Domain: git


Top-2: git_tools_stashing_cleaning_chunk_006 | score: 0.6112
  Text: 'to discard changes in working directory)\n\n    \tmodified:   index.html\n    \tmodified:   lib/simplegit.rb\n\n    no changes added to commit (use "git add"and/or "git commit -a")\n\nYou can see that Git re-m'
  Source: data/raw/07_git_tools_stashing_cleaning.md
  Domain: git


Top-3: git_tools_stashing_cleaning_chunk_007 | score: 0.5624
  Text: 'n’t restaged. To do that, you must run the `git stash apply` command with a `--index` option to tell the command to try to reapply the staged changes.If you had run that instead, you’d have gotten bac'
  Source: data/raw/07_git_tools_stashing_cleaning.md
  Domain: git


Top-4: git_tools_stashing_cleaning_chunk_002 | score: 0.5421
  Text: 'away any time soon, so don’t worry about it suddenly disappearing. But you might want to start migrating over to the `push` alternative for the new functionality.\n---|---\n\n### Stashing Your Work\n\nTo d'
  Source: data/raw/07_git_tools_stashing_cleaning.md
  Domain: git


Top-5: git_tools_stashing_cleaning_chunk_005 | score: 0.5239
  Text: 'can use `git stash list`:\n\n    $ git stash list\n    stash@{0}: WIP on master: 049d078 Create index file\n    stash@{1}: WIP on master: c264051 Revert "Add file_size"\n    stash@{2}: WIP on master: 21d80'
  Source: data/raw/07_git_tools_stashing_cleaning.md
  Domain: git



## Query 6: How do I merge a branch in GitLab?

Top-1: gitlab_getting_started_chunk_007 | score: 0.7459
  Text: '.\nYou can do this in a merge request.\nMerging is a safe way to bring changes from one branch into another while preserving the\nhistory of the changes.If there are conflicts between the branches, for e'
  Source: data/raw/09_gitlab_getting_started.md
  Domain: gitlab


Top-2: gitlab_getting_started_chunk_006 | score: 0.6954
  Text: 'you to create an isolated environment where you can make and test\nchanges without affecting the default branch.\nIn GitLab, the default branch is usually called `main`.\n\n### Merge a branch\n\nAfter a fea'
  Source: data/raw/09_gitlab_getting_started.md
  Domain: gitlab


Top-3: gitlab_getting_started_chunk_008 | score: 0.6915
  Text: 'xample, if you modify the same lines of code\nin both branches, GitLab flags these as merge conflicts.\nThese must be resolved manually by reviewing andediting the code.\n\n### Delete a branch\n\nAfter a su'
  Source: data/raw/09_gitlab_getting_started.md
  Domain: gitlab


Top-4: gitlab_getting_started_chunk_015 | score: 0.6518
  Text: 'anges from the remote repository and merge them into your local branch.\n\nFor more comprehensive information and detailed explanations,\nsee the common Git commands guide.\n\n### Use SSH with Git\n\nWhen yo'
  Source: data/raw/09_gitlab_getting_started.md
  Domain: gitlab


Top-5: branching_branch_management_chunk_003 | score: 0.6494
  Text: 'ut the merge state with respect to some other branch without checking that other branch out first, as in, what is not merged into the `master` branch?A\n      featureB\n\n---|---\n\n### Changing a branch n'
  Source: data/raw/04_branching_branch_management.md
  Domain: git



## Query 7: How do I view the commit history?

Top-1: git_tools_rebasing_chunk_016 | score: 0.5551
  Text: 'ository’s commit history is a record of what actually happened. It’s a historical document, valuable in its own right, and shouldn’t be tampered with.From this angle, changing the commit history is al'
  Source: data/raw/06_git_tools_rebasing.md
  Domain: git


Top-2: git_basics_recording_changes_chunk_028 | score: 0.5388
  Text: 'o (`master`), what SHA-1 checksum the commit has (`463dc4f`), how many files were changed, and statistics about lines added and removed in the commit.Remember that the commit records the snapshot you '
  Source: data/raw/02_git_basics_recording_changes.md
  Domain: git


Top-3: git_tools_rebasing_chunk_010 | score: 0.5366
  Text: 'eate a merge commit which includes both lines of history, and your repository will look like this:\n\nIf you run a `git log` when your history looks like this, you’ll see two commits that have the same '
  Source: data/raw/06_git_tools_rebasing.md
  Domain: git


Top-4: git_basics_recording_changes_chunk_027 | score: 0.5319
  Text: 'help you remember what you’re committing.\n\n  For an even more explicit reminder of what you’ve modified, you can pass the `-v` option to `git commit`.Doing so also puts the diff of your change in the '
  Source: data/raw/02_git_basics_recording_changes.md
  Domain: git


Top-5: git_basics_getting_repository_chunk_001 | score: 0.5254
  Text: 'atterns, how to undo mistakes quickly and easily, how to browse the history of your project and view changes between commits, and how to push and pullfrom remote repositories.\n\n## Getting a Git Reposi'
  Source: data/raw/01_git_basics_getting_repository.md
  Domain: git



## Query 8: How to set up SSH keys for GitLab?

Top-1: gitlab_getting_started_chunk_016 | score: 0.7501
  Text: 'When you work with remote repositories, you should use SSH for secure communication.\n\nGitLab uses the SSH protocol to securely communicate with Git.When you use SSH keys to authenticate to the GitLab '
  Source: data/raw/09_gitlab_getting_started.md
  Domain: gitlab


Top-2: gitlab_getting_started_chunk_015 | score: 0.6254
  Text: 'anges from the remote repository and merge them into your local branch.\n\nFor more comprehensive information and detailed explanations,\nsee the common Git commands guide.\n\n### Use SSH with Git\n\nWhen yo'
  Source: data/raw/09_gitlab_getting_started.md
  Domain: gitlab


Top-3: gitlab_getting_started_chunk_004 | score: 0.5034
  Text: 'your local repository.\n- Push: Push your changes to a remote Git repository hosted on GitLab. This makes your changes available to other team members.- Pull: Pull changes made by others from the remot'
  Source: data/raw/09_gitlab_getting_started.md
  Domain: gitlab


Top-4: gitlab_getting_started_chunk_013 | score: 0.4968
  Text: 'y of the repository that exists in your own namespace.\nUse this workflow when contributing to open-source projects or when your team uses a\ncentralized repository.\n\n## Install Git\n\nTo use Git commands'
  Source: data/raw/09_gitlab_getting_started.md
  Domain: gitlab


Top-5: gitlab_getting_started_chunk_005 | score: 0.4541
  Text: 'by others from the remote repository, and ensure that your local repository is updated with the latest changes.\n\nFor more information, see common Gitcommands.\n\n## Branches\n\nIn Git, you can use branche'
  Source: data/raw/09_gitlab_getting_started.md
  Domain: gitlab



## Query 9: What is rebasing and when should I use it?

Top-1: git_tools_rebasing_chunk_000 | score: 0.6237
  Text: '- Rebasing\n\n## Rebasing\n\nIn Git, there are two main ways to integrate changes from one branch into another: the `merge` and the `rebase`. In this section you’ll learn what rebasing is, how to do it, w'
  Source: data/raw/06_git_tools_rebasing.md
  Domain: git


Top-2: git_tools_rebasing_chunk_008 | score: 0.5893
  Text: 'nches because all the work is integrated and you don’t need them anymore, leaving your history for this entire process looking like Final commit histo$ git branch -d server\n\n### The Perils of Rebasing'
  Source: data/raw/06_git_tools_rebasing.md
  Domain: git


Top-3: git_tools_rebasing_chunk_017 | score: 0.5583
  Text: 'hey’re merged into the mainline branch. They use tools like `rebase` and `filter-branch`, to tell the story in the way that’s best for future readers.Now, to the question of whether merging or rebasin'
  Source: data/raw/06_git_tools_rebasing.md
  Domain: git


Top-4: git_tools_rebasing_chunk_005 | score: 0.5558
  Text: 'y that is different. Rebasing replays changes from one line of work onto another in the order they were introduced, whereas merging takes the endpoints and merges them together.\n\n### More Interesting '
  Source: data/raw/06_git_tools_rebasing.md
  Domain: git


Top-5: git_tools_rebasing_chunk_001 | score: 0.5317
  Text: 'r: the `merge` and the `rebase`. In this section you’ll learn what rebasing is, how to do it, why it’s a pretty amazing tool, and in what cases you won’t want to use it.\n\n### The Basic Rebase\n\nIf you '
  Source: data/raw/06_git_tools_rebasing.md
  Domain: git



## Query 10: How do I push changes to a remote repository?

Top-1: gitlab_getting_started_chunk_011 | score: 0.7247
  Text: 'your work and creates a history of the changes to your files.\n1. Push changes: To share your changes with others, push them to the remote repository.This makes your changes available to other collabor'
  Source: data/raw/09_gitlab_getting_started.md
  Domain: gitlab


Top-2: gitlab_getting_started_chunk_004 | score: 0.7041
  Text: 'your local repository.\n- Push: Push your changes to a remote Git repository hosted on GitLab. This makes your changes available to other team members.- Pull: Pull changes made by others from the remot'
  Source: data/raw/09_gitlab_getting_started.md
  Domain: gitlab


Top-3: distributed_workflows_chunk_007 | score: 0.6683
  Text: 'own public repository and read access to everyone else’s. This scenario often includes a canonical repository that represents the “official” project.To contribute to that project, you create your own '
  Source: data/raw/05_distributed_workflows.md
  Domain: git


Top-4: github_about_git_chunk_010 | score: 0.6236
  Text: 'pers use this command if a teammate has made commits to a branch on a remote, and they would like to reflect those changes in their local environment.ting repository\n\n```bash\n# download a repository o'
  Source: data/raw/08_github_about_git.md
  Domain: github


Top-5: git_basics_getting_repository_chunk_001 | score: 0.5763
  Text: 'atterns, how to undo mistakes quickly and easily, how to browse the history of your project and view changes between commits, and how to push and pullfrom remote repositories.\n\n## Getting a Git Reposi'
  Source: data/raw/01_git_basics_getting_repository.md
  Domain: git

