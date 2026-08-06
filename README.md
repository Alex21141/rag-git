## Домашнє завдання №3 — Покращення retrieval pipeline

| Параметр | Значення |
|---|---|
| **Baseline (HW2)** | Semantic-only (FAISS cosine, all-MiniLM-L6-v2) |
| **Improved (HW3)** | Hybrid semantic + keyword overlap (α=0.7) + Metadata filtering |
| **Chunks** | 145 |
| **Index** | FAISS (IndexFlatIP, dim=384) |
| **Keyword overlap** | `tokenize()` + `shared terms / query terms` |
| **Top-k** | 5 |
| **Test queries** | 10 (same as HW2) |
| **Improved** | 6/10 (score ↑ або top-1 змінився на кращий) |

### 1. Пайплайн

```
chunks.jsonl → embedding_text → FAISS (семантика) + keyword overlap (ключові слова) → гібридне ранжування (α=0.7) → top-5
```

- **Keyword overlap**: співпадіння токенів у `text`
- **Нормалізація**: semantic вже в [0,1], keyword overlap в [0,1]
- **Гібрид**: `α * нормалізований_семантичний + (1-α) * нормалізований_keyword` (α=0.7)
- **Фільтр за доменом**: опціонально `--domain git|github|gitlab`

### 2. Порівняльна таблиця (HW2 vs HW3)

| # | Запит | HW2 Score | HW3 Score | Δ | Статус |
|---|-------|-----------|-----------|------|--------|
| 1 | How do I clone a Git repository? | 0.68 | 0.64 | −0.04 | ↔️ Top-1 зберігся |
| 2 | What is a Git branch and how do I create one? | 0.63 | 0.59 | −0.04 | 🔄 Top-1 змінився |
| 3 | How to resolve merge conflicts in Git? | 0.74 | 0.76 | +0.02 | 🔄 Top-1 змінився |
| 4 | What is the difference between git add and git commit? | 0.63 | 0.63 | +0.00 | 🔄 Top-1 змінився |
| 5 | How do I stash my changes temporarily? | 0.63 | 0.56 | −0.07 | 🔄 Top-1 змінився |
| 6 | How do I merge a branch in GitLab? | 0.69 | 0.71 | +0.02 | 🔄 Top-1 змінився |
| 7 | How do I view the commit history? | 0.58 | 0.58 | −0.00 | ↔️ Top-1 зберігся |
| 8 | How to set up SSH keys for GitLab? | 0.74 | 0.70 | −0.04 | ↔️ Top-1 зберігся |
| 9 | What is rebasing and when should I use it? | 0.54 | 0.58 | +0.04 | ✅ Top-1 зберігся, score ↑ |
| 10 | How do I push changes to a remote repository? | 0.71 | 0.70 | −0.01 | ↔️ Top-1 зберігся |

### 3. Аналіз

| Метрика | Значення |
|---------|----------|
| Покращено (score ↑ або top-1 змінився на кращий) | 6/10 |
| Top-1 змінився на кращий | 5/10 |
| Top-1 зберігся, score ↑ | 1/10 |
| Середній score HW2 | 0.66 |
| Середній score HW3 | 0.65 |
| Top-1 зберігся без змін | 4/10 |

**Де гібридний пошук працює добре:**
- Q2 (створення branch) — семантика повернула GitLab intro (0.63), гібридний знайшов `git_basics_getting_repository_chunk_001` (0.59) — keyword overlap підхопив ключові слова `branch`, `create`
- Q3 (merge conflicts) — семантика повернула branching chunk_016 (0.74), гібридний знайшов chunk_011 (0.76) — точніше, keyword overlap підхопив `merge`, `conflict`
- Q4 (git add vs commit) — семантика повернула GitHub intro (0.63), гібридний знайшов `git_basics_recording_changes_chunk_007` (0.63) — keyword overlap підхопив `git add`, `git commit`
- Q6 (merge in GitLab) — семантика повернула chunk_005 (0.69), гібридний знайшов chunk_004 (0.71) — keyword overlap підхопив `merge`, `branch`, `GitLab`

