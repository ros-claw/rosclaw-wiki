"""Physics Grounding — bridge code constants to Wiki physical judgments.

Inspired by GitNexus's "code as graph" + Graphify's cross-domain alignment:
  1. Scan code for physical constants (AST-based, tree-sitter ready)
  2. Search Wiki judgments for matching parameters
  3. Establish CONSTRAINT_BY edges with sync status
  4. BFS context pruning for token-efficient impact analysis

Edge type: CONSTRAINT_BY(code_constant → wiki_judgment)
"""

from __future__ import annotations

import ast
import json
import logging
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

logger = logging.getLogger("rosclaw.physics_grounding")


# ── Physical constant heuristics ──

_PHYSICS_KEYWORDS = [
    "TORQUE", "VELOCITY", "SPEED", "FORCE", "ACCEL",
    "MAX_", "MIN_", "SAFETY_", "LIMIT_", "NOMINAL_",
    "THRESHOLD", "BOUNDARY", "RANGE", "CAPACITY",
    "HEIGHT", "WIDTH", "DEPTH", "MASS", "WEIGHT",
    "VOLTAGE", "CURRENT", "POWER", "BATTERY",
    "TEMPERATURE", "PRESSURE", "FREQUENCY", "HZ",
]

_PHYS_UNITS_RE = re.compile(
    r"(?i)(N·m|Nm|kg|Hz|m/s|rad/s|deg|°|A|V|W|N|Pa|K|m|s|ms|us|mm|cm|km|g|mg)"
)


@dataclass
class PhysicalConstant:
    """A physical constant discovered in code."""

    name: str
    value: Any
    value_repr: str
    unit: str
    file: str
    repo: str
    lineno: int
    node_id: str
    scope: str = "module"          # module | class | function
    source_line: str = ""
    docstring_hint: str = ""       # e.g. "# max torque in N·m"

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "value": self.value,
            "value_repr": self.value_repr,
            "unit": self.unit,
            "file": self.file,
            "repo": self.repo,
            "lineno": self.lineno,
            "node_id": self.node_id,
            "scope": self.scope,
            "source_line": self.source_line,
            "docstring_hint": self.docstring_hint,
        }


@dataclass
class ConstraintEdge:
    """A CONSTRAINT_BY edge linking a code constant to a Wiki judgment."""

    source: str                      # code constant node_id
    target: str                      # wiki judgment key "entity:context:param"
    constant_name: str
    parameter: str
    entity: str
    code_value: Any
    judgment_value: Any
    unit: str
    confidence: float
    sync_status: str                 # "in_sync" | "outdated" | "unknown"
    deviation_pct: float | None

    def to_dict(self) -> dict[str, Any]:
        return {
            "source": self.source,
            "target": self.target,
            "type": "CONSTRAINT_BY",
            "constant_name": self.constant_name,
            "parameter": self.parameter,
            "entity": self.entity,
            "code_value": self.code_value,
            "judgment_value": self.judgment_value,
            "unit": self.unit,
            "confidence": self.confidence,
            "sync_status": self.sync_status,
            "deviation_pct": self.deviation_pct,
        }


# ── AST-based constant extraction (tree-sitter ready design) ──

def _is_physics_name(name: str) -> bool:
    """Check if a constant name matches physics keywords."""
    upper = name.upper()
    return any(kw in upper for kw in _PHYSICS_KEYWORDS)


def _extract_unit_from_comment(line: str) -> str:
    """Try to find a physical unit in a comment or inline text.

    Prefers the longest/most specific match to avoid single-char false positives.
    """
    matches = _PHYS_UNITS_RE.findall(line)
    if not matches:
        return ""
    # Pick longest match; prefer compound units over single letters
    return max(matches, key=len)


