#!/usr/bin/env python3
"""Incremental SeekDB reindex for pages that exist on disk but not in the collection.

Designed to recover from batch_sync OOM crashes: instead of full rebuild_index(),
processes only the missing page_ids in small batches with explicit gc + sleep
to keep peak memory under 2 GB.

Usage:
    python scripts/reindex_missing_seekdb.py --dry-run   # show diff only
    python scripts/reindex_missing_seekdb.py             # run reindex
    python scripts/reindex_missing_seekdb.py --batch 50  # custom batch size
"""

from __future__ import annotations

import argparse
import gc
import json
import logging
import os
import resource
import sys
import time
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
log = logging.getLogger("reindex_missing")

PROJECT_ROOT = Path(__file__).parent.parent.resolve()
WIKI_ROOT = PROJECT_ROOT / "wiki"
PROGRESS_PATH = PROJECT_ROOT / "data" / "seekdb_reindex_progress.json"

# Ensure project modules importable
for sub in ["search", "core", "utils", "knowledge", "ingest", "robot", "api", "dream"]:
    p = str(PROJECT_ROOT / sub)
    if p not in sys.path:
        sys.path.insert(0, p)

# Set SeekDB env if not already configured
os.environ.setdefault("SEEKDB_MODE", "server")
os.environ.setdefault("SEEKDB_HOST", "127.0.0.1")
os.environ.setdefault("SEEKDB_PORT", "2881")
os.environ.setdefault("SEEKDB_DATABASE", "rosclaw_wiki")
os.environ.setdefault("SEEKDB_USER", "root")
os.environ.setdefault("WIKI_BACKEND", "seekdb")


def mem_rss_mb() -> float:
    """Current process RSS in MB."""
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024


def collect_disk_pages() -> dict[str, Path]:
    """Map page_id (file stem) → absolute Path for all wiki .md files."""
    pages: dict[str, Path] = {}
    skip_names = {"index.md", "log.md", "Admin_Dashboard.md"}
    for md in WIKI_ROOT.rglob("*.md"):
        if md.name in skip_names:
            continue
        pages[md.stem] = md
    return pages


def collect_seekdb_ids() -> set[str]:
    """Fetch every page_id currently in the SeekDB wiki_pages collection."""
    from seekdb_collection_client import get_wiki_collection
    coll = get_wiki_collection()
    total = coll.count()
    log.info("SeekDB reports %d pages", total)

    ids: set[str] = set()
    offset = 0
    page_size = 1000
    while offset < total:
        # pyseekdb get() with offset+limit pattern; fall back to fetching all if unsupported
        try:
            res = coll.get(limit=page_size, offset=offset, include=[])
        except TypeError:
            # Older API: no offset; fetch all once
            res = coll.get(limit=total + 100, include=[])
            offset_ids = res.get("ids", [])
            if offset_ids and isinstance(offset_ids[0], list):
                offset_ids = offset_ids[0]
            ids.update(offset_ids)
            break
        batch_ids = res.get("ids", [])
        if batch_ids and isinstance(batch_ids[0], list):
            batch_ids = batch_ids[0]
        if not batch_ids:
            break
        ids.update(batch_ids)
        offset += len(batch_ids)
    return ids


def load_progress() -> set[str]:
    if not PROGRESS_PATH.exists():
        return set()
    try:
        return set(json.loads(PROGRESS_PATH.read_text(encoding="utf-8")).get("done", []))
    except Exception:
        return set()


def save_progress(done: set[str]) -> None:
    PROGRESS_PATH.parent.mkdir(parents=True, exist_ok=True)
    PROGRESS_PATH.write_text(
        json.dumps({"done": sorted(done), "updated_at": time.time()}, ensure_ascii=False),
        encoding="utf-8",
    )


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true", help="Only print diff, do not index")
    ap.add_argument("--batch", type=int, default=30, help="Batch size (default 30)")
    ap.add_argument("--sleep", type=float, default=1.0, help="Seconds between batches")
    ap.add_argument("--limit", type=int, default=0, help="Max pages to index (0 = unlimited)")
    args = ap.parse_args()

    log.info("Initial RSS: %.0f MB", mem_rss_mb())

    log.info("Scanning %s for .md files…", WIKI_ROOT)
    disk = collect_disk_pages()
    log.info("Disk pages: %d", len(disk))

    log.info("Querying SeekDB for existing page_ids…")
    in_db = collect_seekdb_ids()
    log.info("SeekDB pages: %d", len(in_db))

    missing_ids = sorted(set(disk) - in_db)
    log.info("Missing in SeekDB: %d", len(missing_ids))

    if args.dry_run:
        log.info("Sample missing (first 20): %s", missing_ids[:20])
        return 0

    if not missing_ids:
        log.info("Nothing to do — SeekDB is in sync with disk.")
        return 0

    # Resume from prior progress
    done = load_progress()
    if done:
        before = len(missing_ids)
        missing_ids = [mid for mid in missing_ids if mid not in done]
        log.info("Resuming: %d already done, %d remaining (was %d)", len(done), len(missing_ids), before)

    if args.limit:
        missing_ids = missing_ids[: args.limit]
        log.info("Limiting to first %d pages", len(missing_ids))

    # Load impl once (model loads once)
    from seekdb_search_impl import SeekDBSearchImpl
    impl = SeekDBSearchImpl(str(WIKI_ROOT))
    _ = impl._get_model()  # eager-load to know peak baseline
    log.info("After model load RSS: %.0f MB", mem_rss_mb())

    total = len(missing_ids)
    success = 0
    errors = 0
    start = time.time()

    for i in range(0, total, args.batch):
        batch = missing_ids[i : i + args.batch]
        batch_start = time.time()
        for pid in batch:
            md_path = disk.get(pid)
            if md_path is None:
                continue
            try:
                ok = impl.index_page(str(md_path))
                if ok:
                    success += 1
                    done.add(pid)
                else:
                    errors += 1
            except Exception as exc:
                log.warning("index_page(%s) failed: %s", pid, exc)
                errors += 1

        gc.collect()
        save_progress(done)
        elapsed = time.time() - start
        batch_elapsed = time.time() - batch_start
        processed = min(i + args.batch, total)
        rate = processed / max(elapsed, 0.1)
        eta = (total - processed) / max(rate, 0.001)
        log.info(
            "Batch %d/%d done | success=%d errors=%d | batch=%.1fs | RSS=%.0f MB | ETA=%.0fs",
            processed,
            total,
            success,
            errors,
            batch_elapsed,
            mem_rss_mb(),
            eta,
        )

        if i + args.batch < total:
            time.sleep(args.sleep)

    elapsed = time.time() - start
    log.info(
        "DONE in %.0fs | success=%d errors=%d | peak RSS=%.0f MB",
        elapsed,
        success,
        errors,
        mem_rss_mb(),
    )
    return 0 if errors == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
