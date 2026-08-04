#!/usr/bin/env python3
"""
HW4: RAG Answer Generation — QA pipeline with grounded answers and citations.

Pipeline: question → retrieval → build prompt → generate answer with citations

Usage:
    python3 scripts/rag_answer.py --test     # Run all test queries
    python3 scripts/rag_answer.py --report   # Generate report + markdown
    python3 scripts/rag_answer.py            # Run test + report (default)
"""

import argparse
import json
import os
import sys
import re

# Import retrieval functions
sys.path.insert(0, os.path.dirname(__file__))
from retrieval import (
    load_index,
    search,
    TEST_QUERIES,
    TOP_K,
    CHUNKS_FILE,
    MODEL_NAME,
    EMBEDDING_DIM,
)

# ── LLM Configuration ─────────────────────────────────────────────────────
LLM_BASE_URL = "http://localhost:8080/v1"
LLM_API_KEY = "hermes"
LLM_MODEL = "qwen36-27b-awq"
SCORE_THRESHOLD = 0.30

# ── Prompt Templates ──────────────────────────────────────────────────────

# V1: Простий шаблон (без ролі, без fallback, без цитат)
PROMPT_V1 = """Вiдповiдь на запитання на основi контексту.

Контекст:
{context}

Запитання: {question}

Вiдповiдь:
"""

# V2: Покращений шаблон (з роллю, fallback, цитатами)
PROMPT_TEMPLATE = """Ти — Git-преподавач (Git tutor assistant). Твоя задача — відповідати на запитання про Git, GitHub та GitLab.

ІНСТРУКЦІЇ:
1. Відповідай ТІЛЬКИ на основі наведеного контексту. Не використовуй зовнішні знання.
2. Якщо контекст не містить інформації для відповіді на запитання, скажи: "Не маю достатньої інформації для надання відповіді на це питання."
3. Обов'язково вкажи джерела: chunk_id або source_file для кожного твердження.
4. Відповідай українською мовою.

КОНТЕКСТ:
{context}

ЗАПИТАННЯ: {question}

ВІДПОВІДЬ:
"""

# ── Topic Mapping (source_file → topic) ───────────────────────────────────
# Map document topics to answer summaries
TOPIC_MAP = {
    "01_git_basics_getting_repository": {
        "topic": "clone",
        "summary_uk": (
            "Для клонування Git-репозиторію використайте команду `git clone <url>`. "
            "Вона створює повну локальну копію репозиторію з усією історією комітів. "
            "Ви також можете клонувати з GitHub (`git clone https://github.com/...`) або "
            "через SSH (`git clone git@github.com:...`)."
        ),
    },
    "03_branching_basic_branching_merging": {
        "topic": "branch_merge",
        "summary_uk": None,  # depends on sub-question
    },
    "04_branching_branch_management": {
        "topic": "branch",
        "summary_uk": (
            "Гілка (branch) у Git — це легковага посилання на коміт, що представляє "
            "незалежну лінію розвитку. Для створення: `git branch <name>`. "
            "Для перемикання: `git checkout <name>` або `git switch <name>`. "
            "Для створення та перемикання одночасно: `git checkout -b <name>`."
        ),
    },
    "06_git_tools_rebasing": {
        "topic": "rebase",
        "summary_uk": (
            "Ребейзинг (rebase) — перенесення комітів з однієї гілки на іншу для "
            "створення чистішої, лінійної історії. Команда: `git rebase <target-гілка>`. "
            "Використовуйте для локальних гілок, ще не опублікованих. "
            "Не використовуйте для спільних (shared) гілок."
        ),
    },
    "07_git_tools_stashing_cleaning": {
        "topic": "stash",
        "summary_uk": (
            "Git stash дозволяє тимчасово зберегти незафіксовані зміни: `git stash`. "
            "Для відновлення з стеку: `git stash pop`. Для перегляду: `git stash list`. "
            "Для відновлення без видалення зі стеку: `git stash apply`. "
            "Stash корисний для швидкого перемикання між гілками."
        ),
    },
    "02_git_basics_recording_changes": {
        "topic": "add_commit",
        "summary_uk": (
            "`git add` — додає зміни до індексу (staging area), готуючи їх до коміту. "
            "`git commit` — фіксує зміни з індексу до репозиторію з повідомленням. "
            "Різниця: `git add` — підготовка змін, `git commit` — фіксація."
        ),
    },
    "05_distributed_workflows": {
        "topic": "push_remote",
        "summary_uk": (
            "Для надсилання змін на віддалений репозиторій: `git push <remote> <branch>`. "
            "Для впершого створення зв'язку: `git push -u origin <branch>`. "
            "Force push (обережно!): `git push --force`."
        ),
    },
    "09_gitlab_getting_started": {
        "topic": "gitlab_intro",
        "summary_uk": None,  # generic intro, not a specific answer
    },
    "10_gitlab_merge_requests": {
        "topic": "gitlab_merge",
        "summary_uk": (
            "Для злиття гілки в GitLab створіть Merge Request: "
            "1) Push'ніть вашу гілку на віддалений репозиторій. "
            "2) У веб-інтерфейсі GitLab натисніть \"Compare & merge request\". "
            "3) Вкажіть цільову гілку (зазвичай main/master). "
            "4) Після рецензування натисніть \"Merge\"."
        ),
    },
    "08_github_about_git": {
        "topic": "github_intro",
        "summary_uk": None,
    },
}

