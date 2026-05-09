"""ROSClaw Knowledge Graph Exporter — convert wiki pages to graph formats.

Parses YAML frontmatter and [[wikilink]] syntax to produce
structured node/edge data for visualization libraries.
"""

from __future__ import annotations

import json
import logging
import re
from pathlib import Path
from typing import Any

import wiki_engine as engine

logger = logging.getLogger("rosclaw.graph")

# Wikilink pattern: [[Page Name]] or [[Page Name|display text]]
_WIKILINK_RE = re.compile(r"\[\[([^\]|]+)(?:\|[^\]]+)?\]\]")


def _extract_wikilinks(body: str) -> list[str]:
    """Extract all [[Page Name]] wikilink targets from markdown body."""
    matches = _WIKILINK_RE.findall(body)
    # Normalize: strip whitespace, title case for consistency
    return [m.strip() for m in matches]


def _title_to_id(title: str) -> str:
    """Generate a graph-safe node ID from a title."""
    return engine.generate_page_id(title)


def export_graph(wiki_root: str, output_dir: str | None = None, fmt: str = "json") -> dict[str, Any]:
    """Export wiki pages as a knowledge graph.

    Args:
        wiki_root: Path to wiki root directory.
        output_dir: Directory to write output files. Defaults to wiki_root/../data/graph_export.
        fmt: Output format — "json", "sigma", or "cytoscape".

    Returns:
        Summary dict with node_count, edge_count, output_paths.
    """
    root = Path(wiki_root)
    out_dir = Path(output_dir) if output_dir else root.parent / "data" / "graph_export"
    out_dir.mkdir(parents=True, exist_ok=True)

    nodes: list[dict[str, Any]] = []
    edges: list[dict[str, Any]] = []
    node_ids: set[str] = set()
    edge_keys: set[tuple[str, str]] = set()

    for md_file in root.rglob("*.md"):
        if md_file.name in ("index.md", "log.md", "Admin_Dashboard.md"):
            continue
        try:
            content = md_file.read_text(encoding="utf-8")
            meta, body = engine.parse_frontmatter(content)
        except Exception as exc:
            logger.warning("Failed to parse %s for graph export: %s", md_file, exc)
            continue

        title = meta.get("title", md_file.stem)
        node_id = _title_to_id(title)
        if node_id in node_ids:
            # Skip duplicates (shouldn't happen with proper wiki hygiene)
            continue
        node_ids.add(node_id)

        node = {
            "id": node_id,
            "label": title,
            "type": meta.get("type", "unknown"),
            "confidence": meta.get("confidence", 0.5),
            "tags": meta.get("tags", []),
            "path": str(md_file.relative_to(root)),
        }
        nodes.append(node)

        # Extract wikilinks as edges
        for target_title in _extract_wikilinks(body):
            target_id = _title_to_id(target_title)
            edge_key = (node_id, target_id)
            if edge_key not in edge_keys:
                edge_keys.add(edge_key)
                edges.append({
                    "source": node_id,
                    "target": target_id,
                    "type": "wikilink",
                })

    # Write format-specific outputs
    output_paths: list[str] = []

    if fmt == "json":
        nodes_path = out_dir / "nodes.json"
        edges_path = out_dir / "edges.json"
        nodes_path.write_text(json.dumps(nodes, ensure_ascii=False, indent=2), encoding="utf-8")
        edges_path.write_text(json.dumps(edges, ensure_ascii=False, indent=2), encoding="utf-8")
        output_paths = [str(nodes_path), str(edges_path)]

    elif fmt == "sigma":
        sigma_data = {
            "nodes": [
                {
                    "key": n["id"],
                    "attributes": {
                        "label": n["label"],
                        "type": n["type"],
                        "confidence": n["confidence"],
                        "tags": n["tags"],
                    },
                }
                for n in nodes
            ],
            "edges": [
                {
                    "key": f"e{i}",
                    "source": e["source"],
                    "target": e["target"],
                    "attributes": {"type": e["type"]},
                }
                for i, e in enumerate(edges)
            ],
        }
        sigma_path = out_dir / "sigma.json"
        sigma_path.write_text(json.dumps(sigma_data, ensure_ascii=False, indent=2), encoding="utf-8")
        output_paths = [str(sigma_path)]

    elif fmt == "cytoscape":
        cy_elements = []
        for n in nodes:
            cy_elements.append({
                "data": {
                    "id": n["id"],
                    "label": n["label"],
                    "type": n["type"],
                    "confidence": n["confidence"],
                    "tags": n["tags"],
                },
            })
        for e in edges:
            cy_elements.append({
                "data": {
                    "source": e["source"],
                    "target": e["target"],
                    "type": e["type"],
                },
            })
        cy_path = out_dir / "cytoscape.json"
        cy_path.write_text(json.dumps(cy_elements, ensure_ascii=False, indent=2), encoding="utf-8")
        output_paths = [str(cy_path)]

    else:
        raise ValueError(f"Unknown graph format: {fmt}. Use 'json', 'sigma', or 'cytoscape'.")

    logger.info("Graph exported: %d nodes, %d edges, format=%s", len(nodes), len(edges), fmt)
    return {
        "status": "done",
        "format": fmt,
        "node_count": len(nodes),
        "edge_count": len(edges),
        "output_paths": output_paths,
    }
