# HW2: Semantic Retrieval — Test Results

**Model**: sentence-transformers/all-MiniLM-L6-v2

**Chunks**: 157

**Index**: FAISS (IndexFlatIP, dim=384)

**Top-k**: 5

## Summary

| Metric | Value |
|--------|-------|
| Total chunks indexed | 157 |
| Embedding model | sentence-transformers/all-MiniLM-L6-v2 |
| Embedding dimension | 384 |
| Vector storage | FAISS IndexFlatIP |
| Test queries | 10 |
| Top-k | 5 |

## Query 1: How do I clone a Git repository?

Top-1: git_basics_getting_repository_chunk_007 | score: 0.6763
  Text: 'The Git linkable library called `libgit2`, you can do so like this:\n\n    $ git clone\n\nThat creates a directory named `libgit2`, initializes a git` directory inside it, pulls down all the data for that'
  Source: data/raw/01_git_basics_getting_repository.md
  Domain: git


Top-2: git_basics_getting_repository_chunk_006 | score: 0.6707
  Text: 'If you want to get a copy of an existing Git repository — for example, a project you’d like to contribute to — the command you need is `git If you’re familiar with other VCSs such as Subversion, you’l'
  Source: data/raw/01_git_basics_getting_repository.md
  Domain: git


Top-3: github_about_git_chunk_009 | score: 0.6449
  Text: 'Copy, create, change, and combine code. These commands can be executed directly from the command line or by using an application like GitHub Here are some common commands for using Git:\n\n* `git init` '
  Source: data/raw/08_github_about_git.md
  Domain: github


Top-4: git_basics_getting_repository_chunk_005 | score: 0.6308
  Text: "Version'\n\nWe’ll go over what these commands do in just a minute. At this point, you have a Git repository with tracked files and an initial commit. ### Cloning an Existing Repository\n\nIf you want to g"
  Source: data/raw/01_git_basics_getting_repository.md
  Domain: git


Top-5: gitlab_getting_started_chunk_015 | score: 0.6229
  Text: 'Process varies depending on your operating system.\nFor example, Windows, macOS, or Linux.\nFor information on how to install Git, see install ## Git commands\n\nTo interact with Git from the command line'
  Source: data/raw/09_gitlab_getting_started.md
  Domain: gitlab



## Query 2: What is a Git branch and how do I create one?

Top-1: gitlab_getting_started_chunk_002 | score: 0.6726
  Text: 'Git is part of a larger workflow:\n\nChoose your learning path:\n\n- Install Git\n- Tutorial: Make your first Git commit\n- Understand Git concepts ## Repositories\n\nA Git repository is a directory that cont'
  Source: data/raw/09_gitlab_getting_started.md
  Domain: gitlab


Top-2: gitlab_getting_started_chunk_015 | score: 0.6456
  Text: 'Process varies depending on your operating system.\nFor example, Windows, macOS, or Linux.\nFor information on how to install Git, see install ## Git commands\n\nTo interact with Git from the command line'
  Source: data/raw/09_gitlab_getting_started.md
  Domain: gitlab


Top-3: gitlab_getting_started_chunk_001 | score: 0.6348
  Text: '# Get started with Git\n\nGit is a version control system you use to track changes to your code and collaborate with others.\nGitLab is a web-based Git repository manager that provides CI/CD and other fe'
  Source: data/raw/09_gitlab_getting_started.md
  Domain: gitlab


Top-4: gitlab_getting_started_chunk_011 | score: 0.6237
  Text: 'A standard Git workflow includes the following steps:\n\n1. Clone a repository: Create a local copy of the repository by cloning it to your You can work on the project without affecting the original rep'
  Source: data/raw/09_gitlab_getting_started.md
  Domain: gitlab


Top-5: github_about_git_chunk_004 | score: 0.6174
  Text: 'And keep them focused on doing their best work. Plus, Git makes it possible to align experts across a business to collaborate on major projects. ## About repositories\n\nA repository, or Git project, en'
  Source: data/raw/08_github_about_git.md
  Domain: github



## Query 3: How to resolve merge conflicts in Git?

Top-1: branching_basic_branching_merging_chunk_014 | score: 0.7433
  Text: 'Tricky merge conflicts, we cover more on merging in Advanced Merging.\n\nAfter you exit the merge tool, Git asks you if the merge was If you tell the script that it was, it stages the file to mark it as'
  Source: data/raw/03_branching_basic_branching_merging.md
  Domain: git


