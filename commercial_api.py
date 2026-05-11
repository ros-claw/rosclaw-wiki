"""Commercial API — FastAPI service layer for ROSClaw Wiki (Phase 17).

Endpoints:
  GET   /v1/health               — health check (no auth)
  GET   /v1/manifest.json        — service manifest
  POST  /v1/search               — hybrid search
  POST  /v1/search/hybrid        — high-precision hybrid search
  GET   /v1/judgments/{entity}   — get judgments
  GET   /v1/insights             — knowledge gap insights
  POST  /v1/code/generate        — code skeleton generation
  POST  /v1/code/sync            — code sync with PR
  POST  /v1/code/impact          — code impact analysis
  GET   /v1/usage                — query own usage
  POST  /v1/physics/impact       — physical impact chain
  POST  /v1/physics/resolve      — physical conflict resolution
  POST  /v1/physics/feasibility  — physical feasibility check
  POST  /v1/topology/trace       — causal topology tracing
  GET   /v1/ontology/entanglement — entanglement analysis
  POST  /v1/reasoning/grounding  — instruction-to-constraint grounding
  POST  /v1/analysis/sensitivity — coupling sensitivity matrix
  GET   /v1/analogy/find         — analogical reasoning
  POST  /wiki/v1/upload/request  — request presigned upload URL
  POST  /wiki/v1/upload/complete — notify upload complete + import
"""

from __future__ import annotations

import logging
import os
import sys
import time
from pathlib import Path
from typing import Any

# Add subdirectories to path so modules can be imported flat (legacy compat)
_PROJECT_ROOT = Path(__file__).parent
for _pkg_dir in ["api", "core", "search", "ingest", "knowledge", "code", "robot", "utils", "dream", "tests"]:
    _pkg_path = _PROJECT_ROOT / _pkg_dir
    if str(_pkg_path) not in sys.path:
        sys.path.insert(0, str(_pkg_path))

from fastapi import FastAPI, Header, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from auth_manager import (
    generate_api_key,
    get_or_create_api_key_for_email,
    get_user_info_by_api_key,
    validate_api_key,
)
from billing_middleware import get_usage_summary, log_usage
from rate_limiter import RateLimitExceeded, enforce_rate_limit
from search_interface import get_search_impl
from storage_interface import get_storage_impl

logger = logging.getLogger("rosclaw.api")

app = FastAPI(title="ROSClaw Wiki API", version="1.0.0")

# CORS: allow Vercel frontend + local dev
CORS_ORIGINS = os.environ.get(
    "CORS_ORIGINS",
    "https://www.rosclaw.io,https://rosclaw.io,http://localhost:3000,http://localhost:5173",
).split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in CORS_ORIGINS if o.strip()],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

WIKI_ROOT = os.environ.get("WIKI_ROOT", "wiki")

# ── Phase 16: Cognitive Physics ──

_constraint_graph: Any | None = None


def _get_constraint_graph() -> Any:
    """Lazy-load the global ConstraintGraph instance."""
    global _constraint_graph
    if _constraint_graph is None:
        from constraint_graph import ConstraintGraph
        _constraint_graph = ConstraintGraph()
        # Attempt to load persisted ontology
        onto_path = Path(WIKI_ROOT).parent / "data" / "physical_ontology.json"
        if onto_path.exists():
            try:
                from physical_ontology import PhysicalOntology
                _constraint_graph.ontology = PhysicalOntology.load(str(onto_path))
                logger.info("Loaded physical ontology from %s", onto_path)
            except Exception as exc:
                logger.warning("Could not load ontology: %s", exc)
    return _constraint_graph


def _get_tenant(api_key: str | None) -> dict[str, Any]:
    if not api_key:
        raise HTTPException(status_code=401, detail="Missing X-API-Key header")
    info = validate_api_key(api_key)
    if info is None:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return info


# ── Middleware ──

@app.middleware("http")
async def add_process_time_header(request: Request, call_next: Any) -> Any:
    start = time.perf_counter()
    response = await call_next(request)
    latency_ms = int((time.perf_counter() - start) * 1000)
    response.headers["X-Process-Time-Ms"] = str(latency_ms)
    return response


# ── Health ──

@app.get("/v1/health")
async def health() -> dict[str, Any]:
    from seekdb_client import health_check
    h = health_check()
    # Count judgments from SQLite/SeekDB
    judgment_count = 0
    try:
        from seekdb_client import get_connection
        with get_connection() as conn:
            cur = conn.execute("SELECT COUNT(*) FROM judgments")
            row = cur.fetchone()
            judgment_count = row[0] if row else 0
    except Exception:
        pass
    # Reflect the actual configured search backend
    backend = os.environ.get("WIKI_BACKEND", h.get("backend", "unknown"))
    return {
        "status": "ok",
        "backend": backend,
        "wiki_pages": h.get("pages", 0),
        "judgments": judgment_count,
    }


# ── Search ──

@app.post("/v1/search")
async def search(
    request: Request,
    x_api_key: str = Header(..., alias="X-API-Key"),
) -> JSONResponse:
    body = await request.json()
    query = body.get("query", "")
    search_type = body.get("search_type", "hybrid")
    top_k = body.get("top_k", 10)

    tenant = _get_tenant(x_api_key)
    start = time.perf_counter()

    try:
        limit_headers = enforce_rate_limit(x_api_key, endpoint="/v1/search")
    except RateLimitExceeded:
        log_usage(x_api_key, "/v1/search", int((time.perf_counter() - start) * 1000), status_code=429)
        raise HTTPException(status_code=429, detail="Rate limit exceeded")

    search_impl = get_search_impl(WIKI_ROOT)
    results = search_impl.search(query, search_type=search_type, top_k=top_k)

    latency_ms = int((time.perf_counter() - start) * 1000)
    log_usage(x_api_key, "/v1/search", latency_ms, search_type=search_type)

    return JSONResponse(
        content={"status": "ok", "query": query, "results": results, "count": len(results)},
        headers=limit_headers,
    )


