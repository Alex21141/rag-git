#!/usr/bin/env python3
"""
Prepare knowledge base: read raw documents → chunk with overlap → save as JSONL.

Chunking approach:
 1. Sliding window across entire document text
 2. Break at sentence boundaries for readability  
 3. Overlap: last N chars of each chunk are prepended to the next chunk

Configuration:
 CHUNK_SIZE — max characters per raw chunk
 OVERLAP — characters to overlap between chunks
 MIN_CHUNK — minimum characters per chunk (filtered out)

Output:
 data/processed/chunks.jsonl — one JSON line per chunk
"""

import json
import os
import re
from collections import defaultdict
from pathlib import Path

# ── Configuration ──────────────────────────────────────────────────────────
RAW_DIR = Path(__file__).parent.parent / "data" / "raw"
OUTPUT = Path(__file__).parent.parent / "data" / "processed" / "chunks.jsonl"

CHUNK_SIZE = 850
OVERLAP = 150
MIN_CHUNK = 300

# Domain metadata
DOMAIN_MAP = {
    "git_about_version_control": ("Getting Started", "git", "concept"),
    "git_basics_getting_repository": ("Git Basics", "git", "concept"),
    "git_basics_recording_changes": ("Git Basics", "git", "commands"),
    "branching_basic_branching_merging": ("Branching", "git", "workflow"),
    "branching_branch_management": ("Branching", "git", "reference"),
    "distributed_workflows": ("Distributed Git", "git", "workflow"),
    "git_tools_rebasing": ("Git Tools", "git", "procedure"),
    "git_tools_stashing_cleaning": ("Git Tools", "git", "commands"),
    "github_about_git": ("GitHub", "github", "concept"),
    "gitlab_getting_started": ("GitLab", "gitlab", "concept"),
}


def filename_to_docid(filename: str) -> str:
    """Strip numeric prefix from filename stem.

    '01_git_basics_getting_repository.md' → 'git_basics_getting_repository'
    """
    stem = Path(filename).stem
    return re.sub(r'^\d+_', '', stem)


def build_section_map(text: str):
    """Build a map of character positions → section headings.

    Ignores headings inside code blocks (``` ... ```).
    """
    sections = []
    current_heading = None
    pos = 0
    in_code_block = False
    for line in text.split("\n"):
        stripped = line.strip()
        # Skip code block toggles
        if stripped.startswith("```"):
            in_code_block = not in_code_block
            pos += len(line) + 1
            continue
        # Skip headings inside code blocks
        if in_code_block:
            pos += len(line) + 1
            continue
        header_match = re.match(r'^(#{1,6})\s+(.+)$', stripped)
        if header_match:
            if current_heading:
                sections.append((current_heading, pos))
            current_heading = stripped
        pos += len(line) + 1
    if current_heading:
        sections.append((current_heading, pos))
    return sections


def resolve_section(section_map: list, char_pos: int, title: str):
    """Get the section heading that contains the given character position."""
    if not section_map:
        return title
    if char_pos <= section_map[0][1]:
        return section_map[0][0]
    result = None
    for heading, end_pos in section_map:
        if char_pos <= end_pos:
            return result
    result = heading
    return result or section_map[0][0]


def fix_unclosed_backticks(chunk_text: str, full_text: str, start: int, end: int) -> str:
    """Fix unclosed inline backticks by expanding chunk end to include closing backtick.

    If chunk_text has odd number of backticks (not inside a code block),
    it means we cut an inline code fence in half. Find the closing backtick
    and include it.
    """
    code_block_count = chunk_text.count('```')
    inline_count = chunk_text.count('`') - (code_block_count * 3)

    if inline_count % 2 == 1 and start < end < len(full_text):
        # Odd number of backticks — find the closing one
        search_start = end
        search_end = min(end + 200, len(full_text))
        for pos in range(search_start, search_end):
            if full_text[pos] == '`':
                # Include the closing backtick
                chunk_text = full_text[start:pos + 1].strip()
                break
            # Stop at next heading or section break
            if full_text[pos:pos + 2] == '# ':
                break

    return chunk_text


