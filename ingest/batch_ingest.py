#!/usr/bin/env python3
"""ROSClaw Batch Ingest — process all raw sources into the Wiki.

Usage:
    source .venv/bin/activate && python batch_ingest.py [--reset]
"""

from __future__ import annotations

import argparse
import asyncio
import json
import logging
import os
import sys
import time
from datetime import datetime
from pathlib import Path

import event_bus
import wiki_engine as engine
from knowledge_synthesizer import KnowledgeSynthesizer
from llm_interface import LLMInterface

logger = logging.getLogger("rosclaw.batch")

PROCESSED_LOG = Path("data/processed_files.log")
FAILED_LOG = Path("data/failed_files.log")
WIKI_ROOT = Path("./wiki").resolve()
RAW_ROOT = Path("./data/raw").resolve()
QUALITY_REPORT_DIR = Path("./data/quality_reports").resolve()


def _setup_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def _read_source_text(source_path: str, raw_root: Path) -> tuple[str, str]:
    """Read a raw source and return (text_content, text_source).

    text_source is one of: "full_text", "abstract_only", "raw_text", "error"
    """
    src = Path(source_path)
    if not src.is_absolute():
        src = raw_root / source_path
    if not src.exists():
        return "", "error"

    if src.suffix == ".pdf":
        # Try full-text extraction first
        try:
            from pdf_extractor import extract_pdf_sections, is_extractor_available

            if is_extractor_available():
                sections = extract_pdf_sections(str(src))
                meta_path = src.with_suffix(".json")
                meta = {}
                if meta_path.exists():
                    try:
                        meta = json.loads(meta_path.read_text(encoding="utf-8"))
                    except Exception:
                        pass

                parts = [f"# {meta.get('title', 'Untitled Paper')}"]
                if meta.get("authors"):
                    parts.append(f"**Authors:** {', '.join(meta['authors'])}")

                abstract = sections.get("abstract", "")
                if not abstract and meta.get("summary"):
                    abstract = meta["summary"]
                if abstract:
                    parts.append("**Abstract:**\n" + abstract)

                for section in ("introduction", "methods", "experiments", "conclusion"):
                    content = sections.get(section, "")
                    if content:
                        parts.append("## " + section.capitalize() + "\n" + content)

                return "\n\n".join(parts), "full_text"
        except Exception as exc:
            logger.warning("Full-text extraction failed for %s: %s", src, exc)

        # Fallback to sidecar JSON abstract
        meta_path = src.with_suffix(".json")
        if meta_path.exists():
            try:
                meta = json.loads(meta_path.read_text(encoding="utf-8"))
                parts = [f"# {meta.get('title', 'Untitled Paper')}"]
                if meta.get("authors"):
                    parts.append(f"**Authors:** {', '.join(meta['authors'])}")
                if meta.get("summary"):
                    parts.append(f"**Abstract:** {meta.get('summary')}")
                return "\n\n".join(parts), "abstract_only"
            except Exception:
                pass
        return f"[PDF file at {src}; text extraction not available.]", "error"

    try:
        return src.read_text(encoding="utf-8", errors="ignore")[:12000], "raw_text"
    except Exception as exc:
        return f"[Error reading {src}: {exc}]", "error"


def _get_agents_md_text(wiki_root: Path) -> str:
    agents_path = wiki_root.parent / "AGENTS.md"
    if agents_path.exists():
        return agents_path.read_text(encoding="utf-8")
    return ""


def _load_processed_files() -> set[str]:
    if not PROCESSED_LOG.exists():
        return set()
    return set(line.strip() for line in PROCESSED_LOG.read_text(encoding="utf-8").splitlines() if line.strip())


def _save_processed_file(path: str) -> None:
    PROCESSED_LOG.parent.mkdir(parents=True, exist_ok=True)
    with PROCESSED_LOG.open("a", encoding="utf-8") as f:
        f.write(path + "\n")


def _save_failed_file(path: str, reason: str) -> None:
    FAILED_LOG.parent.mkdir(parents=True, exist_ok=True)
    with FAILED_LOG.open("a", encoding="utf-8") as f:
        f.write(f"{path} | {reason}\n")


