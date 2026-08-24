#!/usr/bin/env python3
"""
HW7 — Перенесення custom agent workflow на LangGraph

Той самий workflow з HW6 (Git tutoring assistant), реалізований як LangGraph-граф:
    State (TypedDict) + Nodes (functions) + Edges (conditional routing).

State:
    AgentState (TypedDict) — user_goal, selected_route, tool_calls,
    observations, final_answer, executed_nodes (trace).

Nodes (5):
    classify_request   — визначає route (ті самі rules з HW6)
    command_workflow   — викликає get_git_command
    config_workflow    — викликає get_git_config
    clarification      — формує уточнювальне питання (без інструменту)
    build_answer       — синтезує фінальну відповідь з observations

Edges:
    classify_request → (conditional) command_workflow | config_workflow | clarification
    command_workflow → build_answer
    config_workflow  → build_answer
    clarification    → END
    build_answer     → END

Тестування: 3 test questions (по одному на кожен route), трасування:
    input → route → executed nodes → final state → final answer.

Usage:
    ./venv/bin/python scripts/langgraph_flow.py
"""

import json
import sys
from typing import Optional, TypedDict

from langgraph.graph import StateGraph, END

# Тот самий domain-код з HW6 (routes, tools, synthesis) — імпорт, а не копія.
sys.path.insert(0, __file__.rsplit("/", 1)[0])
from agent_flow import (
    GIT_COMMANDS,
    get_git_command,
    get_git_config,
    route_query,
    extract_command,
    synthesize_command,
    synthesize_config,
)

DOMAIN = "Git command reference and configuration"
FRAMEWORK = "LangGraph"

# ── State ───────────────────────────────────────────────────────────────
class AgentState(TypedDict, total=False):
    """Спільний стан графа. Кожен node повертає partial-оновлення."""
    user_goal: str
    selected_route: str
    tool_calls: list
    observations: list
    final_answer: str
    executed_nodes: list


# ── Nodes ───────────────────────────────────────────────────────────────
def classify_request(state: AgentState) -> dict:
    """Node 1: визначити route (дзеркало route_query з HW6)."""
    route = route_query(state["user_goal"])
    return {
        "selected_route": route,
        "tool_calls": [],
        "observations": [],
        "final_answer": None,
        "executed_nodes": ["classify_request"],
    }


def run_command_workflow(state: AgentState) -> dict:
    """Node 2: викликати get_git_command для командного запитання."""
    cmd = extract_command(state["user_goal"])
    args = {"command": cmd if cmd else state["user_goal"][:20]}
    obs = get_git_command(args["command"])
    return {
        "tool_calls": [{"name": "get_git_command", "args": args}],
        "observations": [obs],
        "executed_nodes": state.get("executed_nodes", []) + ["command_workflow"],
    }


def run_config_workflow(state: AgentState) -> dict:
    """Node 3: викликати get_git_config для запитання про налаштування."""
    scope = "local" if "local" in state["user_goal"].lower() else "global"
    args = {"scope": scope}
    obs = get_git_config(scope)
    return {
        "tool_calls": [{"name": "get_git_config", "args": args}],
        "observations": [obs],
        "executed_nodes": state.get("executed_nodes", []) + ["config_workflow"],
    }


def ask_clarification(state: AgentState) -> dict:
    """Node 4: уточнювальне питання (інструмент не викликається)."""
    answer = (
        "Уточніть, будь ласка: ви питаєте про git-команду "
        "(наприклад, 'як зробити rebase?') чи про налаштування git "
        "(наприклад, 'яке у мене user.name?')."
    )
    return {
        "final_answer": answer,
        "executed_nodes": state.get("executed_nodes", []) + ["clarification"],
    }


def build_answer(state: AgentState) -> dict:
    """Node 5: синтезувати фінальну відповідь з observations."""
    if state["selected_route"] == "command_workflow":
        answer = synthesize_command(state["observations"][0])
    else:  # config_workflow
        answer = synthesize_config(state["observations"][0])
    return {
        "final_answer": answer,
        "executed_nodes": state.get("executed_nodes", []) + ["build_answer"],
    }


# ── Conditional edge (routing function) ─────────────────────────────────
def route_decision(state: AgentState) -> str:
    """Conditional edge: return ім'я node, куди іти далі."""
    return state["selected_route"]