def _extract_constant_value(node: ast.AST) -> tuple[Any, str]:
    """Extract a Python literal value from an AST assignment node."""
    value_node: ast.AST | None = None
    if isinstance(node, ast.Assign):
        value_node = node.value
    elif isinstance(node, ast.AnnAssign):
        value_node = node.value

    if value_node is None:
        return None, ""

    if isinstance(value_node, ast.Constant):
        return value_node.value, repr(value_node.value)
    if isinstance(value_node, ast.Num):          # Python < 3.8 compat
        return value_node.n, repr(value_node.n)
    if isinstance(value_node, ast.UnaryOp):
        if isinstance(value_node.op, ast.USub):
            inner, _ = _extract_constant_value(ast.Assign(value=[value_node.operand]))
            if inner is not None:
                return -inner, repr(-inner)
    if isinstance(value_node, ast.BinOp):
        # Simple cases like 3.6 * 1000
        left, _ = _extract_constant_value(ast.Assign(value=[value_node.left]))
        right, _ = _extract_constant_value(ast.Assign(value=[value_node.right]))
        if left is not None and right is not None:
            if isinstance(value_node.op, ast.Mult):
                return left * right, f"{left}*{right}"
            if isinstance(value_node.op, ast.Div):
                return left / right if right != 0 else None, f"{left}/{right}"
    return None, ""


def _get_source_line(source: str, lineno: int) -> str:
    """Extract a specific line from source code."""
    lines = source.splitlines()
    if 1 <= lineno <= len(lines):
        return lines[lineno - 1]
    return ""


def scan_file_for_constants(
    file_path: Path,
    repo_name: str,
    source: str | None = None,
) -> list[PhysicalConstant]:
    """Scan a single Python file for physical constants.

    Returns:
        List of PhysicalConstant objects.
    """
    if source is None:
        try:
            source = file_path.read_text(encoding="utf-8", errors="ignore")
        except Exception as exc:
            logger.warning("Cannot read %s: %s", file_path, exc)
            return []

    try:
        tree = ast.parse(source)
    except SyntaxError:
        return []

    rel = str(file_path.relative_to(file_path.parent.parent)) if file_path.parent.parent else file_path.name
    constants: list[PhysicalConstant] = []

    def _scan_body(body: list[ast.stmt], scope: str, parent_id: str) -> None:
        for node in body:
            if isinstance(node, (ast.Assign, ast.AnnAssign)):
                targets: list[str] = []
                if isinstance(node, ast.Assign):
                    for t in node.targets:
                        if isinstance(t, ast.Name) and _is_physics_name(t.id):
                            targets.append(t.id)
                elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
                    if _is_physics_name(node.target.id):
                        targets.append(node.target.id)

                for name in targets:
                    val, val_repr = _extract_constant_value(node)
                    if val is None:
                        continue
                    line = _get_source_line(source, node.lineno)
                    unit = _extract_unit_from_comment(line)
                    node_id = f"{repo_name}:{rel}:{name}"
                    constants.append(
                        PhysicalConstant(
                            name=name,
                            value=val,
                            value_repr=val_repr,
                            unit=unit,
                            file=rel,
                            repo=repo_name,
                            lineno=node.lineno,
                            node_id=node_id,
                            scope=scope,
                            source_line=line.strip(),
                            docstring_hint=unit,
                        )
                    )

            elif isinstance(node, ast.ClassDef):
                class_id = f"{repo_name}:{rel}:{node.name}"
                _scan_body(list(node.body), "class", class_id)
            elif isinstance(node, ast.FunctionDef):
                func_id = f"{repo_name}:{rel}:{node.name}"
                _scan_body(list(node.body), "function", func_id)

    _scan_body(list(ast.iter_child_nodes(tree)), "module", f"{repo_name}:{rel}")
    return constants


def _scan_file_for_constants_ts(
    file_path: Path,
    repo_name: str,
) -> list[PhysicalConstant]:
    """Scan a non-Python file for physical constants using tree-sitter.

    Returns:
        List of PhysicalConstant objects.
    """
    try:
        from tree_sitter_parser import parse_code_file
    except ImportError:
        return []

    result = parse_code_file(str(file_path))
    if "error" in result:
        return []

    rel = str(file_path.relative_to(file_path.parent.parent)) if file_path.parent.parent else file_path.name
    constants: list[PhysicalConstant] = []

    for const in result.get("constants", []):
        name = const["name"]
        if not _is_physics_name(name):
            continue
        node_id = f"{repo_name}:{rel}:{name}"
        constants.append(
            PhysicalConstant(
                name=name,
                value=None,
                value_repr="",
                unit="",
                file=rel,
                repo=repo_name,
                lineno=const.get("lineno", 0),
                node_id=node_id,
                scope="module",
                source_line="",
                docstring_hint="",
            )
        )

    return constants


