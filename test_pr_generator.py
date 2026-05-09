"""Tests for pr_generator.py — Phase 13 auto PR pipeline."""

from __future__ import annotations

import json
import tempfile
from pathlib import Path

import pytest

from code_generator import sync_check
from pr_generator import generate_pr, submit_pr


@pytest.fixture
def mock_code_with_params():
    """Create a temp Python file with outdated params."""
    code = """
MAX_TORQUE = 300
MAX_VELOCITY = 4.0
STEP_HEIGHT = 0.15
"""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
        f.write(code)
        return f.name


@pytest.fixture
def mock_code_safe():
    """Create a temp Python file with matching params."""
    code = """
MAX_TORQUE = 237
MAX_VELOCITY = 3.5
"""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
        f.write(code)
        return f.name


def test_generate_pr_no_changes():
    """PR generator returns no_changes when sync finds nothing."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
        f.write("MAX_TORQUE = 237\n")
        path = f.name

    result = generate_pr("Unitree-G1", "wiki", code_paths=[path])
    assert result["status"] == "no_changes"
    assert result["pr"] is None


def test_generate_pr_normal():
    """PR generator creates PR for normal (safe) discrepancies.

    Uses UR5-Arm SAFETY_MARGIN (0.05 vs limit 0.1 = 50% — well under 90%).
    """
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
        f.write("SAFETY_MARGIN = 0.02\n")
        path = f.name

    result = generate_pr("UR5-Arm", "wiki", code_paths=[path])
    assert result["status"] == "created"
    assert result["pr"] is not None
    assert "auto-generated" in result["pr"]["labels"]
    assert "needs-review" not in result["pr"]["labels"]


def test_generate_pr_red():
    """PR generator refuses PR for over-limit parameters (RED)."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
        f.write("DANGER_PARAM = 50\n")
        path = f.name

    result = generate_pr("Test-Overlimit", "wiki", code_paths=[path])
    assert result["status"] == "red"
    assert result["pr"] is None
    assert "REFUSED" in result["report"]


def test_generate_pr_amber():
    """PR generator adds needs-review label for near-limit parameters (AMBER)."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
        f.write("WARNING_PARAM = 80\n")
        path = f.name

    result = generate_pr("Test-NearLimit", "wiki", code_paths=[path])
    assert result["status"] == "amber"
    assert result["pr"] is not None
    assert "needs-review" in result["pr"]["labels"]
    assert "warning" in result["pr"]["labels"]


def test_sync_check_auto_pr_false():
    """sync_check with auto_pr=False does not generate PR data."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
        f.write("SAFETY_MARGIN = 0.02\n")
        path = f.name

    result = sync_check("UR5-Arm", "wiki", code_paths=[path], auto_pr=False)
    assert result["status"] == "done"
    assert "pr_data" not in result


def test_sync_check_auto_pr_true():
    """sync_check with auto_pr=True generates PR data for safe changes."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
        f.write("SAFETY_MARGIN = 0.02\n")
        path = f.name

    result = sync_check("UR5-Arm", "wiki", code_paths=[path], auto_pr=True)
    assert result["status"] == "done"
    assert "pr_data" in result
    assert result["pr_status"] == "created"
    assert result["pr_submitted"] is True
    assert "pr_file" in result


def test_sync_check_auto_pr_red():
    """sync_check with auto_pr=True refuses PR for RED findings."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
        f.write("DANGER_PARAM = 50\n")
        path = f.name

    result = sync_check("Test-Overlimit", "wiki", code_paths=[path], auto_pr=True)
    assert result["status"] == "red"
    assert result["pr_status"] == "red"
    assert "pr_data" not in result or result.get("pr_data") is None


def test_submit_pr_writes_file():
    """submit_pr writes PR content to data/prs/."""
    pr_data = {
        "entity": "Unitree-G1",
        "pr": {
            "title": "Test PR",
            "body": "## Test\nBody here",
            "labels": ["auto-generated"],
            "findings": [],
        },
    }
    result = submit_pr(pr_data)
    assert result["status"] == "submitted"
    assert Path(result["file"]).exists()
