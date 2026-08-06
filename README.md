# Git tutoring assistant

## Домашнє завдання №1 — Підготовка knowledge base

| Параметр | Значення |
|---|---|
| **Джерела** | 10 документів (Git, GitHub, GitLab) |
| **Chunking** | Two-pass sentence-aware, chunk_size=660, overlap=150 |
| **Чанків** | 145 |
| **Текст всього** | 94,122 chars |
| **Overlap coverage** | 100% (135/135 пар) |
| **Partial words у text** | 0 |
| **Домен** | git (121), github (14), gitlab (10) |

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

Кожен чанк у `chunks.jsonl` має поля:

`branching_basic_branching_merging_chunk_001` (658 chars, domain=git):
```json
{
 "chunk_id": "branching_basic_branching_merging_chunk_001",
 "text": "# 3.2 Git Branching - Basic Branching and Merging\nLet's go through a simple example of branching and merging...",
 "overlap_context": "",
 "embedding_text": "# 3.2 Git Branching - Basic Branching and Merging\nLet's go through...",
 "metadata": {
  "document_id": "branching_basic_branching_merging",
  "source_file": "data/raw/03_branching_basic_branching_merging.md",
  "title": "3.2 Git Branching - Basic Branching and Merging",
  "section": "3.2 Git Branching - Basic Branching and Merging",
  "chunk_index": 1,
  "language": "en",
  "domain": "git",
  "document_type": "reference",
  "overlap_len": 0
 }
}
```

| Поле | Опис |
|------|------|
| `chunk_id` | Унікальний ідентифікатор чанку |
| `text` | Чистий текст чанку (без overlap-префікса — повні слова) |
| `overlap_context` | Текст перекриття з попереднім чанком (для embedding) |
| `embedding_text` | `overlap_context + text` — повний текст для семантичного вбудовування |
| `metadata.document_id` | Ідентифікатор документу (без префікса номеру) |
| `metadata.source_file` | Шлях до raw файлу |
| `metadata.source_type` | Формат джерела (markdown) |
| `metadata.title` | Назва документу |
| `metadata.section` | Заголовок секції |
| `metadata.chunk_index` | Послідовний номер чанку в документі |
| `metadata.language` | Мова (en) |
| `metadata.domain` | Домен (git / github / gitlab) |
| `metadata.document_type` | Тип контенту (reference) |
| `metadata.overlap_len` | Довжина overlap_context (150 для чанків з перекриттям) |

### 4. Стратегія чанкінгу

- **chunk_size**: 660 символів
- **overlap**: 150 символів (100% coverage між сусідніми чанками)
- **метод**: two-pass sentence-aware — спочатку знаходяться точки розриву (кордони речень/слів), потім екстрагуються чанки з overlap
- **sentence-aware**: пріоритет розриву на `.` `!` `?`
- **word-boundary**: розриви тільки на кордонах слів (`\s` `\t` `\n`) — ніяких обрізок
- **partial word protection**: якщо split point призводить до обрізаного слова на початку чанку, split point пропускається
- **text = raw content only**: чанки зберігаються без overlap-префікса — тільки чистий контент з повними словами
- **overlap_context**: окреме поле для семантичної continuity при embedding

### 5. Статистика

| Метрика | Значення |
|---------|---------|
| Документів | 10 |
| Чанків | 145 |
| Текст всього | 94,122 chars |
| Середня довжина | 649 chars |
| Мінімальна довжина | 300 chars |
| Максимальна довжина | 882 chars |
| Overlap chain | 135/135 (100%) |

### За доменом

| Домен | Чанків |
|-------|--------|
| git | 121 |
| github | 14 |
| gitlab | 10 |

### 6. Приклади чанків

**Перший чанк** (без overlap_context — початок документу):
`git_about_version_control_chunk_001` — 658 chars, domain=git, section=1.1 Getting Started - About Version Control

```json
{
 "chunk_id": "git_about_version_control_chunk_001",
 "text": "# 1.1 Getting Started - About Version Control\\n\\nThis chapter will be about getting started with Git...",
 "overlap_context": "",
 "embedding_text": "# 1.1 Getting Started - About Version Control\\n\\nThis chapter will be about getting started with Git...",
 "metadata": {
  "document_id": "git_about_version_control",
  "source_file": "data/raw/00_git_about_version_control.md",
  "section": "1.1 Getting Started - About Version Control",
  "chunk_index": 1,
  "domain": "git",
  "overlap_len": 0
 }
}
```

