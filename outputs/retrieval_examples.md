# HW2: Semantic Retrieval — Test Results

**Model**: sentence-transformers/all-MiniLM-L6-v2

**Chunks**: 149

**Index**: FAISS (IndexFlatIP, dim=384)

**Top-k**: 5


Query: How do I clone a Git repository?

Top-1: git_basics_getting_repository_chunk_006 | score: 0.69
  Text: E — see Getting Git on a Server for more details).  You clone a repository with `git clone <url>`. For example, if you want to clone the Git linkable library called `libgit2`, you can do so like this:
  Source: data/raw/01_git_basics_getting_repository.md

Top-2: git_basics_getting_repository_chunk_007 | score: 0.69
  Text: Additional argument:      $ git clone  mylibgit  That command does the same thing as the previous one, but the target directory is called `mylibgit`.  Git has a number of different transfer protocols
  Source: data/raw/01_git_basics_getting_repository.md

Top-3: git_basics_getting_repository_chunk_002 | score: 0.65
  Text: Rom remote repositories.  ## Getting a Git Repository  You typically obtain a Git repository in one of two ways:    1. You can take a local directory that is currently not under version control, and t
  Source: data/raw/01_git_basics_getting_repository.md

Top-4: github_about_git_chunk_007 | score: 0.65
  Text: Copy, create, change, and combine code. These commands can be executed directly from the command line or by using an application like GitHub Desktop. Here are some common commands for using Git:  * `g
  Source: data/raw/08_github_about_git.md

Top-5: github_about_git_chunk_010 | score: 0.63
  Text: `Git push` updates the remote repository with any commits made locally to a branch.  For more information, see the full reference guide to Git commands.  ### Example: Contribute to an existing reposit
  Source: data/raw/08_github_about_git.md

Comment: Relevant — Top-1 and Top-2 correctly point to git clone documentation. All top results from git_basics_getting_repository.

---

Query: What is a Git branch and how do I create one?

Top-1: github_about_git_chunk_004 | score: 0.62
  Text: Of files and folders associated with a project, along with each file's revision history. The file history appears as snapshots in time called commits. The commits can be organized into multiple lines
  Source: data/raw/08_github_about_git.md

Top-2: gitlab_getting_started_chunk_001 | score: 0.61
  Text: # Get started with Git  Git is a version control system you use to track changes to your code and collaborate with others. GitLab is a web-based Git repository manager that provides CI/CD and other fe
  Source: data/raw/09_gitlab_getting_started.md

Top-3: branching_branch_management_chunk_001 | score: 0.61
  Text: # 3.3 Git Branching - Branch Management  Now that you’ve created, merged, and deleted some branches, let’s look at some branch-management tools that will come in handy when you begin using branches al
  Source: data/raw/04_branching_branch_management.md

Top-4: github_about_git_chunk_006 | score: 0.60
  Text: Development process. Work is organized into repositories where developers can outline requirements or direction and set expectations for team members. Then, using the GitHub flow, developers simply cr
  Source: data/raw/08_github_about_git.md

Top-5: gitlab_getting_started_chunk_006 | score: 0.60
  Text: Ow. A standard Git workflow includes the following steps:  1. Clone a repository: Create a local copy of the repository by cloning it to your machine.    You can work on the project without affecting
  Source: data/raw/09_gitlab_getting_started.md

Comment: Not relevant — Top-1 returns gitlab_getting_started_chunk_002 (general GitLab intro) instead of branch-specific content. Semantic model matches Git broadly but misses branch specificity.

---

Query: How to resolve merge conflicts in Git?

Top-1: branching_basic_branching_merging_chunk_011 | score: 0.73
  Text: Issue-tracking system, and delete the branch:      $ git branch -d iss53  ### Basic Merge Conflicts  Occasionally, this process doesn’t go smoothly. If you changed the same part of the same file diffe
  Source: data/raw/03_branching_basic_branching_merging.md

Top-2: branching_basic_branching_merging_chunk_016 | score: 0.71
  Text: On macOS), you can see all the supported tools listed at the top after “one of the following tools.” Just type the name of the tool you’d rather use.    If you need more advanced tools for resolving t
  Source: data/raw/03_branching_basic_branching_merging.md

Top-3: branching_basic_branching_merging_chunk_017 | score: 0.70
  Text: To conclude merge)      Changes to be committed:          modified:   index.html  If you’re happy with that, and you verify that everything that had conflicts has been staged, you can type `git commit
  Source: data/raw/03_branching_basic_branching_merging.md

