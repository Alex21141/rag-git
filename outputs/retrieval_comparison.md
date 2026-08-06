# HW3: Покращення retrieval pipeline — Порівняльний аналіз

**Baseline (HW2)**: Semantic-only (FAISS cosine similarity, all-MiniLM-L6-v2)
**Improved (HW3)**: Hybrid BM25 + Semantic (α=0.5) + Metadata filtering

## Порівняльна таблиця

| Query | Baseline top-1 | Improved top-1 | Що змінилося |
|-------|---------------|----------------|-------------|
| How do I clone a Git repository? | git_basics_getting_repository_chunk_006 (0.6800) | git_basics_getting_repository_chunk_005 (0.9359) | 🔄 Гібридний пошук обрав інший чанк: git_basics_getting_repository_chunk_006 → git_basics_getting_repository_chunk_005 |
| What is a Git branch and how do I create one? | gitlab_getting_started_chunk_001 (0.6300) | branching_branch_management_chunk_001 (0.9674) | 🔄 Гібридний пошук обрав інший чанк: gitlab_getting_started_chunk_001 → branching_branch_management_chunk_001 |
| How to resolve merge conflicts in Git? | branching_basic_branching_merging_chunk_016 (0.7400) | branching_basic_branching_merging_chunk_011 (0.9888) | 🔄 Гібридний пошук обрав інший чанк: branching_basic_branching_merging_chunk_016 → branching_basic_branching_merging_chunk_011 |
| What is the difference between git add and git commit? | github_about_git_chunk_009 (0.6300) | git_basics_recording_changes_chunk_007 (0.8849) | 🔄 Гібридний пошук обрав інший чанк: github_about_git_chunk_009 → git_basics_recording_changes_chunk_007 |
| How do I stash my changes temporarily? | git_tools_stashing_cleaning_chunk_002 (0.6300) | git_tools_stashing_cleaning_chunk_004 (0.9376) | 🔄 Гібридний пошук обрав інший чанк: git_tools_stashing_cleaning_chunk_002 → git_tools_stashing_cleaning_chunk_004 |
| How do I merge a branch in GitLab? | gitlab_getting_started_chunk_005 (0.6900) | gitlab_getting_started_chunk_004 (0.9983) | 🔄 Гібридний пошук обрав інший чанк: gitlab_getting_started_chunk_005 → gitlab_getting_started_chunk_004 |
| How do I view the commit history? | github_about_git_chunk_001 (0.5800) | github_about_git_chunk_001 (0.9056) | ✅ Top-1 зберігся, гібридний бал вищий — BM25 підтверджує релевантність |
| How to set up SSH keys for GitLab? | gitlab_getting_started_chunk_010 (0.7400) | gitlab_getting_started_chunk_010 (1.0000) | ✅ Top-1 зберігся, гібридний бал вищий — BM25 підтверджує релевантність |
| What is rebasing and when should I use it? | git_tools_rebasing_chunk_001 (0.5400) | git_tools_rebasing_chunk_001 (1.0000) | ✅ Top-1 зберігся, гібридний бал вищий — BM25 підтверджує релевантність |
| How do I push changes to a remote repository? | github_about_git_chunk_010 (0.7100) | github_about_git_chunk_010 (0.9038) | ✅ Top-1 зберігся, гібридний бал вищий — BM25 підтверджує релевантність |

## Висновок

**Покращено**: 10/10 запитів змінили top-1 або отримали кращий бал

**Фільтр за доменом**: Дозволяє звужувати пошук до конкретного домену (git/github/gitlab).
Наприклад, `--domain gitlab` повертає тільки GitLab документи.

**Гібридний пошук**: BM25 допомагає знайти чанки з точними ключовими словами
(напр. `git add`, `git commit`), а semantic зберігає контекстуальну релевантність.

## Детальний аналіз

### Запит 1: How do I clone a Git repository?

**Baseline (HW2):** `git_basics_getting_repository_chunk_006` (0.6800)
**Improved (HW3):** `git_basics_getting_repository_chunk_005` (0.9359)

### Запит 2: What is a Git branch and how do I create one?

**Baseline (HW2):** `gitlab_getting_started_chunk_001` (0.6300)
**Improved (HW3):** `branching_branch_management_chunk_001` (0.9674)

### Запит 3: How to resolve merge conflicts in Git?

**Baseline (HW2):** `branching_basic_branching_merging_chunk_016` (0.7400)
**Improved (HW3):** `branching_basic_branching_merging_chunk_011` (0.9888)

### Запит 4: What is the difference between git add and git commit?

**Baseline (HW2):** `github_about_git_chunk_009` (0.6300)
**Improved (HW3):** `git_basics_recording_changes_chunk_007` (0.8849)

### Запит 5: How do I stash my changes temporarily?

**Baseline (HW2):** `git_tools_stashing_cleaning_chunk_002` (0.6300)
**Improved (HW3):** `git_tools_stashing_cleaning_chunk_004` (0.9376)

### Запит 6: How do I merge a branch in GitLab?

**Baseline (HW2):** `gitlab_getting_started_chunk_005` (0.6900)
**Improved (HW3):** `gitlab_getting_started_chunk_004` (0.9983)

### Запит 7: How do I view the commit history?

**Baseline (HW2):** `github_about_git_chunk_001` (0.5800)
**Improved (HW3):** `github_about_git_chunk_001` (0.9056)

### Запит 8: How to set up SSH keys for GitLab?

**Baseline (HW2):** `gitlab_getting_started_chunk_010` (0.7400)
**Improved (HW3):** `gitlab_getting_started_chunk_010` (1.0000)

### Запит 9: What is rebasing and when should I use it?

**Baseline (HW2):** `git_tools_rebasing_chunk_001` (0.5400)
**Improved (HW3):** `git_tools_rebasing_chunk_001` (1.0000)

### Запит 10: How do I push changes to a remote repository?

**Baseline (HW2):** `github_about_git_chunk_010` (0.7100)
**Improved (HW3):** `github_about_git_chunk_010` (0.9038)


---

Повні результати тестування: запустіть `python3 scripts/retrieval_improved.py --test`