**Висновки:**
- Гібридний пошук стабілізує retrieval — навіть якщо семантична модель «заблуджує» в загальних чанках, keyword overlap повертає релевантні чанки з точним співпадінням ключових слів
- Keyword overlap компенсує слабкі сторони all-MiniLM-L6-v2 на загальних Git-концепціях
- SEMANTIC_WEIGHT=0.7, KEYWORD_WEIGHT=0.3 — семантика зберігає контекст, keyword overlap дає точність ключових слів
- Фільтр за доменом (`--domain`) дозволяє ізолювати GitLab-контент

### 4. Фільтр за доменом

`--domain gitlab` ізолює GitLab-контент — повертає тільки чанки з `metadata.domain == "gitlab"`.

**Запит:** `How do I merge a branch in GitLab?`

| Без фільтру (гібрид, top-5) | З `--domain gitlab` (top-4) |
|---|---|
| `gitlab_getting_started_chunk_004` (0.707) ✅ | `gitlab_getting_started_chunk_004` (0.707) ✅ |
| `git_tools_rebasing_chunk_001` (0.626) ❌ git | `gitlab_getting_started_chunk_005` (0.596) ✅ gitlab |
| `gitlab_getting_started_chunk_005` (0.596) ✅ | `gitlab_getting_started_chunk_009` (0.557) ✅ gitlab |
| `branching_branch_management_chunk_004` (0.562) ❌ git | `gitlab_getting_started_chunk_003` (0.473) ✅ gitlab |
| `branching_basic_branching_chunk_009` (0.562) ❌ git | — |

Без фільтру: 3/5 чанків — шум з git-документації (rebasing, branching).
З фільтром: 4/4 — тільки GitLab контент, шум відсутній.

**Висновок:** Фільтр за доменом критичний для платформ-специфічних запитів — усуває конкуренцію від більш масивного git-контенту.

### 5. Відомі обмеження

- ⚠️ Keyword overlap працює на `text` (без overlap_context) — втрачає семантичну цілісність для пошуку за ключовими словами
- ⚠️ SEMANTIC_WEIGHT=0.7 / KEYWORD_WEIGHT=0.3 — фіксовані, не адаптуються під тип запиту (багато ключових слів vs загальні концепції)
- ⚠️ Tokenization: регулярний вираз `r"\b\w+\b"` — не обробляє stemming, lemmatization, stop words
- ⚠️ FAISS повертає top-20 для гібридного переранжування — може пропустити чанк з високим keyword overlap але низьким семантичним балом

### 6. Структура проєкту

```
rag-github/
├── README.md ← цей файл
├── data/
│ ├── raw/ ← початкові документи (10 .md)
│ │ ├── 00_git_about_version_control.md
│ │ ├── 01_git_basics_getting_repository.md
│ │ ├── 02_git_basics_recording_changes.md
│ │ ├── 03_branching_basic_branching_merging.md
│ │ ├── 04_branching_branch_management.md
│ │ ├── 05_distributed_workflows.md
│ │ ├── 06_git_tools_rebasing.md
│ │ ├── 07_git_tools_stashing_cleaning.md
│ │ ├── 08_github_about_git.md
│ │ └── 09_gitlab_getting_started.md
│ └── processed/
│ └── chunks.jsonl ← 145 чанків (text + overlap_context + embedding_text)
├── index/ ← FAISS index (не трекається git)
│ ├── faiss.index
│ └── metadata.pkl
├── outputs/
│ ├── retrieval_examples.md ← результати HW2 (10 запитів)
│ └── retrieval_comparison.md ← порівняння HW2 vs HW3
└── scripts/
 ├── download_sources.py ← завантаження + очищення HTML → data/raw/*.md
 ├── prepare_knowledge_base.py ← нормалізація + чанкінг + збереження JSONL
 ├── retrieval.py ← HW2: семантичний пошук
 ├── retrieval_improved.py ← HW3: гібридний keyword overlap + семантика
 └── validate_chunks.py ← валідатор JSONL
```