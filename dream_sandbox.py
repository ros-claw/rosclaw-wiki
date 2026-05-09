"""Dream Sandbox — safety wrapper for dream cycle operations.

Ensures dream LLM cannot directly mutate wiki content.
All modifications go through whitelisted safe functions.
Auto-rollback on test failure.
"""

from __future__ import annotations

import json
import logging
import shutil
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Any, Callable

logger = logging.getLogger("rosclaw.dream_sandbox")

# Whitelisted safe operations
def _safe_repair_links(wiki_root: str) -> dict[str, Any]:
    import dream_cycle
    return dream_cycle.repair_broken_links(wiki_root)


def _safe_reinforce(wiki_root: str) -> list[dict[str, Any]]:
    import dream_cycle
    return dream_cycle.reinforce_low_confidence(wiki_root)


def _safe_insights(wiki_root: str) -> list[dict[str, Any]]:
    import dream_cycle
    return dream_cycle.generate_insights(wiki_root)


def _safe_update_index(wiki_root: str) -> str:
    import wiki_engine as engine
    return engine.update_index(wiki_root)


_SAFE_OPS: dict[str, Callable[..., Any]] = {
    "repair_links": _safe_repair_links,
    "reinforce": _safe_reinforce,
    "insights": _safe_insights,
    "update_index": _safe_update_index,
}


def _git_snapshot(wiki_root: str) -> str | None:
    """Create a git commit snapshot before dream runs."""
    root = Path(wiki_root)
    git_dir = root / ".git"
    if not git_dir.exists():
        # Initialize git if not present
        try:
            subprocess.run(["git", "init"], cwd=str(root), capture_output=True, check=True)
            subprocess.run(["git", "add", "."], cwd=str(root), capture_output=True, check=True)
            subprocess.run(
                ["git", "commit", "-m", "dream_pre_snapshot", "--no-gpg-sign"],
                cwd=str(root), capture_output=True, check=True,
            )
        except subprocess.CalledProcessError:
            return None

    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=str(root), capture_output=True, text=True, check=True,
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        return None


def _git_rollback(wiki_root: str, commit: str) -> bool:
    """Rollback wiki to a specific commit."""
    try:
        subprocess.run(
            ["git", "reset", "--hard", commit],
            cwd=str(wiki_root), capture_output=True, check=True,
        )
        logger.warning("Dream rollback executed to %s", commit[:8])
        return True
    except subprocess.CalledProcessError as exc:
        logger.error("Dream rollback failed: %s", exc)
        return False


def run_safe(wiki_root: str, operation: str, *args: Any, **kwargs: Any) -> dict[str, Any]:
    """Execute a whitelisted dream operation inside the sandbox.

    Args:
        wiki_root: Wiki root path.
        operation: Name of whitelisted operation.
        *args, **kwargs: Passed to the operation.

    Returns:
        Dict with result and safety info.
    """
    if operation not in _SAFE_OPS:
        return {
            "status": "blocked",
            "error": f"Operation '{operation}' is not in the dream whitelist",
            "allowed": list(_SAFE_OPS.keys()),
        }

    # Snapshot
    snapshot = _git_snapshot(wiki_root)

    try:
        func = _SAFE_OPS[operation]
        result = func(wiki_root, *args, **kwargs)
        return {
            "status": "ok",
            "operation": operation,
            "result": result,
            "snapshot": snapshot,
        }
    except Exception as exc:
        logger.error("Dream operation %s failed: %s", operation, exc)
        if snapshot:
            _git_rollback(wiki_root, snapshot)
        return {
            "status": "error",
            "operation": operation,
            "error": str(exc),
            "rolled_back": snapshot is not None,
        }


def run_tests_guarded(wiki_root: str, test_cmd: list[str] | None = None) -> dict[str, Any]:
    """Run tests after a dream cycle; rollback on failure.

    Args:
        wiki_root: Wiki root.
        test_cmd: Command list, defaults to ["python", "-m", "pytest", "test_e2e.py", "-q"].

    Returns:
        Dict with test_result, passed, snapshot_used.
    """
    if test_cmd is None:
        test_cmd = ["python", "-m", "pytest", "test_e2e.py", "-q"]

    snapshot = _git_snapshot(wiki_root)

    try:
        result = subprocess.run(
            test_cmd,
            cwd=str(Path(wiki_root).parent),
            capture_output=True,
            text=True,
        )
        passed = result.returncode == 0
        if not passed and snapshot:
            _git_rollback(wiki_root, snapshot)
        return {
            "tests_passed": passed,
            "returncode": result.returncode,
            "stdout": result.stdout[-500:],
            "stderr": result.stderr[-500:],
            "rolled_back": not passed and snapshot is not None,
        }
    except Exception as exc:
        if snapshot:
            _git_rollback(wiki_root, snapshot)
        return {
            "tests_passed": False,
            "error": str(exc),
            "rolled_back": snapshot is not None,
        }


__all__ = [
    "run_safe",
    "run_tests_guarded",
    "_SAFE_OPS",
]
