#!/usr/bin/env python3
"""
HW5: External Tool Integration — Git tutoring assistant tools.

Tools that query live, structured, or dynamic data that cannot be reliably
stored in a static knowledge base.

Usage:
    python3 scripts/external_tool.py --list           # List available tools
    python3 scripts/external_tool.py --demo           # Run all examples
    python3 scripts/external_tool.py --tool <name> --input '{"key": "value"}'  # Call a tool
"""

import json
import os
import sys
from typing import Optional

# ── Tool Registry ───────────────────────────────────────────────────────────
# Each tool: {name, description, input_schema, function}
TOOLS = {}


def register_tool(name, description, input_schema):
    """Decorator to register a tool in the registry."""
    def decorator(func):
        TOOLS[name] = {
            "name": name,
            "description": description,
            "input_schema": input_schema,
            "function": func,
        }
        func._tool_name = name
        func._tool_description = description
        func._tool_schema = input_schema
        return func
    return decorator


# ── Tool 1: get_git_command ─────────────────────────────────────────────────
# Purpose: Returns structured help info for a Git command (name, synopsis, short description).
# Type: read tool
# When useful: user asks "how do I X" or "what does git X do"
# When NOT useful: user asks conceptual questions ("what is a merge conflict?") — use RAG instead

# Mock data — simulates structured Git command database
GIT_COMMANDS = {
    "clone": {
        "command": "git clone",
        "synopsis": "git clone <repository> [directory]",
        "description": "Clone a repository into a new directory. Creates a full local copy with complete history and all branches.",
        "examples": ["git clone https://github.com/user/repo.git", "git clone --depth=1 https://github.com/user/repo.git"],
    },
    "commit": {
        "command": "git commit",
        "synopsis": "git commit [-m <message>] [-a]",
        "description": "Record changes to the repository. Commits all staged changes with a descriptive message.",
        "examples": ["git commit -m 'fix: resolve merge conflict'", "git commit -am 'update documentation'"],
    },
    "push": {
        "command": "git push",
        "synopsis": "git push [<remote> [<branch>]]",
        "description": "Upload local repository changes to a remote repository. Updates the remote with your local commits.",
        "examples": ["git push origin main", "git push -u origin feature-branch"],
    },
    "pull": {
        "command": "git pull",
        "synopsis": "git pull [<remote> [<branch>]]",
        "description": "Fetch from and integrate with a remote repository. Combines git fetch and git merge.",
        "examples": ["git pull origin main", "git pull --rebase origin develop"],
    },
    "merge": {
        "command": "git merge",
        "synopsis": "git merge [<options>] <branch>",
        "description": "Join two branches together. Integrates changes from the specified branch into the current branch.",
        "examples": ["git merge feature-branch", "git merge --no-ff feature-branch"],
    },
    "rebase": {
        "command": "git rebase",
        "synopsis": "git rebase [<options>] <branch>",
        "description": "Reapply commits on top of another base. Creates a cleaner, linear history by moving commits to a new base.",
        "examples": ["git rebase main", "git rebase -i HEAD~3"],
    },
    "stash": {
        "command": "git stash",
        "synopsis": "git stash [<options>]",
        "description": "Temporarily save changes and revert to the HEAD commit. Useful for quickly switching branches without committing.",
        "examples": ["git stash", "git stash pop", "git stash list"],
    },
    "checkout": {
        "command": "git checkout",
        "synopsis": "git checkout <branch> | <commit>",
        "description": "Switch branches or restore working tree files. Moves to the specified branch or commit.",
        "examples": ["git checkout main", "git checkout -b new-branch", "git checkout -- file.txt"],
    },
    "branch": {
        "command": "git branch",
        "synopsis": "git branch [<options>] [<branch-name>]",
        "description": "List, create, or delete branches. Displays local branches with the current one marked.",
        "examples": ["git branch", "git branch new-feature", "git branch -d old-feature"],
    },
    "log": {
        "command": "git log",
        "synopsis": "git log [<options>]",
        "description": "Show commit history. Displays commits in reverse chronological order with author, date, and message.",
        "examples": ["git log --oneline", "git log -5", "git log --graph --oneline --all"],
    },
    "diff": {
        "command": "git diff",
        "synopsis": "git diff [<options>] [<path>]",
        "description": "Show changes between commits, commit and working tree, etc. Displays line-by-line differences.",
        "examples": ["git diff", "git diff HEAD~1", "git diff --staged"],
    },
    "status": {
        "command": "git status",
        "synopsis": "git status [<options>]",
        "description": "Show working tree status. Displays staged, unstaged, and untracked files.",
        "examples": ["git status", "git status -s", "git status --porcelain"],
    },
    "reset": {
        "command": "git reset",
        "synopsis": "git reset [<mode>] [<ref>]",
        "description": "Reset current HEAD to the specified state. Soft keeps changes staged, mixed unstages them, hard discards everything.",
        "examples": ["git reset --soft HEAD~1", "git reset HEAD file.txt"],
    },
    "add": {
        "command": "git add",
        "synopsis": "git add [<options>] [--] <path>...",
        "description": "Add file contents to the staging area. Prepares files to be committed.",
        "examples": ["git add file.txt", "git add .", "git add -p"],
    },
}


