"""ROSClaw Scheduler — tiered automatic metabolism.

Runs background tasks on three schedules even when data/raw/ is empty:
- High frequency (1-8h): raw_watcher
- Daily: daily_review
- Weekly: weekly_deep_scan
"""

from __future__ import annotations

import logging
import time
from datetime import datetime
from pathlib import Path
from typing import Any

import event_bus
import wiki_engine as engine
from batch_ingest import _collect_raw_files, _load_processed_files
from retention_engine import decay_confidence, suggest_archival

logger = logging.getLogger("rosclaw.scheduler")

# Default schedule intervals (seconds)
DEFAULT_RAW_WATCHER_INTERVAL = 3600  # 1 hour
DEFAULT_DAILY_HOUR = 2  # 2 AM
DEFAULT_WEEKLY_DAY = 0  # Monday


def raw_watcher(wiki_root: str, raw_root: str) -> dict[str, Any]:
    """Scan data/raw/ for new files and emit alert if found.

    Does NOT auto-trigger batch_ingest (requires LLM); logs discovery
    so an operator or agent can decide to run ingest.
    """
    raw_path = Path(raw_root)
    wiki_path = Path(wiki_root)

    if not raw_path.exists():
        return {"status": "no_raw_dir", "new_files": 0}

    files = _collect_raw_files(raw_path)
    processed = _load_processed_files()
    new_files = [(rel, kind) for rel, kind in files if rel not in processed]

    if not new_files:
        logger.info("raw_watcher: no new files")
        return {"status": "no_new_files", "new_files": 0}

    logger.info("raw_watcher: found %d new files", len(new_files))
    file_list = [rel for rel, _ in new_files]
    display_files = ", ".join(file_list[:5])
    if len(file_list) > 5:
        display_files += " ..."

    engine.append_log(
        str(wiki_path),
        f"scheduler | raw_watcher | new_files: {len(new_files)} | files: {display_files}",
    )

    event_bus.emit(
        "raw_watcher_alert",
        {
            "new_files_count": len(new_files),
            "files": file_list,
            "timestamp": datetime.now().isoformat(),
        },
    )

    return {"status": "new_files_found", "new_files": len(new_files), "files": file_list}


def daily_review(wiki_root: str) -> dict[str, Any]:
    """Run daily maintenance: retention decay, lint, low-confidence suggestions."""
    wiki_path = Path(wiki_root)

    results: dict[str, Any] = {}

    # 1. Retention decay
    logger.info("daily_review: running retention decay")
    decay_result = decay_confidence(str(wiki_path))
    results["decay"] = decay_result

    # 2. Auto-lint: orphans and low-confidence pages
    logger.info("daily_review: running auto-lint")
    pages = engine.list_pages(str(wiki_path))
    orphans = engine.find_orphan_pages(str(wiki_path))

    low_confidence = [
        {
            "path": p.get("_path"),
            "title": p.get("title", "unknown"),
            "confidence": float(p.get("confidence", 1.0)),
        }
        for p in pages
        if float(p.get("confidence", 1.0)) < 0.4
    ]

    results["lint"] = {
        "orphan_count": len(orphans),
        "orphans": orphans[:20],
        "low_confidence_count": len(low_confidence),
        "low_confidence": low_confidence,
    }

    # 3. Archival suggestions
    archival_candidates = suggest_archival(str(wiki_path), threshold=0.15)
    results["archival_candidates"] = archival_candidates

    engine.append_log(
        str(wiki_path),
        (
            f"scheduler | daily_review | decayed: {decay_result['pages_decayed']} | "
            f"orphans: {len(orphans)} | low_conf: {len(low_confidence)} | "
            f"archival: {len(archival_candidates)}"
        ),
    )

    if decay_result["pages_decayed"] or orphans or low_confidence or archival_candidates:
        event_bus.emit(
            "daily_review_complete",
            {
                "decayed_pages": decay_result["pages_decayed"],
                "orphan_count": len(orphans),
                "low_confidence_count": len(low_confidence),
                "archival_candidates": len(archival_candidates),
                "timestamp": datetime.now().isoformat(),
            },
        )

    return results