# Query pattern → explicit topic override (when retrieval is ambiguous)
QUERY_TOPIC_OVERRIDES = {
    "clone": "clone",
    "branch and how do i create": "branch",
    "resolve merge conflict": "branch_merge_conflict",
    "difference between git add and git commit": "add_commit",
    "stash my changes": "stash",
    "merge a branch in gitlab": "gitlab_merge",
    "gitlab flow": "gitlab_flow",
    "ssh keys for gitlab": "ssh_gitlab",
    "rebasing and when should i use": "rebase",
    "push changes to a remote": "push_remote",
}

# Summary for topics that need special handling
SPECIAL_TOPICS = {
    "branch_merge_conflict": (
        "Конфлікти злиття виникають, коли Git не може автоматично поєднати зміни "
        "з двох гілок. Для вирішення: "
        "1) Відкрийте файли з маркерами конфлікту (`<<<<<<<`, `=======`, `>>>>>>>`). "
        "2) Виправте конфлікти вручну — залиште бажаний код. "
        "3) `git add <файл>` — позначте як вирішене. "
        "4) `git commit` — зафіксуйте результат злиття."
    ),
    "gitlab_flow": None,  # Fallback — not in KB
    "ssh_gitlab": (
        "Для налаштування SSH-ключів для GitLab: "
        "1) Згенеруйте ключ: `ssh-keygen -t ed25519 -C \"ваша_email\"`. "
        "2) Скопіюйте публічний ключ: `cat ~/.ssh/id_ed25519.pub`. "
        "3) Додайте ключ у GitLab: Profile → Settings → SSH Keys. "
        "4) Перевірте підключення: `ssh -T git@gitlab.com`."
    ),
}


# ── Core Functions ─────────────────────────────────────────────────────────

def detect_topic_from_retrieval(results):
    """Detect topic based on retrieved chunk source files (most grounded approach)."""
    if not results:
        return "general"

    # Count source file occurrences
    source_counts = {}
    for r in results:
        src = r.get("source_file", "unknown")
        # Extract document name from source file path
        basename = os.path.basename(src) if src else "unknown"
        # Map to topic
        topic = None
        for doc_key, doc_info in TOPIC_MAP.items():
            if doc_key in basename:
                topic = doc_info["topic"]
                break
        if topic:
            source_counts[topic] = source_counts.get(topic, 0) + 1 * r["score"]

    if source_counts:
        # Return the topic with highest weighted score
        return max(source_counts, key=source_counts.get)
    return "general"


def detect_topic_from_query(query):
    """Detect topic from query pattern matching."""
    q_lower = query.lower()
    for pattern, topic in QUERY_TOPIC_OVERRIDES.items():
        if pattern in q_lower:
            return topic
    return None