def _collect_raw_files(raw_root: Path) -> list[tuple[str, str]]:
    """Collect all raw source files grouped by type. Returns list of (relative_path, kind)."""
    files: list[tuple[str, str]] = []
    for subdir, kind in [("papers", "paper"), ("code", "code"), ("articles", "article")]:
        d = raw_root / subdir
        if not d.exists():
            continue
        for fpath in d.rglob("*"):
            if not fpath.is_file():
                continue
            # Skip sidecar JSONs — PDF handler reads them automatically
            if fpath.suffix == ".json":
                continue
            rel = str(fpath.relative_to(raw_root))
            files.append((rel, kind))
    return files


def _auto_ingest_single(
    source_path: str,
    source_kind: str,
    wiki_root: Path,
    raw_root: Path,
    llm: LLMInterface,
    agents_text: str,
    synth: KnowledgeSynthesizer,
) -> dict:
    """Process a single source file through the full ingest pipeline."""
    source_text, text_source = _read_source_text(source_path, raw_root)
    if not source_text:
        return {"status": "skipped", "reason": "empty_source"}

    source_type = {
        "paper": "arxiv_paper",
        "code": "official_manual",
        "article": "blog_post",
    }.get(source_kind, "unknown")

    # Step 1: LLM extraction
    fulltext_instructions = ""
    if text_source == "full_text":
        fulltext_instructions = (
            "\nThis source contains the FULL TEXT of a research paper. "
            "From the Methods section, extract ALL quantifiable parameters "
            "(model hyperparameters, physical parameters, experimental settings). "
            "From the Experiments section, extract results, comparison tables, and performance metrics. "
            "From the Conclusion, extract key findings and limitations. "
            "Do NOT assume any specific domain—extract whatever numerical or technical details "
            "are actually present in the paper.\n"
        )

    extract_prompt = (
        f"You are extracting structured knowledge from a source for the ROSClaw Wiki.\n\n"
        f"AGENTS.md RULES:\n{agents_text[:2000]}\n\n"
        f"SOURCE:\n---\n{source_text}\n---\n\n"
        f"{fulltext_instructions}"
        f"TASK: Extract entities, algorithms, concepts, and skills mentioned.\n"
        f"Return a JSON list where each item has:\n"
        f'  "entity_type": "entity|algorithm|concept|skill",\n'
        f'  "entity_name": "Name",\n'
        f'  "new_facts": {{\n'
        f'    "parameters": {{"key": "value"}},\n'
        f'    "capabilities": ["cap1", "cap2"],\n'
        f'    "relationships": {{"uses": ["X"], "depends_on": ["Y"]}},\n'
        f'    "new_sections": {{"Section Title": "Content..."}}\n'
        f'  }},\n'
        f'  "source_type": "official_manual|arxiv_paper|blog_post"\n'
        f"\n## Cross-Reference Requirements (MANDATORY)\n"
        f"When extracting entities, you MUST actively search for related concepts already present in the source text "
        f"and establish wikilink connections using [[Page Title]] format. "
        f"For each newly extracted entity, include at least 3 wikilinks to related entities in its new_sections or relationships. "
        f"This ensures the knowledge graph remains densely connected and prevents orphan pages.\n"
        f"Return ONLY valid JSON. No markdown code fences."
    )

    try:
        extract_result = llm.complete(extract_prompt, system=agents_text[:4000], temperature=0.2)
        extract_result = extract_result.strip()
        if extract_result.startswith("```"):
            extract_result = extract_result.split("```json")[-1].split("```")[0].strip()
        entities = json.loads(extract_result)
        if isinstance(entities, dict):
            entities = [entities]
    except Exception as exc:
        return {"status": "failed", "reason": f"extraction_failed: {exc}"}

    # Step 2-4: Synthesize and write each entity
    summaries = []
    conflicts_detected: list[dict] = []
    for ent in entities:
        entity_type = ent.get("entity_type", "entity")
        entity_name = ent.get("entity_name", "Unknown")
        new_facts = ent.get("new_facts", {})

        plan = synth.synthesize(
            entity_type=entity_type,
            entity_name=entity_name,
            new_facts=new_facts,
            source_meta={
                "source_path": source_path,
                "source_type": source_type,
                "url": "",
            },
        )

        if plan.conflicts:
            for c in plan.conflicts:
                conflicts_detected.append({
                    "entity": entity_name,
                    "field": c.get("field"),
                    "old": c.get("old"),
                    "new": c.get("new"),
                    "source": source_path,
                })

        if plan.action == "skip":
            summaries.append({"entity": entity_name, "action": "skip"})
            continue

        if plan.action == "suggest_consolidation":
            summaries.append({"entity": entity_name, "action": "suggest_consolidation"})
            continue

        try:
            new_body = llm.complete(
                plan.prompt_for_rewrite,
                system=agents_text[:4000],
                temperature=0.3,
            )
            new_body = new_body.strip()
            if new_body.startswith("```"):
                new_body = new_body.split("```markdown")[-1].split("```")[0].strip()
        except Exception as exc:
            summaries.append({"entity": entity_name, "action": "error", "reason": str(exc)})
            continue

        if plan.action == "create_new":
            engine.create_page(
                str(Path(plan.target_page_path).parent),
                entity_name,
                new_body,
                plan.updated_frontmatter,
            )
        else:
            target = Path(plan.target_page_path)
            final_content = engine.write_frontmatter(plan.updated_frontmatter, new_body)
            target.write_text(final_content, encoding="utf-8")

        engine.append_log(
            str(wiki_root),
            f"ingest | {source_path} | entity: {entity_name} | action: {plan.action} | text_source: {text_source}",
        )
        summaries.append({
            "entity": entity_name,
            "action": plan.action,
            "confidence": plan.updated_frontmatter.get("confidence"),
        })

    return {
        "status": "done",
        "entities_processed": len(entities),
        "summaries": summaries,
        "conflicts_detected": conflicts_detected,
    }