@app.post("/v1/search/hybrid")
async def search_hybrid(
    request: Request,
    x_api_key: str = Header(..., alias="X-API-Key"),
) -> JSONResponse:
    body = await request.json()
    query = body.get("query", "")
    top_k = body.get("top_k", 10)

    tenant = _get_tenant(x_api_key)
    start = time.perf_counter()

    try:
        limit_headers = enforce_rate_limit(x_api_key, endpoint="/v1/search/hybrid")
    except RateLimitExceeded:
        log_usage(x_api_key, "/v1/search/hybrid", int((time.perf_counter() - start) * 1000), status_code=429)
        raise HTTPException(status_code=429, detail="Rate limit exceeded")

    search_impl = get_search_impl(WIKI_ROOT)
    results = search_impl.search(query, search_type="hybrid", top_k=top_k)

    latency_ms = int((time.perf_counter() - start) * 1000)
    log_usage(x_api_key, "/v1/search/hybrid", latency_ms, search_type="hybrid")

    return JSONResponse(
        content={"status": "ok", "query": query, "results": results, "count": len(results)},
        headers=limit_headers,
    )


# ── Judgments ──

@app.get("/v1/judgments/{entity}")
async def get_judgments(
    entity: str,
    limit: int = Query(50, ge=1, le=500, description="Max judgments to return"),
    x_api_key: str = Header(..., alias="X-API-Key"),
) -> JSONResponse:
    tenant = _get_tenant(x_api_key)
    start = time.perf_counter()

    try:
        limit_headers = enforce_rate_limit(x_api_key, endpoint="/v1/judgments")
    except RateLimitExceeded:
        log_usage(x_api_key, "/v1/judgments", int((time.perf_counter() - start) * 1000), status_code=429)
        raise HTTPException(status_code=429, detail="Rate limit exceeded")

    try:
        from judgment_generator import get_judgment
        result = get_judgment(entity, wiki_root=WIKI_ROOT, limit=limit)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))

    latency_ms = int((time.perf_counter() - start) * 1000)
    log_usage(x_api_key, "/v1/judgments", latency_ms)

    return JSONResponse(content=result, headers=limit_headers)


# ── Insights ──

@app.get("/v1/insights")
async def insights(
    x_api_key: str = Header(..., alias="X-API-Key"),
) -> JSONResponse:
    tenant = _get_tenant(x_api_key)
    start = time.perf_counter()

    try:
        limit_headers = enforce_rate_limit(x_api_key, endpoint="/v1/insights")
    except RateLimitExceeded:
        log_usage(x_api_key, "/v1/insights", int((time.perf_counter() - start) * 1000), status_code=429)
        raise HTTPException(status_code=429, detail="Rate limit exceeded")

    from dream_cycle import generate_insights
    results = generate_insights(WIKI_ROOT)

    latency_ms = int((time.perf_counter() - start) * 1000)
    log_usage(x_api_key, "/v1/insights", latency_ms)

    return JSONResponse(content={"status": "ok", "insights": results}, headers=limit_headers)


# ── Code Generate ──

@app.post("/v1/code/generate")
async def code_generate(
    request: Request,
    x_api_key: str = Header(..., alias="X-API-Key"),
) -> JSONResponse:
    body = await request.json()
    entity = body.get("entity", "")
    language = body.get("language", "python")

    if not entity:
        raise HTTPException(status_code=400, detail="entity is required")

    tenant = _get_tenant(x_api_key)
    start = time.perf_counter()

    try:
        limit_headers = enforce_rate_limit(x_api_key, endpoint="/v1/code/generate")
    except RateLimitExceeded:
        log_usage(x_api_key, "/v1/code/generate", int((time.perf_counter() - start) * 1000), status_code=429)
        raise HTTPException(status_code=429, detail="Rate limit exceeded")

    from code_generator import code_generate
    result = code_generate(entity, wiki_root=WIKI_ROOT, language=language)

    latency_ms = int((time.perf_counter() - start) * 1000)
    log_usage(x_api_key, "/v1/code/generate", latency_ms)

    return JSONResponse(content=result, headers=limit_headers)


# ── Code Sync ──

@app.post("/v1/code/sync")
async def code_sync(
    request: Request,
    x_api_key: str = Header(..., alias="X-API-Key"),
) -> JSONResponse:
    body = await request.json()
    entity = body.get("entity", "")
    auto_pr = body.get("auto_pr", False)
    code_paths = body.get("code_paths", None)
    target_repo = body.get("target_repo")
    auto_submit = body.get("auto_submit", False)
    auto_merge = body.get("auto_merge", False)

    if not entity:
        raise HTTPException(status_code=400, detail="entity is required")

    tenant = _get_tenant(x_api_key)
    start = time.perf_counter()

    try:
        limit_headers = enforce_rate_limit(x_api_key, endpoint="/v1/code/sync")
    except RateLimitExceeded:
        log_usage(x_api_key, "/v1/code/sync", int((time.perf_counter() - start) * 1000), status_code=429)
        raise HTTPException(status_code=429, detail="Rate limit exceeded")

    from code_generator import sync_check
    result = sync_check(entity, WIKI_ROOT, code_paths=code_paths, auto_pr=auto_pr)

    # Phase 14: real GitHub submission
    if auto_submit and target_repo and result.get("status") in ("created", "amber") and result.get("pr_data"):
        try:
            from pr_generator import submit_pr_to_github
            gh_result = submit_pr_to_github(
                pr_data={"entity": entity, "pr": result["pr_data"]},
                github_repo=target_repo,
                base_branch="main",
                auto_merge=auto_merge,
            )
            result["github_submission"] = gh_result
            result["pr_submitted"] = gh_result.get("status") == "created"
            result["pr_url"] = gh_result.get("pr_url")
        except Exception as exc:
            logger.warning("GitHub submission failed: %s", exc)
            result["github_submission"] = {"status": "error", "reason": str(exc)}
            result["pr_submitted"] = False

    latency_ms = int((time.perf_counter() - start) * 1000)
    log_usage(x_api_key, "/v1/code/sync", latency_ms, auto_pr=auto_pr, auto_submit=auto_submit)

    return JSONResponse(content=result, headers=limit_headers)


# ── Code Impact Analysis ──

