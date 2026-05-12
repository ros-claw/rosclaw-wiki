"""Batch Sync — Multi-device ingestion pipeline for ROSClaw Wiki.

Device side:
    python batch_sync.py device-package --name batch_vln --output-dir ./submissions
    → Creates submission tar.gz ready for R2 upload

Production side:
    python batch_sync.py production-merge --submission submissions/batch_vln.tar.gz --dry-run
    python batch_sync.py production-merge --submission submissions/batch_vln.tar.gz
    → Merges into canonical wiki/ + data/code_graph.json + seekdb

R2 workflow:
    # Device pushes to R2
    python batch_sync.py device-upload --name batch_vln --r2-prefix submissions

    # Production pulls from R2 and merges
    python batch_sync.py production-merge --r2-key submissions/batch_vln.tar.gz
"""

from __future__ import annotations

import argparse
import hashlib
import json
import logging
import os
import shutil
import sqlite3
import subprocess
import sys
import tarfile
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Any

logger = logging.getLogger("rosclaw.batch_sync")

WIKI_ROOT = Path(os.environ.get("WIKI_ROOT", "wiki"))
DATA_DIR = Path(os.environ.get("DATA_DIR", "data"))
DB_PATH = Path(os.environ.get("SEEKDB_SQLITE_PATH", DATA_DIR / "seekdb_compat.db"))

# ── Manifest Schema ──
# {
#   "version": "1.0",
#   "device_id": "laptop-A",
#   "created_at": "2026-05-10T12:00:00",
#   "batch_name": "batch_vln",
#   "files": [
#     {"path": "wiki/entities/...", "size": 1234, "md5": "abc..."},
#     ...
#   ],
#   "code_graphs": ["data/code_graph_batch_vln.json"],
#   "judgments": "data/judgments_batch_vln.jsonl",
#   "wiki_pages": "data/wiki_pages_batch_vln.jsonl",
#   "stats": {"pages": 50, "judgments": 120, "code_graph_nodes": 3000}
# }


def _md5(path: Path) -> str:
    h = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def _load_manifest(tar_path: Path) -> dict[str, Any]:
    with tarfile.open(tar_path, "r:gz") as tf:
        manifest_member = tf.getmember("manifest.json")
        f = tf.extractfile(manifest_member)
        if f is None:
            raise ValueError("manifest.json not found in tarball")
        return json.loads(f.read().decode("utf-8"))


def _export_sqlite_to_jsonl(table: str, output_path: Path) -> int:
    """Export SQLite table rows to JSONL. Returns row count."""
    if not DB_PATH.exists():
        logger.warning("SQLite DB not found at %s, skipping %s export", DB_PATH, table)
        return 0
    count = 0
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.execute(f"SELECT * FROM {table}")
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            for row in cur:
                f.write(json.dumps(dict(row), ensure_ascii=False) + "\n")
                count += 1
    logger.info("Exported %d rows from %s → %s", count, table, output_path)
    return count


