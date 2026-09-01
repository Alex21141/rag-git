# Quality Report — Git Tutoring Agent (HW8)

## Що тестувалося

Git tutoring assistant з HW6/HW7 (LangGraph-граф: `classify_request` →
`command_workflow` | `config_workflow` | `clarification` → `build_answer`),
10 test questions, що покривають усі вимогові сценарії:

| Сценарій | Кейси |
|---|---|
| Просте питання з knowledge base (14 git-команд) | 1–4 |
| Питання, де потрібен retrieval (live config) | 5–6 |
| Питання, де retrieval може помилитися (команда не в БД) | 7 |
| Питання, де agent має сказати «не знаю» / уточнити | 8 |
| Питання, де потрібен tool | 3, 5 |
| Складне/неоднозначне (trap-кейси) | 9–10 |

Система **deterministic** (без LLM у циклі): routing — keyword rules,
extract — regex word match + phrase hints, tools — mock DB + subprocess.
Тому eval відтворюваний: кожен перезапуск дає ідентичні результати.

## Результати (реальний виклик, `outputs/eval_results.csv`)

- **Success rate: 7/10 = 70%** (partial 1, fail 2)
- **Groundedness good: 7/10 = 70%**, bad: 2/10
- **Average latency: 1 ms**, max 4 ms (config-кейс 6 ms — subprocess)
- Error types: `none` 7, `wrong_retrieval` 2, `wrong_routing` 1
- Route distribution: command 7, config 2, clarification 1

## Де система працює добре

1. **Прямі командні питання** (кейси 1–4): точний route, точний extract
   (`stash`, `rebase`, `log`, `push`), відповідь повністю підтримана
   observation — 4/4.
2. **Phrase-маршрутизація** (кейс 3): «recent commits graph» → `git log`
   завдяки `PHRASE_HINTS` — механізм, який ми додавали в HW6, працює.
3. **Config retrieval** (кейси 5–6): scope-детекція (global/local) коректна,
   відповідь ґрунтується на реальних `git config` значеннях.
4. **Out-of-domain clarification** (кейс 8): «pizza recipe» → уточнювальне
   питання без виклику інструменту — правильна поведінка «не знаю».
5. **Latency**: deterministic pipeline дає ~1 ms на кейс — нульовий
   network-хвіст, порівняно з 1.5–3 s у LLM-based RAG (див. приклад у ТЗ).

## Де система падає

1. **Наївний word-extract + повний словник команди = впевнена неправильна
   відповідь** (кейс 7): `cherry-pick` не в БД, а `extract_command` бере
   слово `commit`, яке є в запиті («cherry-pick **a commit**») і в БД —
   агент віддає інформацію про `git commit` на запит про `cherry-pick`
   без жодного маркера невпевненості. Це не помилка, а *silent wrong
   answer*: жодного «ближча команда» чи «немає в базі».
2. **Наївний word-extract на неоднозначних запитах** (кейс 9):
   «undo my last commit but keep the changes» — правильна відповідь
   `git reset --soft HEAD~1`, regex же бере перше збігнуте слово `commit`
   і віддає `git commit`. Контрпродуктивно: показує як зробити commit,
   коли користувач хоче його скасувати.
3. **False-positive routing** (кейс 10): «how do I deploy my app to a
   server?» — маркер «how do i» кидає запит у `command_workflow`, extract
   не знаходить команду (arg = урізаний запит «how do I deploy my a» —
   окремий баг: `query[:20]` передається як «command»), fallback «not
   found» чесний, але route мав бути `clarification`.

## 3 головні проблеми

1. **Substring fuzzy match в `get_git_command` повертає суміжну, а не
   найближчу, команду і не позначає, що це approx-match** — у кейсі 7
   агент відповів про `commit` на запит про `cherry-pick` без жодного
   маркера невпевненості. Це найнебезпечніша поведінка: не помилка, а
   *впевнена неправильна відповідь* (silent wrong answer).
   Виправлення: fuzzy match повертати `match: exact|fuzzy` у JSON і
   показувати це в відповіді («ближча команда: ...»).
2. **`extract_command` — пошук першого збігненого слова, без розуміння
   інтенції** — кейс 9 («undo last commit» → `commit` замість `reset`).
   Правила `PHRASE_HINTS` закривають лише випадки, які хтось вручну
   додав. Виправлення: розширити phrase-hints (undo→reset,
   history→log...) або замінити на LLM-екстрактор — сценарій реалізовано
   як опційний `--llm` режим `eval_observability.py` (LLM читає весь
   запит і повертає інтентовану команду; trade-off: сотні ms на замість
   ~0 ms, для 14-командного домену це прийнятно).
3. **Router не має negative-сигналів: «how do i X» без жодного git-маркера
   все одно йде в `command_workflow`** (кейс 10) — замість clarification
   користувач отримує «команду не знайдено». Додатковий баг-симвом:
   fallback `query[:20]` передає урізаний запит як аргумент `command`.
   Виправлення: якщо `extract_command` повернуло None і в запиті немає
   жодного git-маркера — маршрутизувати в `clarification`, а не в tool.

## Що покращити наступним кроком

1. Exact/fuzzy match-маркер в `get_git_command` + чесний «not found»
   замість підсунутої суміжної команди (закриває кейс 7 — найгірший
   за ризиком).
2. Intent-based extract: розширені phrase-hints або LLM-екстрактор
   (`--llm` режим уже написаний і готовий до порівняльного прогону).
3. Negative routing: жодного git-маркера → `clarification` (закриває
   кейс 10) + не передавати урізаний запит як аргумент інструменту.
4. Після виправлень — перепуск цього ж eval set: очікуваний success
   7/10 → 10/10 (кейс 9 залишиться partial, якщо не впровадити LLM,
   бо `reset` не згадано в запиті прямо — це і є аргумент на користь
   LLM-екстрактора).

## Оцінка спостережуваності (meta)

- Traces (executed_nodes, tool_calls, observations) збиралися без
  додаткових змін — стан графа з HW7 вже є мінімальним observability
  шаром; eval просто додав затримки та автоматичну оцінку.
- Deterministic система зробила eval дешевим: 10 кейсів за ~0.1 с,
  регресія бачиться одразу (diff CSV між коммітами).
- Обмеження: scoring порівнює реальний результат з ground truth,
  закладеним в eval set (INTENT map) — для production-системи з LLM
  потрібен LLM-as-a-judge або ручна верифікація, бо відповіді
  нондетерміновані.