# ── Build graph ─────────────────────────────────────────────────────────
def build_graph():
    graph = StateGraph(AgentState)
    graph.add_node("classify_request", classify_request)
    graph.add_node("command_workflow", run_command_workflow)
    graph.add_node("config_workflow", run_config_workflow)
    graph.add_node("clarification", ask_clarification)
    graph.add_node("build_answer", build_answer)

    graph.set_entry_point("classify_request")
    graph.add_conditional_edges("classify_request", route_decision, {
        "command_workflow": "command_workflow",
        "config_workflow": "config_workflow",
        "clarification": "clarification",
    })
    graph.add_edge("command_workflow", "build_answer")
    graph.add_edge("config_workflow", "build_answer")
    graph.add_edge("clarification", END)
    graph.add_edge("build_answer", END)
    return graph.compile()


# ── Test questions (3, по одному на route) ──────────────────────────────
TEST_QUESTIONS = [
    "how do I stash my changes?",        # → command_workflow
    "what is my git user.name?",         # → config_workflow
    "what is the best pizza recipe?",    # → clarification
]


def _compact_observation(obs: str, limit: int = 160) -> str:
    return obs if len(obs) <= limit else obs[:limit] + "…"


def run_graph(app, question: str) -> dict:
    """Запустити граф на одному запиті, повернути трасування + final state."""
    initial = {
        "user_goal": question,
        "selected_route": None,
        "tool_calls": [],
        "observations": [],
        "final_answer": None,
        "executed_nodes": [],
    }
    final_state = app.invoke(initial)
    return {
        "question": question,
        "route": final_state["selected_route"],
        "executed_nodes": final_state["executed_nodes"],
        "tool_calls": final_state["tool_calls"],
        "final_state": {
            "user_goal": final_state["user_goal"],
            "selected_route": final_state["selected_route"],
            "tool_calls": final_state["tool_calls"],
            "observations": [
                _compact_observation(o) for o in final_state["observations"]
            ] or None,
            "final_answer": final_state["final_answer"],
        },
    }


# ── Main ────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app = build_graph()
    print(f"Domain: {DOMAIN}")
    print(f"Framework: {FRAMEWORK}")
    print("Graph: classify_request → (conditional) → command_workflow | "
          "config_workflow | clarification → build_answer/END")
    print()

    results = [run_graph(app, q) for q in TEST_QUESTIONS]

    # Write examples
    with open("outputs/langgraph_examples.md", "w") as f:
        f.write(f"# HW7 — LangGraph workflow: {len(results)} test examples\n\n")
        f.write(f"Domain: {DOMAIN}\n\n")
        f.write("Graph: `classify_request` → (conditional edge) → "
                "`command_workflow` | `config_workflow` | `clarification` → "
                "`build_answer` → END\n\n")
        for i, r in enumerate(results, 1):
            st = r["final_state"]
            f.write(f"## Example {i}\n\n")
            f.write(f"Input question: {r['question']}\n\n")
            f.write(f"Selected route: `{r['route']}`\n\n")
            f.write(f"Executed nodes: {' → '.join(r['executed_nodes'])}\n\n")
            if st["tool_calls"]:
                tc = st["tool_calls"][0]
                f.write(f"Tool called: `{tc['name']}`\n\n")
                f.write("Args:\n```json\n"
                        + json.dumps(tc["args"], indent=2, ensure_ascii=False)
                        + "\n```\n\n")
                f.write("Observation:\n```json\n"
                        + _compact_observation(st["observations"][0], 400)
                        + "\n```\n\n")
            f.write("Final state:\n\n```json\n"
                    + json.dumps(st, indent=2, ensure_ascii=False)
                    + "\n```\n\n")
            f.write(f"Final answer:\n{st['final_answer']}\n\n")
            f.write("---\n\n")

    # Print summary
    for i, r in enumerate(results, 1):
        tool = r["final_state"]["tool_calls"][0]["name"] if r["final_state"]["tool_calls"] else "—"
        print(f"  Example {i}: route={r['route']:<16} tool={tool:<16} "
              f"nodes={' → '.join(r['executed_nodes'])}")
        print(f"            Q: {r['question']}")
    print("\nSaved outputs/langgraph_examples.md")