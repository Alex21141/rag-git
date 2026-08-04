# RAG Git/GitHub/GitLab Tutoring Assistant

Домашнє завдання №1 — Підготовка knowledge base

## 1. Тема проєкту

**Git/GitHub/GitLab tutoring assistant** — чат-бот для навчання основам Git, GitHub та GitLab. Цільова аудиторія — розробники, які починають працювати з системами керування версіями.

Тема охоплює:
- Базові команди Git (`init`, `clone`, `add`, `commit`, `push`, `pull`)
- Роботу з гілками (branching, merging, rebasing)
- Стешинг та очищення (stashing, cleaning)
- Розподілені workflow (distributed workflows)
- GitHub flow та командну роботу
- GitLab Flow та merge requests

## 2. Джерела

| # | Назва | URL | Тип |
|---|-------|-----|-----|
| 1 | Git Basics — Getting a Repository | https://git-scm.com/book/en/v2/Git-Basics-Getting-a-Git-Repository | концепт + команди |
| 2 | Git Basics — Recording Changes | https://git-scm.com/book/en/v2/Git-Basics-Recording-Changes-to-the-Repository | команди |
| 3 | Branching — Basic Branching and Merging | https://git-scm.com/book/en/v2/Git-Branching-Basic-Branching-and-Merging | концепт + workflow |
| 4 | Branching — Branch Management | https://git-scm.com/book/en/v2/Git-Branching-Branch-Management | довідник |
| 5 | Distributed Workflows | https://git-scm.com/book/en/v2/Distributed-Git-Distributed-Workflows | workflow/концепт |
| 6 | Git Tools — Rebasing | https://git-scm.com/book/en/v2/Git-Branching-Rebasing | концепт + процедура |
| 7 | Git Tools — Stashing and Cleaning | https://git-scm.com/book/en/v2/Git-Tools-Stashing-and-Cleaning | команди |
| 8 | GitHub — About Git (intro) | https://docs.github.com/en/get-started/using-git/about-git | концепт, доп. контекст |
| 9 | GitLab — Getting started with Git | https://docs.gitlab.com/topics/git/get_started/index.md | концепт |
| 10 | GitLab Merge Requests | https://docs.gitlab.com/ee/user/project/merge_requests/ | процедура |

## 3. Структура метаданих

Кожен чанк містить:

```json
{
  "chunk_id": "git_basics_getting_repository_chunk_000",
  "text": "текст чанку...",
  "metadata": {
    "document_id": "git_basics_getting_repository",
    "source_file": "data/raw/01_git_basics_getting_repository.md",
    "source_type": "markdown",
    "title": "Git Basics",
    "section": "# Git Basics — Getting a Git Repository",
    "chunk_index": 1,
    "language": "en",
    "domain": "git",
    "document_type": "concept"
  }
}
```

| Поле | Опис |
|------|------|
| `chunk_id` | Унікальний ідентифікатор чанку |
| `text` | Текст чанку |
| `document_id` | Ідентифікатор документу (без префікса номеру) |
| `source_file` | Шлях до raw файлу |
| `source_type` | Формат джерела (markdown) |
| `title` | Назва тематичної групи |
| `section` | Заголовок секції, з якої взятий чанк |
| `chunk_index` | Послідовний номер чанку в документі |
| `language` | Мова (en) |
| `domain` | Домен (git / github / gitlab) |
| `document_type` | Тип контенту (concept / commands / workflow / reference / procedure / procedural) |

## 4. Стратегія чанкінгу

- **chunk_size**: 700 символів
- **overlap**: 150 символів
- **метод**: contiguous sliding window з post-processing overlap injection
- **word-boundary cuts**: розриви на кордонах слів (не посеред слів)
- **sentence-aware**: пріоритет розриву на кордонах речень

## 5. Статистика

| Метрика | Значення |
|---------|----------|
| Документів | 10 |
| Чанків | 164 |
| Середня довжина | 823 chars |
| Мінімальна довжина | 283 chars |
| Максимальна довжина | 923 chars |
| Всього chars | 134,935 |
| Overlap coverage | 100% пар (154/154) |

**По доменах:**
| Домен | Чанків |
|-------|--------|
| git | 114 |
| gitlab | 36 |
| github | 14 |

## 6. Приклади чанків

### Приклад 1 — Git Basics (concept)

