"""ROSClaw Research Advisor — self-reflection and knowledge gap identification.

Analyzes the knowledge graph to find isolated nodes, sparse connections,
and low-coverage topics, then generates actionable research suggestions.
"""

from __future__ import annotations

import json
import logging
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any

import wiki_engine as engine
from graph_exporter import export_graph

logger = logging.getLogger("rosclaw.advisor")


def _build_adjacency(nodes: list[dict[str, Any]], edges: list[dict[str, Any]]) -> dict[str, set[str]]:
    """Build undirected adjacency list from graph edges."""
    adj: dict[str, set[str]] = defaultdict(set)
    node_ids = {n["id"] for n in nodes}
    for e in edges:
        src = e.get("source", "")
        tgt = e.get("target", "")
        if src in node_ids and tgt in node_ids:
            adj[src].add(tgt)
            adj[tgt].add(src)
    return dict(adj)


def _degree_centrality(adj: dict[str, set[str]], total_nodes: int) -> dict[str, float]:
    """Compute degree centrality (degree / (N-1))."""
    if total_nodes <= 1:
        return {n: 0.0 for n in adj}
    return {n: len(neighbors) / (total_nodes - 1) for n, neighbors in adj.items()}


def _clustering_coefficient(adj: dict[str, set[str]]) -> dict[str, float]:
    """Compute local clustering coefficient for each node."""
    coeffs: dict[str, float] = {}
    for node, neighbors in adj.items():
        k = len(neighbors)
        if k < 2:
            coeffs[node] = 0.0
            continue
        edges_between = 0
        neighbor_list = list(neighbors)
        for i in range(len(neighbor_list)):
            for j in range(i + 1, len(neighbor_list)):
                if neighbor_list[j] in adj.get(neighbor_list[i], set()):
                    edges_between += 1
        max_edges = k * (k - 1) / 2
        coeffs[node] = edges_between / max_edges if max_edges > 0 else 0.0
    return coeffs


def identify_knowledge_gaps(wiki_root: str) -> dict[str, Any]:
    """Identify knowledge gaps in the wiki knowledge graph.

    Returns:
        Dict with isolated_nodes, sparse_connections, low_density_topics,
        total_nodes, total_edges.
    """
    graph_result = export_graph(wiki_root, output_dir=None, fmt="json")

    nodes_path = [p for p in graph_result["output_paths"] if "nodes.json" in p][0]
    edges_path = [p for p in graph_result["output_paths"] if "edges.json" in p][0]

    nodes: list[dict[str, Any]] = json.loads(Path(nodes_path).read_text(encoding="utf-8"))
    edges: list[dict[str, Any]] = json.loads(Path(edges_path).read_text(encoding="utf-8"))

    adj = _build_adjacency(nodes, edges)
    total_nodes = len(nodes)

    degree_cent = _degree_centrality(adj, total_nodes)
    clustering = _clustering_coefficient(adj)

    # 1. Isolated nodes: degree == 0
    connected_ids = {nid for nid, nbrs in adj.items() if nbrs}
    isolated: list[dict[str, Any]] = []
    for node in nodes:
        nid = node["id"]
        if nid not in connected_ids:
            isolated.append({
                "id": nid,
                "title": node.get("label", nid),
                "type": node.get("type", "unknown"),
                "path": node.get("path", ""),
            })

    # 2. Sparse connections: low degree, low clustering (potential bridges or gaps)
    sparse: list[dict[str, Any]] = []
    isolated_ids = {i["id"] for i in isolated}
    for node in nodes:
        nid = node["id"]
        if nid in isolated_ids:
            continue
        deg = degree_cent.get(nid, 0)
        clust = clustering.get(nid, 0)
        if deg < 0.1 and clust < 0.3:
            sparse.append({
                "id": nid,
                "title": node.get("label", nid),
                "degree": round(deg, 3),
                "clustering": round(clust, 3),
            })

    # 3. Low-density topics: tags with < 3 pages
    tag_counts: dict[str, list[str]] = defaultdict(list)
    for node in nodes:
        for tag in node.get("tags", []):
            tag_counts[tag].append(node.get("label", node["id"]))

    low_density = [
        {"tag": tag, "pages": pages, "count": len(pages)}
        for tag, pages in tag_counts.items()
        if len(pages) < 3
    ]
    low_density.sort(key=lambda x: x["count"])

    return {
        "isolated_nodes": isolated,
        "sparse_connections": sparse,
        "low_density_topics": low_density,
        "total_nodes": total_nodes,
        "total_edges": len(edges),
    }