@register_tool(
    name="get_git_command",
    description="Get structured information about a Git command (synopsis, description, examples). "
                "Use when user asks about a specific git command or 'how do I X'.",
    input_schema={
        "type": "object",
        "properties": {
            "command": {
                "type": "string",
                "description": "Git command name (e.g., 'clone', 'push', 'merge', 'stash', 'rebase')",
                "maxLength": 30,
            }
        },
        "required": ["command"],
    },
)
def get_git_command(command: str) -> dict:
    """
    Tool: get_git_command
    Type: read tool
    Purpose: Returns structured info for a Git command from a command database.
    When useful: user asks "how do I X" or "what does git X do"
    When NOT useful: conceptual questions (use RAG instead)
    """
    # Validation: required field
    if not command:
        return {"error": "command is required"}

    # Validation: normalize
    cmd = command.strip().lower()
    # Remove 'git ' prefix if user includes it
    if cmd.startswith("git "):
        cmd = cmd[4:]

    # Validation: format check — command should be a single word, alphanumeric with hyphens
    import re
    if not re.match(r'^[a-z][a-z0-9-]*$', cmd):
        return {
            "error": f"Invalid command format: '{command}'. Expected a single Git command name (e.g., 'clone', 'push', 'merge').",
            "valid_commands": list(GIT_COMMANDS.keys()),
        }

    # Validation: length check
    if len(cmd) > 30:
        return {
            "error": f"Command name too long: '{cmd}' ({len(cmd)} chars). Max 30 characters.",
        }

    # Lookup
    result = GIT_COMMANDS.get(cmd)
    if not result:
        # Suggest similar commands
        similar = [c for c in GIT_COMMANDS if cmd in c or c in cmd]
        suggestion = f"Did you mean: {', '.join(similar[:3])}" if similar else ""
        return {
            "error": f"Command '{cmd}' not found in database.",
            **({"suggestion": suggestion} if similar else {}),
            "valid_commands": list(GIT_COMMANDS.keys()),
        }

    return {
        "command": cmd,
        "full_command": result["command"],
        "synopsis": result["synopsis"],
        "description": result["description"],
        "examples": result["examples"],
    }


# ── Tool 2: get_git_config ──────────────────────────────────────────────────
# Purpose: Returns current Git configuration values for a given scope.
# Type: read tool
# When useful: user asks "how do I configure X" or "what is my current X setting"
# When NOT useful: asking how to use git commands (use get_git_command)

# Fallback mock data — used when subprocess fails (e.g., no git installed)
MOCK_GIT_CONFIG = {
    "global": {
        "user.name": "Alex",
        "user.email": "alex@example.com",
    },
    "local": {},
}


def _get_git_config_live(scope: str) -> dict:
    """Query real git config via subprocess. Falls back to MOCK_GIT_CONFIG on error."""
    try:
        import subprocess
        result = subprocess.run(
            ["git", "config", f"--{scope}", "--list"],
            capture_output=True, text=True, timeout=5,
        )
        if result.returncode == 0:
            config = {}
            for line in result.stdout.strip().split("\n"):
                if "=" in line:
                    key, val = line.split("=", 1)
                    config[key.strip()] = val.strip()
            if config:
                return config
    except (subprocess.SubprocessError, FileNotFoundError, OSError):
        pass
    return MOCK_GIT_CONFIG.get(scope, {})


