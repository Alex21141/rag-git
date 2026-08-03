#!/usr/bin/env python3
"""
Prepare knowledge base: normalize documents → chunk with overlap → save as JSONL.

Usage:
    python3 scripts/prepare_knowledge_base.py

Configuration:
    CHUNK_SIZE    — max characters per chunk (500–1000)
    OVERLAP       — overlap between consecutive chunks (100–200)

Output:
    data/processed/chunks.jsonl  — one JSON line per chunk
"""

import json
import os
import re
import uuid
from pathlib import Path

# ── Configuration ──────────────────────────────────────────────────────────
RAW_DIR = Path(__file__).parent.parent / "data" / "raw"
OUTPUT = Path(__file__).parent.parent / "data" / "processed" / "chunks.jsonl"

CHUNK_SIZE = 800
OVERLAP = 150

# Domain metadata for each document (topic → domain)
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


def extract_sections(text: str) -> list:
    """Split text into sections based on markdown headings (## or ###)."""
    sections = []
    current_heading = None
    current_lines = []

    for line in text.split("\n"):
        header_match = re.match(r'^(#{1,3})\s+(.+)$', line.strip())
        if header_match:
            # Save previous section
            if current_heading and current_lines:
                sections.append((current_heading, "\n".join(current_lines)))
            # Start new section
            current_heading = line.strip()
            current_lines = []
        else:
            current_lines.append(line)

    # Don't forget last section
    if current_heading and current_lines:
        sections.append((current_heading, "\n".join(current_lines)))

    return sections


def chunk_text(text: str, chunk_size: int, overlap: int) -> list:
    """Split text into overlapping chunks."""
    if len(text) <= chunk_size:
        return [text.strip()] if text.strip() else []

    chunks = []
    start = 0
    text_len = len(text)

    while start < text_len:
        end = min(start + chunk_size, text_len)
        chunk = text[start:end]

        # Try to break at paragraph boundary
        if end < text_len:
            # Look for paragraph break within last 20% of chunk
            search_end = int(chunk_size * 0.8)
            break_point = chunk.rfind("\n\n", 0, search_end)
            if break_point > int(chunk_size * 0.3):
                chunk = text[start:start + break_point + 2]
                end = start + break_point + 2

        # Strip leading/trailing whitespace
        chunk = chunk.strip()
        if chunk:
            chunks.append(chunk)

        # Move forward — ensure we always advance
        advance = chunk_size - overlap
        if advance <= 0:
            advance = 1  # Safety: at least advance 1 character
        start += advance

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
        # Extract document ID from filename (e.g. 01_git_basics_getting_repository)
        doc_id = doc_file.stem  # without extension

        # Get domain info
        domain_info = DOMAIN_MAP.get(doc_id, (doc_id, "git", "reference"))
        title, domain, doc_type = domain_info

        with open(doc_file, "r", encoding="utf-8") as f:
            text = f.read()

        # Extract sections for better chunking context
        sections = extract_sections(text)

        # Process each section
        chunk_index = 0
        for section_heading, section_text in sections:
            # Combine heading with section text for context
            section_full = f"{section_heading}\n\n{section_text}"

            # Split into chunks
            section_chunks = chunk_text(section_full, CHUNK_SIZE, OVERLAP)

            for chunk_data in section_chunks:
                chunk = {
                    "chunk_id": f"{doc_id}_chunk_{chunk_index:03d}",
                    "text": chunk_data,
                    "metadata": {
                        "document_id": doc_id,
                        "source_file": f"data/raw/{doc_file.name}",
                        "source_type": "markdown",
                        "title": title,
                        "section": section_heading,
                        "chunk_index": chunk_index,
                        "language": "en",
                        "domain": domain,
                        "document_type": doc_type,
                    },
                }
                all_chunks.append(chunk)
                chunk_index += 1

        print(f"  {doc_file.name}: {chunk_index} chunks")

    # Save to JSONL
    print(f"\n{'=' * 60}")
    print("Step 2: Saving chunks")
    print("=" * 60)

    with open(OUTPUT, "w", encoding="utf-8") as f:
        for chunk in all_chunks:
            f.write(json.dumps(chunk, ensure_ascii=False) + "\n")

    print(f"  Saved {len(all_chunks)} chunks to {OUTPUT}")

    # Summary statistics
    print(f"\n{'=' * 60}")
    print("Summary")
    print("=" * 60)

    text_lengths = [len(c["text"]) for c in all_chunks]
    print(f"  Total chunks:       {len(all_chunks)}")
    print(f"  Avg text length:    {sum(text_lengths) / len(text_lengths):.0f} chars")
    print(f"  Min text length:    {min(text_lengths)} chars")
    print(f"  Max text length:    {max(text_lengths)} chars")
    print(f"  Total text length:  {sum(text_lengths):,} chars")

    # Per-domain breakdown
    domain_counts = {}
    for chunk in all_chunks:
        domain = chunk["metadata"]["domain"]
        domain_counts[domain] = domain_counts.get(domain, 0) + 1

    print(f"\n  By domain:")
    for domain, count in sorted(domain_counts.items(), key=lambda x: -x[1]):
        print(f"    {domain:20s} {count:4d} chunks")

    print()


if __name__ == "__main__":
    prepare_chunks()