Top-2: branching_basic_branching_merging_chunk_010 | score: 0.6985
  Text: 'Go smoothly. If you changed the same part of the same file differently in the two branches you’re merging, Git won’t be able to merge them If your fix for issue #53 modified the same part of a file as'
  Source: data/raw/03_branching_basic_branching_merging.md
  Domain: git


Top-3: branching_basic_branching_merging_chunk_009 | score: 0.6914
  Text: 'No further need for the `iss53` branch. You can close the issue in your issue-tracking system, and delete the branch:\n\n    $ git branch -d iss53 ### Basic Merge Conflicts\n\nOccasionally, this process d'
  Source: data/raw/03_branching_basic_branching_merging.md
  Domain: git


Top-4: branching_basic_branching_merging_chunk_012 | score: 0.6857
  Text: 'Like everything in the bottom part. In order to resolve the conflict, you have to either choose one side or the other or merge the contents For instance, you might resolve this conflict by replacing t'
  Source: data/raw/03_branching_basic_branching_merging.md
  Domain: git


Top-5: gitlab_getting_started_chunk_009 | score: 0.6621
  Text: 'The same lines of code\nin both branches, GitLab flags these as merge conflicts.\nThese must be resolved manually by reviewing and editing the code. ### Delete a branch\n\nAfter a successful merge, you ca'
  Source: data/raw/09_gitlab_getting_started.md
  Domain: gitlab



## Query 4: What is the difference between git add and git commit?

Top-1: github_about_git_chunk_010 | score: 0.6026
  Text: 'Staging and committing separately gives developers complete control over the history of their project without changing how they code and * `git commit` saves the snapshot to the project history and co'
  Source: data/raw/08_github_about_git.md
  Domain: github


Top-2: git_basics_recording_changes_chunk_009 | score: 0.5969
  Text: 'Add` command takes a path name for either a file or a directory; if it’s a directory, the command adds all the files in that directory recursively. ### Staging Modified Files\n\nLet’s change a file that'
  Source: data/raw/02_git_basics_recording_changes.md
  Domain: git


Top-3: gitlab_getting_started_chunk_002 | score: 0.5854
  Text: 'Git is part of a larger workflow:\n\nChoose your learning path:\n\n- Install Git\n- Tutorial: Make your first Git commit\n- Understand Git concepts ## Repositories\n\nA Git repository is a directory that cont'
  Source: data/raw/09_gitlab_getting_started.md
  Domain: gitlab


Top-4: git_basics_recording_changes_chunk_010 | score: 0.5592
  Text: 'On branch master\n    Your branch is up-to-date with \'origin/master\'.\n    Changes to be committed:\n      (use "git reset HEAD <file>..." to new file:   README\n\n    Changes not staged for commit:\n      '
  Source: data/raw/02_git_basics_recording_changes.md
  Domain: git


Top-5: github_about_git_chunk_004 | score: 0.5507
  Text: 'And keep them focused on doing their best work. Plus, Git makes it possible to align experts across a business to collaborate on major projects. ## About repositories\n\nA repository, or Git project, en'
  Source: data/raw/08_github_about_git.md
  Domain: github



## Query 5: How do I stash my changes temporarily?

Top-1: git_tools_stashing_cleaning_chunk_001 | score: 0.6282
  Text: '## Stashing and Cleaning\n\nOften, when you’ve been working on part of your project, things are in a messy state and you want to switch branches for a bit to work on something else. The problem is, you '
  Source: data/raw/07_git_tools_stashing_cleaning.md
  Domain: git


Top-2: git_tools_stashing_cleaning_chunk_007 | score: 0.5762
  Text: 'Discard changes in working directory)\n\n    \tmodified:   index.html\n    \tmodified:   lib/simplegit.rb\n\n    no changes added to commit (use "git and/or "git commit -a")\n\nYou can see that Git re-modifies'
  Source: data/raw/07_git_tools_stashing_cleaning.md
  Domain: git


Top-3: git_tools_stashing_cleaning_chunk_008 | score: 0.5575
  Text: 'Restaged. To do that, you must run the `git stash apply` command with a `--index` option to tell the command to try to reapply the staged If you had run that instead, you’d have gotten back to your or'
  Source: data/raw/07_git_tools_stashing_cleaning.md
  Domain: git


Top-4: git_tools_stashing_cleaning_chunk_003 | score: 0.5571
  Text: 'So don’t worry about it suddenly disappearing. But you might want to start migrating over to the `push` alternative for the new functionality. ### Stashing Your Work\n\nTo demonstrate stashing, you’ll g'
  Source: data/raw/07_git_tools_stashing_cleaning.md
  Domain: git


