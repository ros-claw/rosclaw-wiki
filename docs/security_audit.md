# ROSClaw Wiki API Security Audit Report

**Date**: 2026-05-06
**Scope**: commercial_api.py, auth_manager.py, rate_limiter.py, billing_middleware.py

## Checklist

| Check | Method | Result |
|-------|--------|--------|
| SQL/Collection Injection | All DB queries use parameterized placeholders (`?`) | PASS |
| Output Validation | No secrets, paths, or connection strings in JSON responses | PASS |
| Rate Limiting | `enforce_rate_limit()` called on every protected endpoint | PASS |
| API Key Validation | SHA-256 hash check, `rw_` prefix, expiration enforced | PASS |

## Findings

### PASS — Injection Prevention
- `auth_manager.py`: SQLite queries use `?` parameter binding.
- `seekdb_search_impl.py`: pyseekdb collection API natively parameterizes `where_document` and metadata filters.
- `billing_middleware.py`: Usage logging uses parameterized INSERT.

### PASS — Output Sanitization
- `GET /v1/health` returns only `status`, `backend`, `pages`.
- Search responses include `file_path`, `title`, `snippet`, `score` — no internal system paths or credentials.
- Error responses return generic strings (e.g., "Rate limit exceeded", "Invalid API key").

### PASS — Rate Limiting
- `free`: 100 requests/day
- `pro`: 10,000 requests/month
- `enterprise`: unlimited
- All protected endpoints (`/v1/search`, `/v1/judgments`, `/v1/insights`, `/v1/code/generate`, `/v1/code/impact`, `/v1/usage`) enforce rate limits via `enforce_rate_limit()`.
- Rate limit headers returned: `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset`.

### PASS — API Key Security
- Keys use `secrets.token_urlsafe(32)` for entropy.
- Stored as SHA-256 hashes only; plaintext never persisted after generation.
- Keys expire after 365 days.
- Invalid or expired keys return HTTP 401.

### NOTE — Tier Endpoint Isolation
- Current API has no pro-only or enterprise-only endpoints.
- All authenticated users can access all endpoints; differentiation is purely via rate limits.
- If tier-restricted endpoints are added in the future, endpoint-level permission checks should be added.

## Recommendations

1. Add request body size limits (e.g., `request.body` max 1MB) to prevent DoS via large payloads.
2. Consider adding API key prefix rotation support for compromised keys.
3. Monitor `api_usage` table for anomalous traffic patterns.
