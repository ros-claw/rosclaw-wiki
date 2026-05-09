"""SeekDB Collection Client — pyseekdb wrapper for document + vector storage.

Supports both Embedded and Single-node Server modes via SEEKDB_MODE env var.
Implements a connection pool (max 20) for server mode to avoid concurrency issues.
Auth/billing tables remain in SQLite (seekdb_client.py) for SQL aggregate queries.

Environment variables:
  SEEKDB_MODE      — "server" (default) or "embedded"
  SEEKDB_HOST      — server host (default: 127.0.0.1)
  SEEKDB_PORT      — server port (default: 2881)
  SEEKDB_DATABASE  — database name (default: rosclaw_wiki)
  SEEKDB_USER      — user (default: root)
  SEEKDB_PATH      — embedded data path (default: ./seekdb_data)
"""
from __future__ import annotations

import logging
import os
from queue import Queue
from typing import Any

logger = logging.getLogger("rosclaw.seekdb_collection")

# ── Module-level singletons ──
_CLIENT: Any | None = None
_WIKI_COLLECTION: Any | None = None
_JUDGMENTS_COLLECTION: Any | None = None

# ── Connection pool (server mode only) ──
_POOL_MAX_SIZE = 20
_connection_pool: Queue[Any] | None = None


def _pool_get() -> Any | None:
    """Try to get a reusable client from the pool."""
    global _connection_pool
    if _connection_pool is not None:
        try:
            return _connection_pool.get_nowait()
        except Exception:
            pass
    return None


def _pool_put(conn: Any) -> None:
    """Return a client to the pool."""
    global _connection_pool
    if _connection_pool is not None:
        try:
            _connection_pool.put_nowait(conn)
        except Exception:
            try:
                conn.close()
            except Exception:
                pass


def _pool_init() -> None:
    """Initialize the connection pool."""
    global _connection_pool
    if _connection_pool is None:
        _connection_pool = Queue(maxsize=_POOL_MAX_SIZE)


def _create_new_connection() -> Any:
    """Create a fresh pyseekdb Client based on current mode."""
    import pyseekdb

    mode = os.environ.get("SEEKDB_MODE", "server")

    if mode == "server":
        host = os.environ.get("SEEKDB_HOST", "127.0.0.1")
        port = int(os.environ.get("SEEKDB_PORT", "2881"))
        database = os.environ.get("SEEKDB_DATABASE", "rosclaw_wiki")
        user = os.environ.get("SEEKDB_USER", "root")

        logger.info("pyseekdb Client connecting to server %s:%d (database=%s)", host, port, database)
        client = pyseekdb.Client(
            host=host,
            port=port,
            database=database,
            user=user,
        )
    else:
        path = os.environ.get("SEEKDB_PATH", "./seekdb_data")
        database = os.environ.get("SEEKDB_DATABASE", "rosclaw_wiki")

        logger.info("pyseekdb Client initializing embedded mode (path=%s)", path)
        client = pyseekdb.Client(
            path=path,
            database=database,
        )

    return client


def _get_client() -> Any:
    global _CLIENT
    if _CLIENT is not None:
        return _CLIENT

    # Initialize pool for server mode
    mode = os.environ.get("SEEKDB_MODE", "server")
    if mode == "server":
        _pool_init()
        pooled = _pool_get()
        if pooled is not None:
            _CLIENT = pooled
            return _CLIENT

    _CLIENT = _create_new_connection()
    return _CLIENT


def get_wiki_collection() -> Any:
    global _WIKI_COLLECTION
    if _WIKI_COLLECTION is None:
        client = _get_client()
        _WIKI_COLLECTION = client.get_or_create_collection(
            name="wiki_pages",
        )
    return _WIKI_COLLECTION


def get_judgments_collection() -> Any:
    global _JUDGMENTS_COLLECTION
    if _JUDGMENTS_COLLECTION is None:
        client = _get_client()
        _JUDGMENTS_COLLECTION = client.get_or_create_collection(
            name="judgments",
        )
    return _JUDGMENTS_COLLECTION


def health_check() -> dict[str, Any]:
    try:
        client = _get_client()
        collections = client.list_collections()
        wiki_count = get_wiki_collection().count()
        judgment_count = get_judgments_collection().count()
        mode = os.environ.get("SEEKDB_MODE", "server")
        return {
            "status": "ok",
            "backend": "pyseekdb",
            "mode": mode,
            "collections": len(collections),
            "wiki_pages": wiki_count,
            "judgments": judgment_count,
        }
    except Exception as exc:
        return {"status": "error", "error": str(exc)}


def reset_client() -> None:
    global _CLIENT, _WIKI_COLLECTION, _JUDGMENTS_COLLECTION, _connection_pool
    _WIKI_COLLECTION = None
    _JUDGMENTS_COLLECTION = None
    if _CLIENT is not None:
        try:
            _CLIENT.close()
        except Exception:
            pass
        _CLIENT = None
    if _connection_pool is not None:
        while not _connection_pool.empty():
            try:
                conn = _connection_pool.get_nowait()
                conn.close()
            except Exception:
                pass
        _connection_pool = None


__all__ = [
    "get_wiki_collection",
    "get_judgments_collection",
    "health_check",
    "reset_client",
    "_pool_get",
    "_pool_put",
]