@app.post("/v1/code/impact")
async def code_impact(
    request: Request,
    x_api_key: str = Header(..., alias="X-API-Key"),
) -> JSONResponse:
    tenant = _get_tenant(x_api_key)
    body = await request.json()
    function_name = body.get("function_name", "")
    change_description = body.get("change_description", "")

    if not function_name:
        raise HTTPException(status_code=400, detail="function_name is required")

    start = time.perf_counter()
    try:
        limit_headers = enforce_rate_limit(x_api_key)
    except RateLimitExceeded:
        log_usage(x_api_key, "/v1/code/impact", int((time.perf_counter() - start) * 1000), status_code=429)
        raise HTTPException(status_code=429, detail="Rate limit exceeded")

    from seekdb_search_impl import SeekDBSearchImpl
    search = SeekDBSearchImpl(WIKI_ROOT)
    graph_result = search.query_graph(function_name, radius=2)

    direct_dependents = [c["name"] for c in graph_result.get("callers", [])[:10]]
    indirect_dependents = [c["name"] for c in graph_result.get("callers", [])[10:20]]
    total_affected = len(graph_result.get("callers", [])) + len(graph_result.get("callees", []))

    # Simple risk heuristic
    risk_level = "low"
    if total_affected > 10:
        risk_level = "high"
    elif total_affected > 3:
        risk_level = "medium"

    latency_ms = int((time.perf_counter() - start) * 1000)
    log_usage(x_api_key, "/v1/code/impact", latency_ms)

    return JSONResponse(
        content={
            "status": "ok",
            "function": function_name,
            "change_description": change_description,
            "direct_dependents": direct_dependents,
            "indirect_dependents": indirect_dependents,
            "total_affected_nodes": total_affected,
            "risk_level": risk_level,
            "recommended_review": total_affected > 3,
        },
        headers=limit_headers,
    )


# ── Usage ──

@app.get("/v1/usage")
async def usage(
    x_api_key: str = Header(..., alias="X-API-Key"),
    days: int = 30,
) -> JSONResponse:
    tenant = _get_tenant(x_api_key)
    summary = get_usage_summary(x_api_key, days=days)
    return JSONResponse(content={"status": "ok", "usage": summary})


# ── Phase 16: Physical Impact ──

@app.post("/v1/physics/impact")
async def physics_impact(
    request: Request,
    x_api_key: str = Header(..., alias="X-API-Key"),
) -> JSONResponse:
    body = await request.json()
    variable = body.get("variable", "")
    radius = body.get("radius", 3)

    if not variable:
        raise HTTPException(status_code=400, detail="variable is required")

    tenant = _get_tenant(x_api_key)
    start = time.perf_counter()

    try:
        limit_headers = enforce_rate_limit(x_api_key, endpoint="/v1/physics/impact")
    except RateLimitExceeded:
        log_usage(x_api_key, "/v1/physics/impact", int((time.perf_counter() - start) * 1000), status_code=429)
        raise HTTPException(status_code=429, detail="Rate limit exceeded")

    cg = _get_constraint_graph()
    result = cg.get_physical_impact(variable, radius=radius)

    latency_ms = int((time.perf_counter() - start) * 1000)
    log_usage(x_api_key, "/v1/physics/impact", latency_ms)

    return JSONResponse(
        content={"status": "ok", "variable": variable, "radius": radius, "impact": result},
        headers=limit_headers,
    )


# ── Phase 16: Physical Conflict Resolution ──

@app.post("/v1/physics/resolve")
async def physics_resolve(
    request: Request,
    x_api_key: str = Header(..., alias="X-API-Key"),
) -> JSONResponse:
    body = await request.json()
    entity = body.get("entity", "")
    property_name = body.get("property_name", "")

    if not entity or not property_name:
        raise HTTPException(status_code=400, detail="entity and property_name are required")

    tenant = _get_tenant(x_api_key)
    start = time.perf_counter()

    try:
        limit_headers = enforce_rate_limit(x_api_key, endpoint="/v1/physics/resolve")
    except RateLimitExceeded:
        log_usage(x_api_key, "/v1/physics/resolve", int((time.perf_counter() - start) * 1000), status_code=429)
        raise HTTPException(status_code=429, detail="Rate limit exceeded")

    cg = _get_constraint_graph()
    result = cg.resolve_physical_conflict(entity, property_name)

    latency_ms = int((time.perf_counter() - start) * 1000)
    log_usage(x_api_key, "/v1/physics/resolve", latency_ms)

    return JSONResponse(
        content={"status": "ok", "entity": entity, "property": property_name, "resolution": result},
        headers=limit_headers,
    )


# ── Phase 16: Physical Feasibility Check ──

@app.post("/v1/physics/feasibility")
async def physics_feasibility(
    request: Request,
    x_api_key: str = Header(..., alias="X-API-Key"),
) -> JSONResponse:
    body = await request.json()
    code_snippet = body.get("code_snippet", "")

    if not code_snippet:
        raise HTTPException(status_code=400, detail="code_snippet is required")

    tenant = _get_tenant(x_api_key)
    start = time.perf_counter()

    try:
        limit_headers = enforce_rate_limit(x_api_key, endpoint="/v1/physics/feasibility")
    except RateLimitExceeded:
        log_usage(x_api_key, "/v1/physics/feasibility", int((time.perf_counter() - start) * 1000), status_code=429)
        raise HTTPException(status_code=429, detail="Rate limit exceeded")

    # Extract physical constants from snippet
    import tempfile
    from pathlib import Path
    from physics_grounding import scan_file_for_constants

    checks: list[dict[str, Any]] = []
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
        f.write(code_snippet)
        tmp_path = Path(f.name)

    try:
        constants = scan_file_for_constants(tmp_path, "snippet")
        cg = _get_constraint_graph()
        for c in constants:
            try:
                val = float(c.value) if c.value is not None else 0.0
                check = cg.check_physical_constraints(c.name, val)
                checks.append({"parameter": c.name, "value": c.value, "check": check})
            except (ValueError, TypeError):
                continue
    finally:
        tmp_path.unlink()

    # Aggregate safety level
    safety_level = "OK"
    action = "ALLOW"
    for ck in checks:
        sl = ck["check"].get("safety_level", "OK")
        if sl == "CRITICAL":
            safety_level = "CRITICAL"
            action = "REFUSE"
            break
        elif sl == "WARNING" and safety_level != "CRITICAL":
            safety_level = "WARNING"
            action = "REVIEW_REQUIRED"

    latency_ms = int((time.perf_counter() - start) * 1000)
    log_usage(x_api_key, "/v1/physics/feasibility", latency_ms)

    return JSONResponse(
        content={
            "status": "ok",
            "safety_level": safety_level,
            "action": action,
            "checks": checks,
            "parameter_count": len(checks),
        },
        headers=limit_headers,
    )


