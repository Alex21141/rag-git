# Домашнє завдання №6 — Перша agentic-структура

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

## 1. Domain area і use case

**Domain:** Git command reference and configuration

**Use case:** User asks "how do I X in git?" or "what is my git setting Y?".
         The agent routes the question to the correct tool.

## 2. Tools (2)

| # | Назва | Опис | Параметри |
|---|---|---|---|
| 1 | `get_git_command` | Get structured information about a Git command (synopsis, description, examples). Use when user asks about a specific git command or 'how do I X'. | `command` (git command name) |
| 2 | `get_git_config` | Get Git configuration values for a given scope (global or local). Use when user asks about their git settings or configuration. | `scope` (global/local) |

## 3. Routing rules

| Правило (regex) | Інструмент |
|---|---|
| `(how\|як\|как).*(clone\|push\|merge\|rebase\|stash\|reset\|checkout\|branch\|log\|status\|diff\|commit\|add)` | `get_git_command` |
| `(what\|який\|какой).*(clone\|push\|merge\|rebase\|stash\|reset\|checkout\|branch\|log\|status\|diff\|commit\|add)` | `get_git_command` |
| `git\s+(clone\|push\|merge\|rebase\|stash\|reset\|checkout\|branch\|log\|status\|diff\|commit\|add)` | `get_git_command` |
| `(config\|setting\|user\.name\|user\.email\|core\|push\.default)` | `get_git_config` |

Запити, що не відповідають жодному правилу — повертають загальну відповідь без виклику інструмента.

## 4. Agent workflow

```
Query → Route (keyword rules) → Execute (tool) → Observe → Synthesize → Final Answer
```

Парсинг параметрів — keyword extraction з вбудованої DB (14 git-команд).

## 5. Trace examples (5)

Див. `outputs/agent_flow_examples.md`

| # | Запит | Route | Tool | Результат |
|---|---|---|---|---|
| 1 | how do I stash my changes? | `get_git_command` | `get_git_command(stash)` | Synopsis + examples ✅ |
| 2 | how do I rebase onto main? | `get_git_command` | `get_git_command(rebase)` | Synopsis + examples ✅ |
| 3 | what is my git user.name? | `get_git_config` | `get_git_config(global)` | Config settings ✅ |
| 4 | how do I clone a repo with shallow history? | `get_git_command` | `get_git_command(clone)` | Synopsis + `--depth=1` example ✅ |
| 5 | show me recent commits graph | `get_git_command` | `get_git_command(log)` | `--graph --all --oneline` ✅ |

## 6. Lessons learned

**Що працює добре:**
- Keyword routing — простий, швидкий, без залежностей від LLM
- Вбудована DB git-команд — не потребує зовнішніх залежностей
- `get_git_config` через subprocess — повертає реальні налаштування системи

**Що не працює добре:**
- Routing не покриває всі варіанти запитів (наприклад "як скасувати останній коміт" не потрапляє в жодне правило)
- Single-step agent — не може ланцюжувати кілька інструментів

**Наступні кроки:**
- Додати semantic routing (embedding-based) як fallback після keyword rules
- Реалізувати multi-step agent: наприклад `get_git_command(reset)` → пояснити → `get_git_command(revert)` для порівняння
- Покрити routing rules ширшим набором синтактичних конструкцій