Top-4: branching_basic_branching_merging_chunk_010 | score: 0.66
  Text: Ed from some older point. Because the commit on the branch you’re on isn’t a direct ancestor of the branch you’re merging in, Git has to do some work. In this case, Git does a simple three-way merge,
  Source: data/raw/03_branching_basic_branching_merging.md

Top-5: branching_basic_branching_merging_chunk_014 | score: 0.65
  Text: Stance, you might resolve this conflict by replacing the entire block with this:      <div id="footer">     please contact us at email.support@github.com     </div>  This resolution has a little of ea
  Source: data/raw/03_branching_basic_branching_merging.md

Comment: Relevant — Top-1 correctly returns the merge conflict resolution section. Score 0.74 confirms strong semantic match.

---

Query: What is the difference between git add and git commit?

Top-1: github_about_git_chunk_008 | score: 0.61
  Text: And take a snapshot of the changes to include them in the project's history. This command performs staging, the first part of that two-step process. Any changes that are staged will become a part of t
  Source: data/raw/08_github_about_git.md

Top-2: git_basics_recording_changes_chunk_007 | score: 0.58
  Text: New file:   README  You can tell that it’s staged because it’s under the “Changes to be committed” heading. If you commit at this point, the version of the file at the time you ran `git add` is what w
  Source: data/raw/02_git_basics_recording_changes.md

Top-3: github_about_git_chunk_004 | score: 0.57
  Text: Of files and folders associated with a project, along with each file's revision history. The file history appears as snapshots in time called commits. The commits can be organized into multiple lines
  Source: data/raw/08_github_about_git.md

Top-4: git_basics_recording_changes_chunk_009 | score: 0.56
  Text: ” — Which means that a file that is tracked has been modified in the working directory but not yet staged. To stage it, you run the `git add` command. `git add` is a multipurpose command — you use it
  Source: data/raw/02_git_basics_recording_changes.md

Top-5: git_basics_recording_changes_chunk_032 | score: 0.55
  Text: " To update what will be committed)       (use "git checkout -- <file>..." to discard changes in working directory)          modified:   CONTRIBUTING.md      no changes added to commit (use "git add"
  Source: data/raw/02_git_basics_recording_changes.md

Comment: Partially relevant — Top-1 points to GitHub About Git which covers both commands, but not the specific difference. A more targeted chunk would be preferable.

---

Query: How do I stash my changes temporarily?

Top-1: git_tools_stashing_cleaning_chunk_001 | score: 0.63
  Text: # 7.3 Git Tools - Stashing and Cleaning  Often, when you’ve been working on part of your project, things are in a messy state and you want to switch branches for a bit to work on something else. The p
  Source: data/raw/07_git_tools_stashing_cleaning.md

Top-2: git_tools_stashing_cleaning_chunk_002 | score: 0.60
  Text: Discussion on the Git mailing list, wherein the command `git stash save` is being deprecated in favour of the existing alternative `git stash push`. The main reason for this is that `git stash push` i
  Source: data/raw/07_git_tools_stashing_cleaning.md