**Внутрішній чанк** (з overlap_context — 150 chars перекриття з попереднім):
`distributed_workflows_chunk_007` — 657 chars, domain=git, section=5.1 Distributed Git - Distributed Workflows

```json
{
 "chunk_id": "distributed_workflows_chunk_007",
 "text": "that repository and makes changes.\\n3. The contributor pushes to their own public copy.\\n4. The contributor sends the maintainer an email asking them to pull changes.\\n5. The maintainer adds the contributor's repository as a remote and merges locally.\\n6. The maintainer pushes merged changes to the main repository.\\nThis is a very common workflow with hub-based tools like GitHub or GitLab...",
 "overlap_context": "The process works as follows (see Integration-manager workflow):\\n1. The project maintainer pushes to their public repository.\\n2. A contributor clones ",
 "embedding_text": "The process works as follows (see Integration-manager workflow):\\n1. The project maintainer pushes to their public repository.\\n2. A contributor clones that repository and makes changes...\\n[657 chars text + 150 chars overlap]",
 "metadata": {
  "document_id": "distributed_workflows",
  "source_file": "data/raw/05_distributed_workflows.md",
  "section": "5.1 Distributed Git - Distributed Workflows",
  "chunk_index": 7,
  "domain": "git",
  "overlap_len": 150
 }
}
```

| Поле | Опис |
|------|------|
| `text` | Чистий контент — повні слова, без overlap-префікса |
| `overlap_context` | Текст перекриття з попереднім чанком (0 для першого чанка в документі, ~150 для решти) |
| `embedding_text` | `overlap_context + text` — для semantic continuity (якщо overlap_context розрізає code block, використовується тільки `text`) |

### 7. Стратегія обробки

- ✅ **Two-pass sentence-aware chunking** — Pass 1 знаходить split points на кордонах речень/слів, Pass 2 екстрагує чанки без overlap-префікса
- ✅ **Code block guard** — fenced code blocks (`...`) виявляються до split — split points всередині них пропускаються
- ✅ **0 partial words** — `text` починається з повних слів (не `ing`, `ogrammers`, `ributed`)
- ✅ **100% overlap chain** — `prev_chunk.text[-ol:] == curr_chunk.overlap_context` (135/135)
- ✅ **3-полю архітектура** — `text` (чистий контент) + `overlap_context` (перекриття) + `embedding_text` (semantic continuity)
- ✅ **0 split code blocks** — embedding_text не містить розрізаних code blocks (odd fences → overlap_context ігнорується для embedding)
- ✅ **section field** — кожен чанк має `section` у metadata

**Відомі обмеження:**
- ⚠️ 3 odd backticks у embedding_text (в overlap_context-зонах) — не впливають на retrieval
- ⚠️ `document_type` у метаданих — статичний (DOMAIN_MAP), не аналізується реальний контент

## Домашнє завдання №2 — Семантичний retrieval

| Параметр | Значення |
|---|---|
| **Model** | `sentence-transformers/all-MiniLM-L6-v2` |
| **Chunks** | 145 |
| **Index** | FAISS (IndexFlatIP, dim=384) |
| **Embedding source** | `embedding_text` (overlap_context + text) |
| **Top-k** | 5 |
| **Test queries** | 10 |
| **Top-1 accuracy** | 6/10 (60%) |

### 1. Pipeline

```
chunks.jsonl → embedding_text → all-MiniLM-L6-v2 → FAISS index → cosine search → top-5 chunks
```

- `embedding_text` = `overlap_context + text` — семантична continuity між сусідніми чанками
- FAISS `IndexFlatIP` — inner product (косинусна подібність для normalized vector)
- Query encode → search → sort by score → return top-k

### 2. Результати запитів

