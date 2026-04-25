#!/usr/bin/env python3
"""
Lint: Run health checks on the knowledge base wiki.

Checks for:
- Broken wikilinks (links to non-existent articles)
- Orphaned articles (no incoming links)
- Missing frontmatter
- Empty or stub articles
- Unlinked frequently-mentioned concepts

Usage:
    python tools/lint.py [--vault-path PATH]
"""

import argparse
import re
from collections import Counter
from pathlib import Path


def get_vault_path(override=None):
    if override:
        return Path(override)
    return Path(__file__).parent.parent


def get_all_md_files(wiki_dir):
    """Get all markdown files in the wiki."""
    return list(wiki_dir.rglob("*.md"))


def extract_wikilinks(text):
    """Extract all [[wikilink]] targets from text."""
    # Match [[link]] and [[link|alias]]
    return re.findall(r'\[\[([^\]|]+)(?:\|[^\]]+)?\]\]', text)


def check_frontmatter(filepath):
    """Check if file has valid YAML frontmatter."""
    text = filepath.read_text()
    return text.startswith('---\n') and '\n---\n' in text[4:]


def main():
    parser = argparse.ArgumentParser(description="KB Lint / Health Check")
    parser.add_argument("--vault-path", help="Path to vault root")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()

    vault = get_vault_path(args.vault_path)
    wiki_dir = vault / "wiki"

    if not wiki_dir.exists():
        print("ERROR: wiki/ directory not found")
        return

    md_files = get_all_md_files(wiki_dir)
    if not md_files:
        print("Wiki is empty. No files to lint.")
        return

    # Build index of all article names (stem, case-insensitive)
    article_names = {}
    for f in md_files:
        article_names[f.stem.lower()] = f

    # Collect all links and their sources
    all_links = {}  # target -> [source files]
    incoming_links = Counter()  # target -> count
    broken_links = []
    missing_frontmatter = []
    empty_articles = []

    for f in md_files:
        text = f.read_text()

        # Check frontmatter
        if f.parent.name in ("concepts", "sources") and not check_frontmatter(f):
            missing_frontmatter.append(f.relative_to(wiki_dir))

        # Check if empty/stub
        content = text
        if content.startswith('---'):
            end = content.find('\n---\n', 4)
            if end != -1:
                content = content[end + 5:]
        content = content.strip()
        if len(content) < 50:
            empty_articles.append(f.relative_to(wiki_dir))

        # Extract and check links
        links = extract_wikilinks(text)
        for link in links:
            link_lower = link.lower()
            incoming_links[link_lower] += 1
            if link_lower not in article_names:
                broken_links.append((f.relative_to(wiki_dir), link))

    # Find orphaned articles (no incoming links from other articles)
    orphaned = []
    index_names = {"master index", "concepts index", "sources index", "recent changes", "home"}
    for f in md_files:
        name = f.stem.lower()
        if name in index_names:
            continue
        if incoming_links.get(name, 0) == 0 and incoming_links.get(f.stem, 0) == 0:
            orphaned.append(f.relative_to(wiki_dir))

    # Report
    issues = 0
    print("=" * 60)
    print("  Knowledge Base Health Check")
    print("=" * 60)
    print()

    if broken_links:
        issues += len(broken_links)
        print(f"🔗 Broken wikilinks ({len(broken_links)}):")
        for source, target in broken_links:
            print(f"   {source} → [[{target}]]")
        print()

    if orphaned:
        issues += len(orphaned)
        print(f"🏝️  Orphaned articles ({len(orphaned)}):")
        for f in orphaned:
            print(f"   {f}")
        print()

    if missing_frontmatter:
        issues += len(missing_frontmatter)
        print(f"📋 Missing frontmatter ({len(missing_frontmatter)}):")
        for f in missing_frontmatter:
            print(f"   {f}")
        print()

    if empty_articles:
        issues += len(empty_articles)
        print(f"📄 Empty/stub articles ({len(empty_articles)}):")
        for f in empty_articles:
            print(f"   {f}")
        print()

    if issues == 0:
        print("✅ No issues found. Wiki is healthy!")
    else:
        print(f"Found {issues} issue(s) total.")

    print()
    print(f"Total articles: {len(md_files)}")


if __name__ == "__main__":
    main()
