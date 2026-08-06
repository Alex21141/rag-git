# Git tutoring assistant

## Домашнє завдання №4 — RAG Answer Generation

| Параметр | Значення |
|---|---|
| **Embedding model** | all-MiniLM-L6-v2 (384d) |
| **Index** | FAISS IndexFlatIP (dim=384) |
| **Chunks** | 145 |
| **Top-k retrieval** | 5 chunks |
| **Relevance threshold** | 0.3 |
| **Generation** | Template-based (no LLM) |
| **Test queries** | 10 |
| **Grounded answers** | 8/10 (80%) |
| **Partial** | 2/10 (20%) |

### 1. Пайплайн

```
question → semantic retrieval (FAISS) → top-5 chunks → build prompt → generate answer with citations
```

- **Retrieval**: FAISS cosine similarity, top-5 chunks per query
- **Prompt building**: context = retrieved chunk texts, joined with newlines
- **Answer generation**: template-based (LLM unavailable → rule-based answers)
- **Citations**: each answer cites source chunk_id + source_file
- **Fallback**: if top-1 score < 0.3 → "I do not have enough information"

### 2. Результати запитів

| # | Запит | Top-1 score | Chunk | Результат |
|---|-------|-------------|-------|-----------|
| 1 | How do I clone a Git repository? | 0.68 | git_basics_getting_repository_chunk_006 | ✅ Grounded |
| 2 | What is a Git branch and how do I create one? | 0.63 | gitlab_getting_started_chunk_001 | ✅ Grounded |
| 3 | How to resolve merge conflicts in Git? | 0.74 | branching_basic_branching_merging_chunk_016 | ✅ Grounded |
| 4 | What is the difference between git add and git commit? | 0.63 | github_about_git_chunk_009 | ✅ Grounded |
| 5 | How do I stash my changes temporarily? | 0.63 | git_tools_stashing_cleaning_chunk_002 | ✅ Grounded |
| 6 | How do I merge a branch in GitLab? | 0.69 | gitlab_getting_started_chunk_005 | ✅ Grounded |
| 7 | How do I view the commit history? | 0.58 | github_about_git_chunk_001 | ⚠️ Partial |
| 8 | How to set up SSH keys for GitLab? | 0.74 | gitlab_getting_started_chunk_010 | ✅ Grounded |
| 9 | What is rebasing and when should I use it? | 0.54 | git_tools_rebasing_chunk_001 | ⚠️ Partial |
| 10 | How do I push changes to a remote repository? | 0.71 | github_about_git_chunk_010 | ✅ Grounded |

### 3. Аналіз

| Метрика | Значення |
|---------|----------|
| Grounded (повна відповідь) | 8/10 (80%) |
| Partial (часткова відповідь) | 2/10 (20%) |
| Not relevant | 0/10 (0%) |
| Середній top-1 score | 0.65 |
| Min score | 0.54 (Q9 — rebasing) |
| Max score | 0.74 (Q3 — merge conflicts, Q8 — SSH keys) |

**Де RAG працює добре:**
- Q3 (merge conflicts) — найвищий score (0.74), всі 3 чанки з branching розділу
- Q8 (SSH keys) — score 0.74, чанки з GitLab документації
- Q1, Q5, Q6, Q10 — релевантні чанки, відповіді ґрунтуються на контексті

**Де RAG працює погано:**
- Q7 (commit history) — top-1 повернув generic GitHub intro (0.58). Семантична модель не знайшла `git log` чанки. Відповідь про `git add/git commit` — не відповідає на запит
- Q9 (rebasing) — top-1 score лише 0.54. Чанки з rebasing розділу мають низьку семантичну схожість з query phrasing

### 4. Відомі обмеження

- ⚠️ Template-based generation — без LLM відповіді генеруються правилами, а не мовною моделлю
- ⚠️ Semantic retrieval bottleneck — низькі scores (Q7=0.58, Q9=0.54) призводять до не релевантних чанків
- ⚠️ No hybrid search — чистий semantic search (без BM25) дає гірші результати на generic запити
- ⚠️ No query expansion — запитується точний текст, без пародубу синонімів

### 5. Висновки

RAG pipeline працює для специфічних Git-запитів (clone, stash, merge conflicts, SSH keys, push), але має проблеми з generic концепціями (commit history, rebasing). Для покращення:
1. Hybrid search (BM25 + semantic) — як у HW3, дає кращі top-1 результати
2. Query expansion — додавати синоніми та альтернативні формулювання
3. LLM integration — реальна мовна модель даватиме кращі відповіді на partial context

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
│ ├── retrieval_examples.md ← результати HW2 (10 запитів)
│ ├── rag_answers_examples.md ← результати HW4 (10 запитів + відповіді)
│ └── alpha_sweep.md ← порівняння α (BM25 vs semantic ваги)
└── scripts/
 ├── download_sources.py ← завантаження + очищення HTML → data/raw/*.md
 ├── prepare_knowledge_base.py ← нормалізація + чанкінг + збереження JSONL
 ├── retrieval.py ← semantic retrieval (FAISS + MiniLM)
 ├── rag_answer.py ← HW4: RAG QA pipeline
 ├── alpha_sweep.py ← sweep α=0.0..1.0 для гібридного пошуку
 └── validate_chunks.py ← валідатор JSONL
```