def _import_jsonl_to_sqlite(jsonl_path: Path, table: str, on_conflict: str = "REPLACE") -> int:
    """Import JSONL rows into SQLite. Returns imported count."""
    if not DB_PATH.exists():
        logger.error("SQLite DB not found at %s", DB_PATH)
        return 0
    if not jsonl_path.exists():
        logger.warning("JSONL file not found: %s", jsonl_path)
        return 0

    count = 0
    with sqlite3.connect(DB_PATH) as conn:
        # Get columns from table
        cur = conn.execute(f"PRAGMA table_info({table})")
        columns = [row[1] for row in cur.fetchall()]
        if not columns:
            logger.error("Table %s does not exist", table)
            return 0

        placeholders = ",".join("?" for _ in columns)
        sql = f"INSERT OR {on_conflict} INTO {table} ({','.join(columns)}) VALUES ({placeholders})"

        with open(jsonl_path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                row = json.loads(line)
                values = [row.get(c) for c in columns]
                try:
                    conn.execute(sql, values)
                    count += 1
                except Exception as exc:
                    logger.warning("Row insert failed: %s", exc)
        conn.commit()
    logger.info("Imported %d rows into %s from %s", count, table, jsonl_path)
    return count


def _import_jsonl_to_seekdb(jsonl_path: Path, collection_name: str) -> int:
    """Import JSONL rows into seekdb collections via pyseekdb."""
    try:
        from seekdb_collection_client import get_wiki_collection, get_judgments_collection
    except ImportError:
        logger.warning("pyseekdb not available, skipping seekdb import for %s", collection_name)
        return 0

    if not jsonl_path.exists():
        logger.warning("JSONL file not found: %s", jsonl_path)
        return 0

    coll = get_wiki_collection() if collection_name == "wiki_pages" else get_judgments_collection()
    count = 0
    batch: list[dict[str, Any]] = []
    batch_size = 100

    with open(jsonl_path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            row = json.loads(line)
            # Map SQLite schema to seekdb collection schema
            doc: dict[str, Any] = {"id": row.get("id", str(count)), "metadata": {}}
            for k, v in row.items():
                if k == "id":
                    continue
                if k == "embedding" and v is not None:
                    if isinstance(v, str):
                        v = json.loads(v)
                    doc["embeddings"] = v
                else:
                    doc["metadata"][k] = v
            batch.append(doc)
            if len(batch) >= batch_size:
                try:
                    coll.upsert(documents=batch)
                    count += len(batch)
                except Exception as exc:
                    logger.warning("Seekdb batch upsert failed: %s", exc)
                batch = []

    if batch:
        try:
            coll.upsert(documents=batch)
            count += len(batch)
        except Exception as exc:
            logger.warning("Seekdb final batch upsert failed: %s", exc)

    logger.info("Imported %d documents into seekdb collection %s", count, collection_name)
    return count


def _export_seekdb_to_jsonl(collection_name: str, output_path: Path) -> int:
    """Export seekdb collection to JSONL (if available)."""
    try:
        from seekdb_collection_client import get_wiki_collection, get_judgments_collection
    except ImportError:
        logger.info("pyseekdb not available, skipping seekdb export for %s", collection_name)
        return 0

    coll = get_wiki_collection() if collection_name == "wiki_pages" else get_judgments_collection()
    count = 0
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Try to get all documents — pyseekdb API may vary
    try:
        results = coll.get(include=["embeddings", "metadatas"])
        ids = results.get("ids", [])
        embeddings = results.get("embeddings", [])
        metadatas = results.get("metadatas", [])
        with open(output_path, "w", encoding="utf-8") as f:
            for i, doc_id in enumerate(ids):
                row: dict[str, Any] = {"id": doc_id}
                if i < len(metadatas) and metadatas[i]:
                    row.update(metadatas[i])
                if i < len(embeddings) and embeddings[i] is not None:
                    row["embedding"] = embeddings[i]
                f.write(json.dumps(row, ensure_ascii=False) + "\n")
                count += 1
    except Exception as exc:
        logger.warning("Seekdb export failed: %s", exc)

    logger.info("Exported %d documents from seekdb %s → %s", count, collection_name, output_path)
    return count


# ═══════════════════════════════════════════════════════════════════════════════
# Device-side packaging
# ═══════════════════════════════════════════════════════════════════════════════

def device_package(batch_name: str, output_dir: Path, wiki_root: Path, data_dir: Path) -> Path:
    """Package local wiki pages, code graphs, and judgments into a submission tarball."""
    output_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    tar_name = f"{batch_name}_{timestamp}.tar.gz"
    tar_path = output_dir / tar_name

    device_id = os.environ.get("DEVICE_ID", os.environ.get("HOSTNAME", "unknown"))
    staging = Path(tempfile.mkdtemp(prefix=f"rosclaw_pkg_{batch_name}_"))

    manifest: dict[str, Any] = {
        "version": "1.0",
        "device_id": device_id,
        "created_at": datetime.now().isoformat(),
        "batch_name": batch_name,
        "files": [],
        "code_graphs": [],
        "judgments": None,
        "wiki_pages": None,
        "stats": {},
    }

    # 1. Copy wiki pages
    wiki_staging = staging / "wiki"
    page_count = 0
    if wiki_root.exists():
        wiki_staging.mkdir(parents=True, exist_ok=True)
        for md_file in wiki_root.rglob("*.md"):
            if md_file.name in ("index.md", "log.md"):
                continue
            rel = md_file.relative_to(wiki_root)
            dest = wiki_staging / rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(md_file, dest)
            manifest["files"].append({
                "path": f"wiki/{rel}",
                "size": md_file.stat().st_size,
                "md5": _md5(md_file),
            })
            page_count += 1
    manifest["stats"]["pages"] = page_count

    # 2. Copy code_graph batch files
    data_staging = staging / "data"
    data_staging.mkdir(parents=True, exist_ok=True)
    cg_copied = []
    for cg_file in sorted(data_dir.glob("code_graph_batch_*.json")):
        dest = data_staging / cg_file.name
        shutil.copy2(cg_file, dest)
        cg_copied.append(f"data/{cg_file.name}")
        manifest["files"].append({
            "path": f"data/{cg_file.name}",
            "size": cg_file.stat().st_size,
            "md5": _md5(cg_file),
        })
    manifest["code_graphs"] = cg_copied

    # 3. Export judgments (SQLite first, fallback to seekdb)
    judgments_path = data_staging / f"judgments_{batch_name}.jsonl"
    j_count = _export_sqlite_to_jsonl("judgments", judgments_path)
    if j_count == 0:
        j_count = _export_seekdb_to_jsonl("judgments", judgments_path)
    if j_count > 0:
        manifest["judgments"] = f"data/judgments_{batch_name}.jsonl"
        manifest["files"].append({
            "path": manifest["judgments"],
            "size": judgments_path.stat().st_size,
            "md5": _md5(judgments_path),
        })
    manifest["stats"]["judgments"] = j_count

    # 4. Export wiki_pages (SQLite first, fallback to seekdb)
    wp_path = data_staging / f"wiki_pages_{batch_name}.jsonl"
    wp_count = _export_sqlite_to_jsonl("wiki_pages", wp_path)
    if wp_count == 0:
        wp_count = _export_seekdb_to_jsonl("wiki_pages", wp_path)
    if wp_count > 0:
        manifest["wiki_pages"] = f"data/wiki_pages_{batch_name}.jsonl"
        manifest["files"].append({
            "path": manifest["wiki_pages"],
            "size": wp_path.stat().st_size,
            "md5": _md5(wp_path),
        })
    manifest["stats"]["wiki_pages_exported"] = wp_count

    # 5. Write manifest
    manifest_path = staging / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")

    # 6. Create tarball
    with tarfile.open(tar_path, "w:gz") as tf:
        for item in staging.rglob("*"):
            if item.is_file():
                tf.add(item, arcname=item.relative_to(staging))

    # Cleanup staging
    shutil.rmtree(staging)

    logger.info(
        "Packaged submission: %s (%d pages, %d judgments, %d code graphs)",
        tar_path, page_count, j_count, len(cg_copied),
    )
    return tar_path


def device_upload(tar_path: Path, r2_prefix: str = "submissions") -> str:
    """Upload a submission tarball to R2.

    Requires R2 credentials in environment:
        R2_ENDPOINT, R2_ACCESS_KEY_ID, R2_SECRET_ACCESS_KEY, R2_BUCKET
    """
    from r2_sync import _get_r2_client

    s3 = _get_r2_client()
    bucket = os.environ.get("R2_BUCKET", "rosclaw-wiki")
    key = f"{r2_prefix}/{tar_path.name}"

    logger.info("Uploading %s to R2 bucket %s key %s ...", tar_path, bucket, key)
    s3.upload_file(str(tar_path), bucket, key)
    logger.info("Upload complete: %s", key)
    return key


# ═══════════════════════════════════════════════════════════════════════════════
# Production-side merge
# ═══════════════════════════════════════════════════════════════════════════════

def production_merge(
    tar_path: Path,
    wiki_root: Path,
    data_dir: Path,
    dry_run: bool = False,
    skip_code_graph: bool = False,
    skip_judgments: bool = False,
    skip_wiki_pages: bool = False,
) -> dict[str, Any]:
    """Merge a submission tarball into the canonical production dataset.

    Steps:
      1. Validate manifest and checksums
      2. Merge wiki/*.md pages
      3. Merge code_graph_batch_*.json into canonical code_graph.json
      4. Import judgments JSONL into SQLite + seekdb
      5. Import wiki_pages JSONL into SQLite + seekdb
      6. Rebuild wiki index
    """
    manifest = _load_manifest(tar_path)
    logger.info("Merging submission: %s from device=%s", manifest["batch_name"], manifest["device_id"])

    result: dict[str, Any] = {
        "batch_name": manifest["batch_name"],
        "dry_run": dry_run,
        "wiki_merged": 0,
        "wiki_conflicts": 0,
        "code_graph_merged": False,
        "judgments_imported": 0,
        "wiki_pages_imported": 0,
        "errors": [],
    }

    staging = Path(tempfile.mkdtemp(prefix=f"rosclaw_merge_{manifest['batch_name']}_"))

    # Extract tarball
    with tarfile.open(tar_path, "r:gz") as tf:
        tf.extractall(path=staging)

    # ── 1. Validate checksums ──
    for finfo in manifest.get("files", []):
        fpath = staging / finfo["path"]
        if not fpath.exists():
            result["errors"].append(f"Missing file: {finfo['path']}")
            continue
        actual_md5 = _md5(fpath)
        if actual_md5 != finfo["md5"]:
            result["errors"].append(
                f"Checksum mismatch: {finfo['path']} expected={finfo['md5']} actual={actual_md5}"
            )
    if result["errors"]:
        logger.error("Validation failed with %d errors", len(result["errors"]))
        if not dry_run:
            shutil.rmtree(staging)
        return result

    # ── 2. Merge wiki pages ──
    wiki_staging = staging / "wiki"
    if wiki_staging.exists() and not skip_wiki_pages:
        for src_file in wiki_staging.rglob("*.md"):
            rel = src_file.relative_to(wiki_staging)
            dest_file = wiki_root / rel
            if dest_file.exists():
                # Conflict: check frontmatter dates
                try:
                    import wiki_engine as engine
                    src_meta, _ = engine.parse_frontmatter(src_file.read_text(encoding="utf-8"))
                    dest_meta, _ = engine.parse_frontmatter(dest_file.read_text(encoding="utf-8"))
                    src_date = src_meta.get("created_at", "")
                    dest_date = dest_meta.get("created_at", "")
                    if src_date and dest_date and src_date < dest_date:
                        logger.info("Skipping older wiki page: %s", rel)
                        continue
                except Exception:
                    pass
                result["wiki_conflicts"] += 1
                if dry_run:
                    logger.info("[dry-run] Would overwrite wiki page: %s", rel)
                    continue
            if not dry_run:
                dest_file.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src_file, dest_file)
            result["wiki_merged"] += 1
            if dry_run:
                logger.info("[dry-run] Would merge wiki page: %s", rel)

    # ── 3. Merge code graphs ──
    cg_files = manifest.get("code_graphs", [])
    if cg_files and not skip_code_graph:
        canonical = data_dir / "code_graph.json"
        cg_inputs = [canonical] if canonical.exists() else []
        for cg_rel in cg_files:
            cg_path = staging / cg_rel
            if cg_path.exists():
                cg_inputs.append(cg_path)
        if len(cg_inputs) > 1:
            if dry_run:
                logger.info("[dry-run] Would merge %d code graphs into %s", len(cg_inputs), canonical)
            else:
                from code_graph_merger import merge_code_graphs
                merge_result = merge_code_graphs(cg_inputs, canonical, dedup_edges=True)
                logger.info(
                    "Code graph merged: %d nodes, %d edges, %d repos",
                    merge_result["node_count"],
                    merge_result["edge_count"],
                    merge_result.get("repo_count", 0),
                )
                result["code_graph_merged"] = True
                # Clean up merged batch files after successful merge
                for cg_rel in cg_files:
                    batch_path = data_dir / Path(cg_rel).name
                    if batch_path.exists():
                        batch_path.unlink()
                        logger.info("Removed merged batch file: %s", batch_path)

    # ── 4. Import judgments ──
    judgments_rel = manifest.get("judgments")
    if judgments_rel and not skip_judgments:
        j_path = staging / judgments_rel
        if j_path.exists():
            if dry_run:
                count = sum(1 for _ in open(j_path, encoding="utf-8") if _.strip())
                logger.info("[dry-run] Would import %d judgments", count)
                result["judgments_imported"] = count
            else:
                # SQLite
                result["judgments_imported"] = _import_jsonl_to_sqlite(j_path, "judgments")
                # Seekdb
                _import_jsonl_to_seekdb(j_path, "judgments")

    # ── 5. Import wiki_pages ──
    wp_rel = manifest.get("wiki_pages")
    if wp_rel and not skip_wiki_pages:
        wp_path = staging / wp_rel
        if wp_path.exists():
            if dry_run:
                count = sum(1 for _ in open(wp_path, encoding="utf-8") if _.strip())
                logger.info("[dry-run] Would import %d wiki_pages", count)
                result["wiki_pages_imported"] = count
            else:
                result["wiki_pages_imported"] = _import_jsonl_to_sqlite(wp_path, "wiki_pages")
                _import_jsonl_to_seekdb(wp_path, "wiki_pages")

    # ── 6. Rebuild index ──
    if not dry_run:
        try:
            # wiki_engine lives in core/ subdirectory
            _core_path = str(Path(__file__).parent / "core")
            if _core_path not in sys.path:
                sys.path.insert(0, _core_path)
            import wiki_engine as engine
            engine.update_index(str(wiki_root))
            logger.info("Wiki index rebuilt")
        except Exception as exc:
            logger.warning("Index rebuild failed: %s", exc)
            result["errors"].append(f"index_rebuild: {exc}")

    # Cleanup
    shutil.rmtree(staging)

    logger.info(
        "Merge complete: pages=%d conflicts=%d judgments=%d wiki_pages=%d",
        result["wiki_merged"],
        result["wiki_conflicts"],
        result["judgments_imported"],
        result["wiki_pages_imported"],
    )
    return result


def production_merge_from_r2(r2_key: str, **kwargs: Any) -> dict[str, Any]:
    """Download a submission from R2, then merge it."""
    from r2_sync import generate_presigned_download_url

    logger.info("Downloading submission from R2: %s", r2_key)
    url = generate_presigned_download_url(r2_key, expiry=3600)

    # Download via curl
    tar_path = DATA_DIR / "submissions" / Path(r2_key).name
    tar_path.parent.mkdir(parents=True, exist_ok=True)

    subprocess.run(["curl", "-sL", "-o", str(tar_path), url], check=True)
    logger.info("Downloaded to %s", tar_path)

    result = production_merge(tar_path, WIKI_ROOT, DATA_DIR, **kwargs)
    return result


# ═══════════════════════════════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════════════════════════════

def _main() -> None:
    parser = argparse.ArgumentParser(description="ROSClaw Wiki Batch Sync")
    sub = parser.add_subparsers(dest="command", required=True)

    # device-package
    pkg = sub.add_parser("device-package", help="Package local ingestion results")
    pkg.add_argument("--name", required=True, help="Batch name (e.g., batch_vln)")
    pkg.add_argument("--output-dir", type=Path, default=Path("submissions"))
    pkg.add_argument("--wiki-root", type=Path, default=WIKI_ROOT)
    pkg.add_argument("--data-dir", type=Path, default=DATA_DIR)

    # device-upload
    upl = sub.add_parser("device-upload", help="Upload submission to R2")
    upl.add_argument("--tar", type=Path, required=True, help="Path to submission tar.gz")
    upl.add_argument("--r2-prefix", default="submissions", help="R2 key prefix")

    # production-merge
    mrg = sub.add_parser("production-merge", help="Merge submission into production")
    mrg.add_argument("--submission", type=Path, help="Local tar.gz path")
    mrg.add_argument("--r2-key", help="R2 object key (downloads first)")
    mrg.add_argument("--wiki-root", type=Path, default=WIKI_ROOT)
    mrg.add_argument("--data-dir", type=Path, default=DATA_DIR)
    mrg.add_argument("--dry-run", action="store_true", help="Preview changes without applying")
    mrg.add_argument("--skip-code-graph", action="store_true")
    mrg.add_argument("--skip-judgments", action="store_true")
    mrg.add_argument("--skip-wiki-pages", action="store_true")

    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(message)s")

    if args.command == "device-package":
        tar_path = device_package(
            batch_name=args.name,
            output_dir=args.output_dir,
            wiki_root=args.wiki_root,
            data_dir=args.data_dir,
        )
        print(f"\nCreated: {tar_path}")
        print(f"Next step: python batch_sync.py device-upload --tar {tar_path}")

    elif args.command == "device-upload":
        key = device_upload(args.tar, args.r2_prefix)
        print(f"\nUploaded to R2: {key}")
        print(f"Next step (production): python batch_sync.py production-merge --r2-key {key}")

    elif args.command == "production-merge":
        if args.r2_key:
            result = production_merge_from_r2(
                args.r2_key,
                dry_run=args.dry_run,
                skip_code_graph=args.skip_code_graph,
                skip_judgments=args.skip_judgments,
                skip_wiki_pages=args.skip_wiki_pages,
            )
        elif args.submission:
            result = production_merge(
                args.submission,
                wiki_root=args.wiki_root,
                data_dir=args.data_dir,
                dry_run=args.dry_run,
                skip_code_graph=args.skip_code_graph,
                skip_judgments=args.skip_judgments,
                skip_wiki_pages=args.skip_wiki_pages,
            )
        else:
            parser.error("--submission or --r2-key required")
            sys.exit(1)
        print("\n" + json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    _main()
