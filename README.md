## Домашнє завдання №2 — Семантичний retrieval

| Параметр | Значення |
|---|---|
| **Model** | `sentence-transformers/all-MiniLM-L6-v2` |
| **Chunks** | 145 |
| **Index** | FAISS (IndexFlatIP, dim=384) |
| **Embedding source** | `embedding_text` (overlap_context + text) |
| **Top-k** | 5 |
| **Test queries** | 10 |
| **Top-1 accuracy** | 6/10 (60%) |

### 1. Пайплайн

```
chunks.jsonl → embedding_text → all-MiniLM-L6-v2 → FAISS index → cosine search → top-5 чанків
```

- `embedding_text` = `overlap_context + text` — семантична цілісність між сусідніми чанками
- FAISS `IndexFlatIP` — внутрішнє добуток (косинусна подібність для нормалізованих векторів)
- Запит → кодування → пошук → сортування за score → повернення top-k

### 2. Результати запитів

| # | Запит | Score | Chunk | Статус |
|---|-------|-------|-------|--------|
| 1 | How do I clone a Git repository? | 0.68 | git_basics_getting_repository_chunk_006 | ✅ Relevant |
| 2 | What is a Git branch and how do I create one? | 0.63 | gitlab_getting_started_chunk_001 | ❌ Not relevant |
| 3 | How to resolve merge conflicts in Git? | 0.74 | branching_basic_branching_merging_chunk_016 | ✅ Relevant |
| 4 | What is the difference between git add and git commit? | 0.63 | github_about_git_chunk_009 | ⚠️ Partially relevant |
| 5 | How do I stash my changes temporarily? | 0.63 | git_tools_stashing_cleaning_chunk_002 | ✅ Relevant |
| 6 | How do I merge a branch in GitLab? | 0.69 | gitlab_getting_started_chunk_005 | ✅ Relevant |
| 7 | How do I view the commit history? | 0.58 | github_about_git_chunk_001 | ⚠️ Partially relevant |
| 8 | How to set up SSH keys for GitLab? | 0.74 | gitlab_getting_started_chunk_010 | ✅ Relevant |
| 9 | What is rebasing and when should I use it? | 0.54 | git_tools_rebasing_chunk_001 | ⚠️ Partially relevant |
| 10 | How do I push changes to a remote repository? | 0.71 | github_about_git_chunk_010 | ✅ Relevant |

### 3. Аналіз

| Метрика | Значення |
|---------|----------|
| Relevant (top-1 correct) | 6/10 (60%) |
| Partially relevant | 3/10 (30%) |
| Not relevant | 1/10 (10%) |
| Середній top-1 score | 0.66 |
| Min top-1 score | 0.54 (Q9 — rebasing) |
| Max top-1 score | 0.74 (Q3 — merge conflicts, Q8 — SSH keys) |

**Де retrieval працює добре:**
- Специфічні Git-команди (clone, stash, push) — Top-1 індикатор влучає у відповідний розділ документації
- Merge conflicts — найвищий score (0.74), чанк містить пряме роз'яснення конфліктів
- GitLab workflow (SSH keys, branch merge) — контекст GitLab чітко відрізняється від Git-only контенту

**Де retrieval працює погано:**
- Q2 (branch creation) — Top-1 повертає GitLab intro (`gitlab_getting_started_chunk_001`) замість branch-specific контенту. Модель `all-MiniLM-L6-v2` не розрізняє generic Git концепції від branch-specific. Чанк з branch management знаходиться на 4-й позиції (score 0.59)
- Q7 (commit history) — Top-1 повертає GitHub intro (score 0.58). Низький score — семантична модель не розрізняє "view history" від generic Git концепцій
- Q9 (rebasing) — Top-1 влучає у `git_tools_rebasing_chunk_001`, але score 0.54 (borderline). Семантична відстань між query phrasing та chunk content велика

### 4. Відомі обмеження

- ⚠️ `all-MiniLM-L6-v2` (384d) — не спеціалізована для tech content
- ⚠️ BM25 не використовується — тільки semantic search
- ⚠️ Domain filter відсутній — Git/GitHub/GitLab чанки змішані

### 5. Висновки

Семантичний retrieval працює для специфічних Git-запитів (clone, stash, push, merge conflicts, SSH keys), але має проблеми з generic концепціями (branch, commit history, rebasing).

### 6. Структура проєкту

```
rag-github/
├── README.md ← опис проєкту
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
│ └── processed/ ← оброблені дані
│ └── chunks.jsonl ← 145 чанків (text + overlap_context + embedding_text)
├── index/ ← FAISS index (не трекається git, rebuild через --rebuild)
│ ├── faiss.index
│ └── metadata.pkl
├── outputs/
│ └── retrieval_examples.md ← результати HW2 (10 запитів)
└── scripts/
 ├── download_sources.py ← завантаження + очищення HTML → data/raw/*.md
 ├── prepare_knowledge_base.py ← нормалізація + чанкінг + збереження JSONL
 ├── retrieval.py ← HW2: семантичний пошук (FAISS + MiniLM)
 └── validate_chunks.py ← валідатор JSONL
```