def scan_repo_for_constants(repo_path: Path, repo_name: str | None = None) -> list[PhysicalConstant]:
    """Scan an entire repository for physical constants.

    Uses Python ast for .py files and tree-sitter for all other supported languages.
    """
    if repo_name is None:
        repo_name = repo_path.name

    constants: list[PhysicalConstant] = []
    supported_exts = {".py", ".cpp", ".cc", ".cxx", ".c", ".rs", ".go", ".ts", ".js", ".h", ".hpp"}

    for code_file in repo_path.rglob("*"):
        if not code_file.is_file():
            continue
        if code_file.suffix.lower() not in supported_exts:
            continue
        if "/venv/" in str(code_file) or "/.venv/" in str(code_file) or "/__pycache__/" in str(code_file):
            continue

        if code_file.suffix.lower() == ".py":
            constants.extend(scan_file_for_constants(code_file, repo_name))
        else:
            constants.extend(_scan_file_for_constants_ts(code_file, repo_name))

    return constants


# ── Wiki judgment matching ──

def load_judgment_index(wiki_root: str = "wiki") -> dict[str, Any]:
    """Load the unified judgment index."""
    path = Path(wiki_root) / "judgments" / "index.json"
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        logger.warning("Failed to load judgment index: %s", exc)
        return {}


def _normalize_name(name: str) -> str:
    """Normalize a constant name for fuzzy matching."""
    # MAX_TORQUE → max_torque, MaxTorque → max_torque
    result = name.lower()
    # Remove common prefixes
    for prefix in ("max_", "min_", "safety_", "limit_", "nominal_"):
        if result.startswith(prefix):
            result = result[len(prefix):]
            break
    return result


def match_constant_to_judgments(
    constant: PhysicalConstant,
    judgment_index: dict[str, Any],
) -> list[ConstraintEdge]:
    """Find matching Wiki judgments for a physical constant.

    Returns:
        List of ConstraintEdge objects (may be empty).
    """
    edges: list[ConstraintEdge] = []
    norm_name = _normalize_name(constant.name)

    by_entity = judgment_index.get("by_entity", {})
    for entity, contexts in by_entity.items():
        for context, params in contexts.items():
            for param, info in params.items():
                # Fuzzy match: normalized names overlap
                norm_param = _normalize_name(param)
                if norm_name == norm_param or norm_name in norm_param or norm_param in norm_name:
                    j_val = info.get("recommended_value")
                    hw_limit = info.get("hardware_limit")
                    unit = info.get("unit", constant.unit)

                    code_val = _try_numeric(constant.value)
                    judgment_val = _try_numeric(j_val)

                    sync_status = "unknown"
                    deviation = None
                    if code_val is not None and judgment_val is not None and judgment_val != 0:
                        deviation = ((code_val - judgment_val) / abs(judgment_val)) * 100
                        if abs(deviation) <= 5:
                            sync_status = "in_sync"
                        else:
                            sync_status = "outdated"

                    target = f"{entity}:{context}:{param}"
                    edges.append(
                        ConstraintEdge(
                            source=constant.node_id,
                            target=target,
                            constant_name=constant.name,
                            parameter=param,
                            entity=entity,
                            code_value=constant.value,
                            judgment_value=j_val,
                            unit=unit,
                            confidence=info.get("confidence", 0.0),
                            sync_status=sync_status,
                            deviation_pct=deviation,
                        )
                    )

    return edges


def _try_numeric(val: Any) -> float | None:
    """Try to coerce a value to float."""
    if val is None:
        return None
    if isinstance(val, (int, float)):
        return float(val)
    try:
        return float(val)
    except (ValueError, TypeError):
        return None


# ── Graph integration ──

def build_constraint_edges(
    code_root: str = "data/raw/code",
    wiki_root: str = "wiki",
) -> list[dict[str, Any]]:
    """Build all CONSTRAINT_BY edges across all repos.

    Returns:
        List of edge dicts ready for the code graph.
    """
    index = load_judgment_index(wiki_root)
    if not index:
        logger.info("No judgment index found; skipping constraint edges.")
        return []

    root = Path(code_root)
    all_edges: list[dict[str, Any]] = []

    if not root.exists():
        return all_edges

    for repo_dir in root.iterdir():
        if not repo_dir.is_dir() or repo_dir.name.startswith("."):
            continue
        constants = scan_repo_for_constants(repo_dir)
        for c in constants:
            matches = match_constant_to_judgments(c, index)
            for edge in matches:
                all_edges.append(edge.to_dict())

    return all_edges


