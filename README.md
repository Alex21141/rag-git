# Git tutoring assistant

## Домашнє завдання №2 — Базовий semantic retrieval layer

| Параметр | Значення |
|---|---|
| **Embedding model** | sentence-transformers/all-MiniLM-L6-v2 |
| **Vector storage** | FAISS IndexFlatIP (dim=384) |
| **Chunks indexed** | 158 |
| **Test queries** | 10 |
| **Top-k** | 5 |

### Результати тестування

| Запит | Top-1 chunk | Score | Релевантність |
|-------|-------------|-------|---------------|
| How do I clone a Git repository? | git_basics_getting_repository_chunk_005 | 0.70 | ✅ Relevant |
| What is a Git branch and how do I create one? | gitlab_getting_started_chunk_000 | 0.63 | ✅ Relevant |
| How to resolve merge conflicts in Git? | branching_basic_branching_merging_chunk_013 | 0.78 | ✅ Relevant |
| What is the difference between git add and git commit? | github_about_git_chunk_007 | 0.62 | ✅ Relevant |
| How do I stash my changes temporarily? | git_tools_stashing_cleaning_chunk_000 | 0.62 | ✅ Relevant |
| How do I merge a branch in GitLab? | gitlab_getting_started_chunk_004 | 0.74 | ✅ Relevant |
| How do I view the commit history? | github_about_git_chunk_000 | 0.57 | ⚠️ Partially |
| How to set up SSH keys for GitLab? | gitlab_getting_started_chunk_009 | 0.74 | ✅ Relevant |
| What is rebasing and when should I use it? | git_tools_rebasing_chunk_009 | 0.50 | ⚠️ Partially |
| How do I push changes to a remote repository? | distributed_workflows_chunk_005 | 0.72 | ✅ Relevant |

### Висновок

**Де retrieval добре працює:**
- ✅ **Специфічні команди** (`git clone`, `git stash`, `git merge`, `git push`, `git add`, `git commit`, SSH keys) — score 0.62–0.78. У 8/10 запитів Top-1 релевантний.
- ✅ **Унікальні терміни** — `conflict`, `stash`, `merge`, `repository`, `clone` — семантичні вектори добре розрізняють ці поняття.
- ✅ **Домен-специфічні запити** — `gitlab_getting_started` правильно знаходить GitLab SSH та merge workflow.

**Де retrieval погано працює:**
- ⚠️ **Загальні терміни** (`branch`, `rebase`, `commit history`) — повертають вступи замість конкретики. Напр. `branch` знаходить `gitlab_getting_started_chunk_000` (вступ про Git) замість розділу про гілки.
- ⚠️ **Low-score запити** — `rebase` (0.50) і `commit history` (0.57) — семантичний embedding не розрізняє контекст (warning vs реалізацію).
- ⚠️ **Відсутня лексична точність** — чистий semantic не знаходить точні збіги ключових слів (напр. `git add` vs `add`).

**Висновок:** Базовий semantic retrieval задовільно працює для конкретних команд, але потребує гібридного підходу для покращення на загальних термінах.

**Повні результати**: `outputs/retrieval_examples.md`

### Структура проєкту

```
rag-github/
├── README.md ← цей файл
├── data/
│   ├── raw/ ← початкові документи (10 .md)
│   │   ├── 03_branching_basic_branching_merging.md
│   │   ├── 04_branching_branch_management.md
│   │   └── 05_distributed_workflows.md
│   └── processed/
│       └── chunks.jsonl ← 158 чанків
├── index/
│   ├── faiss.index ← FAISS IndexFlatIP (dim=384)
│   └── metadata.pkl ← серіалізовані метадані
├── outputs/
│   └── retrieval_examples.md ← результати 10 запитів
└── scripts/
    ├── download_sources.py ← збір даних з веб
    ├── prepare_knowledge_base.py ← chunking + нормалізація
    ├── retrieval.py ← semantic retrieval (FAISS + sentence-transformers)
    └── validate_chunks.py ← JSONL валідатор
```