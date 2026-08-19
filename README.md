# Домашнє завдання №6 — Перша agentic-структура

## 1. Область застосування та use case

**Область:** Інструкція та конфігурація Git-команд
**Use case:** Користувач запитує "як зробити X в git?" або "що налаштовано у моєму git Y?". Агент маршрутизує запит до правильного інструменту.

## 2. Інструменти (2)

| # | Назва | Опис | Параметри |
|---|---|---|---|
| 1 | `get_git_command` | Отримати структуровану інформацію про Git-команду: синтаксис, опис, приклади. Використовується коли користувач запитує про конкретну git-команду або "як зробити X". | `command` (назва git-команди) |
| 2 | `get_git_config` | Отримати значення Git-налаштувань для заданого рівня (global або local). Використовується коли користувач запитує про свої налаштування git. | `scope` (global/local) |

## 3. Правила маршрутизації

| Правило (regex) | Інструмент |
|---|---|
| `(how\|як\|как).*(clone\|push\|merge\|rebase\|stash\|reset\|checkout\|branch\|log\|status\|diff\|commit\|add)` | `get_git_command` |
| `(what\|який\|какой).*(clone\|push\|merge\|rebase\|stash\|reset\|checkout\|branch\|log\|status\|diff\|commit\|add)` | `get_git_command` |
| `git\s+(clone\|push\|merge\|rebase\|stash\|reset\|checkout\|branch\|log\|status\|diff\|commit\|add)` | `get_git_command` |
| `(config\|setting\|user\.name\|user\.email\|core\|push\.default)` | `get_git_config` |

Запити, що не відповідають жодному правилу — повертають загальну відповідь без виклику інструмента.

## 4. Agentic-робочий процес

```
Запит → Маршрутизація (keyword rules) → Виконання (інструмент) → Спостереження → Синтез → Остаточна відповідь
```

Парсинг параметрів — keyword extraction з вбудованої бази даних (14 git-команд).

## 5. Приклади трасування (5)

Див. `outputs/agent_flow_examples.md`

| # | Запит | Маршрут | Інструмент | Результат |
|---|---|---|---|---|
| 1 | how do I stash my changes? | `get_git_command` | `get_git_command(stash)` | Синтаксис + приклади ✅ |
| 2 | how do I rebase onto main? | `get_git_command` | `get_git_command(rebase)` | Синтаксис + приклади ✅ |
| 3 | what is my git user.name? | `get_git_config` | `get_git_config(global)` | Налаштування ✅ |
| 4 | how do I clone a repo with shallow history? | `get_git_command` | `get_git_command(clone)` | Синтаксис + `--depth=1` ✅ |
| 5 | show me recent commits graph | `get_git_command` | `get_git_command(log)` | `--graph --all --oneline` ✅ |

## 6. Висновки

**Що працює добре:**
- Keyword-маршрутизація — проста, швидка, не залежить від LLM
- Вбудована база даних git-команд — не потребує зовнішніх залежностей
- `get_git_config` через subprocess — повертає реальні налаштування системи

**Що не працює добре:**
- Маршрутизація не покриває всі варіанти запитів (наприклад "як скасувати останній коміт" не потрапляє в жодне правило)
- Однокроковий агент — не може ланцюжувати кілька інструментів

**Наступні кроки:**
- Додати семантичну маршрутизацію (embedding-based) як fallback після keyword rules
- Реалізувати багатокроковий агент: наприклад `get_git_command(reset)` → пояснити → `get_git_command(revert)` для порівняння
- Покрити правила маршрутизації ширшим набором синтактичних конструкцій

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