async def _auto_ingest_single_async(
    rel_path: str,
    kind: str,
    wiki_root: Path,
    raw_root: Path,
    llm: LLMInterface,
    agents_text: str,
    synth: KnowledgeSynthesizer,
    semaphore: asyncio.Semaphore,
    stats: dict[str, Any],
) -> None:
    """Async wrapper around _auto_ingest_single with concurrency control and event emission."""
    async with semaphore:
        try:
            result = await asyncio.to_thread(
                _auto_ingest_single,
                rel_path,
                kind,
                wiki_root,
                raw_root,
                llm,
                agents_text,
                synth,
            )
        except Exception as exc:
            result = {"status": "failed", "reason": str(exc)}

        if result["status"] == "failed":
            stats["failed"] += 1
            _save_failed_file(rel_path, result["reason"])
            logger.error("[FAIL] %s: %s", rel_path, result["reason"])
        elif result["status"] == "skipped":
            stats["skipped"] += 1
        else:
            stats["processed"] += 1
            for s in result.get("summaries", []):
                if s["action"] == "create_new":
                    stats["pages_created"] += 1
                elif s["action"] in ("incremental_update", "full_rewrite"):
                    stats["pages_updated"] += 1
                elif s["action"] == "error":
                    stats["conflicts"] += 1
            logger.info("[DONE] %s: %d entities", rel_path, result["entities_processed"])

            # Emit conflict alerts
            for conflict in result.get("conflicts_detected", []):
                event_bus.emit(
                    "conflict_alert",
                    {
                        "entity": conflict["entity"],
                        "field": conflict["field"],
                        "old_value": conflict["old"],
                        "new_value": conflict["new"],
                        "source": conflict["source"],
                        "timestamp": datetime.now().isoformat(),
                    },
                )
                stats["conflicts"] += 1

        _save_processed_file(rel_path)

        # Emit progress event
        event_bus.emit(
            "ingest_progress",
            {
                "current": stats["processed"] + stats["failed"] + stats["skipped"],
                "total": stats["total"],
                "file": rel_path,
                "status": result["status"],
                "pages_created": stats["pages_created"],
                "pages_updated": stats["pages_updated"],
                "conflicts": stats["conflicts"],
                "timestamp": datetime.now().isoformat(),
            },
        )


