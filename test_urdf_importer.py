"""Tests for urdf_importer.py — URDF structure mapping into physical ontology."""

from __future__ import annotations

import tempfile
from pathlib import Path

import pytest

from physical_ontology import (
    EDGE_CONSTRAINED_BY,
    EDGE_HAS_PROPERTY,
    EDGE_PART_OF,
    EDGE_SEMANTIC_ALIAS,
    NODE_TYPE_ENTITY,
)
from urdf_importer import SEMANTIC_MAPPING, URDFImporter


# ── A minimal URDF for testing ──

MINI_URDF = '''<?xml version="1.0"?>
<robot name="test_robot">
  <link name="base_link">
    <inertial>
      <mass value="5.0"/>
      <inertia ixx="0.1" ixy="0" ixz="0" iyy="0.2" iyz="0" izz="0.3"/>
    </inertial>
  </link>
  <link name="arm_link">
    <inertial>
      <mass value="2.0"/>
      <inertia ixx="0.05" ixy="0" ixz="0" iyy="0.06" iyz="0" izz="0.07"/>
    </inertial>
  </link>
  <joint name="shoulder_joint" type="revolute">
    <parent link="base_link"/>
    <child link="arm_link"/>
    <limit effort="100.0" velocity="10.0" lower="-1.57" upper="1.57"/>
  </joint>
</robot>
'''


def test_semantic_mapping_has_entries() -> None:
    assert "joint1" in SEMANTIC_MAPPING
    assert SEMANTIC_MAPPING["joint1"] == "l_hip_pitch"


def test_parse_urdf_creates_entities() -> None:
    importer = URDFImporter()
    with tempfile.NamedTemporaryFile(suffix=".urdf", delete=False, mode="w") as f:
        f.write(MINI_URDF)
        path = f.name

    result = importer.parse_urdf(path, "TestBot")
    Path(path).unlink()

    assert result["robot_name"] == "TestBot"
    assert len(result["links"]) == 2
    assert len(result["joints"]) == 1

    onto = importer.get_ontology()
    assert onto.get_node("TestBot") is not None
    assert onto.get_node("TestBot.base_link") is not None
    assert onto.get_node("TestBot.arm_link") is not None
    assert onto.get_node("TestBot.shoulder_joint") is not None


def test_parse_urdf_registers_masses() -> None:
    importer = URDFImporter()
    with tempfile.NamedTemporaryFile(suffix=".urdf", delete=False, mode="w") as f:
        f.write(MINI_URDF)
        path = f.name

    importer.parse_urdf(path, "TestBot")
    Path(path).unlink()

    onto = importer.get_ontology()
    base_mass = onto.get_node("TestBot.base_link.mass")
    assert base_mass is not None
    assert base_mass.metadata["value"] == 5.0
    assert base_mass.metadata["unit"] == "kg"


def test_parse_urdf_registers_joint_limits() -> None:
    importer = URDFImporter()
    with tempfile.NamedTemporaryFile(suffix=".urdf", delete=False, mode="w") as f:
        f.write(MINI_URDF)
        path = f.name

    importer.parse_urdf(path, "TestBot")
    Path(path).unlink()

    onto = importer.get_ontology()
    effort_prop = onto.get_node("TestBot.shoulder_joint.effort")
    assert effort_prop is not None
    assert effort_prop.metadata["value"] == 100.0

    # Check CONSTRAINT_BY edge was created
    constraints = onto.get_edges_from("TestBot.shoulder_joint", EDGE_CONSTRAINED_BY)
    assert len(constraints) >= 1


def test_parse_urdf_part_of_edges() -> None:
    importer = URDFImporter()
    with tempfile.NamedTemporaryFile(suffix=".urdf", delete=False, mode="w") as f:
        f.write(MINI_URDF)
        path = f.name

    importer.parse_urdf(path, "TestBot")
    Path(path).unlink()

    onto = importer.get_ontology()
    part_of = onto.get_edges_from("TestBot.shoulder_joint", EDGE_PART_OF)
    assert len(part_of) >= 1


def test_parse_urdf_with_semantic_mapping() -> None:
    urdf = '''<?xml version="1.0"?>
<robot name="mapped_bot">
  <link name="joint1">
    <inertial><mass value="1.0"/></inertial>
  </link>
  <joint name="joint1" type="revolute">
    <parent link="base"/>
    <child link="joint1"/>
    <limit effort="50.0" velocity="5.0"/>
  </joint>
</robot>
'''
    importer = URDFImporter()
    with tempfile.NamedTemporaryFile(suffix=".urdf", delete=False, mode="w") as f:
        f.write(urdf)
        path = f.name

    importer.parse_urdf(path, "G1")
    Path(path).unlink()

    onto = importer.get_ontology()
    # joint1 should be mapped to l_hip_pitch
    assert onto.get_node("G1.l_hip_pitch") is not None

    # Semantic alias edge should exist
    aliases = [e for e in onto.edges if e.edge_type == EDGE_SEMANTIC_ALIAS]
    assert len(aliases) >= 1


def test_parse_urdf_missing_file() -> None:
    importer = URDFImporter()
    with pytest.raises(FileNotFoundError):
        importer.parse_urdf("/nonexistent/file.urdf", "Bot")


def test_parse_urdf_invalid_xml() -> None:
    importer = URDFImporter()
    with tempfile.NamedTemporaryFile(suffix=".urdf", delete=False, mode="w") as f:
        f.write("not xml")
        path = f.name

    with pytest.raises(Exception):
        importer.parse_urdf(path, "Bot")
    Path(path).unlink()


def test_parse_real_minitaur_urdf() -> None:
    """Integration test with the real minitaur URDF in data/raw/code/."""
    urdf_path = "data/raw/code/google-research_google-research/hybrid_zero_dynamics/matlab/minitaur_simple/urdf/minitaur_simple.urdf"
    path = Path(urdf_path)
    if not path.exists():
        pytest.skip("Minitaur URDF not available")

    importer = URDFImporter()
    result = importer.parse_urdf(str(path), "Minitaur")

    assert result["robot_name"] == "Minitaur"
    assert len(result["links"]) > 0
    assert len(result["joints"]) > 0

    onto = importer.get_ontology()
    assert onto.get_node("Minitaur") is not None
    # At least chassis should be registered
    assert any("Minitaur." in n for n in onto.nodes)
