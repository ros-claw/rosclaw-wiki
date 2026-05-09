"""Import to SeekDB — batch import from JSONL to SeekDB/SQLite or pyseekdb.

Usage:
    python import_to_seekdb.py --input data/seekdb_import.jsonl
    python import_to_seekdb.py --input data/seekdb_import.jsonl --backend pyseekdb
    python import_to_seekdb.py --input data/seekdb_import.jsonl --dry-run
"""
from __future__ import annotations

import argparse
import json
import logging
from pathlib import Path
from typing import Any

logger = logging.getLogger("rosclaw.seekdb_import")


def import_pages_sqlite(jsonl_path: str, batch_size: int = 500, dry_run: bool = False) -> dict[str, Any]:
    """Import wiki pages from JSONL to SQLite compat layer."""
    from seekdb_client import get_connection

    path = Path(jsonl_path)
    if not path.exists():
        return {"status": "error", "error": f"File not found: {jsonl_path}"}

    records: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                records.append(json.loads(line))

    if dry_run:
        logger.info("Dry run: would import %d records", len(records))
        return {"status": "dry_run", "records": len(records)}

    imported = 0
    errors = 0

    with get_connection() as conn:
        for i in range(0, len(records), batch_size):
            batch = records[i : i + batch_size]
            for rec in batch:
                try:
                    conn.execute(
                        """
                        INSERT INTO wiki_pages (id, type, title, body, tags, confidence, created_at, last_reinforced, sources, embedding, wikilinks)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        ON CONFLICT(id) DO UPDATE SET
                            type=excluded.type, title=excluded.title, body=excluded.body,
                            tags=excluded.tags, confidence=excluded.confidence,
                            created_at=excluded.created_at, last_reinforced=excluded.last_reinforced,
                            sources=excluded.sources, embedding=excluded.embedding, wikilinks=excluded.wikilinks
                        """,
                        (
                            rec.get("id", ""),
                            rec.get("type", "episode"),
                            rec.get("title", ""),
                            rec.get("body", ""),
                            json.dumps(rec.get("tags", []), ensure_ascii=False),
                            rec.get("confidence", 0.5),
                            rec.get("created_at", ""),
                            rec.get("last_reinforced", ""),
                            json.dumps(rec.get("sources", []), ensure_ascii=False),
                            json.dumps(rec.get("vector"), ensure_ascii=False) if rec.get("vector") else None,
                            json.dumps(rec.get("wikilinks", []), ensure_ascii=False),
                        ),
                    )
                    imported += 1
                except Exception as exc:
                    logger.warning("Import error for %s: %s", rec.get("id"), exc)
                    errors += 1
            conn.commit()
            logger.info("Batch %d-%d imported", i, min(i + batch_size, len(records)))

    logger.info("Import complete: %d imported, %d errors", imported, errors)
    return {"status": "done", "imported": imported, "errors": errors}


def import_pages_pyseekdb(jsonl_path: str, batch_size: int = 100, dry_run: bool = False) -> dict[str, Any]:
    """Import wiki pages from JSONL to pyseekdb collection."""
    from seekdb_collection_client import get_wiki_collection

    path = Path(jsonl_path)
    if not path.exists():
        return {"status": "error", "error": f"File not found: {jsonl_path}"}

    coll = get_wiki_collection()
    total = 0
    errors = 0

    ids_batch: list[str] = []
    docs_batch: list[str] = []
    emb_batch: list[list[float]] = []
    meta_batch: list[dict[str, Any]] = []

    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
            except json.JSONDecodeError:
                errors += 1
                continue

            if dry_run:
                total += 1
                continue

            page_id = rec.get("id", "")
            body = rec.get("body", "")
            title = rec.get("title", page_id)
            page_type = rec.get("type", "episode")
            tags = ",".join(rec.get("tags", []))
            confidence = rec.get("confidence", 0.5)
            created_at = rec.get("created_at", "")
            last_reinforced = rec.get("last_reinforced", "")
            sources = json.dumps(rec.get("sources", []), ensure_ascii=False)
            wikilinks = ",".join(rec.get("wikilinks", []))

            vector = rec.get("vector")
            embedding: list[float] | None = None
            if vector:
                embedding = [round(float(x), 6) for x in vector]

            ids_batch.append(page_id)
            docs_batch.append(body)
            emb_batch.append(embedding)
            meta_batch.append({
                "type": page_type,
                "title": title,
                "tags": tags,
                "confidence": confidence,
                "created_at": created_at,
                "last_reinforced": last_reinforced,
                "sources": sources,
                "wikilinks": wikilinks,
            })

            if len(ids_batch) >= batch_size:
                _flush_pyseekdb_batch(coll, ids_batch, docs_batch, emb_batch, meta_batch)
                total += len(ids_batch)
                logger.info("Imported %d pages so far", total)
                ids_batch, docs_batch, emb_batch, meta_batch = [], [], [], []

    if ids_batch and not dry_run:
        _flush_pyseekdb_batch(coll, ids_batch, docs_batch, emb_batch, meta_batch)
        total += len(ids_batch)

    if dry_run:
        logger.info("Dry run: would import %d records", total)
        return {"status": "dry_run", "records": total}

    logger.info("Import complete: %d imported, %d errors", total, errors)
    return {"status": "done", "imported": total, "errors": errors}


