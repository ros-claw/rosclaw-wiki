"""ROSClaw Retention Engine — knowledge memory metabolism.

Implements confidence decay and archival suggestion following v2 lifecycle rules.
"""

from __future__ import annotations

import logging
from datetime import datetime
from pathlib import Path
from typing import Any

import wiki_engine as engine

logger = logging.getLogger("rosclaw.retention")

# Files excluded from decay / archival scans
_EXCLUDED_FILES = {"index.md", "log.md", "Admin_Dashboard.md"}


def _days_since(date_str: str) -> int:
    """Return days between date_str and today."""
    today = datetime.now().date()
    try:
        # Handle both date-only and isoformat with time
        d = datetime.fromisoformat(date_str).date()
    except Exception:
        return 0
    return (today - d).days


def _compute_decayed_confidence(current: float, days: int) -> float:
    """Apply Ebbinghaus-style decay based on days since last reinforcement.

    Rules:
        30-89 days  → ×0.9
        90-179 days → ×0.7
        ≥180 days   → ×0.5
        <30 days    → unchanged
    """
    if days >= 180:
        return current * 0.5
    if days >= 90:
        return current * 0.7
    if days >= 30:
        return current * 0.9
    return current


def decay_confidence(wiki_root: str) -> dict[str, Any]:
    """Apply confidence decay to all wiki pages based on time since last_reinforced.

    Scans all .md files under wiki_root (excluding index, log, dashboard).
    Updates confidence and adds/updates `last_decayed` timestamp.
    Does NOT modify `last_reinforced`.

    Returns:
        Summary dict with total_scanned, pages_decayed, pages_unchanged,
        and a details list of affected pages.
    """
    root = Path(wiki_root)
    total_scanned = 0
    pages_decayed = 0
    pages_unchanged = 0
    details: list[dict[str, Any]] = []

    for md_file in root.rglob("*.md"):
        if md_file.name in _EXCLUDED_FILES:
            continue

        try:
            content = md_file.read_text(encoding="utf-8")
            meta, body = engine.parse_frontmatter(content)
        except Exception as exc:
            logger.warning("Failed to read %s: %s", md_file, exc)
            continue

        total_scanned += 1
        last_reinforced = meta.get("last_reinforced", "")
        if not last_reinforced:
            pages_unchanged += 1
            continue

        days = _days_since(str(last_reinforced))
        old_conf = float(meta.get("confidence", 0.5))
        new_conf = _compute_decayed_confidence(old_conf, days)
        new_conf = round(new_conf, 2)

        if new_conf != old_conf:
            meta = dict(meta)
            meta["confidence"] = new_conf
            meta["last_decayed"] = datetime.now().isoformat(timespec="seconds")
            new_content = engine.write_frontmatter(meta, body)
            md_file.write_text(new_content, encoding="utf-8")
            pages_decayed += 1
            details.append({
                "path": str(md_file.relative_to(root)),
                "title": meta.get("title", md_file.stem),
                "old_confidence": old_conf,
                "new_confidence": new_conf,
                "days_since_reinforced": days,
            })
            logger.info(
                "Decayed %s: %.2f → %.2f (%d days)",
                md_file.name, old_conf, new_conf, days
            )
        else:
            pages_unchanged += 1

    summary = {
        "total_scanned": total_scanned,
        "pages_decayed": pages_decayed,
        "pages_unchanged": pages_unchanged,
        "details": details,
    }

    # Log the operation
    detail_str = ", ".join(
        f"{d['path']}: {d['old_confidence']}>{d['new_confidence']}"
        for d in details[:10]  # cap log length
    )
    if len(details) > 10:
        detail_str += f" ... ({len(details) - 10} more)"
    engine.append_log(
        str(wiki_root),
        f"retention | decay_round | pages_affected: {pages_decayed} | details: {detail_str}",
    )

    return summary


def suggest_archival(wiki_root: str, threshold: float = 0.15) -> list[dict[str, Any]]:
    """Suggest pages for archival based on low confidence.

    Scans all .md files and returns pages where confidence < threshold.
    Does NOT move any files.

    Returns:
        List of dicts with file_path, title, confidence, last_reinforced.
    """
    root = Path(wiki_root)
    candidates: list[dict[str, Any]] = []

    for md_file in root.rglob("*.md"):
        if md_file.name in _EXCLUDED_FILES:
            continue

        try:
            content = md_file.read_text(encoding="utf-8")
            meta, _ = engine.parse_frontmatter(content)
        except Exception as exc:
            logger.warning("Failed to read %s: %s", md_file, exc)
            continue

        confidence = float(meta.get("confidence", 1.0))
        if confidence < threshold:
            candidates.append({
                "file_path": str(md_file.relative_to(root)),
                "title": meta.get("title", md_file.stem),
                "confidence": confidence,
                "last_reinforced": meta.get("last_reinforced", "unknown"),
            })

    candidates.sort(key=lambda x: x["confidence"])

    # Log the operation
    page_list = ", ".join(f"{c['title']}({c['confidence']:.2f})" for c in candidates[:10])
    if len(candidates) > 10:
        page_list += f" ... ({len(candidates) - 10} more)"
    engine.append_log(
        str(wiki_root),
        f"retention | archival_suggestions | threshold: {threshold} | candidates: {page_list}",
    )

    return candidates
