
## HW4: RAG Answer Generation — Grounded QA Pipeline

**Pipeline**: question → retrieval (semantic) → prompt → grounded answer → citation
**Prompt template**: Grounded answering rule + fallback + citation
**Language**: Українська
**Retrieval**: FAISS semantic search (top-3 chunks per question)

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

**Improvement 1: Grounded answering rule** — Додано явну інструкцію відповідати ТІЛЬКИ з context. Без цього модель вигадувала відповіді (галюцинації).

**Improvement 2: Citation requirement** — Додано вимогу цитувати chunk ID або source file. Без цього неможливо перевірити коректність.

**Improvement 3: Ukrainian language output** — Додано "Answer (in Ukrainian):" для генерації відповідей українською.

### Fallback behavior

Для запитів з низьким score (< 0.50) або недостатнім контекстом модель правильно повертає:
> "Не маю достатньої інформації в доступних документах, щоб відповісти на це запитання."

**Скрипт**: `scripts/rag_answer.py`
**Повні результати**: `outputs/rag_answers_examples.md`
