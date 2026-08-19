#!/usr/bin/env python3
"""
HW6 — Agentic Workflow: Git tutoring assistant

Domain: Git command reference and configuration
Use case: User asks "how do I X in git?" or "what is my git setting Y?"
         The agent routes the question to the correct tool.

Workflow:
    Query → Route (keyword rules) → Execute (tool) → Observe → Synthesize → Answer

Usage:
    python3 scripts/agent_flow.py
"""

import json
import re
import subprocess
from typing import Optional

# ── Domain ──────────────────────────────────────────────────────────────
DOMAIN = "Git command reference and configuration"
USE_CASE = (
    "User asks 'how do I X in git?' or 'what is my git setting Y?'. "
    "The agent routes the question to the correct tool."
)

# ── Built-in Git command DB (from HW5) ─────────────────────────────────
GIT_COMMANDS = {
    "clone": {
        "synopsis": "git clone <repository> [directory]",
        "description": "Clone a repository into a new directory",
        "examples": ["git clone https://github.com/user/repo.git", "git clone --depth=1 <url>"],
    },
    "push": {
        "synopsis": "git push [<remote> [<refspec>]]",
        "description": "Update remote refs with local refs",
        "examples": ["git push origin main", "git push --force-with-lease"],
    },
    "pull": {
        "synopsis": "git pull [<options>] [<remote> [<refspec>]]",
        "description": "Fetch and integrate from another repository or a local branch",
        "examples": ["git pull origin main", "git pull --rebase"],
    },
    "merge": {
        "synopsis": "git merge [<options>] [<commit>…]",
        "description": "Join two or more development histories together",
        "examples": ["git merge feature", "git merge --no-ff feature"],
    },
    "rebase": {
        "synopsis": "git rebase [<options>] [<branch>]",
        "description": "Forward-port local commits to the updated upstream head",
        "examples": ["git rebase main", "git rebase -i HEAD~3"],
    },
    "stash": {
        "synopsis": "git stash [push|pop|list|apply|drop] [<options>]",
        "description": "Temporarily shelf changes in a dirty working directory",
        "examples": ["git stash push -m 'work in progress'", "git stash pop"],
    },
    "reset": {
        "synopsis": "git reset [<flags>] <commit>",
        "description": "Reset current HEAD to the specified state",
        "examples": ["git reset --soft HEAD~1", "git reset HEAD file.txt"],
    },
    "checkout": {
        "synopsis": "git checkout <branch>|<file>…",
        "description": "Switch branches or restore working tree files",
        "examples": ["git checkout feature", "git checkout -- file.txt"],
    },
    "branch": {
        "synopsis": "git branch [<options>] [<branch-name> [<start-point>]]",
        "description": "List, create, or delete branches",
        "examples": ["git branch -a", "git branch -d old-feature"],
    },
    "log": {
        "synopsis": "git log [<options>] [<revision range>]",
        "description": "Show commit logs",
        "examples": ["git log --oneline -10", "git log --graph --all --oneline"],
    },
    "status": {
        "synopsis": "git status [<flags>] [<path>…]",
        "description": "Show working tree status",
        "examples": ["git status", "git status --short"],
    },
    "diff": {
        "synopsis": "git diff [<options>] [<commit>] <file>…",
        "description": "Show changes between commits, commit and working tree, etc.",
        "examples": ["git diff", "git diff HEAD~1"],
    },
    "commit": {
        "synopsis": "git commit [<options>] [<pathspec>…]",
        "description": "Record changes to the repository",
        "examples": ["git commit -m 'fix: resolve issue #42'", "git commit --amend"],
    },
    "add": {
        "synopsis": "git add [<options>] [<pathspec>…]",
        "description": "Add file contents to the staging area",
        "examples": ["git add .", "git add -p"],
    },
}

# ── Tool 1: get_git_command ──────────────────────────────────────────────
def get_git_command(command: str) -> str:
    """Get structured info about a Git command."""
    cmd = command.lower().strip()
    if cmd in GIT_COMMANDS:
        info = GIT_COMMANDS[cmd]
        return json.dumps({
            "command": cmd,
            "synopsis": info["synopsis"],
            "description": info["description"],
            "examples": info["examples"],
        }, indent=2)
    # Fuzzy match
    for key in GIT_COMMANDS:
        if cmd in key or key in cmd:
            return json.dumps({
                "command": key,
                "synopsis": GIT_COMMANDS[key]["synopsis"],
                "description": GIT_COMMANDS[key]["description"],
                "examples": GIT_COMMANDS[key]["examples"],
            }, indent=2)
    return json.dumps({"error": f"Command '{command}' not found in reference DB"}, indent=2)

