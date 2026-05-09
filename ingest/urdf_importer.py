"""URDF/SRDF Importer — parse robot URDF files into PhysicalOntology.

Extracts link-joint topology, masses, inertias, joint limits, and registers
them as a structured physical ontology. Includes semantic mapping table to
normalize naming across different robot manufacturers.
"""

from __future__ import annotations

import logging
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any

from physical_ontology import PhysicalOntology

logger = logging.getLogger("rosclaw.urdf_importer")

# ── Semantic mapping table: non-standard URDF names → canonical ontology names ──

SEMANTIC_MAPPING: dict[str, str] = {
    # Unitree G1
    "joint1": "l_hip_pitch",
    "joint2": "l_hip_roll",
    "joint3": "l_knee_pitch",
    "joint4": "l_ankle_pitch",
    "joint5": "r_hip_pitch",
    "joint6": "r_hip_roll",
    "joint7": "r_knee_pitch",
    "joint8": "r_ankle_pitch",
    # Unitree H1
    "j_hip_yaw": "hip_yaw",
    "j_hip_roll": "hip_roll",
    "j_knee": "knee_pitch",
    # B2 / generic
    "leg_left_1": "l_hip_pitch",
    "leg_left_2": "l_knee_pitch",
    "leg_right_1": "r_hip_pitch",
    "leg_right_2": "r_knee_pitch",
    # Minitaur
    "base_chassis_link": "chassis",
    "motor_front_leftR_joint": "fl_motor_r",
    "motor_front_leftL_joint": "fl_motor_l",
    "motor_back_leftR_joint": "bl_motor_r",
    "motor_back_leftL_joint": "bl_motor_l",
}


def _extract_mass(link_elem: ET.Element) -> float | None:
    """Extract mass from a link element."""
    inertial = link_elem.find("inertial")
    if inertial is None:
        return None
    mass_elem = inertial.find("mass")
    if mass_elem is not None:
        try:
            return float(mass_elem.get("value", "0"))
        except (ValueError, TypeError):
            pass
    return None


def _extract_inertia(link_elem: ET.Element) -> dict[str, float] | None:
    """Extract inertia tensor from a link element."""
    inertial = link_elem.find("inertial")
    if inertial is None:
        return None
    inertia_elem = inertial.find("inertia")
    if inertia_elem is None:
        return None
    result: dict[str, float] = {}
    for key in ("ixx", "ixy", "ixz", "iyy", "iyz", "izz"):
        val = inertia_elem.get(key)
        if val is not None:
            try:
                result[key] = float(val)
            except (ValueError, TypeError):
                pass
    return result if result else None


def _extract_parent(joint_elem: ET.Element) -> str:
    """Extract parent link name from a joint element."""
    parent = joint_elem.find("parent")
    if parent is not None:
        return parent.get("link", "")
    return ""


def _extract_child(joint_elem: ET.Element) -> str:
    """Extract child link name from a joint element."""
    child = joint_elem.find("child")
    if child is not None:
        return child.get("link", "")
    return ""


def _extract_limits(joint_elem: ET.Element) -> dict[str, float] | None:
    """Extract joint limits (effort, velocity, lower, upper)."""
    limit_elem = joint_elem.find("limit")
    if limit_elem is None:
        return None
    result: dict[str, float] = {}
    for key in ("effort", "velocity", "lower", "upper"):
        val = limit_elem.get(key)
        if val is not None:
            try:
                result[key] = float(val)
            except (ValueError, TypeError):
                pass
    return result if result else None


