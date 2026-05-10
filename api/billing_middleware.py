"""Billing Middleware — async API usage logging for commercial API.

Records every API call to the api_usage table without blocking the request.
"""

from __future__ import annotations

import hashlib
import logging
import time
from typing import Any

from seekdb_client import get_connection

logger = logging.getLogger("rosclaw.billing")


def log_usage(
    api_key: str,
    endpoint: str,
    latency_ms: int,
    status_code: int = 200,
    tokens_used: int = 0,
    search_type: str | None = None,
) -> None:
    """Log an API usage event.

    This is fire-and-forget; errors are logged but not raised.
    """
    try:
        key_hash = hashlib.sha256(api_key.encode()).hexdigest()[:64]
        with get_connection() as conn:
            conn.execute(
                """
                INSERT INTO api_usage (api_key_hash, endpoint, search_type, tokens_used, latency_ms, status_code)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (key_hash, endpoint, search_type, tokens_used, latency_ms, status_code),
            )
            conn.commit()
    except Exception as exc:
        logger.warning("Billing log failed: %s", exc)


def get_usage_summary(api_key: str, days: int = 30) -> dict[str, Any]:
    """Get usage summary for an API key.

    Returns:
        Dict with total_calls, total_tokens, avg_latency, by_endpoint, daily_breakdown.
    """
    import datetime

    key_hash = hashlib.sha256(api_key.encode()).hexdigest()[:64]
    start = (datetime.datetime.now() - datetime.timedelta(days=days)).isoformat()

    with get_connection() as conn:
        # Overall totals
        cur = conn.execute(
            """
            SELECT COUNT(*) as calls, COALESCE(SUM(tokens_used), 0) as tokens, AVG(latency_ms) as avg_latency
            FROM api_usage WHERE api_key_hash = ? AND created_at >= ?
            """,
            (key_hash, start),
        )
        row = cur.fetchone()

        # By endpoint breakdown
        cur = conn.execute(
            """
            SELECT endpoint, COUNT(*) as calls
            FROM api_usage WHERE api_key_hash = ? AND created_at >= ?
            GROUP BY endpoint ORDER BY calls DESC
            """,
            (key_hash, start),
        )
        by_endpoint = {r["endpoint"]: r["calls"] for r in cur.fetchall()}

        # Daily breakdown
        cur = conn.execute(
            """
            SELECT DATE(created_at) as day, COUNT(*) as calls
            FROM api_usage WHERE api_key_hash = ? AND created_at >= ?
            GROUP BY day ORDER BY day DESC
            """,
            (key_hash, start),
        )
        daily_breakdown = [
            {"date": r["day"], "calls": r["calls"]} for r in cur.fetchall()
        ]

        return {
            "api_key_prefix": api_key[:8] + "...",
            "total_calls": row["calls"],
            "total_tokens": row["tokens"],
            "avg_latency_ms": round(row["avg_latency"] or 0, 2),
            "period_days": days,
            "by_endpoint": by_endpoint,
            "daily_breakdown": daily_breakdown,
        }


__all__ = ["log_usage", "get_usage_summary"]
