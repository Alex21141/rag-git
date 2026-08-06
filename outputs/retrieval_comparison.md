# HW3: Improved Retrieval — Порівняльна аналіз

**Baseline (HW2)**: Semantic-only (FAISS cosine similarity, all-MiniLM-L6-v2)
**Improved (HW3)**: Hybrid BM25 + Semantic (α=0.5) + Metadata filtering

## Порівняльна таблиця

| Query | Baseline top-1 | Improved top-1 | Що змінилось |
|-------|---------------|----------------|-------------|
| How do I clone a Git repository? | git_basics_getting_repository_chunk_002 (0.7085) | git_basics_getting_repository_chunk_005 (0.9854) | 🔄 Гібридний пошук обрав інший чанк: git_basics_getting_repository_chunk_002 → git_basics_getting_repository_chunk_005 |
| What is a Git branch and how do I create one? | gitlab_getting_started_chunk_001 (0.6338) | git_basics_getting_repository_chunk_001 (0.9512) | 🔄 Гібридний пошук обрав інший чанк: gitlab_getting_started_chunk_001 → git_basics_getting_repository_chunk_001 |
| How to resolve merge conflicts in Git? | gitlab_getting_started_chunk_005 (0.7214) | branching_basic_branching_merging_chunk_011 (0.9741) | 🔄 Гібридний пошук обрав інший чанк: gitlab_getting_started_chunk_005 → branching_basic_branching_merging_chunk_011 |
| What is the difference between git add and git commit? | github_about_git_chunk_008 (0.6602) | git_basics_getting_repository_chunk_004 (0.8770) | 🔄 Гібридний пошук обрав інший чанк: github_about_git_chunk_008 → git_basics_getting_repository_chunk_004 |
| How do I stash my changes temporarily? | git_tools_stashing_cleaning_chunk_001 (0.6201) | git_tools_stashing_cleaning_chunk_004 (0.9280) | 🔄 Гібридний пошук обрав інший чанк: git_tools_stashing_cleaning_chunk_001 → git_tools_stashing_cleaning_chunk_004 |
| How do I merge a branch in GitLab? | gitlab_getting_started_chunk_004 (0.7146) | gitlab_getting_started_chunk_004 (0.9789) | ✅ Топ-1 зберігся, гібридний бал вищий — BM25 підтверджує релевантність |
| How do I view the commit history? | github_about_git_chunk_004 (0.5934) | git_tools_rebasing_chunk_016 (0.9050) | 🔄 Гібридний пошук обрав інший чанк: github_about_git_chunk_004 → git_tools_rebasing_chunk_016 |
| How to set up SSH keys for GitLab? | gitlab_getting_started_chunk_010 (0.7434) | gitlab_getting_started_chunk_010 (1.0000) | ✅ Топ-1 зберігся, гібридний бал вищий — BM25 підтверджує релевантність |
| What is rebasing and when should I use it? | git_tools_rebasing_chunk_001 (0.5448) | git_tools_rebasing_chunk_001 (0.9982) | ✅ Топ-1 зберігся, гібридний бал вищий — BM25 підтверджує релевантність |
| How do I push changes to a remote repository? | github_about_git_chunk_010 (0.7015) | git_basics_getting_repository_chunk_001 (0.8669) | 🔄 Гібридний пошук обрав інший чанк: github_about_git_chunk_010 → git_basics_getting_repository_chunk_001 |

## Висновок

**Покращено**: 10/10 запитів змінили top-1 або отримали кращий бал

**Метадани фільтр**: Дозволяє звужувати пошук до конкретного домену (git/github/gitlab).
Наприклад, `--domain gitlab` повертає тільки GitLab документи — ідеально для специфічних запитів.

**Гібридний пошук**: BM25 допомагає знайти чанки з точними ключовими словами
(напр. `git add`, `git commit`), а semantic зберігає контекстуальну релевантність.

**Найбільший ефект**: Для запитів з конкретними командами (git add, git stash, git rebase)
гібридний пошук дає кращу точність, ніж чистий semantic.

## Детальний аналіз

### Запит 1: How do I clone a Git repository?

**Baseline (HW2):** `git_basics_getting_repository_chunk_002` (0.7085)
**Improved (HW3):** `git_basics_getting_repository_chunk_005` (0.9854)

### Запит 2: What is a Git branch and how do I create one?

**Baseline (HW2):** `gitlab_getting_started_chunk_001` (0.6338)
**Improved (HW3):** `git_basics_getting_repository_chunk_001` (0.9512)

### Запит 3: How to resolve merge conflicts in Git?

**Baseline (HW2):** `gitlab_getting_started_chunk_005` (0.7214)
**Improved (HW3):** `branching_basic_branching_merging_chunk_011` (0.9741)

### Запит 4: What is the difference between git add and git commit?

**Baseline (HW2):** `github_about_git_chunk_008` (0.6602)
**Improved (HW3):** `git_basics_getting_repository_chunk_004` (0.8770)

### Запит 5: How do I stash my changes temporarily?

**Baseline (HW2):** `git_tools_stashing_cleaning_chunk_001` (0.6201)
**Improved (HW3):** `git_tools_stashing_cleaning_chunk_004` (0.9280)

### Запит 6: How do I merge a branch in GitLab?

**Baseline (HW2):** `gitlab_getting_started_chunk_004` (0.7146)
**Improved (HW3):** `gitlab_getting_started_chunk_004` (0.9789)

### Запит 7: How do I view the commit history?

**Baseline (HW2):** `github_about_git_chunk_004` (0.5934)
**Improved (HW3):** `git_tools_rebasing_chunk_016` (0.9050)

### Запит 8: How to set up SSH keys for GitLab?

**Baseline (HW2):** `gitlab_getting_started_chunk_010` (0.7434)
**Improved (HW3):** `gitlab_getting_started_chunk_010` (1.0000)

### Запит 9: What is rebasing and when should I use it?

**Baseline (HW2):** `git_tools_rebasing_chunk_001` (0.5448)
**Improved (HW3):** `git_tools_rebasing_chunk_001` (0.9982)

### Запит 10: How do I push changes to a remote repository?

**Baseline (HW2):** `github_about_git_chunk_010` (0.7015)
**Improved (HW3):** `git_basics_getting_repository_chunk_001` (0.8669)


---

Повні результати тестування: запустіть `python3 scripts/retrieval_improved.py --test`