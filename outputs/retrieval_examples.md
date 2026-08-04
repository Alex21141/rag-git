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

## Results with Relevance Analysis

---

### Query 1: How do I clone a Git repository?

Top-1: git_basics_getting_repository_chunk_005 | score: 0.7031
  Text: '`libgit2`, initializes a `.git` directory inside it, pulls down all the data for that repository, and checks out a working copy of the latest version...'
  Source: data/raw/01_git_basics_getting_repository.md
  Domain: git

Top-2: github_about_git_chunk_006 | score: 0.6456
  Text: 'copy, create, change, and combine code. These commands can be executed directly from the command line...'
  Source: data/raw/08_github_about_git.md
  Domain: github

Top-3: git_basics_getting_repository_chunk_004 | score: 0.6193
  Text: 'of nearly all data that the server has. Every version of every file for the history of the project is pulled down by default when you run `git clone`...'
  Source: data/raw/01_git_basics_getting_repository.md
  Domain: git

Top-4: git_basics_getting_repository_chunk_001 | score: 0.6169
  Text: 'mits, and how to push and pull from remote repositories... ## Getting a Git Repository...'
  Source: data/raw/01_git_basics_getting_repository.md
  Domain: git

Top-5: gitlab_getting_started_chunk_001 | score: 0.6153
  Text: '- Understand Git concepts... ## Repositories... A Git repository is a directory...'
  Source: data/raw/09_gitlab_getting_started.md
  Domain: gitlab

**Comment**: Relevant ✅ Top-1 і Top-3 містять точну відповідь про `git clone`. Top-5 — слабко релевантний (про репозиторії загалом, не про clone).

---

### Query 2: What is a Git branch and how do I create one?

Top-1: gitlab_getting_started_chunk_000 | score: 0.6283
  Text: '# Get started with Git... Git is a version control system...'
  Source: data/raw/09_gitlab_getting_started.md
  Domain: gitlab

Top-2: git_basics_getting_repository_chunk_000 | score: 0.6198
  Text: '# Git Basics — Getting a Git Repository... If you can read only one chapter...'
  Source: data/raw/01_git_basics_getting_repository.md
  Domain: git

Top-3: github_about_git_chunk_009 | score: 0.608
  Text: 'it push updates the remote repository with any commits made locally to a branch...'
  Source: data/raw/08_github_about_git.md
  Domain: github

Top-4: github_about_git_chunk_005 | score: 0.6045
  Text: 'development process. Work is organized into repositories... using the GitHub flow, developers simply cre...'
  Source: data/raw/08_github_about_git.md
  Domain: github

Top-5: branching_branch_management_chunk_000 | score: 0.6006
  Text: '# Git Branching — Branch Management... ## Branch Management... Now that you have created, merged, and deleted some branches...'
  Source: data/raw/04_branching_branch_management.md
  Domain: git

**Comment**: Частково релевантний ⚠️ Top-5 має найбільш релевантний контент (про branch management), але не потрапив на Top-1. Top-1-2 — загальні вступи, не про branches. Retrieval не ідеальний для цього запиту — краще працює для конкретних команд.

---

### Query 3: How to resolve merge conflicts in Git?

Top-1: branching_basic_branching_merging_chunk_013 | score: 0.7773
  Text: 'This resolution has a little of each section, and the `<<<<<<<`, `=======`, and `>>>>>>>` lines have been completely removed...'
  Source: data/raw/03_branching_basic_branching_merging.md
  Domain: git

Top-2: branching_basic_branching_merging_chunk_015 | score: 0.7655
  Text: 'exit the merge tool, Git asks you if the merge was successful... stages the file to mark it as resolved...'
  Source: data/raw/03_branching_basic_branching_merging.md
  Domain: git

Top-3: branching_basic_branching_merging_chunk_010 | score: 0.7012
  Text: '### Basic Merge Conflicts... Occasionally, this process doesn't go smoothly. If you changed the same part of the same file...'
  Source: data/raw/03_branching_basic_branching_merging.md
  Domain: git