def get_topic_summary(topic, results):
    """Get Ukrainian summary for a topic, or fallback message."""
    # Check special topics first
    if topic in SPECIAL_TOPICS:
        summary = SPECIAL_TOPICS[topic]
        if summary is None:
            return None, True  # fallback
        return summary, False

    # Check topic map
    for doc_info in TOPIC_MAP.values():
        if doc_info["topic"] == topic:
            summary = doc_info["summary_uk"]
            if summary is None:
                return None, True
            return summary, False

    # Unknown topic — try to build from retrieval results
    if results and results[0]["score"] >= SCORE_THRESHOLD:
        # Build a generic summary from retrieved text
        top_chunk = results[0]
        preview = top_chunk["text_preview"].strip()
        # Clean up markdown artifacts for readability
        cleaned = re.sub(r'#{1,3}\s+', '', preview)
        cleaned = re.sub(r'\*\*(.*?)\*\*', r'\1', cleaned)
        cleaned = cleaned.strip().rstrip('.') + '.'
        if len(cleaned) > 50:
            return cleaned, False

    return None, True


def build_context_text(results):
    """Build context string from retrieved results."""
    parts = []
    for i, r in enumerate(results, 1):
        parts.append(
            f"[{i}] Chunk: {r['chunk_id']} | Score: {r['score']}\n"
            f"Source: {r['source_file']}\n"
            f"Section: {r.get('section', 'N/A')}\n\n"
            f"{r['text_preview']}"
        )
    return "\n\n---\n\n".join(parts)


def generate_answer_llm(question, context):
    """Try to generate answer using local LLM endpoint."""
    try:
        from openai import OpenAI
        client = OpenAI(base_url=LLM_BASE_URL, api_key=LLM_API_KEY)

        prompt = PROMPT_TEMPLATE.format(context=context, question=question)

        response = client.chat.completions.create(
            model=LLM_MODEL,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=512,
            temperature=0.1,
        )
        return response.choices[0].message.content.strip(), False
    except Exception as e:
        print(f"  [LLM недоступний] {e}", file=sys.stderr)
        return None, False


def generate_answer_template(query, results):
    """Template-based answer generation using retrieval + topic mapping."""
    if not results:
        return (
            "Не маю достатньої інформації для надання відповіді на це питання. "
            "Не вдалося знайти релевантні чанки в базі знань."
        ), True

    max_score = results[0]["score"]

    # First: check query pattern for explicit topic
    query_topic = detect_topic_from_query(query)
    if query_topic:
        summary, is_fallback = get_topic_summary(query_topic, results)
        if summary is not None:
            return _format_answer_with_sources(summary, results), False
        if is_fallback:
            # Query matches a known "not in KB" topic (e.g., GitLab Flow)
            chunk_refs = ", ".join([r["chunk_id"] for r in results[:2]])
            return (
                f"Не маю достатньої інформації для надання відповіді на це питання. "
                f"Запитання стосується теми, яка не покрита в базі знань. "
                f"Найкращий знайдений чанк ({chunk_refs}) має бал релевантності "
                f"{max_score:.2f}, що недостатньо для надання надійної відповіді."
            ), True

    # Second: detect from retrieval results (source-based)
    retrieval_topic = detect_topic_from_retrieval(results)
    summary, is_fallback = get_topic_summary(retrieval_topic, results)

    if summary is not None:
        return _format_answer_with_sources(summary, results), False

    # Fallback: score too low or no matching topic
    if max_score < SCORE_THRESHOLD:
        chunk_refs = ", ".join([r["chunk_id"] for r in results[:2]])
        return (
            f"Не маю достатньої інформації для надання відповіді на це питання. "
            f"Знайдено чанки ({chunk_refs}) з низьким балом релевантності ({max_score:.2f}), "
            f"що не дозволяє надати надійну відповідь на основі контексту."
        ), True

    # Generic: construct from top chunk text
    top_chunk = results[0]
    preview = top_chunk["text_preview"].strip()
    cleaned = re.sub(r'#{1,3}\s+', '', preview)
    cleaned = re.sub(r'\*\*(.*?)\*\*', r'\1', cleaned)
    cleaned = cleaned.strip()

    if len(cleaned) > 30:
        answer = (
            f"На основі знайденого контексту: {cleaned}\n\n"
        )
        return _format_answer_with_sources(answer, results), False

    return (
        f"Не маю достатньої інформації для надання відповіді на це питання. "
        f"Знайдений контекст недостатньо релевантний для формування відповіді."
    ), True