def enrich_code_graph_with_constraints(
    graph: dict[str, Any],
    code_root: str = "data/raw/code",
    wiki_root: str = "wiki",
) -> dict[str, Any]:
    """Add CONSTRAINT_BY edges and constant nodes to an existing code graph.

    Returns:
        Enriched graph dict.
    """
    constraint_edges = build_constraint_edges(code_root, wiki_root)

    # Add constant nodes if not already present
    existing_ids = {n["id"] for n in graph.get("nodes", [])}
    new_nodes: list[dict[str, Any]] = []

    for edge in constraint_edges:
        const_id = edge["source"]
        if const_id not in existing_ids:
            existing_ids.add(const_id)
            new_nodes.append({
                "id": const_id,
                "type": "constant",
                "name": edge["constant_name"],
                "repo": const_id.split(":")[0] if ":" in const_id else "",
                "file": ":".join(const_id.split(":")[1:-1]) if ":" in const_id else "",
                "lineno": 0,
                "docstring": f"Physical constant constrained by {edge['target']}",
            })

    graph["nodes"] = graph.get("nodes", []) + new_nodes
    graph["edges"] = graph.get("edges", []) + constraint_edges
    graph["constraint_edge_count"] = len(constraint_edges)
    graph["constant_node_count"] = len(new_nodes)

    return graph


# ── Context pruning (BFS) ──

def bfs_related_nodes(
    start_node_id: str,
    graph: dict[str, Any],
    max_depth: int = 2,
    edge_types: list[str] | None = None,
) -> dict[str, Any]:
    """BFS from a start node to find related nodes within max_depth hops.

    Inspired by Graphify's graph search for token compression.
    Returns a subgraph with only the relevant nodes and edges.

    Args:
        start_node_id: Node ID to start from.
        graph: Full code graph.
        max_depth: Maximum BFS depth (default 2).
        edge_types: Edge types to traverse (default all).

    Returns:
        Subgraph dict with "nodes" and "edges".
    """
    if edge_types is None:
        edge_types = ["calls", "CONSTRAINT_BY"]

    all_nodes = {n["id"]: n for n in graph.get("nodes", [])}
    all_edges = graph.get("edges", [])

    visited: set[str] = {start_node_id}
    frontier: set[str] = {start_node_id}
    result_edges: list[dict[str, Any]] = []

    for _ in range(max_depth):
        next_frontier: set[str] = set()
        for edge in all_edges:
            if edge.get("type") not in edge_types:
                continue
            src = edge.get("source", "")
            tgt = edge.get("target", "")
            if src in frontier and tgt not in visited:
                visited.add(tgt)
                next_frontier.add(tgt)
                result_edges.append(edge)
            elif tgt in frontier and src not in visited:
                visited.add(src)
                next_frontier.add(src)
                result_edges.append(edge)
        frontier = next_frontier
        if not frontier:
            break

    result_nodes = [all_nodes[nid] for nid in visited if nid in all_nodes]
    return {
        "nodes": result_nodes,
        "edges": result_edges,
        "start_node": start_node_id,
        "max_depth": max_depth,
        "node_count": len(result_nodes),
        "edge_count": len(result_edges),
    }