# ── Tool 2: get_git_config ──────────────────────────────────────────────
def get_git_config(scope: str = "global") -> str:
    """Get Git configuration values for a given scope."""
    try:
        result = subprocess.run(
            ["git", "config", f"--{scope}", "--list"],
            capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0:
            settings = {}
            for line in result.stdout.strip().split("\n"):
                if "=" in line:
                    k, v = line.split("=", 1)
                    settings[k.strip()] = v.strip()
            return json.dumps({"scope": scope, "settings": settings}, indent=2)
        else:
            return json.dumps({"scope": scope, "settings": {}, "note": "No config found"}, indent=2)
    except FileNotFoundError:
        return json.dumps({"scope": scope, "settings": {}, "note": "Git not installed"}, indent=2)
    except subprocess.TimeoutExpired:
        return json.dumps({"scope": scope, "error": "timeout"}, indent=2)

# ── Tool registry ───────────────────────────────────────────────────────
TOOLS = {
    "get_git_command": {
        "description": "Get structured information about a Git command (synopsis, description, examples). Use when user asks about a specific git command or 'how do I X'.",
        "function": get_git_command,
    },
    "get_git_config": {
        "description": "Get Git configuration values for a given scope (global or local). Use when user asks about their git settings or configuration.",
        "function": get_git_config,
    },
}

# ── Routing rules ───────────────────────────────────────────────────────
ROUTE_RULES = [
    # Command queries
    ("(how|how do i|як|как).*(clone|push|pull|merge|rebase|stash|reset|checkout|branch|log|status|diff|commit|add)", "get_git_command"),
    ("(what|який|какой).*(clone|push|pull|merge|rebase|stash|reset|checkout|branch|log|status|diff|commit|add)", "get_git_command"),
    ("(git\\s+(clone|push|pull|merge|rebase|stash|reset|checkout|branch|log|status|diff|commit|add))", "get_git_command"),
    # Config queries
    ("(config|setting|настанов|настройка|user\\.name|user\\.email|core|push\\.default)", "get_git_config"),
]

# ── Router ──────────────────────────────────────────────────────────────
def route_query(query: str) -> Optional[str]:
    """Route query to a tool name, or return None."""
    q = query.lower()
    for pattern, tool_name in ROUTE_RULES:
        if re.search(pattern, q):
            return tool_name
    return None

# ── Extract params ─────────────────────────────────────────────────────
def extract_command(query: str) -> Optional[str]:
    """Extract git command name from query."""
    for cmd in GIT_COMMANDS:
        if cmd in query.lower():
            return cmd
    # Fallback: last word or 'git X' pattern
    m = re.search(r'git\s+(\w+)', query, re.I)
    if m:
        return m.group(1).lower()
    return None

# ── Agent loop (1-step) ─────────────────────────────────────────────────
def agent_run(query: str) -> dict:
    """Run the full agentic loop: route → execute → synthesize → answer."""
    result = {
        "query": query,
        "route": None,
        "tool_called": None,
        "args": None,
        "observation": "",
        "synthesis": "",
        "final_answer": "",
    }

    # 1. Route
    tool = route_query(query)
    result["route"] = tool

    if tool is None:
        result["synthesis"] = "Query does not match any known route — no tool applicable."
        result["final_answer"] = (
            f"Не вдалося визначити, який інструмент використати для запиту '{query}'. "
            "Спробуйте уточнити: чи питаєте ви про git-команду чи налаштування?"
        )
        return result

    # 2. Execute tool
    if tool == "get_git_command":
        cmd = extract_command(query)
        if cmd:
            obs = get_git_command(cmd)
            args = {"command": cmd}
        else:
            obs = get_git_command(query[:20])
            args = {"command": query[:20]}
    elif tool == "get_git_config":
        obs = get_git_config()
        args = {"scope": "global"}
    else:
        obs = "Unknown tool."
        args = {}

    result["tool_called"] = tool
    result["args"] = args
    result["observation"] = obs[:500]

    # 3. Synthesize
    obs_json = json.loads(obs) if obs.startswith("{") else {"raw": obs}
    if "error" in obs_json or "not found" in obs.lower():
        result["synthesis"] = "Tool returned no matching data."
        result["final_answer"] = (
            f"Для запиту '{query}' викликано {tool}, але дані не знайдено. "
            "Доступні команди: " + ", ".join(sorted(GIT_COMMANDS.keys())) + "."
        )
    else:
        result["synthesis"] = "Tool returned relevant data — summarizing for the user."
        result["final_answer"] = obs

    return result

# ── Demo traces ─────────────────────────────────────────────────────────
def generate_traces() -> list:
    """Generate 5 agent traces."""
    queries = [
        "how do I stash my changes?",
        "how do I rebase onto main?",
        "what is my git user.name?",
        "how do I clone a repo with shallow history?",
        "show me recent commits graph",
    ]
    return [agent_run(q) for q in queries]

# ── Main ────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print(f"Domain: {DOMAIN}")
    print(f"Use case: {USE_CASE}")
    print(f"Tools: {list(TOOLS.keys())}")
    print(f"Route rules: {len(ROUTE_RULES)} patterns")
    print()

    traces = generate_traces()
    print(f"Generated {len(traces)} traces\n")

    # Write examples
    with open("outputs/agent_flow_examples.md", "w") as f:
        for i, t in enumerate(traces, 1):
            f.write(f"## Example {i}\n\n")
            f.write(f"**Query:** {t['query']}\n\n")
            f.write(f"**Route:** `{t['route']}`\n\n")
            if t["tool_called"]:
                f.write(f"**Tool called:** `{t['tool_called']}`\n\n")
                f.write(f"**Args:**\n```json\n{json.dumps(t['args'], indent=2)}\n```\n\n")
            f.write(f"**Observation:**\n```json\n{t['observation']}\n```\n\n")
            f.write(f"**Synthesis:** {t['synthesis']}\n\n")
            f.write(f"**Final answer:**\n{t['final_answer']}\n\n")

    # Print summary
    for i, t in enumerate(traces, 1):
        status = "✅" if t["route"] and "error" not in t["observation"].lower() else "⚠️"
        print(f"  {status} Example {i}: {t['route']} → {t['tool_called']} | {t['query'][:60]}")

    print(f"\nSaved outputs/agent_flow_examples.md")