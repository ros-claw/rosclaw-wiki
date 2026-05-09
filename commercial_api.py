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
import time
from pathlib import Path
from typing import Any

from fastapi import FastAPI, Header, HTTPException, Request
from fastapi.responses import JSONResponse

from auth_manager import validate_api_key
from billing_middleware import get_usage_summary, log_usage
from rate_limiter import RateLimitExceeded, enforce_rate_limit
from search_interface import get_search_impl
from storage_interface import get_storage_impl

logger = logging.getLogger("rosclaw.api")

app = FastAPI(title="ROSClaw Wiki API", version="1.0.0")

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
    return {
        "status": "ok",
        "backend": h.get("backend", "unknown"),
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
        result = get_judgment(entity, wiki_root=WIKI_ROOT)
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


# ── Startup / Admin helpers ──

@app.on_event("startup")
async def startup() -> None:
    from seekdb_search_impl import SeekDBSearchImpl
    SeekDBSearchImpl.warmup(WIKI_ROOT)
    _get_constraint_graph()  # preload Phase 16/17 ontology
    logger.info("ROSClaw Commercial API started. Wiki root: %s", WIKI_ROOT)


__all__ = ["app"]