Top-4: branching_basic_branching_merging_chunk_011 | score: 0.6813
  Text: 'files are unmerged at any point after a merge conflict, you can run `git status`...'
  Source: data/raw/03_branching_basic_branching_merging.md
  Domain: git

Top-5: branching_basic_branching_merging_chunk_009 | score: 0.6707
  Text: 'from some older point. Because the commit on the branch you're on isn't a direct ancestor...'
  Source: data/raw/03_branching_basic_branching_merging.md
  Domain: git

**Comment**: Високо релевантний ✅ Усі 5 результатів — з документа про merge conflicts. Top-1 дає точну інструкцію по розв'язанню конфліктів.

---

### Query 4: What is the difference between git add and git commit?

Top-1: github_about_git_chunk_007 | score: 0.6224
  Text: "staging, the first part of that two-step process. Any changes that are staged will become a part of..."
  Source: data/raw/08_github_about_git.md
  Domain: github

Top-2: git_basics_recording_changes_chunk_029 | score: 0.5995
  Text: 'Adding the `-a` option to the `git commit` command makes Git automatically stage every file...'
  Source: data/raw/02_git_basics_recording_changes.md
  Domain: git

Top-3: github_about_git_chunk_009 | score: 0.58
  Text: 'it push updates the remote repository with any commits made locally to a branch...'
  Source: data/raw/08_github_about_git.md
  Domain: github

Top-4: gitlab_getting_started_chunk_001 | score: 0.5745
  Text: 'A Git repository is a directory that contains all the files, folders, and version history...'
  Source: data/raw/09_gitlab_getting_started.md
  Domain: gitlab

Top-5: git_basics_recording_changes_chunk_008 | score: 0.5647
  Text: 'section named "Changes not staged for commit"... To stage it, you run the `git add` command...'
  Source: data/raw/02_git_basics_recording_changes.md
  Domain: git

**Comment**: Релевантний ✅ Top-1 пояснює staging (git add), Top-5 — `git add` команду. Відповідь розкидана між chunks, але семантика правильна.

---

### Query 5: How do I stash my changes temporarily?

Top-1: git_tools_stashing_cleaning_chunk_000 | score: 0.6238
  Text: '# Git Tools — Stashing and Cleaning... ## Stashing and Cleaning... Often, when you've been working on part of your project...'
  Source: data/raw/07_git_tools_stashing_cleaning.md
  Domain: git

Top-2: git_tools_stashing_cleaning_chunk_004 | score: 0.6061
  Text: 'stashed works. You can reapply the one you just stashed by using... `git stash apply`...'
  Source: data/raw/07_git_tools_stashing_cleaning.md
  Domain: git

Top-3: git_tools_stashing_cleaning_chunk_001 | score: 0.569
  Text: 'ou can reapply at any time (even on a different branch)... Migrating to `git stash push`...'
  Source: data/raw/07_git_tools_stashing_cleaning.md
  Domain: git

Top-4: git_tools_stashing_cleaning_chunk_006 | score: 0.5624
  Text: 'n't restaged. To do that, you must run the `git stash apply` command with a `--index` option...'
  Source: data/raw/07_git_tools_stashing_cleaning.md
  Domain: git

Top-5: git_tools_stashing_cleaning_chunk_005 | score: 0.5593
  Text: 'no changes added to commit (use "git add" and/or "git commit -a")... You can see that Git re-modifies the files...'
  Source: data/raw/07_git_tools_stashing_cleaning.md
  Domain: git

**Comment**: Високо релевантний ✅ Усі 5 результатів — з документа про stashing. Top-1-2 дають точну відповідь.

---

### Query 6: How do I merge a branch in GitLab?

Top-1: gitlab_getting_started_chunk_004 | score: 0.7394
  Text: 'ify the same lines of code in both branches, GitLab flags these as merge conflicts... After a successful merge, you can delete the branch...'
  Source: data/raw/09_gitlab_getting_started.md
  Domain: gitlab

Top-2: gitlab_merge_requests_chunk_014 | score: 0.7366
  Text: 'lose a merge request without merging, by selecting Delete source branch...'
  Source: data/raw/10_gitlab_merge_requests.md
  Domain: gitlab