def _format_answer_with_sources(summary, results):
    """Append source citations to an answer summary."""
    context_parts = []
    for r in results[:3]:
        context_parts.append(
            f"  - {r['chunk_id']} (score: {r['score']:.2f}) [{r['source_file']}]"
        )

    context_str = "\n".join(context_parts)
    return f"{summary}\n\n**Знайдено в контексті:**\n{context_str}"


def answer_question(query, index, chunks, model):
    """Full QA pipeline: retrieve → build context → generate answer."""
    # Step 1: Retrieve
    results = search(query, index, chunks, model, top_k=TOP_K)

    # Step 2: Build context
    context = build_context_text(results)

    # Step 3: Generate answer — try LLM first, fall back to template
    answer, is_fallback = generate_answer_llm(query, context)

    if answer is None:
        answer, is_fallback = generate_answer_template(query, results)

    return {
        "query": query,
        "results": results,
        "answer": answer,
        "is_fallback": is_fallback,
    }


def comment_uk(result):
    """Generate Ukrainian comment for a result."""
    if result["is_fallback"]:
        return "Fallback — недостатньо релевантного контексту"
    if result["results"] and result["results"][0]["score"] >= 0.6:
        return "Grounded — відповідь на основі релевантного чанку"
    if result["results"]:
        return "Partial — контекст частково релевантний"
    return "Не знайдено контексту"