def chunk_semantic(text: str, chunk_size: int, overlap: int, min_chunk: int,
                   section_map: list = None):
    """Split text into chunks with overlap between consecutive chunks.

    Simplified sliding window approach:
    1. Walk through text with step = chunk_size - overlap
    2. Find best sentence break near each window end
    3. Prepend overlap from previous chunk for continuity
    4. Fix unclosed backticks

    Returns list of (start_pos, end_pos, chunk_text, section) tuples.
    """
    chunks = []
    text_len = len(text)
    prev_end = 0

    start = 0
    while start < text_len:
        # Calculate window end
        end = min(start + chunk_size, text_len)

        # Find best sentence break near end
        if end < text_len:
            # Search backwards for sentence end
            best_end = end
            for delta in range(0, 80):
                if end - delta > start + min_chunk and text[end - delta] in '.!?':
                    best_end = end - delta + 1
                    break
                # Also try word boundary
                if end - delta > start + min_chunk and text[end - delta] in ' \t\n':
                    best_end = end - delta + 1

            # Ensure forward progress
            if best_end > start:
                end = best_end

        # Extract chunk text (without overlap yet)
        raw_chunk = text[start:end].strip()

        # Prepend overlap from previous chunk (last `overlap` chars of raw text)
        if prev_end > 0:
            overlap_start = max(0, prev_end - overlap)
            # Word boundary on overlap_start: if mid-word, move back to word start
            if overlap_start > 0 and text[overlap_start - 1].isalnum():
                ws = overlap_start - 1
                while ws >= 0 and text[ws].isalnum():
                    ws -= 1
                overlap_start = ws + 1
            overlap_text = text[overlap_start:prev_end].strip()

            if overlap_text and overlap_text != raw_chunk[:len(overlap_text)]:
                # Add space if needed
                if not overlap_text.endswith((" ", "\n", "\t")) and raw_chunk and not raw_chunk.startswith((" ", "\n", "\t")):
                    chunk_text = overlap_text + " " + raw_chunk
                else:
                    chunk_text = overlap_text + raw_chunk
            else:
                chunk_text = raw_chunk
        else:
            chunk_text = raw_chunk

        # Fix unclosed inline backticks AFTER overlap prepending
        # (the combined text may have odd backticks from overlap + chunk)
        chunk_text = fix_unclosed_backticks(chunk_text, text, start, end)

        # Update prev_end BEFORE updating start (for next iteration overlap)
        prev_end = end

        # Resolve section
        section = None
        if section_map:
            section = resolve_section(section_map, start, "Unknown")

        # Filter by min_chunk
        if len(chunk_text) >= min_chunk:
            chunks.append((start, end, chunk_text, section))

        # Advance start: sliding window with overlap
        new_start = end - overlap
        # If we've reached the end of the text, this was the last chunk — exit
        if end >= text_len:
            break
        # Ensure forward progress — never go backward or stay still
        if new_start <= start:
            start = end  # fallback: no overlap if sentence break is too close
        else:
            start = new_start
            # Word boundary: if start lands mid-word, move forward to next word
            if start < text_len and text[start].isalnum():
                # Skip over current word and whitespace to reach next word
                while start < text_len and text[start].isalnum():
                    start += 1
                while start < text_len and text[start] in " \t\n":
                    start += 1

    return chunks


def _capitalize_chunk(text: str) -> str:
    """Capitalize first letter of chunk text."""
    if not text:
        return text
    for i, ch in enumerate(text):
        if ch.isalpha():
            return text[:i] + ch.upper() + text[i + 1:]
    return text


