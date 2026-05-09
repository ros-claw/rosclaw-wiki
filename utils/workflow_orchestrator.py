#!/usr/bin/env python3
"""ROSClaw Workflow Orchestrator — chain-triggered knowledge pipeline.

Watches event_bus and automatically triggers the full pipeline:
    raw_watcher_alert → batch_ingest → entity_linker → conflict_resolver → judgment_generator

Usage:
    python workflow_orchestrator.py --watch           # Start event listener
    python workflow_orchestrator.py --run-all         # Run full pipeline once
    python workflow_orchestrator.py --step conflict_resolver --pages "a.md,b.md"
"""

from __future__ import annotations

import argparse
import asyncio
import json
import logging
import subprocess
import sys
import threading
import time
from datetime import datetime
from pathlib import Path
from typing import Any

import event_bus
import wiki_engine as engine
from llm_interface import LLMInterface

logger = logging.getLogger("rosclaw.workflow")

# Event types this orchestrator listens to
_WATCHED_EVENTS = {
    "raw_watcher_alert",
    "batch_ingest_complete",
    "entity_link_complete",
    "conflict_resolution_complete",
}

# Pipeline state
_pipeline_state: dict[str, Any] = {
    "status": "idle",
    "current_step": None,
    "progress": {},
    "start_time": None,
    "last_update": None,
}
_state_lock = threading.Lock()


def _setup_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def _update_state(status: str, step: str | None = None, progress: dict[str, Any] | None = None) -> None:
    with _state_lock:
        _pipeline_state["status"] = status
        if step is not None:
            _pipeline_state["current_step"] = step
        if progress is not None:
            _pipeline_state["progress"].update(progress)
        _pipeline_state["last_update"] = datetime.now().isoformat()


def _get_state() -> dict[str, Any]:
    with _state_lock:
        return dict(_pipeline_state)


# ── Step runners ──


def _run_batch_ingest(wiki_root: str, raw_root: str, concurrency: int = 5) -> dict[str, Any]:
    """Run batch_ingest.py as a subprocess."""
    _update_state("running", "batch_ingest")
    logger.info("[Pipeline] Starting batch_ingest...")

    cmd = [
        sys.executable,
        "-m",
        "batch_ingest",
        "--wiki-root", wiki_root,
        "--raw-root", raw_root,
        "--concurrency", str(concurrency),
    ]

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=3600,
        )
        success = result.returncode == 0
        logger.info("[Pipeline] batch_ingest finished: rc=%d", result.returncode)
        return {
            "step": "batch_ingest",
            "success": success,
            "stdout": result.stdout[-2000:] if result.stdout else "",
            "stderr": result.stderr[-1000:] if result.stderr else "",
        }
    except subprocess.TimeoutExpired:
        logger.error("[Pipeline] batch_ingest timed out")
        return {"step": "batch_ingest", "success": False, "error": "timeout"}
    except Exception as exc:
        logger.exception("[Pipeline] batch_ingest failed")
        return {"step": "batch_ingest", "success": False, "error": str(exc)}


def _run_entity_linker(wiki_root: str) -> dict[str, Any]:
    """Run entity linker over all wiki pages."""
    _update_state("running", "entity_linker")
    logger.info("[Pipeline] Starting entity_linker...")

    try:
        import entity_linker

        root = Path(wiki_root)
        total_links = 0
        pages_affected = 0

        for md_file in root.rglob("*.md"):
            if md_file.name in ("index.md", "log.md", "Admin_Dashboard.md"):
                continue
            links = entity_linker.process(str(wiki_root), str(md_file), write_back=True)
            if links:
                total_links += len(links)
                pages_affected += 1

        logger.info("[Pipeline] entity_linker finished: %d links on %d pages", total_links, pages_affected)
        return {
            "step": "entity_linker",
            "success": True,
            "total_links": total_links,
            "pages_affected": pages_affected,
        }
    except Exception as exc:
        logger.exception("[Pipeline] entity_linker failed")
        return {"step": "entity_linker", "success": False, "error": str(exc)}


