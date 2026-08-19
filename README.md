# Домашнє завдання №6 — Перша agentic-структура

## 1. Область застосування та use case

**Область:** Інструкція та конфігурація Git-команд
**Use case:** Користувач запитує "як зробити X в git?" або "що налаштовано у моєму git Y?". Агент маршрутизує запит до правильного workflow і інструменту.

## 2. Схема workflow

```
Запит
→ Router (deterministic keyword rules, без LLM)
  → [A] command_workflow → get_git_command → Observation → Synthesis → Answer
  → [B] config_workflow  → get_git_config  → Observation → Synthesis → Answer
  → [C] clarification    → (без інструмента) → уточнювальне питання
```

Три кроки:
1. **Route** — вибір одного з трьох workflow
2. **Execute** — виклик інструмента (крок 3 для route C пропускається)
3. **Synthesize** — observation перетворюється на відповідь природною мовою

## 3. Routes (3)

| Route | Умова активації | Інструмент |
|---|---|---|
| `command_workflow` | У запиті є назва git-команди (word boundary) або маркер командного питання ("як зробити", "how do I", "commits", "graph") | `get_git_command` |
| `config_workflow` | У запиті є ключові слова налаштувань: "config", "setting", "user.name", "user.email", "core.", "push.default" | `get_git_config` |
| `clarification` | Запит не відповідає жодному правилу | — (запит уточнення) |

Правила перевіряються детерміновано, без LLM. Route B (config) має пріоритет — найспецифічніші ключові слова.

## 4. Інструменти (2, mock)

| # | Назва | Опис | Параметри |
|---|---|---|---|
| 1 | `get_git_command` | Отримати структуровану інформацію про Git-команду: синтаксис, опис, приклади. Вбудована база 14 git-команд (з HW5) — фіксований результат, без зовнішніх API. | `command` (назва git-команди) |
| 2 | `get_git_config` | Отримати значення Git-налаштувань для заданого рівня (global або local). | `scope` (global/local) |

## 5. State

State передається між кроками workflow і накопичується:

```json
{
  "user_goal":      "оригінальний запит користувача",
  "selected_route": "command_workflow | config_workflow | clarification",
  "tool_calls":     [ { "name": "...", "args": { ... } } ],
  "observations":   [ "результат інструмента (JSON)" ],
  "final_answer":   "синтезована відповідь"
}
```

- Після **Step 1**: заповнено `selected_route`
- Після **Step 2**: додано записи в `tool_calls` та `observations`
- Після **Step 3**: заповнено `final_answer`

У `outputs/agent_flow_examples.md` для кожного прикладу наведено state після кожного кроку — видно, як state наповнюється з кроку в крок.

## 6. Реалізація

- Скрипт: `scripts/agent_flow.py`
- Запуск: `python3 scripts/agent_flow.py`
- Результат: `outputs/agent_flow_examples.md`

## 7. Приклади трасування (5)

Див. `outputs/agent_flow_examples.md`

| # | Запит | Route | Інструмент | Результат |
|---|---|---|---|---|
| 1 | how do I stash my changes? | `command_workflow` | `get_git_command(stash)` | Синтаксис + приклади ✅ |
| 2 | how do I rebase onto main? | `command_workflow` | `get_git_command(rebase)` | Синтаксис + приклади ✅ |
| 3 | what is my git user.name? | `config_workflow` | `get_git_config(global)` | Налаштування ✅ |
| 4 | show me recent commits graph | `command_workflow` | `get_git_command(log)` | `--graph --all --oneline` ✅ |
| 5 | what is the best pizza recipe? | `clarification` | — | Уточнювальне питання 🟡 |

Приклади 1–2 покривають route A, 3 — route B, 5 — route C. Приклад 4 показує контекстний вибір команди: "commits" + "graph" → `log` (а не `commit`).

## 8. Висновки

**Що працює добре:**
- Детермінована keyword-маршрутизація — проста, швидка, не залежить від LLM
- Три route з явним state — видно, як workflow накопичує контекст між кроками
- Вбудована база даних git-команд — не потребує зовнішніх залежностей
- Word-boundary парсинг + phrase hints розрізняють "commits" (→ `log`) і "commit" (→ `commit`)

**Що не працює добре:**
- Маршрутизація не покриває всі мовні конструкції (наприклад "як скасувати останній коміт" без прямої назви команди потрапляє в clarification)
- Single-step агент — викликає лише один інструмент за запит, не ланцюгує кілька

**Наступні кроки:**
- Додати семантичну маршрутизацію (embedding-based) як fallback після keyword rules
- Реалізувати multi-step agent: наприклад `get_git_command(reset)` → пояснити → `get_git_command(revert)` для порівняння
- Покрити routing rules ширшим набором синтактичних конструкцій

## Структура проєкту

```
├── .gitignore
├── README.md
├── data/
│   └── sources/           # джерельні документи (індексовані на HW1)
├── index/
│   └── ...                # FAISS індекси (створені на HW1–HW2)
├── outputs/
│   ├── agent_flow_examples.md   # 5 трасувань agent-flow (HW6)
│   ├── rag_answers_examples.md  # RAG відповіді (HW4)
│   ├── retrieval_examples.md    # Retrieval приклади (HW2–HW3)
│   └── tool_examples.md         # Tool приклади (HW5)
└── scripts/
    ├── agent_flow.py            # HW6: agent workflow (router + tools)
    ├── external_tool.py         # HW5: external tool integration
    ├── download_sources.py      # HW1: source preparation
    ├── prepare_knowledge_base.py # HW1: KB preparation
    ├── validate_chunks.py       # HW1: chunk validation
    ├── retrieval.py             # HW2–HW3: semantic retrieval
    └── rag_answer.py            # HW4: RAG answer generation
```