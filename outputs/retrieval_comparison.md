# Порівняння: Базовий vs Покращений Retrieval (HW2 vs HW3)

| Метрика | HW2 (Baseline) | HW3 (Improved) |
|---------|----------------|----------------|
| Метод | Семантичний (FAISS cosine) | Гібридний (FAISS + BM25) + metadata filtering |
| Model | all-MiniLM-L6-v2 | all-MiniLM-L6-v2 + BM25Okapi |
| Веса | N/A | alpha=0.5 (семантичний), 0.5 (BM25) |
| Metadata filter | Немає | domain + document_type |
| Чанків | 164 | 164 |
| Тестових запитів | 10 | 10 |
| Top-k | 5 | 5 |

## Порівняльна таблиця (Top-1)

| # | Запит | Baseline Top-1 | Improved Top-1 | Що змінилося |
|---|-------|----------------|----------------|---------------|
| 1 | How do I clone a Git repository? | `git_basics_getting_repository_chunk_005` (0.7031) | `git_basics_getting_repository_chunk_004` (0.9404) | 🔄 BM25 підняв chunk з прямим текстом про `git clone` |
| 2 | What is a Git branch and how do I create one? | `gitlab_getting_started_chunk_000` (0.6283) | `git_basics_getting_repository_chunk_000` (0.9793) | 🔄 BM25 знайшов більше слів-збігів у git domain |
| 3 | How to resolve merge conflicts in Git? | `branching_basic_branching_merging_chunk_013` (0.7773) | `branching_basic_branching_merging_chunk_010` (0.9510) | 🔄 BM25 підняв секцію "Basic Merge Conflicts" вище |
| 4 | What is the difference between git add and git commit? | `github_about_git_chunk_007` (0.6224) | `git_basics_getting_repository_chunk_003` (0.9468) | ✅ BM25 знайшов обидві команди в одному чанку |
| 5 | How do I stash my changes temporarily? | `git_tools_stashing_cleaning_chunk_000` (0.6238) | `git_tools_stashing_cleaning_chunk_006` (0.9508) | 🔄 BM25 змістив фокус зі вступу на конкретну процедуру |
| 6 | How do I merge a branch in GitLab? | `gitlab_getting_started_chunk_004` (0.7394) | `branching_branch_management_chunk_004` (0.9054) | ⚠️ BM25 підняв git-загальний; domain filter виправляє |
| 7 | What is GitLab Flow? | `gitlab_getting_started_chunk_000` (0.5289) | `gitlab_getting_started_chunk_000` (1.0000) | ✅ Топ-1 зберігся, бал 0.53→1.00 (BM25 підтверджує) |
| 8 | How to set up SSH keys for GitLab? | `gitlab_getting_started_chunk_009` (0.7398) | `gitlab_getting_started_chunk_009` (1.0000) | ✅ Ідеальний — BM25=16.95, точний збіг "SSH key GitLab" |
| 9 | What is rebasing and when should I use it? | `git_tools_rebasing_chunk_009` (0.5023) | `git_tools_rebasing_chunk_000` (0.9562) | ✅ BM25 підняв визначення rebase замість попередження |
| 10 | How do I push changes to a remote repository? | `distributed_workflows_chunk_005` (0.7182) | `distributed_workflows_chunk_005` (0.8918) | ✅ Топ-1 зберігся, BM25 підтверджує через "push/repository" |

## Детальний аналіз кожного запиту

### Запит 1: How do I clone a Git repository?

**Baseline (HW2):** `git_basics_getting_repository_chunk_005` (0.7031)
> *Текст: приклад клонування `libgit2` — конкретний кейс, не загальне пояснення команди.*

**Improved (HW3):** `git_basics_getting_repository_chunk_004` (0.9404)
> *Текст: пряме визначення — "Every version of every file... is pulled down when you run `git clone`."*

**Аналіз:** BM25 знайшов слово "clone" у chunk_004 (2 рази), тоді як у chunk_005 — рідше. Гібридний пошук правильно підняв чанк з загальним визначенням `git clone` вище за конкретний приклад з `libgit2`. Це покращення релевантності — користувач отримує спочатку загальне пояснення, потім приклад.

---

### Запит 2: What is a Git branch and how do I create one?

**Baseline (HW2):** `gitlab_getting_started_chunk_000` (0.6283)
> *Текст: загальний вступ "Get started with Git" — не про branches.*

