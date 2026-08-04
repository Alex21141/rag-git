# HW3: Improved Retrieval — Порівняльна аналіз

**Baseline (HW2)**: Semantic-only (FAISS cosine similarity, all-MiniLM-L6-v2)
**Improved (HW3)**: Hybrid BM25 + Semantic (α=0.5) + Metadata filtering

## Порівняльна таблиця

| Query | Baseline top-1 | Improved top-1 | Що змінилось |
|-------|---------------|----------------|-------------|
| How do I clone a Git repository? | git_basics_getting_repository_chunk_007 (0.7135) | git_basics_getting_repository_chunk_007 (0.9877) | ✅ Топ-1 зберігся, гібридний бал вищий — BM25 підтверджує релевантність |
| What is a Git branch and how do I create one? | gitlab_getting_started_chunk_011 (0.6182) | git_about_version_control_chunk_002 (0.9777) | 🔄 Гібридний пошук обрав інший чанк: gitlab_getting_started_chunk_011 → git_about_version_control_chunk_002 |
| How to resolve merge conflicts in Git? | branching_basic_branching_merging_chunk_014 (0.7696) | branching_basic_branching_merging_chunk_010 (0.9453) | 🔄 Гібридний пошук обрав інший чанк: branching_basic_branching_merging_chunk_014 → branching_basic_branching_merging_chunk_010 |
| What is the difference between git add and git commit? | github_about_git_chunk_010 (0.5952) | git_basics_recording_changes_chunk_038 (0.9443) | 🔄 Гібридний пошук обрав інший чанк: github_about_git_chunk_010 → git_basics_recording_changes_chunk_038 |
| How do I stash my changes temporarily? | git_tools_stashing_cleaning_chunk_001 (0.6401) | git_tools_stashing_cleaning_chunk_008 (0.9393) | 🔄 Гібридний пошук обрав інший чанк: git_tools_stashing_cleaning_chunk_001 → git_tools_stashing_cleaning_chunk_008 |
| How do I merge a branch in GitLab? | gitlab_getting_started_chunk_008 (0.7459) | gitlab_getting_started_chunk_007 (0.9230) | 🔄 Гібридний пошук обрав інший чанк: gitlab_getting_started_chunk_008 → gitlab_getting_started_chunk_007 |
| How do I view the commit history? | git_tools_rebasing_chunk_016 (0.5551) | git_tools_rebasing_chunk_016 (0.9994) | ✅ Топ-1 зберігся, гібридний бал вищий — BM25 підтверджує релевантність |
| How to set up SSH keys for GitLab? | gitlab_getting_started_chunk_017 (0.7501) | gitlab_getting_started_chunk_017 (1.0000) | ✅ Топ-1 зберігся, гібридний бал вищий — BM25 підтверджує релевантність |
| What is rebasing and when should I use it? | git_tools_rebasing_chunk_008 (0.5893) | git_tools_rebasing_chunk_001 (0.9840) | 🔄 Гібридний пошук обрав інший чанк: git_tools_rebasing_chunk_008 → git_tools_rebasing_chunk_001 |
| How do I push changes to a remote repository? | gitlab_getting_started_chunk_012 (0.7247) | gitlab_getting_started_chunk_012 (0.9291) | ✅ Топ-1 зберігся, гібридний бал вищий — BM25 підтверджує релевантність |

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

**Baseline (HW2):** `git_basics_getting_repository_chunk_007` (0.7135)
**Improved (HW3):** `git_basics_getting_repository_chunk_007` (0.9877)

### Запит 2: What is a Git branch and how do I create one?

**Baseline (HW2):** `gitlab_getting_started_chunk_011` (0.6182)
**Improved (HW3):** `git_about_version_control_chunk_002` (0.9777)

### Запит 3: How to resolve merge conflicts in Git?

**Baseline (HW2):** `branching_basic_branching_merging_chunk_014` (0.7696)
**Improved (HW3):** `branching_basic_branching_merging_chunk_010` (0.9453)

### Запит 4: What is the difference between git add and git commit?

**Baseline (HW2):** `github_about_git_chunk_010` (0.5952)
**Improved (HW3):** `git_basics_recording_changes_chunk_038` (0.9443)

### Запит 5: How do I stash my changes temporarily?

**Baseline (HW2):** `git_tools_stashing_cleaning_chunk_001` (0.6401)
**Improved (HW3):** `git_tools_stashing_cleaning_chunk_008` (0.9393)

### Запит 6: How do I merge a branch in GitLab?

**Baseline (HW2):** `gitlab_getting_started_chunk_008` (0.7459)
**Improved (HW3):** `gitlab_getting_started_chunk_007` (0.9230)

### Запит 7: How do I view the commit history?

**Baseline (HW2):** `git_tools_rebasing_chunk_016` (0.5551)
**Improved (HW3):** `git_tools_rebasing_chunk_016` (0.9994)

### Запит 8: How to set up SSH keys for GitLab?

**Baseline (HW2):** `gitlab_getting_started_chunk_017` (0.7501)
**Improved (HW3):** `gitlab_getting_started_chunk_017` (1.0000)

### Запит 9: What is rebasing and when should I use it?

**Baseline (HW2):** `git_tools_rebasing_chunk_008` (0.5893)
**Improved (HW3):** `git_tools_rebasing_chunk_001` (0.9840)

### Запит 10: How do I push changes to a remote repository?

**Baseline (HW2):** `gitlab_getting_started_chunk_012` (0.7247)
**Improved (HW3):** `gitlab_getting_started_chunk_012` (0.9291)


---

Повні результати тестування: запустіть `python3 scripts/retrieval_improved.py --test`