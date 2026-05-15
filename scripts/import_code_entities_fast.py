"""Fast import of code entities using bulk embedding computation.

Usage:
    python scripts/import_code_entities_fast.py \
        --input data/code_graph.json \
        --centrality-threshold 5 \
        --max-nodes 8000
"""
from __future__ import annotations

import argparse
import json
import logging
import sys
from pathlib import Path
from typing import Any

logger = logging.getLogger("rosclaw.import_code_entities_fast")


def _is_public_api(name: str) -> bool:
    prefixes = ("get_", "set_", "compute_", "plan_", "execute_", "run_",
                "build_", "create_", "update_", "delete_", "search_",
                "generate_", "validate_", "parse_", "render_", "train_",
                "infer_", "predict_", "forward_", "backward_", "step_",
                "load_", "save_", "init_", "setup_", "configure_",
                "start_", "stop_", "reset_", "evaluate_", "transform_")
    return name.startswith(prefixes) or name == "__init__"


def calculate_centrality(graph: dict[str, Any]) -> dict[str, dict[str, Any]]:
    node_ids = {n["id"] for n in graph["nodes"]}
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
    centrality: dict[str, dict[str, Any]] = {}
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

    selected.sort(key=lambda n: (n["centrality"]["in_degree"], n["centrality"]["centrality_score"]), reverse=True)

    if max_nodes is not None and len(selected) > max_nodes:
        selected = selected[:max_nodes]

    return selected


def import_to_seekdb(nodes: list[dict[str, Any]], batch_size: int = 200) -> dict[str, Any]:
    sys.path.insert(0, str(Path(__file__).parent.parent))
    from seekdb_collection_client import get_wiki_collection
    import numpy as np
    from sentence_transformers import SentenceTransformer

    coll = get_wiki_collection()
    model = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")

    imported = 0
    errors = 0

    for i in range(0, len(nodes), batch_size):
        batch = nodes[i:i + batch_size]
        ids_batch: list[str] = []
        docs_batch: list[str] = []
        meta_batch: list[dict[str, Any]] = []

        for node in batch:
            nid = node["id"]
            docstring = node.get("docstring", "")
            centrality = node.get("centrality", {})
            doc_id = f"code_entity/{node.get('repo', 'unknown')}:{node.get('file', '')}:{node.get('name', '')}"
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

        # Compute embeddings in bulk
        try:
            texts = [d if d else node.get("name", "") for d, node in zip(docs_batch, batch)]
            embeddings = model.encode(texts, show_progress_bar=False).tolist()
            embeddings = [[round(float(x), 6) for x in emb] for emb in embeddings]

            coll.upsert(ids=ids_batch, documents=docs_batch, embeddings=embeddings, metadatas=meta_batch)
            imported += len(ids_batch)
            logger.info("Imported %d/%d code entities", imported, len(nodes))
        except Exception as exc:
            logger.warning("Batch import error: %s", exc)
            errors += len(ids_batch)

    logger.info("Import complete: %d imported, %d errors", imported, errors)
    return {"status": "done", "imported": imported, "errors": errors}


def main() -> int:
    parser = argparse.ArgumentParser(description="Fast import code entities to SeekDB")
    parser.add_argument("--input", default="data/code_graph.json")
    parser.add_argument("--centrality-threshold", type=int, default=5)
    parser.add_argument("--max-nodes", type=int, default=8000)
    parser.add_argument("--batch-size", type=int, default=200)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")

    path = Path(args.input)
    if not path.exists():
        logger.error("File not found: %s", args.input)
        return 1

    with path.open("r", encoding="utf-8") as f:
        graph = json.load(f)

    logger.info("Calculating centrality for %d nodes", len(graph["nodes"]))
    centrality = calculate_centrality(graph)

    selected = filter_high_value_nodes(
        graph, centrality,
        in_degree_threshold=args.centrality_threshold,
        max_nodes=args.max_nodes,
    )
    logger.info("Selected %d high-value nodes (external: %d, public_api: %d)",
                len(selected),
                sum(1 for n in selected if n.get("repo") != "rosclaw-wiki"),
                sum(1 for n in selected if n.get("is_public_api")))

    if args.dry_run:
        logger.info("Dry run: would import %d nodes", len(selected))
        return 0

    result = import_to_seekdb(selected, args.batch_size)
    print(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


__all__ = ["calculate_centrality", "filter_high_value_nodes", "import_to_seekdb"]
