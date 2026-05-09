"""Tests for physics_grounding.py.

Uses synthetic code and judgment index — no real repos required.
"""

from __future__ import annotations

import json
import tempfile
from pathlib import Path

import pytest

from physics_grounding import (
    PhysicalConstant,
    ConstraintEdge,
    _is_physics_name,
    _extract_unit_from_comment,
    _normalize_name,
    _try_numeric,
    scan_file_for_constants,
    scan_repo_for_constants,
    match_constant_to_judgments,
    load_judgment_index,
    build_constraint_edges,
    enrich_code_graph_with_constraints,
    bfs_related_nodes,
    code_physics_impact,
)


# ── Test name heuristics ──

def test_is_physics_name_torque():
    assert _is_physics_name("MAX_TORQUE")
    assert _is_physics_name("torque_limit")
    assert _is_physics_name("SAFETY_VELOCITY")


def test_is_physics_name_non_physics():
    assert not _is_physics_name("DEBUG_MODE")
    assert not _is_physics_name("api_key")


def test_extract_unit_from_comment():
    assert _extract_unit_from_comment("MAX_TORQUE = 237  # N·m") == "N·m"
    assert _extract_unit_from_comment("SPEED = 3.5  # m/s") == "m/s"
    assert _extract_unit_from_comment("foo = 1") == ""


def test_normalize_name():
    assert _normalize_name("MAX_TORQUE") == "torque"
    assert _normalize_name("MIN_VELOCITY") == "velocity"
    assert _normalize_name("SAFETY_LIMIT_HEIGHT") == "limit_height"


def test_try_numeric():
    assert _try_numeric(237) == 237.0
    assert _try_numeric("3.14") == 3.14
    assert _try_numeric(None) is None
    assert _try_numeric("abc") is None


# ── Test file scanning ──

def test_scan_file_for_constants():
    code = '''
MAX_TORQUE = 237  # N·m
STEP_HEIGHT = 0.12
DEBUG = True
SAFE_VELOCITY = 3.5  # m/s
'''
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
        f.write(code)
        f.flush()
        path = Path(f.name)

    try:
        constants = scan_file_for_constants(path, "test_repo")
        names = {c.name for c in constants}
        assert "MAX_TORQUE" in names
        assert "STEP_HEIGHT" in names
        assert "SAFE_VELOCITY" in names
        assert "DEBUG" not in names

        torque = [c for c in constants if c.name == "MAX_TORQUE"][0]
        assert torque.value == 237
        assert torque.unit == "N·m"
        assert torque.scope == "module"
    finally:
        path.unlink()


def test_scan_file_class_scope():
    code = '''
class RobotConfig:
    MAX_TORQUE = 250
    STEP_HEIGHT = 0.15
'''
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
        f.write(code)
        f.flush()
        path = Path(f.name)

    try:
        constants = scan_file_for_constants(path, "test_repo")
        names = {c.name for c in constants}
        assert "MAX_TORQUE" in names
        torque = [c for c in constants if c.name == "MAX_TORQUE"][0]
        assert torque.scope == "class"
    finally:
        path.unlink()


def test_scan_repo_for_constants():
    with tempfile.TemporaryDirectory() as tmp:
        repo = Path(tmp) / "my_repo"
        repo.mkdir()
        (repo / "config.py").write_text("MAX_TORQUE = 237  # N·m\n", encoding="utf-8")
        (repo / "utils.py").write_text("SAFE_SPEED = 2.0  # m/s\n", encoding="utf-8")

        constants = scan_repo_for_constants(repo)
        names = {c.name for c in constants}
        assert "MAX_TORQUE" in names
        assert "SAFE_SPEED" in names


# ── Test judgment matching ──

def test_match_constant_to_judgments_exact():
    constant = PhysicalConstant(
        name="MAX_TORQUE",
        value=237,
        value_repr="237",
        unit="N·m",
        file="config.py",
        repo="test",
        lineno=1,
        node_id="test:config.py:MAX_TORQUE",
    )
    index = {
        "by_entity": {
            "Unitree-G1": {
                "hardware": {
                    "MAX_TORQUE": {
                        "recommended_value": "237",
                        "confidence": 0.92,
                        "unit": "N·m",
                        "hardware_limit": 250,
                    }
                }
            }
        }
    }
    edges = match_constant_to_judgments(constant, index)
    assert len(edges) == 1
    assert edges[0].sync_status == "in_sync"
    assert edges[0].deviation_pct == pytest.approx(0.0, abs=0.1)