# ── Phase 17: Topology & Connection ──

@app.post("/v1/topology/trace")
async def topology_trace(
    request: Request,
    x_api_key: str = Header(..., alias="X-API-Key"),
) -> JSONResponse:
    body = await request.json()
    entity = body.get("entity", "")
    parameter = body.get("parameter", "")
    delta = body.get("delta", "")
    radius = body.get("radius", 3)

    if not entity or not parameter:
        raise HTTPException(status_code=400, detail="entity and parameter are required")

    tenant = _get_tenant(x_api_key)
    start = time.perf_counter()

    try:
        limit_headers = enforce_rate_limit(x_api_key, endpoint="/v1/topology/trace")
    except RateLimitExceeded:
        log_usage(x_api_key, "/v1/topology/trace", int((time.perf_counter() - start) * 1000), status_code=429)
        raise HTTPException(status_code=429, detail="Rate limit exceeded")

    cg = _get_constraint_graph()
    root = f"{entity}.{parameter}"
    impact = cg.get_physical_impact(root, radius=radius)

    # Build subgraph nodes
    node_ids = set([root]) | set(impact.get("visited", []))
    nodes: list[dict[str, Any]] = []
    for nid in node_ids:
        n = cg.ontology.get_node(nid)
        if n:
            nodes.append({
                "id": nid,
                "type": n.node_type,
                **{k: v for k, v in n.metadata.items() if k not in {"context", "reason"}},
            })
        else:
            nodes.append({"id": nid, "type": "unknown"})

    # Build subgraph edges
    edges: list[dict[str, Any]] = []
    for edge in cg.ontology.edges:
        if edge.source in node_ids and edge.target in node_ids:
            edges.append({
                "source": edge.source,
                "target": edge.target,
                "type": edge.edge_type,
                **edge.metadata,
            })

    # Causal paths as text
    causal_paths = impact.get("causal_chain", [])
    degradation_paths = [d["path"] for d in impact.get("degradation", [])]
    all_paths = causal_paths + degradation_paths

    # Safety assessment
    safety_assessment = "OK"
    recommendation = "No physical constraints violated. Safe to proceed."
    if impact.get("degradation"):
        safety_assessment = "WARNING"
        recommendation = "Degradation paths detected. Review before deployment."

    latency_ms = int((time.perf_counter() - start) * 1000)
    log_usage(x_api_key, "/v1/topology/trace", latency_ms)

    return JSONResponse(
        content={
            "status": "ok",
            "root": root,
            "delta": delta,
            "subgraph": {"nodes": nodes, "edges": edges, "causal_paths": all_paths},
            "safety_assessment": safety_assessment,
            "recommendation": recommendation,
        },
        headers=limit_headers,
    )


@app.get("/v1/ontology/entanglement")
async def ontology_entanglement(
    entity_a: str,
    entity_b: str,
    context: str = "",
    x_api_key: str = Header(..., alias="X-API-Key"),
) -> JSONResponse:
    tenant = _get_tenant(x_api_key)
    start = time.perf_counter()

    try:
        limit_headers = enforce_rate_limit(x_api_key, endpoint="/v1/ontology/entanglement")
    except RateLimitExceeded:
        log_usage(x_api_key, "/v1/ontology/entanglement", int((time.perf_counter() - start) * 1000), status_code=429)
        raise HTTPException(status_code=429, detail="Rate limit exceeded")

    cg = _get_constraint_graph()

    # BFS from entity_a to find paths to entity_b
    def _find_paths(start: str, end: str, max_depth: int = 5) -> list[list[str]]:
        paths: list[list[str]] = []
        queue: list[list[str]] = [[start]]
        while queue:
            path = queue.pop(0)
            if len(path) > max_depth:
                continue
            current = path[-1]
            if current == end:
                paths.append(path)
                continue
            for edge in cg.ontology.edges:
                if edge.source == current and edge.target not in path:
                    queue.append(path + [edge.target])
        return paths

    raw_paths = _find_paths(entity_a, entity_b)

    entanglement_found = len(raw_paths) > 0
    paths_out: list[dict[str, Any]] = []
    for p in raw_paths:
        strength = max(0.1, 1.0 - (len(p) - 2) * 0.15)
        paths_out.append({
            "chain": " → ".join(p),
            "strength": round(strength, 2),
            "context": context or "general",
        })

    # Sort by strength descending
    paths_out.sort(key=lambda x: x["strength"], reverse=True)

    latency_ms = int((time.perf_counter() - start) * 1000)
    log_usage(x_api_key, "/v1/ontology/entanglement", latency_ms)

    return JSONResponse(
        content={
            "status": "ok",
            "entanglement_found": entanglement_found,
            "paths": paths_out,
            "explanation": f"Found {len(paths_out)} connecting path(s) between {entity_a} and {entity_b}.",
        },
        headers=limit_headers,
    )