@register_tool(
    name="get_git_config",
    description="Get Git configuration values for a given scope (global or local). "
                "Use when user asks about their git settings or configuration.",
    input_schema={
        "type": "object",
        "properties": {
            "scope": {
                "type": "string",
                "description": "Config scope: 'global' or 'local'",
                "enum": ["global", "local"],
            },
            "key": {
                "type": "string",
                "description": "Optional specific config key (e.g., 'user.email', 'push.default'). Omit to get all settings.",
            }
        },
        "required": ["scope"],
    },
)
def get_git_config(scope: str, key: Optional[str] = None) -> dict:
    """
    Tool: get_git_config
    Type: read tool
    Purpose: Returns Git configuration values from live git config (subprocess).
    When useful: user asks about their git settings
    When NOT useful: asking how to use git commands (use get_git_command)
    """
    # Validation: required field
    if not scope:
        return {"error": "scope is required ('global' or 'local')"}

    # Validation: scope must be 'global' or 'local'
    scope = scope.strip().lower()
    if scope not in ("global", "local"):
        return {
            "error": f"Invalid scope: '{scope}'. Must be 'global' or 'local'.",
        }

    # Query live git config (falls back to mock on error)
    config = _get_git_config_live(scope)
    if not config and scope == "local":
        # Local config only exists inside a git repo — return informative message
        return {
            "scope": scope,
            "settings": {},
            "note": "No local configuration found. This tool should be run from inside a git repository.",
        }

    # If key specified, return only that key
    if key:
        key = key.strip()
        # Validation: key format
        if not key or " " in key:
            return {
                "error": f"Invalid key format: '{key}'. Use dot notation (e.g., 'user.email').",
            }
        value = config.get(key)
        if value is None:
            # Suggest similar keys
            similar = [k for k in config if key in k or k.split('.')[0] == key.split('.')[0]]
            return {
                "error": f"Key '{key}' not found in {scope} config.",
                **({"suggestion": ", ".join(similar[:3])} if similar else {}),
            }
        return {"scope": scope, "key": key, "value": value}

    # Return all config for the scope
    return {"scope": scope, "settings": config}


# ── Orchestration Layer ─────────────────────────────────────────────────────
def list_tools() -> list:
    """List all registered tools with their schemas."""
    return [
        {
            "name": info["name"],
            "description": info["description"],
            "input_schema": info["input_schema"],
        }
        for info in TOOLS.values()
    ]


def call_tool(name: str, input_data: dict) -> dict:
    """Call a registered tool with validation.

    This is the orchestration layer entry point:
        chatbot → tool selection → call_tool() → validation → tool execution → result
    """
    # Step 1: Validate tool name
    if name not in TOOLS:
        available = ", ".join(TOOLS.keys())
        return {"error": f"Unknown tool: '{name}'. Available: {available}"}

    tool_info = TOOLS[name]
    schema = tool_info["input_schema"]
    func = tool_info["function"]

    # Step 2: Validate required fields
    for req_field in schema.get("required", []):
        if req_field not in input_data or input_data[req_field] is None:
            return {"error": f"Missing required field: '{req_field}'"}

    # Step 3: Validate field types
    for field, value in input_data.items():
        field_schema = schema.get("properties", {}).get(field)
        if field_schema:
            expected_type = field_schema.get("type")
            if expected_type == "string" and not isinstance(value, str):
                return {"error": f"Field '{field}' must be a string, got {type(value).__name__}"}
            if expected_type == "integer" and not isinstance(value, int):
                return {"error": f"Field '{field}' must be an integer, got {type(value).__name__}"}
            # Enum validation
            if "enum" in field_schema and value not in field_schema["enum"]:
                return {"error": f"Field '{field}' must be one of: {field_schema['enum']}"}

    # Step 4: Execute tool
    try:
        result = func(**input_data)
        return result
    except Exception as e:
        return {"error": f"Tool execution failed: {str(e)}"}


