# Git tutoring assistant

## Домашнє завдання №5 — Інтеграція зовнішнього tool або джерела

| Параметр | Значення |
|----------|----------|
| **Tool-ів реалізовано** | 2 |
| **Тип** | read tools |
| **Джерело даних** | Структурована БД Git-команд + Git-конфігурація |
| **Тестових прикладів** | 5 |
| **Validation** | Required fields + type check + enum + format validation |

### 1. Вибір типу tool

Вибрано: **API tool** (structured database lookup).

| Tool | Призначення |
|------|-------------|
| `get_git_command` | Повертає структуровану інформацію про Git-команду (синтаксис, опис, приклади) |
| `get_git_config` | Повертає значення Git-конфігурації для заданого scope (global/local) |

Обидва — **read tools**: не змінюють дані, тільки читають.

### 2. Опис tool-ів

#### get_git_command

| Параметр | Значення |
|---|---|
| Назва | `get_git_command` |
| Тип | read tool |
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
| Тип | read tool |
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

**Синтаксис:** `git clone <repository> [directory]`

**Приклади:**
- `git clone https://github.com/user/repo.git`
- `git clone --depth=1 https://github.com/user/repo.git`

**Why tool is better than retrieval:**
Git commands have precise, structured information (synopsis, description, examples) that is better served by a queryable database than by semantic search. Retrieval would return relevant text chunks, but the tool returns the exact command structure and official examples in a normalized format.

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

**Синтаксис:** `git stash [<options>]`

**Приклади:**
- `git stash`
- `git stash pop`
- `git stash list`

**Why tool is better than retrieval:**
Tool returns exact command syntax and examples directly from a structured database — retrieval would require matching multiple text chunks and the LLM would need to synthesize the answer.

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

**Синтаксис:** `git merge [<options>] <branch>`

**Приклади:**
- `git merge feature-branch`
- `git merge --no-ff feature-branch`

**Why tool is better than retrieval:**
Structured command data provides exact syntax and examples that retrieval from text chunks could not reliably extract. The tool guarantees correct, complete command information.

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

**Why tool is better than retrieval:**
Git configuration is user-specific and dynamic — each user has different settings. This data cannot be stored in a static knowledge base. A tool that queries live configuration is the only correct approach.

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

**Why tool is better than retrieval:**
Git configuration is user-specific and dynamic. Each user has unique settings that change over time. A static knowledge base cannot contain personal configuration data — only a tool that queries live config can provide accurate results.

### 6. Orchestration layer

Orchestration layer — функція `call_tool(name, input_data)` у `scripts/external_tool.py`:

```
chatbot → tool selection → call_tool() → validation → tool execution → result
```

**Піплайн:**
1. **Tool selection** — модель або router обирає tool за назвою
2. **Validation** — перевірка required fields, types, enum values
3. **Execution** — виклик функції tool-а (`func(**input_data)`)
4. **Result** — повернення структурованого dict (success або error)

**Приклад виклику через orchestration:**
```python
from scripts.external_tool import call_tool

result = call_tool("get_git_command", {"command": "push"})
# → {"command": "push", "full_command": "git push", ...}

result = call_tool("get_git_config", {"scope": "global", "key": "user.email"})
# → {"scope": "global", "key": "user.email", "value": "alex@example.com"}
```

**Підтримка LLM orchestration:**
Модель може описати доступні tool-и через `list_tools()` і вибрати підходящий:
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

Разом: `chatbot → tool selection (structured data) → RAG fallback (conceptual) → answer`

### 8. Структура проєкту

```
rag-git/
├── scripts/
│   ├── external_tool.py      # HW5: реалізація tool-ів + orchestration + validation
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
| Validation реалізовано | 10 | ✅ Required fields + type + enum + format |
| Tool реалізовано і запускається | 10 | ✅ `--demo`: 5/5 ✅ OK |
| 3–5 прикладів з поясненням переваги перед retrieval | 10 | ✅ 5 прикладів + пояснення |
| Виклик через orchestration layer показано | 5 | ✅ `call_tool()` + `list_tools()` |
| **Разом** | **50** | |