"""Tests for physical_ontology.py — cognitive physics ontology."""

from __future__ import annotations

import json
import tempfile
from pathlib import Path

import pytest

from physical_ontology import (
    EDGE_AFFECTS,
    EDGE_CONSTRAINED_BY,
    EDGE_CONTEXT_DEPENDENT,
    EDGE_CO_OCCURS,
    EDGE_DEGRADATION,
    EDGE_DERIVED_FROM,
    EDGE_HAS_PROPERTY,
    EDGE_LATENCY_SENSITIVE,
    EDGE_PART_OF,
    EDGE_SEMANTIC_ALIAS,
    NODE_TYPE_ENTITY,
    NODE_TYPE_PROPERTY,
    SEVERITY_CRITICAL,
    SEVERITY_OK,
    SEVERITY_WARNING,
    PhysicalEdge,
    PhysicalNode,
    PhysicalOntology,
)


# ── Basic node/edge ──


def test_physical_node_creation() -> None:
    n = PhysicalNode(name="test", node_type=NODE_TYPE_ENTITY, metadata={"x": 1})
    assert n.name == "test"
    assert n.node_type == NODE_TYPE_ENTITY
    assert n.metadata["x"] == 1


def test_physical_node_to_dict() -> None:
    n = PhysicalNode(name="n", node_type=NODE_TYPE_PROPERTY)
    d = n.to_dict()
    assert d["name"] == "n"
    assert d["node_type"] == NODE_TYPE_PROPERTY


def test_physical_edge_creation() -> None:
    e = PhysicalEdge(source="a", target="b", edge_type=EDGE_AFFECTS, confidence=0.8)
    assert e.source == "a"
    assert e.confidence == 0.8


def test_physical_edge_to_dict() -> None:
    e = PhysicalEdge(source="a", target="b", edge_type=EDGE_DEGRADATION)
    d = e.to_dict()
    assert d["edge_type"] == EDGE_DEGRADATION
    assert d["confidence"] == 1.0


# ── Ontology registration ──


def test_register_entity() -> None:
    onto = PhysicalOntology()
    node = onto.register_entity("Unitree_G1", entity_type="robot")
    assert onto.get_node("Unitree_G1") is node
    assert node.node_type == NODE_TYPE_ENTITY
    assert node.metadata["entity_type"] == "robot"


def test_register_property() -> None:
    onto = PhysicalOntology()
    onto.register_entity("Unitree_G1")
    prop = onto.register_property("Unitree_G1", "max_torque", 237.0, "N·m", severity=SEVERITY_CRITICAL)
    assert onto.get_node("Unitree_G1.max_torque") is prop
    assert prop.metadata["value"] == 237.0
    assert prop.metadata["unit"] == "N·m"
    assert prop.metadata["severity"] == SEVERITY_CRITICAL
    edges = onto.get_edges_from("Unitree_G1", EDGE_HAS_PROPERTY)
    assert len(edges) == 1
    assert edges[0].target == "Unitree_G1.max_torque"


def test_register_constraint() -> None:
    onto = PhysicalOntology()
    onto.register_entity("Motor")
    onto.register_entity("Controller")
    edge = onto.register_constraint("Motor", "Controller", "power_limit", formula="P = T * ω")
    assert edge.edge_type == EDGE_CONSTRAINED_BY
    assert edge.metadata["formula"] == "P = T * ω"


def test_register_causal_chain() -> None:
    onto = PhysicalOntology()
    edge = onto.register_causal_chain("load", "battery_range", "negative", confidence=0.9, condition="high_speed")
    assert edge.edge_type == EDGE_AFFECTS
    assert edge.confidence == 0.9
    assert edge.metadata["condition"] == "high_speed"


def test_register_degradation() -> None:
    onto = PhysicalOntology()
    edge = onto.register_degradation("high_current", "motor_life", "thermal_stress", time_scale="hours")
    assert edge.edge_type == EDGE_DEGRADATION
    assert edge.metadata["mechanism"] == "thermal_stress"
    assert edge.metadata["time_scale"] == "hours"


