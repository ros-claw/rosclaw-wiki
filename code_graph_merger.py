"""Code Graph Merger — combine multiple code_graph*.json files into a unified graph.

Usage:
    python code_graph_merger.py --inputs data/code_graph*.json --output data/code_graph.json
    python code_graph_merger.py --inputs data/code_graph.json data/code_graph_batch2.json --output data/code_graph.json
"""

from __future__ import annotations

import argparse
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any

logger = logging.getLogger("rosclaw.code_graph_merger")


def merge_code_graphs(
    inputs: list[Path],
    output: Path,
    dedup_edges: bool = True,
) -> dict[str, Any]:
    """Merge multiple code_graph JSON files into a single graph.

    Deduplicates nodes by ``id`` and edges by ``(source, target, type)``.
    Later files override earlier ones for conflicting node IDs.

    Args:
        inputs: List of code_graph JSON file paths.
        output: Destination path for the merged graph.
        dedup_edges: If True, remove duplicate edges.

    Returns:
        Summary dict with node_count, edge_count, repo_count, output path.
    """
    all_nodes: dict[str, dict[str, Any]] = {}
    all_edges: list[dict[str, Any]] = []
    edge_keys: set[tuple[str, str, str]] = set()
    total_repo_count = 0

    for path in inputs:
        if not path.exists():
            logger.warning("Skipping missing file: %s", path)
            continue

        logger.info("Loading %s ...", path)
        with open(path, encoding="utf-8") as f:
            data = json.load(f)

        nodes = data.get("nodes", [])
        edges = data.get("edges", [])
        repo_count = data.get("repo_count", 0)

        total_repo_count += repo_count if isinstance(repo_count, int) else 0

        for node in nodes:
            node_id = node.get("id")
            if node_id:
                all_nodes[node_id] = node

        for edge in edges:
            s = edge.get("source", "")
            t = edge.get("target", "")
            tp = edge.get("type", "")
            if dedup_edges:
                key = (s, t, tp)
                if key in edge_keys:
                    continue
                edge_keys.add(key)
            all_edges.append(edge)

        logger.info("  + %d nodes, %d edges (repo_count=%s)", len(nodes), len(edges), repo_count)

    merged = {
        "nodes": list(all_nodes.values()),
        "edges": all_edges,
        "repo_count": total_repo_count,
        "node_count": len(all_nodes),
        "edge_count": len(all_edges),
        "generated_at": datetime.now().isoformat(),
        "source_files": [str(p) for p in inputs],
    }

    output.parent.mkdir(parents=True, exist_ok=True)
    with open(output, "w", encoding="utf-8") as f:
        json.dump(merged, f, ensure_ascii=False, indent=2)

    logger.info(
        "Merged graph written to %s: %d nodes, %d edges, %d repos",
        output, merged["node_count"], merged["edge_count"], total_repo_count,
    )

    return {
        "status": "done",
        "output": str(output),
        "node_count": merged["node_count"],
        "edge_count": merged["edge_count"],
        "repo_count": total_repo_count,
        "source_count": len(inputs),
    }


def aggregate_graph_stats(inputs: list[Path]) -> dict[str, Any]:
    """Aggregate statistics from multiple code_graph files without writing output.

    Used by API endpoints that need counts but don't need the merged file.
    """
    total_nodes = 0
    total_edges = 0
    total_repos = 0
    valid_files = 0

    for path in inputs:
        if not path.exists():
            continue
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        total_nodes += len(data.get("nodes", []))
        total_edges += len(data.get("edges", []))
        rc = data.get("repo_count", 0)
        total_repos += rc if isinstance(rc, int) else 0
        valid_files += 1

    return {
        "total_code_graph_nodes": total_nodes,
        "total_code_graph_edges": total_edges,
        "total_repos": total_repos,
        "files_scanned": valid_files,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Merge code_graph JSON files")
    parser.add_argument("--inputs", nargs="+", required=True, help="Input code_graph JSON files")
    parser.add_argument("--output", required=True, help="Output merged JSON file")
    parser.add_argument("--no-dedup-edges", action="store_true", help="Keep duplicate edges")
    parser.add_argument("--stats-only", action="store_true", help="Only print aggregated stats, do not write output")
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(message)s")

    input_paths = [Path(p) for p in args.inputs]

    if args.stats_only:
        result = aggregate_graph_stats(input_paths)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        result = merge_code_graphs(
            input_paths,
            Path(args.output),
            dedup_edges=not args.no_dedup_edges,
        )
        print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
