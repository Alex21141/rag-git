## Example 1

Question: how do I stash my changes?

Route: command_workflow

Tool called: get_git_command

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
  "description": "Temporarily shelf changes in a dirty working directory",
  "examples": [
    "git stash push -m 'work in progress'",
    "git stash pop"
  ]
}
```

State after step:

- Step 1 (Route): `{"user_goal": "how do I stash my changes?", "selected_route": "command_workflow", "tool_calls": [], "observations": [], "final_answer": null}`
- Step 2 (Execute): `{"user_goal": "how do I stash my changes?", "selected_route": "command_workflow", "tool_calls": [{"name": "get_git_command", "args": {"command": "stash"}}], "observations": ["{\n  \"command\": \"stash\",\n  \"synopsis\": \"git stash [push|pop|list|apply|drop] [<options>]\",\n  \"description\": \"Temporarily shelf changes in a dirty working directo…"], "final_answer": null}`
- Step 3 (Synthesize): `{"user_goal": "how do I stash my changes?", "selected_route": "command_workflow", "tool_calls": [{"name": "get_git_command", "args": {"command": "stash"}}], "observations": ["{\n  \"command\": \"stash\",\n  \"synopsis\": \"git stash [push|pop|list|apply|drop] [<options>]\",\n  \"description\": \"Temporarily shelf changes in a dirty working directo…"], "final_answer": "Використовуйте: `git stash [push|pop|list|apply|drop] [<options>]`.\nПризначення: Temporarily shelf changes in a dirty wo"}`

Final answer:
Використовуйте: `git stash [push|pop|list|apply|drop] [<options>]`.
Призначення: Temporarily shelf changes in a dirty working directory.
Приклади:
- `git stash push -m 'work in progress'`
- `git stash pop`

---

## Example 2

Question: how do I rebase onto main?

Route: command_workflow

Tool called: get_git_command

Args:
```json
{
  "command": "rebase"
}
```

Observation:
```json
{
  "command": "rebase",
  "synopsis": "git rebase [<options>] [<branch>]",
  "description": "Forward-port local commits to the updated upstream head",
  "examples": [
    "git rebase main",
    "git rebase -i HEAD~3"
  ]
}
```

State after step:

- Step 1 (Route): `{"user_goal": "how do I rebase onto main?", "selected_route": "command_workflow", "tool_calls": [], "observations": [], "final_answer": null}`
- Step 2 (Execute): `{"user_goal": "how do I rebase onto main?", "selected_route": "command_workflow", "tool_calls": [{"name": "get_git_command", "args": {"command": "rebase"}}], "observations": ["{\n  \"command\": \"rebase\",\n  \"synopsis\": \"git rebase [<options>] [<branch>]\",\n  \"description\": \"Forward-port local commits to the updated upstream head\",\n  \"examp…"], "final_answer": null}`
- Step 3 (Synthesize): `{"user_goal": "how do I rebase onto main?", "selected_route": "command_workflow", "tool_calls": [{"name": "get_git_command", "args": {"command": "rebase"}}], "observations": ["{\n  \"command\": \"rebase\",\n  \"synopsis\": \"git rebase [<options>] [<branch>]\",\n  \"description\": \"Forward-port local commits to the updated upstream head\",\n  \"examp…"], "final_answer": "Використовуйте: `git rebase [<options>] [<branch>]`.\nПризначення: Forward-port local commits to the updated upstream hea"}`

Final answer:
Використовуйте: `git rebase [<options>] [<branch>]`.
Призначення: Forward-port local commits to the updated upstream head.
Приклади:
- `git rebase main`
- `git rebase -i HEAD~3`

---

## Example 3

Question: what is my git user.name?

Route: config_workflow

Tool called: get_git_config

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

State after step:

- Step 1 (Route): `{"user_goal": "what is my git user.name?", "selected_route": "config_workflow", "tool_calls": [], "observations": [], "final_answer": null}`
- Step 2 (Execute): `{"user_goal": "what is my git user.name?", "selected_route": "config_workflow", "tool_calls": [{"name": "get_git_config", "args": {"scope": "global"}}], "observations": ["{\n  \"scope\": \"global\",\n  \"settings\": {\n    \"user.name\": \"Alex21141\",\n    \"user.email\": \"alex21141@gmail.com\"\n  }\n}"], "final_answer": null}`
- Step 3 (Synthesize): `{"user_goal": "what is my git user.name?", "selected_route": "config_workflow", "tool_calls": [{"name": "get_git_config", "args": {"scope": "global"}}], "observations": ["{\n  \"scope\": \"global\",\n  \"settings\": {\n    \"user.name\": \"Alex21141\",\n    \"user.email\": \"alex21141@gmail.com\"\n  }\n}"], "final_answer": "Налаштування git (scope: global):\n- `user.name` = `Alex21141`\n- `user.email` = `alex21141@gmail.com`"}`

Final answer:
Налаштування git (scope: global):
- `user.name` = `Alex21141`
- `user.email` = `alex21141@gmail.com`

---

## Example 4

Question: show me recent commits graph

Route: command_workflow

Tool called: get_git_command

Args:
```json
{
  "command": "log"
}
```

Observation:
```json
{
  "command": "log",
  "synopsis": "git log [<options>] [<revision range>]",
  "description": "Show commit logs",
  "examples": [
    "git log --oneline -10",
    "git log --graph --all --oneline"
  ]
}
```

State after step:

- Step 1 (Route): `{"user_goal": "show me recent commits graph", "selected_route": "command_workflow", "tool_calls": [], "observations": [], "final_answer": null}`
- Step 2 (Execute): `{"user_goal": "show me recent commits graph", "selected_route": "command_workflow", "tool_calls": [{"name": "get_git_command", "args": {"command": "log"}}], "observations": ["{\n  \"command\": \"log\",\n  \"synopsis\": \"git log [<options>] [<revision range>]\",\n  \"description\": \"Show commit logs\",\n  \"examples\": [\n    \"git log --oneline -10\",\n…"], "final_answer": null}`
- Step 3 (Synthesize): `{"user_goal": "show me recent commits graph", "selected_route": "command_workflow", "tool_calls": [{"name": "get_git_command", "args": {"command": "log"}}], "observations": ["{\n  \"command\": \"log\",\n  \"synopsis\": \"git log [<options>] [<revision range>]\",\n  \"description\": \"Show commit logs\",\n  \"examples\": [\n    \"git log --oneline -10\",\n…"], "final_answer": "Використовуйте: `git log [<options>] [<revision range>]`.\nПризначення: Show commit logs.\nПриклади:\n- `git log --oneline "}`

Final answer:
Використовуйте: `git log [<options>] [<revision range>]`.
Призначення: Show commit logs.
Приклади:
- `git log --oneline -10`
- `git log --graph --all --oneline`

---

## Example 5

Question: what is the best pizza recipe?

Route: clarification

State after step:

- Step 1 (Route): `{"user_goal": "what is the best pizza recipe?", "selected_route": "clarification", "tool_calls": [], "observations": [], "final_answer": null}`
- Step 2 (Execute): `{"user_goal": "what is the best pizza recipe?", "selected_route": "clarification", "tool_calls": [], "observations": [], "final_answer": null}`
- Step 3 (Synthesize): `{"user_goal": "what is the best pizza recipe?", "selected_route": "clarification", "tool_calls": [], "observations": [], "final_answer": "Уточніть, будь ласка: ви питаєте про git-команду (наприклад, 'як зробити rebase?') чи про налаштування git (наприклад, '"}`

Final answer:
Уточніть, будь ласка: ви питаєте про git-команду (наприклад, 'як зробити rebase?') чи про налаштування git (наприклад, 'яке у мене user.name?').

---

