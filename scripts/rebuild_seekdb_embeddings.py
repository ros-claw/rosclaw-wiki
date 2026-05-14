#!/usr/bin/env python3
"""Rebuild all SeekDB embeddings with the new multilingual model.

Swaps from all-MiniLM-L6-v2 (English-only) to
paraphrase-multilingual-MiniLM-L12-v2 (Chinese + 50+ languages).

Usage:
    python scripts/rebuild_seekdb_embeddings.py --dry-run
    python scripts/rebuild_seekdb_embeddings.py
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
log = logging.getLogger("rebuild_embeddings")

PROJECT_ROOT = Path(__file__).parent.parent.resolve()
WIKI_ROOT = PROJECT_ROOT / "wiki"
PROGRESS_PATH = PROJECT_ROOT / "data" / "seekdb_rebuild_progress.json"

for sub in ["search", "core", "utils", "knowledge", "ingest", "robot", "api", "dream"]:
    p = str(PROJECT_ROOT / sub)
    if p not in sys.path:
        sys.path.insert(0, p)

os.environ.setdefault("SEEKDB_MODE", "server")
os.environ.setdefault("SEEKDB_HOST", "127.0.0.1")
os.environ.setdefault("SEEKDB_PORT", "2881")
os.environ.setdefault("SEEKDB_DATABASE", "rosclaw_wiki")
os.environ.setdefault("WIKI_BACKEND", "seekdb")


def mem_rss_mb() -> float:
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024


def collect_disk_pages() -> dict[str, Path]:
    pages: dict[str, Path] = {}
    skip_names = {"index.md", "log.md", "Admin_Dashboard.md"}
    for md in WIKI_ROOT.rglob("*.md"):
        if md.name in skip_names:
            continue
        pages[md.stem] = md
    return pages


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
    ap.add_argument("--dry-run", action="store_true", help="Only print diff, do not re-encode")
    ap.add_argument("--batch", type=int, default=30, help="Batch size (default 30)")
    ap.add_argument("--sleep", type=float, default=1.0, help="Seconds between batches")
    args = ap.parse_args()

    log.info("Initial RSS: %.0f MB", mem_rss_mb())

    disk = collect_disk_pages()
    log.info("Disk pages: %d", len(disk))

    from seekdb_collection_client import get_wiki_collection
    coll = get_wiki_collection()
    total_in_db = coll.count()
    log.info("SeekDB wiki_pages: %d", total_in_db)

    if args.dry_run:
        log.info("Dry-run: would re-encode %d pages", len(disk))
        return 0

    # Load impl — this triggers model download on first run
    from seekdb_search_impl import SeekDBSearchImpl
    impl = SeekDBSearchImpl(str(WIKI_ROOT))
    _ = impl._get_model()  # eager-load
    log.info("After model load RSS: %.0f MB", mem_rss_mb())

    done = load_progress()
    if done:
        log.info("Resuming: %d already rebuilt", len(done))

    page_ids = sorted(pid for pid in disk if pid not in done)
    total = len(page_ids)
    log.info("Pages to rebuild: %d", total)

    if not page_ids:
        log.info("Nothing to do — all embeddings are up to date.")
        return 0

    success = 0
    errors = 0
    start = time.time()

    for i in range(0, total, args.batch):
        batch = page_ids[i : i + args.batch]
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

    # Cleanup progress file on full success
    if errors == 0 and PROGRESS_PATH.exists():
        PROGRESS_PATH.unlink()
        log.info("Progress file removed — rebuild complete.")

    return 0 if errors == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
