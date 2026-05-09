"""ROSClaw Heuristic Entity Linker — rule-based relationship discovery.

Zero LLM calls. Uses regex, sentence patterns, and type inference
to automatically discover and create typed relationships between wiki pages.

Inspired by GBrain's auto-link post-hook and context routing infrastructure.
"""

from __future__ import annotations

import logging
import re
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any

import wiki_engine as engine

logger = logging.getLogger("rosclaw.entity_linker")

# ── Page Index Cache ──
_page_index_cache: dict[str, dict[str, Path]] = {}


# ── Regex Patterns ──

_WIKILINK_RE = re.compile(r"\[\[([^\]|]+)(?:\|[^\]]+)?\]\]")
_MARKDOWN_LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")

# Sentence-level relationship patterns: (regex, relation_type)
_RELATION_PATTERNS: list[tuple[re.Pattern, str]] = [
    # X uses Y for Z / X uses Y
    (re.compile(r"(?i)\b([^,\.]{3,50})\s+uses?\s+([^,\.]{3,50})(?:\s+for\s+[^,\.]+)?", re.IGNORECASE), "uses"),
    # X is based on Y
    (re.compile(r"(?i)\b([^,\.]{3,50})\s+is\s+based\s+on\s+([^,\.]{3,50})", re.IGNORECASE), "based_on"),
    # X depends on Y
    (re.compile(r"(?i)\b([^,\.]{3,50})\s+depends?\s+on\s+([^,\.]{3,50})", re.IGNORECASE), "depends_on"),
    # X implements Y
    (re.compile(r"(?i)\b([^,\.]{3,50})\s+implements?\s+([^,\.]{3,50})", re.IGNORECASE), "implements"),
    # X extends Y
    (re.compile(r"(?i)\b([^,\.]{3,50})\s+extends?\s+([^,\.]{3,50})", re.IGNORECASE), "extends"),
    # X is inspired by Y
    (re.compile(r"(?i)\b([^,\.]{3,50})\s+is\s+inspired\s+by\s+([^,\.]{3,50})", re.IGNORECASE), "inspired_by"),
    # X developed by Y
    (re.compile(r"(?i)\b([^,\.]{3,50})\s+(?:is\s+)?developed\s+by\s+([^,\.]{3,50})", re.IGNORECASE), "developed_by"),
    # X built with Y
    (re.compile(r"(?i)\b([^,\.]{3,50})\s+built\s+(?:with|using)\s+([^,\.]{3,50})", re.IGNORECASE), "built_with"),
]

# Type-based default relation mapping: (source_type, target_type) -> relation
_TYPE_RELATION_MAP: dict[tuple[str, str], str] = {
    ("entity", "entity"): "depends_on",
    ("entity", "algorithm"): "uses",
    ("entity", "concept"): "related_to",
    ("algorithm", "entity"): "implements",
    ("algorithm", "algorithm"): "extends",
    ("algorithm", "concept"): "based_on",
    ("concept", "concept"): "related_to",
    ("concept", "entity"): "applies_to",
    ("skill", "entity"): "operates_on",
    ("skill", "algorithm"): "uses",
    ("episode", "entity"): "involves",
}


@dataclass
class DiscoveredLink:
    """A discovered relationship between two pages."""

    source_page: str
    target_page: str
    relation: str
    method: str  # "wikilink" | "pattern" | "type_inference"
    confidence: float = 1.0
    pending_review: bool = False
    context: str = ""


def _extract_wikilink_targets(body: str) -> list[tuple[str, str]]:
    """Extract [[Page Title]] targets and surrounding context.

    Returns list of (target_title, surrounding_sentence).
    """
    results: list[tuple[str, str]] = []
    sentences = re.split(r"(?<=[.!?\n])\s+", body)
    for sent in sentences:
        for match in _WIKILINK_RE.finditer(sent):
            target = match.group(1).split("|")[0].strip()
            results.append((target, sent.strip()))
    return results


def _extract_markdown_link_text(body: str) -> list[str]:
    """Extract link text from [text](url) markdown links."""
    return [m.group(1).strip() for m in _MARKDOWN_LINK_RE.finditer(body)]


def _build_page_index(wiki_root: str) -> dict[str, Path]:
    """Build a cached index of all wiki pages by slug and title_slug."""
    if wiki_root in _page_index_cache:
        return _page_index_cache[wiki_root]

    root = Path(wiki_root)
    index: dict[str, Path] = {}

    for md_file in root.rglob("*.md"):
        if md_file.name in ("index.md", "log.md", "Admin_Dashboard.md"):
            continue
        # Index by filename slug
        index[md_file.stem] = md_file
        # Index by title slug
        try:
            meta, _ = engine.parse_frontmatter(md_file.read_text(encoding="utf-8"))
            if meta.get("title"):
                title_slug = engine.generate_page_id(meta["title"])
                index[title_slug] = md_file
        except Exception:
            continue

    _page_index_cache[wiki_root] = index
    return index


