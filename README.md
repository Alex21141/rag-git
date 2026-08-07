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

Шаблон використовується у pipeline — містить роль, правило grounded answering, fallback та вимогу цитувати джерело.

**Початковий промпт (v1)** — простий шаблон без ролі, fallback та цитування:

```
Answer the question based on the context.

Context:
{context}

Question: {question}

Answer:
```

**Оновлений промпт (v2 / PROMPT_TEMPLATE)** — з усіма необхідними правилами:

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

*Запит*: `How do I clone a Git repository?`

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

#### Відповідь v1
> To clone a Git repository you run the `git clone` command, giving it the URL of the remote repository you want to copy. For example: `git clone https://github.com/user/project.git`

#### Відповідь v2
> To clone a repository you run the `git clone` command with the repository's URL. This creates a new directory, initializes a `.git` directory inside it... _Source: git_basics_getting_repository_chunk_006, 01_git_basics_getting_repository.md_

**Проблема**: V1 давав правильну відповідь, але без цитування джерела і без обмеження на власні знання. Модель могла генерувати відповідь без перевірки фактів.

**Результат**: V2 додає цитування джерела (`chunk_id + file`) і чітко обмежує модель контекстом.

---

**Приклад 2: Додавання правила fallback**

*Запит*: `How do I view the commit history?`

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

#### Відповідь v1 (галюцинація!)
> You can see the full commit history of a Git repository by running the `git log` command. `git log` shows the complete log with full commit hashes, authors, dates, and messages...

#### Відповідь v2 (чесний fallback)
> I do not have enough information in the available documents to answer this question.

**Проблема**: V1 вигадав відповідь (`git log`), хоча контекст не містив інформації про історію комітів. Це галюцинація — модель використала власні знання замість контексту.

**Результат**: V2 з чітким fallback-правилом чесно визнає відсутність інформації замість того, щоб вгадувати.

---

**Приклад 3: Обов'язкове цитування джерел**

*Запит*: `What is the difference between git add and git commit?`

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

#### Відповідь v1 (без цитування)
> `git add` and `git commit` serve different roles in the Git workflow: `git add` stages the changes you want to include, `git commit` saves the staged changes to the repository...

#### Відповідь v2 (з цитуванням)
> **Difference between `git add` and `git commit`**: `git add` — adds (stages) the changes to the index. `git commit` — saves the staged changes to the repository... _Source: github_about_git_chunk_009, 08_github_about_git.md_

**Проблема**: V1 давав правильну відповідь, але без посилань на джерело — неможливо перевірити, звідки взята інформація.

**Результат**: V2 вимагає цитувати `chunk_id` і `source_file`, що робить кожну відповідь перевірною.

### 3.5. Тестові запити

Підготовлено 10 тестових запитів, що покривають 4 обовязкові категорії:

| Категорія | Запити | Опис |
|-----------|--------|------|
| **Просте питання** | Q1, Q2, Q3, Q4, Q6, Q8, Q9 | Відповідь точно є в контексті — retrieval повертає релевантний чанк |
| **Переформульоване питання** | Q5, Q10 | Формулювання відрізняється від тексту в KB, але семантично співпадає |
| **Context недостатній** | Q7 | Тема погано покрита в KB — модель чесно повертає fallback |
| **Слабкий chunk** | Q7 | Retrieval повертає чанк з низьким score (0.58) — context не дає відповіді |

### 4. Результати запитів

| # | Запит | Top-1 score | Chunk | Результат |
|---|-------|-------------|-------|-----------|
| 1 | How do I clone a Git repository? | 0.68 | git_basics_getting_repository_chunk_006 | ✅ Grounded |
| 2 | What is a Git branch and how do I create one? | 0.63 | branching_branch_management_chunk_001 | ✅ Grounded |
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
| Grounded (повна відповідь LLM) | 9/10 (90%) |
| Fallback (контекст недостатній) | 1/10 (10%) |
| Not relevant | 0/10 (0%) |
| Середній top-1 score | 0.65 |
| Min score | 0.54 (Q9 — rebasing) |
| Max score | 0.74 (Q3 — merge conflicts, Q8 — SSH keys) |

**Де RAG працює добре (9/10 Grounded):**
- Q1 (clone) — Nano модель генерує відповідь з командами `git clone`
- Q2 (branch creation) — retrieval знайшов релевантний чанк, LLM дав чітку відповідь
- Q3 (merge conflicts) — найвищий score (0.74), LLM дає детальну відповідь з кроками
- Q4 (git add vs commit) — чітке пояснення різниці
- Q5 (stash) — точна команда `git stash push`
- Q6 (GitLab merge) — Nano генерує детальну інструкцію (UI + CLI)
- Q8 (SSH keys) — Nano генерує повну інструкцію
- Q9 (rebasing) — LLM пояснює концепцію
- Q10 (push) — команди `git push` з поясненням

**Де RAG працює погано (fallback, 1/10):**
- Q7 (commit history) — низький score (0.58), retrieval не знайшов релевантний чанк, повернуто fallback

### 6. Відомі обмеження

- ⚠️ **Semantic retrieval bottleneck** — низькі scores (Q7=0.58, Q9=0.54) дають нерелевантні чанки
- ⚠️ **No hybrid search** — чистий semantic search (без BM25) гірший на generic запити
- ⚠️ **No query expansion** — запитується точний текст, без додавання синонімів
- ⚠️ **Free model limits** — `nvidia/nemotron-3-nano-30b-a3b:free` має rate-limit (20 RPM, 1000 RPD). Застосовано cooldown 20s та retry-логіку

### 7. Висновки

RAG pipeline з реального LLM (Nemotron 3 Nano 30B через OpenRouter) успішно працює для 9/10 запитів. Модель дотримується інструкції "Answer ONLY based on context" і коректно повертає fallback коли контекст недостатній. Всі відповіді генеровані через реального LLM — **не через template**. Nano модель стабільніша за Ultra 550B — значно менше rate-limit помилок.

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