def prepare_knowledge_base():
    """Read all raw documents, chunk them, and save as JSONL."""
    os.makedirs(OUTPUT.parent, exist_ok=True)

    all_chunks = []

    print("=" * 60)
    print("Step 1: Reading raw documents")
    print("=" * 60)

    doc_files = sorted(RAW_DIR.glob("*.md"))
    print(f"  Found {len(doc_files)} documents\n")

    for doc_file in doc_files:
        doc_id = filename_to_docid(doc_file.name)
        domain_info = DOMAIN_MAP.get(doc_id, (doc_id, "git", "reference"))
        title, domain, doc_type = domain_info

        with open(doc_file, "r", encoding="utf-8") as f:
            text = f.read()

        section_map = build_section_map(text)
        raw_splits = chunk_semantic(text, CHUNK_SIZE, OVERLAP, MIN_CHUNK, section_map)

        final_chunks = []
        for start_pos, end_pos, chunk_text, section in raw_splits:
            if section is None:
                section = title
            final_chunks.append({
                "chunk_id": f"{doc_id}_chunk_{len(final_chunks):03d}",
                "text": _capitalize_chunk(chunk_text.strip()),
                "metadata": {
                    "document_id": doc_id,
                    "source_file": f"data/raw/{doc_file.name}",
                    "source_type": "markdown",
                    "title": title,
                    "section": section,
                    "chunk_index": len(final_chunks) + 1,
                    "language": "en",
                    "domain": domain,
                    "document_type": doc_type,
                },
            })

        all_chunks.extend(final_chunks)
        print(f"  {doc_file.name}: {len(final_chunks)} chunks")

    # Merge small chunks (<300 chars) with next chunk
    print(f"\n{'=' * 60}")
    print("Step 2.5: Merging small chunks")
    print("=" * 60)
    merged = []
    skip_next = False
    for i, c in enumerate(all_chunks):
        if skip_next:
            skip_next = False
            continue
        text_len = len(c["text"])
        if text_len < 300 and i + 1 < len(all_chunks):
            next_c = all_chunks[i + 1]
            merged_text = c["text"] + " " + next_c["text"]
            c["text"] = merged_text.strip()
            c["chunk_id"] = f"{c['metadata']['document_id']}_chunk_{c['metadata']['chunk_index']:03d}"
            skip_next = True
            print(f"  Merged {c['metadata']['document_id']}_chunk_{c['metadata']['chunk_index']:03d} "
                  f"({text_len} chars) with next chunk")
        merged.append(c)
    all_chunks = merged

    # Renumber chunk_index & chunk_id per document (sequential)
    print(f"\n{'=' * 60}")
    print("Step 2.6: Renumbering chunk indices")
    print("=" * 60)
    by_doc = defaultdict(list)
    for c in all_chunks:
        did = c["metadata"]["document_id"]
        by_doc[did].append(c)

    fixed = []
    for did in sorted(by_doc.keys()):
        for idx, c in enumerate(by_doc[did]):
            c["metadata"]["chunk_index"] = idx + 1
            c["chunk_id"] = f"{did}_chunk_{idx + 1:03d}"
        fixed.extend(by_doc[did])
    all_chunks = fixed
    print(f"  All chunk_index now sequential per document")

    # Save to JSONL
    print(f"\n{'=' * 60}")
    print("Step 2: Saving chunks")
    print("=" * 60)

    with open(OUTPUT, "w", encoding="utf-8") as f:
        for chunk in all_chunks:
            f.write(json.dumps(chunk, ensure_ascii=False) + "\n")

    print(f"  Saved {len(all_chunks)} chunks to {OUTPUT}")

    # Summary
    print(f"\n{'=' * 60}")
    print("Summary")
    print("=" * 60)

    text_lengths = [len(c["text"]) for c in all_chunks]
    print(f"  Total chunks:       {len(all_chunks)}")
    print(f"  Avg text length:    {sum(text_lengths) / len(text_lengths):.0f} chars")
    print(f"  Min text length:    {min(text_lengths)} chars")
    print(f"  Max text length:    {max(text_lengths)} chars")
    print(f"  Total text length:  {sum(text_lengths):,} chars")

    domain_counts = {}
    for chunk in all_chunks:
        d = chunk["metadata"]["domain"]
        domain_counts[d] = domain_counts.get(d, 0) + 1

    print(f"\n  By domain:")
    for domain, count in sorted(domain_counts.items(), key=lambda x: -x[1]):
        print(f"    {domain:20s} {count:4d} chunks")

    # Overlap analysis
    print(f"\n  Overlap analysis:")
    by_doc = defaultdict(list)
    for c in all_chunks:
        by_doc[c["metadata"]["document_id"]].append(c)

    overlap_pairs = 0
    total_pairs = 0
    for did, doc_chunks in by_doc.items():
        for i in range(len(doc_chunks) - 1):
            t1_end = doc_chunks[i]["text"][-200:]
            t2_start = doc_chunks[i + 1]["text"][:200]
            found = any(
                t1_end[k:] in t2_start and len(t1_end[k:]) >= 15 and t1_end[k:].strip()
                for k in range(len(t1_end))
            )
            if found:
                overlap_pairs += 1
            total_pairs += 1

    if total_pairs:
        print(f"    Overlapping pairs: {overlap_pairs}/{total_pairs} "
              f"({overlap_pairs / total_pairs * 100:.1f}%)")

    # Backtick check
    print(f"\n  Backtick check:")
    odd_backticks = 0
    for c in all_chunks:
        t = c["text"]
        code_blocks = t.count('```')
        inline = t.count('`') - (code_blocks * 3)
        if inline % 2 == 1:
            odd_backticks += 1
    print(f"    Chunks with odd backticks: {odd_backticks}/{len(all_chunks)}")


if __name__ == "__main__":
    prepare_knowledge_base()