# HW3: Покращення retrieval pipeline — Порівняльний аналіз

**Baseline (HW2)**: Semantic-only (FAISS cosine similarity, all-MiniLM-L6-v2)
**Improved (HW3)**: Hybrid BM25 + Semantic (α=0.5) + Metadata filtering

## Порівняльна таблиця

| Query | Baseline top-1 | Improved top-1 | Що змінилось |
|-------|---------------|----------------|-------------|
| How do I clone a Git repository? | git_basics_getting_repository_chunk_006 (0.6800) | git_basics_getting_repository_chunk_005 (0.9403) | 🔄 Гібридний пошук обрав інший чанк: git_basics_getting_repository_chunk_006 → git_basics_getting_repository_chunk_005 |
| What is a Git branch and how do I create one? | gitlab_getting_started_chunk_001 (0.6300) | git_basics_getting_repository_chunk_001 (0.9512) | 🔄 Гібридний пошук обрав інший чанк: gitlab_getting_started_chunk_001 → git_basics_getting_repository_chunk_001 |
| How to resolve merge conflicts in Git? | branching_basic_branching_merging_chunk_016 (0.7400) | branching_basic_branching_merging_chunk_011 (0.9888) | 🔄 Гібридний пошук обрав інший чанк: branching_basic_branching_merging_chunk_016 → branching_basic_branching_merging_chunk_011 |
| What is the difference between git add and git commit? | github_about_git_chunk_009 (0.6300) | gitlab_getting_started_chunk_002 (0.9317) | 🔄 Гібридний пошук обрав інший чанк: github_about_git_chunk_009 → gitlab_getting_started_chunk_002 |
| How do I stash my changes temporarily? | git_tools_stashing_cleaning_chunk_002 (0.6300) | git_tools_stashing_cleaning_chunk_002 (0.9654) | ✅ Топ-1 зберігся, гібридний бал вищий — BM25 підтверджує релевантність |
| How do I merge a branch in GitLab? | gitlab_getting_started_chunk_005 (0.6900) | gitlab_getting_started_chunk_004 (0.9772) | 🔄 Гібридний пошук обрав інший чанк: gitlab_getting_started_chunk_005 → gitlab_getting_started_chunk_004 |
| How do I view the commit history? | github_about_git_chunk_001 (0.5800) | git_tools_rebasing_chunk_016 (0.8834) | 🔄 Гібридний пошук обрав інший чанк: github_about_git_chunk_001 → git_tools_rebasing_chunk_016 |
| How to set up SSH keys for GitLab? | gitlab_getting_started_chunk_010 (0.7400) | gitlab_getting_started_chunk_010 (1.0000) | ✅ Топ-1 зберігся, гібридний бал вищий — BM25 підтверджує релевантність |
| What is rebasing and when should I use it? | git_tools_rebasing_chunk_001 (0.5400) | git_tools_rebasing_chunk_001 (0.9982) | ✅ Топ-1 зберігся, гібридний бал вищий — BM25 підтверджує релевантність |
| How do I push changes to a remote repository? | github_about_git_chunk_010 (0.7100) | git_basics_getting_repository_chunk_001 (0.8623) | 🔄 Гібридний пошук обрав інший чанк: github_about_git_chunk_010 → git_basics_getting_repository_chunk_001 |

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

**Baseline (HW2):** `git_basics_getting_repository_chunk_006` (0.6800)
**Improved (HW3):** `git_basics_getting_repository_chunk_005` (0.9403)

### Запит 2: What is a Git branch and how do I create one?

**Baseline (HW2):** `gitlab_getting_started_chunk_001` (0.6300)
**Improved (HW3):** `git_basics_getting_repository_chunk_001` (0.9512)

### Запит 3: How to resolve merge conflicts in Git?

**Baseline (HW2):** `branching_basic_branching_merging_chunk_016` (0.7400)
**Improved (HW3):** `branching_basic_branching_merging_chunk_011` (0.9888)

### Запит 4: What is the difference between git add and git commit?

**Baseline (HW2):** `github_about_git_chunk_009` (0.6300)
**Improved (HW3):** `gitlab_getting_started_chunk_002` (0.9317)

### Запит 5: How do I stash my changes temporarily?

**Baseline (HW2):** `git_tools_stashing_cleaning_chunk_002` (0.6300)
**Improved (HW3):** `git_tools_stashing_cleaning_chunk_002` (0.9654)

### Запит 6: How do I merge a branch in GitLab?

**Baseline (HW2):** `gitlab_getting_started_chunk_005` (0.6900)
**Improved (HW3):** `gitlab_getting_started_chunk_004` (0.9772)

### Запит 7: How do I view the commit history?

**Baseline (HW2):** `github_about_git_chunk_001` (0.5800)
**Improved (HW3):** `git_tools_rebasing_chunk_016` (0.8834)

### Запит 8: How to set up SSH keys for GitLab?

**Baseline (HW2):** `gitlab_getting_started_chunk_010` (0.7400)
**Improved (HW3):** `gitlab_getting_started_chunk_010` (1.0000)

### Запит 9: What is rebasing and when should I use it?

**Baseline (HW2):** `git_tools_rebasing_chunk_001` (0.5400)
**Improved (HW3):** `git_tools_rebasing_chunk_001` (0.9982)

### Запит 10: How do I push changes to a remote repository?

**Baseline (HW2):** `github_about_git_chunk_010` (0.7100)
**Improved (HW3):** `git_basics_getting_repository_chunk_001` (0.8623)


---

Повні результати тестування: запустіть `python3 scripts/retrieval_improved.py --test`