```json
{
  "chunk_id": "git_basics_getting_repository_chunk_000",
  "text": "# Git Basics — Getting a Git Repository\n\nIf you can read only one chapter to get going with Git, this is it. This chapter covers every basic command you need to do the vast majority of the things you'll eventually spend your time doing with Git.",
  "metadata": {
    "document_id": "git_basics_getting_repository",
    "source_file": "data/raw/01_git_basics_getting_repository.md",
    "source_type": "markdown",
    "title": "Git Basics",
    "section": "# Git Basics — Getting a Git Repository",
    "chunk_index": 1,
    "language": "en",
    "domain": "git",
    "document_type": "concept"
  }
}
```

### Приклад 2 — GitHub (concept)

```json
{
  "chunk_id": "github_about_git_chunk_000",
  "text": "# GitHub — About Git\n\nLearn about the version control system, Git, and how it works with GitHub.\n\n## About version control and Git\n\nA version control system, or VCS, tracks the history of changes as people and teams collaborate on projects together.",
  "metadata": {
    "document_id": "github_about_git",
    "source_file": "data/raw/08_github_about_git.md",
    "source_type": "markdown",
    "title": "GitHub",
    "section": "# GitHub — About Git",
    "chunk_index": 1,
    "language": "en",
    "domain": "github",
    "document_type": "concept"
  }
}
```

### Приклад 3 — GitLab (concept)

```json
{
  "chunk_id": "gitlab_getting_started_chunk_000",
  "text": "# Get started with Git\n\nGit is a version control system you use to track changes to your code and collaborate with others. GitLab is a web-based Git repository manager that provides CI/CD and other features to help you manage your software development lifecycle.\n\nYou can use the GitLab web interface for many Git operations, but understanding Git commands provides you with additional flexibility and control.",
  "metadata": {
    "document_id": "gitlab_getting_started",
    "source_file": "data/raw/09_gitlab_getting_started.md",
    "source_type": "markdown",
    "title": "GitLab",
    "section": "# Get started with Git",
    "chunk_index": 1,
    "language": "en",
    "domain": "gitlab",
    "document_type": "concept"
  }
}
```

## 7. Висновок

**Що вийшло добре:**
- ✅ 10 якісних джерел з трьох доменів (Git, GitHub, GitLab)
- ✅ Оригінальні заголовки документів збережено (без нумерації та дублів)
- ✅ Повна metadata структура — 10 полів, включаючи section, domain, document_type
- ✅ Contiguous sliding window chunking з overlap — 100% пар чанків мають перекриття (150 chars)
- ✅ Word-boundary розриви — чанки не обриваються посеред слів
- ✅ Sentence-aware break — пріоритет розриву на кордонах речень
- ✅ Очистка від посилань, жирного тексту, навігаційного сміття, prev|next, порожніх заголовків

**Що треба покращити:**
- ⚠️ Середня довжина (824 chars) — можна збільшити chunk_size до 850-900
- ⚠️ Немає семантичного чанкінгу — розбиття на основі змісту, а не фіксованих розмірів
- ⚠️ 09_gitlab_flow.md згенеровано вручну на основі about.gitlab.com — краще офіційна документація
- ⚠️ Немає валідації JSONL — бажано додати скрипт перевірки валідності кожного рядка

## 8. Структура проєкту

```
rag-github/
├── README.md                          ← цей файл
├── data/
│   ├── raw/                           ← початкові документи (10 .md)
│   │   ├── 01_git_basics_getting_repository.md
│   │   ├── 02_git_basics_recording_changes.md
│   │   ├── 03_branching_basic_branching_merging.md
│   │   ├── 04_branching_branch_management.md
│   │   ├── 05_distributed_workflows.md
│   │   ├── 06_git_tools_rebasing.md
│   │   ├── 07_git_tools_stashing_cleaning.md
│   │   ├── 08_github_about_git.md
│   │   └── 09_gitlab_getting_started.md
│   │   └── 10_gitlab_merge_requests.md
│   └── processed/                     ← оброблені дані
│       └── chunks.jsonl               ← 164 чанків
└── scripts/
    ├── download_sources.py            ← збір даних з веб-сторінок
    ├── download_sources.py            ← збір даних з веб-сторінок
    ├── prepare_knowledge_base.py      ← нормалізація + чанкінг
    ├── retrieval.py                   ← semantic retrieval
    └── rag_answer.py                  ← RAG QA pipeline (HW4)
```

---

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