def generate_research_suggestions(gaps: dict[str, Any]) -> list[dict[str, Any]]:
    """Generate actionable research suggestions from identified gaps."""
    suggestions: list[dict[str, Any]] = []

    for node in gaps.get("isolated_nodes", [])[:10]:
        suggestions.append({
            "priority": "medium",
            "type": "isolated_knowledge",
            "title": node["title"],
            "message": (
                f"页面 '{node['title']}' 没有被任何其他页面引用。"
                "建议添加与其他概念的关联链接。"
            ),
            "search_keywords": [node["title"], f"{node['title']} related work"],
        })

    for topic in gaps.get("low_density_topics", [])[:10]:
        priority = "high" if topic["count"] == 1 else "medium"
        suggestions.append({
            "priority": priority,
            "type": "low_coverage",
            "tag": topic["tag"],
            "message": (
                f"主题 '{topic['tag']}' 仅有 {topic['count']} 个页面覆盖，"
                "知识密度不足。建议调研更多相关文献。"
            ),
            "search_keywords": [topic["tag"], f"{topic['tag']} survey"],
        })

    for node in gaps.get("sparse_connections", [])[:10]:
        suggestions.append({
            "priority": "low",
            "type": "sparse_connection",
            "title": node["title"],
            "message": (
                f"'{node['title']}' 连接度低（degree={node['degree']}），"
                "可能是知识空白区域。"
            ),
            "search_keywords": [node["title"]],
        })

    return suggestions


def generate_weekly_report(
    wiki_root: str,
    output_dir: str | None = None,
) -> Path:
    """Generate a weekly knowledge gap report and append to log.

    Returns:
        Path to the written report file.
    """
    gaps = identify_knowledge_gaps(wiki_root)
    suggestions = generate_research_suggestions(gaps)

    out_dir = Path(output_dir or Path(wiki_root).parent / "data" / "quality_reports")
    out_dir.mkdir(parents=True, exist_ok=True)

    date_str = datetime.now().strftime("%Y-%m-%d")
    report_path = out_dir / f"weekly_advisor_{date_str}.md"

    lines: list[str] = [
        "# 每周知识空白报告\n",
        f"**生成日期**: {datetime.now().isoformat()}\n",
        f"**Wiki 总节点数**: {gaps['total_nodes']} | **总边数**: {gaps['total_edges']}\n",
        f"**发现空白数**: {len(suggestions)}\n\n",
        "## 知识空白列表\n\n",
    ]

    for i, s in enumerate(suggestions, 1):
        name = s.get("title") or s.get("tag", "")
        lines.append(f"### {i}. [{s['priority'].upper()}] {name}\n")
        lines.append(f"- **类型**: {s['type']}\n")
        lines.append(f"- **描述**: {s['message']}\n")
        lines.append(f"- **建议搜索关键词**: {', '.join(s['search_keywords'])}\n\n")

    if gaps["isolated_nodes"]:
        lines.append("## 孤立节点详情\n\n")
        lines.append("| 标题 | 类型 | 路径 |\n")
        lines.append("|------|------|------|\n")
        for node in gaps["isolated_nodes"]:
            lines.append(f"| {node['title']} | {node['type']} | {node['path']} |\n")
        lines.append("\n")

    if gaps["low_density_topics"]:
        lines.append("## 低密度主题详情\n\n")
        lines.append("| 主题标签 | 页面数 | 相关页面 |\n")
        lines.append("|----------|--------|----------|\n")
        for topic in gaps["low_density_topics"]:
            pages_str = ", ".join(topic["pages"][:5])
            lines.append(f"| {topic['tag']} | {topic['count']} | {pages_str} |\n")
        lines.append("\n")

    report_path.write_text("".join(lines), encoding="utf-8")

    engine.append_log(
        wiki_root,
        (
            f"advisor | weekly_report | gaps_found: {len(suggestions)} | "
            f"isolated: {len(gaps['isolated_nodes'])} | "
            f"low_density: {len(gaps['low_density_topics'])}"
        ),
    )

    logger.info("Weekly advisor report written to %s", report_path)
    return report_path


__all__ = [
    "identify_knowledge_gaps",
    "generate_research_suggestions",
    "generate_weekly_report",
]