async def _run_batch(
    files: list[tuple[str, str]],
    wiki_root: Path,
    raw_root: Path,
    llm: LLMInterface,
    agents_text: str,
    synth: KnowledgeSynthesizer,
    concurrency: int,
) -> dict[str, Any]:
    """Process all raw files concurrently with limited parallelism."""
    semaphore = asyncio.Semaphore(concurrency)
    stats: dict[str, Any] = {
        "total": len(files),
        "processed": 0,
        "skipped": 0,
        "failed": 0,
        "pages_created": 0,
        "pages_updated": 0,
        "conflicts": 0,
        "start_time": time.time(),
    }

    tasks = []
    for rel_path, kind in files:
        tasks.append(
            _auto_ingest_single_async(
                rel_path,
                kind,
                wiki_root,
                raw_root,
                llm,
                agents_text,
                synth,
                semaphore,
                stats,
            )
        )

    await asyncio.gather(*tasks, return_exceptions=True)

    elapsed = time.time() - stats["start_time"]
    stats["elapsed_seconds"] = round(elapsed, 1)
    return stats


def main() -> int:
    _setup_logging()
    parser = argparse.ArgumentParser(description="ROSClaw Batch Ingest")
    parser.add_argument("--reset", action="store_true", help="Clear progress and restart")
    parser.add_argument("--raw-root", default="./data/raw", help="Path to raw data directory")
    parser.add_argument("--wiki-root", default="./wiki", help="Path to wiki directory")
    parser.add_argument("--concurrency", type=int, default=5, help="Max concurrent LLM requests (default: 5)")
    args = parser.parse_args()

    wiki_root = Path(args.wiki_root).resolve()
    raw_root = Path(args.raw_root).resolve()
    wiki_root.mkdir(parents=True, exist_ok=True)
    raw_root.mkdir(parents=True, exist_ok=True)

    if args.reset:
        if PROCESSED_LOG.exists():
            PROCESSED_LOG.unlink()
            logger.info("Cleared processed files log")
        if FAILED_LOG.exists():
            FAILED_LOG.unlink()
            logger.info("Cleared failed files log")

    # Verify LLM
    try:
        llm = LLMInterface()
        if llm.backend == "none":
            logger.error("No LLM backend configured. Set ANTHROPIC_API_KEY, OPENAI_API_KEY, or DEEPSEEK_API_KEY.")
            return 1
        logger.info("LLM backend: %s", llm.backend)
    except Exception as exc:
        logger.error("LLM initialization failed: %s", exc)
        return 1

    agents_text = _get_agents_md_text(wiki_root)
    synth = KnowledgeSynthesizer(str(wiki_root))
    processed = _load_processed_files()

    files = _collect_raw_files(raw_root)
    logger.info("Found %d raw files to process", len(files))

    # Filter out already-processed files before spawning async tasks
    pending_files = [(rel, kind) for rel, kind in files if rel not in processed]
    if len(pending_files) < len(files):
        logger.info("Skipping %d already-processed files", len(files) - len(pending_files))

    # Emit batch start event
    event_bus.emit(
        "batch_ingest_started",
        {
            "total_files": len(pending_files),
            "concurrency": args.concurrency,
            "timestamp": datetime.now().isoformat(),
        },
    )

    stats = asyncio.run(
        _run_batch(
            pending_files,
            wiki_root,
            raw_root,
            llm,
            agents_text,
            synth,
            args.concurrency,
        )
    )

    # Emit batch complete event
    event_bus.emit(
        "batch_ingest_complete",
        {
            "summary": stats,
            "timestamp": datetime.now().isoformat(),
        },
    )

    # Update index once after all files are processed
    engine.update_index(str(wiki_root))

    # Final report
    report_lines = [
        "=" * 60,
        "ROSClaw Batch Ingest Report",
        "=" * 60,
        f"Total files:     {stats['total']}",
        f"Processed:       {stats['processed']}",
        f"Skipped:         {stats['skipped']}",
        f"Failed:          {stats['failed']}",
        f"Pages created:   {stats['pages_created']}",
        f"Pages updated:   {stats['pages_updated']}",
        f"Errors/conflicts:{stats['conflicts']}",
        f"Total time:      {stats['elapsed_seconds']}s",
        "=" * 60,
    ]
    report = "\n".join(report_lines)
    print(report)
    logger.info("Batch ingest complete. %s", report.replace("\n", " | "))

    engine.append_log(
        str(wiki_root),
        f"batch_ingest | total: {stats['total']} | processed: {stats['processed']} | "
        f"created: {stats['pages_created']} | updated: {stats['pages_updated']} | "
        f"failed: {stats['failed']} | time: {stats['elapsed_seconds']}s",
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
