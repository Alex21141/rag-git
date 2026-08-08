# HW5: Інтеграція зовнішнього tool — Приклади викликів

**Tool-ів зареєстровано**: 2

**Тестових прикладів**: 5

## Зареєстровані tool-и

- **`get_git_command`** — Get structured information about a Git command (synopsis, description, examples). Use when user asks about a specific git command or 'how do I X'.
- **`get_git_config`** — Get Git configuration values for a given scope (global or local). Use when user asks about their git settings or configuration.

## Опис tool-ів

### 1. get_git_command

| Параметр | Значення |
|---|---|
| Тип | read tool |
| Мета | Повертає структуровану інформацію про Git-команду (синтаксис, опис, приклади) |
| Коли викликати | Користувач запитує 'як зробити X' або 'що робить git X' |
| Коли НЕ викликати | Концептуальні питання ('що таке merge conflict?') — використовувати RAG |

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
  "required": [
    "command"
  ]
}
```


### 2. get_git_config

| Параметр | Значення |
|---|---|
| Тип | read tool |
| Мета | Повертає значення Git-конфігурації для заданого scope (global/local) |
| Коли викликати | Користувач запитує про свої налаштування git |
| Коли НЕ викликати | Запитання про використання git-команд — використовувати get_git_command |

**Input schema:**
```json

{
  "type": "object",
  "properties": {
    "scope": {
      "type": "string",
      "description": "Config scope: 'global' or 'local'",
      "enum": [
        "global",
        "local"
      ]
    },
    "key": {
      "type": "string",
      "description": "Optional specific config key (e.g., 'user.email', 'push.default'). Omit to get all settings."
    }
  },
  "required": [
    "scope"
  ]
}
```


## Приклад 1

**User question:** How do I clone a Git repository?

**Tool called:** `get_git_command`

**Input:** ```json
{
  "command": "clone"
}
```

**Result:** ```json
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

**Чому tool кращий за retrieval:**
Git-команди мають точну структуровану інформацію (синтаксис, опис, приклади), яку краще надавати через запитуючу базу даних, ніж через семантичний пошук. Retrieval повернув би релевантні текстові чанки, а tool повертає точну структуру команди та офіційні приклади у нормалізованому форматі.

## Приклад 2

**User question:** What does git stash do?

**Tool called:** `get_git_command`

**Input:** ```json
{
  "command": "stash"
}
```

**Result:** ```json
{
  "command": "stash",
  "full_command": "git stash",
  "synopsis": "git stash [<options>]",
  "description": "Temporarily save changes and revert to the HEAD commit. Useful for quickly switching branches without committing.",
  "examples": [
    "git stash",
    "git stash pop",
    "git stash list"
  ]
}
```

**Final answer:**
`git stash` — Temporarily save changes and revert to the HEAD commit. Useful for quickly switching branches without committing.

**Синтаксис:** `git stash [<options>]`

**Приклади:**
- `git stash`
- `git stash pop`
- `git stash list`

**Чому tool кращий за retrieval:**
Git-команди мають точну структуровану інформацію (синтаксис, опис, приклади), яку краще надавати через запитуючу базу даних, ніж через семантичний пошук. Retrieval повернув би релевантні текстові чанки, а tool повертає точну структуру команди та офіційні приклади у нормалізованому форматі.

## Приклад 3

**User question:** How do I resolve a merge conflict?

**Tool called:** `get_git_command`

**Input:** ```json
{
  "command": "merge"
}
```

**Result:** ```json
{
  "command": "merge",
  "full_command": "git merge",
  "synopsis": "git merge [<options>] <branch>",
  "description": "Join two branches together. Integrates changes from the specified branch into the current branch.",
  "examples": [
    "git merge feature-branch",
    "git merge --no-ff feature-branch"
  ]
}
```

**Final answer:**
`git merge` — Join two branches together. Integrates changes from the specified branch into the current branch.

**Синтаксис:** `git merge [<options>] <branch>`

**Приклади:**
- `git merge feature-branch`
- `git merge --no-ff feature-branch`

**Чому tool кращий за retrieval:**
Git-команди мають точну структуровану інформацію (синтаксис, опис, приклади), яку краще надавати через запитуючу базу даних, ніж через семантичний пошук. Retrieval повернув би релевантні текстові чанки, а tool повертає точну структуру команди та офіційні приклади у нормалізованому форматі.

## Приклад 4

**User question:** What is my git username?

**Tool called:** `get_git_config`

**Input:** ```json
{
  "scope": "global",
  "key": "user.name"
}
```

**Result:** ```json
{
  "scope": "global",
  "key": "user.name",
  "value": "Alex"
}
```

**Final answer:**
**global `user.name`** = `Alex`

**Чому tool кращий за retrieval:**
Git-конфігурація є персональною та динамічною — кожен користувач має різні налаштування. Ці дані неможливо зберігати в статичній knowledge base. Tool, який запитує поточну конфігурацію — єдиний правильний підхід.

## Приклад 5

**User question:** Show me all my global git settings

**Tool called:** `get_git_config`

**Input:** ```json
{
  "scope": "global"
}
```

**Result:** ```json
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
Git-конфігурація є персональною та динамічною — кожен користувач має різні налаштування. Ці дані неможливо зберігати в статичній knowledge base. Tool, який запитує поточну конфігурацію — єдиний правильний підхід.
