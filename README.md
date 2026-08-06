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
- **Domain filter**: опціонально `--domain git|github|gitlab`

### 2. Порівняльна таблиця (HW2 vs HW3)

| # | Запит | HW2 Score | HW3 Score | Δ | Статус |
|---|-------|-----------|-----------|------|--------|
| 1 | How do I clone a Git repository? | 0.68 | 0.94 | +0.26 | 🔄 Top-1 змінився |
| 2 | What is a Git branch and how do I create one? | 0.63 | 0.95 | +0.32 | 🔄 Top-1 змінився |
| 3 | How to resolve merge conflicts in Git? | 0.74 | 0.99 | +0.25 | 🔄 Top-1 змінився |
| 4 | What is the difference between git add and git commit? | 0.63 | 0.93 | +0.30 | 🔄 Top-1 змінився |
| 5 | How do I stash my changes temporarily? | 0.63 | 0.97 | +0.34 | ✅ Top-1 зберігся |
| 6 | How do I merge a branch in GitLab? | 0.69 | 0.98 | +0.29 | 🔄 Top-1 змінився |
| 7 | How do I view the commit history? | 0.58 | 0.88 | +0.30 | 🔄 Top-1 змінився |
| 8 | How to set up SSH keys for GitLab? | 0.74 | 1.00 | +0.26 | ✅ Top-1 зберігся |
| 9 | What is rebasing and when should I use it? | 0.54 | 1.00 | +0.46 | ✅ Top-1 зберігся |
| 10 | How do I push changes to a remote repository? | 0.71 | 0.86 | +0.15 | 🔄 Top-1 змінився |

### 3. Аналіз

| Метрика | Значення |
|---------|----------|
| Усі 10 запитів покращені | 10/10 (100%) |
| Top-1 змінився на кращий | 7/10 |
| Top-1 зберігся, score ↑ | 3/10 |
| Середній score HW2 | 0.66 |
| Середній score HW3 | 0.95 |
| Середнє покращення | +0.29 |

**Де гібридний пошук працює добре:**
- Q2 (branch creation) — semantic повернув GitLab intro (0.63), гібридний знайшов `git_basics_getting_repository_chunk_001` (0.95) — BM25 підхопив ключові слова `branch`, `create`
- Q3 (merge conflicts) — semantic повернув branching chunk_016 (0.74), гібридний знайшов chunk_011 (0.99) — точніше, BM25 підхопив `merge`, `conflict`
- Q4 (git add vs commit) — semantic повернув GitHub intro (0.63), гібридний знайшов GitLab chunk (0.93) — BM25 підхопив `git add`, `git commit`
- Q7 (commit history) — semantic повернув GitHub intro (0.58), гібридний знайшов `git_tools_rebasing_chunk_016` (0.88) — BM25 підхопив `commit`, `history`

**Висновки:**
- Гібридний пошук стабілізує retrieval — навіть якщо semantic модель «заблуджує» в generic чанках, BM25 повертає релевантні чанки з точним keyword matching
- BM25 компенсує слабкі сторони all-MiniLM-L6-v2 на generic Git-концепціях
- Alpha=0.5 — збалансований: semantic зберігає контекст, BM25 дає keyword precision
- Domain filter (`--domain`) дозволяє ізолювати GitLab-only контент

### 4. Domain filter

`--domain gitlab` ізолює GitLab-контент — повертає тільки чанки з `metadata.domain == "gitlab"`.

**Запит:** `How do I merge a branch in GitLab?`

| Без фільтру (гібрид, top-5) | З `--domain gitlab` (top-5) |
|---|---|
| `gitlab_getting_started_chunk_004` (0.98) ✅ | `gitlab_getting_started_chunk_004` (0.98) ✅ |
| `git_tools_rebasing_chunk_001` (0.92) ❌ git | `gitlab_getting_started_chunk_005` (0.75) ✅ gitlab |
| `branching_basic_branching_chunk_009` (0.84) ❌ git | `gitlab_getting_started_chunk_003` (0.60) ✅ gitlab |
| `branching_basic_branching_chunk_001` (0.83) ❌ git | `gitlab_getting_started_chunk_009` (0.57) ✅ gitlab |
| `gitlab_getting_started_chunk_005` (0.75) ✅ | `gitlab_getting_started_chunk_001` (0.52) ✅ gitlab |

Без фільтру: 3/5 чанків — noise з git-документації (rebasing, branching).
З фільтром: 5/5 — тільки GitLab контент, 0 noise.

**Висновок:** Domain filter критичний для платформ-специфічних запитів — усуває competition від більш масивного git-контенту.

### 5. Відомі обмеження

- ⚠️ BM25 працює на `text` (без overlap_context) — втрачає семантичну continuity для keyword matching
- ⚠️ Alpha=0.5 — фіксований, не адаптується під тип запиту (keyword-heavy vs concept-heavy)
- ⚠️ BM25 tokenization: простий `.split()` — не обробляє stemming, lemmatization, stop words
- ⚠️ FAISS search returns top-20 for hybrid re-ranking — може пропустити чанк з високим BM25 але низьким semantic score

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