# Git tutoring assistant

## Домашнє завдання №1 — Підготовка knowledge base

| Параметр | Значення |
|---|---|
| **Джерела** | 10 документів (Git, GitHub, GitLab) |
| **Chunking** | Sliding window, chunk_size=850, overlap=150 |
| **Чанків** | 149 |
| **Текст всього** | 117,889 chars |
| **Overlap coverage** | 99.3% (138/139 пар) |
| **Odd backticks** | 0/149 |
| **Домен** | git (125), github (14), gitlab (10) |

### 1. Тема проєкту

**Git tutoring assistant** — чат-бот для навчання основам Git. Цільова аудиторія — розробники, які починають працювати з системами керування версіями.

Тема охоплює:
- Концепцію контролю версій (local, centralized, distributed VCS)
- Базові команди Git (`init`, `clone`, `add`, `commit`, `push`, `pull`)
- Роботу з гілками (branching, merging, rebasing)
- Стешинг та очищення (stashing, cleaning)
- Розподілені workflow (distributed workflows)
- GitHub (About Git)
- GitLab (Getting started with Git)

### 2. Джерела

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

### 3. Структура метаданих

Кожен чанк містить:

`branching_basic_branching_merging_chunk_001`:
```json
{
 "text": "# 3.2 Git Branching - Basic Branching and Merging\\n\\nLet's go through a simple example of branching and merging with a workflow that you might use in the real world. You'll follow these steps:\\n\\n  1. Do some work on a website.\\n\\n  2. Create a branch for a new user story you're working on.\\n\\n  3. Do some ...",
 "metadata": {
  "document_id": "branching_basic_branching_merging",
  "source_file": "data/raw/03_branching_basic_branching_merging.md",
  "section": "# 3.2 Git Branching - Basic Branching and Merging",
  "chunk_index": 1,
  "domain": "git",
  "document_type": "workflow"
 }
}
```
`branching_branch_management_chunk_001`:
```json
{
 "text": "# 3.3 Git Branching - Branch Management\\n\\nNow that you've created, merged, and deleted some branches, let's look at some branch-management tools that will come in handy when you begin using branches all the time.\\n\\nThe `git branch` command does more than just create and delete branches. If you run it ...",
 "metadata": {
  "document_id": "branching_branch_management",
  "source_file": "data/raw/04_branching_branch_management.md",
  "section": "# 3.3 Git Branching - Branch Management",
  "chunk_index": 1,
  "domain": "git",
  "document_type": "reference"
 }
}
```
`distributed_workflows_chunk_001`:
```json
{
 "text": "# 5.1 Distributed Git - Distributed Workflows\\n\\nNow that you have a remote Git repository set up as a focal point for all the developers to share their code, and you're familiar with basic Git commands in a local workflow, you'll look at how to utilize some of the distributed workflows that Git affor...",
 "metadata": {
  "document_id": "distributed_workflows",
  "source_file": "data/raw/05_distributed_workflows.md",
  "section": "# 5.1 Distributed Git - Distributed Workflows",
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

### 4. Стратегія чанкінгу

- **chunk_size**: 850 символів
- **overlap**: 150 символів (99.3% coverage між сусідніми чанками)
- **метод**: sliding window — кожне наступне вікно зсувається на `chunk_size - overlap` символів назад. Розриви на кордонах речень/слів.
- **word-boundary cuts**: розриви на кордонах слів (не посеред слів)
- **sentence-aware**: пріоритет розриву на кордонах речень (`.` `!` `?`)
- **backtick fix**: якщо чанк має непарну кількість inline backticks, шукати закриваючий backtick у наступних 200 символах
- **partial word fix**: якщо чанк починається з фрагмента слова (напр. `D continue`), фрагмент видаляється, перша літера капіталізується

### 5. Статистика

| Метрика | Значення |
|---------|---------|
| Документів | 10 |
| Чанків | 149 |
| Текст всього | 117,533 chars |
| Середня довжина | 790 chars |
| Мінімальна довжина | 392 chars |
| Максимальна довжина | 875 chars |

### За доменом

| Домен | Чанків |
|-------|--------|
| git | 125 |
| github | 14 |
| gitlab | 10 |

### 6. Приклади чанків

- `branching_basic_branching_merging_chunk_001` (791 chars, domain=git, section=# 3.2 Git Branching - Basic Branching and Merging)
- `branching_branch_management_chunk_001` (771 chars, domain=git, section=# 3.3 Git Branching - Branch Management)
- `distributed_workflows_chunk_001` (847 chars, domain=git, section=# 5.1 Distributed Git - Distributed Workflows)

### 7. Виправлення та покращення

- ✅ Overlap 100% — переписано chunking на sliding window з гарантованим перекриттям 150 символів між усіма сусідніми чанками
- ✅ Zero overlap fix — прибрано 3-фазний pipeline, який руйнував overlap на section boundaries
- ✅ Infinite loop fix — guard `new_start <= start` запобігає зворотньому руху вікна
- ✅ Unclosed backticks — автоматичне розширення чанку для включення backtick (backward + forward search)
- ✅ Small chunk merge — чанки <300 chars об'єднуються з наступним
- ✅ Chunk index renumbering — послідовна нумерація після merge
- ✅ Capitalize first letter — чанки починаються з великої літери
- ✅ Partial words fix — 51 фрагментів слів виправлено (напр. `D continue` → `Continue working`, `''S history` → `History`, `Ed from` → `From`, `Er\nBecause` → `Because`)
- ✅ `---|---` cleanup — видалення артефактів таблиць/блоків
- ✅ Caution|/Warning| cleanup — видалення маркерів блоків попереджень

**Відомі обмеження:**
- ⚠️ Overlap 99.3% — 1 пара чанків без повного перекриття (138/139) — через cross-section transition
- ⚠️ `document_type` у метаданих — статичний (DOMAIN_MAP), не аналізується реальний контент

### 8. Структура проєкту

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
│ └── chunks.jsonl ← 149 чанків
└── scripts/
 ├── download_sources.py ← збір даних з веб-сторінок + очистка
 ├── prepare_knowledge_base.py ← нормалізація + semantic chunking + merge
 └── validate_chunks.py ← JSONL валідатор
```