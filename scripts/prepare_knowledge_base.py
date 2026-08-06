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


def _backtick_balanced(text: str) -> bool:
    """Check if text has balanced backticks.

    Handles both code fences (```) and inline code (`).
    Code fences are balanced if count of ``` is even.
    Inline backticks are balanced after removing code fences.
    """
    fence_count = text.count('```')
    if fence_count % 2 == 1:
        return False  # Unclosed code fence
    inline_count = text.count('`') - fence_count * 3
    return inline_count % 2 == 0


def fix_unclosed_backticks(chunk_text: str, full_text: str, start: int, end: int) -> str:
    """No-op: do NOT modify chunk_text here.

    Extending chunk_text (forward search) breaks the overlap chain because
    the last `ol` chars of this chunk no longer match the first `ol` chars
    of the next chunk. Step 2.8 handles remaining odd backticks.
    """
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

        # Track overlap length for post-processing
        actual_overlap_len = 0

        # Prepend overlap from previous chunk (last `overlap` chars of raw text)
        if prev_end > 0:
            overlap_start = max(0, prev_end - overlap)
            overlap_text = text[overlap_start:prev_end].strip()

            if overlap_text:
                if overlap_text == raw_chunk[:len(overlap_text)]:
                    # Overlap already in raw_chunk — no duplication needed,
                    # but track it for verification
                    chunk_text = raw_chunk
                    actual_overlap_len = len(overlap_text)
                else:
                    # Add space if needed
                    if not overlap_text.endswith((" ", "\n", "\t")) and raw_chunk and not raw_chunk.startswith((" ", "\n", "\t")):
                        chunk_text = overlap_text + " " + raw_chunk
                        actual_overlap_len = len(overlap_text) + 1  # +1 for space
                    else:
                        chunk_text = overlap_text + raw_chunk
                        actual_overlap_len = len(overlap_text)
            else:
                chunk_text = raw_chunk
                actual_overlap_len = 0
        else:
            chunk_text = raw_chunk
            actual_overlap_len = 0

        # Fix unclosed inline backticks AFTER overlap prepending
        chunk_text = fix_unclosed_backticks(chunk_text, text, start, end)

        # Update prev_end to original boundary (NOT extended) to preserve overlap chain
        prev_end = end

        # Resolve section
        section = None
        if section_map:
            section = resolve_section(section_map, start, "Unknown")

        # Filter by min_chunk
        if len(chunk_text) >= min_chunk:
            chunks.append((start, end, chunk_text, section, actual_overlap_len))

        # Advance start: sliding window with overlap
        new_start = end - overlap
        # Ensure forward progress — never go backward or stay still
        if new_start <= start:
            start = end  # fallback: no overlap if sentence break is too close
        else:
            start = new_start

    return chunks


