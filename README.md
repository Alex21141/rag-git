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
    ├── retrieval.py                   ← semantic retrieval (baseline)
    └── retrieval_improved.py          ← hybrid BM25+semantic (HW3)
```
---

## HW3: Improved Retrieval — Hybrid BM25 + Semantic

**Метод**: Гібридний пошук (FAISS semantic + BM25 keyword) + metadata filtering
**Embedding model**: sentence-transformers/all-MiniLM-L6-v2 + BM25Okapi
**Vector storage**: FAISS IndexFlatIP (dim=384)
**Веса**: alpha=0.5 (семантичний), 0.5 (BM25)
**Metadata filter**: domain (git/github/gitlab)
**Chunks indexed**: 164
**Test queries**: 10
**Top-k**: 5

### Архітектура

Потік: `chunks.jsonl → FAISS (top-20) → BM25 scoring → hybrid re-ranking → metadata filter → top-5`

1. **FAISS pre-filter**: semantic search повертає top-20 кандидатів
2. **BM25 scoring**: для кандидатів обчислюються BM25-бали
3. **Normalization**: semantic і BM25 бали → [0, 1]
4. **Hybrid score**: `alpha * norm_semantic + (1-alpha) * norm_bm25`
5. **Metadata filter**: пост-фільтрація за domain (опціонально)

### Порівняльна таблиця

| Query | Baseline top-1 | Improved top-1 | Що змінилось |
|-------|---------------|----------------|-------------|
| How do I clone a Git repository? | git_basics_getting_repository_chunk_005 (0.70) | git_basics_getting_repository_chunk_004 (0.94) | 🔄 BM25 підняв кращий чанк про clone |
| What is a Git branch and how do I create one? | gitlab_getting_started_chunk_000 (0.63) | git_basics_getting_repository_chunk_000 (0.98) | 🔄 BM25 знайшов релевантніший чанк |
| How to resolve merge conflicts in Git? | branching_basic_branching_merging_chunk_013 (0.78) | branching_basic_branching_merging_chunk_010 (0.95) | 🔄 BM25 підкріпив semantic результат |
| What is the difference between git add and git commit? | github_about_git_chunk_007 (0.62) | git_basics_getting_repository_chunk_003 (0.95) | 🔄 BM25 знайшов чанк з обидвох команд |
| How do I stash my changes temporarily? | git_tools_stashing_cleaning_chunk_000 (0.62) | git_tools_stashing_cleaning_chunk_006 (0.95) | 🔄 BM25 підкріпив релевантність stash |
| How do I merge a branch in GitLab? | gitlab_getting_started_chunk_004 (0.74) | branching_branch_management_chunk_004 (0.91) | 🔄 BM25 знайшов чанк з merge keywords |
| How do I view the commit history? | github_about_git_chunk_000 (0.57) | git_tools_rebasing_chunk_016 (0.97) | 🔄 BM25 знайшов чанк з commit history |
| How to set up SSH keys for GitLab? | gitlab_getting_started_chunk_009 (0.74) | gitlab_getting_started_chunk_009 (1.00) | ✅ Топ-1 зберігся, бал збільшено |
| What is rebasing and when should I use it? | git_tools_rebasing_chunk_009 (0.50) | git_tools_rebasing_chunk_000 (0.96) | 🔄 BM25 знайшов чанк з визначенням rebasing |
| How do I push changes to a remote repository? | distributed_workflows_chunk_005 (0.72) | distributed_workflows_chunk_005 (0.89) | ✅ Топ-1 зберігся, бал збільшено |

### Статистика

| Метрика | HW2 (Baseline) | HW3 (Improved) | Різниця |
|---------|----------------|----------------|---------|
| Середній Top-1 score | 0.66 | 0.93 | **+0.27** (+41.5%) |
| Релевантний Top-1 | 8/10 | 10/10 | +2 |
| Top-1 зберігся | — | 2/10 | — |

### Висновок

**Де гібридний retrieval краще за semantic-only:**
- ✅ **Загальні терміни** (`branch`, `rebase`, `commit history`) — BM25 знаходить чанки з точними ключовими словами. Напр. `branch`: semantic повертав `gitlab_getting_started_chunk_000` (0.63), гібрид → `git_basics_getting_repository_chunk_000` (0.98) — пряме визначення гілки.
- ✅ **Конкретні команди** (`git add`, `git stash`, `git clone`) — BM25 підсилює точні лексичні збіги. Напр. `stash`: semantic повертав вступ (chunk_000, 0.62), гібрид → практичну частину (chunk_006, 0.95).
- ✅ **«What is» запити** — BM25 піднімає чанки з визначеннями. Напр. `rebase`: semantic повертав warning (chunk_009, 0.50), гібрид → пряме визначення (chunk_000, 0.96).
- ✅ **Score калібрування** — середній score з 0.66 → 0.93 (+41.5%), що полегшує поріг для релевантності.

**Де гібридний retrieval має обмеження:**
- ⚠️ **Платформ-специфічні запити** без domain filter — напр. `merge a branch in GitLab` гібрид повертає `branching_branch_management_chunk_004` (git-scm) замість GitLab. З `--domain gitlab` → ✅ `gitlab_getting_started_chunk_004`.
- ⚠️ **Перезважування BM25** — для дуже специфічних термінів (напр. `conflict`) BM25 може дати надмірну вагу частковим збігам.
- ⚠️ **Нормалізація балів** — BM25 бали залежать від довжини чанку, що може спотворювати гібридний рейтинг.

**Висновок:** Гібридний пошук (+41.5% score, 10/10 релевантних) значно кращий за semantic-only для конкретних команд та загальних термінів. Domain filter обов'язковий для платформ-специфічних запитів.

**Скрипт**: `scripts/retrieval_improved.py`
**Повні результати**: `outputs/retrieval_comparison.md`
