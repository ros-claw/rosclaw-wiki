"""Safety boundary tests for Phase 14 Module 3.

Tests:
1. _check_safety_boundary for green/amber/red cases
2. generate_code_framework respects safety boundaries
3. sync_check detects parameter mismatches
"""
from __future__ import annotations

import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from code_generator import _check_safety_boundary, generate_code_framework, sync_check


def test_check_safety_boundary_green():
    """Value < 80% of limit → green."""
    severity, is_safe = _check_safety_boundary("TEST", 50.0, 100.0)
    assert severity == "green"
    assert is_safe is True


def test_check_safety_boundary_amber():
    """Value >= 80% but < 100% of limit → amber."""
    severity, is_safe = _check_safety_boundary("TEST", 85.0, 100.0)
    assert severity == "amber"
    assert is_safe is True


def test_check_safety_boundary_red():
    """Value >= limit → red."""
    severity, is_safe = _check_safety_boundary("TEST", 110.0, 100.0)
    assert severity == "red"
    assert is_safe is False


def test_check_safety_boundary_exact_limit():
    """Value exactly at limit → red (100% >= 100%)."""
    severity, is_safe = _check_safety_boundary("TEST", 100.0, 100.0)
    assert severity == "red"
    assert is_safe is False


def test_check_safety_boundary_at_80pct():
    """Value exactly 80% → amber."""
    severity, is_safe = _check_safety_boundary("TEST", 80.0, 100.0)
    assert severity == "amber"
    assert is_safe is True


def test_check_safety_boundary_no_limit():
    """No hardware limit provided → green."""
    severity, is_safe = _check_safety_boundary("TEST", 999.0, None)
    assert severity == "green"
    assert is_safe is True


def test_generate_code_with_safe_param():
    """Normal parameter within spec generates normally."""
    result = generate_code_framework("Unitree-G1", wiki_root=".", language="python")
    assert result["status"] == "generated"
    code = result["code"]
    assert "MAX_TORQUE" in code
    # Should NOT have CRITICAL for normal params
    assert "[!CRITICAL]" not in code


def test_generate_code_blocked_for_red():
    """Parameter exceeding hardware limit is rejected."""
    # Test-Overlimit has DANGER_PARAM = 999 with limit 100
    result = generate_code_framework("Test-Overlimit", wiki_root=".", language="python")
    assert result["status"] == "generated"
    code = result["code"]
    assert "[!CRITICAL]" in code
    assert "DANGER_PARAM" in code
    assert "REFUSED" in code
    assert any("exceeds hardware limit" in w for w in result["warnings"])


def test_generate_code_amber_for_near_limit():
    """Parameter >= 80% of limit triggers amber warning."""
    # Test-NearLimit has WARNING_PARAM = 95 with limit 100 (95%)
    result = generate_code_framework("Test-NearLimit", wiki_root=".", language="python")
    assert result["status"] == "generated"
    code = result["code"]
    assert "[!WARNING]" in code
    assert any(">=80% of hardware limit" in w for w in result["warnings"])


def test_sync_check_detects_mismatch():
    """sync_check finds outdated parameter in code."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
        f.write("MAX_TORQUE = 300\n")
        f.write("STEP_HEIGHT = 0.12\n")
        temp_path = f.name

    try:
        result = sync_check("Unitree-G1", wiki_root=".", code_paths=[temp_path])
        assert result["status"] == "done"
        assert result["discrepancies"] >= 1
        assert any(
            f["parameter"] == "MAX_TORQUE" and f["code_value"] == 300.0
            for f in result["findings"]
        )
        assert "Outdated Code Found" in result["report"]
        assert len(result["warnings"]) >= 1
    finally:
        Path(temp_path).unlink()


def test_sync_check_no_mismatch():
    """sync_check passes when code matches judgment."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
        f.write("MAX_TORQUE = 237\n")
        temp_path = f.name

    try:
        result = sync_check("Unitree-G1", wiki_root=".", code_paths=[temp_path])
        assert result["status"] == "done"
        # MAX_TORQUE matches judgment, so no discrepancy
        assert result["discrepancies"] == 0
        assert "No discrepancies found" in result["report"]
    finally:
        Path(temp_path).unlink()


def test_sync_check_no_judgments():
    """sync_check handles entity with no judgments."""
    result = sync_check("NonExistent-Entity", wiki_root=".", code_paths=[])
    assert result["status"] == "no_judgments"
    assert result["discrepancies"] == 0


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])
