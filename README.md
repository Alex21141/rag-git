# Домашнє завдання №8 — Evaluation + Observability layer

## 1. Що робить шар спостереження

До системи з HW7 (LangGraph git-агент) додано мінімальний шар спостереження
й оцінювання якості: eval set із 10 запитів, автозапуск реального графа,
збір результатів у структуровану таблицю, розрахунок метрик і quality report.

- Скрипт: `scripts/eval_observability.py`
- Таблиця: `outputs/eval_results.csv` (також `eval_results.md`)
- Метрики: `outputs/eval_summary.md`
- Повні трасування: `outputs/eval_raw.json`
- Звіт: `outputs/quality_report.md`
- Опційно: `--llm` — LLM-інтент-екстрактор (Nemotron 3 Nano 30B A3B через
  OpenRouter, той самий підхід, що HW4); проведено: 6/6

## 2. Composition eval set (10 запитів)

| # | Сценарій | Приклад |
|---|---|---|
| 1–4 | Просте питання з knowledge base | «how do I stash my changes?» |
| 3 | Питання, де потрібен tool (phrase → команда) | «show me recent commits graph» → `log` |
| 5–6 | Питання, де потрібен retrieval (live config, global/local) | «what is my git user.name?» |
| 7 | Питання, де retrieval може помилитися (команда не в БД) | «how do I cherry-pick a commit?» |
| 8 | Agent має сказати «не знаю» / уточнити | «what is the best pizza recipe?» |
| 9–10 | Складне / неоднозначне (trap-кейси) | «undo my last commit but keep the changes» |

Ground truth (яку команду має видобути система) закладено в
`INTENT` map всередині скрипту.

## 3. Як запустити

```bash
./venv/bin/python scripts/eval_observability.py          # eval
export OPENROUTER_API_KEY=***
./venv/bin/python scripts/eval_observability.py --llm    # + LLM-демо
```

`--llm` використовує той самий підхід, що HW4 (`scripts/rag_answer.py`):
OpenRouter + `nvidia/nemotron-3-nano-30b-a3b` (Nemotron 3 Nano 30B A3B),
`reasoning` увімкнено, фолбек на `reasoning_details` (у Nano Nemotron
`content` буває None). Ключ — з `OPENROUTER_API_KEY`, не зберігається
в репо. Зауваження: `:free`-варіант моделі OpenRouter вимкнено,
тому за замовчуванням платний slug (той самій моделі).
Для eval без LLM жодних зовнішніх залежностей не потрібно.

## 4. Результати (реальний виклик)

```
Total cases: 10
Success rate: 7/10 = 70%
Partial success: 1/10 = 10%
Failure rate: 2/10 = 20%

Groundedness good: 7/10 = 70%
Groundedness bad: 2/10 = 20%

Average latency: 1 ms
Max latency: 4 ms (config-кейс — subprocess)

Error types:
  none: 7
  wrong_retrieval: 2
  wrong_routing: 1
```

Route-розподіл: command 7, config 2, clarification 1.

### LLM-демо (реальний прогон, Nemotron 3 Nano 30B A3B через OpenRouter)

| id | question | regex (фактично) | intended | Nemotron (LLM) |
|----|----------|------------------|----------|----------------|
| 7 | how do I cherry-pick a commit? | `commit` | `cherry-pick` | `cherry-pick` ✅ |
| 9 | undo my last commit but keep the changes? | `commit` | `reset` | `reset` ✅ |
| 1–4, 6 | прямі командні запити | правильні | — | правильні ✅ |

**6/6** command-кейсів повернули інтентовану команду — LLM-екстрактор
вирішує обидва trap-кейси, які regex давав неправильно. Деталі:
`outputs/llm_intent_demo.md`.

## 5. Аналітичні висновки: де працює добре, а де ні

**Працює добре:**
- Прямі командні запити (stash/rebase/log/push) — точний route + точний
  extract, 4/4.
- Phrase-маршрутизація («commits graph» → `log`) — механізм з HW6 спрацював.
- Config-retrieval із scope-детекцією (global/local) — відповідь ґрунтується
  на реальних значеннях `git config`.
- Out-of-domain («pizza recipe») — правильне уточнювальне питання без
  інструменту.
- Latency ~1 ms: deterministic pipeline дає нульовий network-хвіст,
  на відміну від 1.5–3 s у LLM-based RAG.

**Працює погано:**
- Кейс 7: `cherry-pick` не в БД → extract бере слово `commit` з самого
  запиту → агент **впевнено** віддає інформацію про `git commit` без жодного
  маркера невпевненості (silent wrong answer — найнебезпечніший тип помилки).
- Кейс 9: «undo my last commit but keep the changes» → правильна відповідь
  `git reset --soft HEAD~1`, regex бере перше збігнуте слово `commit`.
- Кейс 10: «how do I deploy my app to a server?» → маркер «how do i» кидає
  запит в command_workflow замість clarification; додатковий баг — fallback
  передає урізаний запит `query[:20]` як аргумент `command`.

**3 головні проблеми:**
1. Word-extract без інтент-розуміння: повний словник команди в запиті дає
   впевнену неправильну відповідь (кейс 7) — потрібен exact/fuzzy-маркер
   у відповіді інструмента і чесний «немає в базі».
2. Regex-екстрактор не розуміє інтенцію («undo» → `reset`): LLM-екстрактор
   (`--llm`) проведено — 6/6, включаючи цей кейс.
3. Router не має negative-сигналів: запит без жодного git-маркера все одно
   йде в command_workflow (кейс 10) — потрібне «жодного маркера →
   clarification» і не передавати урізаний запит як аргумент.

**Наступний крок:** після трьох виправлень перепуск того ж eval set
(скрипт відтворюваний, deterministic — diff CSV між коммітами покаже
регресію/покращення); очікуваний success 7/10 → 9/10.

## 6. Як оцінюється (scoring)

- `task_success` / `groundedness` / `answer_quality` — порівняння
  **фактичного** результату (route, tool args, observation) з ground truth
  з eval set; жодне значення не вигадане — усі колонки `answer`,
  `retrieved_chunks`, `route_or_mode`, `tools_used`, `latency_ms`
  записані з реального виклику.
- Типи помилок: `none`, `wrong_retrieval` (неправильна команда),
  `wrong_routing` (офтоп замість clarification).
- Обмеження: система deterministic, тому порівняння з ground truth
  достатнє; для LLM-систем потрібен LLM-as-a-judge (відмічено у звіті).

## 7. Структура проекту (HW8)

```
scripts/eval_observability.py   — eval-харнес (10 кейсів, метрики, LLM-демо)
outputs/eval_results.csv        — повна eval table (13 колонок)
outputs/eval_results.md         — та сама таблиця, Markdown
outputs/eval_summary.md         — observability metrics
outputs/eval_raw.json           — повні трасування (для відтворюваності)
outputs/quality_report.md       — quality report (3 проблеми, next steps)
outputs/llm_intent_demo.md      — (опційно, --llm) LLM-інтент-екстрактор
```

Посилання на базову систему: гілка `hw7-langgraph` (граф, вузли, тести).