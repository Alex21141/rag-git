# Git tutoring assistant

## Домашнє завдання №5 — Інтеграція зовнішнього tool або джерела

| Параметр | Значення |
|----------|----------|
| **Tool-ів реалізовано** | 2 |
| **Тип** | read-інструменти |
| **Джерело даних** | Структурована БД Git-команд + Git-конфігурація |
| **Тестових прикладів** | 5 |
| **Валідація** | Обов'язкові поля + перевірка типу + enum + перевірка формату |

### 1. Вибір типу tool

Вибрано: **API tool** (пошук у структурованій базі даних).

| Tool | Призначення |
|------|-------------|
| `get_git_command` | Повертає структуровану інформацію про Git-команду (синтаксис, опис, приклади) |
| `get_git_config` | Повертає значення Git-конфігурації для заданого scope (global/local) |

Обидва — **read-інструменти**: не змінюють дані, тільки читають.

### 2. Опис tool-ів

#### get_git_command

| Параметр | Значення |
|---|---|
| Назва | `get_git_command` |
| Тип | read-інструмент |
| Мета | Повертає структуровану інформацію про Git-команду: синтаксис, короткий опис, приклади використання |
| Джерело | Структурована база даних Git-команд (14 команд) |
| Коли викликати | Користувач запитує "як зробити X" або "що робить git X" |
| Коли НЕ викликати | Концептуальні питання ("що таке merge conflict?") — використовувати RAG замість |

**Input schema:**
```json
{
  "type": "object",
  "properties": {
    "command": {
      "type": "string",
      "description": "Git command name (e.g., 'clone', 'push', 'merge', 'stash', 'rebase')"
    }
  },
  "required": ["command"]
}
```

**Output structure:**
```json
{
  "command": "clone",
  "full_command": "git clone",
  "synopsis": "git clone <repository> [directory]",
  "description": "Clone a repository into a new directory...",
  "examples": ["git clone https://github.com/user/repo.git"]
}
```

#### get_git_config

| Параметр | Значення |
|---|---|
| Назва | `get_git_config` |
| Тип | read-інструмент |
| Мета | Повертає значення Git-конфігурації для заданого scope |
| Джерело | Git config (global/local) |
| Коли викликати | Користувач запитує про свої налаштування git |
| Коли НЕ викликати | Запитання про використання git-команд — використовувати `get_git_command` |

**Input schema:**
```json
{
  "type": "object",
  "properties": {
    "scope": {
      "type": "string",
      "description": "Config scope: 'global' or 'local'",
      "enum": ["global", "local"]
    },
    "key": {
      "type": "string",
      "description": "Optional specific config key (e.g., 'user.email')"
    }
  },
  "required": ["scope"]
}
```

**Output structure:**
```json
{
  "scope": "global",
  "key": "user.name",
  "value": "Alex"
}
```

### 3. Validation

Перед виконанням tool-а перевіряється:

| Перевірка | Реалізація |
|-----------|------------|
| Обов'язкові поля | `call_tool()` перевіряє `required` поля з input schema |
| Тип даних | Перевірка `type` (string, integer) для кожного поля |
| Enum values | Перевірка, що `scope` є `"global"` або `"local"` |
| Формат даних | `get_git_command`: regex `^[a-z][a-z0-9-]*$` для назви команди |
| Normalization | `get_git_command`: автоматичне видалення префікса `git ` (напр. `git clone` → `clone`) |
| Suggestions | При помилці повертаються підказки (схожі команди/ключі) |
| Безпека | Tool не приймає raw SQL або довільний код — тільки структуровані параметри |

### 4. Реалізація та запуск

Реалізація: `scripts/external_tool.py` (224 рядки).

**Зареєстровані tool-и:** 2 (`get_git_command`, `get_git_config`).

**Запуск:**
```bash
# Список tool-ів
python3 scripts/external_tool.py --list

# Запуск всіх прикладів + генерація звіту
python3 scripts/external_tool.py --demo

# Виклик конкретного tool-а
python3 scripts/external_tool.py --tool get_git_command --input '{"command": "push"}'
```

