"""Seed synthetic judgments for common robot hardware parameters.

Usage:
    python scripts/seed_judgments.py
"""
from __future__ import annotations

import json
import logging
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from seekdb_client import get_connection

logger = logging.getLogger("rosclaw.seed_judgments")


SEED_JUDGMENTS: list[dict] = [
    {
        "entity": "Unitree-G1",
        "context": "hardware",
        "parameter": "MAX_TORQUE",
        "recommended_value": "237",
        "unit": "N·m",
        "confidence": 0.92,
        "sources": ["[[Unitree-G1-Spec]]", "[[G1-Torque-Analysis]]"],
        "hardware_limit": 250,
        "conflicts_resolved": 1,
        "resolution_method": "authority_weighted",
        "usage_notes": "Peak torque per hip actuator. 95% of hardware limit.",
    },
    {
        "entity": "Unitree-G1",
        "context": "hardware",
        "parameter": "MAX_VELOCITY",
        "recommended_value": "3.5",
        "unit": "m/s",
        "confidence": 0.88,
        "sources": ["[[Unitree-G1-Spec]]"],
        "hardware_limit": 4.0,
        "conflicts_resolved": 1,
        "resolution_method": "authority_weighted",
        "usage_notes": "Maximum walking speed. 87.5% of hardware limit.",
    },
    {
        "entity": "Unitree-G1",
        "context": "hardware",
        "parameter": "STEP_HEIGHT",
        "recommended_value": "0.12",
        "unit": "m",
        "confidence": 0.85,
        "sources": ["[[G1-Gait-Study]]", "[[Unitree-G1-Spec]]"],
        "hardware_limit": 0.15,
        "conflicts_resolved": 1,
        "resolution_method": "authority_weighted",
        "usage_notes": "Nominal step height for flat terrain. 80% of hardware limit.",
    },
    {
        "entity": "Unitree-G1",
        "context": "hardware",
        "parameter": "JOINT_LIMIT_HIP_ROLL",
        "recommended_value": "45",
        "unit": "deg",
        "confidence": 0.90,
        "sources": ["[[Unitree-G1-Spec]]"],
        "hardware_limit": 50,
        "conflicts_resolved": 1,
        "resolution_method": "authority_weighted",
        "usage_notes": "Hip roll joint limit. 90% of mechanical limit.",
    },
    {
        "entity": "Unitree-G1",
        "context": "hardware",
        "parameter": "CONTROL_FREQUENCY",
        "recommended_value": "1000",
        "unit": "Hz",
        "confidence": 0.95,
        "sources": ["[[Unitree-G1-Spec]]", "[[ROS2-Control-Guide]]"],
        "hardware_limit": 1200,
        "conflicts_resolved": 1,
        "resolution_method": "authority_weighted",
        "usage_notes": "Motor control loop frequency. 83% of max supported.",
    },
    {
        "entity": "UR5-Arm",
        "context": "hardware",
        "parameter": "MAX_PAYLOAD",
        "recommended_value": "5.0",
        "unit": "kg",
        "confidence": 0.94,
        "sources": ["[[UR5-Datasheet]]"],
        "hardware_limit": 5.0,
        "conflicts_resolved": 1,
        "resolution_method": "authority_weighted",
        "usage_notes": "Maximum payload at full reach. At 100% of limit — requires [!WARNING].",
    },
    {
        "entity": "UR5-Arm",
        "context": "hardware",
        "parameter": "REACH_RADIUS",
        "recommended_value": "0.85",
        "unit": "m",
        "confidence": 0.91,
        "sources": ["[[UR5-Datasheet]]"],
        "hardware_limit": 0.85,
        "conflicts_resolved": 1,
        "resolution_method": "authority_weighted",
        "usage_notes": "Maximum reach radius.",
    },
    {
        "entity": "UR5-Arm",
        "context": "hardware",
        "parameter": "SAFETY_MARGIN",
        "recommended_value": "0.05",
        "unit": "m",
        "confidence": 0.89,
        "sources": ["[[UR5-Safety-Guide]]", "[[ISO-10218]]"],
        "hardware_limit": 0.10,
        "conflicts_resolved": 1,
        "resolution_method": "authority_weighted",
        "usage_notes": "Minimum distance to human worker. 50% of regulatory limit.",
    },
    {
        "entity": "TurtleBot3",
        "context": "hardware",
        "parameter": "MAX_LINEAR_VEL",
        "recommended_value": "0.26",
        "unit": "m/s",
        "confidence": 0.87,
        "sources": ["[[TurtleBot3-Spec]]"],
        "hardware_limit": 0.30,
        "conflicts_resolved": 1,
        "resolution_method": "authority_weighted",
        "usage_notes": "Maximum linear velocity (Burger model). 87% of hardware limit.",
    },
    {
        "entity": "TurtleBot3",
        "context": "hardware",
        "parameter": "MAX_ANGULAR_VEL",
        "recommended_value": "1.8",
        "unit": "rad/s",
        "confidence": 0.86,
        "sources": ["[[TurtleBot3-Spec]]"],
        "hardware_limit": 2.0,
        "conflicts_resolved": 1,
        "resolution_method": "authority_weighted",
        "usage_notes": "Maximum angular velocity (Burger model). 90% of hardware limit.",
    },
    {
        "entity": "Test-Overlimit",
        "context": "safety_test",
        "parameter": "DANGER_PARAM",
        "recommended_value": "999",
        "unit": "N·m",
        "confidence": 0.80,
        "sources": ["[[Test-Safety]]"],
        "hardware_limit": 100,
        "conflicts_resolved": 1,
        "resolution_method": "authority_weighted",
        "usage_notes": "Test parameter for CRITICAL boundary check. Exceeds hardware limit by 10x.",
    },
    {
        "entity": "Test-NearLimit",
        "context": "safety_test",
        "parameter": "WARNING_PARAM",
        "recommended_value": "95",
        "unit": "%",
        "confidence": 0.80,
        "sources": ["[[Test-Safety]]"],
        "hardware_limit": 100,
        "conflicts_resolved": 1,
        "resolution_method": "authority_weighted",
        "usage_notes": "Test parameter for WARNING boundary check. At 95% of hardware limit.",
    },
]