Top-5: git_tools_stashing_cleaning_chunk_014 | score: 0.5396
  Text: 'To discard changes in working directory)\n\n    \tmodified:   lib/simplegit.rb\n\n    Dropped refs/stash@{0} ### Cleaning your Working Directory\n\nFinally, you may not want to stash some work or files in yo'
  Source: data/raw/07_git_tools_stashing_cleaning.md
  Domain: git



## Query 6: How do I merge a branch in GitLab?

Top-1: gitlab_getting_started_chunk_008 | score: 0.7543
  Text: 'You can do this in a merge request.\nMerging is a safe way to bring changes from one branch into another while preserving the\nhistory of the If there are conflicts between the branches, for example, if'
  Source: data/raw/09_gitlab_getting_started.md
  Domain: gitlab


Top-2: gitlab_getting_started_chunk_009 | score: 0.7361
  Text: 'The same lines of code\nin both branches, GitLab flags these as merge conflicts.\nThese must be resolved manually by reviewing and editing the code. ### Delete a branch\n\nAfter a successful merge, you ca'
  Source: data/raw/09_gitlab_getting_started.md
  Domain: gitlab


Top-3: gitlab_getting_started_chunk_007 | score: 0.706
  Text: 'Environment where you can make and test\nchanges without affecting the default branch.\nIn GitLab, the default branch is usually called `main`. ### Merge a branch\n\nAfter a feature is complete or a bug i'
  Source: data/raw/09_gitlab_getting_started.md
  Domain: gitlab


Top-4: gitlab_getting_started_chunk_016 | score: 0.6629
  Text: 'Repository and merge them into your local branch.\n\nFor more comprehensive information and detailed explanations,\nsee the common Git commands guide. ### Use SSH with Git\n\nWhen you work with remote repo'
  Source: data/raw/09_gitlab_getting_started.md
  Domain: gitlab


Top-5: branching_branch_management_chunk_004 | score: 0.6101
  Text: 'The merge state with respect to some other branch without checking that other branch out first, as in, what is not merged into the `master` ### Changing a branch name\n\n  Do not rename branches that ar'
  Source: data/raw/04_branching_branch_management.md
  Domain: git



## Query 7: How do I view the commit history?

Top-1: git_tools_rebasing_chunk_016 | score: 0.6134
  Text: 'Commit history is a record of what actually happened. It’s a historical document, valuable in its own right, and shouldn’t be tampered From this angle, changing the commit history is almost blasphemou'
  Source: data/raw/06_git_tools_rebasing.md
  Domain: git


Top-2: git_basics_getting_repository_chunk_002 | score: 0.6104
  Text: 'Quickly and easily, how to browse the history of your project and view changes between commits, and how to push and pull from remote repositories. ## Getting a Git Repository\n\nYou typically obtain a G'
  Source: data/raw/01_git_basics_getting_repository.md
  Domain: git


Top-3: git_basics_recording_changes_chunk_029 | score: 0.5551
  Text: 'You remember what you’re committing.\n\n  For an even more explicit reminder of what you’ve modified, you can pass the `-v` option to `git Doing so also puts the diff of your change in the editor so you'
  Source: data/raw/02_git_basics_recording_changes.md
  Domain: git


Top-4: github_about_git_chunk_001 | score: 0.5486
  Text: '## About version control and Git\n\nA version control system, or VCS, tracks the history of changes as people and teams collaborate on projects together. As developers make changes to the project, any e'
  Source: data/raw/08_github_about_git.md
  Domain: github


Top-5: git_basics_recording_changes_chunk_028 | score: 0.5481
  Text: '`EDITOR` environment variable — usually vim or emacs, although you can configure it with whatever you want using the `git config --global #\tmodified:   CONTRIBUTING.md\n    #\n    ~\n    ~\n    ~\n    ".gi'
  Source: data/raw/02_git_basics_recording_changes.md
  Domain: git



## Query 8: How to set up SSH keys for GitLab?

Top-1: gitlab_getting_started_chunk_017 | score: 0.741
  Text: 'When you work with remote repositories, you should use SSH for secure communication.\n\nGitLab uses the SSH protocol to securely communicate with When you use SSH keys to authenticate to the GitLab remo'
  Source: data/raw/09_gitlab_getting_started.md
  Domain: gitlab


Top-2: gitlab_getting_started_chunk_016 | score: 0.6328
  Text: 'Repository and merge them into your local branch.\n\nFor more comprehensive information and detailed explanations,\nsee the common Git commands guide. ### Use SSH with Git\n\nWhen you work with remote repo'
  Source: data/raw/09_gitlab_getting_started.md
  Domain: gitlab


