#!/usr/bin/env python3
"""
HW6 — Agentic Workflow: Git tutoring assistant

Domain: Git command reference and configuration
Use case: user asks "how do I X in git?" or "what is my git setting Y?".
         The agent routes the question to the correct tool.

Workflow (3 steps):
    Query -> Step 1: Route -> Step 2: Execute tool -> Step 3: Synthesize

Routes (3):
    command_workflow -> get_git_command   (питання про git-команди)
    config_workflow  -> get_git_config    (питання про налаштування git)
    clarification    -> (без інструмента, уточнювальне питання)

Tools (2, mock, deterministic):
    get_git_command(command) -> JSON з вбудованої БД 14 git-команд
    get_git_config(scope)    -> JSON значень git config через subprocess

State (передається між кроками):
    {
        "user_goal":      str  — оригінальний запит,
        "selected_route": str  — command_workflow / config_workflow / clarification,
        "tool_calls":     list — [ {name, args} ],
        "observations":   list — результати інструментів,
        "final_answer":   str  — синтезована відповідь,
    }

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

# ── Built-in Git command DB (з HW5) ─────────────────────────────────────
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

# ── Tool 1: get_git_command (mock) ──────────────────────────────────────
def get_git_command(command: str) -> str:
    """Get structured info about a Git command (built-in DB, fixed result)."""
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

# ── Tool 2: get_git_config (mock) ───────────────────────────────────────
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
        return json.dumps({"scope": scope, "settings": {}, "note": "No config found"}, indent=2)
    except FileNotFoundError:
        return json.dumps({"scope": scope, "settings": {}, "note": "Git not installed"}, indent=2)
    except subprocess.TimeoutExpired:
        return json.dumps({"scope": scope, "error": "timeout"}, indent=2)

# ── Tool registry ───────────────────────────────────────────────────────
TOOLS = {
    "get_git_command": {
        "description": (
            "Get structured information about a Git command (synopsis, "
            "description, examples). Use when user asks about a specific "
            "git command or 'how do I X'."
        ),
        "parameters": ["command"],
        "function": get_git_command,
    },
    "get_git_config": {
        "description": (
            "Get Git configuration values for a given scope (global or "
            "local). Use when user asks about their git settings."
        ),
        "parameters": ["scope"],
        "function": get_git_config,
    },
}

# ── Routing rules (deterministic, без LLM) ──────────────────────────────
# Route B (config) — найспецифічніші ключові слова, перевіряються першими
CONFIG_HINTS = [
    "config", "setting", "settings", "настановк", "налаштуванн",
    "user.name", "user.email", "core.", "push.default", "credential",
]

# Route A (command) — загальні маркери командних питань
COMMAND_HINTS = [
    "how do i", "how to", "як ", "как ", "command", "команд",
]

# Фрази, які вказують на команду без прямої назви
# (наприклад "recent commits graph" → log, а не commit)
PHRASE_HINTS = {
    "log": ["commit log", "commits", "commit history", "graph"],
    "clone": ["shallow clone", "download the repo"],
}


def route_query(query: str) -> str:
    """Route query to a workflow name (deterministic rules, без LLM)."""
    q = query.lower()
    # Route B: config questions (most specific first)
    if any(h in q for h in CONFIG_HINTS):
        return "config_workflow"
    # Route A: command questions
    if (
        any(h in q for h in COMMAND_HINTS)
        or any(re.search(r"\b" + cmd + r"\b", q) for cmd in GIT_COMMANDS)
        or any(p in q for p in sum(PHRASE_HINTS.values(), []))
    ):
        return "command_workflow"
    # Route C: clarification
    return "clarification"


# ── Extract params ──────────────────────────────────────────────────────
def extract_command(query: str) -> Optional[str]:
    """Extract the git command name from the query."""
    q = query.lower()
    # 1. Exact command word (word boundary: "commits" ≠ "commit")
    for cmd in GIT_COMMANDS:
        if re.search(r"\b" + cmd + r"\b", q):
            return cmd
    # 2. Phrase hints (e.g. "recent commits graph" → log)
    for cmd, phrases in PHRASE_HINTS.items():
        if any(p in q for p in phrases):
            return cmd
    # 3. "git X" pattern
    m = re.search(r"git\s+(\w+)", q)
    if m and m.group(1) in GIT_COMMANDS:
        return m.group(1)
    return None


# ── Synthesis (observation → natural language answer) ───────────────────
def synthesize_command(observation: str) -> str:
    """Формулювати відповідь природною мовою з observation."""
    info = json.loads(observation)
    if "error" in info:
        return (
            f"Команду не знайдено в базі. Доступні команди: "
            f"{', '.join(sorted(GIT_COMMANDS))}."
        )
    lines = [
        f"Використовуйте: `{info['synopsis']}`.",
        f"Призначення: {info['description']}.",
        "Приклади:",
    ]
    lines += [f"- `{ex}`" for ex in info["examples"]]
    return "\n".join(lines)


def synthesize_config(observation: str) -> str:
    info = json.loads(observation)
    settings = info.get("settings", {})
    if not settings:
        return "Налаштувань git у обраному scope не знайдено."
    lines = [f"Налаштування git (scope: {info.get('scope', 'global')}):"]
    lines += [f"- `{k}` = `{v}`" for k, v in settings.items()]
    return "\n".join(lines)


# ── Agent loop (3 steps) ────────────────────────────────────────────────
def agent_run(query: str) -> dict:
    """Run the agentic loop: route → execute → synthesize.

    Returns {"state": final state, "steps": [(label, state_snapshot), ...]}.
    State accumulates across steps — each snapshot shows state after that step.
    """
    state = {
        "user_goal": query,
        "selected_route": None,
        "tool_calls": [],
        "observations": [],
        "final_answer": None,
    }
    steps = []

    def snapshot(label: str):
        """Compact state snapshot (observations truncated for readability)."""
        steps.append((label, {
            "user_goal": state["user_goal"],
            "selected_route": state["selected_route"],
            "tool_calls": [dict(tc) for tc in state["tool_calls"]],
            "observations": [
                o if len(o) <= 160 else o[:160] + "…"
                for o in state["observations"]
            ],
            "final_answer": (
                None if state["final_answer"] is None
                else state["final_answer"][:120]
            ),
        }))

    # Step 1: Route
    state["selected_route"] = route_query(query)
    snapshot("Step 1 (Route)")

    # Step 2: Execute tool
    if state["selected_route"] == "command_workflow":
        cmd = extract_command(query)
        args = {"command": cmd if cmd else query[:20]}
        obs = get_git_command(args["command"])
        state["tool_calls"].append({"name": "get_git_command", "args": args})
        state["observations"].append(obs)
    elif state["selected_route"] == "config_workflow":
        scope = "local" if "local" in query.lower() else "global"
        args = {"scope": scope}
        obs = get_git_config(scope)
        state["tool_calls"].append({"name": "get_git_config", "args": args})
        state["observations"].append(obs)
    # clarification — інструмент не викликається
    snapshot("Step 2 (Execute)")

    # Step 3: Synthesize
    if state["selected_route"] == "command_workflow":
        state["final_answer"] = synthesize_command(state["observations"][0])
    elif state["selected_route"] == "config_workflow":
        state["final_answer"] = synthesize_config(state["observations"][0])
    else:
        state["final_answer"] = (
            "Уточніть, будь ласка: ви питаєте про git-команду "
            "(наприклад, 'як зробити rebase?') чи про налаштування git "
            "(наприклад, 'яке у мене user.name?')."
        )
    snapshot("Step 3 (Synthesize)")

    return {"state": state, "steps": steps}


# ── Demo traces ─────────────────────────────────────────────────────────
QUERIES = [
    "how do I stash my changes?",
    "how do I rebase onto main?",
    "what is my git user.name?",
    "show me recent commits graph",
    "what is the best pizza recipe?",
]


def generate_traces() -> list:
    """Generate 5 agent traces covering all 3 routes."""
    return [agent_run(q) for q in QUERIES]


# ── Main ────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print(f"Domain: {DOMAIN}")
    print(f"Use case: {USE_CASE}")
    print(f"Routes: command_workflow, config_workflow, clarification")
    print(f"Tools: {list(TOOLS.keys())}")
    print()

    results = generate_traces()
    print(f"Generated {len(results)} traces\n")

    # Write examples
    with open("outputs/agent_flow_examples.md", "w") as f:
        for i, r in enumerate(results, 1):
            st = r["state"]
            f.write(f"## Example {i}\n\n")
            f.write(f"Question: {st['user_goal']}\n\n")
            f.write(f"Route: {st['selected_route']}\n\n")
            if st["tool_calls"]:
                f.write(f"Tool called: {st['tool_calls'][0]['name']}\n\n")
                f.write(
                    "Args:\n```json\n"
                    + json.dumps(st["tool_calls"][0]["args"], indent=2)
                    + "\n```\n\n"
                )
                f.write(
                    "Observation:\n```json\n"
                    + st["observations"][0]
                    + "\n```\n\n"
                )
            f.write("State after step:\n\n")
            for label, snap in r["steps"]:
                f.write(f"- {label}: `{json.dumps(snap, ensure_ascii=False)}`\n")
            f.write("\n")
            f.write(f"Final answer:\n{st['final_answer']}\n\n")
            f.write("---\n\n")

    # Print summary
    for i, r in enumerate(results, 1):
        st = r["state"]
        if st["selected_route"] == "clarification":
            status = "🟡"
        elif st["observations"] and "error" not in st["observations"][0].lower():
            status = "✅"
        else:
            status = "⚠️"
        tool = st["tool_calls"][0]["name"] if st["tool_calls"] else "—"
        print(f"  {status} Example {i}: {st['selected_route']} → {tool} | {st['user_goal'][:50]}")

    print("\nSaved outputs/agent_flow_examples.md")