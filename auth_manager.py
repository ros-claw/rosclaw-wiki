"""Auth Manager — API Key generation and validation for commercial API.

Supports three plans: free (100/day), pro (10k/month), enterprise (unlimited).
"""

from __future__ import annotations

import hashlib
import logging
import secrets
from datetime import datetime, timedelta
from typing import Any

from seekdb_client import get_connection

logger = logging.getLogger("rosclaw.auth")

_PLAN_LIMITS: dict[str, int | None] = {
    "free": 100,        # per day
    "pro": 10000,       # per month
    "enterprise": None, # unlimited
}


def _hash_key(api_key: str) -> str:
    return hashlib.sha256(api_key.encode()).hexdigest()[:64]


def generate_api_key(tenant_id: str, plan: str = "free") -> dict[str, Any]:
    """Generate a new API key.

    Returns:
        Dict with api_key (plaintext, shown once), tenant_id, plan.
    """
    if plan not in _PLAN_LIMITS:
        raise ValueError(f"Unknown plan: {plan}. Choose from: {list(_PLAN_LIMITS.keys())}")

    raw_key = "rw_" + secrets.token_urlsafe(32)
    key_hash = _hash_key(raw_key)

    with get_connection() as conn:
        conn.execute(
            "INSERT INTO api_keys (api_key_hash, tenant_id, plan, created_at, expires_at) VALUES (?, ?, ?, ?, ?)",
            (key_hash, tenant_id, plan, datetime.now().isoformat(), (datetime.now() + timedelta(days=365)).isoformat()),
        )
        conn.commit()

    logger.info("Generated API key for tenant=%s plan=%s", tenant_id, plan)
    return {"api_key": raw_key, "tenant_id": tenant_id, "plan": plan}


def validate_api_key(api_key: str) -> dict[str, Any] | None:
    """Validate an API key and return tenant info.

    Returns:
        Dict with tenant_id, plan, or None if invalid.
    """
    if not api_key or not api_key.startswith("rw_"):
        return None

    key_hash = _hash_key(api_key)
    with get_connection() as conn:
        cur = conn.execute(
            "SELECT tenant_id, plan, expires_at FROM api_keys WHERE api_key_hash = ?",
            (key_hash,),
        )
        row = cur.fetchone()
        if row is None:
            return None

        expires = row["expires_at"]
        if expires and datetime.fromisoformat(expires) < datetime.now():
            return None

        return {"tenant_id": row["tenant_id"], "plan": row["plan"]}


def check_rate_limit(api_key: str, window: str = "day") -> dict[str, Any]:
    """Check current usage against plan limit.

    Returns:
        Dict with allowed (bool), remaining (int), limit (int), reset_time (str).
    """
    info = validate_api_key(api_key)
    if info is None:
        return {"allowed": False, "remaining": 0, "limit": 0, "reset_time": ""}

    plan = info["plan"]
    limit = _PLAN_LIMITS.get(plan)
    if limit is None:
        return {"allowed": True, "remaining": -1, "limit": -1, "reset_time": ""}

    key_hash = _hash_key(api_key)
    tenant_id = info["tenant_id"]

    with get_connection() as conn:
        if window == "day":
            start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0).isoformat()
            cur = conn.execute(
                "SELECT COUNT(*) FROM api_usage WHERE api_key_hash = ? AND created_at >= ?",
                (key_hash, start),
            )
        else:
            start = (datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)).isoformat()
            cur = conn.execute(
                "SELECT COUNT(*) FROM api_usage WHERE api_key_hash = ? AND created_at >= ?",
                (key_hash, start),
            )
        used = cur.fetchone()[0]

    remaining = max(0, limit - used)
    reset = (datetime.now() + timedelta(days=1)).replace(hour=0, minute=0, second=0).isoformat()
    return {"allowed": used < limit, "remaining": remaining, "limit": limit, "reset_time": reset}


__all__ = ["generate_api_key", "validate_api_key", "check_rate_limit", "_PLAN_LIMITS"]
