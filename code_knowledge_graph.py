"""Code Knowledge Graph — AST-based call graph extraction for Phase 10.

Extracts classes, functions, constants and call relationships from Python code.
Stores to data/code_graph.json for visualization and code-aware generation.
"""

from __future__ import annotations

import ast
import json
import logging
from pathlib import Path
from typing import Any

logger = logging.getLogger("rosclaw.code_graph")


def _is_internal_module(node: ast.AST) -> bool:
    """Check if a call/attribute chain refers to a module-level import."""
    if isinstance(node, ast.Name):
        return True
    if isinstance(node, ast.Attribute):
        return _is_internal_module(node.value)
    return False


def _get_call_name(node: ast.Call) -> str:
    """Extract dotted name from a Call node, e.g. 'self.foo' or 'module.bar'."""
    if isinstance(node.func, ast.Name):
        return node.func.id
    if isinstance(node.func, ast.Attribute):
        parts: list[str] = []
        n = node.func
        while isinstance(n, ast.Attribute):
            parts.append(n.attr)
            n = n.value
        if isinstance(n, ast.Name):
            parts.append(n.id)
        return ".".join(reversed(parts))
    return ""


def _extract_node_info(node: ast.AST, source_file: str, repo_name: str) -> dict[str, Any] | None:
    """Extract a node dict for classes, functions, or assignments."""
    if isinstance(node, ast.ClassDef):
        return {
            "id": f"{repo_name}:{source_file}:{node.name}",
            "type": "class",
            "name": node.name,
            "file": source_file,
            "repo": repo_name,
            "lineno": node.lineno,
            "docstring": (ast.get_docstring(node) or "")[:300],
        }
    if isinstance(node, ast.FunctionDef) and not node.name.startswith("_"):
        return {
            "id": f"{repo_name}:{source_file}:{node.name}",
            "type": "function",
            "name": node.name,
            "file": source_file,
            "repo": repo_name,
            "lineno": node.lineno,
            "docstring": (ast.get_docstring(node) or "")[:300],
        }
    if isinstance(node, (ast.Assign, ast.AnnAssign)):
        # Constants at module level
        targets = []
        if isinstance(node, ast.Assign):
            for t in node.targets:
                if isinstance(t, ast.Name) and t.id.isupper():
                    targets.append(t.id)
        elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name) and node.target.id.isupper():
            targets.append(node.target.id)
        if targets:
            return {
                "id": f"{repo_name}:{source_file}:{targets[0]}",
                "type": "constant",
                "name": targets[0],
                "file": source_file,
                "repo": repo_name,
                "lineno": node.lineno,
                "docstring": "",
            }
    return None


def _extract_calls(node: ast.AST, parent_id: str) -> list[dict[str, Any]]:
    """Extract call edges from an AST node."""
    edges: list[dict[str, Any]] = []
    for child in ast.walk(node):
        if isinstance(child, ast.Call):
            call_name = _get_call_name(child)
            if call_name and not call_name.startswith("_"):
                edges.append({
                    "source": parent_id,
                    "target": call_name,
                    "type": "calls",
                    "lineno": child.lineno,
                })
    return edges


def scan_repo(repo_path: Path, repo_name: str | None = None) -> dict[str, Any]:
    """Scan a single repository and return nodes + edges.

    Uses Python ast for .py files and tree-sitter for other languages.
    Returns:
        Dict with "nodes" (list) and "edges" (list).
    """
    if repo_name is None:
        repo_name = repo_path.name

    nodes: list[dict[str, Any]] = []
    edges: list[dict[str, Any]] = []

    # Phase 15: scan all supported code files
    supported_exts = {".py", ".cpp", ".cc", ".cxx", ".c", ".rs", ".go", ".ts", ".js", ".h", ".hpp"}

    for code_file in repo_path.rglob("*"):
        if not code_file.is_file():
            continue
        if code_file.suffix.lower() not in supported_exts:
            continue
        rel = str(code_file.relative_to(repo_path))
        # Skip virtualenv
        if "/venv/" in str(code_file) or "/.venv/" in str(code_file) or "/__pycache__/" in str(code_file):
            continue

        if code_file.suffix.lower() == ".py":
            # Python: use built-in ast
            try:
                source = code_file.read_text(encoding="utf-8", errors="ignore")
                tree = ast.parse(source)
            except (SyntaxError, UnicodeDecodeError):
                continue
            except Exception as exc:
                logger.warning("Parse error in %s: %s", code_file, exc)
                continue

            def _scan_module(node_list: list[ast.AST], parent_id: str | None = None) -> None:
                for node in node_list:
                    info = _extract_node_info(node, rel, repo_name)
                    if info:
                        nodes.append(info)
                        edges.extend(_extract_calls(node, info["id"]))
                        # Recurse into class bodies
                        if isinstance(node, ast.ClassDef):
                            _scan_module(list(node.body), info["id"])

            _scan_module(list(ast.iter_child_nodes(tree)))
        else:
            # Non-Python: use tree-sitter
            try:
                from tree_sitter_parser import parse_code_file
                result = parse_code_file(str(code_file))
                if "error" in result:
                    continue

                for func in result.get("functions", []):
                    fid = f"{repo_name}:{rel}:{func['name']}"
                    nodes.append({
                        "id": fid,
                        "type": "function",
                        "name": func["name"],
                        "file": rel,
                        "repo": repo_name,
                        "lineno": func.get("lineno", 0),
                        "docstring": "",
                    })

                for cls in result.get("classes", []):
                    cid = f"{repo_name}:{rel}:{cls['name']}"
                    nodes.append({
                        "id": cid,
                        "type": "class",
                        "name": cls["name"],
                        "file": rel,
                        "repo": repo_name,
                        "lineno": cls.get("lineno", 0),
                        "docstring": "",
                    })

                for const in result.get("constants", []):
                    cid = f"{repo_name}:{rel}:{const['name']}"
                    nodes.append({
                        "id": cid,
                        "type": "constant",
                        "name": const["name"],
                        "file": rel,
                        "repo": repo_name,
                        "lineno": const.get("lineno", 0),
                        "docstring": "",
                    })

                for call in result.get("calls", []):
                    # Link from file-level since we don't have parent function info
                    edges.append({
                        "source": f"{repo_name}:{rel}",
                        "target": call["target"],
                        "type": "calls",
                        "lineno": call.get("lineno", 0),
                    })
            except Exception as exc:
                logger.debug("Tree-sitter parse error in %s: %s", code_file, exc)
                continue

    return {"nodes": nodes, "edges": edges}


