"""Shared cache client with Redis primary and in-memory fallback.

Supports cross-worker cache consistency for Gunicorn multi-process deployments.
"""

from __future__ import annotations

import json
import logging
import os
from typing import Any

logger = logging.getLogger("rosclaw.cache")

# In-memory fallback (per-process, used when Redis is unavailable)
_MEMORY_CACHE: dict[str, tuple[float, float, Any]] = {}
_DEFAULT_TTL_SEC = 300


class CacheClient:
    """Unified cache interface: Redis primary, memory fallback."""

    def __init__(self) -> None:
        self._redis = None
        self._available = False
        self._connect()

    def _connect(self) -> None:
        try:
            import redis as redis_lib

            host = os.environ.get("REDIS_HOST", "redis")
            port = int(os.environ.get("REDIS_PORT", "6379"))
            db = int(os.environ.get("REDIS_DB", "0"))
            password = os.environ.get("REDIS_PASSWORD") or None

            self._redis = redis_lib.Redis(
                host=host,
                port=port,
                db=db,
                password=password,
                decode_responses=True,
                socket_connect_timeout=2,
                socket_timeout=2,
            )
            self._redis.ping()
            self._available = True
            logger.info("Redis cache connected: %s:%s", host, port)
        except Exception as exc:
            logger.warning("Redis unavailable, using memory fallback: %s", exc)
            self._available = False

    def get(self, key: str) -> Any | None:
        """Get cached value. Returns None if miss or expired."""
        if self._available and self._redis:
            try:
                raw = self._redis.get(key)
                if raw is not None:
                    return json.loads(raw)
            except Exception:
                pass
        # Memory fallback
        if key in _MEMORY_CACHE:
            cached_at, ttl, value = _MEMORY_CACHE[key]
            if ttl > 0 and (self._now() - cached_at) < ttl:
                return value
            del _MEMORY_CACHE[key]
        return None

    def set(self, key: str, value: Any, ttl: int = _DEFAULT_TTL_SEC) -> bool:
        """Set cached value with TTL. Returns True if stored."""
        if self._available and self._redis:
            try:
                self._redis.setex(key, ttl, json.dumps(value, default=str))
                return True
            except Exception:
                pass
        # Memory fallback
        _MEMORY_CACHE[key] = (self._now(), float(ttl), value)
        return True

    def delete(self, key: str) -> bool:
        """Delete cached value."""
        if self._available and self._redis:
            try:
                self._redis.delete(key)
            except Exception:
                pass
        _MEMORY_CACHE.pop(key, None)
        return True

    def _now(self) -> float:
        import time

        return time.time()


# Singleton instance
_client: CacheClient | None = None


def get_cache() -> CacheClient:
    """Get the shared cache client singleton."""
    global _client
    if _client is None:
        _client = CacheClient()
    return _client


def cache_get(key: str) -> Any | None:
    """Convenience: get from shared cache."""
    return get_cache().get(key)


def cache_set(key: str, value: Any, ttl: int = _DEFAULT_TTL_SEC) -> bool:
    """Convenience: set in shared cache."""
    return get_cache().set(key, value, ttl)


def cache_delete(key: str) -> bool:
    """Convenience: delete from shared cache."""
    return get_cache().delete(key)
