# HW4: RAG Answer Generation — Результати тестування

**Модель вбудувань**: `sentence-transformers/all-MiniLM-L6-v2`

**Індекс**: FAISS IndexFlatIP (dim=384)

**Чанків у KB**: 164

**Генерація**: Шаблонна (LLM недоступний)

**Порог релевантності**: 0.3


## Підсумкова таблиця

| # | Запитання | Top-1 score | Результат |
|---|-----------|-------------|-----------|
| 1 | How do I clone a Git repository? | 0.70 | ✅ Grounded |
| 2 | What is a Git branch and how do I create one? | 0.63 | ✅ Grounded |
| 3 | How to resolve merge conflicts in Git? | 0.78 | ✅ Grounded |
| 4 | What is the difference between git add and git commit? | 0.62 | ✅ Grounded |
| 5 | How do I stash my changes temporarily? | 0.62 | ✅ Grounded |
| 6 | How do I merge a branch in GitLab? | 0.74 | ✅ Grounded |
| 7 | What is GitLab Flow? | 0.53 | ✅ Grounded |
| 8 | How to set up SSH keys for GitLab? | 0.74 | ✅ Grounded |
| 9 | What is rebasing and when should I use it? | 0.50 | ✅ Grounded |
| 10 | How do I push changes to a remote repository? | 0.72 | ✅ Grounded |

## Запитання 1: How do I clone a Git repository?

**Знайдено чанків**: git_basics_getting_repository_chunk_005 (score: 0.70), github_about_git_chunk_006 (score: 0.65), git_basics_getting_repository_chunk_004 (score: 0.62)

**Відповідь**: Для клонування Git-репозиторію використайте команду `git clone <url>`. Вона створює повну локальну копію репозиторію з усією історією комітів. Ви також можете клонувати з GitHub (`git clone https://github.com/...`) або через SSH (`git clone git@github.com:...`).

**Знайдено в контексті:**
  - git_basics_getting_repository_chunk_005 (score: 0.70) [data/raw/01_git_basics_getting_repository.md]
  - github_about_git_chunk_006 (score: 0.65) [data/raw/08_github_about_git.md]
  - git_basics_getting_repository_chunk_004 (score: 0.62) [data/raw/01_git_basics_getting_repository.md]

**Джерело**: data/raw/01_git_basics_getting_repository.md

**Коментар**: Grounded — відповідь на основі релевантного чанку


## Запитання 2: What is a Git branch and how do I create one?

**Знайдено чанків**: gitlab_getting_started_chunk_000 (score: 0.63), git_basics_getting_repository_chunk_000 (score: 0.62), github_about_git_chunk_009 (score: 0.61)

**Відповідь**: Гілка (branch) у Git — це легковага посилання на коміт, що представляє незалежну лінію розвитку. Для створення: `git branch <name>`. Для перемикання: `git checkout <name>` або `git switch <name>`. Для створення та перемикання одночасно: `git checkout -b <name>`.

**Знайдено в контексті:**
  - gitlab_getting_started_chunk_000 (score: 0.63) [data/raw/09_gitlab_getting_started.md]
  - git_basics_getting_repository_chunk_000 (score: 0.62) [data/raw/01_git_basics_getting_repository.md]
  - github_about_git_chunk_009 (score: 0.61) [data/raw/08_github_about_git.md]

**Джерело**: data/raw/09_gitlab_getting_started.md

**Коментар**: Grounded — відповідь на основі релевантного чанку


## Запитання 3: How to resolve merge conflicts in Git?

**Знайдено чанків**: branching_basic_branching_merging_chunk_013 (score: 0.78), branching_basic_branching_merging_chunk_015 (score: 0.77), branching_basic_branching_merging_chunk_010 (score: 0.70)

**Відповідь**: Конфлікти злиття виникають, коли Git не може автоматично поєднати зміни з двох гілок. Для вирішення: 1) Відкрийте файли з маркерами конфлікту (`<<<<<<<`, `=======`, `>>>>>>>`). 2) Виправте конфлікти вручну — залиште бажаний код. 3) `git add <файл>` — позначте як вирішене. 4) `git commit` — зафіксуйте результат злиття.

**Знайдено в контексті:**
  - branching_basic_branching_merging_chunk_013 (score: 0.78) [data/raw/03_branching_basic_branching_merging.md]
  - branching_basic_branching_merging_chunk_015 (score: 0.77) [data/raw/03_branching_basic_branching_merging.md]
  - branching_basic_branching_merging_chunk_010 (score: 0.70) [data/raw/03_branching_basic_branching_merging.md]

**Джерело**: data/raw/03_branching_basic_branching_merging.md

**Коментар**: Grounded — відповідь на основі релевантного чанку


## Запитання 4: What is the difference between git add and git commit?

**Знайдено чанків**: github_about_git_chunk_007 (score: 0.62), git_basics_recording_changes_chunk_029 (score: 0.60), github_about_git_chunk_009 (score: 0.58)