def _run_conflict_resolver(wiki_root: str, pages: list[str] | None = None) -> dict[str, Any]:
    """Run conflict resolver over specified or all pages."""
    _update_state("running", "conflict_resolver")
    logger.info("[Pipeline] Starting conflict_resolver...")

    try:
        import conflict_resolver

        root = Path(wiki_root)
        targets = pages if pages else []

        if not targets:
            for md_file in root.rglob("*.md"):
                if md_file.name in ("index.md", "log.md", "Admin_Dashboard.md"):
                    continue
                try:
                    content = md_file.read_text(encoding="utf-8")
                    if "### 待核实冲突" in content:
                        targets.append(str(md_file))
                except Exception:
                    continue

        resolved = 0
        unresolved = 0
        for page_path in targets:
            adjs = conflict_resolver.resolve_page_conflicts(page_path)
            if adjs:
                conflict_resolver.write_adjudication_to_page(page_path, adjs)
                resolved += sum(1 for a in adjs if a.resolved)
                unresolved += sum(1 for a in adjs if not a.resolved)

        logger.info("[Pipeline] conflict_resolver finished: %d resolved, %d unresolved", resolved, unresolved)
        return {
            "step": "conflict_resolver",
            "success": True,
            "resolved": resolved,
            "unresolved": unresolved,
        }
    except Exception as exc:
        logger.exception("[Pipeline] conflict_resolver failed")
        return {"step": "conflict_resolver", "success": False, "error": str(exc)}


def _run_judgment_generator(wiki_root: str) -> dict[str, Any]:
    """Run judgment generator over all pages."""
    _update_state("running", "judgment_generator")
    logger.info("[Pipeline] Starting judgment_generator...")

    try:
        import judgment_generator

        result = judgment_generator.generate_all_judgments(wiki_root)
        logger.info("[Pipeline] judgment_generator finished: %d judgments", result.get("judgments_generated", 0))
        return {
            "step": "judgment_generator",
            "success": True,
            "judgments_generated": result.get("judgments_generated", 0),
        }
    except Exception as exc:
        logger.exception("[Pipeline] judgment_generator failed")
        return {"step": "judgment_generator", "success": False, "error": str(exc)}


def _generate_report(wiki_root: str, results: list[dict[str, Any]]) -> None:
    """Write workflow summary to wiki/log.md."""
    lines = [
        f"## [{datetime.now().isoformat(timespec='seconds')}] workflow_orchestrator | pipeline complete",
        "",
        "| Step | Status | Details |",
        "|------|--------|---------|",
    ]
    for r in results:
        status = "✅" if r.get("success") else "❌"
        details = r.get("error", "")
        if not details and "total_links" in r:
            details = f"{r['total_links']} links, {r['pages_affected']} pages"
        elif not details and "resolved" in r:
            details = f"{r['resolved']} resolved, {r['unresolved']} unresolved"
        elif not details and "judgments_generated" in r:
            details = f"{r['judgments_generated']} judgments"
        lines.append(f"| {r['step']} | {status} | {details} |")
    lines.append("")

    report = "\n".join(lines)
    log_path = Path(wiki_root) / "log.md"
    with log_path.open("a", encoding="utf-8") as f:
        f.write(report + "\n")
    logger.info("[Pipeline] Report written to wiki/log.md")


# ── Pipeline orchestration ──


