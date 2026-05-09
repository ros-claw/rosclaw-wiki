"""ROSClaw Gap Visualizer — export heatmap data for knowledge gaps.

Consumes research_advisor output to produce gap_heatmap.json,
suitable for rendering in a Web UI.
"""

from __future__ import annotations

import json
import logging
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any

from graph_exporter import export_graph
from research_advisor import identify_knowledge_gaps

logger = logging.getLogger("rosclaw.gap_viz")


def generate_gap_heatmap(
    wiki_root: str,
    output_dir: str | None = None,
) -> Path:
    """Generate heatmap JSON data for knowledge gap visualization.

    Nodes represent topics/tags. Size reflects coverage (page count).
    Color reflects urgency (red = high priority gap).

    Returns:
        Path to the written gaps.json file.
    """
    gaps = identify_knowledge_gaps(wiki_root)

    out_dir = Path(output_dir or Path(wiki_root).parent / "data" / "graph_export")
    out_dir.mkdir(parents=True, exist_ok=True)

    # Tag coverage from graph nodes
    graph_result = export_graph(wiki_root, output_dir=str(out_dir), fmt="json")
    nodes_path = [p for p in graph_result["output_paths"] if "nodes.json" in p][0]
    nodes: list[dict[str, Any]] = json.loads(
        Path(nodes_path).read_text(encoding="utf-8")
    )

    all_tags: dict[str, list[str]] = defaultdict(list)
    for node in nodes:
        for tag in node.get("tags", []):
            all_tags[tag].append(node.get("label", node["id"]))

    # Determine urgency based on coverage
    heatmap_nodes: list[dict[str, Any]] = []
    low_density_tags = {t["tag"] for t in gaps.get("low_density_topics", [])}

    for tag, pages in all_tags.items():
        coverage = len(pages)
        if tag in low_density_tags:
            urgency = "high" if coverage == 1 else "medium"
        elif coverage < 5:
            urgency = "medium"
        else:
            urgency = "low"

        heatmap_nodes.append({
            "id": tag,
            "label": tag,
            "coverage": coverage,
            "urgency": urgency,
            "pages": pages[:10],
        })

    heatmap_data = {
        "nodes": heatmap_nodes,
        "metadata": {
            "total_nodes": gaps["total_nodes"],
            "total_edges": gaps["total_edges"],
            "isolated_count": len(gaps["isolated_nodes"]),
            "low_density_count": len(gaps["low_density_topics"]),
            "generated_at": datetime.now().isoformat(),
        },
    }

    gaps_path = out_dir / "gaps.json"
    gaps_path.write_text(
        json.dumps(heatmap_data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    logger.info("Gap heatmap written to %s", gaps_path)
    return gaps_path


__all__ = ["generate_gap_heatmap"]
