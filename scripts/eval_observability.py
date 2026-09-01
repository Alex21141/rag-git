#!/usr/bin/env python3
"""
HW8 — Evaluation + Observability layer for the Git tutoring agent (HW7 / LangGraph).

What this does:
  1. Defines an eval set of 10 questions covering the required scenario types:
       - simple KB question
       - question requiring retrieval (config lookup)
       - question where retrieval may fail (command not in reference DB)
       - question where the agent should say "I don't know" / clarify (out of domain)
       - question requiring a tool
       - one complex / ambiguous question (wrong-retrieval trap)
  2. Runs the REAL compiled LangGraph (build_graph from langgraph_flow.py) on each
     question, capturing the actual route, tools, observation source, final answer
     and wall-clock latency.
  3. Scores each case (task_success / groundedness / answer_quality) against a
     per-question ground-truth expectation, and classifies the error type.
  4. Emits:
       outputs/eval_results.csv   — full eval table (all 13 required columns)
       outputs/eval_results.md    — same table as Markdown
       outputs/eval_summary.md    — observability metrics
       outputs/eval_raw.json      — full traces (for reproducibility / debugging)

The actual columns (answer, retrieved_chunks, route_or_mode, tools_used, latency_ms)
are taken from real execution, NOT invented. Scoring compares real output against
the declared expectation.

Usage:
    ./venv/bin/python scripts/eval_observability.py
"""

import csv
import json
import os
import re
import sys
import time

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from langgraph_flow import build_graph  # the system under test (HW7 graph)

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(HERE, "outputs")
os.makedirs(OUT, exist_ok=True)

# ── Eval set ────────────────────────────────────────────────────────────
# Each case declares ground-truth used for SCORING:
#   expected_route     — which route a correct system picks
#   expected_behavior  — human description of correct behavior
#   exp_success        — yes / partial / no for a correct system
#   exp_grounded       — good / partial / bad / not_applicable
#   exp_quality        — good / partial / bad
# The ACTUAL values below are filled from execution.
EVAL_SET = [
    {
        "id": 1,
        "question": "how do I stash my changes?",
        "scenario": "simple KB question",
        "expected_behavior": "Route to command tool, return `git stash` synopsis + examples",
        "expected_route": "command_workflow",
        "exp_success": "yes", "exp_grounded": "good", "exp_quality": "good",
        "expect_cmd": "stash",
    },
    {
        "id": 2,
        "question": "how do I rebase onto main?",
        "scenario": "simple KB question",
        "expected_behavior": "Route to command tool, return `git rebase` info",
        "expected_route": "command_workflow",
        "exp_success": "yes", "exp_grounded": "good", "exp_quality": "good",
        "expect_cmd": "rebase",
    },
    {
        "id": 3,
        "question": "show me recent commits graph",
        "scenario": "requires tool (phrase → log)",
        "expected_behavior": "Map 'commits graph' phrase to `git log`, return log info",
        "expected_route": "command_workflow",
        "exp_success": "yes", "exp_grounded": "good", "exp_quality": "good",
        "expect_cmd": "log",
    },
    {
        "id": 4,
        "question": "git push --force-with-lease",
        "scenario": "simple KB question (explicit command)",
        "expected_behavior": "Route to command tool, return `git push` info",
        "expected_route": "command_workflow",
        "exp_success": "yes", "exp_grounded": "good", "exp_quality": "good",
        "expect_cmd": "push",
    },
    {
        "id": 5,
        "question": "what is my git user.name?",
        "scenario": "retrieval (config lookup)",
        "expected_behavior": "Route to config tool (global), return user.name value",
        "expected_route": "config_workflow",
        "exp_success": "yes", "exp_grounded": "good", "exp_quality": "good",
    },
    {
        "id": 6,
        "question": "what is my local git config?",
        "scenario": "retrieval (config lookup, local scope)",
        "expected_behavior": "Route to config tool with local scope, return local settings",
        "expected_route": "config_workflow",
        "exp_success": "yes", "exp_grounded": "good", "exp_quality": "good",
        "note_scope": "local",
    },
    {
        "id": 7,
        "question": "how do I cherry-pick a commit?",
        "scenario": "retrieval may fail (command not in DB)",
        "expected_behavior": "Command not in reference DB → honestly report 'not found' + list available commands",
        "expected_route": "command_workflow",
        "exp_success": "partial", "exp_grounded": "partial", "exp_quality": "partial",
    },
    {
        "id": 8,
        "question": "what is the best pizza recipe?",
        "scenario": "out of domain → should say 'I don't know' / clarify",
        "expected_behavior": "No git intent → ask clarifying question, do NOT call a tool",
        "expected_route": "clarification",
        "exp_success": "yes", "exp_grounded": "not_applicable", "exp_quality": "good",
    },
    {
        "id": 9,
        "question": "how do I undo my last commit but keep the changes?",
        "scenario": "complex / ambiguous (wrong-retrieval trap)",
        "expected_behavior": "Correct answer is `git reset --soft HEAD~1`; naive extract matches the word 'commit' → returns `git commit` (WRONG)",
        "expected_route": "command_workflow",
        "exp_success": "no", "exp_grounded": "bad", "exp_quality": "bad",
        "note_trap": "ambiguous",
    },
    {
        "id": 10,
        "question": "how do I deploy my app to a server?",
        "scenario": "out of domain but looks command-like (mis-route trap)",
        "expected_behavior": "Not a git command → should clarify; naive router sends to command tool with no command → 'not found' fallback",
        "expected_route": "clarification",
        "exp_success": "partial", "exp_grounded": "partial", "exp_quality": "partial",
        "note_trap": "out-of-domain mis-route",
    },
]

