#!/usr/bin/env python3
"""
Prepare knowledge base: read raw documents → chunk with overlap → save as JSONL.

Chunking approach:
  1. Sliding window across entire document text
  2. Break at sentence boundaries for readability
  3. Overlap: last N chars of each chunk are prepended to the next chunk

Configuration:
    CHUNK_SIZE    — max characters per raw chunk
    OVERLAP       — characters to overlap between chunks
    MIN_CHUNK     — minimum characters per chunk (filtered out)

Output:
    data/processed/chunks.jsonl  — one JSON line per chunk
"""

import json
import os
import re
from pathlib import Path

# ── Configuration ──────────────────────────────────────────────────────────
RAW_DIR = Path(__file__).parent.parent / "data" / "raw"
OUTPUT = Path(__file__).parent.parent / "data" / "processed" / "chunks.jsonl"

CHUNK_SIZE = 700
OVERLAP = 150
MIN_CHUNK = 120

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


def find_sentence_break(text: str, pos: int, window: int = 80) -> int:
    """Find the best sentence break near pos within ±window characters."""
    best = pos
    best_dist = window + 1
    for delta in range(-window, window + 1):
        candidate = pos + delta
        if 0 < candidate < len(text) and text[candidate] in '.!?)]\'"':
            dist = abs(delta)
            if dist < best_dist:
                best = candidate + 1
                best_dist = dist
    return best


def find_chunk_end(text: str, start: int, max_end: int) -> int:
    """Find best chunk endpoint — sentence or word boundary for readability."""
    sentence_end = find_sentence_break(text, max_end, 80)
    if sentence_end > start + MIN_CHUNK:
        return sentence_end
    last_space = text.rfind(' ', max(0, max_end - 50), max_end)
    if last_space > start + MIN_CHUNK:
        return last_space + 1
    return max_end


def build_section_map(text: str):
    """Build a map of character positions → section headings."""
    sections = []
    current_heading = None
    pos = 0
    for line in text.split("\n"):
        stripped = line.strip()
        header_match = re.match(r'^(#{1,6})\s+(.+)$', stripped)
        if header_match:
            if current_heading:
                sections.append((current_heading, pos - len(line) - 1))
            current_heading = stripped
            pos += len(line) + 1
        else:
            pos += len(line) + 1
    if current_heading:
        sections.append((current_heading, pos))
    return sections


def get_section_at(section_map: list, char_pos: int, title: str):
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


def chunk_with_overlap(text: str, chunk_size: int, overlap: int, min_chunk: int):
    """Split text into chunks with overlap between consecutive chunks.
    
    Each chunk i contains text[i_start:i_end].
    Chunk i+1 starts at i_end - overlap (so the last `overlap` chars of chunk i
    appear at the start of chunk i+1).
    
    Returns list of (start_pos, end_pos, chunk_text) tuples.
    """
    raw_splits = []
    start = 0
    text_len = len(text)
    
    # Phase 1: Split into contiguous raw chunks
    while start < text_len:
        end = min(start + chunk_size, text_len)
        if end < text_len:
            end = find_chunk_end(text, start, end)
        raw_splits.append((start, end))
        start = end
    
    # Phase 2: Apply overlap by adjusting boundaries
    # Chunk i ends at raw_splits[i][1], but we want its last `overlap` chars
    # to also appear at the start of chunk i+1.
    # So chunk i's effective text is text[raw_splits[i][0]:raw_splits[i][1]]
    # and chunk i+1's effective text starts at raw_splits[i][1] - overlap.
    
    chunks = []
    for i, (s, e) in enumerate(raw_splits):
        chunk_text = text[s:e].strip()
        
        if i > 0:
            # Prepend overlap from previous raw split
            prev_s, prev_e = raw_splits[i - 1]
            overlap_start = max(prev_s, prev_e - overlap)
            overlap_text = text[overlap_start:prev_e]
            chunk_text = overlap_text + chunk_text
        
        if len(chunk_text) >= min_chunk:
            chunks.append((s, e, chunk_text))
    
    return chunks


def prepare_chunks():
    """Read all raw documents, chunk them, and save as JSONL."""
    os.makedirs(OUTPUT.parent, exist_ok=True)

    all_chunks = []

    print("=" * 60)
    print("Step 1: Reading raw documents")
    print("=" * 60)

    doc_files = sorted(RAW_DIR.glob("*.md"))
    print(f"  Found {len(doc_files)} documents\n")

    for doc_file in doc_files:
        raw_doc_id = doc_file.stem
        doc_id = re.sub(r'^\d+_', '', raw_doc_id)
        domain_info = DOMAIN_MAP.get(doc_id, (doc_id, "git", "reference"))
        title, domain, doc_type = domain_info

        with open(doc_file, "r", encoding="utf-8") as f:
            text = f.read()

        section_map = build_section_map(text)

        # Get chunks with overlap
        raw_splits = chunk_with_overlap(text, CHUNK_SIZE, OVERLAP, MIN_CHUNK)

        final_chunks = []
        for start_pos, end_pos, chunk_text in raw_splits:
            section = get_section_at(section_map, start_pos, title)
            final_chunks.append({
                "chunk_id": f"{doc_id}_chunk_{len(final_chunks):03d}",
                "text": chunk_text.strip(),
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
    from collections import defaultdict
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
              f"({overlap_pairs/total_pairs*100:.1f}%)")


if __name__ == "__main__":
    prepare_chunks()