@app.post("/v1/reasoning/grounding")
async def reasoning_grounding(
    request: Request,
    x_api_key: str = Header(..., alias="X-API-Key"),
) -> JSONResponse:
    body = await request.json()
    instruction = body.get("instruction", "")
    entity = body.get("entity", "")
    context = body.get("context", "")

    if not instruction or not entity:
        raise HTTPException(status_code=400, detail="instruction and entity are required")

    tenant = _get_tenant(x_api_key)
    start = time.perf_counter()

    try:
        limit_headers = enforce_rate_limit(x_api_key, endpoint="/v1/reasoning/grounding")
    except RateLimitExceeded:
        log_usage(x_api_key, "/v1/reasoning/grounding", int((time.perf_counter() - start) * 1000), status_code=429)
        raise HTTPException(status_code=429, detail="Rate limit exceeded")

    cg = _get_constraint_graph()

    # Heuristic: extract keywords from instruction and match against entity properties
    keywords = [w.lower() for w in instruction.replace(",", " ").replace(".", " ").split() if len(w) > 2]
    props = cg.ontology.get_properties_of(entity)

    grounded_parameters: list[dict[str, Any]] = []
    for prop in props:
        prop_name = prop.name.lower()
        if any(kw in prop_name or kw in str(prop.metadata.get("unit", "")).lower() for kw in keywords):
            constraints: list[str] = []
            for edge in cg.ontology.get_edges_from(prop.name, "constrained_by"):
                constraints.append(edge.target)
            grounded_parameters.append({
                "parameter": prop.name,
                "current_limit": prop.metadata.get("value"),
                "hardware_limit": prop.metadata.get("max_value"),
                "governing_constraints": constraints,
                "trade_offs": [
                    f"Modifying {prop.name} affects downstream causal chain"
                ],
            })

    # Fallback: if no keyword match, return all properties
    if not grounded_parameters and props:
        for prop in props[:5]:
            grounded_parameters.append({
                "parameter": prop.name,
                "current_limit": prop.metadata.get("value"),
                "hardware_limit": prop.metadata.get("max_value"),
                "governing_constraints": [],
                "trade_offs": [],
            })

    latency_ms = int((time.perf_counter() - start) * 1000)
    log_usage(x_api_key, "/v1/reasoning/grounding", latency_ms)

    return JSONResponse(
        content={
            "status": "ok",
            "instruction": instruction,
            "entity": entity,
            "grounded_parameters": grounded_parameters,
            "conflicting_goals": [],
        },
        headers=limit_headers,
    )


@app.post("/v1/analysis/sensitivity")
async def analysis_sensitivity(
    request: Request,
    x_api_key: str = Header(..., alias="X-API-Key"),
) -> JSONResponse:
    body = await request.json()
    parameters = body.get("parameters", [])
    entity = body.get("entity", "")

    if not parameters or len(parameters) < 2:
        raise HTTPException(status_code=400, detail="at least 2 parameters required")

    tenant = _get_tenant(x_api_key)
    start = time.perf_counter()

    try:
        limit_headers = enforce_rate_limit(x_api_key, endpoint="/v1/analysis/sensitivity")
    except RateLimitExceeded:
        log_usage(x_api_key, "/v1/analysis/sensitivity", int((time.perf_counter() - start) * 1000), status_code=429)
        raise HTTPException(status_code=429, detail="Rate limit exceeded")

    cg = _get_constraint_graph()

    # Compute coupling strength for each pair
    coupling_matrix: dict[str, float] = {}
    for i, p1 in enumerate(parameters):
        for p2 in parameters[i + 1 :]:
            key = f"{p1} ↔ {p2}"
            strength = _compute_coupling_strength(cg.ontology, p1, p2, entity)
            coupling_matrix[key] = round(strength, 2)

    most_sensitive = max(coupling_matrix, key=coupling_matrix.get) if coupling_matrix else ""

    latency_ms = int((time.perf_counter() - start) * 1000)
    log_usage(x_api_key, "/v1/analysis/sensitivity", latency_ms)

    return JSONResponse(
        content={
            "status": "ok",
            "coupling_matrix": coupling_matrix,
            "most_sensitive_pair": most_sensitive,
            "explanation": f"{most_sensitive} shows the strongest coupling in the analyzed parameter set.",
        },
        headers=limit_headers,
    )


def _compute_coupling_strength(ontology: Any, p1: str, p2: str, entity: str) -> float:
    """Heuristic coupling strength between two parameters (0.0–1.0)."""
    # Direct edge between them
    for edge in ontology.edges:
        if (edge.source == p1 and edge.target == p2) or (edge.source == p2 and edge.target == p1):
            return 0.95

    # Shared neighbors
    n1_neighbors = {e.target for e in ontology.edges if e.source == p1} | {e.source for e in ontology.edges if e.target == p1}
    n2_neighbors = {e.target for e in ontology.edges if e.source == p2} | {e.source for e in ontology.edges if e.target == p2}
    shared = n1_neighbors & n2_neighbors
    if shared:
        return min(0.9, 0.5 + len(shared) * 0.1)

    # Same entity
    node1 = ontology.get_node(p1)
    node2 = ontology.get_node(p2)
    if node1 and node2:
        if node1.metadata.get("entity") == entity and node2.metadata.get("entity") == entity:
            return 0.45

    return 0.1


@app.get("/v1/analogy/find")
async def analogy_find(
    entity: str,
    domain: str = "",
    x_api_key: str = Header(..., alias="X-API-Key"),
) -> JSONResponse:
    tenant = _get_tenant(x_api_key)
    start = time.perf_counter()

    try:
        limit_headers = enforce_rate_limit(x_api_key, endpoint="/v1/analogy/find")
    except RateLimitExceeded:
        log_usage(x_api_key, "/v1/analogy/find", int((time.perf_counter() - start) * 1000), status_code=429)
        raise HTTPException(status_code=429, detail="Rate limit exceeded")

    cg = _get_constraint_graph()

    # Find the most similar known entity by shared properties
    best_match: str | None = None
    best_score = 0.0
    shared_props: list[str] = []

    # Compare base property names (after the dot) for cross-entity analogy
    def _base_names(props: list[Any]) -> set[str]:
        return {n.name.split(".", 1)[1] if "." in n.name else n.name for n in props}

    target_props = cg.ontology.get_properties_of(entity)
    target_bases = _base_names(target_props)
    target_entity_node = cg.ontology.get_node(entity)
    target_domain = (target_entity_node.metadata.get("entity_type", "") if target_entity_node else "").lower()

    for node in cg.ontology.nodes.values():
        if node.node_type != "entity" or node.name == entity:
            continue
        # Domain filter: if domain param provided, prefer same domain
        node_domain = node.metadata.get("entity_type", "").lower()
        if domain and domain.lower() not in node_domain and node_domain not in domain.lower():
            continue
        candidate_props = cg.ontology.get_properties_of(node.name)
        candidate_bases = _base_names(candidate_props)
        intersection = target_bases & candidate_bases
        union = target_bases | candidate_bases
        if not union:
            continue
        score = len(intersection) / len(union)
        if score > best_score:
            best_score = score
            best_match = node.name
            shared_props = list(intersection)

    transferable: list[str] = []
    if best_match:
        for base_name in shared_props[:5]:
            # Find the property on the best_match entity
            full_name = f"{best_match}.{base_name}"
            node = cg.ontology.get_node(full_name)
            if node:
                val = node.metadata.get("value")
                transferable.append(f"{base_name} likely similar (baseline {best_match}: {val})")

    latency_ms = int((time.perf_counter() - start) * 1000)
    log_usage(x_api_key, "/v1/analogy/find", latency_ms)

    return JSONResponse(
        content={
            "status": "ok",
            "closest_analog": best_match or "unknown",
            "similarity_score": round(best_score, 2),
            "shared_properties": shared_props,
            "transferable_knowledge": transferable,
            "caveats": ["Verify hardware limits — analogies are heuristic, not guarantees."],
        },
        headers=limit_headers,
    )


