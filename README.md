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

## 2. Що реалізовано

Одне цілісне покращення навколо цієї однієї слабкої точки (комбінація
варіантів *Improved tool call* + *Simple guardrail* + *Fallback behavior*):

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

## 4. A/B бенчмарк embedding-моделей (додаткове дослідження)

Після зауваження, що `all-MiniLM-L6-v2` (384d) не спеціалізована для
технічного контенту, проведено A/B на **реальних даних**: ті самі 145
чанків GitLab-КБ і ті самі 10 test-запитів HW2 (`scripts/retrieval.py`).

| Метрика | A: MiniLM-L6-v2 | B: bge-small-en-v1.5 |
|---|---|---|
| Середній top-1 cosine | 0.6642 | **0.8127** |
| Top-1 за якістю (ручне читання чанків) | 3 / 3 / 4 нічиї | 3 / 3 / 4 нічиї |

**Висновок:** це не «10 до 0». Перемоги B — за *приземленням на тему*
(B віддає точну главу, A — загальний інтро); перемоги A — за *глибиною*
(B бирає нішевий суб-чанк тої самої глави замість опенеру). Калібрація
балів чітко на боці B (вищі і розрізненіші cosine → краще для пере-ранкінгу
в гібриді HW3). B — та сама 384d, введення drop-in (`MODEL_NAME` +
перебудова індексу за ~3 с). **Рекомендація: bge-small-en-v1.5 для
semantic-ноги гібридного пошуку.** Деталі — `outputs/embedding_ab.md`.

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