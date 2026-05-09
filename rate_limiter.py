"""Rate Limiter — sliding window rate limiting for commercial API.

Uses SeekDB/SQLite for persistent counters.
"""

from __future__ import annotations

import logging
from typing import Any

from auth_manager import check_rate_limit

logger = logging.getLogger("rosclaw.rate_limiter")


class RateLimitExceeded(Exception):
    """Raised when rate limit is exceeded."""
    pass


def enforce_rate_limit(api_key: str, endpoint: str = "") -> dict[str, Any]:
    """Enforce rate limit for an API key.

    Args:
        api_key: The API key to check.
        endpoint: Optional endpoint name for logging.

    Returns:
        Dict with headers: X-RateLimit-Limit, X-RateLimit-Remaining, X-RateLimit-Reset.

    Raises:
        RateLimitExceeded: If limit exceeded.
    """
    result = check_rate_limit(api_key)
    if not result["allowed"]:
        logger.warning("Rate limit exceeded for key=%s endpoint=%s", api_key[:8], endpoint)
        raise RateLimitExceeded("Rate limit exceeded. Please upgrade your plan.")

    return {
        "X-RateLimit-Limit": str(result["limit"]),
        "X-RateLimit-Remaining": str(result["remaining"]),
        "X-RateLimit-Reset": result["reset_time"],
    }


__all__ = ["enforce_rate_limit", "RateLimitExceeded"]