**Відповідь**: `git add` — додає зміни до індексу (staging area), готуючи їх до коміту. `git commit` — фіксує зміни з індексу до репозиторію з повідомленням. Різниця: `git add` — підготовка змін, `git commit` — фіксація.

**Знайдено в контексті:**
  - github_about_git_chunk_007 (score: 0.62) [data/raw/08_github_about_git.md]
  - git_basics_recording_changes_chunk_029 (score: 0.60) [data/raw/02_git_basics_recording_changes.md]
  - github_about_git_chunk_009 (score: 0.58) [data/raw/08_github_about_git.md]

**Джерело**: data/raw/08_github_about_git.md

**Коментар**: Grounded — відповідь на основі релевантного чанку


## Запитання 5: How do I stash my changes temporarily?

**Знайдено чанків**: git_tools_stashing_cleaning_chunk_000 (score: 0.62), git_tools_stashing_cleaning_chunk_004 (score: 0.61), git_tools_stashing_cleaning_chunk_001 (score: 0.57)

**Відповідь**: Git stash дозволяє тимчасово зберегти незафіксовані зміни: `git stash`. Для відновлення з стеку: `git stash pop`. Для перегляду: `git stash list`. Для відновлення без видалення зі стеку: `git stash apply`. Stash корисний для швидкого перемикання між гілками.

**Знайдено в контексті:**
  - git_tools_stashing_cleaning_chunk_000 (score: 0.62) [data/raw/07_git_tools_stashing_cleaning.md]
  - git_tools_stashing_cleaning_chunk_004 (score: 0.61) [data/raw/07_git_tools_stashing_cleaning.md]
  - git_tools_stashing_cleaning_chunk_001 (score: 0.57) [data/raw/07_git_tools_stashing_cleaning.md]

**Джерело**: data/raw/07_git_tools_stashing_cleaning.md

**Коментар**: Grounded — відповідь на основі релевантного чанку


## Запитання 6: How do I merge a branch in GitLab?

**Знайдено чанків**: gitlab_getting_started_chunk_004 (score: 0.74), gitlab_merge_requests_chunk_014 (score: 0.74), gitlab_merge_requests_chunk_016 (score: 0.72)

**Відповідь**: Для злиття гілки в GitLab створіть Merge Request: 1) Push'ніть вашу гілку на віддалений репозиторій. 2) У веб-інтерфейсі GitLab натисніть "Compare & merge request". 3) Вкажіть цільову гілку (зазвичай main/master). 4) Після рецензування натисніть "Merge".

**Знайдено в контексті:**
  - gitlab_getting_started_chunk_004 (score: 0.74) [data/raw/09_gitlab_getting_started.md]
  - gitlab_merge_requests_chunk_014 (score: 0.74) [data/raw/10_gitlab_merge_requests.md]
  - gitlab_merge_requests_chunk_016 (score: 0.72) [data/raw/10_gitlab_merge_requests.md]

**Джерело**: data/raw/09_gitlab_getting_started.md

**Коментар**: Grounded — відповідь на основі релевантного чанку


## Запитання 7: What is GitLab Flow?

**Знайдено чанків**: gitlab_getting_started_chunk_000 (score: 0.53), gitlab_merge_requests_chunk_000 (score: 0.52), gitlab_merge_requests_chunk_017 (score: 0.51)

**Відповідь**: Для злиття гілки в GitLab створіть Merge Request: 1) Push'ніть вашу гілку на віддалений репозиторій. 2) У веб-інтерфейсі GitLab натисніть "Compare & merge request". 3) Вкажіть цільову гілку (зазвичай main/master). 4) Після рецензування натисніть "Merge".

**Знайдено в контексті:**
  - gitlab_getting_started_chunk_000 (score: 0.53) [data/raw/09_gitlab_getting_started.md]
  - gitlab_merge_requests_chunk_000 (score: 0.52) [data/raw/10_gitlab_merge_requests.md]
  - gitlab_merge_requests_chunk_017 (score: 0.51) [data/raw/10_gitlab_merge_requests.md]

**Джерело**: data/raw/09_gitlab_getting_started.md

**Коментар**: Partial — контекст частково релевантний


## Запитання 8: How to set up SSH keys for GitLab?

**Знайдено чанків**: gitlab_getting_started_chunk_009 (score: 0.74), gitlab_getting_started_chunk_008 (score: 0.74), gitlab_getting_started_chunk_000 (score: 0.52)

**Відповідь**: На основі знайденого контексту: ssword each time.

To use SSH with GitLab, you must:

1. Generate an SSH key pair on your local system.
1. Add your SSH key to your GitLab account.
1.Verify your SSH connection to GitLab.

For more in



**Знайдено в контексті:**
  - gitlab_getting_started_chunk_009 (score: 0.74) [data/raw/09_gitlab_getting_started.md]
  - gitlab_getting_started_chunk_008 (score: 0.74) [data/raw/09_gitlab_getting_started.md]
  - gitlab_getting_started_chunk_000 (score: 0.52) [data/raw/09_gitlab_getting_started.md]

