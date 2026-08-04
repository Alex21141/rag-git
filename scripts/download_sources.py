#!/usr/bin/env python3
"""
Скрипт для скачивания страниц документации Git/GitHub/GitLab
и очистки их до чистого тексту (без nav/sidebar/footer/ссылок/жирного/навігації).

Установка зависимостей:
    pip install requests beautifulsoup4 html2text --break-system-packages

Запуск:
    python3 download_sources.py
"""

import os
import re
import time
import requests
from bs4 import BeautifulSoup
import html2text

OUTPUT_DIR = "data/raw"

# Список источников: (filename, url, css-селектор основного контента)
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
        "url": "https://docs.github.com/api/article/body?pathname=/en/get-started/using-git/about-git",
        "title": "GitHub — About Git",
        "selector": "body",
    },
    {
        "filename": "09_gitlab_flow.md",
        "url": "https://docs.gitlab.com/topics/git/get_started/index.md",
        "title": "GitLab — Getting started with Git",
        "selector": "#main-content",
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
    """Скачивает страницу, вырезает основной контент, чистит HTML → markdown-текст.
    
    Для plain markdown URL (ending in .md) — просто скачивает через requests без HTML парсинга.
    Для HTML страниц — использует BeautifulSoup + html2text.
    """
    resp = requests.get(url, headers=HEADERS, timeout=20)
    resp.raise_for_status()

    # Plain markdown endpoint — skip HTML parsing entirely
    if url.endswith('.md') or 'text/markdown' in resp.headers.get('content-type', ''):
        text = resp.text.strip()
    else:
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

    text = "\n".join(cleaned).strip()
    return text


def clean_raw_document(text: str, filename: str) -> str:
    """Post-processing pipeline: removes all formatting artifacts from scraped docs.
    
    Steps (in order):
    1. Remove 'Source: URL' metadata lines
    2. Remove '---' horizontal rule separators (standalone ---)
    3. Remove 'prev | next' navigation links
    4. Remove 'Tip |' / 'Note |' block markers (git-scm formatting)
    5. Remove '---|---' / '---|---|---' closing dividers (Note/Tip blocks)
    6. Remove markdown links [text](url) → keep text only
    7. Remove **bold** formatting → keep text only
    8. Remove bare URLs (https://..., http://..., //docs.github...)
    9. Remove numbered duplicate headings (# X.Y Title where # Title already exists)
    10. Remove empty headings (## with no text)
    11. Fix broken multi-row tables (merge |---|---|---... into single separator)
    12. Remove image alt-text brackets [](/path/to/image.png)
    13. Clean up extra blank lines
    """
    text = clean_source_metadata(text)
    text = clean_horizontal_rules(text)
    text = clean_prev_next_navigation(text)
    text = clean_tip_note_markers(text)
    text = clean_note_tip_dividers(text)
    text = clean_markdown_links(text)
    text = clean_bold_formatting(text)
    text = clean_bare_urls(text)
    text = clean_duplicate_headings(text)
    text = clean_empty_headings(text)
    text = clean_table_separators(text)
    text = clean_image_refs(text)
    text = clean_note_blocks(text)
    text = clean_cross_references(text)
    text = clean_blank_lines(text)
    return text


def clean_source_metadata(text: str) -> str:
    """Remove 'Source: URL' lines added by the scraper."""
    return re.sub(r'^Source:\s+https?://.*$\n?', '', text, flags=re.MULTILINE)


def clean_horizontal_rules(text: str) -> str:
    """Remove standalone '---' horizontal rules."""
    return re.sub(r'^---$\n?', '', text, flags=re.MULTILINE)


def clean_prev_next_navigation(text: str) -> str:
    """Remove 'prev | next' and 'Prev | Next' navigation at end of git-scm pages."""
    text = re.sub(r'prev\s+\|\s+next\s*$', '', text, flags=re.MULTILINE | re.IGNORECASE)
    # Also handle variations with links
    text = re.sub(r'\[.*?\]\(.*?\)\s*\|\s*\[.*?\]\(.*?\)\s*$', '', text, flags=re.MULTILINE)
    return text


def clean_tip_note_markers(text: str) -> str:
    """Remove 'Tip |' / 'Note |' block markers (git-scm book formatting)."""
    text = re.sub(r'^Tip\s*\|', '', text, flags=re.MULTILINE)
    text = re.sub(r'^Note\s*\|', '', text, flags=re.MULTILINE)
    return text


def clean_note_tip_dividers(text: str) -> str:
    """Remove '---|---' / '---|---|---' closing dividers from Note/Tip blocks.
    
    These are artifacts of git-scm's two-column Note/Tip layout that ends with ---|---."""
    # Only remove if it's a standalone line (not a table separator with content columns)
    text = re.sub(r'^(\|-?)+(\\n|)$', '', text, flags=re.MULTILINE)
    return text


def clean_markdown_links(text: str) -> str:
    """Remove [text](url) links → keep text only."""
    return re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)


def clean_bold_formatting(text: str) -> str:
    """Remove **bold** formatting → keep text only."""
    return re.sub(r'\*\*(.*?)\*\*', r'\1', text)


def clean_bare_urls(text: str) -> str:
    """Remove bare URLs (https://..., http://..., git://).
    
    Keeps code blocks intact by only removing URLs outside of ``` blocks."""
    # For lines NOT inside code blocks, remove bare URLs
    lines = text.split('\n')
    result = []
    in_code_block = False
    for line in lines:
        stripped = line.strip()
        if stripped.startswith('```'):
            in_code_block = not in_code_block
            result.append(line)
            continue
        if not in_code_block:
            # Remove bare URLs (https://..., http://..., //docs...)
            line = re.sub(r'https?://[^\s`"\'<>\)]+', '', line)
            line = re.sub(r'git://[^\s`"\'<>\)]+', '', line)
            line = re.sub(r'//docs\.[^\s`"\'<>\)]+', '', line)
            # Remove image references [](/path/to/image.png)
            line = re.sub(r'\[\]\([^)]*\)', '', line)
        result.append(line)
    return '\n'.join(result)