# ── Intent map: запит → команда, яку МОГЛА б повернути ідеальна система ──
# Витягнуто вручну з питань eval set (ground truth для оцінки). Використовується
# для (1) перевірки фактичної відповіді на правильну команду і (2) оцінки
# «ідеальної» версії з LLM/інтент-екстракцією (сценарій next-step).
INTENT = {
    "how do I stash my changes?": "stash",
    "how do I rebase onto main?": "rebase",
    "show me recent commits graph": "log",
    "git push --force-with-lease": "push",
    "how do I cherry-pick a commit?": "cherry-pick",   # немає в БД
    "how do I undo my last commit but keep the changes?": "reset",
}

COLUMNS = [
    "id", "question", "expected_behavior", "answer", "retrieved_chunks",
    "route_or_mode", "tools_used", "task_success", "groundedness",
    "answer_quality", "latency_ms", "errors", "notes",
]


def run_one(app, question: str) -> dict:
    """Run the real graph on one question; return trace + latency."""
    initial = {
        "user_goal": question,
        "selected_route": None,
        "tool_calls": [],
        "observations": [],
        "final_answer": None,
        "executed_nodes": [],
    }
    t0 = time.perf_counter()
    st = app.invoke(initial)
    latency_ms = int((time.perf_counter() - t0) * 1000)
    return {
        "route": st.get("selected_route"),
        "tools": [tc["name"] for tc in st.get("tool_calls", [])],
        "tool_args": st.get("tool_calls", []),
        "observations": st.get("observations", []),
        "answer": st.get("final_answer") or "",
        "latency_ms": latency_ms,
        "executed_nodes": st.get("executed_nodes", []),
    }


def classify_error(case: dict, res: dict) -> str:
    """Determine the error type from the ACTUAL result vs the case's intent."""
    obs = res["observations"][0] if res["observations"] else ""
    has_error = '"error"' in obs
    route = res["route"]
    q = case["question"]

    # out-of-domain question that got routed to a tool instead of clarify
    if case["expected_route"] == "clarification" and route == "command_workflow":
        return "wrong_routing"
    # command intent: did we extract the INTENDED command (INTENT map)?
    if q in INTENT:
        actual = (res["tool_args"][0]["args"].get("command")
                  if res["tool_args"] else None)
        intended = INTENT[q]
        if intended not in [k for k in GIT_COMMANDS_KEYS]:
            # command absent from DB: correct behavior = honest "not found"
            if actual is not None and actual != intended and not has_error:
                return "wrong_retrieval"   # fuzzy match returned a WRONG command
            return "none"                  # honest not-found fallback
        if actual != intended:
            return "wrong_retrieval"
        return "none"
    return "none"


GIT_COMMANDS_KEYS = ["clone", "push", "pull", "merge", "rebase", "stash",
                     "reset", "checkout", "branch", "log", "status", "diff",
                     "commit", "add"]


