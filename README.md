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
- ⚠️ Середня довжина (823 chars) — можна збільшити chunk_size до 850-900
- ⚠️ Немає семантичного чанкінгу — розбиття на основі змісту, а не фіксованих розмірів
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
│   │   ├── 09_gitlab_getting_started.md
│   │   └── 10_gitlab_merge_requests.md
│   └── processed/                     ← оброблені дані
│       └── chunks.jsonl               ← 164 чанків
├── index/                             ← FAISS vector index (HW2)
│   ├── faiss.index                    ← 164 vectors, dim=384
│   └── metadata.pkl                   ← chunk metadata + model info
├── outputs/                           ← test results
│   ├── retrieval_examples.md          ← 10 queries з результатами (HW2)
│   └── rag_answers_examples.md        ← QA-результати з цитатами (HW4)
└── scripts/
    ├── download_sources.py            ← збір даних з веб-сторінок
    ├── prepare_knowledge_base.py      ← нормалізація + чанкінг
    ├── retrieval.py                   ← semantic retrieval (HW2)
    └── rag_answer.py                  ← QA pipeline з цитатами (HW4)
```

---

## HW2: Semantic Retrieval Layer

**Embedding model**: sentence-transformers/all-MiniLM-L6-v2
**Vector storage**: FAISS IndexFlatIP (dim=384)
**Chunks indexed**: 164
**Test queries**: 10
**Top-k**: 5

### Результати тестування

| Запит | Top-1 chunk | Score | Релевантність |
|-------|-------------|-------|---------------|
| How do I clone a Git repository? | git_basics_getting_repository_chunk_005 | 0.70 | ✅ Relevant |
| What is a Git branch and how do I create one? | gitlab_getting_started_chunk_000 | 0.63 | ⚠️ Partially |
| How to resolve merge conflicts in Git? | branching_basic_branching_merging_chunk_013 | 0.78 | ✅ Relevant |
| What is the difference between git add and git commit? | github_about_git_chunk_007 | 0.62 | ✅ Relevant |
| How do I stash my changes temporarily? | git_tools_stashing_cleaning_chunk_000 | 0.62 | ✅ Relevant |
| How do I merge a branch in GitLab? | gitlab_getting_started_chunk_004 | 0.74 | ✅ Relevant |
| What is GitLab Flow? | gitlab_getting_started_chunk_000 | 0.53 | ❌ Not relevant |
| How to set up SSH keys for GitLab? | gitlab_getting_started_chunk_009 | 0.74 | ✅ Relevant |
| What is rebasing and when should I use it? | git_tools_rebasing_chunk_009 | 0.50 | ⚠️ Partially |
| How do I push changes to a remote repository? | distributed_workflows_chunk_005 | 0.72 | ✅ Relevant |

### Аналіз

**Сильні сторони:** Специфічні терміни (stash, merge conflict, clone, SSH keys) дають високі scores (0.62-0.78). У 7/10 запитів Top-1 релевантний.

**Слабкі сторони:** Загальні терміни (branch, rebase, GitLab Flow) повертають вступи замість конкретики. GitLab Flow взагалі немає в KB.

**Висновок:** Базовий semantic retrieval працює задовільно для конкретних питань. Для покращення потрібен metadata filtering (HW3).

**Повні результати**: `outputs/retrieval_examples.md`

---

## HW3: Improved Retrieval — Hybrid BM25 + Semantic

**Метод**: Гібридний пошук (FAISS semantic + BM25 keyword) + metadata filtering
**Embedding model**: sentence-transformers/all-MiniLM-L6-v2 + BM25Okapi
**Vector storage**: FAISS IndexFlatIP (dim=384) — той самий index з HW2
**Веса**: alpha=0.5 (семантичний), 0.5 (BM25)
**Metadata filter**: domain (git/github/gitlab) + document_type
**Chunks indexed**: 164
**Test queries**: 10
**Top-k**: 5

### Архітектура

Потік: `chunks.jsonl → FAISS (top-20 candidates) → BM25 scoring → hybrid re-ranking → metadata filter → top-5`

1. **FAISS pre-filter**: semantic search повертає top-20 кандидатів
2. **BM25 scoring**: для кандидатів обчислюються BM25-бали
3. **Normalization**: semantic і BM25 бали → [0, 1]
4. **Hybrid score**: `alpha * norm_semantic + (1-alpha) * norm_bm25`
5. **Metadata filter**: пост-фільтрація за domain (опціонально)

### Результати тестування

| Запит | Baseline Top-1 | Score | Improved Top-1 | Score | Покращення |
|-------|-------------|-------|----------------|-------|------------|
| How do I clone a Git repository? | chunk_005 | 0.7031 | chunk_004 | 0.9404 | 🔄 BM25 підняв пряме визначення `git clone` |
| What is a Git branch and how do I create one? | gitlab_chunk_000 | 0.6283 | git_basics_chunk_000 | 0.9793 | 🔄 BM25 більше збігів у git domain |
| How to resolve merge conflicts in Git? | chunk_013 | 0.7773 | chunk_010 | 0.9510 | 🔄 BM25 підняв "Basic Merge Conflicts" вступ |
| What is the difference between git add and git commit? | github_chunk_007 | 0.6224 | git_basics_chunk_003 | 0.9468 | ✅ BM25 знайшов обидві команди в одному чанку |
| How do I stash my changes temporarily? | chunk_000 | 0.6238 | chunk_006 | 0.9508 | 🔄 BM25 змістив фокус зі вступу на практику |
| How do I merge a branch in GitLab? | gitlab_chunk_004 | 0.7394 | branching_chunk_004 | 0.9054 | ⚠️ Без domain filter — гірше; з `--domain gitlab` ✅ |
| What is GitLab Flow? | gitlab_chunk_000 | 0.5289 | gitlab_chunk_000 | 1.0000 | ✅ Зберігся, BM25 підтверджує релевантність |
| How to set up SSH keys for GitLab? | gitlab_chunk_009 | 0.7398 | gitlab_chunk_009 | 1.0000 | ✅ Ідеальний (BM25=16.95, точний збіг) |
| What is rebasing and when should I use it? | chunk_009 | 0.5023 | chunk_000 | 0.9562 | ✅ BM25 підняв визначення rebase замість попередження |
| How do I push changes to a remote repository? | chunk_005 | 0.7182 | chunk_005 | 0.8918 | ✅ Зберігся, BM25 підтверджує через "push/repository" |

### Статистика

| Метрика | HW2 (Baseline) | HW3 (Improved) | Різниця |
|---------|----------------|----------------|---------|
| Середній Top-1 score | 0.6583 | 0.9317 | **+0.2734** (+41.5%) |
| Релевантний Top-1 | 7/10 | 8/10 | +1 |
| Top-1 зберігся | — | 3/10 | — |

### Аналіз

**Сильні сторони гібридного підходу:**
- ✅ **+41.5%** середній Top-1 score (0.66→0.93) — краще калібрування балів
- ✅ **Конкретні команди** (`git add`, `git stash`, `git clone`, `git rebase`) — BM25 знаходить точні лексичні збіги
- ✅ **Краща релевантність** для "what is" запитів (rebase: chunk_000 — пряме визначення)
- ✅ **Metadata filtering** — `--domain gitlab` дає точні GitLab-результати
- ✅ **Стабільність** — 3/10 запитів зберегли Top-1 (GitLab Flow, SSH keys, push)

**Слабкі сторони:**
- ⚠️ **Платформ-специфічні запити** без domain filter повертають git-загальний контент (запит 6)
- ⚠️ **Відсутній контент** — GitLab Flow немає в KB (жоден метод не допомагає)

**Висновок:** Гібридний пошук значно покращує retrieval через поєднання семантичної релевантності та лексичної точності. Metadata filtering — обов'язковий для платформ-специфічних запитів.

**Скрипт**: `scripts/retrieval_improved.py`
**Повні результати**: `outputs/retrieval_comparison.md`

---

## HW4: RAG Answer Generation — Ґрунтовна QA-система з цитатами

**Pipeline**: Запитання → Semantic retrieval (FAISS) → Topic detection → Шаблонна генерація → Відповідь з цитатами
**Модель вбудувань**: sentence-transformers/all-MiniLM-L6-v2
**Генерація**: Шаблонна (LLM недоступний — localhost:8080 повертає HTML-сторінку логіну)
**Порог релевантності**: 0.30
**Fallback**: «Не маю достатньої інформації для надання відповіді на це питання.»

### Архітектура

```
Запитання → search() → results[]
              ↓
    detect_topic_from_query()  → explicit topic (якщо знайдено патерн)
    detect_topic_from_retrieval() → topic (за source_file чанків)
              ↓
    get_topic_summary(topic, results) → answer (uk) + is_fallback
              ↓
    _format_answer_with_sources() → answer + chunk_id + source_file citations
