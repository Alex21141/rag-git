"""
Prepare knowledge base for Git tutoring assistant.

Reads Markdown files from data/raw/, normalizes them, and splits into chunks
with overlap. Outputs data/processed/chunks.jsonl.

Usage:
    python scripts/prepare_knowledge_base.py
"""

import json
import re
from collections import defaultdict
from pathlib import Path
from typing import Any

RAW_DIR = Path("data/raw")
PROCESSED_DIR = Path("data/processed")
OUTPUT_PATH = PROCESSED_DIR / "chunks.jsonl"

CHUNK_SIZE = 660
CHUNK_OVERLAP = 150
MIN_CHUNK = 250

# Domain mapping: document_id (without numeric prefix) → domain
DOMAIN_MAP = {
    "git_about_version_control": "git",
    "git_basics_getting_repository": "git",
    "git_basics_recording_changes": "git",
    "branching_basic_branching_merging": "git",
    "branching_branch_management": "git",
    "distributed_workflows": "git",
    "git_tools_rebasing": "git",
    "git_tools_stashing_cleaning": "git",
    "github_about_git": "github",
    "gitlab_getting_started": "gitlab",
}

# Map short prefixes to full doc_id keys
PREFIX_TO_DOC = {
    "00_": "git_about_version_control",
    "01_": "git_basics_getting_repository",
    "02_": "git_basics_recording_changes",
    "03_": "branching_basic_branching_merging",
    "04_": "branching_branch_management",
    "05_": "distributed_workflows",
    "06_": "git_tools_rebasing",
    "07_": "git_tools_stashing_cleaning",
    "08_": "github_about_git",
    "09_": "gitlab_getting_started",
}


def extract_title(text: str) -> str:
    """Extract first H1 heading from Markdown."""
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("# "):
            return stripped.replace("# ", "", 1).strip()
    return ""


def normalize_whitespace(text: str) -> str:
    """Remove empty lines while keeping section boundaries."""
    lines = [line.strip() for line in text.splitlines()]
    return "\n".join(line for line in lines if line)


def read_markdown(file_path: Path) -> dict[str, Any]:
    """Read a Markdown file as a normalized document."""
    text = file_path.read_text(encoding="utf-8")
    title = extract_title(text) or file_path.stem.replace("_", " ").title()

    # Strip numeric prefix (e.g. "03_branching_..." → "branching_...")
    stem = file_path.stem
    for prefix, full_id in PREFIX_TO_DOC.items():
        if stem.startswith(prefix):
            doc_id = full_id
            break
    else:
        doc_id = stem

    domain = DOMAIN_MAP.get(doc_id, "git")
    return {
        "document_id": doc_id,
        "source_file": str(file_path),
        "source_type": "markdown",
        "title": title,
        "text": text,
        "metadata": {
            "language": "en",
            "domain": domain,
            "document_type": "reference",
        },
    }


def split_with_overlap(text: str, chunk_size: int, overlap: int) -> list[tuple[str, int]]:
    """Split text into overlapping chunks with sentence awareness.

    Two-pass approach that guarantees 100% overlap integrity.
    Returns list of (chunk_text, overlap_len) tuples.
    """
    clean_text = normalize_whitespace(text)
    text_len = len(clean_text)

    # Pass 1: find split points (sentence boundaries)
    split_points = [0]
    pos = 0
    while pos < text_len:
        target = min(pos + chunk_size, text_len)
        if target >= text_len:
            split_points.append(target)
            break

        found = False
        for delta in range(0, 80):
            p = target - delta
            if p <= pos + 200:
                break
            if clean_text[p] in ".!?":
                split_points.append(p + 1)
                found = True
                break
            if clean_text[p] in " \t\n":
                split_points.append(p + 1)
                found = True
                break

        if not found:
            split_points.append(target)

        pos = split_points[-1]

    # Pass 2: extract chunks with overlap
    # For overlap to work: prev_chunk[-ol:] must equal curr_chunk[:ol:]
    # Do NOT strip raw_content — that would remove trailing whitespace that
    # becomes the overlap prefix for the next chunk.
    chunks: list[tuple[str, int]] = []
    for i in range(1, len(split_points)):
        start = split_points[i - 1]
        end = split_points[i]

        # Raw content: text between split points (no strip — preserves overlap)
        raw_content = clean_text[start:end]

        if i > 1:
            # Prepend overlap from raw text preceding this chunk
            ol_start = max(0, start - overlap)
            overlap_text = clean_text[ol_start:start]
            ol_len = len(overlap_text)
            chunk_text = overlap_text + raw_content
        else:
            chunk_text = raw_content
            ol_len = 0

        if chunk_text.strip():  # skip truly empty chunks
            chunks.append((chunk_text, ol_len))

    return chunks


