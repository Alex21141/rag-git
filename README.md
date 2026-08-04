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
| 0 | Getting Started — About Version Control | https://git-scm.com/book/en/v2/Getting-Started-About-Version-Control | reference |
| 1 | Git Basics — Getting a Git Repository | https://git-scm.com/book/en/v2/Git-Basics-Getting-a-Git-Repository | reference |
| 2 | Git Basics — Recording Changes to the Repository | https://git-scm.com/book/en/v2/Git-Basics-Recording-Changes-to-the-Repository | reference |
| 3 | Git Branching — Basic Branching and Merging | https://git-scm.com/book/en/v2/Git-Branching-Basic-Branching-and-Merging | reference |
| 4 | Git Branching — Branch Management | https://git-scm.com/book/en/v2/Git-Branching-Branch-Management | reference |
| 5 | Distributed Git — Distributed Workflows | https://git-scm.com/book/en/v2/Distributed-Git-Distributed-Workflows | reference |
| 6 | Git Tools — Rebasing | https://git-scm.com/book/en/v2/Git-Branching-Rebasing | reference |
| 7 | Git Tools — Stashing and Cleaning | https://git-scm.com/book/en/v2/Git-Tools-Stashing-and-Cleaning | reference |
| 8 | GitHub — About Git | https://docs.github.com/api/article/body?pathname=/en/get-started/using-git/about-git | reference |
| 9 | GitLab — Getting started with Git | https://docs.gitlab.com/topics/git/get_started/index.md | reference |

## 3. Структура метаданих

Кожен чанк містить:

`branching_basic_branching_merging_chunk_001`:
```json
{
 "text": "- Basic Branching and Merging

## Basic Branching and Merging

Let’s go through a simple example of branching and merging with a workflow that you might use in the real world. You’ll follow these step...",
 "metadata": {
  "document_id": "branching_basic_branching_merging",
  "source_file": "data/raw/03_branching_basic_branching_merging.md",
  "section": "# Git Branching — Basic Branching and Merging",
  "chunk_index": 1,
  "domain": "git",
  "document_type": "workflow"
 }
}
```
`branching_branch_management_chunk_001`:
```json
{
 "text": "- Branch Management

## Branch Management

Now that you’ve created, merged, and deleted some branches, let’s look at some branch-management tools that will come in handy when you begin using branches ...",
 "metadata": {
  "document_id": "branching_branch_management",
  "source_file": "data/raw/04_branching_branch_management.md",
  "section": "# Git Branching — Branch Management",
  "chunk_index": 1,
  "domain": "git",
  "document_type": "reference"
 }
}
```
`distributed_workflows_chunk_001`:
```json
{
 "text": "# Distributed Git — Distributed Workflows

# 5.1 Distributed Git - Distributed Workflows

Now that you have a remote Git repository set up as a focal point for all the developers to share their code, ...",
 "metadata": {
  "document_id": "distributed_workflows",
  "source_file": "data/raw/05_distributed_workflows.md",
  "section": "# Distributed Git — Distributed Workflows",
  "chunk_index": 1,
  "domain": "git",
  "document_type": "workflow"
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

- **chunk_size**: 850 символів
- **overlap**: 150 символів
- **метод**: semantic chunking — спочатку розбивається по секціях (заголовки `#`), потім кожну секцію чанкується з overlap
- **word-boundary cuts**: розриви на кордонах слів (не посеред слів)
- **sentence-aware**: пріоритет розриву на кордонах речень

## 5. Статистика

| Метрика | Значення |
|---------|---------|
| Документів | 10 |
| Чанків | 157 |
| Текст всього | 114,980 chars |
| Середня довжина | 732 chars |
| Мінімальна довжина | 303 chars |
| Максимальна довжина | 1076 chars |

### За доменом

| Домен | Чанків |
|-------|--------|
| git | 125 |
| github | 16 |
| gitlab | 17 |

## 6. Приклади чанків


- `$branching_basic_branching_merging_chunk_001` (654 chars, domain=git, section=# Git Branching — Basic Branching and Merging)
- `$branching_branch_management_chunk_001` (867 chars, domain=git, section=# Git Branching — Branch Management)
- `$distributed_workflows_chunk_001` (670 chars, domain=git, section=# Distributed Git — Distributed Workflows)

## 7. Виправлення та покращення

- ✅ Overlap space fix — автоматичне додавання пробілу між overlap та контентом
- ✅ Small chunk merge — чанки <300 chars об'єднуються з наступним
- ✅ Chunk index renumbering — послідовна нумерація після merge
- ✅ Capitalize first letter — чанки починаються з великої літери
- ✅ `---|---` cleanup — видалення артефактів таблиць/блоків
- ✅ Caution|/Warning| cleanup — видалення маркерів блоків попереджень
- ✅ Sequential chunk_index — ренумерація після об'єднання чанків

**Що треба покращити:**
- ⚠️ Немає постаналізу — перевірки якості retrieval на реальних запитаннях
- ⚠️ Metadata `document_type` присвоюється за DOMAIN_MAP — не аналізується реальний контент

## 8. Структура проєкту

```
rag-github/
├── README.md ← цей файл
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
│ └── chunks.jsonl ← 157 чанків
└── scripts/
 ├── download_sources.py ← збір даних з веб-сторінок + очистка
 ├── prepare_knowledge_base.py ← нормалізація + semantic chunking + merge
 └── validate_chunks.py ← JSONL валідатор
```