Top-3: gitlab_merge_requests_chunk_016 | score: 0.7201
  Text: '2 merges into `feature-alpha`... The updated merge request 1, which now contains the contents of `feature-alpha` and `feature-beta`, merges into `main`...'
  Source: data/raw/10_gitlab_merge_requests.md
  Domain: gitlab

Top-4: gitlab_merge_requests_chunk_012 | score: 0.7173
  Text: '* Only Maintainers and higher roles can merge into the default branch... Developers can merge any merge request...'
  Source: data/raw/10_gitlab_merge_requests.md
  Domain: gitlab

Top-5: gitlab_merge_requests_chunk_002 | score: 0.7002
  Text: '## Create a merge request... Learn the different ways to create a merge request...'
  Source: data/raw/10_gitlab_merge_requests.md
  Domain: gitlab

**Comment**: Високо релевантний ✅ Усі 5 результатів — з GitLab докерментації про merge. Domain filter автоматично звужує до gitlab.

---

### Query 7: What is GitLab Flow?

Top-1: gitlab_getting_started_chunk_000 | score: 0.5289
  Text: '# Get started with Git... Git is a version control system...'
  Source: data/raw/09_gitlab_getting_started.md
  Domain: gitlab

Top-2: gitlab_merge_requests_chunk_000 | score: 0.5152
  Text: '# GitLab — Merge Requests... Merge requests provide a central location for your team to review code...'
  Source: data/raw/10_gitlab_merge_requests.md
  Domain: gitlab

Top-3: gitlab_merge_requests_chunk_017 | score: 0.5114
  Text: 'that are not compatible with your project, with license approval policies...'
  Source: data/raw/10_gitlab_merge_requests.md
  Domain: gitlab

Top-4: gitlab_merge_requests_chunk_011 | score: 0.4833
  Text: 'rs... GitLab adds the merge request to the user's Assigned merge requests page...'
  Source: data/raw/10_gitlab_merge_requests.md
  Domain: gitlab

Top-5: gitlab_merge_requests_chunk_018 | score: 0.4814
  Text: 'r web designers to implement their changes... Squashes the commits... Merges the commit...'
  Source: data/raw/10_gitlab_merge_requests.md
  Domain: gitlab

**Comment**: Слабко релевантний ❌ «GitLab Flow» — це специфічна концепція branching strategy, якої немає в поточних документах (документ 09 замінено на getting-started). Top-1 дає загальний вступ, а не відповідь на запит. Потрібен документ про GitLab Flow для покращення.

---

### Query 8: How to set up SSH keys for GitLab?

Top-1: gitlab_getting_started_chunk_009 | score: 0.7398
  Text: 'ssword each time... To use SSH with GitLab, you must: 1. Generate an SSH key pair... 1. Add your SSH key to your GitLab account... 1. Verify your SSH connection...'
  Source: data/raw/09_gitlab_getting_started.md
  Domain: gitlab

Top-2: gitlab_getting_started_chunk_008 | score: 0.738
  Text: 'en different branches in your local repository... `git add`: Stage changes for commit... `git push`: Push local commits...'
  Source: data/raw/09_gitlab_getting_started.md
  Domain: gitlab

Top-3: gitlab_getting_started_chunk_000 | score: 0.5195
  Text: '# Get started with Git... Git is a version control system...'
  Source: data/raw/09_gitlab_getting_started.md
  Domain: gitlab

Top-4: gitlab_merge_requests_chunk_017 | score: 0.51
  Text: 'that are not compatible with your project, with license approval policies...'
  Source: data/raw/10_gitlab_merge_requests.md
  Domain: gitlab

Top-5: gitlab_merge_requests_chunk_010 | score: 0.506
  Text: 'DK). To use Ona, you must turn on Ona in your user account...'
  Source: data/raw/10_gitlab_merge_requests.md
  Domain: gitlab

**Comment**: Високо релевантний ✅ Top-1 дає точну відповідь з 3 кроками налаштування SSH. Top-2 менш релевантний (про git commands).

---

### Query 9: What is rebasing and when should I use it?

Top-1: git_tools_rebasing_chunk_009 | score: 0.5023
  Text: 'When you rebase stuff, you're abandoning existing commits and creating new ones that are similar but different...'
  Source: data/raw/06_git_tools_rebasing.md
  Domain: git