def seed_judgments() -> dict:
    """Insert seed judgments into SQLite and pyseekdb."""
    try:
        from seekdb_collection_client import get_judgments_collection
    except Exception:
        get_judgments_collection = None

    with get_connection() as conn:
        imported = 0
        for j in SEED_JUDGMENTS:
            j_id = f"{j['entity']}:{j['parameter']}"
            try:
                conn.execute(
                    """
                    INSERT INTO judgments (id, entity, context, parameter, recommended_value, confidence, sources, conflicts_resolved, resolution_method, usage_notes)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ON CONFLICT(id) DO UPDATE SET
                        entity=excluded.entity, context=excluded.context, parameter=excluded.parameter,
                        recommended_value=excluded.recommended_value, confidence=excluded.confidence,
                        sources=excluded.sources, conflicts_resolved=excluded.conflicts_resolved,
                        resolution_method=excluded.resolution_method, usage_notes=excluded.usage_notes
                    """,
                    (
                        j_id,
                        j["entity"],
                        j["context"],
                        j["parameter"],
                        j["recommended_value"],
                        j["confidence"],
                        json.dumps(j["sources"], ensure_ascii=False),
                        j["conflicts_resolved"],
                        j["resolution_method"],
                        j["usage_notes"],
                    ),
                )
                imported += 1
            except Exception as exc:
                logger.warning("SQLite insert error for %s: %s", j_id, exc)
        conn.commit()

    # Also update pyseekdb judgments collection
    coll = None
    if get_judgments_collection is not None:
        try:
            coll = get_judgments_collection()
        except Exception:
            coll = None
    if coll is not None:
        for j in SEED_JUDGMENTS:
            j_id = f"{j['entity']}:{j['parameter']}"
            doc = json.dumps({
                "entity": j["entity"],
                "context": j["context"],
                "parameter": j["parameter"],
                "recommended_value": j["recommended_value"],
                "confidence": j["confidence"],
                "conflicts_resolved": bool(j["conflicts_resolved"]),
                "usage_notes": j["usage_notes"],
            }, ensure_ascii=False)
            try:
                coll.upsert(
                    ids=[j_id],
                    documents=[doc],
                    metadatas=[{
                        "entity": j["entity"],
                        "context": j["context"],
                        "parameter": j["parameter"],
                        "confidence": j["confidence"],
                    }]
                )
            except Exception as exc:
                logger.warning("pyseekdb insert error for %s: %s", j_id, exc)

    # Update index.json
    index_path = Path("wiki/judgments/index.json")
    index_data = {
        "version": "2.0.0",
        "generated_at": datetime.now().isoformat(),
        "total_judgments": len(SEED_JUDGMENTS),
        "by_entity": {},
        "by_context": {},
    }
    for j in SEED_JUDGMENTS:
        entity = j["entity"]
        context = j["context"]
        param = j["parameter"]
        if entity not in index_data["by_entity"]:
            index_data["by_entity"][entity] = {}
        if context not in index_data["by_entity"][entity]:
            index_data["by_entity"][entity][context] = {}
        index_data["by_entity"][entity][context][param] = {
            "recommended_value": j["recommended_value"],
            "confidence": j["confidence"],
            "unit": j.get("unit", ""),
            "hardware_limit": j.get("hardware_limit"),
            "sources": j["sources"],
            "conflicts_resolved": [f"Resolved via {j['resolution_method']}"],
            "resolution_method": j["resolution_method"],
            "usage_notes": j["usage_notes"],
        }
        if context not in index_data["by_context"]:
            index_data["by_context"][context] = {}
        if entity not in index_data["by_context"][context]:
            index_data["by_context"][context][entity] = []
        index_data["by_context"][context][entity].append(param)

    index_path.parent.mkdir(parents=True, exist_ok=True)
    index_path.write_text(json.dumps(index_data, ensure_ascii=False, indent=2))

    logger.info("Seeded %d judgments (%d SQLite + pyseekdb)", imported, imported)
    return {"status": "done", "imported": imported, "total": len(SEED_JUDGMENTS)}


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    result = seed_judgments()
    print(result)