def build_chunk_id(document_id: str, index: int) -> str:
    """Create stable chunk ID."""
    return f"{document_id}_chunk_{index:03d}"


def chunk_document(document: dict[str, Any], chunk_size: int, overlap: int) -> list[dict[str, Any]]:
    """Split one document into metadata-rich chunks."""
    text_chunks = split_with_overlap(document["text"], chunk_size, overlap)
    chunks: list[dict[str, Any]] = []
    chunk_index = 0

    for chunk_text, ol_len in text_chunks:
        if len(chunk_text) < MIN_CHUNK:
            if chunks:
                chunks[-1]["text"] += " " + chunk_text
            continue

        chunk_index += 1
        # Resolve section from document title
        section = document["title"]
        chunks.append({
            "chunk_id": build_chunk_id(document["document_id"], chunk_index),
            "text": chunk_text,
            "metadata": {
                "document_id": document["document_id"],
                "source_file": document["source_file"],
                "source_type": document["source_type"],
                "title": section,
                "section": section,
                "chunk_index": chunk_index,
                "language": document["metadata"].get("language"),
                "domain": document["metadata"].get("domain"),
                "document_type": document["metadata"].get("document_type"),
                "overlap_len": ol_len,
            },
        })

    return chunks


def load_raw_sources(raw_dir: Path) -> list[dict[str, Any]]:
    """Load Markdown files from raw directory."""
    if not raw_dir.exists():
        raise FileNotFoundError(f"Raw directory not found: {raw_dir}")

    documents: list[dict[str, Any]] = []
    for file_path in sorted(raw_dir.glob("*.md")):
        documents.append(read_markdown(file_path))
    return documents


def save_jsonl(records: list[dict[str, Any]], output_path: Path) -> None:
    """Save records in JSONL format."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as f:
        for record in records:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")


def inspect_chunks(chunks: list[dict[str, Any]]) -> None:
    """Print quality report."""
    chunk_lengths = [len(c["text"]) for c in chunks]
    total_chars = sum(chunk_lengths)
    domain_dist = defaultdict(int)
    for c in chunks:
        domain_dist[c["metadata"].get("domain", "unknown")] += 1

    # Check overlap integrity using metadata overlap_len
    overlap_ok = 0
    overlap_total = 0
    for i in range(1, len(chunks)):
        ol = chunks[i]["metadata"].get("overlap_len", 0)
        if ol > 0:
            overlap_total += 1
            if chunks[i - 1]["text"][-ol:] == chunks[i]["text"][:ol]:
                overlap_ok += 1

    print("=" * 80)
    print("PREPARE KNOWLEDGE BASE")
    print("=" * 80)
    print(f"Total chunks: {len(chunks)}")
    print(f"Total text: {total_chars} characters")
    print(f"Average chunk length: {total_chars // len(chunks)} characters")
    print(f"Min chunk: {min(chunk_lengths)} | Max chunk: {max(chunk_lengths)}")
    print(f"Overlap integrity: {overlap_ok}/{overlap_total} ({100 * overlap_ok // max(overlap_total, 1)}%)")
    print(f"Output: {OUTPUT_PATH}")
    print()

    print("Chunks per domain:")
    for domain, count in sorted(domain_dist.items()):
        print(f"  {domain}: {count}")
    print()

    # Warnings
    warnings = []
    for c in chunks:
        text_len = len(c["text"])
        if text_len < 200:
            warnings.append(f"{c['chunk_id']}: very short ({text_len})")
        if text_len > 1200:
            warnings.append(f"{c['chunk_id']}: very long ({text_len})")

    if warnings:
        print("Warnings:")
        for w in warnings[:10]:
            print(f"  ⚠️ {w}")
    else:
        print("No issues found.")


def main() -> None:
    documents = load_raw_sources(RAW_DIR)
    all_chunks: list[dict[str, Any]] = []
    for document in documents:
        all_chunks.extend(chunk_document(document, CHUNK_SIZE, CHUNK_OVERLAP))

    save_jsonl(all_chunks, OUTPUT_PATH)
    inspect_chunks(all_chunks)


if __name__ == "__main__":
    main()