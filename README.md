# Git tutoring assistant

## Домашнє завдання №4 — Генерація відповіді поверх retrieval

| Параметр | Значення |
|---|---|
| **Embedding model** | all-MiniLM-L6-v2 (384d) |
| **Індекс** | FAISS IndexFlatIP (dim=384) |
| **Чанків** | 145 |
| **Top-k retrieval** | 5 чанків |
| **Поріг релевантності** | 0.3 |
| **LLM** | OpenRouter — `nvidia/nemotron-3-nano-30b-a3b:free` (reasoning) |
| **API ключ** | env var `OPENROUTER_API_KEY` (не в git) |
| **Тестові запити** | 10 |

### 1. Пайплайн

Реалізовано pipeline:

```
user question
→ retrieve top-k chunks
→ build prompt with context
→ call LLM
→ return grounded answer with source
```

- **Ретривал**: FAISS cosine similarity, top-5 чанків на запит
- **Побудова промпту**: контекст = текст отриманих чанків, з'єднаний розділювачами
- **Генерація відповіді**: OpenRouter Nemotron 3 Nano 30B (reasoning enabled)
- **Цитування**: кожна відповідь цитує chunk_id + source_file
- **Fallback**: якщо контекст не містить інформації → "I do not have enough information"

### 2. Шаблон запиту

Шаблон використовується у pipeline — містить роль, правило grounded answering, fallback та вимогу цитувати джерело:

```
You are a Git tutoring assistant. Your job is to answer questions about Git, GitHub, and GitLab.

IMPORTANT RULES:
1. Answer ONLY based on the provided context below.
2. If the context does not contain enough information to answer the question, say:
   "I do not have enough information in the available documents to answer this question."
3. Do NOT use any general knowledge outside the provided context.
4. Always cite the source chunk ID or source file used in your answer.

Context:
{context}

Question: {question}

Answer:
```

### 3. Покращення шаблону запиту

**Приклад 1: Додавання ролі та інструкцій**

#### Початковий промпт (v1)
```
Answer the question based on the context.

Context:
{context}

Question: {question}

Answer:
```

#### Оновлений промпт (v2)
```
You are a Git tutoring assistant. Your job is to answer questions about Git, GitHub, and GitLab.

IMPORTANT RULES:
1. Answer ONLY based on the provided context below.
2. If the context does not contain enough information to answer the question, say:
   "I do not have enough information in the available documents to answer this question."
3. Do NOT use any general knowledge outside the provided context.
4. Always cite the source chunk ID or source file used in your answer.

Context:
{context}

Question: {question}

Answer:
```

**Проблема**: Без ролі модель давала загальні відповіді з власних знань, а не з контексту.

**Результат**: Додавання ролі та інструкції значно зменшило галюцинації.

---

**Приклад 2: Додавання правила fallback**

#### Початковий промпт (v1)
```
Answer the question based on the context.

Context:
{context}

Question: {question}

Answer:
```

#### Оновлений промпт (v2)
```
You are a Git tutoring assistant. Your job is to answer questions about Git, GitHub, and GitLab.

IMPORTANT RULES:
1. Answer ONLY based on the provided context below.
2. If the context does not contain enough information to answer the question, say:
   "I do not have enough information in the available documents to answer this question."
3. Do NOT use any general knowledge outside the provided context.

Context:
{context}

Question: {question}

Answer:
```

**Проблема**: Для запиту "How do I view the commit history?" модель намагалася вгадати відповідь, бо тема погано покрита в базі. Це призводило до вигаданих відповідей.

**Результат**: Чітке правило fallback дозволяє моделі чесно визнати відсутність інформації.

---

**Приклад 3: Обов'язкове цитування джерел**

#### Початковий промпт (v1)
```
You are a Git tutoring assistant. Your job is to answer questions about Git, GitHub, and GitLab.

IMPORTANT RULES:
1. Answer ONLY based on the provided context below.
2. If the context does not contain enough information to answer the question, say:
   "I do not have enough information in the available documents to answer this question."
3. Do NOT use any general knowledge outside the provided context.

Context:
{context}

Question: {question}

Answer:
```

#### Оновлений промпт (v2)
```
You are a Git tutoring assistant. Your job is to answer questions about Git, GitHub, and GitLab.

IMPORTANT RULES:
1. Answer ONLY based on the provided context below.
2. If the context does not contain enough information to answer the question, say:
   "I do not have enough information in the available documents to answer this question."
3. Do NOT use any general knowledge outside the provided context.
4. Always cite the source chunk ID or source file used in your answer.

Context:
{context}

Question: {question}

Answer:
```

**Проблема**: Відповіді не містили посилань на джерела, що ускладнювало перевірку коректності.

