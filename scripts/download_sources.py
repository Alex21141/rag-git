#!/usr/bin/env python3
"""
Скрипт для скачивания страниц документации Git/GitHub/GitLab
и очистки их до чистого текста (без nav/sidebar/footer).

Установка зависимостей:
    pip install requests beautifulsoup4 html2text --break-system-packages

Запуск:
    python3 download_sources.py
"""

import os
import time
import requests
from bs4 import BeautifulSoup
import html2text

OUTPUT_DIR = "data/raw"

# Список источников: (filename, url, css-селектор основного контента)
# Селекторы могут потребовать подстройки — сайты меняют вёрстку.
SOURCES = [
    {
        "filename": "01_git_basics_getting_repository.md",
        "url": "https://git-scm.com/book/en/v2/Git-Basics-Getting-a-Git-Repository",
        "title": "Git Basics — Getting a Git Repository",
        "selector": "#main",
    },
    {
        "filename": "02_git_basics_recording_changes.md",
        "url": "https://git-scm.com/book/en/v2/Git-Basics-Recording-Changes-to-the-Repository",
        "title": "Git Basics — Recording Changes to the Repository",
        "selector": "#main",
    },
    {
        "filename": "03_branching_basic_branching_merging.md",
        "url": "https://git-scm.com/book/en/v2/Git-Branching-Basic-Branching-and-Merging",
        "title": "Git Branching — Basic Branching and Merging",
        "selector": "#main",
    },
    {
        "filename": "04_branching_branch_management.md",
        "url": "https://git-scm.com/book/en/v2/Git-Branching-Branch-Management",
        "title": "Git Branching — Branch Management",
        "selector": "#main",
    },
    {
        "filename": "05_distributed_workflows.md",
        "url": "https://git-scm.com/book/en/v2/Distributed-Git-Distributed-Workflows",
        "title": "Distributed Git — Distributed Workflows",
        "selector": "#main",
    },
    {
        "filename": "06_git_tools_rebasing.md",
        "url": "https://git-scm.com/book/en/v2/Git-Branching-Rebasing",
        "title": "Git Tools — Rebasing",
        "selector": "#main",
    },
    {
        "filename": "07_git_tools_stashing_cleaning.md",
        "url": "https://git-scm.com/book/en/v2/Git-Tools-Stashing-and-Cleaning",
        "title": "Git Tools — Stashing and Cleaning",
        "selector": "#main",
    },
    {
        "filename": "08_github_about_git.md",
        "url": "https://docs.github.com/en/get-started/using-git/about-git",
        "title": "GitHub — About Git",
        "selector": "article",
    },
    {
        "filename": "09_gitlab_flow.md",
        "url": "https://docs.gitlab.com/topics/gitlab_flow/",
        "title": "GitLab Flow",
        "selector": "article",
    },
    {
        "filename": "10_gitlab_merge_requests.md",
        "url": "https://docs.gitlab.com/user/project/merge_requests/",
        "title": "GitLab — Merge Requests",
        "selector": "article",
    },
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; KnowledgeBaseBot/1.0; educational homework project)"
}


def fetch_and_clean(url: str, selector: str) -> str:
    """Скачивает страницу, вырезает основной контент, чистит HTML -> markdown-текст."""
    resp = requests.get(url, headers=HEADERS, timeout=20)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")

    # Убираем явный мусор до выбора основного блока
    for tag in soup(["script", "style", "nav", "header", "footer", "aside"]):
        tag.decompose()

    main = soup.select_one(selector)
    if main is None:
        # fallback — если селектор не совпал с реальной вёрсткой сайта
        print(f"  [!] селектор '{selector}' не найден, беру <body> целиком — проверь вручную")
        main = soup.body if soup.body else soup

    converter = html2text.HTML2Text()
    converter.ignore_links = False
    converter.ignore_images = True
    converter.body_width = 0  # не переносить строки принудительно

    text = converter.handle(str(main))

    # Базовая пост-очистка: убираем лишние пустые строки
    lines = [line.rstrip() for line in text.splitlines()]
    cleaned = []
    prev_blank = False
    for line in lines:
        is_blank = line.strip() == ""
        if is_blank and prev_blank:
            continue
        cleaned.append(line)
        prev_blank = is_blank

    return "\n".join(cleaned).strip()


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    for i, src in enumerate(SOURCES, 1):
        print(f"[{i}/{len(SOURCES)}] Скачиваю: {src['title']} ({src['url']})")
        try:
            content = fetch_and_clean(src["url"], src["selector"])
        except Exception as e:
            print(f"  [ОШИБКА] Не удалось скачать {src['url']}: {e}")
            continue

        out_path = os.path.join(OUTPUT_DIR, src["filename"])
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(f"# {src['title']}\n\n")
            f.write(f"Source: {src['url']}\n\n")
            f.write("---\n\n")
            f.write(content)

        print(f"  -> сохранено: {out_path} ({len(content)} символов)")

        # Вежливая пауза между запросами
        time.sleep(1.5)

    print("\nГотово. Проверь файлы в data/raw/ — особенно те, где сработал fallback на <body>,")
    print("там может остаться мусор (меню, реклама и т.п.), который нужно будет почистить вручную.")


if __name__ == "__main__":
    main()
