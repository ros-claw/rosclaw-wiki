#!/usr/bin/env python3
"""wikilink_cleanup.py — clean up broken/placeholder wikilinks across wiki pages.

Fixes applied:
1. Remove [[wikilink]] placeholder (literal string used as example)
2. Convert relationship-type wikilinks to plain text
   (uses, depends_on, related_to, used_by, based_on, etc.)
3. Strip links to geographic/common-knowledge terms that don't have wiki pages
4. Remove empty/self links

Usage:
    .venv/bin/python scripts/wikilink_cleanup.py [--dry-run]
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

WIKI_ROOT = PROJECT_ROOT / "wiki"
WIKILINK_RE = re.compile(r"\[\[([^\]|]+)(?:\|([^\]]+))?\]\]")

# Words that are relationship types, not wiki page targets
RELATIONSHIP_WORDS = {
    "uses", "depends_on", "related_to", "used_by", "based_on",
    "contradicts", "supersedes", "extends", "implements", "requires",
    "references", "cites", "includes", "contains", "supports",
    "compatible_with", "replaces", "influenced_by", "part_of",
    "has_part", "instance_of", "subclass_of", "precedes", "follows",
    "wikilink",  # literal placeholder
}

# Geographic/common-knowledge terms that shouldn't be wikilinked
COMMON_TERMS = {
    "north america", "south america", "europe", "asia", "africa",
    "australia", "antarctica", "arctic", "pacific", "atlantic",
    "indian ocean", "mediterranean", "china", "japan", "usa",
    "united states", "germany", "france", "uk", "canada", "india",
    "russia", "brazil", "mexico", "korea", "singapore", "taiwan",
    "california", "texas", "new york", "london", "tokyo", "beijing",
    "github", "gitlab", "bitbucket", "pypi", "npm", "docker hub",
    "huggingface", "arxiv", "google scholar", "reddit", "twitter",
    "x", "discord", "slack", "telegram", "youtube", "wikipedia",
    "mit", "stanford", "cmu", "berkeley", "google", "microsoft",
    "meta", "openai", "anthropic", "deepmind", "nvidia",
    "python", "javascript", "typescript", "rust", "go", "c++",
    "cuda", "ros", "ros2", "linux", "ubuntu", "macos", "windows",
    "kubernetes", "docker", "aws", "azure", "gcp", "cloudflare",
    "react", "vue", "angular", "svelte", "next.js", "flask", "django",
    "fastapi", "spring boot", "express", "laravel", "rails",
}


def should_keep_link(target_raw: str, target_id: str, page_ids: set[str]) -> bool:
    """Return True if the wikilink target is valid and should be kept."""
    # Check exact match first (handles path prefixes like "entities/spot")
    if target_raw in page_ids:
        return True
    # Check id match
    if target_id in page_ids:
        return True
    # Filter relationship words
    if target_id.lower() in RELATIONSHIP_WORDS:
        return False
    if target_raw.lower() in RELATIONSHIP_WORDS:
        return False
    # Filter common terms
    if target_id.lower() in COMMON_TERMS:
        return False
    if target_raw.lower() in COMMON_TERMS:
        return False
    # Unknown target — it's a dead link
    return False


def fix_page(md_file: Path, page_ids: set[str], dry_run: bool = False) -> dict:
    """Fix wikilinks in a single page. Returns stats."""
    content = md_file.read_text(encoding="utf-8")
    original = content
    changes = {"removed": 0, "converted": 0, "kept": 0}

    def replacer(m: re.Match) -> str:
        target_raw = m.group(1).strip()
        display = m.group(2)
        target_id = target_raw.split("/")[-1].strip()

        if should_keep_link(target_raw, target_id, page_ids):
            changes["kept"] += 1
            return m.group(0)  # keep as-is

        # Remove the link — convert to plain text
        changes["removed"] += 1
        # Use display name if present, otherwise the target
        text = display.strip() if display else target_raw
        return text

    new_content = WIKILINK_RE.sub(replacer, content)

    if new_content != original and not dry_run:
        md_file.write_text(new_content, encoding="utf-8")

    return changes


def run_cleanup(wiki_root: Path, dry_run: bool = True) -> dict:
    """Run cleanup across all wiki pages."""
    # Collect all page ids first
    page_ids: set[str] = set()
    for md_file in wiki_root.rglob("*.md"):
        if md_file.name in ("index.md", "log.md"):
            continue
        content = md_file.read_text(encoding="utf-8")
        m = re.search(r"^id:\s*(\S+)", content, re.M)
        if m:
            page_ids.add(m.group(1).strip())
            # Also add the relative path as a valid target
            rel = str(md_file.relative_to(wiki_root)).replace("\\", "/")
            page_ids.add(rel)
            page_ids.add(rel.replace(".md", ""))

    total_removed = 0
    total_kept = 0
    files_changed = 0
    files_scanned = 0

    for md_file in wiki_root.rglob("*.md"):
        if md_file.name in ("index.md", "log.md"):
            continue
        files_scanned += 1
        changes = fix_page(md_file, page_ids, dry_run=dry_run)
        if changes["removed"] > 0 or changes["kept"] > 0:
            if changes["removed"] > 0:
                files_changed += 1
            total_removed += changes["removed"]
            total_kept += changes["kept"]

    return {
        "files_scanned": files_scanned,
        "files_changed": files_changed,
        "links_removed": total_removed,
        "links_kept": total_kept,
        "dry_run": dry_run,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Clean up broken wikilinks")
    parser.add_argument("--wiki-root", default=str(WIKI_ROOT))
    parser.add_argument("--dry-run", action="store_true", default=True,
                        help="Preview changes without writing (default)")
    parser.add_argument("--apply", action="store_true",
                        help="Actually write fixes to files")
    args = parser.parse_args()

    wiki_root = Path(args.wiki_root)
    dry_run = not args.apply

    result = run_cleanup(wiki_root, dry_run=dry_run)

    print("=" * 60)
    print("WIKILINK CLEANUP REPORT")
    print("=" * 60)
    print(f"Mode: {'DRY-RUN (preview only)' if dry_run else 'APPLY (writing files)'}")
    print(f"Files scanned: {result['files_scanned']}")
    print(f"Files that would change: {result['files_changed']}")
    print(f"Dead links removed: {result['links_removed']}")
    print(f"Valid links kept: {result['links_kept']}")
    print("=" * 60)

    if dry_run and result["links_removed"] > 0:
        print("\nRun with --apply to write these changes.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