def clean_duplicate_headings(text: str) -> str:
    """Remove numbered duplicate headings.
    
    Pattern: '# Title\n\n# X.Y Title' → '# Title'
    The first heading is the real one; the numbered one is a navigation artifact."""
    # Match: # Some Title\n\n# X.Y Some Title\n\n → # Some Title\n\n
    text = re.sub(r'(#[^#][^\n]+)\n\n# \d+\.\d+ [^\n]+\n\n', r'\1\n\n', text)
    return text


def clean_empty_headings(text: str) -> str:
    """Remove empty headings like '##' (no text after the #)."""
    text = re.sub(r'^#+\s*$', '', text, flags=re.MULTILINE)
    return text


def clean_table_separators(text: str) -> str:
    """Fix broken table separators.
    
    When html2text mangles a multi-line table header, it creates separate rows like:
    |col1
    |col2
    |col3
    ---
    ---
    ---
    Fix by merging consecutive | and --- lines into proper table format."""
    lines = text.split('\n')
    result = []
    i = 0
    while i < len(lines):
        line = lines[i]
        # Detect table header pattern: consecutive lines ending with | or ---
        if re.match(r'^[\s\w\-/]+[\|]?\s*$', line) and i + 1 < len(lines):
            # Collect consecutive table-like lines
            table_lines = [line]
            j = i + 1
            while j < len(lines):
                next_line = lines[j]
                if re.match(r'^[\s\w\-/]+[\|]?\s*$', next_line) or re.match(r'^\-+\s*$', next_line):
                    table_lines.append(next_line)
                    j += 1
                else:
                    break
            
            if len(table_lines) > 2:
                # Merge into proper table: header|separator
                headers = []
                separators = []
                for tl in table_lines:
                    if tl.strip().startswith('|') or tl.strip().endswith('|'):
                        if tl.strip() == '|':
                            continue
                        headers.append(tl.strip().rstrip('|').lstrip('|').strip())
                    elif re.match(r'^\-+$', tl.strip()):
                        separators.append(tl.strip())
                
                if headers:
                    # Rebuild table
                    header_row = ' | '.join(h for h in headers if h)
                    sep_row = '-|-'.join('---' for _ in headers)
                    result.append(f"|{header_row}|")
                    result.append(sep_row)
                    i = j
                    continue
            
            result.append(line)
            i += 1
        else:
            result.append(line)
            i += 1
    
    return '\n'.join(result)


def clean_image_refs(text: str) -> str:
    """Remove image references [](/path/to/image.png) and broken !alt_text artifacts."""
    text = re.sub(r'\[\]\([^)]*\)', '', text)
    # Remove broken image alt text: ![Alt text](url) → removed entirely
    # When URL is stripped, we get !Alt text — remove these lines
    text = re.sub(r'^!\s*[^\n]*$\n?', '', text, flags=re.MULTILINE)
    # Remove image markers like ![image] that remain
    text = re.sub(r'!\[([^\]]*)\]\s*\(\s*\)', '', text)
    return text


def clean_note_blocks(text: str) -> str:
    """Convert > [!note] / > [!tip] / > [!important] callout blocks.
    
    GitLab uses: > [!note]\n> Text here
    Convert to: Note: Text here
    """
    # Match > [!note] / > [!tip] / > [!warning] / > [!important] blocks
    text = re.sub(r'>\s*\[!(note|tip|warning|important)\]\s*\n((?:>\s*.+\n?)*)',
                  lambda m: f"Note: {''.join(line.lstrip('>').lstrip() for line in m.group(2).splitlines() if line.strip())}\n",
                  text, flags=re.IGNORECASE)
    return text


def clean_cross_references(text: str) -> str:
    """Remove internal cross-references like 'see X.' and 'Continue reading'.
    
    These are artifacts of the documentation navigation.
    """
    # Remove "For more information, see X." → keep just "For more information, see X."
    # Actually these are fine as text — the links were stripped, just bare text remains
    # Remove "Continue reading" artifacts
    text = re.sub(r':\s*Continue reading\s*$', '', text, flags=re.MULTILINE)
    # Remove "- Item: See link" patterns where the link was stripped
    text = re.sub(r'- (.*?):\s+.*?reading$', r'- \1', text, flags=re.MULTILINE)
    return text


def clean_blank_lines(text: str) -> str:
    """Remove consecutive blank lines (keep max 1 blank line between content)."""
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
            raw_text = fetch_and_clean(src["url"], src["selector"])
        except Exception as e:
            print(f"  [ОШИБКА] Не удалось скачать {src['url']}: {e}")
            continue

        # Apply full cleaning pipeline
        cleaned = clean_raw_document(raw_text, src["filename"])

        # Write final clean document
        out_path = os.path.join(OUTPUT_DIR, src["filename"])
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(f"# {src['title']}\n\n")
            f.write(cleaned)

        print(f"  -> сохранено: {out_path} ({len(cleaned)} символов)")

        # Вежливая пауза между запросами
        time.sleep(1.5)

    print("\nГотово. Проверь файлы в data/raw/ — особенно те, где сработал fallback на <body>.")


if __name__ == "__main__":
    main()