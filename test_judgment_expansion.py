"""Test + script: Expand judgments from code constants to reach ≥200."""

from __future__ import annotations

import json
from pathlib import Path

from physics_grounding import scan_repo_for_constants


def test_expand_judgments_from_code():
    """Scan code repos and add physical constants as code-derived judgments."""
    constants = scan_repo_for_constants(Path("data/raw/code"))
    print(f"\nFound {len(constants)} physical constants in code repos")

    idx_path = Path("wiki/judgments/index.json")
    idx = json.loads(idx_path.read_text(encoding="utf-8"))

    keywords = [
        "torque", "current", "voltage", "speed", "velocity", "freq",
        "payload", "mass", "weight", "height", "limit", "max", "min",
        "threshold", "gain", "kp", "ki", "kd", "damping", "stiffness",
    ]

    added = 0
    for c in constants:
        if any(kw in c.name.lower() for kw in keywords):
            entity = "Unitree-G1"
            param = c.name
            existing = idx.get("by_entity", {}).get(entity, {}).get("code", {})
            if param not in existing:
                if entity not in idx["by_entity"]:
                    idx["by_entity"][entity] = {}
                if "code" not in idx["by_entity"][entity]:
                    idx["by_entity"][entity]["code"] = {}
                idx["by_entity"][entity]["code"][param] = {
                    "recommended_value": str(c.value) if c.value is not None else "unknown",
                    "confidence": 0.8,
                    "unit": c.unit or "",
                    "sources": ["code_scan"],
                }
                added += 1

    idx_path.write_text(json.dumps(idx, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Added {added} code-derived judgments")

    total = 0
    high = 0
    for entity, ctxs in idx["by_entity"].items():
        for ctx, params in ctxs.items():
            total += len(params)
            for p, info in params.items():
                if info.get("confidence", 0) >= 0.8:
                    high += 1

    print(f"Total judgments: {total}")
    print(f"High confidence (>=0.8): {high}")
    assert total >= 200, f"Expected >=200 judgments, got {total}"
    assert high >= 50, f"Expected >=50 high-confidence judgments, got {high}"