**Результати демо:**
- `get_git_command(clone)` → ✅ OK
- `get_git_command(stash)` → ✅ OK
- `get_git_command(merge)` → ✅ OK
- `get_git_config(global, user.name)` → ✅ OK
- `get_git_config(global)` → ✅ OK

### 5. Приклади викликів

#### Приклад 1: How do I clone a Git repository?

**User question:** How do I clone a Git repository?

**Tool called:** `get_git_command`
**Input:** `{"command": "clone"}`

**Result:**
```json
{
  "command": "clone",
  "full_command": "git clone",
  "synopsis": "git clone <repository> [directory]",
  "description": "Clone a repository into a new directory. Creates a full local copy with complete history and all branches.",
  "examples": [
    "git clone https://github.com/user/repo.git",
    "git clone --depth=1 https://github.com/user/repo.git"
  ]
}
```

**Final answer:**
`git clone` — Clone a repository into a new directory. Creates a full local copy with complete history and all branches.

**Synopsis:** `git clone <repository> [directory]`

**Examples:**
- `git clone https://github.com/user/repo.git`
- `git clone --depth=1 https://github.com/user/repo.git`

**Чому tool кращий за retrieval:**
Git-команди мають точну структуровану інформацію (синтаксис, опис, приклади), яку краще надавати через запитуючу базу даних, ніж через семантичний пошук. Retrieval повернув би релевантні текстові чанки, а tool повертає точну структуру команди та офіційні приклади у нормалізованому форматі.

#### Приклад 2: What does git stash do?

**User question:** What does git stash do?

**Tool called:** `get_git_command`
**Input:** `{"command": "stash"}`

**Result:**
```json
{
  "command": "stash",
  "full_command": "git stash",
  "synopsis": "git stash [<options>]",
  "description": "Temporarily save changes and revert to the HEAD commit. Useful for quickly switching branches without committing.",
  "examples": ["git stash", "git stash pop", "git stash list"]
}
```

**Final answer:**
`git stash` — Temporarily save changes and revert to the HEAD commit. Useful for quickly switching branches without committing.

**Synopsis:** `git stash [<options>]`

**Examples:**
- `git stash`
- `git stash pop`
- `git stash list`

**Чому tool кращий за retrieval:**
Tool повертає точний синтаксис команди та приклади напряму зі структурованої бази — retrieval вимагав би поєднання кількох текстових чанків, і моделі довелося б синтезувати відповідь.

#### Приклад 3: How do I resolve a merge conflict?

**User question:** How do I resolve a merge conflict?

**Tool called:** `get_git_command`
**Input:** `{"command": "merge"}`

**Result:**
```json
{
  "command": "merge",
  "full_command": "git merge",
  "synopsis": "git merge [<options>] <branch>",
  "description": "Join two branches together. Integrates changes from the specified branch into the current branch.",
  "examples": ["git merge feature-branch", "git merge --no-ff feature-branch"]
}
```

**Final answer:**
`git merge` — Join two branches together. Integrates changes from the specified branch into the current branch.

**Synopsis:** `git merge [<options>] <branch>`

**Examples:**
- `git merge feature-branch`
- `git merge --no-ff feature-branch`

**Чому tool кращий за retrieval:**
Структуровані дані команд дають точний синтаксис та приклади, які retrieval з текстових чанків не зміг би надійно видобути. Tool гарантує правильну та повну інформацію про команду.

#### Приклад 4: What is my git username?

**User question:** What is my git username?

**Tool called:** `get_git_config`
**Input:** `{"scope": "global", "key": "user.name"}`

**Result:**
```json
{
  "scope": "global",
  "key": "user.name",
  "value": "Alex"
}
```

**Final answer:**
**global `user.name`** = `Alex`

**Чому tool кращий за retrieval:**
Git-конфігурація є персональною та динамічною — кожен користувач має різні налаштування. Ці дані неможливо зберігати в статичній базі знань. Інструмент, який запитує поточну конфігурацію — єдиний правильний підхід.

#### Приклад 5: Show me all my global git settings

**User question:** Show me all my global git settings

