"""Dream Cycle — autonomous nightly thinking engine for Phase 10.

Three phases:
  1. Repair & Merge: fix stale citations, broken links, merge fragments
  2. Knowledge Reinforcement: search new sources for low-confidence pages
  3. Forward Insight: analyze knowledge gaps, generate research suggestions
"""

from __future__ import annotations

import logging
import re
import time
from datetime import datetime
from pathlib import Path
from typing import Any

import wiki_engine as engine

logger = logging.getLogger("rosclaw.dream")

# Simple TTL cache for expensive insight generation
_INSIGHTS_CACHE: dict[str, tuple[float, list[dict[str, Any]]]] = {}
_INSIGHTS_TTL_SEC = 300  # 5 minutes


# ── Phase 1: Repair & Merge ──


def _find_broken_wikilinks(wiki_root: str) -> list[dict[str, Any]]:
    """Find wikilinks that point to non-existent pages."""
    root = Path(wiki_root)
    broken: list[dict[str, Any]] = []
    wikilink_re = re.compile(r"\[\[([^\]]+)\]\]")

    all_pages: set[str] = set()
    for md_file in root.rglob("*.md"):
        rel = md_file.relative_to(root).with_suffix("").as_posix()
        all_pages.add(rel)
        all_pages.add(md_file.stem)
        try:
            meta, _ = engine.parse_frontmatter(md_file.read_text(encoding="utf-8"))
            if meta.get("title"):
                all_pages.add(engine.generate_page_id(meta["title"]))
        except Exception:
            pass

    for md_file in root.rglob("*.md"):
        content = md_file.read_text(encoding="utf-8")
        for match in wikilink_re.finditer(content):
            target = match.group(1).split("|")[0].strip()
            target_slug = engine.generate_page_id(target)
            if target not in all_pages and target_slug not in all_pages:
                broken.append({
                    "source_file": str(md_file.relative_to(root)),
                    "link_text": target,
                    "position": match.start(),
                })

    return broken


def _find_stale_citations(wiki_root: str, days: int = 180) -> list[dict[str, Any]]:
    """Find pages whose last_reinforced is older than `days`."""
    root = Path(wiki_root)
    stale: list[dict[str, Any]] = []
    cutoff = datetime.now() - __import__("datetime").timedelta(days=days)

    for md_file in root.rglob("*.md"):
        if md_file.name in ("index.md", "log.md"):
            continue
        try:
            meta, _ = engine.parse_frontmatter(md_file.read_text(encoding="utf-8"))
            last_str = meta.get("last_reinforced") or meta.get("created_at", "")
            if last_str:
                last = datetime.fromisoformat(last_str)
                if last < cutoff:
                    stale.append({
                        "file": str(md_file.relative_to(root)),
                        "title": meta.get("title", md_file.stem),
                        "last_reinforced": last_str,
                        "confidence": meta.get("confidence", 0.5),
                    })
        except Exception:
            continue

    return stale


def repair_broken_links(wiki_root: str) -> dict[str, Any]:
    """Auto-fix broken wikilinks where possible.

    Fixes applied:
      - If a similar page exists (case-insensitive match), rewrite the link.
      - Otherwise, mark with ⚠️ in place.
    """
    broken = _find_broken_wikilinks(wiki_root)
    fixed = 0
    unresolved = 0

    # Build slug → path mapping
    root = Path(wiki_root)
    slug_map: dict[str, str] = {}
    for md_file in root.rglob("*.md"):
        rel = md_file.relative_to(root).with_suffix("").as_posix()
        slug_map[md_file.stem.lower()] = rel
        slug_map[rel.lower()] = rel
        try:
            meta, _ = engine.parse_frontmatter(md_file.read_text(encoding="utf-8"))
            if meta.get("title"):
                slug_map[engine.generate_page_id(meta["title"]).lower()] = rel
        except Exception:
            pass

    for item in broken:
        src = root / item["source_file"]
        if not src.exists():
            continue
        content = src.read_text(encoding="utf-8")
        link_text = item["link_text"]
        slug = engine.generate_page_id(link_text).lower()

        if slug in slug_map:
            correct = slug_map[slug]
            content = content.replace(f"[[{link_text}]]", f"[[{correct}]]")
            src.write_text(content, encoding="utf-8")
            fixed += 1
            logger.info("Fixed link: %s -> %s in %s", link_text, correct, src)
        else:
            # Mark unresolved
            content = content.replace(
                f"[[{link_text}]]",
                f"[[{link_text}]] ⚠️",
            )
            src.write_text(content, encoding="utf-8")
            unresolved += 1

    return {"fixed": fixed, "unresolved": unresolved, "total_checked": len(broken)}