def _capitalize_chunk(text: str) -> str:
    """Capitalize first letter of chunk text.

    Does NOT try to fix mid-word fragments here — that is done
    in a post-processing step using overlap context to avoid
    false positives (e.g. 'It checked out' is NOT a fragment).
    """
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
        for start_pos, end_pos, chunk_text, section, overlap_len in raw_splits:
            if section is None:
                section = title
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
                    "overlap_len": overlap_len,
                },
            })

        all_chunks.extend(final_chunks)
        print(f"  {doc_file.name}: {len(final_chunks)} chunks")

    # Capitalize first alpha char of raw content (after overlap zone)
    # This preserves overlap chain: prev[-ol:] == curr[:ol:]
    print(f"\n{'=' * 60}")
    print("Step 2.4: Capitalize raw content (skip overlap)")
    print("=" * 60)
    cap_count = 0
    for c in all_chunks:
        text = c["text"]
        ol = c["metadata"].get("overlap_len", 0)
        raw = text[ol:]
        for j, ch in enumerate(raw):
            if ch.isalpha():
                c["text"] = text[:ol + j] + ch.upper() + text[ol + j + 1:]
                cap_count += 1
                break
    print(f"  Capitalized {cap_count} chunks")

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

    # Fix mid-word fragments (post-processing)
    print(f"\n{'=' * 60}")
    print("Step 2.7: Fixing mid-word fragments")
    print("=" * 60)
    fragment_fixes = 0
    overlap_skipped = 0
    COMMON_START_WORDS = {
        # 1-2 letter common English words (single-letter: a, i only)
        "a", "an", "in", "on", "at", "to", "as", "by", "or", "if", "no", "so", "up",
        "it", "is", "be", "do", "go", "we", "he", "my", "us", "am", "i",
        # 3 letter common English words
        "the", "but", "for", "not", "all", "can", "had", "how", "new", "now",
        "old", "see", "way", "who", "did", "let", "say", "she", "too", "use",
        "and", "any", "get", "our", "out", "own", "has", "her", "him", "his",
        "are", "was", "you", "yet",
    }
    for i, c in enumerate(all_chunks):
        text = c["text"]
        if not text:
            continue

        # Get overlap length — fragments in overlap zone must NOT be modified
        # (they are legitimate overlap text from the previous chunk)
        overlap_len = c["metadata"].get("overlap_len", 0)

        # Pattern 1: apostrophe/quote fragment: ''S history -> History
        m = re.match(r"^[''\u2019\u2018]+[A-Za-z]+([\s\-\—._:;,]+)([a-z])", text)
        if m:
            if m.end() <= overlap_len:
                overlap_skipped += 1
                continue  # fragment is in overlap zone — skip
            rest = text[m.end():]
            c["text"] = m.group(2).upper() + rest
            fragment_fixes += 1
            if fragment_fixes <= 3:
                print(f"  Fixed (apos) {c['chunk_id']}: '{text[:25]}' -> '{c['text'][:25]}'")
            continue

        # Pattern 2: 1-3 letter token NOT in common words list
        # Catches mid-word fragments: Er, Eir, Ing, Nce, D, Ed, O, Y, Te, U've
        # Legitimate words (The, And, But, It, In, You, etc.) are skipped.
        m = re.match(r"^([A-Za-z]{1,3})(\b)", text)
        if m:
            first_word = m.group(1)
            if first_word.lower() not in COMMON_START_WORDS:
                # Skip if the fragment end is within overlap zone
                if m.end() <= overlap_len:
                    overlap_skipped += 1
                    continue
                rest = text[m.end():]
                # Strip leading non-alpha chars (punctuation, apostrophes, spaces)
                rest = re.sub(r'^[^a-zA-Z]*', '', rest)
                # Handle contraction fragments: "U've never" → rest="ve never"
                # "ve" is itself a fragment → skip past it to find the real word
                m_rest_frag = re.match(r"^([a-z]{1,3})\b", rest)
                if m_rest_frag:
                    rest2 = rest[m_rest_frag.end():]
                    rest2 = re.sub(r'^[^a-zA-Z]*', '', rest2)
                    if rest2 and rest2[0].isalpha() and len(rest2) > 3:
                        old_start = text[:30]
                        c["text"] = rest2[0].upper() + rest2[1:]
                        fragment_fixes += 1
                        if fragment_fixes <= 10:
                            print(f"  Fixed {c['chunk_id']}: '{old_start}' -> '{c['text'][:30]}'")
                        continue
                # No contraction fragment — use rest directly
                if rest and rest[0].isalpha():
                    old_start = text[:30]
                    c["text"] = rest[0].upper() + rest[1:]
                    fragment_fixes += 1
                    if fragment_fixes <= 10:
                        print(f"  Fixed {c['chunk_id']}: '{old_start}' -> '{c['text'][:30]}'")
                    continue

    print(f"  Total fragments fixed: {fragment_fixes}")
    if overlap_skipped:
        print(f"  Fragments in overlap zone (skipped): {overlap_skipped}")

    # Final pass: fix odd backticks ONLY for last chunks in document (overlap_len=0)
    # Extending a chunk with overlap breaks the chain: prev[-ol:] != next[:ol]
    print(f"\n{'=' * 60}")
    print("Step 2.8: Final backtick balance check (overlap_len=0 only)")
    print("=" * 60)
    backtick_fixes = 0
    for i, c in enumerate(all_chunks):
        ol = c["metadata"].get("overlap_len", 0)
        if ol > 0:
            # Has a next sibling — extending would break overlap chain
            continue
        text = c["text"]
        fence_count = text.count('```')
        inline = text.count('`') - fence_count * 3
        if fence_count % 2 == 1 or inline % 2 == 1:
            # Unbalanced — find in source and extend forward
            did = c["metadata"]["source_file"]
            try:
                with open(did) as sf:
                    source = sf.read()
                search_str = text[-150:] if len(text) > 150 else text[-80:]
                src_pos = source.find(search_str)
                if src_pos >= 0:
                    chunk_end_in_src = src_pos + len(search_str)
                    for pos in range(chunk_end_in_src, min(chunk_end_in_src + 500, len(source))):
                        candidate = text + source[chunk_end_in_src:pos + 1]
                        fc = candidate.count('```')
                        ic = candidate.count('`') - fc * 3
                        if fc % 2 == 0 and ic % 2 == 0:
                            c["text"] = candidate.strip()
                            backtick_fixes += 1
                            print(f"  Fixed (inline) {c['chunk_id']}")
                            break
                        if source[pos:pos + 2] == '# ' and fc % 2 == 0:
                            break
            except FileNotFoundError:
                pass
    print(f"  Total backtick fixes: {backtick_fixes}")

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