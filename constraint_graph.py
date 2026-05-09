"""Constraint Graph — physical constraint graph with tri-party arbitration.

Integrates URDF, code, and paper sources into a unified causal reasoning graph.
Implements:
  - Tri-party arbitration (URDF 1.0 + code 0.8 + paper 0.6)
  - Physical impact chain analysis (BFS radius 3)
  - Context switching (simulation vs real_world)
  - Export to SeekDB
"""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any

from physical_ontology import (
    EDGE_AFFECTS,
    EDGE_CONSTRAINED_BY,
    EDGE_CONTEXT_DEPENDENT,
    EDGE_DEGRADATION,
    EDGE_LATENCY_SENSITIVE,
    NODE_TYPE_PROPERTY,
    SEVERITY_CRITICAL,
    SEVERITY_OK,
    SEVERITY_WARNING,
    PhysicalEdge,
    PhysicalOntology,
)

logger = logging.getLogger("rosclaw.constraint_graph")


# ── Tri-party arbitration ──


def tri_party_arbitration(
    property_name: str,
    urdf_value: float | int | str | None,
    code_value: float | int | str | None,
    paper_value: float | int | str | None,
) -> dict[str, Any]:
    """Resolve conflicting physical values from URDF, code, and paper sources.

    Weights: URDF=1.0 (hardware constitution), code=0.8 (implementation),
    paper=0.6 (experimental/ideal).

    Returns:
        Dict with resolved status, winning value, confidence, and reason.
    """
    claims: list[dict[str, Any]] = []
    if urdf_value is not None:
        claims.append({"value": urdf_value, "weight": 1.0, "source": "urdf"})
    if code_value is not None:
        claims.append({"value": code_value, "weight": 0.8, "source": "code"})
    if paper_value is not None:
        claims.append({"value": paper_value, "weight": 0.6, "source": "paper"})

    if not claims:
        return {
            "resolved": False,
            "reason": "No claims provided",
            "claims": [],
        }

    if len(claims) == 1:
        return {
            "resolved": True,
            "value": claims[0]["value"],
            "confidence": claims[0]["weight"] / 1.0,
            "reason": f"Only source: {claims[0]['source']}",
            "claims": claims,
        }

    # Check for unanimous agreement
    unique_values = {str(c["value"]) for c in claims}
    if len(unique_values) == 1:
        return {
            "resolved": True,
            "value": claims[0]["value"],
            "confidence": 1.0,
            "reason": "All sources agree",
            "claims": claims,
        }

    # Weighted voting
    weighted_scores: dict[str, float] = {}
    for claim in claims:
        val_key = str(claim["value"])
        weighted_scores[val_key] = weighted_scores.get(val_key, 0.0) + claim["weight"]

    winner_value = max(weighted_scores, key=lambda k: weighted_scores[k])
    winner_score = weighted_scores[winner_value]
    runner_up_score = max(
        (w for v, w in weighted_scores.items() if v != winner_value),
        default=0.0,
    )

    # Convert winner_value string back to original type
    winner_original = next(
        c["value"] for c in claims if str(c["value"]) == winner_value
    )

    total_weight = sum(c["weight"] for c in claims)
    confidence = winner_score / total_weight if total_weight > 0 else 0.0

    # 0.3 margin threshold
    if winner_score - runner_up_score >= 0.3:
        return {
            "resolved": True,
            "value": winner_original,
            "confidence": confidence,
            "reason": f"{winner_score:.1f} vs {runner_up_score:.1f} — consensus sufficient",
            "claims": claims,
        }

    return {
        "resolved": False,
        "reason": "Insufficient consensus (margin < 0.3)",
        "claims": claims,
    }


# ── Constraint Graph ──