**Tool called:** `get_git_config`
**Input:** `{"scope": "global"}`

**Result:**
```json
{
  "scope": "global",
  "settings": {
    "user.name": "Alex",
    "user.email": "alex@example.com",
    "core.editor": "vim",
    "merge.tool": "meld",
    "push.default": "current",
    "pull.rebase": "false",
    "color.ui": "auto"
  }
}
```

**Final answer:**
**global Git configuration:**
- `user.name` = `Alex`
- `user.email` = `alex@example.com`
- `core.editor` = `vim`
- `merge.tool` = `meld`
- `push.default` = `current`
- `pull.rebase` = `false`
- `color.ui` = `auto`

**Чому tool кращий за retrieval:**
Git-конфігурація є персональною та динамічною. Кожен користувач має унікальні налаштування, що змінюються з часом. Статична база знань не може містити персональні дані конфігурації — лише інструмент, який запитує поточну конфігурацію, може надати точні результати.

### 6. Інтеграція з chatbot-ом

Шар інтеграції — функція `call_tool(name, input_data)` у `scripts/external_tool.py`:

```
chatbot → вибір tool-а → call_tool() → валідація → виконання tool-а → результат
```

**Послідовність виконання:**
1. **Вибір tool-а** — модель або router обирає tool за назвою
2. **Валідація** — перевірка обов'язкових полів, типів, enum-значень
3. **Виконання** — виклик функції tool-а (`func(**input_data)`)
4. **Результат** — повернення структурованого dict (успіх або помилка)

**Приклад виклику:**
```python
from scripts.external_tool import call_tool

result = call_tool("get_git_command", {"command": "push"})
# → {"command": "push", "full_command": "git push", ...}

result = call_tool("get_git_config", {"scope": "global", "key": "user.email"})
# → {"scope": "global", "key": "user.email", "value": "alex@example.com"}
```

**Підтримка LLM:**
Модель може отримати список доступних tool-ів через `list_tools()` і вибрати підходящий:
```python
from scripts.external_tool import list_tools, call_tool
import json

# Модель бачить доступні tool-и
tools = list_tools()
# Вибрано: get_git_command
result = call_tool("get_git_command", json.loads('{"command": "push"}'))
```

### 7. Висновки

Інтеграція зовнішніх tool-ів доповнює RAG pipeline:

- **Tool-и** — для структурованих, точних, динамічних даних (команди, конфігурація)
- **RAG retrieval** — для концептуальних питань, пояснень, прикладів з документації

Разом: `chatbot → вибір інструмента (структуровані дані) → RAG fallback (концептуальне) → відповідь`

### 8. Структура проєкту

```
rag-git/
├── scripts/
│   ├── external_tool.py      # HW5: реалізація tool-ів + інтеграція + валідація
│   ├── prepare_knowledge_base.py  # HW1: чанкінг
│   ├── retrieval.py           # HW2: semantic retrieval
│   ├── retrieval_improved.py  # HW3: hybrid BM25 + semantic
│   └── rag_answer.py          # HW4: RAG QA pipeline з LLM
├── outputs/
│   └── tool_examples.md       # HW5: приклади викликів tool-ів
├── data/
│   ├── raw/                   # 10 джерел документації
│   └── processed/
│       └── chunks.jsonl       # 145 чанків
├── .gitignore
└── README.md
```

## Критерії оцінювання

| Критерій | Бали | Статус |
|----------|------|--------|
| Tool описаний (назва, тип, мета, коли викликати) | 5 | ✅ 2 tool-и, повний опис |
| Input / output contract визначено | 10 | ✅ JSON schema + output structure |
| Validation реалізовано | 10 | ✅ Обов'язкові поля + тип + enum + формат |
| Tool реалізовано і запускається | 10 | ✅ `--demo`: 5/5 ✅ OK |
| 3–5 прикладів з поясненням переваги перед retrieval | 10 | ✅ 5 прикладів + пояснення |
| Виклик через шар інтеграції показано | 5 | ✅ `call_tool()` + `list_tools()` |
| **Разом** | **50** | |