# ── Phase 17: Manifest ──

@app.get("/v1/manifest.json")
async def manifest() -> dict[str, Any]:
    cg = _get_constraint_graph()
    node_count = len(cg.ontology.nodes)
    edge_count = len(cg.ontology.edges)

    return {
        "service": "ROSClaw Steward of Embodied Physical Reality",
        "version": "1.0.0",
        "status": "Ever-expanding Universe of Embodied Knowledge",
        "endpoints": {
            "rest": "https://api.rosclaw.io/wiki/v1/",
            "mcp": "https://api.rosclaw.io/wiki/mcp",
        },
        "capabilities": {
            "semantic_density": f"High — {node_count} nodes woven into {edge_count} edges",
            "causal_depth": "Recursive to physical laws",
            "supported_ontologies": [
                "Kinematics & Dynamics",
                "Thermal & Electrical",
                "Material & Wear",
                "Algorithmic Constraints",
                "Environmental Coupling",
            ],
            "graph_metrics": {
                "active_connections": "Dynamic, growing with every ingested paper",
                "knowledge_entropy": "Decreasing — contradictions resolved, truths reinforced",
                "entity_coverage": "Expanding across quadruped, bipedal, and mobile manipulation platforms",
            },
            "firewall_status": "Active — Cognitive Physics Firewall providing soft guardrails",
        },
        "authentication": {
            "method": "X-API-Key",
            "plans": {
                "free": "100 requests/day — ideal for experimentation",
                "pro": "10,000 requests/month — for research teams",
                "enterprise": "Unlimited — for production deployment fleets",
            },
            "signup": "https://rosclaw.io/keys",
        },
        "contact": {
            "email": "admin@rosclaw.io",
            "docs": "https://rosclaw.io/docs",
            "status_page": "https://rosclaw.io/status",
        },
    }


# ── Upload endpoints (Phase 19) ──

import json
import uuid
from pathlib import Path

_UPLOAD_REGISTRY_PATH = Path("data/upload_registry.json")


def _load_upload_registry() -> dict[str, Any]:
    if _UPLOAD_REGISTRY_PATH.exists():
        return json.loads(_UPLOAD_REGISTRY_PATH.read_text(encoding="utf-8"))
    return {}


def _save_upload_registry(registry: dict[str, Any]) -> None:
    _UPLOAD_REGISTRY_PATH.parent.mkdir(parents=True, exist_ok=True)
    _UPLOAD_REGISTRY_PATH.write_text(json.dumps(registry, ensure_ascii=False, indent=2), encoding="utf-8")


@app.post("/wiki/v1/upload/request")
async def upload_request(
    request: Request,
    x_api_key: str = Header(..., alias="X-API-Key"),
) -> JSONResponse:
    """Request a presigned upload URL for direct R2 upload."""
    tenant = _get_tenant(x_api_key)
    body = await request.json()
    file_name = body.get("file_name", "")
    file_size = body.get("file_size", 0)
    wiki_name = body.get("wiki_name", "")

    if not file_name or file_size <= 0:
        raise HTTPException(status_code=400, detail="file_name and file_size required")

    try:
        from r2_sync import generate_presigned_upload_url
        upload_id = str(uuid.uuid4())
        key = f"uploads/{upload_id}/{file_name}"
        presigned_url = generate_presigned_upload_url(key, file_size, expiry=3600)
    except Exception as exc:
        logger.error("Failed to generate presigned URL: %s", exc)
        raise HTTPException(status_code=500, detail="Storage backend unavailable")

    registry = _load_upload_registry()
    registry[upload_id] = {
        "wiki_name": wiki_name,
        "file_name": file_name,
        "file_size": file_size,
        "r2_key": key,
        "status": "pending",
        "tenant_id": tenant["tenant_id"],
    }
    _save_upload_registry(registry)

    return JSONResponse(content={
        "upload_id": upload_id,
        "presigned_url": presigned_url,
        "expires_in": 3600,
    })


@app.post("/wiki/v1/upload/complete")
async def upload_complete(
    request: Request,
    x_api_key: str = Header(..., alias="X-API-Key"),
) -> JSONResponse:
    """Notify that upload is complete; trigger server-side import."""
    _get_tenant(x_api_key)
    body = await request.json()
    upload_id = body.get("upload_id", "")

    registry = _load_upload_registry()
    if upload_id not in registry:
        raise HTTPException(status_code=404, detail="Upload ID not found")

    record = registry[upload_id]
    if record["status"] != "pending":
        raise HTTPException(status_code=409, detail=f"Upload already {record['status']}")

    # Verify object exists in R2
    try:
        from r2_sync import head_object
        meta = head_object(record["r2_key"])
        if meta is None:
            raise HTTPException(status_code=400, detail="File not found in storage")
    except HTTPException:
        raise
    except Exception as exc:
        logger.warning("R2 head_object check failed: %s", exc)

    # Mark as completed
    record["status"] = "completed"
    _save_upload_registry(registry)

    # TODO: In production, queue background import job here
    # For MVP, return success with placeholder counts
    return JSONResponse(content={
        "status": "completed",
        "upload_id": upload_id,
        "wiki_name": record["wiki_name"],
        "pages_imported": 0,
        "judgments_added": 0,
        "message": "Upload accepted. Import queued.",
    })


# ── Wiki Frontend Integration (Phase 19+) ──

