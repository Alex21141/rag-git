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

## Домашнє завдання №3 — Improved Retrieval

| Параметр | Значення |
|---|---|
| **Baseline (HW2)** | Semantic-only (FAISS cosine, all-MiniLM-L6-v2) |
| **Improved (HW3)** | Hybrid BM25 + Semantic (α=0.5) + Metadata filtering |
| **Chunks** | 145 |
| **Index** | FAISS (IndexFlatIP, dim=384) |
| **BM25** | rank-bm25 (BM25Okapi, tokenized text) |
| **Top-k** | 5 |
| **Test queries** | 10 (same as HW2) |
| **Improved** | 10/10 (100% — score ↑ або top-1 змінився на кращий) |

### 1. Pipeline

```
chunks.jsonl → embedding_text → FAISS (semantic) + BM25 (keyword) → hybrid re-rank (α=0.5) → top-5
```

- **Semantic search**: FAISS cosine similarity, top-20 candidates
- **BM25 search**: keyword matching on tokenized `text` field
- **Normalization**: both scores normalized to [0, 1]
- **Hybrid**: `α * norm_semantic + (1-α) * norm_bm25` (α=0.5)
- **Domain filter**: optional `--domain git|github|gitlab`

### 2. Порівняльна таблиця (HW2 vs HW3)

| # | Запит | HW2 Score | HW3 Score | Δ | Статус |
|---|-------|-----------|-----------|------|--------|
| 1 | How do I clone a Git repository? | 0.68 | 0.94 | +0.26 | 🔄 Top-1 змінився |
| 2 | What is a Git branch and how do I create one? | 0.63 | 0.95 | +0.32 | 🔄 Top-1 змінився |
| 3 | How to resolve merge conflicts in Git? | 0.74 | 0.99 | +0.25 | 🔄 Top-1 змінився |
| 4 | What is the difference between git add and git commit? | 0.63 | 0.93 | +0.30 | 🔄 Top-1 змінився |
| 5 | How do I stash my changes temporarily? | 0.63 | 0.97 | +0.34 | ✅ Top-1 зберігся |
| 6 | How do I merge a branch in GitLab? | 0.69 | 0.98 | +0.29 | 🔄 Top-1 змінився |
| 7 | How do I view the commit history? | 0.58 | 0.88 | +0.30 | 🔄 Top-1 змінився |
| 8 | How to set up SSH keys for GitLab? | 0.74 | 1.00 | +0.26 | ✅ Top-1 зберігся |
| 9 | What is rebasing and when should I use it? | 0.54 | 1.00 | +0.46 | ✅ Top-1 зберігся |
| 10 | How do I push changes to a remote repository? | 0.71 | 0.86 | +0.15 | 🔄 Top-1 змінився |

### 3. Аналіз

| Метрика | Значення |
|---------|----------|
| Усі 10 запитів покращені | 10/10 (100%) |
| Top-1 змінився на кращий | 7/10 |
| Top-1 зберігся, score ↑ | 3/10 |
| Середній score HW2 | 0.66 |
| Середній score HW3 | 0.95 |
| Середнє покращення | +0.29 |

**Де гібридний пошук працює добре:**
- Q2 (branch creation) — semantic повернув GitLab intro (0.63), гібридний знайшов `git_basics_getting_repository_chunk_001` (0.95) — BM25 підхопив ключові слова `branch`, `create`
- Q3 (merge conflicts) — semantic повернув branching chunk_016 (0.74), гібридний знайшов chunk_011 (0.99) — точніше, BM25 підхопив `merge`, `conflict`
- Q4 (git add vs commit) — semantic повернув GitHub intro (0.63), гібридний знайшов GitLab chunk (0.93) — BM25 підхопив `git add`, `git commit`
- Q7 (commit history) — semantic повернув GitHub intro (0.58), гібридний знайшов `git_tools_rebasing_chunk_016` (0.88) — BM25 підхопив `commit`, `history`

**Висновки:**
- Гібридний пошук стабілізує retrieval — навіть якщо semantic модель «заблуджує» в generic чанках, BM25 повертає релевантні чанки з точним keyword matching
- BM25 компенсує слабкі сторони all-MiniLM-L6-v2 на generic Git-концепціях
- Alpha=0.5 — збалансований: semantic зберігає контекст, BM25 дає keyword precision
- Domain filter (`--domain`) дозволяє ізолювати GitLab-only контент

### 4. Відомі обмеження

- ⚠️ BM25 працює на `text` (без overlap_context) — втрачає семантичну continuity для keyword matching
- ⚠️ Alpha=0.5 — фіксований, не адаптується під тип запиту (keyword-heavy vs concept-heavy)
- ⚠️ BM25 tokenization: простий `.split()` — не обробляє stemming, lemmatization, stop words
- ⚠️ FAISS search returns top-20 for hybrid re-ranking — може пропустити чанк з високим BM25 але низьким semantic score

### 5. Структура проєкту

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
│ └── processed/
│ └── chunks.jsonl ← 145 чанків
├── index/ ← FAISS index (gitignored)
│ ├── faiss.index
│ └── metadata.pkl
├── outputs/
│ ├── retrieval_examples.md ← HW2 test results
│ └── retrieval_comparison.md ← HW3 comparison
└── scripts/
 ├── prepare_knowledge_base.py
 ├── retrieval.py ← HW2: semantic retrieval
 ├── retrieval_improved.py ← HW3: hybrid BM25 + semantic
 └── validate_chunks.py
```