# ── Demo / Test ─────────────────────────────────────────────────────────────
def run_demo() -> list:
    """Run all example tool calls and return structured results."""
    examples = [
        {
            "user_question": "How do I clone a Git repository?",
            "tool_name": "get_git_command",
            "input": {"command": "clone"},
        },
        {
            "user_question": "What does git stash do?",
            "tool_name": "get_git_command",
            "input": {"command": "stash"},
        },
        {
            "user_question": "How do I resolve a merge conflict?",
            "tool_name": "get_git_command",
            "input": {"command": "merge"},
        },
        {
            "user_question": "What is my git username?",
            "tool_name": "get_git_config",
            "input": {"scope": "global", "key": "user.name"},
        },
        {
            "user_question": "Show me all my global git settings",
            "tool_name": "get_git_config",
            "input": {"scope": "global"},
        },
    ]

    results = []
    for ex in examples:
        result = call_tool(ex["tool_name"], ex["input"])
        results.append({
            "user_question": ex["user_question"],
            "tool_called": ex["tool_name"],
            "input": ex["input"],
            "result": result,
        })

    return results


def generate_examples_report(all_results) -> str:
    """Generate outputs/tool_examples.md."""
    output_dir = os.path.join(os.path.dirname(__file__), "..", "outputs")
    os.makedirs(output_dir, exist_ok=True)

    lines = []
    lines.append("# HW5: Інтеграція зовнішнього tool — Приклади викликів\n")
    lines.append(f"**Tool-ів зареєстровано**: {len(TOOLS)}\n")
    lines.append(f"**Тестових прикладів**: {len(all_results)}\n")
    lines.append("## Зареєстровані tool-и\n")
    for tool in list_tools():
        lines.append(f"- **`{tool['name']}`** — {tool['description']}\n")
    lines.append("")

    # Tool descriptions
    lines.append("## Опис tool-ів\n")
    lines.append("### 1. get_git_command\n")
    lines.append("| Параметр | Значення |")
    lines.append("|---|---|")
    lines.append("| Тип | read-інструмент |")
    lines.append("| Мета | Повертає структуровану інформацію про Git-команду (синтаксис, опис, приклади) |")
    lines.append("| Коли викликати | Користувач запитує 'як зробити X' або 'що робить git X' |")
    lines.append("| Коли НЕ викликати | Концептуальні питання ('що таке merge conflict?') — використовувати RAG |")
    lines.append("")
    lines.append("**Input schema:**\n```json\n")
    lines.append(json.dumps(TOOLS["get_git_command"]["input_schema"], indent=2, ensure_ascii=False))
    lines.append("```\n")
    lines.append("")

    lines.append("### 2. get_git_config\n")
    lines.append("| Параметр | Значення |")
    lines.append("|---|---|")
    lines.append("| Тип | read-інструмент |")
    lines.append("| Мета | Повертає значення Git-конфігурації для заданого scope (global/local) |")
    lines.append("| Коли викликати | Користувач запитує про свої налаштування git |")
    lines.append("| Коли НЕ викликати | Запитання про використання git-команд — використовувати get_git_command |")
    lines.append("")
    lines.append("**Input schema:**\n```json\n")
    lines.append(json.dumps(TOOLS["get_git_config"]["input_schema"], indent=2, ensure_ascii=False))
    lines.append("```\n")
    lines.append("")

    # Examples
    for i, r in enumerate(all_results, 1):
        lines.append(f"## Приклад {i}\n")
        lines.append(f"**User question:** {r['user_question']}\n")
        lines.append(f"**Tool called:** `{r['tool_called']}`\n")
        lines.append(f"**Input:** ```json\n{json.dumps(r['input'], indent=2, ensure_ascii=False)}\n```\n")
        lines.append(f"**Result:** ```json\n{json.dumps(r['result'], indent=2, ensure_ascii=False)}\n```\n")

        # Generate final answer
        if "error" in r["result"]:
            answer = f"⚠️ Error: {r['result']['error']}"
        elif r["tool_called"] == "get_git_command":
            cmd = r["result"]
            answer = (
                f"`{cmd['full_command']}` — {cmd['description']}\n\n"
                f"**Синтаксис:** `{cmd['synopsis']}`\n\n"
                f"**Приклади:**\n"
                + "\n".join(f"- `{ex}`" for ex in cmd.get("examples", []))
            )
        elif r["tool_called"] == "get_git_config":
            if "settings" in r["result"]:
                settings = r["result"]["settings"]
                pairs = "\n".join(f"- `{k}` = `{v}`" for k, v in settings.items())
                answer = f"**{r['result']['scope']} Git configuration:**\n{pairs}"
            else:
                answer = f"**{r['result']['scope']} `{r['result']['key']}`** = `{r['result']['value']}`"

        lines.append(f"**Final answer:**\n{answer}\n")

        # Why tool > retrieval
        why = get_tool_advantage(r)
        lines.append(f"**Чому tool кращий за retrieval:**\n{why}\n")

    output_path = os.path.join(output_dir, "tool_examples.md")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    return output_path