def score(case: dict, res: dict) -> dict:
    """Compare actual result against ground truth; return scoring dict."""
    obs = res["observations"][0] if res["observations"] else ""
    has_error = '"error"' in obs
    route = res["route"]
    err = classify_error(case, res)

    # task_success: did the system do the right thing for this case?
    if err == "wrong_routing":
        success = "partial" if route == "command_workflow" else "no"
    elif err == "wrong_retrieval":
        success = "no"
    elif has_error and case["question"] in INTENT:
        success = "partial"  # command not in DB: honest 'not found' fallback
    else:
        success = case["exp_success"]

    # groundedness: is the answer supported by the observation?
    if route == "clarification":
        grounded = "not_applicable"
    elif err == "wrong_retrieval":
        grounded = "bad"
    elif has_error and case["question"] in INTENT:
        grounded = "partial"  # 'not found' is honest, grounded in the miss
    else:
        grounded = "good"

    # answer_quality
    if success == "yes" and grounded in ("good", "not_applicable"):
        quality = "good"
    elif success == "partial" or grounded in ("partial",):
        quality = "partial"
    else:
        quality = "bad"

    # retrieved_chunks: the source(s) the answer was grounded in
    if route == "command_workflow":
        chunks = f"get_git_command DB → {obs if has_error else case.get('expect_cmd', '?')}"
        if has_error:
            chunks = "get_git_command DB → (not found, no matching chunk)"
    elif route == "config_workflow":
        scope = (res["tool_args"][0]["args"].get("scope")
                 if res["tool_args"] else "global")
        chunks = f"get_git_config scope={scope} (live `git config`)"
    else:
        chunks = "none (no tool called)"

    notes_bits = []
    if err != "none":
        notes_bits.append(f"error={err}")
    if case.get("note_trap"):
        notes_bits.append(f"trap case ({case['note_trap']})")
    if has_error and case["question"] in INTENT:
        notes_bits.append("honest not-found fallback")
    if case["expected_route"] != route:
        notes_bits.append(f"route drift: expected {case['expected_route']}")

    return {
        "route_or_mode": route,
        "tools_used": ", ".join(res["tools"]) if res["tools"] else "—",
        "task_success": success,
        "groundedness": grounded,
        "answer_quality": quality,
        "latency_ms": res["latency_ms"],
        "errors": err,
        "notes": "; ".join(notes_bits) or "matches expectation",
    }


def llm_extract_command(question: str, model: str = None) -> dict:
    """Демо: LLM як інтент-екстрактор (наївний regex-екстрактор → LLM).

    Читає LITELLM_BASE_URL / LITELLM_API_KEY / LITELLM_MODEL зі środowiskа.
    Повертає {"command": str|None, "raw": str, "ok": bool}.
    """
    import os
    try:
        from openai import OpenAI
    except ImportError:
        return {"command": None, "ok": False,
                "raw": "openai package not installed (pip install openai)"}
    base = os.environ.get("LITELLM_BASE_URL", "http://10.10.0.41:4000/v1")
    key = os.environ.get("LITELLM_API_KEY", "")
    model = model or os.environ.get("LITELLM_MODEL", "qwen38-27b-awq")
    valid = ", ".join(sorted(GIT_COMMANDS_KEYS))
    sys_prompt = (
        "You extract the git command a user is asking about. "
        "Valid commands: " + valid + ". "
        "If the user means a command NOT in the list (e.g. cherry-pick) "
        "return that name. If there is no git intent, return NONE. "
        "Answer with exactly one word, no explanation."
    )
    try:
        client = OpenAI(base_url=base, api_key=key)
        r = client.chat.completions.create(
            model=model,
            messages=[{"role": "system", "content": sys_prompt},
                      {"role": "user", "content": question}],
            max_tokens=16,
            temperature=0,
        )
        out = (r.choices[0].message.content or "").strip()
        # some reasoning models put the answer inside reasoning; take last token
        cand = [w for w in out.replace("\n", " ").split() if w and not w.startswith("{")]
        word = (cand[-1] if cand else out).strip(".\"'").lower()
        if word in ("none", "нічого", "") :
            word = None
        return {"command": word, "ok": True, "raw": out}
    except Exception as e:
        return {"command": None, "ok": False, "raw": str(e)}