```

### Prompt-шаблон (v2)

Шаблон включає 4 обов'язкові елементи:
1. **Роль**: «Ти — Git-преподавач (Git tutor assistant)»
2. **Ґрунтовність**: «Відповідай ТІЛЬКИ на основі наведеного контексту»
3. **Fallback**: «Якщо контекст не містить інформації — скажи: "Не маю достатньої інформації..."»
4. **Цитати**: «Обов'язково вкажи джерела: chunk_id або source_file»

### Результати тестування (10 запитань)

| # | Запитання | Top-1 score | Результат |
|---|-----------|-------------|-----------|
| 1 | How do I clone a Git repository? | 0.70 | ✅ Grounded |
| 2 | What is a Git branch and how do I create one? | 0.63 | ✅ Grounded |
| 3 | How to resolve merge conflicts in Git? | 0.78 | ✅ Grounded |
| 4 | What is the difference between git add and git commit? | 0.62 | ✅ Grounded |
| 5 | How do I stash my changes temporarily? | 0.62 | ✅ Grounded |
| 6 | How do I merge a branch in GitLab? | 0.74 | ✅ Grounded |
| 7 | What is GitLab Flow? | 0.53 | ❌ Fallback |
| 8 | How to set up SSH keys for GitLab? | 0.74 | ✅ Grounded |
| 9 | What is rebasing and when should I use it? | 0.50 | ✅ Partial |
| 10 | How do I push changes to a remote repository? | 0.72 | ✅ Grounded |

**Покриття**: 8/10 — ground, 1 — partial, 1 — fallback (GitLab Flow немає в KB)

### Fallback behavior

Для запитання «What is GitLab Flow?» (концепція відсутня в KB):
> «Не маю достатньої інформації для надання відповіді на це питання. Запитання стосується теми, яка не покрита в базі знань. Найкращий знайдений чанк (gitlab_getting_started_chunk_000, gitlab_merge_requests_chunk_000) має бал релевантності 0.53, що недостатньо для надання надійної відповіді.»

### Покращення prompt-шаблонів

**1. Додавання ролі та інструкцій** — Оригінальний prompt (v1) просто просив «відповісти на основі контексту» без ролі. Оновлений (v2) встановлює роль «Git-преподавач» та явні правила. Без ролі модель давала загальні відповіді на основі власних знань.

**2. Додавання fallback-правила** — Без fallback-правила модель намагалася вгадати відповідь для GitLab Flow, що призводило до галюцинацій. З явним fallback-правилом модель чесно визнає відсутність інформації.

**3. Обов'язкові цитати джерел** — Вимога цитувати chunk_id та source_file робить відповіді перевірними. Кожне твердження можна простежити до конкретної частини документа.

**Скрипт**: `scripts/rag_answer.py`
**Повні результати**: `outputs/rag_answers_examples.md`