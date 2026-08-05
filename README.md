# Git tutoring assistant

## Домашнє завдання №4 — Генерація відповіді поверх retrieval

| Параметр | Значення |
|---|---|
| **Модель вбудувань** | sentence-transformers/all-MiniLM-L6-v2 |
| **Індекс** | FAISS IndexFlatIP (dim=384) |
| **Чанків у KB** | 149 |
| **Тестових запитів** | 10 |
| **Prompt template** | Grounded answering + fallback + citation |
| **Мова відповідей** | Англійська |

### 1. Опис завдання

Побудувати QA pipeline, у якому модель відповідає на основі знайденого context, а не з загальних знань.

Потік:
```
user question
→ retrieve top-k chunks
→ build prompt with context
→ call LLM / template
→ return grounded answer with source
```

**Мета** — grounded QA: модель відповідає тільки на основі retrieved context і чесно каже "не знаю", якщо context недостатній.

### 2. Prompt template

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

Question:
{question}

Answer:
```

### 3. QA Pipeline

Реалізовано в `scripts/rag_answer.py`:

1. **Load** — завантаження FAISS індексу + chunks + metadata
2. **Retrieve** — semantic search (top-k=3) для кожного запиту
3. **Build prompt** — ін'єкція контексту в prompt template
4. **Generate** — створення відповіді на основі контексту
5. **Citation** — додавання source chunk_id + source_file до відповіді

### 4. Результати тестування

**10 тестових запитів** (5 простих + 5 переформульованих + fallback):

| # | Запитання | Top-1 chunk | Score | Результат |
|---|-----------|-------------|-------|-----------|
| 1 | How do I clone a Git repository? | git_basics_getting_repository_chunk_007 | 0.68 | ✅ Grounded |
| 2 | What is a Git branch and how do I create one? | gitlab_getting_started_chunk_002 | 0.67 | ✅ Grounded |
| 3 | How to resolve merge conflicts in Git? | branching_basic_branching_merging_chunk_013 | 0.74 | ✅ Grounded |
| 4 | What is the difference between git add and git commit? | github_about_git_chunk_007 | 0.60 | ✅ Grounded |
| 5 | How do I stash my changes temporarily? | git_tools_stashing_cleaning_chunk_000 | 0.63 | ✅ Grounded |
| 6 | How do I merge a branch in GitLab? | gitlab_getting_started_chunk_004 | 0.75 | ✅ Grounded |
| 7 | How do I view the commit history? | github_about_git_chunk_000 | 0.61 | ✅ Grounded |
| 8 | How to set up SSH keys for GitLab? | gitlab_getting_started_chunk_009 | 0.74 | ✅ Grounded |
| 9 | What is rebasing and when should I use it? | git_tools_rebasing_chunk_009 | 0.56 | ✅ Grounded |
| 10 | How do I push changes to a remote repository? | distributed_workflows_chunk_005 | 0.74 | ✅ Grounded |

### 5. Fallback behavior

Для запитів з низьким score (< 0.50) або недостатнім контекстом модель повертає:
> "I do not have enough information in the available documents to answer this question."

### 6. Prompt improvements

**Improvement 1: Grounded answering rule**

*Проблема:* Перший prompt був занадто простий — модель вигадувала відповіді з загальних знань.

*Before:*
```
Answer the question using the context.
Context: {retrieved_context}
Question: {user_question}
```

*After:*
```
Answer ONLY based on the provided context below.
Do NOT use any general knowledge outside the provided context.
Context: {retrieved_context}
Question: {user_question}
```

*Результат:* Відповіді стали grounded, модель більше не додає зовнішню інформацію.

---

**Improvement 2: Citation requirement**

*Проблема:* Без вимоги цитувати джерело неможливо перевірити коректність відповіді.

*Before:* Жодної вимоги про джерела.

*After:*
```
Always cite the source chunk ID or source file used in your answer.
```

*Результат:* Кожна відповідь містить посилання на конкретний chunk та source file.

---

**Improvement 3: Fallback for insufficient context**

*Проблема:* Для запитів без релевантного контексту модель намагалась відповісти і помилялась.

*Before:* Фallback відсутній — модель завжди намагалась відповісти.

*After:*
```
If the context does not contain enough information to answer the question, say:
"I do not have enough information in the available documents to answer this question."
```

*Результат:* Модель чесно каже "не знаю" замість вигадування.

### 7. Структура проєкту

```
rag-github/
├── README.md ← цей файл
├── data/
│   ├── raw/ ← початкові документи (3 .md)
│   │   ├── 03_branching_basic_branching_merging.md
│   │   ├── 04_branching_branch_management.md
│   │   └── 05_distributed_workflows.md
│   └── processed/
│       └── chunks.jsonl ← 149 чанків
├── index/
│   ├── faiss.index ← FAISS IndexFlatIP (dim=384)
│   └── metadata.pkl ← серіалізовані метадані
├── outputs/
│   ├── retrieval_examples.md ← результати retrieval
│   └── rag_answers_examples.md ← RAG відповіді + цитати
└── scripts/
    ├── download_sources.py ← збір даних з веб
    ├── prepare_knowledge_base.py ← chunking + нормалізація
    ├── retrieval.py ← semantic retrieval (FAISS)
    ├── rag_answer.py ← RAG QA pipeline (prompt + LLM + citations)
    └── validate_chunks.py ← JSONL валідатор
```

**Повні результати**: `outputs/rag_answers_examples.md`