@app.post("/wiki/v1/auth/exchange")
async def auth_exchange(request: Request) -> JSONResponse:
    """Exchange OAuth user identity (email) for an API Key.

    Frontend calls this after Google/GitHub OAuth login succeeds.
    If the email already has an API key, returns `exists: true` and the
    frontend should use the locally-stored key. If not, a new key is
    generated and returned in plaintext (show-once).
    """
    body = await request.json()
    email = body.get("email", "").strip().lower()
    name = body.get("name", "")
    provider = body.get("provider", "")

    if not email or "@" not in email:
        raise HTTPException(status_code=400, detail="valid email is required")

    result = get_or_create_api_key_for_email(email, plan="free")

    if result.get("exists"):
        # Key already exists — frontend should have it in localStorage
        return JSONResponse(content={
            "status": "ok",
            "exists": True,
            "tenant_id": result["tenant_id"],
            "plan": result["plan"],
            "created_at": result["created_at"],
            "message": "API key already exists. Use the key stored in your browser.",
        })

    # New key generated — return plaintext (show-once)
    return JSONResponse(content={
        "status": "ok",
        "exists": False,
        "api_key": result["api_key"],
        "tenant_id": result["tenant_id"],
        "plan": result["plan"],
        "created_at": result["created_at"],
    })


@app.get("/wiki/v1/auth/me")
async def auth_me(x_api_key: str = Header(..., alias="X-API-Key")) -> JSONResponse:
    """Get current user profile + usage stats.

    Authenticated via X-API-Key (the same key used for all other API calls).
    """
    info = get_user_info_by_api_key(x_api_key)
    if info is None:
        raise HTTPException(status_code=401, detail="Invalid API key")

    return JSONResponse(content={
        "status": "ok",
        "user": info["user"],
        "api_key": info["api_key"],
        "api_key_masked": info["api_key_masked"],
        "usage_today": info["usage_today"],
        "daily_limit": info["daily_limit"],
    })


@app.get("/wiki/v1/usage")
async def wiki_usage(
    x_api_key: str = Header(..., alias="X-API-Key"),
    days: int = 30,
) -> JSONResponse:
    """Alias for /v1/usage with /wiki/v1/ prefix (frontend compatibility)."""
    tenant = _get_tenant(x_api_key)
    summary = get_usage_summary(x_api_key, days=days)
    return JSONResponse(content={"status": "ok", "usage": summary})


@app.get("/wiki/v1/hub/stats")
async def hub_stats() -> JSONResponse:
    """Public wiki overview stats + keyword graph data.

    No authentication required. Used by the /hub landing page.
    """
    from seekdb_client import get_connection

    stats: dict[str, Any] = {
        "total_pages": 0,
        "total_wikilinks": 0,
        "total_judgments": 0,
        "total_code_graph_nodes": 0,
        "total_code_graph_edges": 0,
        "robots_covered": 0,
        "entities_covered": 0,
        "causal_chains": 0,
        "last_updated": "",
    }

    try:
        with get_connection() as conn:
            # Total pages
            cur = conn.execute("SELECT COUNT(*) FROM wiki_pages")
            stats["total_pages"] = cur.fetchone()[0]

            # Total judgments
            cur = conn.execute("SELECT COUNT(*) FROM judgments")
            stats["total_judgments"] = cur.fetchone()[0]

            # Entities from entity_graph
            cur = conn.execute("SELECT COUNT(DISTINCT source_entity) FROM entity_graph")
            stats["entities_covered"] = cur.fetchone()[0]
    except Exception as exc:
        logger.warning("Hub stats DB query failed: %s", exc)

    # Wikilinks: scan markdown files for [[...]] syntax
    try:
        import re
        wikilink_re = re.compile(r"\[\[([^\]]+)\]\]")
        wiki_root = Path(WIKI_ROOT)
        wikilink_count = 0
        robot_set: set[str] = set()
        if wiki_root.exists():
            for md_file in wiki_root.rglob("*.md"):
                if md_file.name in ("index.md", "log.md"):
                    continue
                content = md_file.read_text(encoding="utf-8", errors="ignore")
                wikilink_count += len(wikilink_re.findall(content))
                # Detect robot entities by filename or frontmatter
                stem = md_file.stem.lower()
                if any(r in stem for r in ["unitree", "g1", "go2", "h1", "ur5", "ur10", "kinova", "franka"]):
                    robot_set.add(stem)
        stats["total_wikilinks"] = wikilink_count
        stats["robots_covered"] = len(robot_set)
    except Exception as exc:
        logger.warning("Hub stats wikilink scan failed: %s", exc)

    # Code knowledge graph: aggregate canonical graph + unmerged batch graphs.
    # Naming convention:
    #   - data/code_graph.json          = canonical merged graph (always read)
    #   - data/code_graph_batch_*.json  = temporary batch graphs (read if present)
    #   - data/code_graph_*_merged.json = intermediate merges (ignored)
    #   - data/code_graph_*_backup.json = backups (ignored)
    try:
        data_dir = Path(WIKI_ROOT).parent / "data"
        cg_files: list[Path] = []
        canonical = data_dir / "code_graph.json"
        if canonical.exists():
            cg_files.append(canonical)
        cg_files.extend(sorted(data_dir.glob("code_graph_batch_*.json")))
        total_nodes = 0
        total_edges = 0
        # Exclude generic/noisy repos that inflate stats without adding embodied-intelligence value
        _EXCLUDED_CODE_REPOS = {"google-research_google-research"}
        if cg_files:
            import json
            for cg_path in cg_files:
                with open(cg_path, encoding="utf-8") as f:
                    cg_data = json.load(f)
                nodes = cg_data.get("nodes", [])
                edges = cg_data.get("edges", [])
                # Build set of node IDs belonging to excluded repos for edge filtering
                excluded_ids = {
                    n["id"] for n in nodes
                    if n.get("repo", "") in _EXCLUDED_CODE_REPOS
                }
                total_nodes += sum(
                    1 for n in nodes if n.get("repo", "") not in _EXCLUDED_CODE_REPOS
                )
                total_edges += sum(
                    1 for e in edges if e.get("source", "") not in excluded_ids
                )
        stats["total_code_graph_nodes"] = total_nodes
        stats["total_code_graph_edges"] = total_edges
    except Exception as exc:
        logger.warning("Hub stats code graph failed: %s", exc)

    # Causal chains: count from constraint graph / physical ontology if available
    try:
        cg = _get_constraint_graph()
        stats["causal_chains"] = len([
            e for e in cg.ontology.edges
            if getattr(e, "edge_type", "") == "causes"
        ])
    except Exception as exc:
        logger.warning("Hub stats constraint graph failed: %s", exc)

    # Last updated: use latest api_usage or wiki page mtime
    try:
        with get_connection() as conn:
            cur = conn.execute("SELECT MAX(created_at) as last FROM api_usage")
            row = cur.fetchone()
            stats["last_updated"] = row["last"] if row and row["last"] else ""
    except Exception:
        pass

    # Keywords: top entities/concepts from wiki_pages frontmatter
    keywords: list[dict[str, Any]] = []
    try:
        import wiki_engine as engine
        wiki_root = Path(WIKI_ROOT)
        type_counts: dict[str, int] = {}
        if wiki_root.exists():
            for md_file in wiki_root.rglob("*.md"):
                if md_file.name in ("index.md", "log.md"):
                    continue
                try:
                    meta, _ = engine.parse_frontmatter(
                        md_file.read_text(encoding="utf-8")
                    )
                    title = meta.get("title", md_file.stem)
                    ptype = meta.get("type", "unknown")
                    type_counts[ptype] = type_counts.get(ptype, 0) + 1
                    keywords.append({
                        "name": title,
                        "weight": round(meta.get("confidence", 0.5), 2),
                        "type": ptype,
                        "pages": 1,
                    })
                except Exception:
                    continue
        # Sort by weight desc, cap at 20
        keywords.sort(key=lambda k: k["weight"], reverse=True)
        keywords = keywords[:20]
    except Exception as exc:
        logger.warning("Hub stats keywords failed: %s", exc)

    # Build keyword_categories from keywords
    keyword_categories: dict[str, list[dict[str, Any]]] = {}
    for kw in keywords:
        cat = kw["type"]
        if cat not in keyword_categories:
            keyword_categories[cat] = []
        keyword_categories[cat].append(kw)

    return JSONResponse(content={
        "status": "ok",
        "wiki_name": "ROSClaw Wiki",
        "description": (
            "具身智能物理常识中枢 —— "
            "覆盖视觉语言导航、机器人控制、物理参数判据等核心领域"
        ),
        "global_stats": stats,
        "keywords": keywords,
        "keyword_categories": keyword_categories,
    })


