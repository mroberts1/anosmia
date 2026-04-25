#!/usr/bin/env python3
"""
Compile: Scan raw/ for new or updated files and report what needs ingesting.

This is a helper that identifies unprocessed raw documents by comparing
raw/ contents against wiki/sources/. The actual LLM compilation is done
by the LLM agent — this script just identifies the work to be done.

Usage:
    python tools/compile.py [--vault-path PATH]
"""

import argparse
import os
import re
from pathlib import Path


def get_vault_path(override=None):
    if override:
        return Path(override)
    return Path(__file__).parent.parent


def slugify(name):
    """Convert a filename to a wiki-friendly slug."""
    name = Path(name).stem
    name = re.sub(r'[^\w\s-]', '', name)
    name = re.sub(r'[-\s]+', '-', name).strip('-')
    return name


def get_raw_files(vault):
    """Get all files in raw/ (excluding images used as attachments)."""
    raw_dir = vault / "raw"
    files = []
    for root, dirs, filenames in os.walk(raw_dir):
        # Skip hidden directories
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        for f in filenames:
            if f.startswith('.'):
                continue
            filepath = Path(root) / f
            rel = filepath.relative_to(raw_dir)
            files.append(rel)
    return sorted(files)


def get_source_summaries(vault):
    """Get all existing source summaries."""
    sources_dir = vault / "wiki" / "sources"
    if not sources_dir.exists():
        return set()
    summaries = set()
    for f in sources_dir.glob("*.md"):
        summaries.add(f.stem.lower())
    return summaries


def find_unprocessed(vault):
    """Find raw files that don't have corresponding source summaries."""
    raw_files = get_raw_files(vault)
    existing = get_source_summaries(vault)
    unprocessed = []
    for f in raw_files:
        slug = slugify(f.name).lower()
        # Also check with the parent directory as prefix
        if slug not in existing and f.stem.lower() not in existing:
            unprocessed.append(f)
    return unprocessed


def get_stats(vault):
    """Get current wiki statistics."""
    wiki_dir = vault / "wiki"
    concepts = list((wiki_dir / "concepts").glob("*.md")) if (wiki_dir / "concepts").exists() else []
    sources = list((wiki_dir / "sources").glob("*.md")) if (wiki_dir / "sources").exists() else []

    total_words = 0
    for md_dir in [wiki_dir / "concepts", wiki_dir / "sources"]:
        if md_dir.exists():
            for f in md_dir.glob("*.md"):
                total_words += len(f.read_text().split())

    return {
        "concepts": len(concepts),
        "sources": len(sources),
        "total_words": total_words,
    }


def main():
    parser = argparse.ArgumentParser(description="KB Compile Helper")
    parser.add_argument("--vault-path", help="Path to vault root")
    parser.add_argument("--stats", action="store_true", help="Show wiki stats")
    args = parser.parse_args()

    vault = get_vault_path(args.vault_path)

    if args.stats:
        stats = get_stats(vault)
        print(f"Concepts: {stats['concepts']}")
        print(f"Sources:  {stats['sources']}")
        print(f"Words:    {stats['total_words']}")
        return

    unprocessed = find_unprocessed(vault)
    if not unprocessed:
        print("All raw files have been processed. Wiki is up to date.")
    else:
        print(f"Found {len(unprocessed)} unprocessed raw file(s):\n")
        for f in unprocessed:
            print(f"  - raw/{f}")
        print(f"\nRun the LLM ingest workflow to compile these into the wiki.")


if __name__ == "__main__":
    main()