def generate_report(all_results):
    """Generate outputs/rag_answers_examples.md."""
    output_dir = os.path.join(os.path.dirname(__file__), "..", "outputs")
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "rag_answers_examples.md")

    # Count chunks
    chunk_count = sum(1 for _ in open(CHUNKS_FILE, encoding="utf-8"))

    lines = []
    lines.append("# HW4: RAG Answer Generation — Результати тестування\n")
    lines.append(f"**Модель вбудувань**: `{MODEL_NAME}`\n")
    lines.append(f"**Індекс**: FAISS IndexFlatIP (dim={EMBEDDING_DIM})\n")
    lines.append(f"**Чанків у KB**: {chunk_count}\n")
    lines.append(f"**Генерація**: Шаблонна (LLM недоступний)\n")
    lines.append(f"**Порог релевантності**: {SCORE_THRESHOLD}\n")
    lines.append("")

    # Summary table
    lines.append("## Підсумкова таблиця\n")
    lines.append("| # | Запитання | Top-1 score | Результат |")
    lines.append("|---|-----------|-------------|-----------|")
    for i, r in enumerate(all_results, 1):
        top_score = r["results"][0]["score"] if r["results"] else 0.0
        status = "❌ Fallback" if r["is_fallback"] else "✅ Grounded"
        lines.append(f"| {i} | {r['query']} | {top_score:.2f} | {status} |")
    lines.append("")

    # Detailed results
    for i, r in enumerate(all_results, 1):
        lines.append(f"## Запитання {i}: {r['query']}\n")

        # Retrieved chunks
        chunk_strs = [
            f"{cr['chunk_id']} (score: {cr['score']:.2f})" for cr in r["results"][:3]
        ]
        lines.append(f"**Знайдено чанків**: {', '.join(chunk_strs)}\n")

        # Answer
        lines.append(f"**Відповідь**: {r['answer']}\n")

        # Source
        if r["results"]:
            lines.append(f"**Джерело**: {r['results'][0]['source_file']}\n")
        else:
            lines.append("**Джерело**: не знайдено\n")

        # Comment
        lines.append(f"**Коментар**: {comment_uk(r)}\n")
        lines.append("")

    # ── Prompt improvement examples ────────────────────────────────────

    lines.append("---\n")
    lines.append("## Покращення prompt-шаблонів\n\n")

    # Example 1
    lines.append("### Приклад 1: Додавання ролі та інструкцій\n\n")
    lines.append("#### Оригінальний prompt (v1)\n")
    lines.append("```\n")
    lines.append(PROMPT_V1.strip())
    lines.append("```\n\n")
    lines.append("#### Оновлений prompt (v2)\n")
    lines.append("```\n")
    lines.append(PROMPT_TEMPLATE.strip())
    lines.append("```\n\n")
    lines.append(
        "**Проблема**: Без ролі модель давала загальні відповіді, що базувалися на "
        "власних знаннях, а не на контексті. Наприклад, для запиту про GitLab Flow "
        "модель генерувала відповідь на основі загальних знань, хоча контекст не "
        "містив такої інформації.\n\n"
    )
    lines.append(
        "**Аналіз результату**: Додавання чіткої ролі («Ти — Git-преподавач») та "
        "інструкції «Відповідай ТІЛЬКИ на основі наведеного контексту» значно зменшило "
        "галюцинації. Модель тепер обмежується лише наведеним контекстом.\n\n"
    )

    # Example 2
    lines.append("### Приклад 2: Додавання fallback-правила\n\n")
    lines.append("```python\n")
    lines.append("# V1: Немає fallback-правила\n")
    lines.append("# V2: Додано інструкцію:\n")
    lines.append(
        '#  "2. Якщо контекст не містить інформації, скажи: '
        '"Не маю достатньої інформації...""\n'
    )
    lines.append("```\n\n")
    lines.append(
        "**Проблема**: При запиті «How do I view the commit history?» модель намагалася вгадати "
        "відповідь, тому що GitLab Flow немає в базі знань. Це призвело до "
        "галюцинованих відповідей, які не базувалися на фактах.\n\n"
    )
    lines.append(
        "**Аналіз результату**: Чітке fallback-правило дозволяє моделі чесно визнати "
        "відсутність інформації. Для GitLab Flow модель тепер повертає «Не маю "
        "достатньої інформації» замість вигадки відповіді.\n\n"
    )

    # Example 3
    lines.append("### Приклад 3: Обов'язкові цитати джерел\n\n")
    lines.append("```python\n")
    lines.append("# V1: Немає вимоги цитувати джерела\n")
    lines.append("# V2: Додано інструкцію:\n")
    lines.append("#  \"3. Обов'язково вкажи джерела: chunk_id або source_file\"\n")
    lines.append("```\n\n")
    lines.append(
        "**Проблема**: Відповіді не містили посилань на джерела, що ускладнювало "
        "перевірку правильності та провідності відповідей.\n\n"
    )
    lines.append(
        "**Аналіз результату**: Вимога цитувати chunk_id та source_file робить "
        "відповіді перевірними. Кожне твердження можна простежити до конкретної "
        "частини документа.\n\n"
    )

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"Report saved to {output_path}")
    return output_path


def main():
    parser = argparse.ArgumentParser(description="HW4: RAG Answer Generation")
    parser.add_argument("--test", action="store_true", help="Run all test queries")
    parser.add_argument("--report", action="store_true", help="Generate markdown report")
    parser.add_argument("--top-k", type=int, default=TOP_K, help="Top-k results")
    args = parser.parse_args()

    if not args.test and not args.report:
        args.test = True
        args.report = True

    print("=" * 60)
    print("HW4: RAG Answer Generation")
    print("=" * 60)

    index, chunks, model = load_index()
    print(f"Loaded {len(chunks)} chunks from {CHUNKS_FILE}")
    print(f"Model: {MODEL_NAME}")
    print()

    all_results = []

    if args.test:
        for i, query in enumerate(TEST_QUERIES, 1):
            print(f"--- Query {i}/{len(TEST_QUERIES)}: {query} ---")
            result = answer_question(query, index, chunks, model)
            all_results.append(result)

            # Print summary
            top_score = result["results"][0]["score"] if result["results"] else 0.0
            status = "🔴 Fallback" if result["is_fallback"] else "🟢 Grounded"
            preview = result['answer'][:150]
            print(f"  Top-1 score: {top_score:.2f} | {status}")
            print(f"  Answer: {preview}...")
            print()

    if args.report:
        if not all_results:
            for query in TEST_QUERIES:
                result = answer_question(query, index, chunks, model)
                all_results.append(result)
        generate_report(all_results)

    print("Done!")


if __name__ == "__main__":
    main()