class URDFImporter:
    """Parse URDF files and import robot topology into PhysicalOntology."""

    def __init__(self, ontology: PhysicalOntology | None = None) -> None:
        self.ontology = ontology or PhysicalOntology()

    def parse_urdf(self, urdf_path: str, robot_name: str) -> dict[str, Any]:
        """Parse a URDF file and register links, joints, and constraints.

        Args:
            urdf_path: Path to the URDF file.
            robot_name: Name to prefix all entities (e.g. "Unitree_G1").

        Returns:
            Dict with 'links' and 'joints' lists.
        """
        path = Path(urdf_path)
        if not path.exists():
            raise FileNotFoundError(f"URDF not found: {urdf_path}")

        tree = ET.parse(path)
        root = tree.getroot()
        robot_elem = root if root.tag == "robot" else root.find("robot")
        if robot_elem is None:
            raise ValueError("No <robot> element found in URDF")

        # Register robot entity
        self.ontology.register_entity(robot_name, entity_type="robot")

        links: list[dict[str, Any]] = []
        joints: list[dict[str, Any]] = []

        # ── Extract links ──
        for link_elem in robot_elem.findall("link"):
            link_name = link_elem.get("name", "")
            if not link_name:
                continue
            canonical_name = SEMANTIC_MAPPING.get(link_name, link_name)
            entity_key = f"{robot_name}.{canonical_name}"

            mass = _extract_mass(link_elem)
            inertia = _extract_inertia(link_elem)

            link_data: dict[str, Any] = {
                "name": link_name,
                "canonical_name": canonical_name,
                "mass": mass,
                "inertia": inertia,
            }
            links.append(link_data)

            # Register to ontology
            self.ontology.register_entity(
                entity_key,
                entity_type="link",
                metadata={"urdf_name": link_name, "robot": robot_name},
            )
            if mass is not None:
                self.ontology.register_property(
                    entity_key, "mass", mass, "kg",
                    provenance={"source": "urdf", "robot": robot_name},
                )
            if inertia:
                self.ontology.register_property(
                    entity_key, "inertia", inertia, "kg·m²",
                    provenance={"source": "urdf", "robot": robot_name},
                )

        # ── Extract joints ──
        for joint_elem in robot_elem.findall("joint"):
            joint_name = joint_elem.get("name", "")
            if not joint_name:
                continue
            joint_type = joint_elem.get("type", "")
            canonical_name = SEMANTIC_MAPPING.get(joint_name, joint_name)
            parent = _extract_parent(joint_elem)
            child = _extract_child(joint_elem)
            limits = _extract_limits(joint_elem)

            joint_data: dict[str, Any] = {
                "name": joint_name,
                "canonical_name": canonical_name,
                "type": joint_type,
                "parent": parent,
                "child": child,
                "limits": limits,
            }
            joints.append(joint_data)

            entity_key = f"{robot_name}.{canonical_name}"
            parent_key = f"{robot_name}.{SEMANTIC_MAPPING.get(parent, parent)}"
            child_key = f"{robot_name}.{SEMANTIC_MAPPING.get(child, child)}"

            # Register joint entity
            self.ontology.register_entity(
                entity_key,
                entity_type="joint",
                metadata={
                    "urdf_name": joint_name,
                    "joint_type": joint_type,
                    "robot": robot_name,
                },
            )

            # Register semantic alias if different
            if joint_name != canonical_name:
                self.ontology.register_semantic_alias(
                    canonical_name, joint_name, source=f"{robot_name}_urdf"
                )

            # PART_OF: joint is part of parent link's kinematic chain
            if parent:
                self.ontology.register_part_of(entity_key, parent_key)

            # PART_OF: child link is part of joint
            if child:
                self.ontology.register_part_of(child_key, entity_key)

            # CONSTRAINT_BY: joint limits
            if limits:
                for limit_type, limit_value in limits.items():
                    unit = "N·m" if limit_type == "effort" else "rad/s" if limit_type == "velocity" else "rad"
                    prop_node = self.ontology.register_property(
                        entity_key, limit_type, limit_value, unit,
                        provenance={"source": "urdf", "robot": robot_name},
                    )
                    self.ontology.register_constraint(
                        entity_key,
                        f"{entity_key}.{limit_type}",
                        "hardware_limit",
                        description=f"URDF defined {limit_type} limit: {limit_value}",
                    )

        logger.info(
            "URDF imported: %s — %d links, %d joints", robot_name, len(links), len(joints)
        )
        return {"links": links, "joints": joints, "robot_name": robot_name}

    def get_ontology(self) -> PhysicalOntology:
        return self.ontology


__all__ = ["URDFImporter", "SEMANTIC_MAPPING"]
