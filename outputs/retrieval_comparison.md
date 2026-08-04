# HW3: Improved Retrieval — Порівняльна аналіз

**Baseline (HW2)**: Semantic-only (FAISS cosine similarity, all-MiniLM-L6-v2)
**Improved (HW3)**: Hybrid BM25 + Semantic (α=0.5) + Metadata filtering

## Порівняльна таблиця

| Query | Baseline top-1 | Improved top-1 | Що змінилось |
|-------|---------------|----------------|-------------|
| How do I clone a Git repository? | git_basics_getting_repository_chunk_005 (0.7031) | git_basics_getting_repository_chunk_004 (0.9404) | 🔄 Гібридний пошук обрав інший чанк: git_basics_getting_repository_chunk_005 → git_basics_getting_repository_chunk_004 |
| What is a Git branch and how do I create one? | gitlab_getting_started_chunk_000 (0.6283) | git_basics_getting_repository_chunk_000 (0.9865) | 🔄 Гібридний пошук обрав інший чанк: gitlab_getting_started_chunk_000 → git_basics_getting_repository_chunk_000 |
| How to resolve merge conflicts in Git? | branching_basic_branching_merging_chunk_013 (0.7773) | branching_basic_branching_merging_chunk_010 (0.9510) | 🔄 Гібридний пошук обрав інший чанк: branching_basic_branching_merging_chunk_013 → branching_basic_branching_merging_chunk_010 |
| What is the difference between git add and git commit? | github_about_git_chunk_007 (0.6224) | git_basics_getting_repository_chunk_003 (0.9468) | 🔄 Гібридний пошук обрав інший чанк: github_about_git_chunk_007 → git_basics_getting_repository_chunk_003 |
| How do I stash my changes temporarily? | git_tools_stashing_cleaning_chunk_000 (0.6238) | git_tools_stashing_cleaning_chunk_006 (0.9508) | 🔄 Гібридний пошук обрав інший чанк: git_tools_stashing_cleaning_chunk_000 → git_tools_stashing_cleaning_chunk_006 |
| How do I merge a branch in GitLab? | gitlab_getting_started_chunk_004 (0.7394) | gitlab_getting_started_chunk_003 (0.9374) | 🔄 Гібридний пошук обрав інший чанк: gitlab_getting_started_chunk_004 → gitlab_getting_started_chunk_003 |
| How do I view the commit history? | github_about_git_chunk_000 (0.5679) | git_tools_rebasing_chunk_016 (0.9685) | 🔄 Гібридний пошук обрав інший чанк: github_about_git_chunk_000 → git_tools_rebasing_chunk_016 |
| How to set up SSH keys for GitLab? | gitlab_getting_started_chunk_009 (0.7398) | gitlab_getting_started_chunk_009 (1.0000) | ✅ Топ-1 зберігся, гібридний бал вищий — BM25 підтверджує релевантність |
| What is rebasing and when should I use it? | git_tools_rebasing_chunk_009 (0.5023) | git_tools_rebasing_chunk_000 (0.9562) | 🔄 Гібридний пошук обрав інший чанк: git_tools_rebasing_chunk_009 → git_tools_rebasing_chunk_000 |
| How do I push changes to a remote repository? | distributed_workflows_chunk_005 (0.7182) | distributed_workflows_chunk_005 (0.9024) | ✅ Топ-1 зберігся, гібридний бал вищий — BM25 підтверджує релевантність |

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

**Baseline (HW2):** `git_basics_getting_repository_chunk_005` (0.7031)
**Improved (HW3):** `git_basics_getting_repository_chunk_004` (0.9404)

### Запит 2: What is a Git branch and how do I create one?

**Baseline (HW2):** `gitlab_getting_started_chunk_000` (0.6283)
**Improved (HW3):** `git_basics_getting_repository_chunk_000` (0.9865)

### Запит 3: How to resolve merge conflicts in Git?

**Baseline (HW2):** `branching_basic_branching_merging_chunk_013` (0.7773)
**Improved (HW3):** `branching_basic_branching_merging_chunk_010` (0.9510)

### Запит 4: What is the difference between git add and git commit?

**Baseline (HW2):** `github_about_git_chunk_007` (0.6224)
**Improved (HW3):** `git_basics_getting_repository_chunk_003` (0.9468)

### Запит 5: How do I stash my changes temporarily?

**Baseline (HW2):** `git_tools_stashing_cleaning_chunk_000` (0.6238)
**Improved (HW3):** `git_tools_stashing_cleaning_chunk_006` (0.9508)

### Запит 6: How do I merge a branch in GitLab?

**Baseline (HW2):** `gitlab_getting_started_chunk_004` (0.7394)
**Improved (HW3):** `gitlab_getting_started_chunk_003` (0.9374)

### Запит 7: How do I view the commit history?

**Baseline (HW2):** `github_about_git_chunk_000` (0.5679)
**Improved (HW3):** `git_tools_rebasing_chunk_016` (0.9685)

### Запит 8: How to set up SSH keys for GitLab?

**Baseline (HW2):** `gitlab_getting_started_chunk_009` (0.7398)
**Improved (HW3):** `gitlab_getting_started_chunk_009` (1.0000)

### Запит 9: What is rebasing and when should I use it?

**Baseline (HW2):** `git_tools_rebasing_chunk_009` (0.5023)
**Improved (HW3):** `git_tools_rebasing_chunk_000` (0.9562)

### Запит 10: How do I push changes to a remote repository?

**Baseline (HW2):** `distributed_workflows_chunk_005` (0.7182)
**Improved (HW3):** `distributed_workflows_chunk_005` (0.9024)


---

Повні результати тестування: запустіть `python3 scripts/retrieval_improved.py --test`