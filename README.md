# RAG Git/GitHub/GitLab Tutoring Assistant

Домашнє завдання №1 — Підготовка knowledge base

## 1. Subject area

**Git/GitHub/GitLab tutoring assistant** — чат-бот для навчання основам Git, GitHub та GitLab. Цільова аудиторія — розробники, які починають працювати з системах керування версіями.

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
| 1 | Git Basics — Getting a Repository | https://git-scm.com/book/en/v2/Git-Basics-Getting-a-Git-Repository | concept + commands |
| 2 | Git Basics — Recording Changes | https://git-scm.com/book/en/v2/Git-Basics-Recording-Changes-to-the-Repository | commands |
| 3 | Branching — Basic Branching and Merging | https://git-scm.com/book/en/v2/Git-Branching-Basic-Branching-and-Merging | concept + workflow |
| 4 | Branching — Branch Management | https://git-scm.com/book/en/v2/Git-Branching-Branch-Management | reference |
| 5 | Distributed Workflows | https://git-scm.com/book/en/v2/Distributed-Git-Distributed-Workflows | workflow/concept |
| 6 | Git Tools — Rebasing | https://git-scm.com/book/en/v2/Git-Branching-Rebasing | concept + procedure |
| 7 | Git Tools — Stashing and Cleaning | https://git-scm.com/book/en/v2/Git-Tools-Stashing-and-Cleaning | commands |
| 8 | GitHub — About Git (intro) | https://docs.github.com/en/get-started/using-git/about-git | concept, доп. контекст |
| 9 | GitLab Flow | https://about.gitlab.com/topics/version-control/what-is-gitlab-flow/ | concept/workflow |
| 10 | GitLab Merge Requests | https://docs.gitlab.com/ee/user/project/merge_requests/ | procedural |

## 3. Metadata structure

Кожен chunk містить:

```json
{
  "chunk_id": "git_basics_getting_repository_chunk_001",
  "text": "The text content of the chunk...",
  "metadata": {
    "document_id": "git_basics_getting_repository",
    "source_file": "data/raw/01_git_basics_getting_repository.md",
    "source_type": "markdown",
    "title": "Git Basics",
    "section": "## About version control",
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

## 4. Chunking strategy

- **chunk_size**: 800 символів
- **overlap**: 150 символів
- **метод**: секційний чанкінг — спочатку розбиття тексту на секції за заголовками `##`/`###`, потім розбиття кожної секції на чанки з overlap
- **paragraph-aware break**: при розбитті спробує знайти кордон абзацу (`\n\n`) у межах чанку

## 5. Статистика

| Метрика | Значення |
|---------|----------|
| Документів | 10 |
| Чанків | 248 |
| Середня довжина | 405 chars |
| Мінімальна довжина | 10 chars |
| Максимальна довжина | 800 chars |
| Всього chars | 100,319 |

**By domain:**
| Домен | Чанків |
|-------|--------|
| git | 160 |
| github | 41 |
| gitlab | 47 |

## 6. Приклади chunks

### Приклад 1 — Git Basics (concept)

```json
{
  "chunk_id": "git_basics_getting_repository_chunk_001",
  "text": "## About version control and Git\n\nA version control system, or VCS, tracks the history of changes as people and teams collaborate on projects together. As developers make changes to the project, any earlier version of the project can be recovered at any time.",
  "metadata": {
    "document_id": "git_basics_getting_repository",
    "source_file": "data/raw/01_git_basics_getting_repository.md",
    "source_type": "markdown",
    "title": "Git Basics",
    "section": "## About version control and Git",
    "chunk_index": 1,
    "language": "en",
    "domain": "git",
    "document_type": "concept"
  }
}
```

### Приклад 2 — GitHub commands (commands)

```json
{
  "chunk_id": "github_about_git_chunk_015",
  "text": "### Basic Git commands\n\nTo use Git, developers use specific commands to copy, create, change, and combine code. These commands can be executed directly from the command line or by using an application like GitHub Desktop. Here are some common commands for using Git:\n\n- `git init` initializes a brand new Git repository and begins tracking an existing directory. It adds a hidden subfolder within the existing directory that houses the internal data structure required for version control.",
  "metadata": {
    "document_id": "github_about_git",
    "source_file": "data/raw/08_github_about_git.md",
    "source_type": "markdown",
    "title": "GitHub",
    "section": "### Basic Git commands",
    "chunk_index": 15,
    "language": "en",
    "domain": "github",
    "document_type": "concept"
  }
}
```

### Приклад 3 — GitLab Flow (workflow)

```json
{
  "chunk_id": "gitlab_flow_chunk_005",
  "text": "## How does GitLab Flow work?\n\nWith GitFlow, developers create a `develop` branch and make that the default, while GitLab Flow works with the `main` branch right away. GitLab Flow incorporates a pre-production branch to make bug fixes before merging changes back to `main` before going to production. Teams can add as many pre-production branches as needed — for example, from `main` to test, from test to acceptance, and from acceptance to production.",
  "metadata": {
    "document_id": "gitlab_flow",
    "source_file": "data/raw/09_gitlab_flow.md",
    "source_type": "markdown",
    "title": "GitLab Flow",
    "section": "## How does GitLab Flow work?",
    "chunk_index": 5,
    "language": "en",
    "domain": "gitlab",
    "document_type": "workflow"
  }
}
```

## 7. Висновок

**Що вийшло добре:**
- ✅ 10 якісних джерел з трьох доменів (Git, GitHub, GitLab)
- ✅ Повна metadata структура — 10 полів, включаючи section, domain, document_type
- ✅ Секційний чанкінг — кожен чанк має контекст заголовка секції
- ✅ Параграф-aware break — чанки рідко обриваються посеред речення
- ✅ Очистка від посилань, жирного тексту, навігаційного сміття
- ✅ Таблиці відокремлені порожніми рядками для коректного рендерингу

**Що треба покращити:**
- ⚠️ Мінімум чанків має 10 chars — надто короткий для самостійного читання
- ⚠️ Середня довжина (405 chars) нижча за рекомендовані 500+ — можна збільшити chunk_size до 1000
- ⚠️ 09_gitlab_flow.md згенеровано вручну на основі about.gitlab.com — краще було б взяти офіційну документацію з docs.gitlab.com
- ⚠️ Не використовується семантичний чанкінг — розбиття на основі змісту, а не фіксованих розмірів
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
│   │   ├── 09_gitlab_flow.md
│   │   └── 10_gitlab_merge_requests.md
│   └── processed/                     ← оброблені дані
│       └── chunks.jsonl               ← 248 чанків
└── scripts/
    ├── download_sources.py            ← збір даних з веб-сторінок
    └── prepare_knowledge_base.py      ← нормалізація + чанкінг
```