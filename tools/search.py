#!/usr/bin/env python3
"""
Search: Simple search engine over the knowledge base wiki.

Searches across all wiki markdown files using TF-IDF-like scoring.
Can be used directly via CLI or handed to an LLM as a tool.

Usage:
    python tools/search.py "query terms" [--vault-path PATH] [--limit N]
    python tools/search.py "query terms" --full   # Show full matched content
"""

import argparse
import math
import re
from collections import Counter
from pathlib import Path


def get_vault_path(override=None):
    if override:
        return Path(override)
    return Path(__file__).parent.parent


def tokenize(text):
    """Simple tokenizer: lowercase, split on non-alphanumeric."""
    return re.findall(r'[a-z0-9]+', text.lower())


def search(vault, query, limit=10, full=False):
    wiki_dir = vault / "wiki"
    if not wiki_dir.exists():
        print("No wiki/ directory found.")
        return

    query_tokens = tokenize(query)
    if not query_tokens:
        print("Empty query.")
        return

    # Index all documents
    docs = {}
    for f in wiki_dir.rglob("*.md"):
        text = f.read_text()
        rel = str(f.relative_to(vault))
        docs[rel] = {
            "path": f,
            "text": text,
            "tokens": tokenize(text),
            "title": f.stem,
        }

    if not docs:
        print("Wiki is empty.")
        return

    # Calculate IDF
    n_docs = len(docs)
    doc_freq = Counter()
    for doc in docs.values():
        unique_tokens = set(doc["tokens"])
        for t in unique_tokens:
            doc_freq[t] += 1

    idf = {}
    for token in query_tokens:
        df = doc_freq.get(token, 0)
        idf[token] = math.log((n_docs + 1) / (df + 1)) + 1

    # Score each document
    results = []
    for path, doc in docs.items():
        token_counts = Counter(doc["tokens"])
        n_tokens = len(doc["tokens"]) or 1

        score = 0
        for qt in query_tokens:
            tf = token_counts.get(qt, 0) / n_tokens
            score += tf * idf.get(qt, 0)

        # Boost for title matches
        title_tokens = tokenize(doc["title"])
        for qt in query_tokens:
            if qt in title_tokens:
                score *= 2.0

        if score > 0:
            results.append((score, path, doc))

    results.sort(reverse=True)
    results = results[:limit]

    if not results:
        print(f"No results for: {query}")
        return

    print(f"Search results for: \"{query}\"\n")
    for i, (score, path, doc) in enumerate(results, 1):
        print(f"{i}. [{doc['title']}] ({path})")
        print(f"   Score: {score:.4f}")

        if full:
            # Show first 500 chars of content (skip frontmatter)
            text = doc["text"]
            if text.startswith("---"):
                end = text.find("\n---\n", 4)
                if end != -1:
                    text = text[end + 5:]
            text = text.strip()[:500]
            print(f"   {text}")
        else:
            # Show snippet around first match
            text = doc["text"]
            for qt in query_tokens:
                pattern = re.compile(re.escape(qt), re.IGNORECASE)
                match = pattern.search(text)
                if match:
                    start = max(0, match.start() - 80)
                    end = min(len(text), match.end() + 80)
                    snippet = text[start:end].replace('\n', ' ').strip()
                    print(f"   ...{snippet}...")
                    break
        print()


def main():
    parser = argparse.ArgumentParser(description="KB Search")
    parser.add_argument("query", help="Search query")
    parser.add_argument("--vault-path", help="Path to vault root")
    parser.add_argument("--limit", type=int, default=10, help="Max results")
    parser.add_argument("--full", action="store_true", help="Show full content")
    args = parser.parse_args()

    vault = get_vault_path(args.vault_path)
    search(vault, args.query, args.limit, args.full)


if __name__ == "__main__":
    main()
