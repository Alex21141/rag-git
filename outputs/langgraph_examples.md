# HW7 — LangGraph workflow: 3 test examples

Domain: Git command reference and configuration

Graph: `classify_request` → (conditional edge) → `command_workflow` | `config_workflow` | `clarification` → `build_answer` → END

## Example 1

Input question: how do I stash my changes?

Selected route: `command_workflow`

Executed nodes: classify_request → command_workflow → build_answer

Tool called: `get_git_command`

Args:
```json
{
  "command": "stash"
}
```

Observation:
```json
{
  "command": "stash",
  "synopsis": "git stash [push|pop|list|apply|drop] [<options>]",
  "description": "Temporarily shelf changes in a dirty working directo…
```

Final state:

```json
{
  "user_goal": "how do I stash my changes?",
  "selected_route": "command_workflow",
  "tool_calls": [
    {
      "name": "get_git_command",
      "args": {
        "command": "stash"
      }
    }
  ],
  "observations": [
    "{\n  \"command\": \"stash\",\n  \"synopsis\": \"git stash [push|pop|list|apply|drop] [<options>]\",\n  \"description\": \"Temporarily shelf changes in a dirty working directo…"
  ],
  "final_answer": "Використовуйте: `git stash [push|pop|list|apply|drop] [<options>]`.\nПризначення: Temporarily shelf changes in a dirty working directory.\nПриклади:\n- `git stash push -m 'work in progress'`\n- `git stash pop`"
}
```

Final answer:
Використовуйте: `git stash [push|pop|list|apply|drop] [<options>]`.
Призначення: Temporarily shelf changes in a dirty working directory.
Приклади:
- `git stash push -m 'work in progress'`
- `git stash pop`

---

## Example 2

Input question: what is my git user.name?

Selected route: `config_workflow`

Executed nodes: classify_request → config_workflow → build_answer

Tool called: `get_git_config`

Args:
```json
{
  "scope": "global"
}
```

Observation:
```json
{
  "scope": "global",
  "settings": {
    "user.name": "Alex21141",
    "user.email": "alex21141@gmail.com"
  }
}
```

Final state:

```json
{
  "user_goal": "what is my git user.name?",
  "selected_route": "config_workflow",
  "tool_calls": [
    {
      "name": "get_git_config",
      "args": {
        "scope": "global"
      }
    }
  ],
  "observations": [
    "{\n  \"scope\": \"global\",\n  \"settings\": {\n    \"user.name\": \"Alex21141\",\n    \"user.email\": \"alex21141@gmail.com\"\n  }\n}"
  ],
  "final_answer": "Налаштування git (scope: global):\n- `user.name` = `Alex21141`\n- `user.email` = `alex21141@gmail.com`"
}
```

Final answer:
Налаштування git (scope: global):
- `user.name` = `Alex21141`
- `user.email` = `alex21141@gmail.com`

---

## Example 3

Input question: what is the best pizza recipe?

Selected route: `clarification`

Executed nodes: classify_request → clarification

Final state:

```json
{
  "user_goal": "what is the best pizza recipe?",
  "selected_route": "clarification",
  "tool_calls": [],
  "observations": [],
  "final_answer": "Уточніть, будь ласка: ви питаєте про git-команду (наприклад, 'як зробити rebase?') чи про налаштування git (наприклад, 'яке у мене user.name?')."
}
```

Final answer:
Уточніть, будь ласка: ви питаєте про git-команду (наприклад, 'як зробити rebase?') чи про налаштування git (наприклад, 'яке у мене user.name?').

---