def code_physics_impact(
    constant_name: str,
    graph: dict[str, Any] | None = None,
    wiki_root: str = "wiki",
) -> dict[str, Any]:
    """MCP-style tool: given a code constant name, return impact analysis.

    Returns:
        Dict with:
          - matching_constants: list of constant nodes
          - constraints: list of CONSTRAINT_BY edges
          - affected_functions: list of function nodes within 2 hops
          - sync_summary: dict of in_sync/outdated/unknown counts
    """
    if graph is None:
        from code_knowledge_graph import load_code_graph
        graph = load_code_graph()

    # Find constant nodes matching the name
    matching_constants = [
        n for n in graph.get("nodes", [])
        if n.get("type") == "constant" and constant_name.lower() in n.get("name", "").lower()
    ]

    constraints: list[dict[str, Any]] = []
    affected_functions: list[dict[str, Any]] = []
    sync_counts = {"in_sync": 0, "outdated": 0, "unknown": 0}

    for const_node in matching_constants:
        cid = const_node["id"]
        # Find CONSTRAINT_BY edges
        for edge in graph.get("edges", []):
            if edge.get("type") == "CONSTRAINT_BY" and edge.get("source") == cid:
                constraints.append(edge)
                sync_counts[edge.get("sync_status", "unknown")] += 1

        # BFS for affected functions
        subgraph = bfs_related_nodes(cid, graph, max_depth=2, edge_types=["calls", "CONSTRAINT_BY"])
        for node in subgraph.get("nodes", []):
            if node.get("type") == "function" and node not in affected_functions:
                affected_functions.append(node)

    return {
        "constant_name": constant_name,
        "matching_constants": matching_constants,
        "constraints": constraints,
        "constraint_count": len(constraints),
        "affected_functions": affected_functions,
        "affected_function_count": len(affected_functions),
        "sync_summary": sync_counts,
    }


# ── Code topology mining (Phase 16 Module 2A) ──

def mine_code_topology(file_path: str) -> list[dict[str, Any]]:
    """Mine CO_OCCURS and LATENCY_SENSITIVE relationships from code.

    Uses tree-sitter to scan functions and extract:
      - Variable co-occurrences within the same function scope
      - Latency-sensitive patterns (sleep, timer, callback)

    Returns:
        List of edge dicts with source, target, type, metadata.
    """
    edges: list[dict[str, Any]] = []
    try:
        from tree_sitter_parser import parse_code_file
    except ImportError:
        return edges

    result = parse_code_file(file_path)
    if "error" in result:
        return edges

    # For each function, look at calls to infer co-occurrence
    functions = result.get("functions", [])
    calls = result.get("calls", [])

    # Group calls by function (approximate: calls between function boundaries)
    # Since tree-sitter queries don't give parent function info directly,
    # we use all calls in the file and create pairwise co-occurrences
    call_targets = [c["target"] for c in calls if not c["target"].startswith("_")]

    # CO_OCCURS: every pair of calls in the same file
    if len(call_targets) >= 2:
        from itertools import combinations
        seen_pairs: set[tuple[str, str]] = set()
        for t1, t2 in combinations(call_targets, 2):
            pair = tuple(sorted((t1, t2)))
            if pair in seen_pairs:
                continue
            seen_pairs.add(pair)
            edges.append({
                "source": pair[0],
                "target": pair[1],
                "type": "CO_OCCURS",
                "context": Path(file_path).name,
                "metadata": {"file": file_path},
            })

    # LATENCY_SENSITIVE: detect sleep/timer patterns
    latency_keywords = {"sleep", "usleep", "nanosleep", "wall_timer", "timer", "delay", "wait"}
    for func in functions:
        func_name = func["name"]
        func_calls = [c for c in calls if c.get("lineno", 0) >= func.get("lineno", 0)]
        for c in func_calls:
            if any(kw in c["target"].lower() for kw in latency_keywords):
                edges.append({
                    "source": func_name,
                    "target": "control_loop",
                    "type": "LATENCY_SENSITIVE",
                    "context": Path(file_path).name,
                    "metadata": {"pattern": c["target"], "file": file_path},
                })
                break  # one latency flag per function is enough

    return edges


# ── High-level convenience ──

def build_full_grounded_graph(
    code_root: str = "data/raw/code",
    wiki_root: str = "wiki",
    output_path: str = "data/code_graph.json",
) -> dict[str, Any]:
    """Build the complete code graph enriched with physical constraints.

    Returns:
        Enriched graph dict.
    """
    from code_knowledge_graph import build_code_graph

    graph = build_code_graph(code_root, output_path)
    enriched = enrich_code_graph_with_constraints(graph, code_root, wiki_root)

    # Save back
    Path(output_path).write_text(
        json.dumps(enriched, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    logger.info(
        "Grounded graph: %d nodes, %d edges (%d constraint edges)",
        enriched["node_count"],
        enriched["edge_count"],
        enriched.get("constraint_edge_count", 0),
    )
    return enriched