class ConstraintGraph:
    """Physical constraint graph manager.

    Wraps PhysicalOntology and adds tri-party arbitration, impact analysis,
    and context-aware value resolution.
    """

    def __init__(self, ontology: PhysicalOntology | None = None) -> None:
        self.ontology = ontology or PhysicalOntology()
        self.urdf_data: dict[str, Any] = {}
        self.code_data: dict[str, Any] = {}
        self.paper_data: dict[str, Any] = {}

    # ── Build from sources ──

    def add_urdf_source(self, robot_name: str, urdf_result: dict[str, Any]) -> None:
        """Store URDF parsing result for tri-party arbitration."""
        self.urdf_data[robot_name] = urdf_result

    def add_code_source(self, entity: str, param_name: str, value: float | int | str) -> None:
        """Store code-derived parameter value."""
        key = f"{entity}.{param_name}"
        self.code_data[key] = value

    def add_paper_source(self, entity: str, param_name: str, value: float | int | str) -> None:
        """Store paper-derived parameter value."""
        key = f"{entity}.{param_name}"
        self.paper_data[key] = value

    def resolve_physical_conflict(
        self,
        entity: str,
        property_name: str,
    ) -> dict[str, Any]:
        """Run tri-party arbitration for a specific entity property."""
        key = f"{entity}.{property_name}"

        # Try to get URDF value from ontology property
        urdf_val = None
        node = self.ontology.get_node(key)
        if node and node.node_type == NODE_TYPE_PROPERTY:
            urdf_val = node.metadata.get("value")

        code_val = self.code_data.get(key)
        paper_val = self.paper_data.get(key)

        return tri_party_arbitration(property_name, urdf_val, code_val, paper_val)

    # ── Impact analysis ──

    def get_physical_impact(self, variable: str, radius: int = 3) -> dict[str, Any]:
        """BFS traversal to get physical impact chain within radius hops.

        Returns categorized impacts: hardware, code, properties,
        degradation paths, latency-sensitive nodes, causal chain.
        """
        return self.ontology.bfs_impact_chain(variable, radius=radius)

    # ── Context awareness ──

    def get_context_aware_value(
        self,
        property_name: str,
        context: str = "simulation",
    ) -> dict[str, Any] | None:
        """Get context-adjusted value for a property.

        Checks ontology for context-dependent override first,
        falls back to base property value.
        """
        adjusted = self.ontology.get_context_adjusted_value(property_name, context)
        if adjusted:
            return adjusted

        # Fallback: return base property if no context override
        node = self.ontology.get_node(property_name)
        if node and node.node_type == NODE_TYPE_PROPERTY:
            return {
                "value": node.metadata.get("value"),
                "reason": "Base value (no context override)",
            }
        return None

    def switch_context(self, global_context: str) -> dict[str, Any]:
        """Switch global operating context (simulation | real_world | lab_ice).

        Returns a summary of all adjusted values for the new context.
        """
        adjusted: list[dict[str, Any]] = []
        for node in self.ontology.nodes.values():
            if node.node_type == NODE_TYPE_PROPERTY and "@" in node.name:
                prop_ctx = node.metadata.get("context", "")
                if prop_ctx == global_context:
                    base_name = node.name.split("@")[0]
                    adjusted.append({
                        "property": base_name,
                        "context": global_context,
                        "value": node.metadata.get("value"),
                        "reason": node.metadata.get("reason", ""),
                    })
        return {
            "context": global_context,
            "adjusted_count": len(adjusted),
            "adjusted_properties": adjusted,
        }

    # ── Safety check ──

    def check_physical_constraints(
        self,
        param_name: str,
        proposed_value: float,
    ) -> dict[str, Any]:
        """Runtime physical constraint firewall.

        Checks a proposed parameter value against:
          1. Hardware limits (CONSTRAINED_BY edges)
          2. Degradation paths
          3. Latency constraints
          4. Context-aware adjustments

        Returns safety report with action (ALLOW | REVIEW_REQUIRED | REFUSE).
        """
        impact = self.get_physical_impact(param_name, radius=3)
        violations: list[dict[str, Any]] = []

        # Step 1: Hardware limits
        for edge in self.ontology.get_edges_from(param_name, EDGE_CONSTRAINED_BY):
            limit_val = edge.metadata.get("max_value")
            if limit_val is not None and proposed_value > limit_val:
                violations.append({
                    "severity": SEVERITY_CRITICAL,
                    "property": edge.target,
                    "limit": limit_val,
                    "proposed": proposed_value,
                    "reason": f"Exceeds hardware limit from {edge.metadata.get('source', 'unknown')}",
                })

        # Step 2: Degradation paths
        for deg in impact.get("degradation", []):
            violations.append({
                "severity": SEVERITY_WARNING,
                "degradation_path": deg["path"],
                "mechanism": deg.get("mechanism", ""),
                "reason": f"May cause accelerated degradation: {deg.get('mechanism', '')}",
            })

        # Step 3: Latency constraints
        for lat in impact.get("latency_sensitive", []):
            max_lat = lat.get("max_latency_ms")
            if max_lat is not None and proposed_value > max_lat:
                violations.append({
                    "severity": SEVERITY_CRITICAL,
                    "latency_path": lat["path"],
                    "max_allowed": max_lat,
                    "proposed": proposed_value,
                    "reason": "Violates real-time control loop timing constraint",
                })

        # Step 4: Context awareness
        ctx = self.get_context_aware_value(param_name)
        if ctx and ctx.get("value") is not None:
            ctx_val = ctx["value"]
            try:
                if isinstance(ctx_val, (int, float)) and proposed_value != ctx_val:
                    violations.append({
                        "severity": SEVERITY_WARNING,
                        "property": param_name,
                        "context_value": ctx_val,
                        "proposed": proposed_value,
                        "reason": f"Context-aware value is {ctx_val}, proposed differs",
                    })
            except (TypeError, ValueError):
                pass

        # Determine action
        if any(v["severity"] == SEVERITY_CRITICAL for v in violations):
            safety_level = "CRITICAL"
            action = "REFUSE"
        elif any(v["severity"] == SEVERITY_WARNING for v in violations):
            safety_level = "WARNING"
            action = "REVIEW_REQUIRED"
        else:
            safety_level = "OK"
            action = "ALLOW"

        return {
            "safety_level": safety_level,
            "action": action,
            "violations": violations,
            "causal_chain": impact.get("causal_chain", []),
            "recommendation": _generate_recommendation(violations),
        }

    # ── Export ──

    def export_to_seekdb(self, output_path: str | None = None) -> str:
        """Export constraint graph to JSON file (SeekDB integration stub)."""
        data = {
            "ontology": self.ontology.export_to_dict(),
            "urdf_sources": list(self.urdf_data.keys()),
            "code_sources": len(self.code_data),
            "paper_sources": len(self.paper_data),
        }
        if output_path is None:
            output_path = "data/constraint_graph.json"
        p = Path(output_path)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        logger.info("Constraint graph exported to %s", output_path)
        return str(p)

    def save(self, path: str) -> None:
        self.export_to_seekdb(path)

    @classmethod
    def load(cls, path: str) -> "ConstraintGraph":
        """Load constraint graph from disk."""
        p = Path(path)
        if not p.exists():
            return cls()
        data = json.loads(p.read_text(encoding="utf-8"))
        onto = PhysicalOntology()
        for n in data.get("ontology", {}).get("nodes", []):
            onto.nodes[n["name"]] = PhysicalOntology.__new__(PhysicalOntology)
        # Simpler: just use ontology.load
        onto = PhysicalOntology.load(path.replace("constraint_graph", "physical_ontology"))
        cg = cls(ontology=onto)
        return cg


# ── Helpers ──


def _generate_recommendation(violations: list[dict[str, Any]]) -> str:
    """Generate a human-readable recommendation from violations."""
    if not violations:
        return "No physical constraints violated. Safe to proceed."

    criticals = [v for v in violations if v.get("severity") == SEVERITY_CRITICAL]
    warnings = [v for v in violations if v.get("severity") == SEVERITY_WARNING]

    parts: list[str] = []
    if criticals:
        parts.append(f"CRITICAL: {len(criticals)} hard limit violation(s) detected. Modify parameter or upgrade hardware.")
    if warnings:
        parts.append(f"WARNING: {len(warnings)} degradation/timing concern(s). Review before deployment.")

    return " ".join(parts)


__all__ = [
    "ConstraintGraph",
    "tri_party_arbitration",
]
