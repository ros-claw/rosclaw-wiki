"""Simple cross-platform file locking utility.

Uses fcntl on Unix, and a global thread-safe fallback for environments
where fcntl is unavailable.
"""

from __future__ import annotations

import logging
import threading
from contextlib import contextmanager
from pathlib import Path
from typing import Any

logger = logging.getLogger("rosclaw.file_lock")

# In-process fallback lock table (for Windows or fcntl unavailable)
_fallback_locks: dict[str, threading.Lock] = {}
_fallback_lock_table_lock = threading.Lock()


def _get_fallback_lock(path: str) -> threading.Lock:
    """Return a per-path thread lock for in-process serialization."""
    with _fallback_lock_table_lock:
        return _fallback_locks.setdefault(path, threading.Lock())


@contextmanager
def acquire_lock(lock_path: str | Path):
    """Acquire a file lock for the given path.

    On Unix with fcntl available, uses an advisory file lock.
    Otherwise falls back to an in-process thread lock.

    Usage:
        with acquire_lock("/path/to/file"):
            # exclusive access
    """
    path = str(lock_path)
    lock_file: Any | None = None
    fcntl_module: Any | None = None

    try:
        import fcntl
        fcntl_module = fcntl
    except ImportError:
        pass

    if fcntl_module is not None:
        # Use fcntl advisory lock
        lock_file_path = Path(path).parent / (Path(path).name + ".lock")
        lock_file = open(str(lock_file_path), "w")
        try:
            fcntl_module.flock(lock_file.fileno(), fcntl_module.LOCK_EX)
        except Exception as exc:
            logger.warning("fcntl flock failed for %s: %s", path, exc)
            lock_file.close()
            lock_file = None

    if lock_file is None:
        # Fallback to thread lock
        thread_lock = _get_fallback_lock(path)
        thread_lock.acquire()

    try:
        yield
    finally:
        if lock_file is not None:
            try:
                fcntl_module.flock(lock_file.fileno(), fcntl_module.LOCK_UN)
            except Exception:
                pass
            try:
                lock_file.close()
            except Exception:
                pass
            # Clean up lock file
            try:
                lock_file_path = Path(path).parent / (Path(path).name + ".lock")
                if lock_file_path.exists():
                    lock_file_path.unlink()
            except Exception:
                pass
        else:
            thread_lock = _get_fallback_lock(path)
            thread_lock.release()
