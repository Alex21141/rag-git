# Git tutoring assistant

## Домашнє завдання №3 — Покращення retrieval pipeline

| Параметр | Значення |
|---|---|
| **Baseline (HW2)** | Semantic-only (FAISS cosine, all-MiniLM-L6-v2) |
| **Improved (HW3)** | Hybrid BM25 + Semantic (α=0.5) + Metadata filtering |
| **Chunks** | 145 |
| **Index** | FAISS (IndexFlatIP, dim=384) |
| **BM25** | rank-bm25 (BM25Okapi, tokenized text) |
| **Top-k** | 5 |
| **Test queries** | 10 (same as HW2) |
| **Improved** | 10/10 (100% — score ↑ або top-1 змінився на кращий) |

### 1. Пайплайн

```
chunks.jsonl → embedding_text → FAISS (семантика) + BM25 (ключові слова) → гібридне ранжування (α=0.5) → top-5
```

- **Семантичний пошук**: FAISS cosine similarity, top-20 кандидатів
- **BM25 пошук**: matching на токінізованому `text`
- **Нормалізація**: обидва score → [0, 1]
- **Гібрид**: `α * norm_semantic + (1-α) * norm_bm25` (α=0.5)
- **Фільтр за доменом**: опціонально `--domain git|github|gitlab`

### 2. Порівняльна таблиця (HW2 vs HW3)

| # | Запит | HW2 Score | HW3 Score | Δ | Статус |
|---|-------|-----------|-----------|------|--------|
| 1 | How do I clone a Git repository? | 0.68 | 0.94 | +0.26 | 🔄 Top-1 змінився |
| 2 | What is a Git branch and how do I create one? | 0.63 | 0.97 | +0.34 | 🔄 Top-1 змінився |
| 3 | How to resolve merge conflicts in Git? | 0.74 | 0.99 | +0.25 | 🔄 Top-1 змінився |
| 4 | What is the difference between git add and git commit? | 0.63 | 0.88 | +0.25 | 🔄 Top-1 змінився |
| 5 | How do I stash my changes temporarily? | 0.63 | 0.94 | +0.31 | 🔄 Top-1 змінився |
| 6 | How do I merge a branch in GitLab? | 0.69 | 1.00 | +0.31 | 🔄 Top-1 змінився |
| 7 | How do I view the commit history? | 0.58 | 0.91 | +0.33 | ✅ Top-1 зберігся |
| 8 | How to set up SSH keys for GitLab? | 0.74 | 1.00 | +0.26 | ✅ Top-1 зберігся |
| 9 | What is rebasing and when should I use it? | 0.54 | 1.00 | +0.46 | ✅ Top-1 зберігся |
| 10 | How do I push changes to a remote repository? | 0.71 | 0.90 | +0.19 | ✅ Top-1 зберігся |

### 3. Фільтр за доменом

`--domain gitlab` ізолює GitLab-контент — повертає тільки чанки з `metadata.domain == "gitlab"`.

**Запит:** `How do I merge a branch in GitLab?`

| Без фільтру (гібрид, top-5) | З `--domain gitlab` (top-4) |
|---|---|
| `gitlab_getting_started_chunk_004` (0.998) ✅ | `gitlab_getting_started_chunk_004` (0.998) ✅ |
| `git_tools_rebasing_chunk_001` (0.766) ❌ git | `gitlab_getting_started_chunk_005` (0.716) ✅ gitlab |
| `branching_branch_management_chunk_005` (0.758) ❌ git | `gitlab_getting_started_chunk_009` (0.675) ✅ gitlab |
| `gitlab_getting_started_chunk_005` (0.716) ✅ | `gitlab_getting_started_chunk_003` (0.620) ✅ gitlab |
| `branching_basic_branching_chunk_009` (0.712) ❌ git | — |

Без фільтру: 3/5 чанків — шум з git-документації (rebasing, branching).
З фільтром: 4/4 — тільки GitLab контент, шум відсутній.

**Висновок:** Фільтр за доменом критичний для платформ-специфічних запитів — усуває конкуренцію від більш масивного git-контенту.

### 4. Аналіз

| Метрика | Значення |
|---------|----------|
| Усі 10 запитів покращені | 10/10 (100%) |
| Top-1 змінився на кращий | 6/10 |
| Top-1 зберігся, score ↑ | 4/10 |
| Середній score HW2 | 0.66 |
| Середній score HW3 | 0.94 |
| Середнє покращення | +0.28 |

**Де гібридний пошук працює добре:**
- Q2 (створення branch) — семантика повернула GitLab intro (0.63), гібридний знайшов `branching_branch_management_chunk_001` (0.97) — BM25 підхопив ключові слова `branch`, `create`
- Q3 (merge conflicts) — семантика повернула branching chunk_016 (0.74), гібридний знайшов chunk_011 (0.99) — точніше, BM25 підхопив `merge`, `conflict`
- Q4 (git add vs commit) — семантика повернула GitHub intro (0.63), гібридний знайшов `git_basics_recording_changes_chunk_007` (0.88) — BM25 підхопив `git add`, `git commit`
- Q6 (merge in GitLab) — семантика повернула chunk_005 (0.69), гібридний знайшов chunk_004 (1.00) — BM25 підхопив `merge`, `branch`, `GitLab`

**Висновки:**
- Гібридний пошук стабілізує retrieval — навіть якщо семантична модель «заблуджує» в загальних чанках, BM25 повертає релевантні чанки з точним співпадінням ключових слів
- BM25 компенсує слабкі сторони all-MiniLM-L6-v2 на загальних Git-концепціях
- Alpha=0.5 — збалансований: семантика зберігає контекст, BM25 дає точність ключових слів
- Фільтр за доменом (`--domain`) дозволяє ізолювати GitLab-контент

### 5. Відомі обмеження

- ⚠️ BM25 працює на `text` (без overlap_context) — втрачає семантичну цілісність для пошуку за ключовими словами
- ⚠️ Alpha=0.5 — фіксований, не адаптується під тип запиту (багато ключових слів vs загальні концепції)
- ⚠️ BM25 токенизація: регулярний вираз `r"\b\w+\b"` — не обробляє stemming, lemmatization, stop words
- ⚠️ FAISS повертає top-20 для гібридного переранжування — може пропустити чанк з високим BM25 але низьким семантичним балом

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
 ├── retrieval_improved.py ← HW3: гібридний BM25 + семантика
 └── validate_chunks.py ← валідатор JSONL
```