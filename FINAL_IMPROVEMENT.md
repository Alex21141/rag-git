# Final Technical Improvement

## 1. Selected weak point

**Silent confident-wrong answers from word-level command extraction.**

`extract_command` (scripts/agent_flow.py) treated **any DB command word that
happened to appear anywhere in the query as the requested command**
(`if re.search(r"\b" + cmd + r"\b", q)`). The word `commit` is both a DB
command and an extremely common *object* noun in natural git questions, so:

- "how do I cherry-pick a **commit**?" → answered with `git commit`
  (cherry-pick is not in the reference DB at all — the system presented an
  unrelated command as the answer, with full confidence);
- "how do I **undo my last commit** but keep the changes?" → answered with
  `git commit` — the exact opposite of what the user wanted
  (correct answer is `git reset --soft HEAD~1`);
- "how do I deploy my app to a server?" → the command node passed a
  fabricated argument (`query[:20]` = "how do i deploy my a") to the tool,
  which returned a "not found" for a string that was never a command.

A second amplifier: `get_git_command` had a **substring fuzzy match**
(`cmd in key or key in cmd`), so even the tool itself could silently swap in
a different command for a close-looking string.

This is the worst class of failure for a helper: not "I don't know", but a
confident, plausible, **wrong** answer. It was measured on the HW8 eval set
(10 cases, real execution): 2 `wrong_retrieval` + 1 `wrong_routing`,
success rate 70%, and both `wrong_retrieval` cases were exactly this pattern.

## 2. Improvement implemented

One coherent improvement around this single weak point — intent-based
extraction + guardrail + honest fallback (combines the "Improved tool call",
"Simple guardrail" and "Fallback behavior" variants from the task table):

1. **Intent-based extraction** (`extract_command`, scripts/agent_flow.py):
   a command is returned only on a *strong signal*:
   - explicit `git <command>`;
   - a known natural-language intent phrase (`INTENT_PHRASES`, e.g.
     "undo my last commit" → `reset`, "amend my last commit" → `commit`);
   - a command directly after a command-intent marker
     ("how do I <cmd>", "як зробити <cmd>", …);
   - existing safe phrase hints ("recent commits graph" → `log`).
   The dangerous rule — "any DB word anywhere in the query" — is removed:
   an object word no longer selects a command.
2. **Guardrail before the tool call** (HW6 `agent_run` + HW7 LangGraph node
   `run_command_workflow`): if no command can be confidently extracted, the
   tool is **not called with a fabricated argument**. The graph gets a new
   conditional edge: guardrail fallback goes straight to END instead of
   `build_answer` (which expects a non-empty observation).
3. **Honest fallback** (`COMMAND_FALLBACK`, shared constant): instead of a
   confident wrong answer the system says it could not determine the command
   and lists what it *can* help with.
4. **Safe tool matching** (`get_git_command`): substring fuzzy match removed
   (it could silently substitute a wrong command). Only exact match after
   normalization + safe plural→singular ("logs" → "log") remain.

## 3. Why this improvement matters

In a tutoring/reference assistant, a wrong confident answer is worse than no
answer: a user asked "undo my last commit" who receives `git commit` will
create *another* commit, not undo one. The improvement makes failure
**visible and honest**: when the system cannot ground an answer in the
reference DB, it says so. Latency is unchanged (pure Python rules, no LLM),
so there is no quality/speed trade-off — this is a correctness fix.

## 4. Before / after behavior

All examples are from the HW8 eval set (real execution, deterministic).
"Before" numbers are from the committed eval output of the
`hw8-evaluation-observability-layer` branch (old system); "After" — from the
current `final` branch.

### Case 1 — object word no longer hijacks the answer

```
Before:
  Question: how do I cherry-pick a commit?
  System behavior: answers with `git commit` (synopsis + examples), fully
  confident. cherry-pick is not in the reference DB; the object word
  "commit" was extracted as the command. (eval: wrong_retrieval)

After:
  Question: how do I cherry-pick a commit?
  System behavior: "Не вдалося визначити, яку саме git-команду ви маєте на
  увазі. Сформулюйте, будь ласка, питання конкретніше — наприклад: 'git
  rebase' або 'як зробити git reset?'. Доступні команди: add, branch, ..."
  — honest decline + pointer to the available commands. (eval: honest
  not-found fallback, no error)
```

### Case 2 — intent phrase resolves the ambiguity correctly

```
Before:
  Question: how do I undo my last commit but keep the changes?
  System behavior: answers with `git commit` — the opposite of the requested
  operation. (eval: wrong_retrieval)

After:
  Question: how do I undo my last commit but keep the changes?
  System behavior: intent phrase "undo my last commit" → `reset`; answers
  with `git reset`, examples include `git reset --soft HEAD~1` — exactly the
  requested operation. (eval: success)
```

### Case 3 — no fabricated tool arguments

```
Before:
  Question: how do I deploy my app to a server?
  System behavior: command node calls get_git_command with
  "how do i deploy my a" (query[:20]) — a fabricated argument; tool returns
  "Command 'how do i deploy my a' not found". (eval: wrong_routing trap)

After:
  Question: how do I deploy my app to a server?
  System behavior: no command extracted → guardrail stops the tool call,
  honest fallback with the list of commands the bot can help with.
  (eval: success — no tool call with a fabricated argument)
```

### Eval summary (10 cases, real execution)

| Metric | Before (hw8 branch) | After (final branch) |
|---|---|---|
| Success rate | 7/10 (70%) | 9/10 (90%) |
| Partial | 1/10 | 1/10 |
| Failure | 2/10 | **0/10** |
| Groundedness good | 7/10 | 7/10 |
| Groundedness bad | 2/10 | **0/10** |
| wrong_retrieval errors | 2 | **0** |
| wrong_routing errors | 1 | **0** |
| Average latency | 1 ms | 1 ms (unchanged — no LLM) |