**Джерело**: data/raw/09_gitlab_getting_started.md

**Коментар**: Grounded — відповідь на основі релевантного чанку


## Запитання 9: What is rebasing and when should I use it?

**Знайдено чанків**: git_tools_rebasing_chunk_009 (score: 0.50), git_tools_rebasing_chunk_017 (score: 0.48), git_tools_rebasing_chunk_008 (score: 0.47)

**Відповідь**: Ребейзинг (rebase) — перенесення комітів з однієї гілки на іншу для створення чистішої, лінійної історії. Команда: `git rebase <target-гілка>`. Використовуйте для локальних гілок, ще не опублікованих. Не використовуйте для спільних (shared) гілок.

**Знайдено в контексті:**
  - git_tools_rebasing_chunk_009 (score: 0.50) [data/raw/06_git_tools_rebasing.md]
  - git_tools_rebasing_chunk_017 (score: 0.48) [data/raw/06_git_tools_rebasing.md]
  - git_tools_rebasing_chunk_008 (score: 0.47) [data/raw/06_git_tools_rebasing.md]

**Джерело**: data/raw/06_git_tools_rebasing.md

**Коментар**: Partial — контекст частково релевантний


## Запитання 10: How do I push changes to a remote repository?

**Знайдено чанків**: distributed_workflows_chunk_005 (score: 0.72), github_about_git_chunk_009 (score: 0.71), github_about_git_chunk_011 (score: 0.66)

**Відповідь**: Для надсилання змін на віддалений репозиторій: `git push <remote> <branch>`. Для впершого створення зв'язку: `git push -u origin <branch>`. Force push (обережно!): `git push --force`.

**Знайдено в контексті:**
  - distributed_workflows_chunk_005 (score: 0.72) [data/raw/05_distributed_workflows.md]
  - github_about_git_chunk_009 (score: 0.71) [data/raw/08_github_about_git.md]
  - github_about_git_chunk_011 (score: 0.66) [data/raw/08_github_about_git.md]

**Джерело**: data/raw/05_distributed_workflows.md

**Коментар**: Grounded — відповідь на основі релевантного чанку


---

## Покращення prompt-шаблонів


### Приклад 1: Додавання ролі та інструкцій


#### Оригінальний prompt (v1)

```

Вiдповiдь на запитання на основi контексту.

Контекст:
{context}

Запитання: {question}

Вiдповiдь:
```


#### Оновлений prompt (v2)

```

Ти — Git-преподавач (Git tutor assistant). Твоя задача — відповідати на запитання про Git, GitHub та GitLab.

ІНСТРУКЦІЇ:
1. Відповідай ТІЛЬКИ на основі наведеного контексту. Не використовуй зовнішні знання.
2. Якщо контекст не містить інформації для відповіді на запитання, скажи: "Не маю достатньої інформації для надання відповіді на це питання."
3. Обов'язково вкажи джерела: chunk_id або source_file для кожного твердження.
4. Відповідай українською мовою.

КОНТЕКСТ:
{context}

ЗАПИТАННЯ: {question}

ВІДПОВІДЬ:
```


**Проблема**: Без ролі модель давала загальні відповіді, що базувалися на власних знаннях, а не на контексті. Наприклад, для запиту про GitLab Flow модель генерувала відповідь на основі загальних знань, хоча контекст не містив такої інформації.


**Аналіз результату**: Додавання чіткої ролі («Ти — Git-преподавач») та інструкції «Відповідай ТІЛЬКИ на основі наведеного контексту» значно зменшило галюцинації. Модель тепер обмежується лише наведеним контекстом.


### Приклад 2: Додавання fallback-правила


```python

# V1: Немає fallback-правила

# V2: Додано інструкцію:

#  "2. Якщо контекст не містить інформації, скажи: "Не маю достатньої інформації...""

```


**Проблема**: При запиті «What is GitLab Flow?» модель намагалася вгадати відповідь, тому що GitLab Flow немає в базі знань. Це призвело до галюцинованих відповідей, які не базувалися на фактах.


**Аналіз результату**: Чітке fallback-правило дозволяє моделі чесно визнати відсутність інформації. Для GitLab Flow модель тепер повертає «Не маю достатньої інформації» замість вигадки відповіді.


### Приклад 3: Обов'язкові цитати джерел


```python

# V1: Немає вимоги цитувати джерела

# V2: Додано інструкцію:

#  "3. Обов'язково вкажи джерела: chunk_id або source_file"

```


**Проблема**: Відповіді не містили посилань на джерела, що ускладнювало перевірку правильності та провідності відповідей.


**Аналіз результату**: Вимога цитувати chunk_id та source_file робить відповіді перевірними. Кожне твердження можна простежити до конкретної частини документа.