def test_register_latency_constraint() -> None:
    onto = PhysicalOntology()
    edge = onto.register_latency_constraint("VLA_model", "control_loop", 1.0)
    assert edge.edge_type == EDGE_LATENCY_SENSITIVE
    assert edge.metadata["max_latency_ms"] == 1.0


def test_register_context_switch() -> None:
    onto = PhysicalOntology()
    node = onto.register_context_switch("friction_coeff", "ice_surface", 0.1, reason="Ice reduces friction")
    assert onto.get_node("friction_coeff@ice_surface") is node
    assert node.metadata["value"] == 0.1
    assert node.metadata["context"] == "ice_surface"
    edges = onto.get_edges_from("friction_coeff", EDGE_CONTEXT_DEPENDENT)
    assert len(edges) == 1


def test_register_semantic_alias() -> None:
    onto = PhysicalOntology()
    edge = onto.register_semantic_alias("l_hip_pitch", "joint1", source="Unitree_URDF")
    assert edge.edge_type == EDGE_SEMANTIC_ALIAS
    assert edge.source == "joint1"
    assert edge.target == "l_hip_pitch"


def test_register_part_of() -> None:
    onto = PhysicalOntology()
    edge = onto.register_part_of("hand", "arm")
    assert edge.edge_type == EDGE_PART_OF


def test_register_co_occurs() -> None:
    onto = PhysicalOntology()
    edge = onto.register_co_occurs("target_torque", "gear_ratio", context="compute_torque", distance=3)
    assert edge.edge_type == EDGE_CO_OCCURS
    assert edge.metadata["distance"] == 3


def test_register_derived_from() -> None:
    onto = PhysicalOntology()
    edge = onto.register_derived_from("max_torque_code", "max_torque_urdf", derivation_type="override")
    assert edge.edge_type == EDGE_DERIVED_FROM


# ── Queries ──


def test_get_edges_from() -> None:
    onto = PhysicalOntology()
    onto.register_entity("A")
    onto.register_property("A", "p1", 1)
    onto.register_property("A", "p2", 2)
    edges = onto.get_edges_from("A", EDGE_HAS_PROPERTY)
    assert len(edges) == 2


def test_get_edges_to() -> None:
    onto = PhysicalOntology()
    onto.register_causal_chain("X", "Y", "positive")
    onto.register_causal_chain("Z", "Y", "negative")
    edges = onto.get_edges_to("Y", EDGE_AFFECTS)
    assert len(edges) == 2


def test_get_properties_of() -> None:
    onto = PhysicalOntology()
    onto.register_entity("Robot")
    onto.register_property("Robot", "mass", 50.0, "kg")
    onto.register_property("Robot", "height", 1.7, "m")
    props = onto.get_properties_of("Robot")
    assert len(props) == 2
    names = {p.name for p in props}
    assert names == {"Robot.mass", "Robot.height"}


def test_get_constraint() -> None:
    onto = PhysicalOntology()
    onto.register_constraint("motor", "limit", "effort", formula="T <= 100")
    c = onto.get_constraint("motor")
    assert c is not None
    assert c.metadata["formula"] == "T <= 100"


def test_get_constraint_none() -> None:
    onto = PhysicalOntology()
    assert onto.get_constraint("missing") is None


def test_get_context_adjusted_value() -> None:
    onto = PhysicalOntology()
    onto.register_context_switch("friction", "ice", 0.05, "ice is slippery")
    adj = onto.get_context_adjusted_value("friction", "ice")
    assert adj is not None
    assert adj["value"] == 0.05


def test_get_context_adjusted_value_missing() -> None:
    onto = PhysicalOntology()
    assert onto.get_context_adjusted_value("friction", "mars") is None


# ── BFS impact chain ──


