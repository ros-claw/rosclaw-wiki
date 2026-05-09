"""Simple cross-process event bus using JSONL file.

Allows CLI scripts (e.g., batch_ingest.py) to emit events that the Web UI
picks up via SocketIO real-time push.
"""

from __future__ import annotations

import json
import logging
import time
from pathlib import Path
from typing import Any

logger = logging.getLogger("rosclaw.events")

DEFAULT_EVENT_LOG = Path("data/events.jsonl")
DEFAULT_ROTATION_BYTES = 10 * 1024 * 1024  # 10 MB


def _rotate_if_needed(log_path: Path, max_bytes: int = DEFAULT_ROTATION_BYTES) -> Path:
    """Rotate log file if it exceeds max_bytes. Returns the active log path."""
    if not log_path.exists():
        return log_path

    try:
        size = log_path.stat().st_size
    except Exception:
        return log_path

    if size < max_bytes:
        return log_path

    # Rotate: events.jsonl -> events.jsonl.1, existing .1 -> .2, etc.
    for i in range(4, 0, -1):
        older = log_path.parent / f"{log_path.name}.{i}"
        newer = log_path.parent / f"{log_path.name}.{i + 1}"
        if older.exists():
            try:
                older.replace(newer)
            except Exception:
                pass

    first_backup = log_path.parent / f"{log_path.name}.1"
    try:
        log_path.replace(first_backup)
    except Exception as exc:
        logger.warning("Failed to rotate event log: %s", exc)

    return log_path


def emit(
    event_type: str,
    payload: dict[str, Any],
    *,
    event_log: Path | None = None,
    max_bytes: int = DEFAULT_ROTATION_BYTES,
) -> None:
    """Append an event to the shared JSONL log.

    Args:
        event_type: Event name (e.g., "ingest_progress", "conflict_alert").
        payload: Arbitrary JSON-serializable dict.
        event_log: Override the default log path.
        max_bytes: Rotate log when it exceeds this size.
    """
    log_path = event_log or DEFAULT_EVENT_LOG
    log_path.parent.mkdir(parents=True, exist_ok=True)
    log_path = _rotate_if_needed(log_path, max_bytes)
    record = {
        "t": time.time(),
        "type": event_type,
        "payload": payload,
    }
    try:
        with log_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
    except Exception as exc:
        logger.warning("Failed to emit event %s: %s", event_type, exc)


def tail_events(
    since: float = 0,
    *,
    event_log: Path | None = None,
) -> list[dict[str, Any]]:
    """Read events newer than ``since`` timestamp.

    Args:
        since: Unix timestamp; only events with ``t > since`` are returned.
        event_log: Override the default log path.

    Returns:
        List of event dicts ordered by time.
    """
    log_path = event_log or DEFAULT_EVENT_LOG
    if not log_path.exists():
        return []

    events: list[dict[str, Any]] = []
    try:
        with log_path.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    evt = json.loads(line)
                    if evt.get("t", 0) > since:
                        events.append(evt)
                except json.JSONDecodeError:
                    continue
    except Exception as exc:
        logger.warning("Failed to tail events: %s", exc)

    return events


def clear_events(*, event_log: Path | None = None) -> None:
    """Truncate the event log."""
    log_path = event_log or DEFAULT_EVENT_LOG
    if log_path.exists():
        log_path.unlink()


__all__ = ["emit", "tail_events", "clear_events", "DEFAULT_EVENT_LOG", "DEFAULT_ROTATION_BYTES", "_rotate_if_needed"]
