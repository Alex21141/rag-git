#!/usr/bin/env python3
"""
Prepare knowledge base: read raw documents → chunk with overlap → save as JSONL.

Chunking approach:
  1. For each document, use sliding window across entire text
  2. Break at sentence boundaries for readability
  3. POST-PROCESS: inject overlap by prepending last OVERLAP chars of each chunk
     to the start of the next chunk (standard RAG overlap pattern)

Configuration:
    CHUNK_SIZE    — max characters per chunk
    OVERLAP       — characters to carry over between chunks
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
    "git_basics_getting_repository": ("Git Basics", "git", "concept"),
    "git_basics_recording_changes": ("Git Basics", "git", "commands"),
    "branching_basic_branching_merging": ("Branching", "git", "workflow"),
    "branching_branch_management": ("Branching", "git", "reference"),
    "distributed_workflows": ("Distributed Git", "git", "workflow"),
    "git_tools_rebasing": ("Git Tools", "git", "procedure"),
    "git_tools_stashing_cleaning": ("Git Tools", "git", "commands"),
    "github_about_git": ("GitHub", "github", "concept"),
    "gitlab_flow": ("GitLab Flow", "gitlab", "workflow"),
    "gitlab_merge_requests": ("GitLab", "gitlab", "procedural"),
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
    # Try sentence break
    sentence_end = find_sentence_break(text, max_end, 80)
    if sentence_end > start + MIN_CHUNK:
        return sentence_end
    # Try word boundary (space)
    last_space = text.rfind(' ', max(0, max_end - 50), max_end)
    if last_space > start + MIN_CHUNK:
        return last_space + 1
    # Last resort
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
    # At position 0, return first heading
    if char_pos <= section_map[0][1]:
        return section_map[0][0]
    result = None
    for heading, end_pos in section_map:
        if char_pos <= end_pos:
            return result
        result = heading
    return result or section_map[0][0]


def inject_overlap(raw_chunks: list, overlap: int) -> list:
    """Inject overlap between consecutive chunks.
    
    For each pair (i, i+1):
    - Take the last ~`overlap` chars from the already-processed chunk i
    - Truncate chunk i before those chars
    - Prepend those chars to chunk i+1
    
    This ensures: end of result[i] == start of result[i+1] (overlapping region)
    """
    if len(raw_chunks) <= 1:
        return raw_chunks

    result = []
    for i in range(len(raw_chunks)):
        chunk = dict(raw_chunks[i])
        text = chunk["text"]
        
        # Prepend overlap from the ALREADY PROCESSED previous chunk
        if i > 0 and result:
            prev_processed_text = result[-1]["text"]
            overlap_tail = prev_processed_text[-overlap:] if len(prev_processed_text) > overlap else prev_processed_text
            text = overlap_tail + text
        
        # Truncate if too long
        max_size = CHUNK_SIZE + OVERLAP + 100
        if len(text) > max_size:
            text = text[:max_size]
        
        # For non-last chunks, truncate the end to reserve overlap for next
        if i < len(raw_chunks) - 1:
            cut_point = len(text) - overlap
            # Move forward/backward to nearest word boundary
            space_pos = text.find(' ', cut_point - 10, cut_point + 10)
            if space_pos < 0 or abs(space_pos - cut_point) > 10:
                space_pos = cut_point
            text = text[:space_pos].strip()
        
        chunk["text"] = text.strip()
        result.append(chunk)
    
    return result


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

        # Build section map for metadata tracking
        section_map = build_section_map(text)

        # Phase 1: Sliding window chunking (no overlap yet)
        raw_chunks = []
        step = CHUNK_SIZE  # Advance full chunk size (no overlap in raw phase)
        start = 0
        text_len = len(text)

        while start < text_len:
            end = min(start + CHUNK_SIZE, text_len)

            # Adjust endpoint for readability
            if end < text_len:
                end = find_chunk_end(text, start, end)

            chunk_text = text[start:end].strip()

            if len(chunk_text) >= MIN_CHUNK:
                section = get_section_at(section_map, start, title)
                raw_chunks.append({
                    "chunk_id": f"{doc_id}_chunk_{len(raw_chunks):03d}",
                    "text": chunk_text,
                    "metadata": {
                        "document_id": doc_id,
                        "source_file": f"data/raw/{doc_file.name}",
                        "source_type": "markdown",
                        "title": title,
                        "section": section,
                        "chunk_index": len(raw_chunks) + 1,
                        "language": "en",
                        "domain": domain,
                        "document_type": doc_type,
                    },
                })

            start += step
            if start >= end:
                start = end

        # Phase 2: Inject overlap between consecutive chunks
        final_chunks = inject_overlap(raw_chunks, OVERLAP)

        all_chunks.extend(final_chunks)
        print(f"  {doc_file.name}: {len(final_chunks)} chunks "
              f"(raw: {len(raw_chunks)}, with overlap: {len(final_chunks)})")

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

    # Overlap analysis (post-injection)
    print(f"\n  Overlap analysis:")
    from collections import defaultdict
    by_doc = defaultdict(list)
    for c in all_chunks:
        by_doc[c["metadata"]["document_id"]].append(c)

    overlap_pairs = 0
    total_pairs = 0
    for did, doc_chunks in by_doc.items():
        for i in range(len(doc_chunks) - 1):
            t1 = doc_chunks[i]["text"][-80:]
            t2 = doc_chunks[i + 1]["text"][:80]
            shared = 0
            for k in range(min(len(t1), len(t2))):
                if t1[k] == t2[k]:
                    shared += 1
                else:
                    break
            if shared > 15:
                overlap_pairs += 1
            total_pairs += 1

    if total_pairs:
        print(f"    Overlapping pairs: {overlap_pairs}/{total_pairs} "
              f"({overlap_pairs/total_pairs*100:.1f}%)")


if __name__ == "__main__":
    prepare_chunks()