Top-3: git_tools_stashing_cleaning_chunk_006 | score: 0.55
  Text: (Use "git checkout -- <file>..." to discard changes in working directory)      	modified:   index.html     	modified:   lib/simplegit.rb      no changes added to commit (use "git add" and/or "git comm
  Source: data/raw/07_git_tools_stashing_cleaning.md

Top-4: git_tools_stashing_cleaning_chunk_004 | score: 0.54
  Text: Ex state \       "WIP on master: 049d078 Create index file"     HEAD is now at 049d078 Create index file     (To restore them type "git stash apply")  You can now see that your working directory is cl
  Source: data/raw/07_git_tools_stashing_cleaning.md

Top-5: git_tools_stashing_cleaning_chunk_005 | score: 0.54
  Text: Ter: 21d80a5 Add number to log  In this case, two stashes were saved previously, so you have access to three different stashed works. You can reapply the one you just stashed by using the command show
  Source: data/raw/07_git_tools_stashing_cleaning.md

Comment: Relevant — Top-1 correctly returns the stashing section. Score 0.62 is moderate but the result is accurate.

---

Query: How do I merge a branch in GitLab?

Top-1: gitlab_getting_started_chunk_005 | score: 0.74
  Text: Ify the same lines of code in both branches, GitLab flags these as merge conflicts. These must be resolved manually by reviewing and editing the code.  ### Delete a branch  After a successful merge, y
  Source: data/raw/09_gitlab_getting_started.md

Top-2: gitlab_getting_started_chunk_004 | score: 0.71
  Text: An use branches to work on different features, bug fixes, or experiments simultaneously without interfering with each other's work. Branching enables you to create an isolated environment where you ca
  Source: data/raw/09_gitlab_getting_started.md

Top-3: gitlab_getting_started_chunk_009 | score: 0.60
  Text: Use Git commands:  - `git clone`: Clone a repository to your local machine. - `git branch`: List, create, or delete branches in your local repository. - `git checkout`: Switch between different branch
  Source: data/raw/09_gitlab_getting_started.md

Top-4: git_tools_rebasing_chunk_001 | score: 0.57
  Text: # 3.6 Git Branching - Rebasing  In Git, there are two main ways to integrate changes from one branch into another: the `merge` and the `rebase`. In this section you’ll learn what rebasing is, how to d
  Source: data/raw/06_git_tools_rebasing.md

Top-5: branching_branch_management_chunk_002 | score: 0.56
  Text: This point, the `master` branch will be moved forward with your new work. To see the last commit on each branch, you can run `git branch -v`:      $ git branch -v       iss53   93b412c Fix javascript
  Source: data/raw/04_branching_branch_management.md

Comment: Relevant — Top-1 returns GitLab Getting Started content. Score 0.74 is strong. Covers the GitLab merge workflow.

---

Query: How do I view the commit history?

Top-1: github_about_git_chunk_001 | score: 0.54
  Text: # About Git  Learn about the version control system, Git, and how it works with GitHub.  ## About version control and Git  A version control system, or VCS, tracks the history of changes as people and
  Source: data/raw/08_github_about_git.md

Top-2: git_basics_recording_changes_chunk_030 | score: 0.53
  Text: 2 Files changed, 2 insertions(+)      create mode 100644 README  Now you’ve created your first commit! You can see that the commit has given you some output about itself: which branch you committed to
  Source: data/raw/02_git_basics_recording_changes.md

Top-3: git_basics_recording_changes_chunk_029 | score: 0.53
  Text: Remember what you’re committing.    For an even more explicit reminder of what you’ve modified, you can pass the `-v` option to `git commit`. Doing so also puts the diff of your change in the editor s
  Source: data/raw/02_git_basics_recording_changes.md

Top-4: github_about_git_chunk_008 | score: 0.52
  Text: And take a snapshot of the changes to include them in the project's history. This command performs staging, the first part of that two-step process. Any changes that are staged will become a part of t
  Source: data/raw/08_github_about_git.md

Top-5: git_basics_recording_changes_chunk_007 | score: 0.50
  Text: New file:   README  You can tell that it’s staged because it’s under the “Changes to be committed” heading. If you commit at this point, the version of the file at the time you ran `git add` is what w
  Source: data/raw/02_git_basics_recording_changes.md

Comment: Partially relevant — Top-1 returns GitHub About Git intro instead of git log specifics. Score 0.57 is low — semantic model does not distinguish view history from general Git concepts.

---

Query: How to set up SSH keys for GitLab?

Top-1: gitlab_getting_started_chunk_010 | score: 0.73
  Text: Th remote repositories, you should use SSH for secure communication.  GitLab uses the SSH protocol to securely communicate with Git. When you use SSH keys to authenticate to the GitLab remote server,
  Source: data/raw/09_gitlab_getting_started.md

Top-2: gitlab_getting_started_chunk_009 | score: 0.61
  Text: Use Git commands:  - `git clone`: Clone a repository to your local machine. - `git branch`: List, create, or delete branches in your local repository. - `git checkout`: Switch between different branch
  Source: data/raw/09_gitlab_getting_started.md

Top-3: gitlab_getting_started_chunk_001 | score: 0.51
  Text: # Get started with Git  Git is a version control system you use to track changes to your code and collaborate with others. GitLab is a web-based Git repository manager that provides CI/CD and other fe
  Source: data/raw/09_gitlab_getting_started.md

Top-4: gitlab_getting_started_chunk_008 | score: 0.47
  Text: Open-source projects, may use different workflows. For example, forks.  A fork is a personal copy of the repository that exists in your own namespace. Use this workflow when contributing to open-sourc
  Source: data/raw/09_gitlab_getting_started.md

Top-5: gitlab_getting_started_chunk_005 | score: 0.45
  Text: Ify the same lines of code in both branches, GitLab flags these as merge conflicts. These must be resolved manually by reviewing and editing the code.  ### Delete a branch  After a successful merge, y
  Source: data/raw/09_gitlab_getting_started.md

Comment: Relevant — Top-1 correctly returns GitLab Getting Started covering SSH key setup. Score 0.74 is strong.

---

Query: What is rebasing and when should I use it?

Top-1: git_tools_rebasing_chunk_004 | score: 0.58
  Text: Of the integration, but rebasing makes for a cleaner history. If you examine the log of a rebased branch, it looks like a linear history: it appears that all the work happened in series, even when it
  Source: data/raw/06_git_tools_rebasing.md

Top-2: git_tools_rebasing_chunk_018 | score: 0.56
  Text: The question of whether merging or rebasing is better: hopefully you’ll see that it’s not that simple. Git is a powerful tool, and allows you to do many things to and with your history, but every team
  Source: data/raw/06_git_tools_rebasing.md

Top-3: git_tools_rebasing_chunk_010 | score: 0.54
  Text: At an example of how rebasing work that you’ve made public can cause problems. Suppose you clone from a central server and then do some work off that. Your commit history looks like this:  Now, someon
  Source: data/raw/06_git_tools_rebasing.md

Top-4: git_tools_rebasing_chunk_005 | score: 0.52
  Text: — Just a fast-forward or a clean apply.  Note that the snapshot pointed to by the final commit you end up with, whether it’s the last of the rebased commits for a rebase or the final merge commit afte
  Source: data/raw/06_git_tools_rebasing.md

Top-5: git_tools_rebasing_chunk_001 | score: 0.51
  Text: # 3.6 Git Branching - Rebasing  In Git, there are two main ways to integrate changes from one branch into another: the `merge` and the `rebase`. In this section you’ll learn what rebasing is, how to d
  Source: data/raw/06_git_tools_rebasing.md

Comment: Partially relevant — Top-1 returns git_tools_rebasing_chunk_000 but with score 0.50, which is borderline. The chunk is correct but the low score suggests semantic distance from the query phrasing.

---

Query: How do I push changes to a remote repository?

Top-1: github_about_git_chunk_010 | score: 0.73
  Text: `Git push` updates the remote repository with any commits made locally to a branch.  For more information, see the full reference guide to Git commands.  ### Example: Contribute to an existing reposit
  Source: data/raw/08_github_about_git.md

Top-2: github_about_git_chunk_012 | score: 0.69
  Text: To the `my-repo` directory cd my-repo  # create the first file in the project touch README.md  # git isn't aware of the file, stage it git add README.md  # take a snapshot of the staging area git comm
  Source: data/raw/08_github_about_git.md

Top-3: distributed_workflows_chunk_006 | score: 0.66
  Text: Own public repository and read access to everyone else’s. This scenario often includes a canonical repository that represents the “official” project. To contribute to that project, you create your own
  Source: data/raw/05_distributed_workflows.md

Top-4: gitlab_getting_started_chunk_009 | score: 0.60
  Text: Use Git commands:  - `git clone`: Clone a repository to your local machine. - `git branch`: List, create, or delete branches in your local repository. - `git checkout`: Switch between different branch
  Source: data/raw/09_gitlab_getting_started.md

Top-5: github_about_git_chunk_013 | score: 0.59
  Text: GitHub since the last time changes were made locally.  ```bash # change into the `repo` directory cd repo  # update all remote tracking branches, and the currently checked out branch git pull  # chang
  Source: data/raw/08_github_about_git.md

Comment: Relevant — Top-1 returns distributed_workflows_chunk_005 with score 0.72. Covers git push and remote repository operations correctly.

---
