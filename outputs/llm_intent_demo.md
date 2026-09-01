# HW8 — LLM intent-extraction demo (next-step scenario)

Scenario: replace the naive `extract_command` (regex word match) with an LLM call. The LLM reads the WHOLE question and returns the intended command. Evaluated on the command cases of the eval set.

| id | question | actual (regex) | intended | LLM output | verdict |
|----|----------|----------------|----------|------------|---------|
| 1 | how do I stash my changes? | `stash` | `stash` | `stash` | ✅ fixed |
| 2 | how do I rebase onto main? | `rebase` | `rebase` | `rebase` | ✅ fixed |
| 3 | show me recent commits graph | `log` | `log` | `log` | ✅ fixed |
| 4 | git push --force-with-lease | `push` | `push` | `push` | ✅ fixed |
| 7 | how do I cherry-pick a commit? | `commit` | `cherry-pick` | `cherry-pick` | ✅ fixed |
| 9 | how do I undo my last commit but keep the changes? | `commit` | `reset` | `reset` | ✅ fixed |

**Result:** 6/6 command cases would return the intended command.

Latency trade-off: each extraction becomes an LLM call (hundreds of ms vs ~0 ms), so this is a quality/latency trade — appropriate for a small, ambiguous command set like git.