def test_match_constant_to_judgments_outdated():
    constant = PhysicalConstant(
        name="MAX_TORQUE",
        value=200,
        value_repr="200",
        unit="N·m",
        file="config.py",
        repo="test",
        lineno=1,
        node_id="test:config.py:MAX_TORQUE",
    )
    index = {
        "by_entity": {
            "Unitree-G1": {
                "hardware": {
                    "MAX_TORQUE": {
                        "recommended_value": "250",
                        "confidence": 0.92,
                        "unit": "N·m",
                    }
                }
            }
        }
    }
    edges = match_constant_to_judgments(constant, index)
    assert len(edges) == 1
    assert edges[0].sync_status == "outdated"
    assert edges[0].deviation_pct == pytest.approx(-20.0, abs=0.1)


def test_match_constant_no_match():
    constant = PhysicalConstant(
        name="OBSCURE_PARAM",
        value=42,
        value_repr="42",
        unit="",
        file="config.py",
        repo="test",
        lineno=1,
        node_id="test:config.py:OBSCURE_PARAM",
    )
    index = {
        "by_entity": {
            "Unitree-G1": {
                "hardware": {
                    "MAX_TORQUE": {"recommended_value": "237", "confidence": 0.92}
                }
            }
        }
    }
    edges = match_constant_to_judgments(constant, index)
    assert edges == []


# ── Test load_judgment_index ──

def test_load_judgment_index_missing():
    with tempfile.TemporaryDirectory() as tmp:
        result = load_judgment_index(tmp)
        assert result == {}


def test_load_judgment_index_valid():
    with tempfile.TemporaryDirectory() as tmp:
        idx = Path(tmp) / "judgments" / "index.json"
        idx.parent.mkdir(parents=True)
        idx.write_text(
            json.dumps({"by_entity": {"Test": {"general": {"param": {}}}}}
        ))
        result = load_judgment_index(tmp)
        assert "by_entity" in result


# ── Test build_constraint_edges ──

def test_build_constraint_edges_integration():
    with tempfile.TemporaryDirectory() as tmp:
        repo = Path(tmp) / "code_repos" / "test_repo"
        repo.mkdir(parents=True)
        (repo / "config.py").write_text("MAX_TORQUE = 237  # N·m\n", encoding="utf-8")

        wiki = Path(tmp) / "wiki"
        wiki.mkdir()
        (wiki / "judgments").mkdir()
        (wiki / "judgments" / "index.json").write_text(
            json.dumps({
                "by_entity": {
                    "Unitree-G1": {
                        "hardware": {
                            "MAX_TORQUE": {
                                "recommended_value": "237",
                                "confidence": 0.92,
                                "unit": "N·m",
                            }
                        }
                    }
                }
            }),
            encoding="utf-8",
        )

        edges = build_constraint_edges(str(repo.parent), str(wiki))
        assert len(edges) >= 1
        assert edges[0]["type"] == "CONSTRAINT_BY"
        assert edges[0]["sync_status"] == "in_sync"


# ── Test enrich_code_graph ──

def test_enrich_code_graph():
    graph = {
        "nodes": [
            {"id": "test:config.py:MAX_TORQUE", "type": "constant", "name": "MAX_TORQUE"}
        ],
        "edges": [],
    }
    with tempfile.TemporaryDirectory() as tmp:
        # Create code repo with matching constant
        code_root = Path(tmp) / "code_repos"
        repo = code_root / "test_repo"
        repo.mkdir(parents=True)
        (repo / "config.py").write_text("MAX_TORQUE = 237  # N·m\n", encoding="utf-8")

        wiki = Path(tmp) / "wiki"
        wiki.mkdir()
        (wiki / "judgments").mkdir()
        (wiki / "judgments" / "index.json").write_text(
            json.dumps({
                "by_entity": {
                    "Unitree-G1": {
                        "hardware": {
                            "MAX_TORQUE": {
                                "recommended_value": "237",
                                "confidence": 0.92,
                                "unit": "N·m",
                            }
                        }
                    }
                }
            }),
            encoding="utf-8",
        )

        enriched = enrich_code_graph_with_constraints(
            graph, code_root=str(code_root), wiki_root=str(wiki)
        )
        assert enriched.get("constraint_edge_count", 0) >= 1
        assert any(e.get("type") == "CONSTRAINT_BY" for e in enriched["edges"])


# ── Test BFS context pruning ──

def test_bfs_related_nodes():
    graph = {
        "nodes": [
            {"id": "A", "type": "constant"},
            {"id": "B", "type": "function"},
            {"id": "C", "type": "function"},
            {"id": "D", "type": "class"},
        ],
        "edges": [
            {"source": "A", "target": "B", "type": "CONSTRAINT_BY"},
            {"source": "B", "target": "C", "type": "calls"},
            {"source": "C", "target": "D", "type": "calls"},
        ],
    }
    result = bfs_related_nodes("A", graph, max_depth=2)
    ids = {n["id"] for n in result["nodes"]}
    assert "A" in ids
    assert "B" in ids
    assert "C" in ids
    assert "D" not in ids  # depth 3, max_depth=2


