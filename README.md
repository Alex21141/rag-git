# Курсовий проєкт — Фінальне технічне доопрацювання chatbot-а

## 1. Слабка точка, яку виправлено

**Слабка точка:** `extract_command` (`scripts/agent_flow.py`) вважав за
команду **будь-яке слово з БД, що випадково зустрічається в запиті**.
Слово `commit` — і команда в БД, і дуже поширене *іменник-об'єкт* у
природних git-питаннях. До того ж `get_git_command` мав
substring-фаззійний збіг, який міг м'яко підсунути іншу команду, а вузол
command передавав у tool вигаданий аргумент `query[:20]`, коли команду не
було.

Результат — **впевнена неправильна відповідь** (найгірший тип помилки для
допоміжника):

| Запит | Система відповідала | Правильно |
|---|---|---|
| `how do I cherry-pick a commit?` | `git commit` (cherry-pick взагалі не в БД) | чесне «немає в базі» |
| `how do I undo my last commit…` | `git commit` (протилежне дії) | `git reset --soft HEAD~1` |
| `how do I deploy my app…` | tool з аргументом «how do i deploy my a» | чесний fallback |

Виміряно на eval з HW8 (10 кейсів, реальний виклик графа):
2 `wrong_retrieval` + 1 `wrong_routing`, success 70%.

## 2. Вибраний варіант покращення

Згідно з ТЗ, варіант покращення обирається **один на вибір** з
представленого переліку:

| Варіант | Обрано? | Чому |
|---|---|---|
| Fallback behavior | **так** | Частина вибраного зсуву: замість впевненої помилки — чесне «не можу визначити команду» + перелік доступних |
| Simple guardrail | **так** | Частина вибраного зсуву: перевірка перед tool call — без впевненої команди tool не викликається (раніше — аргумент `query[:20]`) |
| Improved tool call | частково | Аргумент `command` тепер тільки з закритого набору ключів `GIT_COMMANDS`; прибрано substring-фаззі |
| Retry для read операцій | ні | У системі немає I/O-помилк: обидва tool детерміновані (вбудована БД + `git config`), нетранспортних помилок, які варто повторювати, немає |
| State handling | ні | Агент одноразовий: одне звернення = одна відповідь, між репліками нічого зберігати |
| Кращий routing | ні | Router працював **правильно** — усі команди йшли в command_workflow (це і має бути). Хибним був *екстрактор всередині* маршруту, а не вибір маршруту; зміна router — це вже інша слабка точка |
| Better prompt | ні | Production-граф без LLM (детермінований, 1 ms) — промпту там немає; LLM-екстрактор існує лише в демо-режимі HW8 `--llm` |
| Metadata filtering | ні | Стосується retrieval-шару HW2/HW3, який за рішенням залишено без змін (підтверджено A/B-бенчмарком, розділ 4) |

**Висновок:** обрано цілісне покращення, яке покриває *одну* реальну
слабку точку (впевнені неправильні відповіді) і складається з
*Simple guardrail* + *Fallback behavior* (+ частково *Improved tool call*):
guardrail без fallback — це тиша, а fallback без guardrail — чесна
відповідь, але tool із сміт-аргументом все одно псує trace. Разом це
єдине змінює поведінку на тих самих кейсах, де система найгірше
підводила.

### Реалізація

1. **Intent-based extraction** — команда повертається лише за сильним
   сигналом: експліцитний `git <cmd>`, відома intent-фраза
   (`INTENT_PHRASES`: «undo my last commit» → `reset`, «amend my last
   commit» → `commit`), команда одразу після маркера інтенції
   («how do I <cmd>», «як зробити <cmd>»), безпечні phrase-hints
   («recent commits graph» → `log`). Правило «будь-яке слово з БД у запиті»
   прибрано.
2. **Guardrail перед tool call** (в HW6 `agent_run` і HW7 LangGraph-вузлі
   `run_command_workflow`) — без впевненої команди tool **не викликається**;
   в графі додано умовний edge: fallback іде одразу в END (не в
   `build_answer`, який очікує observation).
3. **Чесний fallback** (`COMMAND_FALLBACK`) — замість впевненої помилки
   система каже, що не змогла визначити команду, і перелічує доступні.
4. **Безпечний збіг у tool** — substring-фаззі в `get_git_command`
   видалено; залишено лише exact після нормалізації + plural→singular.

## 3. Before / after (реальний виклик, eval set з HW8)

