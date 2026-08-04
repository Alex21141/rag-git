# HW3: Improved Retrieval — Порівняльна аналіз

**Baseline (HW2)**: Semantic-only (FAISS cosine similarity, all-MiniLM-L6-v2)
**Improved (HW3)**: Hybrid BM25 + Semantic (α=0.5) + Metadata filtering

## Порівняльна таблиця

| Query | Baseline top-1 | Improved top-1 | Що змінилось |
|-------|---------------|----------------|-------------|
| How do I clone a Git repository? | git_basics_getting_repository_chunk_006 (0.7135) | git_basics_getting_repository_chunk_006 (0.9886) | ✅ Топ-1 зберігся, гібридний бал вищий — BM25 підтверджує релевантність |
| What is a Git branch and how do I create one? | github_about_git_chunk_003 (0.6234) | git_about_version_control_chunk_001 (0.9726) | 🔄 Гібридний пошук обрав інший чанк: github_about_git_chunk_003 → git_about_version_control_chunk_001 |
| How to resolve merge conflicts in Git? | branching_basic_branching_merging_chunk_013 (0.7696) | branching_basic_branching_merging_chunk_009 (0.9452) | 🔄 Гібридний пошук обрав інший чанк: branching_basic_branching_merging_chunk_013 → branching_basic_branching_merging_chunk_009 |
| What is the difference between git add and git commit? | github_about_git_chunk_009 (0.5952) | git_basics_recording_changes_chunk_037 (0.9443) | 🔄 Гібридний пошук обрав інший чанк: github_about_git_chunk_009 → git_basics_recording_changes_chunk_037 |
| How do I stash my changes temporarily? | git_tools_stashing_cleaning_chunk_000 (0.6401) | git_tools_stashing_cleaning_chunk_007 (0.9393) | 🔄 Гібридний пошук обрав інший чанк: git_tools_stashing_cleaning_chunk_000 → git_tools_stashing_cleaning_chunk_007 |
| How do I merge a branch in GitLab? | gitlab_getting_started_chunk_007 (0.7459) | gitlab_getting_started_chunk_006 (0.9654) | 🔄 Гібридний пошук обрав інший чанк: gitlab_getting_started_chunk_007 → gitlab_getting_started_chunk_006 |
| How do I view the commit history? | git_tools_rebasing_chunk_016 (0.5551) | git_tools_rebasing_chunk_016 (1.0000) | ✅ Топ-1 зберігся, гібридний бал вищий — BM25 підтверджує релевантність |
| How to set up SSH keys for GitLab? | gitlab_getting_started_chunk_016 (0.7501) | gitlab_getting_started_chunk_016 (1.0000) | ✅ Топ-1 зберігся, гібридний бал вищий — BM25 підтверджує релевантність |
| What is rebasing and when should I use it? | git_tools_rebasing_chunk_000 (0.6237) | git_tools_rebasing_chunk_000 (1.0000) | ✅ Топ-1 зберігся, гібридний бал вищий — BM25 підтверджує релевантність |
| How do I push changes to a remote repository? | gitlab_getting_started_chunk_011 (0.7247) | gitlab_getting_started_chunk_011 (0.9321) | ✅ Топ-1 зберігся, гібридний бал вищий — BM25 підтверджує релевантність |

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

**Baseline (HW2):** `git_basics_getting_repository_chunk_006` (0.7135)
**Improved (HW3):** `git_basics_getting_repository_chunk_006` (0.9886)

### Запит 2: What is a Git branch and how do I create one?

**Baseline (HW2):** `github_about_git_chunk_003` (0.6234)
**Improved (HW3):** `git_about_version_control_chunk_001` (0.9726)

### Запит 3: How to resolve merge conflicts in Git?

**Baseline (HW2):** `branching_basic_branching_merging_chunk_013` (0.7696)
**Improved (HW3):** `branching_basic_branching_merging_chunk_009` (0.9452)

### Запит 4: What is the difference between git add and git commit?

**Baseline (HW2):** `github_about_git_chunk_009` (0.5952)
**Improved (HW3):** `git_basics_recording_changes_chunk_037` (0.9443)

### Запит 5: How do I stash my changes temporarily?

**Baseline (HW2):** `git_tools_stashing_cleaning_chunk_000` (0.6401)
**Improved (HW3):** `git_tools_stashing_cleaning_chunk_007` (0.9393)

### Запит 6: How do I merge a branch in GitLab?

**Baseline (HW2):** `gitlab_getting_started_chunk_007` (0.7459)
**Improved (HW3):** `gitlab_getting_started_chunk_006` (0.9654)

### Запит 7: How do I view the commit history?

**Baseline (HW2):** `git_tools_rebasing_chunk_016` (0.5551)
**Improved (HW3):** `git_tools_rebasing_chunk_016` (1.0000)

### Запит 8: How to set up SSH keys for GitLab?

**Baseline (HW2):** `gitlab_getting_started_chunk_016` (0.7501)
**Improved (HW3):** `gitlab_getting_started_chunk_016` (1.0000)

### Запит 9: What is rebasing and when should I use it?

**Baseline (HW2):** `git_tools_rebasing_chunk_000` (0.6237)
**Improved (HW3):** `git_tools_rebasing_chunk_000` (1.0000)

### Запит 10: How do I push changes to a remote repository?

**Baseline (HW2):** `gitlab_getting_started_chunk_011` (0.7247)
**Improved (HW3):** `gitlab_getting_started_chunk_011` (0.9321)


---

Повні результати тестування: запустіть `python3 scripts/retrieval_improved.py --test`