def _find_page_by_title_or_slug(wiki_root: str, title: str) -> Path | None:
    """Find a page file by its title or slug using cached index."""
    index = _build_page_index(wiki_root)
    slug = engine.generate_page_id(title)
    return index.get(slug)


def _get_page_type(page_path: Path) -> str:
    """Read page frontmatter and return its type."""
    try:
        meta, _ = engine.parse_frontmatter(page_path.read_text(encoding="utf-8"))
        return meta.get("type", "unknown")
    except Exception:
        return "unknown"


def _get_page_title(page_path: Path) -> str:
    """Read page frontmatter and return its title."""
    try:
        meta, _ = engine.parse_frontmatter(page_path.read_text(encoding="utf-8"))
        return meta.get("title", page_path.stem)
    except Exception:
        return page_path.stem


def _match_sentence_patterns(body: str, source_title: str) -> list[DiscoveredLink]:
    """Match predefined sentence patterns to discover relationships."""
    discovered: list[DiscoveredLink] = []
    sentences = re.split(r"(?<=[.!?\n])\s+", body)

    for sent in sentences:
        for pattern, rel_type in _RELATION_PATTERNS:
            for match in pattern.finditer(sent):
                entity_a = match.group(1).strip()
                entity_b = match.group(2).strip()
                # Check if entity_b looks like a page title (capitalized or known)
                if len(entity_b) >= 2 and entity_b[0].isupper():
                    discovered.append(
                        DiscoveredLink(
                            source_page=source_title,
                            target_page=entity_b,
                            relation=rel_type,
                            method="pattern",
                            context=sent.strip()[:200],
                        )
                    )
    return discovered


def _infer_relation_by_type(source_type: str, target_type: str) -> str | None:
    """Infer a default relation based on source and target page types."""
    return _TYPE_RELATION_MAP.get((source_type, target_type))


def _resolve_target_page(wiki_root: str, target_name: str, source_path: Path) -> Path | None:
    """Find the actual page file for a target name, excluding the source page itself."""
    target_path = _find_page_by_title_or_slug(wiki_root, target_name)
    if target_path and target_path.resolve() == source_path.resolve():
        return None
    return target_path


def process_page(page_path: str, wiki_root: str) -> list[DiscoveredLink]:
    """Process a single page and discover all possible relationships.

    Returns a list of DiscoveredLink objects. Logs actions to wiki/log.md.
    """
    path = Path(page_path)
    if not path.exists():
        logger.warning("Page does not exist: %s", page_path)
        return []

    try:
        content = path.read_text(encoding="utf-8")
        meta, body = engine.parse_frontmatter(content)
    except Exception as exc:
        logger.warning("Failed to parse page %s: %s", page_path, exc)
        return []

    source_title = meta.get("title", path.stem)
    source_type = meta.get("type", "unknown")
    discovered: list[DiscoveredLink] = []
    seen_targets: set[str] = set()

    # 1. Wikilink extraction → create typed relations
    for target_title, context in _extract_wikilink_targets(body):
        if target_title in seen_targets:
            continue
        target_path = _resolve_target_page(wiki_root, target_title, path)
        if not target_path:
            continue

        target_type = _get_page_type(target_path)
        # Try type inference for the relation type
        inferred_rel = _infer_relation_by_type(source_type, target_type)
        if inferred_rel:
            discovered.append(
                DiscoveredLink(
                    source_page=source_title,
                    target_page=target_title,
                    relation=inferred_rel,
                    method="wikilink+type_inference",
                    confidence=0.9,
                    context=context[:200],
                )
            )
        else:
            # Fallback: generic related_to with pending review
            discovered.append(
                DiscoveredLink(
                    source_page=source_title,
                    target_page=target_title,
                    relation="related_to",
                    method="wikilink",
                    confidence=0.6,
                    pending_review=True,
                    context=context[:200],
                )
            )
        seen_targets.add(target_title)

    # 2. Sentence pattern matching
    pattern_links = _match_sentence_patterns(body, source_title)
    for pl in pattern_links:
        if pl.target_page in seen_targets:
            continue
        target_path = _resolve_target_page(wiki_root, pl.target_page, path)
        if target_path:
            discovered.append(pl)
            seen_targets.add(pl.target_page)

    # 3. Log discovered links
    if discovered:
        log_entries: list[str] = []
        for link in discovered:
            status = "pending_review" if link.pending_review else "auto_linked"
            log_entries.append(
                f"entity_linker | {status} | {link.source_page} --{link.relation}--> "
                f"{link.target_page} (method={link.method})"
            )
        # Append a single consolidated log entry
        engine.append_log(wiki_root, "entity_linker | " + f"{len(discovered)} link(s) discovered for [[{source_title}]]")

    return discovered