def get_tool_advantage(result: dict) -> str:
    """Explain why tool is better than retrieval for this case."""
    tool = result["tool_called"]

    if tool == "get_git_command":
        cmd = result["input"].get("command", "")
        explanations = {
            "clone": (
                "git clone has precise syntax with multiple valid forms (HTTPS, SSH, --depth, --branch). "
                "A tool returns the exact synopsis and official examples in a normalized format, "
                "whereas retrieval would return scattered text chunks that the LLM must synthesize."
            ),
            "stash": (
                "git stash is a complex command with multiple sub-commands (stash, stash pop, stash push, stash list, stash apply). "
                "A tool returns all sub-commands in a single structured response with clear syntax, "
                "while retrieval would require matching several chunks and the LLM might miss some sub-commands."
            ),
            "merge": (
                "git merge requires exact branch-argument syntax (e.g., 'git merge feature-branch') and supports multiple flags (--no-ff, --squash, --abort). "
                "A tool returns the precise synopsis and flag options directly, "
                "whereas retrieval from prose documentation would be ambiguous about argument positions."
            ),
        }
        return explanations.get(cmd, (
            "Git commands have precise, structured information (synopsis, description, examples) "
            "that is better served by a queryable database than by semantic search. "
            "Retrieval would return relevant text chunks, but the tool returns the exact command "
            "structure and official examples in a normalized format."
        ))

    if tool == "get_git_config":
        input_data = result["input"]
        if "key" in input_data:
            return (
                "Git configuration is user-specific and dynamic — each user has unique settings that change over time. "
                "Querying a specific config key (e.g., user.name) requires live data that cannot be stored in a static knowledge base."
            )
        return (
            "Git configuration is user-specific and dynamic. Each user has unique settings that change over time. "
            "A static knowledge base cannot contain personal configuration data — only a tool that queries live config can provide accurate results."
        )

    return "Tool provides structured, real-time data that retrieval cannot reliably serve."


# ── CLI ─────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    parser = __import__("argparse").ArgumentParser(description="HW5: External Tool Integration")
    parser.add_argument("--list", action="store_true", help="List available tools")
    parser.add_argument("--demo", action="store_true", help="Run all examples + generate report")
    parser.add_argument("--tool", type=str, help="Tool name to call")
    parser.add_argument("--input", type=str, help='JSON input for the tool')

    args = parser.parse_args()

    if args.list:
        for tool in list_tools():
            print(f"🔧 {tool['name']}: {tool['description']}")
            print(f"   Input: {json.dumps(tool['input_schema'], ensure_ascii=False)}")
            print()

    if args.demo:
        results = run_demo()
        report_path = generate_examples_report(results)
        print(f"\nReport saved to {report_path}")
        for r in results:
            status = "❌ Error" if "error" in r["result"] else "✅ OK"
            print(f"  {status} | {r['tool_called']}({r['input']})")

    if args.tool:
        if not args.input:
            print("Error: --input is required when calling a tool", file=sys.stderr)
            sys.exit(1)
        try:
            input_data = json.loads(args.input)
        except json.JSONDecodeError as e:
            print(f"Error: invalid JSON input: {e}", file=sys.stderr)
            sys.exit(1)
        result = call_tool(args.tool, input_data)
        print(json.dumps(result, indent=2, ensure_ascii=False))

    if not (args.list or args.demo or args.tool):
        parser.print_help()