# ── Phase 2: Knowledge Reinforcement ──


def reinforce_low_confidence(wiki_root: str, threshold: float = 0.3) -> list[dict[str, Any]]:
    """Find pages with confidence below threshold and flag for reinforcement.

    Returns:
        List of pages needing attention.
    """
    root = Path(wiki_root)
    weak: list[dict[str, Any]] = []

    for md_file in root.rglob("*.md"):
        if md_file.name in ("index.md", "log.md"):
            continue
        try:
            meta, body = engine.parse_frontmatter(md_file.read_text(encoding="utf-8"))
            confidence = float(meta.get("confidence", 0.5))
            if confidence < threshold:
                weak.append({
                    "file": str(md_file.relative_to(root)),
                    "title": meta.get("title", md_file.stem),
                    "confidence": confidence,
                    "type": meta.get("type", "unknown"),
                })
        except Exception:
            continue

    logger.info("Reinforcement: %d pages below confidence %.2f", len(weak), threshold)
    return weak


# ── Phase 3: Forward Insight ──


def generate_insights(wiki_root: str) -> list[dict[str, Any]]:
    """Analyze knowledge graph and suggest research directions.

    Returns:
        List of insight dicts with type, description, suggested_action.
        Results are cached for 5 minutes to avoid expensive re-computation.
    """
    cache_key = str(wiki_root)
    now = time.time()
    if cache_key in _INSIGHTS_CACHE:
        cached_at, cached_data = _INSIGHTS_CACHE[cache_key]
        if now - cached_at < _INSIGHTS_TTL_SEC:
            return cached_data

    insights: list[dict[str, Any]] = []

    # Insight 1: High-orphan areas
    orphans = engine.find_orphan_pages(wiki_root)
    if len(orphans) > 3:
        insights.append({
            "type": "connectivity_gap",
            "description": f"{len(orphans)} orphan pages lack inbound links",
            "suggested_action": "Run entity linker or add cross-references",
            "severity": "medium",
        })

    # Insight 2: Low-confidence clusters
    weak = reinforce_low_confidence(wiki_root, threshold=0.3)
    if len(weak) > 5:
        insights.append({
            "type": "confidence_gap",
            "description": f"{len(weak)} pages have confidence < 0.3",
            "suggested_action": "Search for newer primary sources",
            "severity": "high",
        })

    # Insight 3: Type imbalance
    root = Path(wiki_root)
    type_counts: dict[str, int] = {}
    for md_file in root.rglob("*.md"):
        if md_file.name in ("index.md", "log.md"):
            continue
        try:
            meta, _ = engine.parse_frontmatter(md_file.read_text(encoding="utf-8"))
            ptype = meta.get("type", "unknown")
            type_counts[ptype] = type_counts.get(ptype, 0) + 1
        except Exception:
            continue

    if type_counts.get("skill", 0) < type_counts.get("concept", 0) // 5:
        insights.append({
            "type": "coverage_gap",
            "description": "Few skill pages relative to concepts",
            "suggested_action": "Extract actionable skills from concept pages",
            "severity": "low",
        })

    _INSIGHTS_CACHE[cache_key] = (now, insights)
    return insights


# ── Orchestrator ──


def run_dream_cycle(wiki_root: str) -> dict[str, Any]:
    """Run all three dream phases and return a report.

    Returns:
        Dict with phase results and summary.
    """
    logger.info("Dream cycle starting for %s", wiki_root)

    # Phase 1
    repair_result = repair_broken_links(wiki_root)

    # Phase 2
    weak_pages = reinforce_low_confidence(wiki_root)

    # Phase 3
    insights = generate_insights(wiki_root)

    report = {
        "timestamp": datetime.now().isoformat(),
        "phase1_repair": repair_result,
        "phase2_reinforce": {
            "weak_pages_count": len(weak_pages),
            "weak_pages": weak_pages[:10],  # cap detail
        },
        "phase3_insights": insights,
        "summary": (
            f"Fixed {repair_result['fixed']} links, "
            f"{repair_result['unresolved']} unresolved, "
            f"{len(weak_pages)} weak pages, "
            f"{len(insights)} insights"
        ),
    }

    logger.info("Dream cycle complete: %s", report["summary"])
    return report


__all__ = [
    "repair_broken_links",
    "reinforce_low_confidence",
    "generate_insights",
    "run_dream_cycle",
]