Top-3: gitlab_getting_started_chunk_001 | score: 0.5343
  Text: '# Get started with Git\n\nGit is a version control system you use to track changes to your code and collaborate with others.\nGitLab is a web-based Git repository manager that provides CI/CD and other fe'
  Source: data/raw/09_gitlab_getting_started.md
  Domain: gitlab


Top-4: gitlab_getting_started_chunk_014 | score: 0.4984
  Text: 'That exists in your own namespace.\nUse this workflow when contributing to open-source projects or when your team uses a\ncentralized repository. ## Install Git\n\nTo use Git commands and contribute to Gi'
  Source: data/raw/09_gitlab_getting_started.md
  Domain: gitlab


Top-5: gitlab_getting_started_chunk_005 | score: 0.4934
  Text: 'Local repository.\n- Push: Push your changes to a remote Git repository hosted on GitLab. This makes your changes available to other team - Pull: Pull changes made by others from the remote repository,'
  Source: data/raw/09_gitlab_getting_started.md
  Domain: gitlab



## Query 9: What is rebasing and when should I use it?

Top-1: git_tools_rebasing_chunk_001 | score: 0.5632
  Text: '## Rebasing\n\nIn Git, there are two main ways to integrate changes from one branch into another: the `merge` and the `rebase`. In this section you’ll learn what rebasing is, how to do it, why it’s a pr'
  Source: data/raw/06_git_tools_rebasing.md
  Domain: git


Top-2: git_tools_rebasing_chunk_017 | score: 0.5355
  Text: 'Merged into the mainline branch. They use tools like `rebase` and `filter-branch`, to tell the story in the way that’s best for future Now, to the question of whether merging or rebasing is better: ho'
  Source: data/raw/06_git_tools_rebasing.md
  Domain: git


Top-3: git_tools_rebasing_chunk_004 | score: 0.4788
  Text: 'To submit your patches to the main project. That way, the maintainer doesn’t have to do any integration work — just a fast-forward or a clean Note that the snapshot pointed to by the final commit you '
  Source: data/raw/06_git_tools_rebasing.md
  Domain: git


Top-4: git_tools_rebasing_chunk_008 | score: 0.4763
  Text: 'Because all the work is integrated and you don’t need them anymore, leaving your history for this entire process looking like Final commit ### The Perils of Rebasing\n\nAhh, but the bliss of rebasing is'
  Source: data/raw/06_git_tools_rebasing.md
  Domain: git


Top-5: git_tools_rebasing_chunk_015 | score: 0.4741
  Text: 'Find it necessary at some point, make sure everyone knows to run `git pull --rebase` to try to make the pain after it happens a little bit simpler. ### Rebase vs. Merge\n\nNow that you’ve seen rebasing '
  Source: data/raw/06_git_tools_rebasing.md
  Domain: git



## Query 10: How do I push changes to a remote repository?

Top-1: gitlab_getting_started_chunk_005 | score: 0.7367
  Text: 'Local repository.\n- Push: Push your changes to a remote Git repository hosted on GitLab. This makes your changes available to other team - Pull: Pull changes made by others from the remote repository,'
  Source: data/raw/09_gitlab_getting_started.md
  Domain: gitlab


Top-2: github_about_git_chunk_011 | score: 0.728
  Text: 'Use this command if a teammate has made commits to a branch on a remote, and they would like to reflect those changes in their local * `git push` updates the remote repository with any commits made lo'
  Source: data/raw/08_github_about_git.md
  Domain: github


Top-3: github_about_git_chunk_013 | score: 0.6896
  Text: 'Commit"\n\n# provide the path for the repository you created on github\ngit remote add origin ### Example: contribute to an existing branch on GitHub\n\nThis example assumes that you already have a project'
  Source: data/raw/08_github_about_git.md
  Domain: github


Top-4: distributed_workflows_chunk_008 | score: 0.6736
  Text: 'Own public repository and read access to everyone else’s. This scenario often includes a canonical repository that represents the “official” To contribute to that project, you create your own public c'
  Source: data/raw/05_distributed_workflows.md
  Domain: git


Top-5: git_basics_getting_repository_chunk_002 | score: 0.6491
  Text: 'Quickly and easily, how to browse the history of your project and view changes between commits, and how to push and pull from remote repositories. ## Getting a Git Repository\n\nYou typically obtain a G'
  Source: data/raw/01_git_basics_getting_repository.md
  Domain: git