def test_bfs_related_nodes_constraint_only():
    graph = {
        "nodes": [
            {"id": "A", "type": "constant"},
            {"id": "B", "type": "function"},
            {"id": "C", "type": "function"},
        ],
        "edges": [
            {"source": "A", "target": "B", "type": "CONSTRAINT_BY"},
            {"source": "B", "target": "C", "type": "calls"},
        ],
    }
    result = bfs_related_nodes("A", graph, max_depth=2, edge_types=["CONSTRAINT_BY"])
    ids = {n["id"] for n in result["nodes"]}
    assert "A" in ids
    assert "B" in ids
    assert "C" not in ids  # B->C is "calls", not "CONSTRAINT_BY"


# ── Test code_physics_impact ──

def test_code_physics_impact():
    graph = {
        "nodes": [
            {"id": "repo:config.py:MAX_TORQUE", "type": "constant", "name": "MAX_TORQUE"},
            {"id": "repo:config.py:move_robot", "type": "function", "name": "move_robot"},
        ],
        "edges": [
            {
                "source": "repo:config.py:MAX_TORQUE",
                "target": "Unitree-G1:hardware:MAX_TORQUE",
                "type": "CONSTRAINT_BY",
                "sync_status": "in_sync",
                "constant_name": "MAX_TORQUE",
            },
            {"source": "repo:config.py:move_robot", "target": "repo:config.py:MAX_TORQUE", "type": "calls"},
        ],
    }
    result = code_physics_impact("MAX_TORQUE", graph=graph)
    assert result["constraint_count"] == 1
    assert result["affected_function_count"] >= 1
    assert result["sync_summary"]["in_sync"] == 1


def test_code_physics_impact_no_match():
    graph = {"nodes": [], "edges": []}
    result = code_physics_impact("NONEXISTENT", graph=graph)
    assert result["constraint_count"] == 0
    assert result["affected_function_count"] == 0


# ── Test PhysicalConstant dataclass ──

def test_physical_constant_to_dict():
    c = PhysicalConstant(
        name="MAX_TORQUE",
        value=237,
        value_repr="237",
        unit="N·m",
        file="config.py",
        repo="test",
        lineno=1,
        node_id="test:config.py:MAX_TORQUE",
    )
    d = c.to_dict()
    assert d["name"] == "MAX_TORQUE"
    assert d["value"] == 237


# ── Test ConstraintEdge dataclass ──

def test_constraint_edge_to_dict():
    e = ConstraintEdge(
        source="repo:a.py:MAX_TORQUE",
        target="Unitree-G1:hardware:MAX_TORQUE",
        constant_name="MAX_TORQUE",
        parameter="MAX_TORQUE",
        entity="Unitree-G1",
        code_value=237,
        judgment_value="250",
        unit="N·m",
        confidence=0.92,
        sync_status="outdated",
        deviation_pct=-5.2,
    )
    d = e.to_dict()
    assert d["type"] == "CONSTRAINT_BY"
    assert d["sync_status"] == "outdated"


# ── Test code topology mining (Phase 16) ──

def test_mine_code_topology_cooccurs():
    from physics_grounding import mine_code_topology

    with tempfile.NamedTemporaryFile(suffix=".py", delete=False, mode="w") as f:
        f.write("def foo():\n    bar()\n    baz()\n")
        path = f.name

    edges = mine_code_topology(path)
    Path(path).unlink()
    cooccurs = [e for e in edges if e["type"] == "CO_OCCURS"]
    assert len(cooccurs) >= 1
    names = {cooccurs[0]["source"], cooccurs[0]["target"]}
    assert "bar" in names or "baz" in names


def test_mine_code_topology_latency_sensitive():
    from physics_grounding import mine_code_topology

    with tempfile.NamedTemporaryFile(suffix=".py", delete=False, mode="w") as f:
        f.write("import time\ndef control():\n    time.sleep(0.001)\n")
        path = f.name

    edges = mine_code_topology(path)
    Path(path).unlink()
    lat = [e for e in edges if e["type"] == "LATENCY_SENSITIVE"]
    assert len(lat) >= 1
    assert lat[0]["target"] == "control_loop"


def test_mine_code_topology_empty_for_unknown():
    from physics_grounding import mine_code_topology

    edges = mine_code_topology("/nonexistent/file.py")
    assert edges == []