| # | Запит | Score | Chunk | Статус |
|---|-------|-------|-------|--------|
| 1 | How do I clone a Git repository? | 0.68 | git_basics_getting_repository_chunk_006 | ✅ Relevant |
| 2 | What is a Git branch and how do I create one? | 0.63 | gitlab_getting_started_chunk_001 | ❌ Not relevant |
| 3 | How to resolve merge conflicts in Git? | 0.74 | branching_basic_branching_merging_chunk_016 | ✅ Relevant |
| 4 | What is the difference between git add and git commit? | 0.63 | github_about_git_chunk_009 | ⚠️ Partially relevant |
| 5 | How do I stash my changes temporarily? | 0.63 | git_tools_stashing_cleaning_chunk_002 | ✅ Relevant |
| 6 | How do I merge a branch in GitLab? | 0.69 | gitlab_getting_started_chunk_005 | ✅ Relevant |
| 7 | How do I view the commit history? | 0.58 | github_about_git_chunk_001 | ⚠️ Partially relevant |
| 8 | How to set up SSH keys for GitLab? | 0.74 | gitlab_getting_started_chunk_010 | ✅ Relevant |
| 9 | What is rebasing and when should I use it? | 0.54 | git_tools_rebasing_chunk_001 | ⚠️ Partially relevant |
| 10 | How do I push changes to a remote repository? | 0.71 | github_about_git_chunk_010 | ✅ Relevant |

### 3. Аналіз

| Метрика | Значення |
|---------|----------|
| Relevant (top-1 correct) | 6/10 (60%) |
| Partially relevant | 3/10 (30%) |
| Not relevant | 1/10 (10%) |
| Середній top-1 score | 0.66 |
| Min top-1 score | 0.54 (Q9 — rebasing) |
| Max top-1 score | 0.74 (Q3 — merge conflicts, Q8 — SSH keys) |

**Де retrieval працює добре:**
- Специфічні Git-команди (clone, stash, push) — Top-1 індикатор влучає у відповідний розділ документації
- Merge conflicts — найвищий score (0.74), чанк містить пряме роз'яснення конфліктів
- GitLab workflow (SSH keys, branch merge) — контекст GitLab чітко відрізняється від Git-only контенту

**Де retrieval працює погано:**
- Q2 (branch creation) — Top-1 повертає GitLab intro (`gitlab_getting_started_chunk_001`) замість branch-specific контенту. Модель `all-MiniLM-L6-v2` не розрізняє generic Git концепції від branch-specific. Чанк з branch management знаходиться на 4-й позиції (score 0.59)
- Q7 (commit history) — Top-1 повертає GitHub intro (score 0.58). Низький score — семантична модель не розрізняє "view history" від generic Git концепцій
- Q9 (rebasing) — Top-1 влучає у `git_tools_rebasing_chunk_001`, але score 0.54 (borderline). Семантична відстань між query phrasing та chunk content велика

### 4. Відомі обмеження

- ⚠️ `all-MiniLM-L6-v2` — мультимодельний (384d), не specialize для Git/tech content. Larger models (nli-mpnet-base-v2, allroberta-base-v1) дають кращу retrieval quality
- ⚠️ Неточність на generic запити — "What is a Git branch", "How do I view commit history" повертають intro чанки замість специфічного контенту
- ⚠️ Domain dilution — GitHub/GitLab чанки розмивають семантичний простір Git-only концепцій
- ⚠️ BM25 не використовується — тільки semantic search. Hybrid (BM25 + semantic) покращує precision на keyword-heavy запити

### 5. Виводи

Семантичний retrieval працює для специфічних Git-запитів (clone, stash, push, merge conflicts, SSH keys), але має проблеми з:
1. Generic концепціями (branch, commit history, rebasing) — повертає intro/general чанки
2. Низькими scores для partial relevant — модель має труднощі з phrasing mismatch
3. Domain ambiguity — Git vs GitLab vs GitHub контекст не завжди розрізняється

Для HW3 планується: hybrid retrieval (BM25 + semantic) + re-ranking для покращення precision.

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
│ └── chunks.jsonl ← 145 чанків
├── index/ ← FAISS index (gitignored, rebuild with --rebuild)
│ ├── faiss.index
│ └── metadata.pkl
├── outputs/
│ └── retrieval_examples.md ← HW2 test results
└── scripts/
 ├── prepare_knowledge_base.py ← normalize + chunk + save
 ├── retrieval.py ← HW2: semantic retrieval (FAISS + MiniLM)
 └── validate_chunks.py ← JSONL validator
```