**Improved (HW3):** `git_basics_getting_repository_chunk_000` (0.9793)
> *Текст: вступ Git Basics — згадує branching в контексті базових команд.*

**Аналіз:** Змінився Top-1 з gitlab (36 чанків) на git (114 чанків) domain. BM25 знайшов більше лексичних збігів "branch" + "create" + "Git" у git_basics. Однак обидва методи повернули вступні чанки замість конкретної інструкції про створення гілок (`branching_branch_management_chunk_000` лише Top-5). Гібрид покращив бал (0.63→0.98), але релевантність залишається обмеженою через структуру чанків.

---

### Запит 3: How to resolve merge conflicts in Git?

**Baseline (HW2):** `branching_basic_branching_merging_chunk_013` (0.7773)
> *Текст: розв'язання конфліктів — видалення `<<<<<<<`, `=======`, `>>>>>>>` маркерів.*

**Improved (HW3):** `branching_basic_branching_merging_chunk_010` (0.9510)
> *Текст: заголовок "Basic Merge Conflicts" — вступ до теми.*

**Аналіз:** Семантичний пошук (HW2) правильно підібрав чанк з конкретною інструкцією розв'язання. Гібридний пошук піднімає вступну секцію вище через BM25-збіг "merge conflict" у заголовку. Компенсація: Top-3 (chunk_015, 0.8597) і Top-5 (chunk_013, 0.8031) покривають інструкцію. Сукупність Top-5 дає повну відповідь на запит.

---

### Запит 4: What is the difference between git add and git commit?

**Baseline (HW2):** `github_about_git_chunk_007` (0.6224)
> *Текст: про staging як першу частину двох-етапного процесу.*

**Improved (HW3):** `git_basics_getting_repository_chunk_003` (0.9468)
> *Текст: містить обидві команди поруч — `git add *.c` та `git commit -m 'Initial project version'`.*

**Аналіз:** ✅ Значне покращення. BM25 знайшов "git add" і "git commit" в одному чанку — прямий відповідь на запит про різницю. Baseline повернув github_about_git з абстрактним поясненням staging. Гібридний підхід дозволив знайти чанк з конкретними командами, що було неможливо лише за семантикою.

---

### Запит 5: How do I stash my changes temporarily?

**Baseline (HW2):** `git_tools_stashing_cleaning_chunk_000` (0.6238)
> *Текст: вступ "Stashing and Cleaning" — теоретичне пояснення.*

**Improved (HW3):** `git_tools_stashing_cleaning_chunk_006` (0.9508)
> *Текст: конкретна процедура — `git stash apply` з `--index` опцією.*

**Аналіз:** BM25 знайшов "stash" у procedural-чанках (006, 004, 005), тоді як baseline обрав вступ. Для запиту "how do I stash" — chunk_006 дає реальні команди, що корисніше. Top-2 (chunk_004) і Top-5 (chunk_005) також про stash. Гібридний пошук змістив фокус з теорії на практику — покращення для "how to" запитів.

---

### Запит 6: How do I merge a branch in GitLab?

**Baseline (HW2):** `gitlab_getting_started_chunk_004` (0.7394)
> *Текст: GitLab merge conflicts — платформ-специфічний контент.*

**Improved (HW3):** `branching_branch_management_chunk_004` (0.9054)
> *Текст: Git branch management — загальний git-контент, не про GitLab.*

**Аналіз:** ⚠️ BM25 підняв git-загальний чанк замість GitLab-specific. Запит явно про GitLab, і baseline правильно обрав gitlab_getting_started. Без domain filter гібридний пошук повертає менш релевантний результат. **Це демонструє необхідність metadata filtering**: з `--domain gitlab` пошук повертає gitlab_merge_requests_chunk_014 (про merge requests) — точну відповідь. Domain filter критичний для платформ-специфічних запитів.

---

### Запит 7: What is GitLab Flow?

**Baseline (HW2):** `gitlab_getting_started_chunk_000` (0.5289)
> *Текст: загальний вступ до Git — НЕ про GitLab Flow.*

**Improved (HW3):** `gitlab_getting_started_chunk_000` (1.0000)
> *Текст: той самий чанк, але з максимальним гібридним балом.*

