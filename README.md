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
| 9 | GitLab Flow | https://about.gitlab.com/topics/version-control/what-is-gitlab-flow/ | концепт/workflow |
| 10 | GitLab Merge Requests | https://docs.gitlab.com/ee/user/project/merge_requests/ | процедура |

## 3. Структура метаданих

Кожен чанк містить:

```json
{
  "chunk_id": "git_basics_getting_repository_chunk_001",
  "text": "текст чанку...",
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

## 4. Стратегія чанкінгу

- **chunk_size**: 700 символів
- **overlap**: 150 символів
- **метод**: sliding window з post-processing overlap injection
- **word-boundary cuts**: розриви на кордонах слів (не посеред слів)
- **sentence-aware**: пріоритет розриву на кордонах речень

## 5. Статистика

| Метрика | Значення |
|---------|----------|
| Документів | 10 |
| Чанків | 165 |
| Середня довжина | 678 chars |
| Мінімальна довжина | 301 chars |
| Максимальна довжина | 840 chars |
| Всього chars | 111,839 |
| Overlap coverage | 94% пар |

**По доменах:**
| Домен | Чанків |
|-------|--------|
| git | 116 |
| gitlab | 35 |
| github | 14 |

## 6. Приклади чанків

### Приклад 1 — Git Basics (concept)

```json
{
  "chunk_id": "git_basics_getting_repository_chunk_001",
  "text": "текст про контроль версій і Git...",
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

### Приклад 2 — GitHub commands (concept)

```json
{
  "chunk_id": "github_about_git_chunk_005",
  "text": "текст про базові команди Git...",
  "metadata": {
    "document_id": "github_about_git",
    "source_file": "data/raw/08_github_about_git.md",
    "source_type": "markdown",
    "title": "GitHub",
    "section": "### Basic Git commands",
    "chunk_index": 5,
    "language": "en",
    "domain": "github",
    "document_type": "concept"
  }
}
```

### Приклад 3 — GitLab Flow (workflow)

```json
{
  "chunk_id": "gitlab_flow_chunk_003",
  "text": "текст про те, як працює GitLab Flow...",
  "metadata": {
    "document_id": "gitlab_flow",
    "source_file": "data/raw/09_gitlab_flow.md",
    "source_type": "markdown",
    "title": "GitLab Flow",
    "section": "## How does GitLab Flow work?",
    "chunk_index": 3,
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
- ✅ Sliding window чанкінг з overlap — 94% пар чанків мають перекриття
- ✅ Word-boundary розриви — чанки не обриваються посеред слів
- ✅ Sentence-aware break — пріоритет розриву на кордонах речень
- ✅ Очистка від посилань, жирного тексту, навігаційного сміття, prev|next
- ✅ Таблиці відокремлені порожніми рядками для коректного рендерингу

**Що треба покращити:**
- ⚠️ Середня довжина (678 chars) — можна збільшити chunk_size до 800+
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
│   │   ├── 09_gitlab_flow.md
│   │   └── 10_gitlab_merge_requests.md
│   └── processed/                     ← оброблені дані
│       └── chunks.jsonl               ← 165 чанків
└── scripts/
    ├── download_sources.py            ← збір даних з веб-сторінок
    └── prepare_knowledge_base.py      ← нормалізація + чанкінг
```