No regressions: the 6 cases that worked before still produce identical
answers (cases 1–6 and 8 of the eval set).

## 5. Changelog

## What was improved
Confident wrong answers caused by word-level command extraction
("cherry-pick a commit" → `git commit`, "undo my last commit" → `git commit`,
out-of-domain queries passed as fabricated tool arguments).

## Why this was needed
The HW8 evaluation measured this as the system's main failure mode
(2 wrong_retrieval + 1 wrong_routing). For a reference/tutoring assistant a
wrong confident answer is more harmful than an honest "I don't know".

## What changed technically
- `scripts/agent_flow.py`: `extract_command` rewritten to intent-based
  extraction (explicit `git X` → intent phrases → marker + command position →
  safe phrase hints); dangerous "any DB word anywhere" rule removed.
- `scripts/agent_flow.py`: `COMMAND_FALLBACK` constant + guardrail in
  `agent_run` (no tool call without a confident command).
- `scripts/agent_flow.py`: `get_git_command` substring fuzzy match removed;
  only normalized exact match + plural→singular remain.
- `scripts/langgraph_flow.py`: `run_command_workflow` node applies the same
  guardrail; new conditional edge after `command_workflow` — fallback goes to
  END, normal path goes to `build_answer`.
- `scripts/eval_observability.py`: ground truth for the three trap cases
  updated to the correct behavior; scoring handles the guardrail fallback
  (no tool call, no observation).

## Result
Success 70% → 90%, failures 2 → 0, groundedness bad 2 → 0,
wrong_retrieval/wrong_routing errors 3 → 0. Latency unchanged (1 ms average).
The system now either returns a correctly grounded answer or an honest
fallback; it no longer returns a confident wrong command.

## 6. Remaining limitations

- **Limited intent coverage.** `INTENT_PHRASES` covers the cases from the
  eval set ("undo my last commit", "amend my last commit"). Other
  paraphrases ("скасувати останній комміт", "revert the previous commit",
  "back out the commit") still fall back to the honest decline rather than a
  correct answer — they are *handled safely*, not solved. Extending the map
  (or using the HW8 `--llm` intent extractor) would turn those declines
  into correct answers.
- **The reference DB still lacks `cherry-pick`** (and other commands —
  `revert`, `amend`, `reflog`, …). The fallback honestly lists what is
  available, but the underlying knowledge gap remains; adding commands to
  `GIT_COMMANDS` is a separate, mechanical change.
- **Router still over-triggers.** `route_query` sends "how do i …" queries
  to `command_workflow` even for non-git questions ("deploy my app"), which
  is why the guardrail (not the router) currently catches case 10. A proper
  fix would be a negative-signal check in the router; it was intentionally
  left out to keep the change focused on the one selected weak point.
- **The fallback message is generic.** It lists available commands but does
  not suggest the closest *plausible* command (e.g. "did you mean …?") —
  such suggestions risk reintroducing the confident-wrong pattern, so none
  are made.
- **Only the HW6/HW7 deterministic path was changed.** The `--llm` demo
  (HW8) shows an LLM extractor would also fix these cases, but it is not
  integrated into the production graph (latency/cost trade, out of scope).

## 7. Retrieval-layer embedding A/B/C: MiniLM-L6-v2 vs bge-small vs nomic-embed (real KB)

Separate investigation of the embedding model used by the HW2/HW3
semantic retrieval leg. Question raised after noting that
`all-MiniLM-L6-v2` (384d) is a general-purpose model, not specialized for
technical content. Ran a benchmark on the **real** data — the same 145-chunk
GitLab collection and the same 10 test queries from `scripts/retrieval.py`
(HW2 set). See `outputs/embedding_ab.md` / `.csv`.

| metric | A: MiniLM-L6-v2 (384d) | B: bge-small-en-v1.5 (384d) | C: nomic-embed-text-v1.5 (768d) |
|---|---|---|---|
| mean top-1 cosine | 0.6642 | 0.8126 | 0.7256 |
| mean top1-top2 margin | 0.0388 | 0.0377 | 0.0209 |
| doc-level correct (manual) | 9/10 | 9/10 | 10/10 |
| index build | 1.5s | 2.8s | 11.8s |
| drop-in (same 384d)? | — (current) | yes | no (768d) |

Key finding: **not a runaway** on any pair — the three are close at
document level (9–10/10); the differences are chunk precision and score
calibration. bge-small is the strongest single-model pick (best
calibration, most precise tutorial chunk choices, *and* a 384d drop-in).
nomic-embed-text-v1.5 is genuinely strong (best Q1 "clone", best Q7
"history") but brings no net win here: it never beats bge where bge is
already exact, has the weakest reranking margin, doubles index size, and
requires code changes (768d). Its strengths (8K context, multilingual,
long docs) don't matter for 145 short GitLab chunks. MiniLM's real
weakness — generic intro chunks instead of the exact tutorial — is visible
on Q1/Q2/Q7 and is what bge fixes. BM25 in the HW3 hybrid anchors exact
terms, mitigating the semantic model's mild weaknesses. **Decision (project
owner): keep all-MiniLM-L6-v2 as-is** — bge-small-en-v1.5 is recorded as
the measured drop-in upgrade option; nomic-embed-text-v1.5 measured as an
alternative.

(Note: this benchmark documents the *options*; none is wired into the
retrieval pipeline on this branch — that pipeline is HW2/HW3 code, kept
as-is here. Running `scripts/embedding_ab_benchmark.py` reproduces the
numbers.)