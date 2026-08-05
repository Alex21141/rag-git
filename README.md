# Git tutoring assistant

## Домашнє завдання №4 — RAG-бот з заземленими відповідями

| Параметр | Значення |
|---|---|
| **Pipeline** | question → retrieval (semantic) → prompt → grounded answer → citation |
| **Prompt template** | Grounded answering rule + fallback + citation |
| **Language** | Українська |
| **Retrieval** | FAISS semantic search (top-3 chunks per question) |

### Архітектура

Потік: `запит → FAISS retrieval → prompt template → answer generation → source citation`

1. **Retrieval**: Semantic search (sentence-transformers/all-MiniLM-L6-v2) через FAISS
2. **Context injection**: Top-3 чанки об'єднуються в context блок
3. **Prompt template**: Grounded answering rules + fallback + citation requirement
4. **Answer generation**: Відповідь на основі контексту з цитуванням джерел
5. **Fallback**: Якщо score < 0.50 або контекст недостатній → fallback повідомлення

### Результати тестування

### Prompt Template

```
You are a Git tutoring assistant. Your job is to answer questions about Git, GitHub, and GitLab.

IMPORTANT RULES:
1. Answer ONLY based on the provided context below.
2. If the context does not contain enough information to answer the question, say:
   "Не маю достатньої інформації в доступних документах, щоб відповісти на це запитання."
3. Do NOT use any general knowledge outside the provided context.
4. Always cite the source chunk ID or source file used in your answer.

Context:
{context}

Question:
{question}

Answer (in Ukrainian):
```

### Prompt Improvements

**Improvement 1: Grounded answering rule**

*Проблема:* Перший prompt був занадто простий — модель вигадувала відповіді з загальних знань.
*Before:* `Answer the question using the context.`
*After:* `Answer ONLY based on the provided context below. Do NOT use any general knowledge outside the provided context.`
*Результат:* Відповіді стали grounded, модель більше не додає зовнішню інформацію.

**Improvement 2: Citation requirement**

*Проблема:* Без вимоги цитувати джерело неможливо перевірити коректність відповіді.
*Before:* Жодної вимоги про джерела.
*After:* `Always cite the source chunk ID or source file used in your answer.`
*Результат:* Кожна відповідь містить посилання на конкретний chunk та source file.

**Improvement 3: Fallback for insufficient context**

*Проблема:* Для запитів без релевантного контексту модель намагалась відповісти і помилялась.
*Before:* Фallback відсутній — модель завжди намагалась відповісти.
*After:* `If the context does not contain enough information to answer the question, say: "Не маю достатньої інформації в доступних документах, щоб відповісти на це запитання."`
*Результат:* Модель чесно каже "не знаю" замість вигадування.

**Improvement 4: Ukrainian language output**

*Проблема:* Модель генерувала відповіді англійською (мова контексту).
*Before:* `Answer:`
*After:* `Answer (in Ukrainian):`
*Результат:* Відповіді українською, що відповідає цільовій аудиторії.

### Fallback behavior

Для запитів з низьким score (< 0.50) або недостатнім контекстом модель правильно повертає:
> "Не маю достатньої інформації в доступних документах, щоб відповісти на це запитання."

**Скрипт**: `scripts/rag_answer.py`
**Повні результати**: `outputs/rag_answers_examples.md`