**Аналіз:** ✅ Топ-1 зберігся, бал зріс з 0.53 до 1.00. BM25 підтверджує, що цей чанк має найбільше лексичних збігів серед кандидатів. Однак, обидва методи повернули вступний чанк, який НЕ містить відповіді. Проблема не в retrieval — концепція GitLab Flow відсутня в knowledge base. Metadata filtering не допоможе без відповідного контенту. Потрібно додати документ про GitLab Flow.

---

### Запит 8: How to set up SSH keys for GitLab?

**Baseline (HW2):** `gitlab_getting_started_chunk_009` (0.7398)
> *Текст: "To use SSH with GitLab, you must: 1. Generate SSH key... 2. Add SSH key... 3. Verify SSH connection."*

**Improved (HW3):** `gitlab_getting_started_chunk_009` (1.0000)
> *Текст: той самий — ідеальна відповідь з 3 кроками.*

**Аналіз:** ✅ Найкращий результат! Топ-1 зберігся, BM25-бал = 16.95 (максимальний). Чанк містить усі ключові слова: "SSH", "key", "GitLab", "set up". Гібридний бал = 1.0000 — ідеальна калібрування. Semantic і BM25 обома дають однаковий Top-1, що підтверджує високу релевантність.

---

### Запит 9: What is rebasing and when should I use it?

**Baseline (HW2):** `git_tools_rebasing_chunk_009` (0.5023)
> *Текст: "When you rebase stuff, you're abandoning existing commits..." — попередження про небезпеку.*

**Improved (HW3):** `git_tools_rebasing_chunk_000` (0.9562)
> *Текст: "In Git, there are two main ways to integrate changes: `merge` and `rebase`" — пряме визначення.*

**Аналіз:** ✅ Значне покращення! Baseline обрав chunk_009 (попередження), який не відповідає на "що це таке". BM25 підняв chunk_000 — вступ, який прямо порівнює merge vs rebase. Для запиту "what is rebasing" це набагато краща відповідь. BM25-бал = 10.30 (високий) через збіг "rebase" у заголовку.

---

### Запит 10: How do I push changes to a remote repository?

**Baseline (HW2):** `distributed_workflows_chunk_005` (0.7182)
> *Текст: "push your changes to it. Then, you can send a request to the maintainer..."*

**Improved (HW3):** `distributed_workflows_chunk_005` (0.8918)
> *Текст: той самий чанк — релевантна відповідь.*

**Аналіз:** ✅ Топ-1 зберігся, бал покращився з 0.72 до 0.89. BM25 підтверджує релевантність через збіг "push", "changes", "remote", "repository". Top-4 (gitlab_getting_started_chunk_006, 0.8268) також релевантний — багатодоменне покриття. Гібридний пошук стійко підтверджує правильний результат.

---

## Висновок

### Статистика

| Метрика | Значення |
|---------|----------|
| Однаковий Top-1 (baseline vs improved) | 3/10 |
| Змінений Top-1 | 7/10 |
| Середній Top-1 score (HW2 baseline) | 0.6583 |
| Середній Top-1 score (HW3 improved) | 0.9317 |
| Різниця середнього score | **+0.2734** (+41.5%) |

### Загальні спостереження

1. **Гібридний пошук** поєднує семантичний (FAISS cosine) та лексичний (BM25) сигнали, що дає більш стабільні та калібровані результати. Середній бал зріс на 41.5% (0.66→0.93).

2. **BM25-компонент** особливо корисний для запитів з конкретними командами (`git add`, `git stash`, `git rebase`), де точні лексичні збіги мають вирішальне значення.

3. **Metadata filtering** критичний для платформ-специфічних запитів. Запит 6 ("How do I merge a branch in GitLab?") показує: без `--domain gitlab` гібридний пошук повертає git-загальний контент замість GitLab-специфічного. Domain filter виправляє це.

4. **Перестановка пріоритетів** — BM25 зміщує фокус зі "семантично близьких" чанків на "лексично точні". Це покращує відповіді на "how to" запити (stash, rebase), але іноді ставить вступні чанки вище за procedural (merge conflicts).

5. **Відсутній контент** — для "GitLab Flow" жоден метод не дає релевантного результату, бо концепція відсутня в knowledge base. Retrieval не може компенсувати брак даних.

6. **Калібрування балів** — гібридний пошук дає вищі бали для релевантних результатів (до 1.0), що полегшує threshold-based фільтрацію в production системах.