def run_llm_demo(rows: list, raw: list) -> None:
    """Для command-кейсів: показати, що LLM-екстрактор повернув би
    правильно інтентовану команду (у порівнянні з фактичною regex-екстракцією)."""
    import os
    lines = [
        "# HW8 — LLM intent-extraction demo (next-step scenario)",
        "",
        "Scenario: replace the naive `extract_command` (regex word match) with an "
        "LLM call. The LLM reads the WHOLE question and returns the intended "
        "command. Evaluated on the command cases of the eval set.",
        "",
        "| id | question | actual (regex) | intended | LLM output | verdict |",
        "|----|----------|----------------|----------|------------|---------|",
    ]
    fixed = 0
    tested = 0
    for r in raw:
        q = r["question"]
        if q not in INTENT:
            continue
        tested += 1
        actual = (r["tool_calls"][0]["args"].get("command")
                  if r["tool_calls"] else "—")
        intended = INTENT[q]
        res = llm_extract_command(q)
        out = res["command"] if res["ok"] else f"ERROR: {res['raw'][:40]}"
        verdict = "✅ fixed" if (res["ok"] and out == intended) else "❌"
        if res["ok"] and out == intended:
            fixed += 1
        lines.append(f"| {r['id']} | {q} | `{actual}` | `{intended}` | "
                     f"`{out}` | {verdict} |")
    lines += [
        "",
        f"**Result:** {fixed}/{tested} command cases would return the intended command.",
        "",
        "Latency trade-off: each extraction becomes an LLM call "
        "(hundreds of ms vs ~0 ms), so this is a quality/latency trade — "
        "appropriate for a small, ambiguous command set like git.",
        "",
    ]
    with open(os.path.join(OUT, "llm_intent_demo.md"), "w") as f:
        f.write("\n".join(lines))
    print(f"LLM demo: {fixed}/{tested} intended commands extracted "
          f"-> outputs/llm_intent_demo.md")


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--llm", action="store_true",
                    help="run the optional LLM intent-extraction demo")
    args = ap.parse_args()

    app = build_graph()
    rows = []
    raw = []

    for case in EVAL_SET:
        res = run_one(app, case["question"])
        sc = score(case, res)
        ans = res["answer"].replace("\n", " ⏎ ")
        if len(ans) > 200:
            ans = ans[:200] + "…"
        row = {
            "id": case["id"],
            "question": case["question"],
            "expected_behavior": case["expected_behavior"],
            "answer": ans,
            "retrieved_chunks": sc_score_chunks(case, res),
            "route_or_mode": res["route"],
            "tools_used": ", ".join(res["tools"]) if res["tools"] else "—",
            "task_success": sc["task_success"],
            "groundedness": sc["groundedness"],
            "answer_quality": sc["answer_quality"],
            "latency_ms": res["latency_ms"],
            "errors": sc["errors"],
            "notes": sc["notes"],
        }
        rows.append(row)
        raw.append({
            "id": case["id"],
            "question": case["question"],
            "scenario": case["scenario"],
            "route": res["route"],
            "executed_nodes": res["executed_nodes"],
            "tool_calls": res["tool_args"],
            "observation": res["observations"][0] if res["observations"] else None,
            "final_answer": res["answer"],
            "latency_ms": res["latency_ms"],
            "scoring": {k: sc[k] for k in
                        ("task_success", "groundedness", "answer_quality", "errors")},
        })

    # ── write CSV ──
    with open(os.path.join(OUT, "eval_results.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=COLUMNS)
        w.writeheader()
        w.writerows(rows)

    # ── write MD table ──
    with open(os.path.join(OUT, "eval_results.md"), "w") as f:
        f.write("# HW8 — Evaluation results\n\n")
        f.write("System under test: **Git tutoring agent** (HW7, LangGraph). "
                "Routes: `command_workflow` / `config_workflow` / `clarification`. "
                "Tools: `get_git_command` (mock DB, 14 commands), `get_git_config` (live subprocess).\n\n")
        f.write(f"Cases: **{len(rows)}** (real execution, deterministic — no LLM in the loop).\n\n")
        f.write("| " + " | ".join(COLUMNS) + " |\n")
        f.write("|" + "---|" * len(COLUMNS) + "\n")
        for r in rows:
            cells = [str(r[c]).replace("|", "\\|") for c in COLUMNS]
            f.write("| " + " | ".join(cells) + " |\n")
        f.write("\n")

    # ── metrics ──
    total = len(rows)
    def count(field, val):
        return sum(1 for r in rows if r[field] == val)
    success = count("task_success", "yes")
    partial = count("task_success", "partial")
    fail = count("task_success", "no")
    g_good = count("groundedness", "good")
    g_part = count("groundedness", "partial")
    g_bad = count("groundedness", "bad")
    lats = [r["latency_ms"] for r in rows]
    avg_lat = sum(lats) // total if total else 0
    max_lat = max(lats) if lats else 0
    max_id = rows[lats.index(max_lat)]["id"] if lats else "—"
    err_counts = {}
    for r in rows:
        err_counts[r["errors"]] = err_counts.get(r["errors"], 0) + 1

    metrics = {
        "total_cases": total,
        "success": success, "partial": partial, "fail": fail,
        "success_rate": f"{success}/{total} = {round(100*success/total)}%",
        "partial_rate": f"{partial}/{total} = {round(100*partial/total)}%",
        "fail_rate": f"{fail}/{total} = {round(100*fail/total)}%",
        "groundedness_good": f"{g_good}/{total} = {round(100*g_good/total)}%",
        "groundedness_partial": f"{g_part}/{total} = {round(100*g_part/total)}%",
        "groundedness_bad": f"{g_bad}/{total} = {round(100*g_bad/total)}%",
        "average_latency_ms": avg_lat,
        "max_latency_ms": max_lat,
        "max_latency_case_id": max_id,
        "error_types": err_counts,
    }

    with open(os.path.join(OUT, "eval_summary.md"), "w") as f:
        f.write("# HW8 — Observability metrics\n\n")
        f.write("```\n")
        f.write(f"Total cases: {metrics['total_cases']}\n")
        f.write(f"Success rate: {metrics['success_rate']}\n")
        f.write(f"Partial success: {metrics['partial_rate']}\n")
        f.write(f"Failure rate: {metrics['fail_rate']}\n\n")
        f.write(f"Groundedness good: {metrics['groundedness_good']}\n")
        f.write(f"Groundedness partial: {metrics['groundedness_partial']}\n")
        f.write(f"Groundedness bad: {metrics['groundedness_bad']}\n\n")
        f.write(f"Average latency: {metrics['average_latency_ms']} ms\n")
        f.write(f"Max latency: {metrics['max_latency_ms']} ms (case #{metrics['max_latency_case_id']})\n\n")
        f.write("Error types:\n")
        for k, v in sorted(err_counts.items(), key=lambda x: -x[1]):
            f.write(f"  {k}: {v}\n")
        f.write("```\n\n")
        f.write("Route distribution:\n")
        route_counts = {}
        for r in rows:
            route_counts[r["route_or_mode"]] = route_counts.get(r["route_or_mode"], 0) + 1
        for k, v in route_counts.items():
            f.write(f"- {k}: {v}\n")

    with open(os.path.join(OUT, "eval_raw.json"), "w") as f:
        json.dump(raw, f, indent=2, ensure_ascii=False)

    # ── console summary ──
    print(f"Ran {total} eval cases against the real HW7 LangGraph agent.")
    print(f"  success={success} partial={partial} fail={fail}")
    print(f"  groundedness good={g_good} partial={g_part} bad={g_bad}")
    print(f"  avg latency={avg_lat} ms, max={max_lat} ms (case #{max_id})")
    print(f"  errors: {err_counts}")
    print("Wrote: outputs/eval_results.csv, eval_results.md, eval_summary.md, eval_raw.json")
    if args.llm:
        run_llm_demo(rows, raw)


def sc_score_chunks(case, res):
    """retrieved_chunks: що ФАКТИЧНО отримало з інструменту (з tool args)."""
    obs = res["observations"][0] if res["observations"] else ""
    has_error = '"error"' in obs
    route = res["route"]
    if route == "command_workflow":
        actual_cmd = (res["tool_args"][0]["args"].get("command")
                      if res["tool_args"] else "?")
        if has_error:
            return (f"get_git_command(«{actual_cmd}») → "
                    "(not found, no matching chunk)")
        return f"get_git_command(«{actual_cmd}») → {actual_cmd} з DB"
    if route == "config_workflow":
        scope = (res["tool_args"][0]["args"].get("scope")
                 if res["tool_args"] else "global")
        return f"get_git_config scope={scope} (live `git config`)"
    return "none (no tool called)"


if __name__ == "__main__":
    main()