Top-2: git_tools_rebasing_chunk_017 | score: 0.4847
  Text: 'from A to B. People in this camp use tools like `rebase` and `filter-branch` to rewrite their commits...'
  Source: data/raw/06_git_tools_rebasing.md
  Domain: git

Top-3: git_tools_rebasing_chunk_008 | score: 0.4676
  Text: 'h (`master`): $ git checkout master... $ git merge server... You can remove the `client` and `server` branches...'
  Source: data/raw/06_git_tools_rebasing.md
  Domain: git

Top-4: git_tools_rebasing_chunk_000 | score: 0.4583
  Text: '# Git Tools — Rebasing... ## Rebasing... In Git, there are two main ways to integrate changes: the `merge` and the `rebase`...'
  Source: data/raw/06_git_tools_rebasing.md
  Domain: git

Top-5: git_tools_rebasing_chunk_004 | score: 0.4502
  Text: 'is case, you'd do your work in a branch and then rebase your work onto `origin/master` when you were ready...'
  Source: data/raw/06_git_tools_rebasing.md
  Domain: git

**Comment**: Частково релевантний ⚠️ Top-4 краще за Top-1 (дефінує rebasing vs merge), але semantic search ставить Top-9 вище. Top-4 — найбільш релевантний для відповіді на запит.

---

### Query 10: How do I push changes to a remote repository?

Top-1: distributed_workflows_chunk_005 | score: 0.7182
  Text: 'n public clone of the project and push your changes to it. Then, you can send a request to the maintainer...'
  Source: data/raw/05_distributed_workflows.md
  Domain: git

Top-2: github_about_git_chunk_009 | score: 0.7134
  Text: 'it push updates the remote repository with any commits made locally to a branch...'
  Source: data/raw/08_github_about_git.md
  Domain: github

Top-3: github_about_git_chunk_011 | score: 0.6608
  Text: 'touch README.md... git add README.md... git commit -m "add README to initial commit"... provide the path f...'
  Source: data/raw/08_github_about_git.md
  Domain: github

Top-4: gitlab_getting_started_chunk_006 | score: 0.6361
  Text: 'Commit your staged changes to your local repository... 1. Push changes: To share your changes with others, pu...'
  Source: data/raw/09_gitlab_getting_started.md
  Domain: gitlab

Top-5: gitlab_getting_started_chunk_005 | score: 0.6358
  Text: 'sitory: Create a local copy of the repository by cloning it to your machine...'
  Source: data/raw/09_gitlab_getting_started.md
  Domain: gitlab

**Comment**: Високо релевантний ✅ Top-1-2 дають відповідь про push. Багатодоменна релевантність — користь з Git, GitHub і GitLab документів.

---

## Висновок

### Де retrieval працює добре ✅

| Запит | Top-1 score | Причина |
|-------|-------------|---------|
| Merge conflicts | 0.7773 | Специфічний термін, чітко мапується |
| SSH keys GitLab | 0.7398 | Конкретна процедура, чітка семантика |
| Stash changes | 0.6238 | Унікальний термін "stash" |
| Clone repository | 0.7031 | `git clone` — чіткий ключ |
| Push changes | 0.7182 | `push` термін присутній у всіх документах |

### Де retrieval працює слабко ❌

| Запит | Top-1 score | Причина |
|-------|-------------|---------|
| GitLab Flow | 0.5289 | Документ 09 не містить GitLab Flow — концепція відсутня в KB |
| Branch creation | 0.6283 | "branch" — занадто загальний термін, повертає вступи |
| Rebasing | 0.5023 | Top-4 (0.4583) релевантніший за Top-1 |

### Загальні спостереження

1. **Специфічні терміни** (stash, merge conflict, clone) працюють краще за загальні (branch, rebase)
2. **Domain distribution** — git=114 чанків домінує, github/gitlab менше представлені
3. **Відсутній контент** — GitLab Flow концепція немає в KB (потрібно додати)
4. **Середній Top-1 score** — 0.65 (задовільний для all-MiniLM-L6-v2)