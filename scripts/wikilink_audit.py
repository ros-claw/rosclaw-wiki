#!/usr/bin/env python3
"""wikilink_audit.py — scan all wiki pages for link quality issues.

Checks:
1. Dead wikilinks — targets that don't exist as pages
2. Orphan pages — pages with zero inbound wikilinks
3. Self-links — pages linking to themselves
4. Empty/malformed wikilinks
5. Duplicate slugs — different paths with same id

Usage:
    .venv/bin/python scripts/wikilink_audit.py [--fix] [--output report.json]
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "utils"))
sys.path.insert(0, str(PROJECT_ROOT / "core"))

WIKI_ROOT = PROJECT_ROOT / "wiki"
WIKILINK_RE = re.compile(r"\[\[([^\]|]+)(?:\|([^\]]+))?\]\]")


def collect_pages(wiki_root: Path) -> dict[str, Path]:
    """Map page id (from frontmatter) → file path."""
    pages: dict[str, Path] = {}
    for md_file in wiki_root.rglob("*.md"):
        if md_file.name in ("index.md", "log.md"):
            continue
        content = md_file.read_text(encoding="utf-8")
        # Extract id from frontmatter
        m = re.search(r"^id:\s*(\S+)", content, re.M)
        if m:
            page_id = m.group(1).strip()
            pages[page_id] = md_file
    return pages


def collect_wikilinks(content: str, source_id: str) -> list[dict]:
    """Extract all wikilinks from page content."""
    links = []
    for m in WIKILINK_RE.finditer(content):
        target_raw = m.group(1).strip()
        display = (m.group(2) or "").strip()
        # Target may include path prefix like "entities/spot"
        # We care about the actual target id
        target_id = target_raw.split("/")[-1].strip()
        links.append({
            "target_raw": target_raw,
            "target_id": target_id,
            "display": display,
            "span": m.span(),
        })
    return links


def run_audit(wiki_root: Path, fix: bool = False) -> dict:
    pages = collect_pages(wiki_root)
    page_ids = set(pages.keys())

    # Inbound link tracking
    inbound: dict[str, list[tuple[str, str]]] = defaultdict(list)  # target_id -> [(source_id, target_raw)]
    dead_links: list[dict] = []
    self_links: list[dict] = []
    empty_links: list[dict] = []
    malformed: list[dict] = []

    for page_id, md_file in pages.items():
        content = md_file.read_text(encoding="utf-8")
        links = collect_wikilinks(content, page_id)

        for link in links:
            target_id = link["target_id"]
            target_raw = link["target_raw"]

            if not target_id:
                empty_links.append({"source": page_id, "file": str(md_file), "raw": target_raw})
                continue

            if target_id == page_id:
                self_links.append({"source": page_id, "file": str(md_file), "target": target_raw})
                continue

            # Check if target exists
            if target_id not in page_ids:
                # Also check if target_raw (with path prefix) exists as an id
                if target_raw not in page_ids:
                    dead_links.append({
                        "source": page_id,
                        "file": str(md_file),
                        "target": target_raw,
                        "target_id": target_id,
                    })
                else:
                    inbound[target_raw].append((page_id, target_raw))
            else:
                inbound[target_id].append((page_id, target_raw))

    # Orphan pages = pages with zero inbound links
    orphan_ids = [pid for pid in page_ids if pid not in inbound and pid not in {"index", "log"}]
    orphans = [{"id": pid, "file": str(pages[pid])} for pid in orphan_ids]

    # Duplicate ids check — same id in multiple files
    id_to_files: dict[str, list[Path]] = defaultdict(list)
    for pid, path in pages.items():
        id_to_files[pid].append(path)
    duplicates = {pid: [str(p) for p in paths] for pid, paths in id_to_files.items() if len(paths) > 1}

    result = {
        "total_pages": len(pages),
        "dead_links": {
            "count": len(dead_links),
            "items": dead_links[:200],  # cap output
        },
        "orphan_pages": {
            "count": len(orphans),
            "items": orphans[:200],
        },
        "self_links": {
            "count": len(self_links),
            "items": self_links[:50],
        },
        "empty_links": {
            "count": len(empty_links),
            "items": empty_links[:50],
        },
        "duplicate_ids": {
            "count": len(duplicates),
            "items": {k: v for k, v in list(duplicates.items())[:50]},
        },
        "inbound_stats": {
            "max_inbound": max((len(v) for v in inbound.values()), default=0),
            "median_inbound": 0,
            "pages_with_inbound": len(inbound),
            "pages_without_inbound": len(orphans),
        },
    }

    # Median inbound
    inbound_counts = sorted([len(v) for v in inbound.values()], reverse=True)
    if inbound_counts:
        result["inbound_stats"]["median_inbound"] = inbound_counts[len(inbound_counts) // 2]

    return result


def print_report(result: dict) -> None:
    print("=" * 60)
    print("WIKILINK AUDIT REPORT")
    print("=" * 60)
    print(f"\nTotal pages scanned: {result['total_pages']}")
    print(f"\n--- Dead links (target doesn't exist): {result['dead_links']['count']} ---")
    if result["dead_links"]["items"]:
        for item in result["dead_links"]["items"][:20]:
            print(f"  [{item['source']}] -> [[{item['target']}]] (file: {item['file']})")
        if result["dead_links"]["count"] > 20:
            print(f"  ... and {result['dead_links']['count'] - 20} more")

    print(f"\n--- Orphan pages (no inbound links): {result['orphan_pages']['count']} ---")
    if result["orphan_pages"]["items"]:
        for item in result["orphan_pages"]["items"][:20]:
            print(f"  {item['id']} ({item['file']})")
        if result["orphan_pages"]["count"] > 20:
            print(f"  ... and {result['orphan_pages']['count'] - 20} more")

    print(f"\n--- Self-links: {result['self_links']['count']} ---")
    print(f"\n--- Empty/malformed links: {result['empty_links']['count']} ---")
    print(f"\n--- Duplicate IDs: {result['duplicate_ids']['count']} ---")

    print(f"\n--- Inbound link stats ---")
    print(f"  Pages with inbound links: {result['inbound_stats']['pages_with_inbound']}")
    print(f"  Pages without inbound links (orphans): {result['inbound_stats']['pages_without_inbound']}")
    print(f"  Max inbound links to a page: {result['inbound_stats']['max_inbound']}")
    print(f"  Median inbound links: {result['inbound_stats']['median_inbound']}")
    print("=" * 60)


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit wikilink quality across the wiki")
    parser.add_argument("--wiki-root", default=str(WIKI_ROOT), help="Path to wiki directory")
    parser.add_argument("--fix", action="store_true", help="Attempt to fix issues (not yet implemented)")
    parser.add_argument("--output", default=None, help="Write JSON report to file")
    args = parser.parse_args()

    wiki_root = Path(args.wiki_root)
    result = run_audit(wiki_root, fix=args.fix)
    print_report(result)

    if args.output:
        Path(args.output).write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"\nFull report written to: {args.output}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