def build_code_graph(code_root: str, output_path: str | None = None) -> dict[str, Any]:
    """Build the full code graph from all repos under code_root.

    Args:
        code_root: Directory containing cloned repos (e.g. data/raw/code/).
        output_path: Where to write data/code_graph.json. Defaults to data/code_graph.json.

    Returns:
        Dict with nodes, edges, repo_count, node_count, edge_count.
    """
    root = Path(code_root)
    if output_path is None:
        output_path = "data/code_graph.json"

    all_nodes: list[dict[str, Any]] = []
    all_edges: list[dict[str, Any]] = []
    repo_count = 0

    if root.exists():
        for repo_dir in root.iterdir():
            if not repo_dir.is_dir():
                continue
            if repo_dir.name.startswith("."):
                continue
            repo_count += 1
            result = scan_repo(repo_dir)
            all_nodes.extend(result["nodes"])
            all_edges.extend(result["edges"])

    graph = {
        "nodes": all_nodes,
        "edges": all_edges,
        "repo_count": repo_count,
        "node_count": len(all_nodes),
        "edge_count": len(all_edges),
        "generated_at": __import__("datetime").datetime.now().isoformat(),
    }

    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(graph, ensure_ascii=False, indent=2), encoding="utf-8")
    logger.info("Code graph saved: %d nodes, %d edges from %d repos", len(all_nodes), len(all_edges), repo_count)
    return graph


def load_code_graph(path: str = "data/code_graph.json") -> dict[str, Any]:
    """Load the code graph from disk."""
    p = Path(path)
    if not p.exists():
        return {"nodes": [], "edges": [], "repo_count": 0, "node_count": 0, "edge_count": 0}
    return json.loads(p.read_text(encoding="utf-8"))


def find_function_implementation(func_name: str, graph: dict[str, Any] | None = None) -> dict[str, Any] | None:
    """Find the first node matching a function or class name.

    Returns:
        Node dict or None.
    """
    if graph is None:
        graph = load_code_graph()
    for node in graph.get("nodes", []):
        if node["name"] == func_name:
            return node
    return None


def get_callers(func_name: str, graph: dict[str, Any] | None = None) -> list[str]:
    """Return IDs of all functions that call the given function."""
    if graph is None:
        graph = load_code_graph()
    callers: list[str] = []
    for edge in graph.get("edges", []):
        if edge["target"] == func_name:
            callers.append(edge["source"])
    return callers


def get_callees(func_id: str, graph: dict[str, Any] | None = None) -> list[str]:
    """Return names of all functions called by the given function ID."""
    if graph is None:
        graph = load_code_graph()
    callees: list[str] = []
    for edge in graph.get("edges", []):
        if edge["source"] == func_id:
            callees.append(edge["target"])
    return callees


def get_constraint_edges(
    graph: dict[str, Any] | None = None,
    constant_name: str | None = None,
) -> list[dict[str, Any]]:
    """Return all CONSTRAINT_BY edges, optionally filtered by constant name.

    Args:
        graph: Code graph dict. Loads from disk if None.
        constant_name: Filter by constant name (case-insensitive substring match).

    Returns:
        List of CONSTRAINT_BY edge dicts.
    """
    if graph is None:
        graph = load_code_graph()
    edges: list[dict[str, Any]] = []
    for edge in graph.get("edges", []):
        if edge.get("type") != "CONSTRAINT_BY":
            continue
        if constant_name is not None:
            if constant_name.lower() not in edge.get("constant_name", "").lower():
                continue
        edges.append(edge)
    return edges


def build_grounded_graph(
    code_root: str = "data/raw/code",
    wiki_root: str = "wiki",
    output_path: str = "data/code_graph.json",
) -> dict[str, Any]:
    """Build code graph enriched with physical CONSTRAINT_BY edges.

    Returns:
        Enriched graph dict.
    """
    graph = build_code_graph(code_root, output_path)
    from physics_grounding import enrich_code_graph_with_constraints
    enriched = enrich_code_graph_with_constraints(graph, code_root, wiki_root)
    Path(output_path).write_text(
        json.dumps(enriched, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return enriched


__all__ = [
    "scan_repo",
    "build_code_graph",
    "load_code_graph",
    "find_function_implementation",
    "get_callers",
    "get_callees",
    "get_constraint_edges",
    "build_grounded_graph",
]