**Результат**: Вимога цитувати chunk_id і source_file робить відповіді перевірними.

### 3.5. Тестові запити

Підготовлено 10 тестових запитів, що покривають 4 обовязкові категорії:

| Категорія | Запити | Опис |
|-----------|--------|------|
| **Просте питання** | Q1, Q3, Q4, Q6, Q8, Q9 | Відповідь точно є в контексті — retrieval повертає релевантний чанк |
| **Переформульоване питання** | Q5, Q10 | Формулювання відрізняється від тексту в KB, але семантично співпадає |
| **Context недостатній** | Q2 | Тема погано покрита в KB — модель чесно повертає fallback |
| **Слабкий chunk** | Q7 | Retrieval повертає чанк з низьким score (0.58) — context не дає відповіді |

### 4. Результати запитів

| # | Запит | Top-1 score | Chunk | Результат |
|---|-------|-------------|-------|-----------|
| 1 | How do I clone a Git repository? | 0.68 | git_basics_getting_repository_chunk_006 | ✅ Grounded |
| 2 | What is a Git branch and how do I create one? | 0.63 | gitlab_getting_started_chunk_001 | ❌ Fallback |
| 3 | How to resolve merge conflicts in Git? | 0.74 | branching_basic_branching_merging_chunk_016 | ✅ Grounded |
| 4 | What is the difference between git add and git commit? | 0.63 | github_about_git_chunk_009 | ✅ Grounded |
| 5 | How do I stash my changes temporarily? | 0.63 | git_tools_stashing_cleaning_chunk_002 | ✅ Grounded |
| 6 | How do I merge a branch in GitLab? | 0.69 | gitlab_getting_started_chunk_005 | ✅ Grounded |
| 7 | How do I view the commit history? | 0.58 | github_about_git_chunk_001 | ❌ Fallback |
| 8 | How to set up SSH keys for GitLab? | 0.74 | gitlab_getting_started_chunk_010 | ✅ Grounded |
| 9 | What is rebasing and when should I use it? | 0.54 | git_tools_rebasing_chunk_001 | ✅ Grounded |
| 10 | How do I push changes to a remote repository? | 0.71 | github_about_git_chunk_010 | ✅ Grounded |

### 5. Аналіз

| Метрика | Значення |
|---------|----------|
| Grounded (повна відповідь LLM) | 8/10 (80%) |
| Fallback (контекст недостатній) | 2/10 (20%) |
| Not relevant | 0/10 (0%) |
| Середній top-1 score | 0.65 |
| Min score | 0.54 (Q9 — rebasing) |
| Max score | 0.74 (Q3 — merge conflicts, Q8 — SSH keys) |

**Де RAG працює добре (8/10 Grounded):**
- Q3 (merge conflicts) — найвищий score (0.74), LLM дає детальну відповідь з кроками
- Q4 (git add vs commit) — чітке пояснення різниці
- Q5 (stash) — точна команда `git stash push`
- Q1 (clone) — Nano модель генерує відповідь, хоча score=0.68
- Q6 (GitLab merge) — Nano генерує детальну інструкцію (UI + CLI)
- Q8 (SSH keys) — Nano генерує повну інструкцію
- Q9 (rebasing) — LLM пояснює концепцію
- Q10 (push) — команди `git push` з поясненням

**Де RAG працює погано (fallback, 2/10):**
- Q2 (branch creation) — контекст не містить команди `git branch`/`git checkout -b`
- Q7 (commit history) — низький score (0.58), повернуто fallback

### 6. Відомі обмеження

- ⚠️ **Semantic retrieval bottleneck** — низькі scores (Q7=0.58, Q9=0.54) дають нерелевантні чанки
- ⚠️ **No hybrid search** — чистий semantic search (без BM25) гірший на generic запити
- ⚠️ **No query expansion** — запитується точний текст, без додавання синонімів
- ⚠️ **Free model limits** — `nvidia/nemotron-3-nano-30b-a3b:free` має rate-limit (20 RPM, 1000 RPD). Застосовано cooldown 20s та retry-логіку

### 7. Висновки

RAG pipeline з LLM (Nemotron 3 Nano 30B) успішно працює для 8/10 запитів. Модель дотримується інструкції "Answer ONLY based on context" і коректно повертає fallback коли контекст недостатній. Nano модель стабільніша за Ultra 550B — значно менше rate-limit помилок.

Для покращення:
1. **Hybrid search** (BM25 + semantic) — як у HW3, дає кращі top-1 результати
2. **Query expansion** — додавати синоніми та альтернативні формулювання
3. **Top-k = 10** — більше чанків у контексті може покрити прогалини

### 8. Структура проєкту

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