def test_bfs_impact_chain_basic() -> None:
    onto = PhysicalOntology()
    onto.register_causal_chain("A", "B", "positive")
    onto.register_causal_chain("B", "C", "positive")
    impact = onto.bfs_impact_chain("A", radius=3)
    assert impact["start_node"] == "A"
    assert "A → B" in impact["causal_chain"]
    assert "B → C" in impact["causal_chain"]


def test_bfs_impact_chain_radius_limit() -> None:
    onto = PhysicalOntology()
    onto.register_causal_chain("A", "B", "positive")
    onto.register_causal_chain("B", "C", "positive")
    onto.register_causal_chain("C", "D", "positive")
    impact = onto.bfs_impact_chain("A", radius=1)
    assert "A → B" in impact["causal_chain"]
    assert "B → C" not in impact["causal_chain"]


def test_bfs_impact_chain_degradation() -> None:
    onto = PhysicalOntology()
    onto.register_degradation("current", "temperature", "joule_heating")
    onto.register_degradation("temperature", "motor_life", "thermal_aging")
    impact = onto.bfs_impact_chain("current", radius=3)
    paths = [d["path"] for d in impact["degradation"]]
    assert "current → temperature" in paths
    assert "temperature → motor_life" in paths


def test_bfs_impact_chain_latency() -> None:
    onto = PhysicalOntology()
    onto.register_latency_constraint("vision_model", "control_loop", 1.0)
    impact = onto.bfs_impact_chain("vision_model", radius=2)
    assert len(impact["latency_sensitive"]) == 1
    assert impact["latency_sensitive"][0]["max_latency_ms"] == 1.0


def test_bfs_deduplication() -> None:
    onto = PhysicalOntology()
    onto.register_causal_chain("A", "B", "positive")
    onto.register_causal_chain("A", "B", "positive")  # duplicate
    impact = onto.bfs_impact_chain("A", radius=3)
    assert impact["causal_chain"].count("A → B") == 1


# ── Export / Import ──


def test_export_to_dict() -> None:
    onto = PhysicalOntology()
    onto.register_entity("Robot")
    onto.register_property("Robot", "mass", 50.0, "kg")
    d = onto.export_to_dict()
    assert d["node_count"] == 2
    assert d["edge_count"] == 1
    assert len(d["nodes"]) == 2
    assert len(d["edges"]) == 1


def test_save_and_load() -> None:
    onto = PhysicalOntology()
    onto.register_entity("Unitree_G1", entity_type="robot")
    onto.register_property("Unitree_G1", "max_torque", 237.0, "N·m")
    onto.register_degradation("high_current", "motor_life", "thermal")

    with tempfile.TemporaryDirectory() as tmpdir:
        path = Path(tmpdir) / "ontology.json"
        onto.save(str(path))
        assert path.exists()

        loaded = PhysicalOntology.load(str(path))
        assert loaded.get_node("Unitree_G1") is not None
        assert loaded.get_node("Unitree_G1.max_torque") is not None
        assert len(loaded.edges) == 2


def test_load_missing_file() -> None:
    onto = PhysicalOntology.load("/nonexistent/ontology.json")
    assert onto.get_node("anything") is None
    assert len(onto.edges) == 0


# ── Severity constants ──


def test_severity_levels() -> None:
    assert SEVERITY_CRITICAL == "critical"
    assert SEVERITY_WARNING == "warning"
    assert SEVERITY_OK == "ok"


# ── Node / Edge type sets ──


def test_node_types_coverage() -> None:
    from physical_ontology import NODE_TYPES
    assert "entity" in NODE_TYPES
    assert "property" in NODE_TYPES
    assert "constraint" in NODE_TYPES
    assert "environment" in NODE_TYPES
    assert "algorithm" in NODE_TYPES
    assert "state" in NODE_TYPES


def test_edge_types_coverage() -> None:
    from physical_ontology import EDGE_TYPES
    expected = {
        "has_property", "part_of", "constrained_by", "affects",
        "co_occurs", "derived_from", "degradation",
        "latency_sensitive", "context_dependent", "semantic_alias",
    }
    assert EDGE_TYPES == expected
