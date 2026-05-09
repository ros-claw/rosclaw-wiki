"""Physical Ontology — unified cognitive physics model for embodied intelligence.

Defines 6 node types and 10 edge types that form a "common-sense physics web"
for causal reasoning about robotic systems.
"""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

logger = logging.getLogger("rosclaw.physical_ontology")


# ── Node types ──

NODE_TYPE_ENTITY = "entity"
NODE_TYPE_PROPERTY = "property"
NODE_TYPE_CONSTRAINT = "constraint"
NODE_TYPE_ENVIRONMENT = "environment"
NODE_TYPE_ALGORITHM = "algorithm"
NODE_TYPE_STATE = "state"

NODE_TYPES = {
    NODE_TYPE_ENTITY,
    NODE_TYPE_PROPERTY,
    NODE_TYPE_CONSTRAINT,
    NODE_TYPE_ENVIRONMENT,
    NODE_TYPE_ALGORITHM,
    NODE_TYPE_STATE,
}

# ── Edge types ──

EDGE_HAS_PROPERTY = "has_property"
EDGE_PART_OF = "part_of"
EDGE_CONSTRAINED_BY = "constrained_by"
EDGE_AFFECTS = "affects"
EDGE_CO_OCCURS = "co_occurs"
EDGE_DERIVED_FROM = "derived_from"
EDGE_DEGRADATION = "degradation"
EDGE_LATENCY_SENSITIVE = "latency_sensitive"
EDGE_CONTEXT_DEPENDENT = "context_dependent"
EDGE_SEMANTIC_ALIAS = "semantic_alias"

EDGE_TYPES = {
    EDGE_HAS_PROPERTY,
    EDGE_PART_OF,
    EDGE_CONSTRAINED_BY,
    EDGE_AFFECTS,
    EDGE_CO_OCCURS,
    EDGE_DERIVED_FROM,
    EDGE_DEGRADATION,
    EDGE_LATENCY_SENSITIVE,
    EDGE_CONTEXT_DEPENDENT,
    EDGE_SEMANTIC_ALIAS,
}

# ── Severity levels ──

SEVERITY_CRITICAL = "critical"
SEVERITY_WARNING = "warning"
SEVERITY_OK = "ok"


@dataclass
class PhysicalNode:
    """A node in the physical ontology graph."""

    name: str
    node_type: str
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.node_type not in NODE_TYPES:
            logger.warning("Unknown node type: %s", self.node_type)

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "node_type": self.node_type,
            "metadata": self.metadata,
        }


@dataclass
class PhysicalEdge:
    """A directed edge in the physical ontology graph."""

    source: str
    target: str
    edge_type: str
    confidence: float = 1.0
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.edge_type not in EDGE_TYPES:
            logger.warning("Unknown edge type: %s", self.edge_type)

    def to_dict(self) -> dict[str, Any]:
        return {
            "source": self.source,
            "target": self.target,
            "edge_type": self.edge_type,
            "confidence": self.confidence,
            "metadata": self.metadata,
        }


