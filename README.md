# Домашнє завдання №7 — Перенесення workflow на framework (LangGraph)

## 1. Вибір framework і обґрунтування

**Обрано: LangGraph.**

Обґрунтування:
- Workflow з HW6 — це граф: спільний state, кроки (route → execute → synthesize) та **conditional routing** (3 routes). LangGraph відображає саме ці понятія: `StateGraph`, nodes як functions, conditional edges.
- State у LangGraph — TypedDict з partial updates: кожен node повертає лише ті поля, які змінює. Це один-в-один відповідає ручному накопиченню state з HW6.
- Вбудоване трасування (executed nodes, checkpointing, `graph.get_graph()`) — те, що в HW6 довелося робити вручну (`snapshot()` у кожному кроці).
- Альтернативи (LlamaIndex Workflow, CrewAI Flow, smolagents) орієнтовані на LLM-event-driven підхід і для детермінованого 5-node графа з mock-інструментами додають зайву абстракцію.

## 2. Схема графа

```
                    ┌────────────────────────────────────────────┐
                    │            classify_request                │
                    │  (route_query — ті самі rules з HW6)       │
                    └───────┬───────────────┬──────────────┬─────┘
                            │ conditional   │              │
            command_workflow┘    config_workflow     clarification
                            │               │                 │
                            └───────┬───────┘                 │
                    ┌───────────────▼────────────┐            │
                    │         build_answer       │            │
                    │ (synthesize_command/config)│            │
                    └───────────────┬────────────┘            │
                                    │                         │
                                   END                       END
```

## 3. State

```python
class AgentState(TypedDict, total=False):
    user_goal: str          # оригінальний запит
    selected_route: str      # command_workflow / config_workflow / clarification
    tool_calls: list         # [{name, args}]
    observations: list       # результати інструментів
    final_answer: str        # синтезована відповідь
    executed_nodes: list     # трасування виконаних node
```

Різниця проти HW6: `executed_nodes` — трасування графа (у HW6 це робив ручний `snapshot()` у `agent_run`). Кожен node повертає **partial dict** — LangGraph сам зливає оновлення в спільний state.

## 4. Nodes (5)

| Node | Функція | Оновлює поля |
|---|---|---|
| `classify_request` | Визначає route (імпорт `route_query` з HW6) | `selected_route`, ініціалізує `tool_calls/observations`, `executed_nodes` |
| `command_workflow` | Викликає `get_git_command` (extract_command з HW6) | `tool_calls`, `observations`, `executed_nodes` |
| `config_workflow` | Викликає `get_git_config` | `tool_calls`, `observations`, `executed_nodes` |
| `clarification` | Формує уточнювальне питання (без інструменту) | `final_answer`, `executed_nodes` |
| `build_answer` | Синтезує відповідь (`synthesize_command`/`synthesize_config` з HW6) | `final_answer`, `executed_nodes` |

Domain-код (route rules, mock-інструменти, synthesis) **імпортується з `agent_flow.py` (HW6)**, а не копіюється — той самий workflow, інша обгортка.

## 5. Edges

- **Conditional edge** після `classify_request` → функція `route_decision(state)` повертає `state["selected_route"]`, маппінг: `command_workflow → command_workflow`, `config_workflow → config_workflow`, `clarification → clarification`.
- Звичайні edges: `command_workflow → build_answer`, `config_workflow → build_answer`, `clarification → END`, `build_answer → END`.

## 6. Тестування (3 приклади)

Повні трасування — в `outputs/langgraph_examples.md` (input question, selected route, executed nodes, final state, final answer).

| # | Input | Route | Executed nodes | Інструмент |
|---|---|---|---|---|
| 1 | how do I stash my changes? | `command_workflow` | classify_request → command_workflow → build_answer | `get_git_command(stash)` |
| 2 | what is my git user.name? | `config_workflow` | classify_request → config_workflow → build_answer | `get_git_config(global)` |
| 3 | what is the best pizza recipe? | `clarification` | classify_request → clarification | — |

Поведення графа збігається з custom flow з HW6 (ті самі routes, інструменти, відповіді).

## 7. Порівняння: custom flow (HW6) vs LangGraph (HW7)

| Аспект | Custom flow | LangGraph |
|---|---|---|
| Складність коду | Простіше: один `agent_run()` з if/else | Більше boilerplate: TypedDict, `add_node`, `add_edge`, `compile`, partial updates |
| Видимість workflow | Не явна — треба читати `agent_run` | Граф описаний явно: nodes/edges видно у коді та через `graph.get_graph()` |
| Робота зі state | Вручну: одна dict, накопичується в циклі | TypedDict + partial updates — структура явна, merge робить runtime |
| Conditional routing | `if state["selected_route"] == ...` у коді кроку | Explicit conditional edge з маппінгом route → node |
| Debug/трасування | Ручний `snapshot()` у кожному кроці | Вбудоване (executed nodes, checkpointing), partial state після кожного node |
| Ризик помилок | Легко пропустити крок або забуднути оновити поле state | Runtime валідує graph (немає node для route → помилка при compile/invoke) |

**Що стало краще:**
- Routing явний: маппінг route → node замість розрісненого if/else по кроках.
- State структурований (TypedDict) і оновлюється partial-диктами — неможливо "забутити" поле, яке очікує наступний node.
- Трасування (`executed_nodes`, а за потреби — checkpointing) дається без ручного snapshot-коду.
- Граф легко розширювати: новий route = новий node + один рядок у conditional edge.

**Що стало складніше:**
- Boilerplate: TypedDict, `StateGraph`, `add_node` × 5, edges, `compile` — ~40 рядків "каркасу" для задачі, яка в custom flow помістилася б у 30.
- Кожному node потрібно знати формат partial update (які поля повертати), а не просто мутувати dict.
- Для детермінованого 5-node графа без LLM перевага framework переважно в читабельності, а не в функціональності.

**Висновок:** для задачі розміру HW6 (3 steps, 3 routes) framework додає boilerplate, але робить структуру явною і розширюваною. Вигід LangGraph починає зростати від 4+ routes, паралельних гілок (fan-out), циклів (retry/feedback loop) та checkpointing — усі ці можливості в custom flow доводилося би писати вручну. Для цього розміру задачі: **окрема, але не зайва** складність.

## 8. Як запустити

```bash
uv venv venv && uv pip install --python ./venv/bin/python langgraph
./venv/bin/python scripts/langgraph_flow.py
```

Результат: `outputs/langgraph_examples.md` + консольний summary (route → nodes для кожного з 3 запитів).