def write_links_to_page(page_path: str, links: list[DiscoveredLink]) -> None:
    """Append discovered links to the page's ### 自动链接关系 section.

    Skips if section already exists to avoid duplicates on re-processing.
    """
    if not links:
        return

    path = Path(page_path)
    try:
        content = path.read_text(encoding="utf-8")
        meta, body = engine.parse_frontmatter(content)
    except Exception:
        return

    section_header = "### 自动链接关系"
    if section_header in body:
        # Already has auto-link section; don't duplicate
        return

    lines = [f"\n{section_header}\n"]
    lines.append("_These relationships were discovered automatically by the heuristic entity linker._\n")

    pending: list[DiscoveredLink] = []
    confirmed: list[DiscoveredLink] = []
    for link in links:
        if link.pending_review:
            pending.append(link)
        else:
            confirmed.append(link)

    if confirmed:
        lines.append("**Confirmed links:**\n")
        for link in confirmed:
            lines.append(f"- `{link.source_page}` --[[{link.relation}]]--> `{link.target_page}`\n")

    if pending:
        lines.append("**Pending review:**\n")
        for link in pending:
            lines.append(
                f"- `{link.source_page}` --[[{link.relation}]]--> `{link.target_page}` "
                f"_({link.method})_\n"
            )

    new_body = body.rstrip() + "\n" + "".join(lines)
    new_content = engine.write_frontmatter(meta, new_body)
    path.write_text(new_content, encoding="utf-8")
    logger.info("Wrote %d links to page %s", len(links), page_path)


def process(wiki_root: str, page_path: str, write_back: bool = True) -> list[DiscoveredLink]:
    """Main entry point: process a page and optionally write links back.

    This is the hook called by wiki_engine.create_page() and update_page().

    Args:
        wiki_root: Root directory of the wiki.
        page_path: Path to the page just created/updated.
        write_back: If True, append links to the page body.

    Returns:
        List of discovered links.
    """
    links = process_page(page_path, wiki_root)
    if write_back:
        write_links_to_page(page_path, links)

    # Phase 8: emit entity link complete event
    try:
        import event_bus
        event_bus.emit(
            "entity_link_complete",
            {
                "page": str(Path(page_path).relative_to(Path(wiki_root))),
                "new_links": len(links),
                "timestamp": datetime.now().isoformat(),
            },
        )
    except Exception:
        pass

    return links


