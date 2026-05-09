"""Import high-value code entities from code_graph.json to SeekDB.

Usage:
    python scripts/import_code_entities.py \
        --input data/code_graph.json \
        --centrality-threshold 5 \
        --max-nodes 8000
"""
from __future__ import annotations

import argparse
import json
import logging
from pathlib import Path
from typing import Any

logger = logging.getLogger("rosclaw.import_code_entities")


def _is_public_api(name: str) -> bool:
    """Check if a function/class name indicates a public API."""
    prefixes = ("get_", "set_", "compute_", "plan_", "execute_", "run_",
                "build_", "create_", "update_", "delete_", "search_",
                "generate_", "validate_", "parse_", "render_", "train_",
                "infer_", "predict_", "forward_", "backward_", "step_",
                "load_", "save_", "init_", "setup_", "configure_",
                "start_", "stop_", "reset_", "evaluate_", "transform_")
    return name.startswith(prefixes) or name == "__init__"


def calculate_centrality(graph: dict[str, Any]) -> dict[str, dict[str, Any]]:
    """Calculate in-degree, out-degree, and centrality score for each node."""
    node_ids = {n["id"] for n in graph["nodes"]}
    centrality: dict[str, dict[str, Any]] = {}

    # Build index for fast lookup
    in_counts: dict[str, int] = {}
    out_counts: dict[str, int] = {}
    for edge in graph["edges"]:
        src = edge.get("source", "")
        tgt = edge.get("target", "")
        if src in node_ids:
            out_counts[src] = out_counts.get(src, 0) + 1
        if tgt in node_ids:
            in_counts[tgt] = in_counts.get(tgt, 0) + 1

    total_nodes = len(graph["nodes"])
    for node in graph["nodes"]:
        nid = node["id"]
        indeg = in_counts.get(nid, 0)
        outdeg = out_counts.get(nid, 0)
        centrality[nid] = {
            "in_degree": indeg,
            "out_degree": outdeg,
            "total_degree": indeg + outdeg,
            "centrality_score": round(indeg / max(1, total_nodes), 6),
        }
    return centrality


def filter_high_value_nodes(
    graph: dict[str, Any],
    centrality: dict[str, dict[str, Any]],
    in_degree_threshold: int = 5,
    max_nodes: int | None = None,
) -> list[dict[str, Any]]:
    """Filter nodes that are high-value by centrality or public API."""
    selected: list[dict[str, Any]] = []
    node_by_id = {n["id"]: n for n in graph["nodes"]}

    for nid, c in centrality.items():
        node = node_by_id[nid]
        is_external = node.get("repo", "") != "rosclaw-wiki"
        is_public = _is_public_api(node.get("name", ""))
        if c["in_degree"] >= in_degree_threshold or is_public or is_external:
            enriched = dict(node)
            enriched["centrality"] = c
            enriched["is_public_api"] = is_public
            selected.append(enriched)

    # Sort by in_degree descending, then by centrality_score
    selected.sort(key=lambda n: (n["centrality"]["in_degree"], n["centrality"]["centrality_score"]), reverse=True)

    if max_nodes is not None and len(selected) > max_nodes:
        selected = selected[:max_nodes]

    return selected


def import_to_seekdb(nodes: list[dict[str, Any]], batch_size: int = 100) -> dict[str, Any]:
    """Import selected code entities to SeekDB wiki_pages collection."""
    import sys
    sys.path.insert(0, str(Path(__file__).parent.parent))
    from seekdb_collection_client import get_wiki_collection

    coll = get_wiki_collection()
    imported = 0
    errors = 0

    ids_batch: list[str] = []
    docs_batch: list[str] = []
    meta_batch: list[dict[str, Any]] = []

    for node in nodes:
        nid = node["id"]
        docstring = node.get("docstring", "")
        centrality = node.get("centrality", {})

        doc_id = f"code_entity/{node.get('repo', 'unknown')}:{node.get('file', '')}:{node.get('name', '')}"
        # Normalize doc_id to avoid collisions
        doc_id = doc_id.replace("/", "_").replace(" ", "_")[:256]

        ids_batch.append(doc_id)
        docs_batch.append(docstring)
        meta_batch.append({
            "type": "code_entity",
            "title": node.get("name", ""),
            "tags": f"{node.get('repo', '')},{node.get('type', '')}",
            "confidence": 0.7,
            "created_at": "",
            "last_reinforced": "",
            "sources": json.dumps([node.get("file", "")]),
            "wikilinks": "",
            "in_degree": centrality.get("in_degree", 0),
            "out_degree": centrality.get("out_degree", 0),
            "centrality_score": centrality.get("centrality_score", 0.0),
            "is_public_api": node.get("is_public_api", False),
            "source_repo": node.get("repo", ""),
            "language": "python",
            "auto_generated": True,
        })

        if len(ids_batch) >= batch_size:
            try:
                coll.upsert(ids=ids_batch, documents=docs_batch, metadatas=meta_batch)
                imported += len(ids_batch)
                logger.info("Imported %d code entities", imported)
            except Exception as exc:
                logger.warning("Batch import error: %s", exc)
                errors += len(ids_batch)
            ids_batch, docs_batch, meta_batch = [], [], []

    if ids_batch:
        try:
            coll.upsert(ids=ids_batch, documents=docs_batch, metadatas=meta_batch)
            imported += len(ids_batch)
        except Exception as exc:
            logger.warning("Final batch import error: %s", exc)
            errors += len(ids_batch)

    logger.info("Import complete: %d imported, %d errors", imported, errors)
    return {"status": "done", "imported": imported, "errors": errors}


def main() -> int:
    parser = argparse.ArgumentParser(description="Import high-value code entities to SeekDB")
    parser.add_argument("--input", default="data/code_graph.json", help="Code graph JSON")
    parser.add_argument("--centrality-threshold", type=int, default=5, help="Min in-degree")
    parser.add_argument("--max-nodes", type=int, default=8000, help="Max nodes to import")
    parser.add_argument("--batch-size", type=int, default=100, help="Batch size")
    parser.add_argument("--dry-run", action="store_true", help="Preview only")
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")

    path = Path(args.input)
    if not path.exists():
        logger.error("File not found: %s", args.input)
        return 1

    logger.info("Loading code graph from %s", args.input)
    with path.open("r", encoding="utf-8") as f:
        graph = json.load(f)

    logger.info("Calculating centrality for %d nodes", len(graph["nodes"]))
    centrality = calculate_centrality(graph)

    logger.info("Filtering high-value nodes (threshold=%d, max=%s)", args.centrality_threshold, args.max_nodes)
    selected = filter_high_value_nodes(
        graph, centrality,
        in_degree_threshold=args.centrality_threshold,
        max_nodes=args.max_nodes,
    )
    logger.info("Selected %d high-value nodes", len(selected))

    # Summary stats
    external_count = sum(1 for n in selected if n.get("repo") != "rosclaw-wiki")
    public_count = sum(1 for n in selected if n.get("is_public_api"))
    logger.info("External: %d, Public API: %d", external_count, public_count)

    if args.dry_run:
        logger.info("Dry run: would import %d nodes", len(selected))
        return 0

    result = import_to_seekdb(selected, args.batch_size)
    print(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


__all__ = ["calculate_centrality", "filter_high_value_nodes", "import_to_seekdb"]