def weekly_deep_scan(wiki_root: str) -> dict[str, Any]:
    """Run weekly deep scan: dedup, fragmentation, weekly report."""
    wiki_path = Path(wiki_root)

    results: dict[str, Any] = {}

    # 1. Entity deduplication report
    logger.info("weekly_deep_scan: running dedup report")
    from entity_resolver import entity_dedup_report, write_dedup_report

    duplicates = entity_dedup_report(str(wiki_path), similarity_threshold=0.7)
    results["duplicates"] = duplicates

    if duplicates:
        report_path = write_dedup_report(str(wiki_path))
        results["dedup_report_path"] = str(report_path)
        event_bus.emit(
            "dedup_alert",
            {
                "duplicate_count": len(duplicates),
                "top_pairs": [
                    {"a": d["title_a"], "b": d["title_b"], "sim": d["similarity"]}
                    for d in duplicates[:5]
                ],
                "timestamp": datetime.now().isoformat(),
            },
        )

    # 2. Content-level dedup
    logger.info("weekly_deep_scan: running fragment/content dedup")
    from fragment_detector import dedup_information

    content_dupes = dedup_information(str(wiki_path), similarity_threshold=0.85)
    results["content_duplicates"] = content_dupes

    # 3. Weekly research advisor report
    logger.info("weekly_deep_scan: generating weekly report")
    from research_advisor import generate_weekly_report

    report_path = generate_weekly_report(str(wiki_path))
    results["weekly_report_path"] = str(report_path)

    engine.append_log(
        str(wiki_path),
        (
            f"scheduler | weekly_deep_scan | duplicates: {len(duplicates)} | "
            f"content_dupes: {len(content_dupes)} | report: {report_path.name}"
        ),
    )

    event_bus.emit(
        "weekly_scan_complete",
        {
            "duplicate_count": len(duplicates),
            "content_duplicate_count": len(content_dupes),
            "report_path": str(report_path),
            "timestamp": datetime.now().isoformat(),
        },
    )

    return results


def run_scheduler(
    wiki_root: str,
    raw_root: str,
    raw_interval: int = DEFAULT_RAW_WATCHER_INTERVAL,
    daily_hour: int = DEFAULT_DAILY_HOUR,
    weekly_day: int = DEFAULT_WEEKLY_DAY,
) -> None:
    """Run the metabolism scheduler loop indefinitely.

    Args:
        wiki_root: Path to the wiki directory.
        raw_root: Path to the raw data directory.
        raw_interval: Seconds between raw_watcher checks.
        daily_hour: Hour of day (0-23) to run daily_review.
        weekly_day: Day of week (0=Monday) to run weekly_deep_scan.
    """
    try:
        import schedule
    except ImportError as exc:
        raise ImportError(
            "The 'schedule' library is required for the scheduler. "
            "Install it with: pip install schedule"
        ) from exc

    # Register jobs
    schedule.every(raw_interval).seconds.do(raw_watcher, wiki_root, raw_root)
    schedule.every().day.at(f"{daily_hour:02d}:00").do(daily_review, wiki_root)
    # schedule library uses monday-sunday strings
    day_names = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
    weekly_job = getattr(schedule.every(), day_names[weekly_day])
    weekly_job.at("09:00").do(weekly_deep_scan, wiki_root)

    logger.info(
        "Scheduler started. wiki=%s raw=%s raw_interval=%ds daily_at=%02d:00 weekly_on=%s",
        wiki_root,
        raw_root,
        raw_interval,
        daily_hour,
        day_names[weekly_day],
    )

    while True:
        schedule.run_pending()
        time.sleep(60)


def run_once(wiki_root: str, raw_root: str, task: str) -> dict[str, Any]:
    """Run a single scheduler task immediately (for CLI or testing).

    Args:
        wiki_root: Path to wiki directory.
        raw_root: Path to raw data directory.
        task: One of "raw_watcher", "daily_review", "weekly_deep_scan".

    Returns:
        Task result dict.
    """
    if task == "raw_watcher":
        return raw_watcher(wiki_root, raw_root)
    if task == "daily_review":
        return daily_review(wiki_root)
    if task == "weekly_deep_scan":
        return weekly_deep_scan(wiki_root)
    raise ValueError(f"Unknown task: {task}. Choose from: raw_watcher, daily_review, weekly_deep_scan")


__all__ = [
    "raw_watcher",
    "daily_review",
    "weekly_deep_scan",
    "run_scheduler",
    "run_once",
    "DEFAULT_RAW_WATCHER_INTERVAL",
    "DEFAULT_DAILY_HOUR",
    "DEFAULT_WEEKLY_DAY",
]
