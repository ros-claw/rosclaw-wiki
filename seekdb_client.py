"""SeekDB Client — connection management for Phase 11.

Uses SQLite as a compatibility layer when SeekDB is not available.
When SeekDB is installed, swap _connect_sqlite() for _connect_seekdb().
"""

from __future__ import annotations

import logging
import os
import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Generator

logger = logging.getLogger("rosclaw.seekdb_client")

_DEFAULT_DB_PATH = os.environ.get("SEEKDB_SQLITE_PATH", "data/seekdb_compat.db")


def _get_db_path() -> str:
    return _DEFAULT_DB_PATH


def _ensure_schema(conn: sqlite3.Connection) -> None:
    """Create tables if they don't exist (SQLite compatibility mode)."""
    conn.executescript("""
    CREATE TABLE IF NOT EXISTS wiki_pages (
        id TEXT PRIMARY KEY,
        type TEXT NOT NULL,
        title TEXT NOT NULL,
        body TEXT,
        tags TEXT,         -- JSON array stored as text
        confidence REAL DEFAULT 0.5,
        created_at TEXT,
        last_reinforced TEXT,
        sources TEXT,      -- JSON
        embedding TEXT,    -- JSON array of floats
        wikilinks TEXT,    -- JSON array
        entity_relations TEXT, -- JSON
        tenant_id TEXT DEFAULT 'default'
    );

    CREATE TABLE IF NOT EXISTS judgments (
        id TEXT PRIMARY KEY,
        entity TEXT NOT NULL,
        context TEXT,
        parameter TEXT NOT NULL,
        recommended_value TEXT NOT NULL,
        confidence REAL DEFAULT 0.0,
        sources TEXT,
        conflicts_resolved INTEGER DEFAULT 0,
        resolution_method TEXT,
        usage_notes TEXT,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        updated_at TEXT DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS api_usage (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        api_key_hash TEXT NOT NULL,
        tenant_id TEXT,
        endpoint TEXT NOT NULL,
        search_type TEXT,
        tokens_used INTEGER DEFAULT 0,
        latency_ms INTEGER,
        status_code INTEGER,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS entity_graph (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        source_entity TEXT NOT NULL,
        target_entity TEXT NOT NULL,
        relationship_type TEXT NOT NULL,
        confidence REAL DEFAULT 1.0,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(source_entity, target_entity, relationship_type)
    );

    CREATE TABLE IF NOT EXISTS api_keys (
        api_key_hash TEXT PRIMARY KEY,
        tenant_id TEXT NOT NULL,
        plan TEXT DEFAULT 'free',
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        expires_at TEXT
    );

    CREATE VIRTUAL TABLE IF NOT EXISTS wiki_pages_fts USING fts5(
        id,
        title,
        body,
        content='wiki_pages',
        content_rowid='rowid'
    );
    """)
    conn.commit()


class SeekDBClient:
    """SeekDB connection client with lazy initialization and auto-reconnect.

    In compatibility mode, this wraps SQLite. When SeekDB is available,
    swap the _connect method to use pylibseekdb.
    """

    def __init__(self, db_path: str | None = None) -> None:
        self.db_path = db_path or _get_db_path()
        self._conn: sqlite3.Connection | None = None

    def _connect(self) -> sqlite3.Connection:
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(self.db_path, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        _ensure_schema(conn)
        return conn

    def get_connection(self) -> sqlite3.Connection:
        if self._conn is None:
            self._conn = self._connect()
        return self._conn

    def health(self) -> dict[str, Any]:
        try:
            conn = self.get_connection()
            cur = conn.execute("SELECT COUNT(*) FROM wiki_pages")
            page_count = cur.fetchone()[0]
            return {
                "status": "ok",
                "backend": "sqlite_compat",
                "pages": page_count,
                "db_path": self.db_path,
            }
        except Exception as exc:
            return {"status": "error", "error": str(exc)}

    def close(self) -> None:
        if self._conn:
            self._conn.close()
            self._conn = None

    def __enter__(self) -> "SeekDBClient":
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()


@contextmanager
def get_connection() -> Generator[sqlite3.Connection, None, None]:
    """Context manager for short-lived connections."""
    client = SeekDBClient()
    try:
        yield client.get_connection()
    finally:
        client.close()


def health_check() -> dict[str, Any]:
    with SeekDBClient() as client:
        return client.health()


__all__ = ["SeekDBClient", "get_connection", "health_check"]