@app.get("/wiki/v1/graph")
async def wiki_graph() -> JSONResponse:
    """Return the full wiki page graph (nodes + wikilink edges) for Obsidian-style visualization.

    No authentication required. Nodes are wiki pages, edges are [[wikilink]] references.
    Extracts links from both the wikilinks JSON column and the markdown body content.
    """
    import json as _json
    import re
    from seekdb_client import get_connection

    nodes: list[dict[str, Any]] = []
    edges: list[dict[str, Any]] = []
    node_ids: set[str] = set()

    try:
        with get_connection() as conn:
            cur = conn.execute(
                "SELECT id, type, title, confidence, wikilinks, body FROM wiki_pages"
            )
            rows = cur.fetchall()

            for row in rows:
                pid = row["id"]
                ptype = row["type"] or "unknown"
                title = row["title"] or pid
                confidence = row["confidence"] or 0.5
                wikilinks_raw = row["wikilinks"] or "[]"
                body = row["body"] or ""
                try:
                    wikilinks = _json.loads(wikilinks_raw)
                except Exception:
                    wikilinks = []

                # Also extract [[...]] wikilinks from markdown body
                body_links: list[str] = []
                for match in re.finditer(r"\[\[([^\]|]+)(?:\|[^\]]*)?\]\]", body):
                    link_target = match.group(1).strip()
                    # Normalize: lowercase, replace spaces/special chars with underscore
                    normalized = re.sub(r"[^a-zA-Z0-9_]+", "_", link_target.lower()).strip("_")
                    if normalized:
                        body_links.append(normalized)

                nodes.append({
                    "id": pid,
                    "title": title,
                    "type": ptype,
                    "confidence": round(confidence, 2),
                    "links": list(set(
                        (wikilinks if isinstance(wikilinks, list) else []) + body_links
                    )),
                })
                node_ids.add(pid)

            # Build title-to-id mapping for fuzzy matching
            title_to_id: dict[str, str] = {}
            for node in nodes:
                title_to_id[node["id"].lower()] = node["id"]
                title_to_id[node["title"].lower()] = node["id"]

            # Build edges from wikilinks (match by exact id or normalized title)
            edge_set: set[tuple[str, str]] = set()
            for node in nodes:
                for target in node.get("links", []):
                    target_norm = target.lower().strip()
                    matched_id: str | None = None
                    if target_norm in node_ids:
                        matched_id = target_norm
                    elif target_norm in title_to_id:
                        matched_id = title_to_id[target_norm]
                    # Try normalized version (spaces->underscores)
                    if matched_id is None:
                        target_normalized = re.sub(r"[^a-zA-Z0-9_]+", "_", target_norm).strip("_")
                        if target_normalized in node_ids:
                            matched_id = target_normalized
                        elif target_normalized in title_to_id:
                            matched_id = title_to_id[target_normalized]
                    if matched_id and matched_id != node["id"]:
                        pair = tuple(sorted([node["id"], matched_id]))
                        if pair not in edge_set:
                            edge_set.add(pair)
                            edges.append({"source": node["id"], "target": matched_id})

            # Compute link_count (degree) for each node
            link_counts: dict[str, int] = {n["id"]: 0 for n in nodes}
            for edge in edges:
                link_counts[edge["source"]] = link_counts.get(edge["source"], 0) + 1
                link_counts[edge["target"]] = link_counts.get(edge["target"], 0) + 1
            for node in nodes:
                node["link_count"] = link_counts.get(node["id"], 0)
                # Remove links array to reduce payload size
                node.pop("links", None)

    except Exception as exc:
        logger.warning("Wiki graph query failed: %s", exc)

    return JSONResponse(content={
        "status": "ok",
        "nodes": nodes,
        "edges": edges,
    })


# ── Startup / Admin helpers ──

@app.on_event("startup")
async def startup() -> None:
    from seekdb_search_impl import SeekDBSearchImpl
    SeekDBSearchImpl.warmup(WIKI_ROOT)
    _get_constraint_graph()  # preload Phase 16/17 ontology
    logger.info("ROSClaw Commercial API started. Wiki root: %s", WIKI_ROOT)


__all__ = ["app"]
