## Example 1

**Query:** how do I stash my changes?

**Route:** `get_git_command`

**Tool called:** `get_git_command`

**Args:**
```json
{
  "command": "stash"
}
```

**Observation:**
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

**Synthesis:** Tool returned relevant data — summarizing for the user.

**Final answer:**
{
  "command": "stash",
  "synopsis": "git stash [push|pop|list|apply|drop] [<options>]",
  "description": "Temporarily shelf changes in a dirty working directory",
  "examples": [
    "git stash push -m 'work in progress'",
    "git stash pop"
  ]
}

## Example 2

**Query:** how do I rebase onto main?

**Route:** `get_git_command`

**Tool called:** `get_git_command`

**Args:**
```json
{
  "command": "rebase"
}
```

**Observation:**
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

**Synthesis:** Tool returned relevant data — summarizing for the user.

**Final answer:**
{
  "command": "rebase",
  "synopsis": "git rebase [<options>] [<branch>]",
  "description": "Forward-port local commits to the updated upstream head",
  "examples": [
    "git rebase main",
    "git rebase -i HEAD~3"
  ]
}

## Example 3

**Query:** what is my git user.name?

**Route:** `get_git_config`

**Tool called:** `get_git_config`

**Args:**
```json
{
  "scope": "global"
}
```

**Observation:**
```json
{
  "scope": "global",
  "settings": {
    "user.name": "Alex21141",
    "user.email": "alex21141@gmail.com"
  }
}
```

**Synthesis:** Tool returned relevant data — summarizing for the user.

**Final answer:**
{
  "scope": "global",
  "settings": {
    "user.name": "Alex21141",
    "user.email": "alex21141@gmail.com"
  }
}

## Example 4

**Query:** how do I clone a repo with shallow history?

**Route:** `get_git_command`

**Tool called:** `get_git_command`

**Args:**
```json
{
  "command": "clone"
}
```

**Observation:**
```json
{
  "command": "clone",
  "synopsis": "git clone <repository> [directory]",
  "description": "Clone a repository into a new directory",
  "examples": [
    "git clone https://github.com/user/repo.git",
    "git clone --depth=1 <url>"
  ]
}
```

**Synthesis:** Tool returned relevant data — summarizing for the user.

**Final answer:**
{
  "command": "clone",
  "synopsis": "git clone <repository> [directory]",
  "description": "Clone a repository into a new directory",
  "examples": [
    "git clone https://github.com/user/repo.git",
    "git clone --depth=1 <url>"
  ]
}

## Example 5

**Query:** show me recent commits graph

**Route:** `get_git_command`

**Tool called:** `get_git_command`

**Args:**
```json
{
  "command": "commit"
}
```

**Observation:**
```json
{
  "command": "commit",
  "synopsis": "git commit [<options>] [<pathspec>\u2026]",
  "description": "Record changes to the repository",
  "examples": [
    "git commit -m 'fix: resolve issue #42'",
    "git commit --amend"
  ]
}
```

**Synthesis:** Tool returned relevant data — summarizing for the user.

**Final answer:**
{
  "command": "commit",
  "synopsis": "git commit [<options>] [<pathspec>\u2026]",
  "description": "Record changes to the repository",
  "examples": [
    "git commit -m 'fix: resolve issue #42'",
    "git commit --amend"
  ]
}

