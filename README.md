# Git tutoring assistant

Домашнє завдання №1 — Підготовка knowledge base

## 1. Тема проєкту

**Git tutoring assistant** — чат-бот для навчання основам Git. Цільова аудиторія — розробники, які починають працювати з системами керування версіями.

Тема охоплює:
- Концепцію контролю версій (local, centralized, distributed VCS)
- Базові команди Git (`init`, `clone`, `add`, `commit`, `push`, `pull`)
- Роботу з гілками (branching, merging, rebasing)
- Стешинг та очищення (stashing, cleaning)
- Розподілені workflow (distributed workflows)
- GitHub (About Git)
- GitLab (Getting started with Git)

## 2. Джерела

| # | Назва | URL | Тип |
|---|-------|-----|-----|
| 0 | Getting Started — About Version Control | https://git-scm.com/book/en/v2/Getting-Started-About-Version-Control | концепт |
| 1 | Git Basics — Getting a Git Repository | https://git-scm.com/book/en/v2/Git-Basics-Getting-a-Git-Repository | концепт |
| 2 | Git Basics — Recording Changes to the Repository | https://git-scm.com/book/en/v2/Git-Basics-Recording-Changes-to-the-Repository | команди |
| 3 | Git Branching — Basic Branching and Merging | https://git-scm.com/book/en/v2/Git-Branching-Basic-Branching-and-Merging | концепт + workflow |
| 4 | Git Branching — Branch Management | https://git-scm.com/book/en/v2/Git-Branching-Branch-Management | довідник |
| 5 | Distributed Git — Distributed Workflows | https://git-scm.com/book/en/v2/Distributed-Git-Distributed-Workflows | концепт + workflow |
| 6 | Git Tools — Rebasing | https://git-scm.com/book/en/v2/Git-Branching-Rebasing | концепт + процедура |
| 7 | Git Tools — Stashing and Cleaning | https://git-scm.com/book/en/v2/Git-Tools-Stashing-and-Cleaning | команди |
| 8 | GitHub — About Git | https://docs.github.com/api/article/body?pathname=/en/get-started/using-git/about-git | концепт |
| 9 | GitLab — Getting started with Git | https://docs.gitlab.com/topics/git/get_started/index.md | концепт |

## 3. Структура метаданих

Кожен чанк містить:

```json
{
  "chunk_id": "git_basics_getting_repository_chunk_000",
  "text": "# 2.1 Git Basics - Getting a Git Repository\n\nIf you can read only one chapter to get going with Git, this is it. This chapter covers every basic command you need to do the vast majority of the things ...",
  "metadata": {
    "document_id": "git_basics_getting_repository",
    "source_file": "data/raw/01_git_basics_getting_repository.md",
    "source_type": "markdown",
    "title": "Git Basics",
    "section": "# 2.1 Git Basics - Getting a Git Repository",
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
| `document_type` | Тип контенту (concept / commands / workflow / reference / procedure) |

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
| Чанків | 144 |
| Середня довжина | 813 chars |
| Мінімальна довжина | 246 chars |
| Максимальна довжина | 921 chars |
| Всього chars | 117,117 |
| Overlap coverage | 100% пар (143/143) |

**По доменах:**
| Домен | Чанків |
|-------|--------|
| git | 120 |
| github | 14 |
| gitlab | 10 |

## 6. Аналіз перекриття даних

**Тематичне перекриття (ключові терміни):** Високе — базові команди `add`, `commit`, `push`, `checkout`, `branch`, `merge` зустрічаються в більшості документів. Це природно — кожен документ контекстуально пояснює базові операції Git у своєму аспекті.

**Дослівне перекриття (10-слівні shingles, Jaccard similarity):** Низьке — жодна пара документів не має Jaccard >2%. Це означає відсутність дослівних дублікатів тексту між документами.

**Висновок:** Документи мають високе тематичне перекриття (одні й тіж базові команди повторюються в різних контекстах), але низьке дослівне перекриття. Для RAG-системи це означає:
- ✅ Пошук по загальних термінах (clone, branch, merge) поверне релевантні чанки з багатьох документів — добре для всебічної відповіді
- ⚠️ Семантичний embedding може мати труднощі розрізнити контекст (напр. `branch` у branching vs `branch` у merge workflow)
- ⚠️ Для специфічних термінів (stash, rebase, conflict) пошук буде точнішим через менше перекриття

## 7. Приклади чанків

### Приклад — Getting Started (git)

```json
{
  "chunk_id": "git_about_version_control_chunk_000",
  "text": "# 1.1 Getting Started - About Version Control\n\nThis chapter will be about getting started with Git. We will begin by explaining some background on version control tools, then move on to how to get Git...",
  "metadata": {
    "document_id": "git_about_version_control",
    "source_file": "data/raw/00_git_about_version_control.md",
    "source_type": "markdown",
    "title": "Getting Started",
    "section": "# 1.1 Getting Started - About Version Control",
    "chunk_index": 1,
    "language": "en",
    "domain": "git",
    "document_type": "concept"
  }
}
```

### Приклад — Git Basics (git)

```json
{
  "chunk_id": "git_basics_getting_repository_chunk_000",
  "text": "# 2.1 Git Basics - Getting a Git Repository\n\nIf you can read only one chapter to get going with Git, this is it. This chapter covers every basic command you need to do the vast majority of the things ...",
  "metadata": {
    "document_id": "git_basics_getting_repository",
    "source_file": "data/raw/01_git_basics_getting_repository.md",
    "source_type": "markdown",
    "title": "Git Basics",
    "section": "# 2.1 Git Basics - Getting a Git Repository",
    "chunk_index": 1,
    "language": "en",
    "domain": "git",
    "document_type": "concept"
  }
}
```

### Приклад — GitHub (github)

```json
{
  "chunk_id": "github_about_git_chunk_000",
  "text": "# GitHub — About Git\n\n# About Git\n\nLearn about the version control system, Git, and how it works with GitHub.\n\n## About version control and Git\n\nA version control system, or VCS, tracks the history of...",
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

### Приклад — GitLab (gitlab)

```json
{
  "chunk_id": "gitlab_getting_started_chunk_000",
  "text": "# GitLab — Getting started with Git\n\n# Get started with Git\n\nGit is a version control system you use to track changes to your code and collaborate with others.\nGitLab is a web-based Git repository man...",
  "metadata": {
    "document_id": "gitlab_getting_started",
    "source_file": "data/raw/09_gitlab_getting_started.md",
    "source_type": "markdown",
    "title": "GitLab",
    "section": "# GitLab — Getting started with Git",
    "chunk_index": 1,
    "language": "en",
    "domain": "gitlab",
    "document_type": "concept"
  }
}
```

## 8. Висновок

**Що вийшло добре:**
- ✅ 10 якісних джерел з трьох доменів (Git, GitHub, GitLab)
- ✅ Нумеровані заголовки документів збережено (формат `# X.Y Title`)
- ✅ Повна metadata структура — 10 полів, включаючи section, domain, document_type
- ✅ Contiguous sliding window chunking з overlap — 100% пар чанків мають перекриття (150 chars)
- ✅ Word-boundary розриви — чанки не обриваються посеред слів
- ✅ Sentence-aware break — пріоритет розриву на кордонах речень
- ✅ Очистка від посилань, жирного тексту, figure captions, навігаційного сміття, prev|next
- ✅ Низьке дослівне перекриття між документами (Jaccard <2%)

**Що треба покращити:**
- ⚠️ Середня довжина (813 chars) — можна збільшити chunk_size до 850-900
- ⚠️ Немає семантичного чанкінгу — розбиття на основі змісту, а не фіксованих розмірів
- ⚠️ Високе тематичне перекриття базових команд (10 документів) — може ускладнювати точний пошук контексту
- ⚠️ Немає валідації JSONL — бажано додати скрипт перевірки валідності кожного рядка

## 9. Структура проєкту

```
rag-github/
├── README.md                          ← цей файл
├── data/
│   ├── raw/                           ← початкові документи (10 .md)
│   │   ├── 00_git_about_version_control.md
│   │   ├── 01_git_basics_getting_repository.md
│   │   ├── 02_git_basics_recording_changes.md
│   │   ├── 03_branching_basic_branching_merging.md
│   │   ├── 04_branching_branch_management.md
│   │   ├── 05_distributed_workflows.md
│   │   ├── 06_git_tools_rebasing.md
│   │   ├── 07_git_tools_stashing_cleaning.md
│   │   ├── 08_github_about_git.md
│   │   └── 09_gitlab_getting_started.md
│   └── processed/                     ← оброблені дані
│       └── chunks.jsonl               ← 144 чанків
└── scripts/
    ├── download_sources.py            ← збір даних з веб-сторінок + очистка
    └── prepare_knowledge_base.py      ← нормалізація + чанкінг
```
