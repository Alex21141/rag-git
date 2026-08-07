# Git tutoring assistant

## Домашнє завдання №4 — Генерація відповіді поверх retrieval

| Параметр | Значення |
|---|---|
| **Embedding model** | all-MiniLM-L6-v2 (384d) |
| **Index** | FAISS IndexFlatIP (dim=384) |
| **Chunks** | 145 |
| **Top-k retrieval** | 5 chunks |
| **Relevance threshold** | 0.3 |
| **LLM** | OpenRouter — `nvidia/nemotron-3-ultra-550b-a55b:free` (reasoning) |
| **API key** | env var `OPENROUTER_API_KEY` (не в git) |
| **Test queries** | 10 |

### 1. Пайплайн

```
question → semantic retrieval (FAISS) → top-5 chunks → build prompt → LLM answer with citations
```

- **Retrieval**: FAISS cosine similarity, top-5 chunks per query
- **Prompt building**: context = retrieved chunk texts, joined with separators
- **Answer generation**: OpenRouter Nemotron 3 Ultra 550B (reasoning enabled)
- **Citations**: each answer cites source chunk_id + source_file
- **Fallback**: if context lacks info → "I do not have enough information"

### 2. Результати запитів

| # | Запит | Top-1 score | Chunk | Результат |
|---|-------|-------------|-------|-----------|
| 1 | How do I clone a Git repository? | 0.68 | git_basics_getting_repository_chunk_006 | ✅ Grounded |
| 2 | What is a Git branch and how do I create one? | 0.63 | gitlab_getting_started_chunk_001 | ✅ Fallback |
| 3 | How to resolve merge conflicts in Git? | 0.74 | branching_basic_branching_merging_chunk_016 | ✅ Grounded |
| 4 | What is the difference between git add and git commit? | 0.63 | github_about_git_chunk_009 | ✅ Grounded |
| 5 | How do I stash my changes temporarily? | 0.63 | git_tools_stashing_cleaning_chunk_002 | ✅ Grounded |
| 6 | How do I merge a branch in GitLab? | 0.69 | gitlab_getting_started_chunk_005 | ✅ Fallback |
| 7 | How do I view the commit history? | 0.58 | github_about_git_chunk_001 | ✅ Fallback |
| 8 | How to set up SSH keys for GitLab? | 0.74 | gitlab_getting_started_chunk_010 | ✅ Grounded |
| 9 | What is rebasing and when should I use it? | 0.54 | git_tools_rebasing_chunk_001 | ✅ Grounded |
| 10 | How do I push changes to a remote repository? | 0.71 | github_about_git_chunk_010 | ✅ Grounded |

### 3. Аналіз

| Метрика | Значення |
|---------|----------|
| Grounded (повна відповідь LLM) | 7/10 (70%) |
| Fallback (контекст недостатній) | 3/10 (30%) |
| Not relevant | 0/10 (0%) |
| Середній top-1 score | 0.65 |
| Min score | 0.54 (Q9 — rebasing) |
| Max score | 0.74 (Q3 — merge conflicts, Q8 — SSH keys) |

**Де RAG працює добре:**
- Q3 (merge conflicts) — найвищий score (0.74), LLM дає детальну відповідь з кроками
- Q4 (git add vs commit) — чітке пояснення різниці
- Q5 (stash) — точна команда `git stash push`
- Q8 (SSH keys) — покрокова інструкція
- Q9 (rebasing) — LLM пояснює концепцію
- Q10 (push) — команди `git push` з поясненням

**Де RAG працює погано (fallback):**
- Q2 (branch creation) — контекст не містить команди `git branch`/`git checkout -b`
- Q6 (GitLab merge) — контекст не містить інструкцію Merge Request
- Q7 (commit history) — контекст повернув generic GitHub intro, без `git log`

### 4. Відомі обмеження

- ⚠️ Semantic retrieval bottleneck — низькі scores (Q7=0.58, Q9=0.54) дають нерелевантні чанки
- ⚠️ No hybrid search — чистий semantic search (без BM25) гірший на generic запити
- ⚠️ No query expansion — запитується точний текст, без додавання синонімів
- ⚠️ Free model limits — `nvidia/nemotron-3-ultra-550b-a55b:free` може повертати порожню відповідь (rate limit)

### 5. Висновки

RAG pipeline з LLM (Nemotron 3 Ultra) працює для специфічних Git-запитів. Модель дотримується інструкції "Answer ONLY based on context" і коректно повертає fallback коли контекст недостатній.

Для покращення:
1. **Hybrid search** (BM25 + semantic) — як у HW3, дає кращі top-1 результати
2. **Query expansion** — додавати синоніми та альтернативні формулювання
3. **Top-k = 10** — більше чанків у контексті може покрити прогалини

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
│ └── rag_answers_examples.md ← результати HW4 (10 запитів + LLM відповіді)
└── scripts/
 ├── download_sources.py ← завантаження + очищення HTML → data/raw/*.md
 ├── prepare_knowledge_base.py ← нормалізація + чанкінг + збереження JSONL
 ├── retrieval.py ← semantic retrieval (FAISS + MiniLM)
 ├── rag_answer.py ← HW4: RAG QA pipeline (LLM via OpenRouter)
 └── validate_chunks.py ← валідатор JSONL
```