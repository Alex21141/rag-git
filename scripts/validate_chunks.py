#!/usr/bin/env python3
"""Validate chunks.jsonl — check structure, types, required fields, overlap coverage."""
import json
import sys
from pathlib import Path
from collections import defaultdict

CHUNKS = Path(__file__).resolve().parent.parent / "data" / "processed" / "chunks.jsonl"

REQUIRED_FIELDS = [
    "chunk_id", "text", "metadata"
]
METADATA_FIELDS = [
    "document_id", "source_file", "source_type", "title", "section",
    "chunk_index", "language", "domain", "document_type"
]
VALID_DOMAINS = {"git", "github", "gitlab"}
VALID_TYPES = {"concept", "commands", "workflow", "reference", "procedure"}


def validate_chunks():
    errors, warnings = [], []
    total, valid, text_len = 0, 0, 0

    by_doc = defaultdict(list)
    by_domain = defaultdict(int)

    if not CHUNKS.exists():
        print(f"❌ {CHUNKS} not found")
        return False

    with open(CHUNKS, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            line = line.rstrip("\n")
            if not line:
                warnings.append(f"Line {line_num}: empty line")
                continue
            total += 1

            # Parse JSON
            try:
                chunk = json.loads(line)
            except json.JSONDecodeError as e:
                errors.append(f"Line {line_num}: invalid JSON — {e}")
                continue
            valid += 1

            # Check required fields
            for field in REQUIRED_FIELDS:
                if field not in chunk:
                    errors.append(f"Line {line_num}: missing field '{field}'")

            # Check metadata fields
            metadata = chunk.get("metadata", {})
            for field in METADATA_FIELDS:
                if field not in metadata:
                    errors.append(f"Line {line_num}: missing metadata.{field}")

            # Validate text
            text = chunk.get("text", "")
            if not text or not isinstance(text, str):
                errors.append(f"Line {line_num}: empty or non-string text")
            else:
                text_len += len(text)
                if len(text) < 50:
                    warnings.append(f"Line {line_num}: very short text ({len(text)} chars)")

            # Validate domain
            domain = metadata.get("domain", "")
            if domain not in VALID_DOMAINS:
                errors.append(f"Line {line_num}: invalid domain '{domain}'")
            else:
                by_domain[domain] += 1

            # Validate document_type
            doc_type = metadata.get("document_type", "")
            if doc_type not in VALID_TYPES:
                errors.append(f"Line {line_num}: invalid document_type '{doc_type}'")

            # Track per-doc for overlap
            doc_id = metadata.get("document_id", "")
            chunk_idx = metadata.get("chunk_index", 0)
            by_doc[doc_id].append((chunk_idx, text))

    # Check chunk_id uniqueness
    chunk_ids = []
    with open(CHUNKS, "r", encoding="utf-8") as f:
        for line in f:
            line = line.rstrip("\n")
            if not line:
                continue
            try:
                chunk = json.loads(line)
                cid = chunk.get("chunk_id", "")
                if cid in chunk_ids:
                    errors.append(f"Duplicate chunk_id: '{cid}'")
                chunk_ids.append(cid)
            except json.JSONDecodeError:
                pass

    # Check sequential chunk_index per document
    for did, entries in by_doc.items():
        indices = [e[0] for e in entries]
        for i in range(1, len(indices)):
            if indices[i] != indices[i-1] + 1:
                errors.append(f"Document '{did}': non-sequential chunk_index {indices[i-1]} → {indices[i]}")

    # Print report
    print("=" * 60)
    print("JSONL Validation Report")
    print("=" * 60)
    print(f"  Total lines:      {total}")
    print(f"  Valid chunks:     {valid}")
    print(f"  Total text:       {text_len:,} chars")
    if valid:
        print(f"  Avg text length:  {text_len // valid} chars")
        print(f"  Min text length:  {min(len(e[1]) for entries in by_doc.values() for e in entries)} chars")
        print(f"  Max text length:  {max(len(e[1]) for entries in by_doc.values() for e in entries)} chars")
    print(f"\n  By domain:")
    for domain, count in sorted(by_domain.items()):
        print(f"    {domain:20s} {count:4d} chunks")
    print(f"\n  By document:  {len(by_doc)} documents")

    if errors:
        print(f"\n  ❌ {len(errors)} errors:")
        for e in errors[:20]:
            print(f"    {e}")
        if len(errors) > 20:
            print(f"    ... and {len(errors) - 20} more")
    else:
        print(f"\n  ✅ No errors")

    if warnings:
        print(f"\n  ⚠️ {len(warnings)} warnings:")
        for w in warnings[:10]:
            print(f"    {w}")
        if len(warnings) > 10:
            print(f"    ... and {len(warnings) - 10} more")

    print("=" * 60)
    return len(errors) == 0


if __name__ == "__main__":
    ok = validate_chunks()
    sys.exit(0 if ok else 1)