def run_full_pipeline(wiki_root: str, raw_root: str, concurrency: int = 5) -> list[dict[str, Any]]:
    """Execute the full pipeline once."""
    _update_state("running", "batch_ingest", {"start_time": datetime.now().isoformat()})
    _pipeline_state["start_time"] = datetime.now().isoformat()

    results: list[dict[str, Any]] = []

    # Step 1: batch ingest
    r1 = _run_batch_ingest(wiki_root, raw_root, concurrency)
    results.append(r1)
    if not r1["success"]:
        logger.error("[Pipeline] batch_ingest failed, aborting pipeline")
        _update_state("failed")
        _generate_report(wiki_root, results)
        return results

    # Step 2: entity linker
    r2 = _run_entity_linker(wiki_root)
    results.append(r2)

    # Step 3: conflict resolver
    r3 = _run_conflict_resolver(wiki_root)
    results.append(r3)

    # Step 4: judgment generator
    r4 = _run_judgment_generator(wiki_root)
    results.append(r4)

    _update_state("completed")
    _generate_report(wiki_root, results)

    # Emit completion event
    event_bus.emit(
        "workflow_complete",
        {
            "steps": [r["step"] for r in results],
            "all_success": all(r["success"] for r in results),
            "timestamp": datetime.now().isoformat(),
        },
    )

    return results


# ── Event-driven watcher ──


def _poll_events(wiki_root: str, raw_root: str, concurrency: int, interval: float = 5.0) -> None:
    """Poll event_bus for raw_watcher_alert and trigger pipeline."""
    logger.info("[Watcher] Starting event poll loop (interval=%.1fs)", interval)
    last_t = 0.0

    while True:
        events = event_bus.tail_events(since=last_t)
        for evt in events:
            last_t = max(last_t, evt.get("t", 0))

            if evt.get("type") == "raw_watcher_alert":
                new_files = evt.get("payload", {}).get("new_files", [])
                count = evt.get("payload", {}).get("count", 0)
                logger.info("[Watcher] Detected %d new raw file(s), triggering pipeline", count)
                run_full_pipeline(wiki_root, raw_root, concurrency)

            elif evt.get("type") == "batch_ingest_complete":
                # Auto-trigger entity linker after batch ingest
                logger.info("[Watcher] batch_ingest_complete detected, triggering entity_linker")
                _run_entity_linker(wiki_root)
                # Then trigger conflict resolver
                _run_conflict_resolver(wiki_root)
                # Then trigger judgment generator
                _run_judgment_generator(wiki_root)

        time.sleep(interval)


# ── CLI ──


def main() -> int:
    _setup_logging()
    parser = argparse.ArgumentParser(description="ROSClaw Workflow Orchestrator")
    parser.add_argument("--watch", action="store_true", help="Start event watcher loop")
    parser.add_argument("--run-all", action="store_true", help="Run full pipeline once")
    parser.add_argument("--step", choices=["batch_ingest", "entity_linker", "conflict_resolver", "judgment_generator"],
                        help="Run a single step")
    parser.add_argument("--pages", default="", help="Comma-separated page paths for conflict_resolver step")
    parser.add_argument("--wiki-root", default="./wiki", help="Wiki root directory")
    parser.add_argument("--raw-root", default="./data/raw", help="Raw data directory")
    parser.add_argument("--concurrency", type=int, default=5, help="Max concurrent LLM requests")
    args = parser.parse_args()

    wiki_root = str(Path(args.wiki_root).resolve())
    raw_root = str(Path(args.raw_root).resolve())

    if args.watch:
        _poll_events(wiki_root, raw_root, args.concurrency)
        return 0

    if args.run_all:
        results = run_full_pipeline(wiki_root, raw_root, args.concurrency)
        success = all(r["success"] for r in results)
        return 0 if success else 1

    if args.step:
        if args.step == "batch_ingest":
            r = _run_batch_ingest(wiki_root, raw_root, args.concurrency)
        elif args.step == "entity_linker":
            r = _run_entity_linker(wiki_root)
        elif args.step == "conflict_resolver":
            pages = [p.strip() for p in args.pages.split(",") if p.strip()]
            r = _run_conflict_resolver(wiki_root, pages or None)
        elif args.step == "judgment_generator":
            r = _run_judgment_generator(wiki_root)
        else:
            logger.error("Unknown step: %s", args.step)
            return 1

        print(json.dumps(r, indent=2, default=str))
        return 0 if r.get("success") else 1

    parser.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