| Кейс | Before | After |
|---|---|---|
| `cherry-pick a commit` | впевнено `git commit` (wrong_retrieval) | чесний fallback + перелік команд |
| `undo my last commit…` | `git commit` (wrong_retrieval) | `git reset`, приклад `--soft HEAD~1` |
| `deploy my app…` | tool з вигаданим аргументом | guardrail, чесний fallback |

Метрики (10 кейсів):

| | Before (hw8) | After (final) |
|---|---|---|
| Success | 7/10 (70%) | 9/10 (90%) |
| Failures | 2/10 | **0/10** |
| Groundedness bad | 2/10 | **0/10** |
| wrong_retrieval / wrong_routing | 2 / 1 | **0 / 0** |
| Середня затримка | 1 ms | 1 ms (без LLM — без втрат) |

Регресій немає: 6 «зелених» кейсів дають ідентичні відповіді.

Повне обґрунтування, повний changelog та чесний перелік
remaining limitations — у **`FINAL_IMPROVEMENT.md`**.

## 4. A/B/C бенчмарк embedding-моделей (додаткове дослідження)

Після зауваження, що `all-MiniLM-L6-v2` (384d) не спеціалізована для
технічного контенту, проведено бенчмарк на **реальних даних**: ті самі
145 чанків GitLab-КБ і ті самі 10 test-запитів HW2 (`scripts/retrieval.py`).
Три моделі: A = MiniLM-L6-v2 (384d, production), B = bge-small-en-v1.5
(384d, drop-in), C = nomic-embed-text-v1.5 (768d, instruction-tuned,
не drop-in). Скрипт: `scripts/embedding_ab_benchmark.py`, звіт:
`outputs/embedding_ab.md` + `.csv`.

| Метрика | A: MiniLM (384d) | B: bge-small (384d) | C: nomic (768d) |
|---|---|---|---|
| Середній top-1 cosine | 0.6642 | **0.8126** | 0.7256 |
| Середній margin (top1-top2) | 0.0388 | 0.0377 | 0.0209 |
| Коректний документ (ручне) | 9/10 | 9/10 | **10/10** |
| Build індексу | 1.5s | 2.8s | 11.8s |
| Drop-in (384d)? | — (поточна) | **так** | ні (768d) |

**Висновок:** на рівні документів усі три моделі близькі (9–10/10),
різниця — у точності чанка та калібрації балів. B — найкраща
single-model опція (калібрація + найточніші чанки на tutorial-запитах +
drop-in). C — справді сильна (найкращі Q1 «clone» і Q7 «history»), але
**net-виграшу не дає**: ніде не б'є bge, де та вже точна, найслабший
margin (гірший rerank-сигнал для гібриду), удвічі більший індекс і
потребує змін коду (768d). Її переваги (8K контекст, мультилінгва) для
145 коротких чанків GitLab неактуальні. Реальна слабкість MiniLM —
загальні інтро-чанки замість точного туторіалу (видно на Q1/Q2/Q7) —
саме це B виправляє. **Рішення: залишити all-MiniLM-L6-v2 як є**;
bge-small — визначений drop-in варіант на майбутнє, nomic — виміряна
альтернатива. Деталі — `outputs/embedding_ab.md`.

## 5. Як запустити

```bash
./venv/bin/python scripts/agent_flow.py        # HW6: 5 demo traces
./venv/bin/python scripts/langgraph_flow.py    # HW7: 3 route tests
./venv/bin/python scripts/eval_observability.py  # HW8: eval 10 кейсів
./venv/bin/python scripts/embedding_ab_benchmark.py  # A/B embedding (torch + sentence-transformers)
```

## 6. Що залишилось (коротко, повністю — в FINAL_IMPROVEMENT.md)

- Intent-мапа покриває кейси з eval; інші перефразування («скасувати
  останній комміт», «revert the previous commit») обробляються **безпечно**
  (чесний fallback), але не вирішуються — розширення мапи або `--llm`
  екстрактор (HW8) перетворять ці відмови на правильні відповіді.
- В БД досі немає `cherry-pick`, `revert`, `reflog` — це механічне
  доповнення `GIT_COMMANDS`, окрема зміна.
- Router досі надмірно направляє «how do i …» в command_workflow; його
  ловить guardrail, а не router. Негативний сигнал у router — свідомо
  не включено, щоб змінити саме одну вибрану слабку точку.