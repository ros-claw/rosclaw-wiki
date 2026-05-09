"""ROSClaw Entity Resolver — disambiguate and merge duplicate entities.

Uses whoosh search + difflib SequenceMatcher for name similarity,
with LLM-assisted resolution for borderline cases.
"""

from __future__ import annotations

import difflib
import logging
from pathlib import Path
from typing import Any

import search_backend
import wiki_engine as engine

logger = logging.getLogger("rosclaw.resolver")

# Similarity thresholds
MERGE_THRESHOLD = 0.9
LLM_THRESHOLD = 0.6


def find_candidate_entities(entity_name: str, wiki_root: str) -> list[dict[str, Any]]:
    """Find potentially matching existing entities.

    Uses whoosh search for candidate retrieval, then scores each
    candidate with difflib.SequenceMatcher on the entity name.

    Returns:
        List of candidates sorted by similarity descending.
        Each candidate has: path, title, similarity.
    """
    candidates: list[dict[str, Any]] = []
    seen_paths: set[str] = set()

    # 1. Whoosh search for candidates
    try:
        whoosh_results = search_backend.search_index(wiki_root, entity_name, limit=10)
        for hit in whoosh_results:
            rel = hit["file_path"]
            if rel in seen_paths:
                continue
            seen_paths.add(rel)
            title = hit.get("title", Path(rel).stem)
            sim = difflib.SequenceMatcher(None, entity_name.lower(), title.lower()).ratio()
            if sim >= LLM_THRESHOLD:
                candidates.append({"path": rel, "title": title, "similarity": round(sim, 3)})
    except Exception as exc:
        logger.warning("whoosh search failed in entity resolution: %s", exc)

    # 2. Also scan filenames directly (catches pages not well-indexed)
    root = Path(wiki_root)
    slug_name = engine.generate_page_id(entity_name)
    for md_file in root.rglob("*.md"):
        if md_file.name in ("index.md", "log.md", "Admin_Dashboard.md"):
            continue
        rel = str(md_file.relative_to(root))
        if rel in seen_paths:
            continue
        try:
            content = md_file.read_text(encoding="utf-8")
            meta, _ = engine.parse_frontmatter(content)
            title = meta.get("title", md_file.stem)
            sim = difflib.SequenceMatcher(None, entity_name.lower(), title.lower()).ratio()
            # Also compare slugs for exact filename matches
            slug_title = engine.generate_page_id(title)
            if slug_title == slug_name:
                sim = max(sim, 0.95)
            if sim >= LLM_THRESHOLD:
                seen_paths.add(rel)
                candidates.append({"path": rel, "title": title, "similarity": round(sim, 3)})
        except Exception:
            continue

    candidates.sort(key=lambda x: x["similarity"], reverse=True)
    return candidates


def resolve_entity(entity_name: str, wiki_root: str) -> dict[str, Any]:
    """Determine whether a new entity should be merged, reviewed, or created.

    Returns:
        - similarity > MERGE_THRESHOLD → {"action": "merge", "target": path}
        - similarity in [LLM_THRESHOLD, MERGE_THRESHOLD] → {"action": "llm_required", "candidates": [...]}
        - otherwise → {"action": "create_new"}
    """
    candidates = find_candidate_entities(entity_name, wiki_root)
    if not candidates:
        return {"action": "create_new"}

    best = candidates[0]
    if best["similarity"] >= MERGE_THRESHOLD:
        return {
            "action": "merge",
            "target": best["path"],
            "title": best["title"],
            "similarity": best["similarity"],
        }

    return {
        "action": "llm_required",
        "candidates": candidates[:5],
        "best_similarity": best["similarity"],
    }


def entity_dedup_report(wiki_root: str, similarity_threshold: float = 0.7) -> list[dict[str, Any]]:
    """Scan all wiki pages and report potential duplicates.

    Compares every pair of entity/algorithm/concept/skill pages
    and returns pairs with similarity >= threshold.

    Returns:
        List of duplicate pairs with similarity score.
    """
    root = Path(wiki_root)
    pages: list[dict[str, str]] = []

    for md_file in root.rglob("*.md"):
        if md_file.name in ("index.md", "log.md", "Admin_Dashboard.md"):
            continue
        try:
            content = md_file.read_text(encoding="utf-8")
            meta, _ = engine.parse_frontmatter(content)
            title = meta.get("title", md_file.stem)
            rel = str(md_file.relative_to(root))
            pages.append({"path": rel, "title": title})
        except Exception:
            continue

    duplicates: list[dict[str, Any]] = []
    n = len(pages)
    for i in range(n):
        for j in range(i + 1, n):
            sim = difflib.SequenceMatcher(
                None, pages[i]["title"].lower(), pages[j]["title"].lower()
            ).ratio()
            if sim >= similarity_threshold:
                duplicates.append(
                    {
                        "page_a": pages[i]["path"],
                        "title_a": pages[i]["title"],
                        "page_b": pages[j]["path"],
                        "title_b": pages[j]["title"],
                        "similarity": round(sim, 3),
                    }
                )

    duplicates.sort(key=lambda x: x["similarity"], reverse=True)
    return duplicates


def write_dedup_report(wiki_root: str, output_dir: str | None = None) -> Path:
    """Generate and save a deduplication report to disk.

    Returns:
        Path to the written report file.
    """
    duplicates = entity_dedup_report(wiki_root)
    out_dir = Path(output_dir or Path(wiki_root).parent / "data" / "quality_reports")
    out_dir.mkdir(parents=True, exist_ok=True)

    lines = ["# Entity Deduplication Report\n", f"**Wiki Root:** {wiki_root}\n", f"**Potential Duplicates:** {len(duplicates)}\n"]
    if not duplicates:
        lines.append("\nNo potential duplicates found.\n")
    else:
        lines.append("\n| Title A | Title B | Similarity |\n")
        lines.append("|---------|---------|------------|\n")
        for d in duplicates:
            lines.append(f"| {d['title_a']} | {d['title_b']} | {d['similarity']} |\n")

    report_path = out_dir / "dedup_candidates.md"
    report_path.write_text("".join(lines), encoding="utf-8")
    logger.info("Deduplication report written to %s", report_path)
    return report_path