class PhysicalOntology:
    """Unified physical ontology manager.

    Manages nodes (entities, properties, constraints, environments, algorithms, states)
    and edges (has_property, part_of, constrained_by, affects, co_occurs,
    derived_from, degradation, latency_sensitive, context_dependent, semantic_alias).
    """

    def __init__(self) -> None:
        self.nodes: dict[str, PhysicalNode] = {}
        self.edges: list[PhysicalEdge] = []

    # ── Registration helpers ──

    def register_entity(self, name: str, entity_type: str = "", metadata: dict[str, Any] | None = None) -> PhysicalNode:
        """Register a physical entity (e.g. Unitree_G1, Link_L_Ankle)."""
        meta = metadata or {}
        if entity_type:
            meta["entity_type"] = entity_type
        node = PhysicalNode(name=name, node_type=NODE_TYPE_ENTITY, metadata=meta)
        self.nodes[name] = node
        return node

    def register_property(
        self,
        entity: str,
        property_name: str,
        value: float | int | str | None = None,
        unit: str = "",
        provenance: dict[str, Any] | None = None,
        severity: str = SEVERITY_OK,
        tolerance: float | None = None,
    ) -> PhysicalNode:
        """Register a physical property and establish HAS_PROPERTY edge."""
        node_key = f"{entity}.{property_name}"
        meta: dict[str, Any] = {
            "value": value,
            "unit": unit,
            "severity": severity,
            "provenance": provenance or {},
        }
        if tolerance is not None:
            meta["tolerance"] = tolerance

        node = PhysicalNode(name=node_key, node_type=NODE_TYPE_PROPERTY, metadata=meta)
        self.nodes[node_key] = node
        self.edges.append(
            PhysicalEdge(source=entity, target=node_key, edge_type=EDGE_HAS_PROPERTY)
        )
        return node

    def register_constraint(
        self,
        source: str,
        target: str,
        constraint_type: str = "",
        formula: str | None = None,
        description: str | None = None,
    ) -> PhysicalEdge:
        """Register a physical constraint (e.g. Power = Torque * Angular_Velocity)."""
        edge = PhysicalEdge(
            source=source,
            target=target,
            edge_type=EDGE_CONSTRAINED_BY,
            metadata={
                "constraint_type": constraint_type,
                "formula": formula,
                "description": description,
            },
        )
        self.edges.append(edge)
        return edge

    def register_causal_chain(
        self,
        cause: str,
        effect: str,
        relation: str = "",
        confidence: float = 1.0,
        condition: str | None = None,
    ) -> PhysicalEdge:
        """Register a causal relationship (e.g. load increase -> range decrease)."""
        edge = PhysicalEdge(
            source=cause,
            target=effect,
            edge_type=EDGE_AFFECTS,
            confidence=confidence,
            metadata={"relation": relation, "condition": condition},
        )
        self.edges.append(edge)
        return edge

    def register_degradation(
        self,
        cause: str,
        effect: str,
        mechanism: str = "",
        time_scale: str | None = None,
    ) -> PhysicalEdge:
        """Register a degradation relationship (e.g. high current -> temperature rise -> motor life shortening)."""
        edge = PhysicalEdge(
            source=cause,
            target=effect,
            edge_type=EDGE_DEGRADATION,
            metadata={"mechanism": mechanism, "time_scale": time_scale},
        )
        self.edges.append(edge)
        return edge

    def register_latency_constraint(
        self,
        algorithm: str,
        hardware: str,
        max_tolerable_latency_ms: float,
    ) -> PhysicalEdge:
        """Register a timing constraint (e.g. inference latency < control period)."""
        edge = PhysicalEdge(
            source=algorithm,
            target=hardware,
            edge_type=EDGE_LATENCY_SENSITIVE,
            metadata={"max_latency_ms": max_tolerable_latency_ms},
        )
        self.edges.append(edge)
        return edge

    def register_context_switch(
        self,
        property_name: str,
        context: str,
        adjusted_value: float | int | str,
        reason: str = "",
    ) -> PhysicalNode:
        """Register a context-dependent property value (e.g. friction coefficient on ice)."""
        node_key = f"{property_name}@{context}"
        node = PhysicalNode(
            name=node_key,
            node_type=NODE_TYPE_PROPERTY,
            metadata={
                "value": adjusted_value,
                "context": context,
                "reason": reason,
            },
        )
        self.nodes[node_key] = node
        self.edges.append(
            PhysicalEdge(
                source=property_name,
                target=node_key,
                edge_type=EDGE_CONTEXT_DEPENDENT,
            )
        )
        return node

    def register_semantic_alias(
        self,
        canonical_name: str,
        alias: str,
        source: str = "",
    ) -> PhysicalEdge:
        """Register a semantic mapping (e.g. joint1 -> l_hip_pitch)."""
        edge = PhysicalEdge(
            source=alias,
            target=canonical_name,
            edge_type=EDGE_SEMANTIC_ALIAS,
            metadata={"source": source},
        )
        self.edges.append(edge)
        return edge

    def register_part_of(self, child: str, parent: str) -> PhysicalEdge:
        """Register structural hierarchy (e.g. hand is part of arm)."""
        edge = PhysicalEdge(source=child, target=parent, edge_type=EDGE_PART_OF)
        self.edges.append(edge)
        return edge

    def register_co_occurs(
        self,
        source: str,
        target: str,
        context: str = "",
        distance: int | None = None,
    ) -> PhysicalEdge:
        """Register code co-occurrence relationship."""
        edge = PhysicalEdge(
            source=source,
            target=target,
            edge_type=EDGE_CO_OCCURS,
            metadata={"context": context, "distance": distance},
        )
        self.edges.append(edge)
        return edge

    def register_derived_from(
        self,
        derived: str,
        source: str,
        derivation_type: str = "",
    ) -> PhysicalEdge:
        """Register provenance (e.g. parameter derived from URDF)."""
        edge = PhysicalEdge(
            source=derived,
            target=source,
            edge_type=EDGE_DERIVED_FROM,
            metadata={"derivation_type": derivation_type},
        )
        self.edges.append(edge)
        return edge

    # ── Queries ──

    def get_node(self, name: str) -> PhysicalNode | None:
        return self.nodes.get(name)

    def get_edges_from(self, node_name: str, edge_type: str | None = None) -> list[PhysicalEdge]:
        """Get all outgoing edges from a node, optionally filtered by type."""
        result: list[PhysicalEdge] = []
        for edge in self.edges:
            if edge.source == node_name:
                if edge_type is None or edge.edge_type == edge_type:
                    result.append(edge)
        return result

    def get_edges_to(self, node_name: str, edge_type: str | None = None) -> list[PhysicalEdge]:
        """Get all incoming edges to a node, optionally filtered by type."""
        result: list[PhysicalEdge] = []
        for edge in self.edges:
            if edge.target == node_name:
                if edge_type is None or edge.edge_type == edge_type:
                    result.append(edge)
        return result

    def get_properties_of(self, entity: str) -> list[PhysicalNode]:
        """Get all property nodes belonging to an entity."""
        props: list[PhysicalNode] = []
        for edge in self.edges:
            if edge.source == entity and edge.edge_type == EDGE_HAS_PROPERTY:
                node = self.nodes.get(edge.target)
                if node:
                    props.append(node)
        return props

    def get_constraint(self, property_name: str) -> PhysicalEdge | None:
        """Get the first CONSTRAINED_BY edge for a property."""
        for edge in self.edges:
            if edge.source == property_name and edge.edge_type == EDGE_CONSTRAINED_BY:
                return edge
        return None

    def get_context_adjusted_value(
        self,
        property_name: str,
        context: str,
    ) -> dict[str, Any] | None:
        """Get context-adjusted value for a property."""
        node_key = f"{property_name}@{context}"
        node = self.nodes.get(node_key)
        if node:
            return {
                "value": node.metadata.get("value"),
                "reason": node.metadata.get("reason", ""),
            }
        return None

    # ── BFS impact chain ──

    def bfs_impact_chain(self, start_node: str, radius: int = 3) -> dict[str, Any]:
        """BFS traversal to find physical impact chain within a given radius.

        Returns a dict with categorized impacts:
          - hardware: directly affected hardware nodes
          - code: directly affected code/algorithm nodes
          - properties: indirectly affected properties (causal chain)
          - degradation: degradation paths
          - latency_sensitive: timing-sensitive nodes
          - causal_chain: complete causal chain as text
        """
        visited: set[str] = set()
        queue: list[tuple[str, int]] = [(start_node, 0)]

        impact: dict[str, list[Any]] = {
            "hardware": [],
            "code": [],
            "properties": [],
            "degradation": [],
            "latency_sensitive": [],
            "causal_chain": [],
        }

        while queue:
            node, depth = queue.pop(0)
            if node in visited or depth > radius:
                continue
            visited.add(node)

            for edge in self.edges:
                if edge.source == node and edge.target not in visited:
                    # Only record impacts within radius
                    if depth + 1 <= radius:
                        if edge.edge_type == EDGE_DEGRADATION:
                            impact["degradation"].append({
                                "path": f"{node} → {edge.target}",
                                "mechanism": edge.metadata.get("mechanism", ""),
                                "time_scale": edge.metadata.get("time_scale"),
                            })
                        elif edge.edge_type == EDGE_LATENCY_SENSITIVE:
                            impact["latency_sensitive"].append({
                                "path": f"{node} → {edge.target}",
                                "max_latency_ms": edge.metadata.get("max_latency_ms"),
                            })
                        elif edge.edge_type == EDGE_AFFECTS:
                            impact["causal_chain"].append(f"{node} → {edge.target}")
                            target_node = self.nodes.get(edge.target)
                            if target_node and target_node.node_type == NODE_TYPE_PROPERTY:
                                impact["properties"].append(edge.target)
                            elif target_node and target_node.node_type == NODE_TYPE_ENTITY:
                                impact["hardware"].append(edge.target)
                            elif target_node and target_node.node_type == NODE_TYPE_ALGORITHM:
                                impact["code"].append(edge.target)

                    if depth + 1 <= radius:
                        queue.append((edge.target, depth + 1))

        # Deduplicate while preserving order
        for key in impact:
            if isinstance(impact[key], list):
                seen: set[str] = set()
                deduped: list[Any] = []
                for item in impact[key]:
                    item_key = str(item)
                    if item_key not in seen:
                        seen.add(item_key)
                        deduped.append(item)
                impact[key] = deduped

        return {
            "start_node": start_node,
            "radius": radius,
            "visited": list(visited),
            **impact,
        }

    # ── Export ──

    def export_to_dict(self) -> dict[str, Any]:
        return {
            "nodes": [n.to_dict() for n in self.nodes.values()],
            "edges": [e.to_dict() for e in self.edges],
            "node_count": len(self.nodes),
            "edge_count": len(self.edges),
        }

    def export_to_seekdb(self, output_path: str | None = None) -> str:
        """Export ontology to a JSON file (SeekDB integration stub).

        In production, this would write to SeekDB's entity_graph collection.
        For now, writes to a local JSON file that can be bulk-imported.
        """
        data = self.export_to_dict()
        if output_path is None:
            output_path = "data/physical_ontology.json"
        p = Path(output_path)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        logger.info("Physical ontology exported: %d nodes, %d edges to %s", len(self.nodes), len(self.edges), output_path)
        return str(p)

    def save(self, path: str) -> None:
        """Save ontology to disk."""
        self.export_to_seekdb(path)

    @classmethod
    def load(cls, path: str) -> "PhysicalOntology":
        """Load ontology from disk."""
        p = Path(path)
        if not p.exists():
            return cls()
        data = json.loads(p.read_text(encoding="utf-8"))
        onto = cls()
        for n in data.get("nodes", []):
            onto.nodes[n["name"]] = PhysicalNode(
                name=n["name"],
                node_type=n["node_type"],
                metadata=n.get("metadata", {}),
            )
        for e in data.get("edges", []):
            onto.edges.append(
                PhysicalEdge(
                    source=e["source"],
                    target=e["target"],
                    edge_type=e["edge_type"],
                    confidence=e.get("confidence", 1.0),
                    metadata=e.get("metadata", {}),
                )
            )
        return onto


__all__ = [
    "PhysicalNode",
    "PhysicalEdge",
    "PhysicalOntology",
    "NODE_TYPES",
    "EDGE_TYPES",
    "SEVERITY_CRITICAL",
    "SEVERITY_WARNING",
    "SEVERITY_OK",
]