def _flush_pyseekdb_batch(coll, ids, documents, embeddings, metadatas):
    # Split into two groups: with embeddings and without
    ids_with, docs_with, emb_with, meta_with = [], [], [], []
    ids_without, docs_without, meta_without = [], [], []

    for i, emb in enumerate(embeddings):
        if emb is not None:
            ids_with.append(ids[i])
            docs_with.append(documents[i])
            emb_with.append(emb)
            meta_with.append(metadatas[i])
        else:
            ids_without.append(ids[i])
            docs_without.append(documents[i])
            meta_without.append(metadatas[i])

    if ids_with:
        coll.upsert(
            ids=ids_with,
            documents=docs_with,
            embeddings=emb_with,
            metadatas=meta_with,
        )
    if ids_without:
        coll.upsert(
            ids=ids_without,
            documents=docs_without,
            metadatas=meta_without,
        )


def import_judgments_sqlite(wiki_root: str, dry_run: bool = False) -> dict[str, Any]:
    """Import judgments from file system to SQLite."""
    from seekdb_client import get_connection

    try:
        from judgment_generator import list_judgments
        result = list_judgments(wiki_root=wiki_root)
        judgments = result.get("judgments", [])
    except Exception as exc:
        return {"status": "error", "error": str(exc)}

    if dry_run:
        return {"status": "dry_run", "judgments": len(judgments)}

    imported = 0
    with get_connection() as conn:
        for j in judgments:
            try:
                conn.execute(
                    """
                    INSERT INTO judgments (id, entity, context, parameter, recommended_value, confidence, sources, conflicts_resolved)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    ON CONFLICT(id) DO UPDATE SET
                        entity=excluded.entity, context=excluded.context, parameter=excluded.parameter,
                        recommended_value=excluded.recommended_value, confidence=excluded.confidence,
                        sources=excluded.sources, conflicts_resolved=excluded.conflicts_resolved
                    """,
                    (
                        j.get("id", f"{j.get('entity')}:{j.get('parameter')}"),
                        j.get("entity", ""),
                        j.get("context", ""),
                        j.get("parameter", ""),
                        str(j.get("recommended_value", "")),
                        j.get("confidence", 0.0),
                        json.dumps(j.get("sources", []), ensure_ascii=False),
                        not j.get("unresolved", True),
                    ),
                )
                imported += 1
            except Exception as exc:
                logger.warning("Judgment import error: %s", exc)
        conn.commit()

    return {"status": "done", "imported": imported}


def main() -> int:
    parser = argparse.ArgumentParser(description="Import ROSClaw Wiki data to SeekDB")
    parser.add_argument("--input", default="data/seekdb_import.jsonl", help="JSONL input file")
    parser.add_argument("--batch-size", type=int, default=500, help="Batch size")
    parser.add_argument("--dry-run", action="store_true", help="Preview without writing")
    parser.add_argument("--wiki-root", default="wiki", help="Wiki root for judgments")
    parser.add_argument("--backend", default="pyseekdb", choices=["sqlite", "pyseekdb"], help="Backend to import to")
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")

    if args.backend == "sqlite":
        pages_result = import_pages_sqlite(args.input, args.batch_size, args.dry_run)
    else:
        pages_result = import_pages_pyseekdb(args.input, args.batch_size, args.dry_run)

    judgments_result = import_judgments_sqlite(args.wiki_root, args.dry_run)

    print({"pages": pages_result, "judgments": judgments_result})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


__all__ = ["import_pages_sqlite", "import_pages_pyseekdb", "import_judgments_sqlite"]