def repair_orphans_with_llm(
    wiki_root: str,
    llm_func: Any | None = None,
    max_pages: int = 20,
) -> dict[str, Any]:
    """Batch-repair orphan pages using LLM-assisted link placement.

    1. Find all orphan pages (no inbound wikilinks).
    2. For each orphan, search Whoosh for top 5 relevant candidates.
    3. Ask LLM to decide which candidates should link to the orphan.
    4. Inject [[OrphanTitle]] links into approved candidate pages.
    5. Log actions to wiki/log.md.

    Args:
        wiki_root: Root directory of the wiki.
        llm_func: Function accepting (prompt, system, temperature) -> str.
                  If None, uses a simple heuristic fallback.
        max_pages: Maximum orphan pages to process per call.

    Returns:
        Dict with processed count, links added, and skipped count.
    """
    root = Path(wiki_root)
    orphans = engine.find_orphan_pages(wiki_root)
    if not orphans:
        return {"status": "no_orphans", "processed": 0, "links_added": 0}

    # Limit to max_pages
    orphans_to_process = orphans[:max_pages]
    links_added = 0
    processed = 0

    for orphan_path_str in orphans_to_process:
        orphan_path = Path(orphan_path_str)
        try:
            orphan_meta, orphan_body = engine.parse_frontmatter(
                orphan_path.read_text(encoding="utf-8")
            )
        except Exception:
            continue

        orphan_title = orphan_meta.get("title", orphan_path.stem)
        orphan_type = orphan_meta.get("type", "unknown")
        orphan_slug = engine.generate_page_id(orphan_title)

        # Skip if already has inbound links (race condition with background jobs)
        if orphan_path_str not in engine.find_orphan_pages(wiki_root):
            continue

        # Search for relevant candidate pages
        try:
            from search_backend import search_index

            query = f"{orphan_title} {orphan_type}"
            candidates = search_index(wiki_root, query, limit=10)
        except Exception:
            candidates = []

        if not candidates:
            continue

        # Filter out the orphan itself and pages that already link to it
        filtered_candidates: list[dict[str, Any]] = []
        for c in candidates:
            cand_path = root / c.get("file_path", "")
            if not cand_path.exists():
                continue
            if cand_path.resolve() == orphan_path.resolve():
                continue
            # Check if already links to orphan
            try:
                cand_content = cand_path.read_text(encoding="utf-8")
                if f"[[{orphan_title}]]" in cand_content:
                    continue
                if f"[[{orphan_slug}]]" in cand_content:
                    continue
            except Exception:
                continue
            filtered_candidates.append(c)
            if len(filtered_candidates) >= 5:
                break

        if not filtered_candidates:
            continue

        # Use LLM to decide which candidates should link to the orphan
        chosen_candidates: list[dict[str, Any]] = []
        if llm_func is not None:
            candidate_descriptions = []
            for i, c in enumerate(filtered_candidates, 1):
                candidate_descriptions.append(
                    f"{i}. Title: {c.get('title', 'Unknown')}\n   Snippet: {c.get('snippet', '')[:150]}"
                )
            candidates_text = "\n".join(candidate_descriptions)

            prompt = (
                f"You are a knowledge graph curator. An orphan page needs inbound links.\n\n"
                f"ORPHAN PAGE:\n"
                f"Title: {orphan_title}\n"
                f"Type: {orphan_type}\n"
                f"Content excerpt: {orphan_body[:300]}\n\n"
                f"CANDIDATE PAGES (found via search):\n"
                f"{candidates_text}\n\n"
                f"TASK: Select which candidate pages should link to '{orphan_title}'.\n"
                f"Return ONLY a JSON list of indices (e.g., [1, 3]) representing the candidates\n"
                f"that are semantically related enough to warrant a link. Return [] if none are suitable.\n"
                f"Do NOT include the orphan page itself."
            )
            try:
                import json as _json

                response = llm_func(prompt, temperature=0.2)
                response = response.strip()
                if response.startswith("```"):
                    response = response.split("```json")[-1].split("```")[0].strip()
                selected = _json.loads(response)
                if isinstance(selected, list):
                    for idx in selected:
                        if isinstance(idx, int) and 1 <= idx <= len(filtered_candidates):
                            chosen_candidates.append(filtered_candidates[idx - 1])
            except Exception:
                # LLM failed; fall back to heuristic
                chosen_candidates = filtered_candidates[:3]
        else:
            # Heuristic fallback: take top 3
            chosen_candidates = filtered_candidates[:3]

        # Add links to chosen candidate pages
        for cand in chosen_candidates:
            cand_path = root / cand.get("file_path", "")
            if not cand_path.exists():
                continue
            try:
                cand_content = cand_path.read_text(encoding="utf-8")
                cand_meta, cand_body = engine.parse_frontmatter(cand_content)
            except Exception:
                continue

            # Inject wikilink in a "Related" or "See Also" section if present,
            # otherwise append to end
            link_line = f"- [[{orphan_title}]]"
            new_body = cand_body

            # Try to append to See Also section
            if "## See Also" in cand_body:
                parts = cand_body.split("## See Also", 1)
                new_body = parts[0] + "## See Also\n\n" + link_line + "\n" + parts[1].split("\n", 1)[1] if "\n" in parts[1] else parts[0] + "## See Also\n\n" + link_line + "\n"
            elif "## Relationships" in cand_body:
                parts = cand_body.split("## Relationships", 1)
                new_body = parts[0] + "## Relationships\n\n" + link_line + "\n" + parts[1].split("\n", 1)[1] if "\n" in parts[1] else parts[0] + "## Relationships\n\n" + link_line + "\n"
            else:
                # Append at end before auto-link section if present
                if "### 自动链接关系" in cand_body:
                    parts = cand_body.split("### 自动链接关系", 1)
                    new_body = parts[0].rstrip() + "\n\n## See Also\n\n" + link_line + "\n\n### 自动链接关系" + parts[1]
                else:
                    new_body = cand_body.rstrip() + "\n\n## See Also\n\n" + link_line + "\n"

            if new_body != cand_body:
                new_content = engine.write_frontmatter(cand_meta, new_body)
                cand_path.write_text(new_content, encoding="utf-8")
                links_added += 1

        processed += 1
        engine.append_log(
            wiki_root,
            f"orphan_repair | [[{orphan_title}]] | linked from {len(chosen_candidates)} page(s)"
        )

    # Emit event
    try:
        import event_bus

        event_bus.emit(
            "orphan_repair_complete",
            {
                "processed": processed,
                "links_added": links_added,
                "timestamp": datetime.now().isoformat(),
            },
        )
    except Exception:
        pass

    return {
        "status": "done",
        "orphans_found": len(orphans),
        "processed": processed,
        "links_added": links_added,
        "max_pages": max_pages,
    }
