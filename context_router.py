"""ROSClaw Context Router — route scenario descriptions to relevant judgments and pages.

Given a natural-language scenario (e.g., "G1 slips on wet ground"),
the router returns the most relevant judgments and wiki pages.

Routing logic:
  1. Extract keywords from scenario
  2. Match judgment context + parameter fields
  3. Search wiki pages as fallback
  4. Sort by confidence, boost items with warnings
  5. Return top K with priority flags
"""

from __future__ import annotations

import logging
import re
from pathlib import Path
from typing import Any

import wiki_engine as engine

logger = logging.getLogger("rosclaw.context_router")

# Context keyword mapping for scenario interpretation
_SCENARIO_CONTEXT_MAP: dict[str, list[str]] = {
    "locomotion_control": ["slip", "wet", "ground", "torque", "gait", "walk", "speed", "velocity", "friction"],
    "manipulation": ["grasp", "grip", "object", "pick", "place", "arm", "hand"],
    "perception": ["see", "detect", "recognize", "camera", "lidar", "vision", "sensor"],
    "navigation": ["map", "path", "route", "plan", "slam", "localize", "lost"],
    "safety": ["emergency", "stop", "collision", "fall", "danger", "limit"],
    "power": ["battery", "charge", "die", "low", "voltage", "power"],
}


def _extract_keywords(text: str) -> set[str]:
    """Extract meaningful keywords from scenario text."""
    text = text.lower()
    # Remove punctuation
    text = re.sub(r"[^\w\s]", " ", text)
    tokens = text.split()
    stop_words = {"the", "a", "an", "is", "are", "was", "were", "what", "how", "does", "do", "in", "on", "of", "for", "to", "and", "or", "it", "this", "that"}
    return {t for t in tokens if t not in stop_words and len(t) >= 2}


def _infer_context_from_scenario(scenario: str) -> str:
    """Infer the operational context from scenario keywords."""
    keywords = _extract_keywords(scenario)
    scores: dict[str, int] = {}
    for ctx, ctx_keywords in _SCENARIO_CONTEXT_MAP.items():
        score = sum(1 for kw in ctx_keywords if kw in keywords)
        if score > 0:
            scores[ctx] = score
    if scores:
        return max(scores.items(), key=lambda x: x[1])[0]
    return "general"


def _score_judgment_relevance(judgment: dict[str, Any], keywords: set[str]) -> float:
    """Score how relevant a judgment is to the given keywords."""
    score = 0.0
    text = f"{judgment.get('parameter', '')} {judgment.get('context', '')} {judgment.get('usage_notes', '')}"
    text_lower = text.lower()

    for kw in keywords:
        if kw in text_lower:
            score += 1.0

    # Boost confidence-weighted relevance
    score += judgment.get("confidence", 0.0) * 2.0

    # Boost warnings
    if judgment.get("unresolved") or "⚠️" in judgment.get("usage_notes", ""):
        score += 3.0

    return score


def _score_page_relevance(page: dict[str, Any], keywords: set[str]) -> float:
    """Score how relevant a wiki page is to the given keywords."""
    score = 0.0
    text = f"{page.get('title', '')} {page.get('body', '')}".lower()
    for kw in keywords:
        if kw in text:
            score += 1.0
    return score


def route(
    scenario: str,
    wiki_root: str,
    top_k: int = 5,
) -> dict[str, Any]:
    """Route a scenario description to the most relevant judgments and pages.

    Args:
        scenario: Natural language scenario (e.g., "G1 slips on wet ground").
        wiki_root: Wiki root directory.
        top_k: Number of top results to return.

    Returns:
        Dict with inferred_context, judgments, pages, and priority_items.
    """
    keywords = _extract_keywords(scenario)
    inferred_context = _infer_context_from_scenario(scenario)

    # 1. Load judgments
    all_judgments: list[dict[str, Any]] = []
    try:
        from judgment_generator import list_judgments
        result = list_judgments(wiki_root=wiki_root)
        all_judgments = result.get("judgments", [])
    except Exception as exc:
        logger.warning("Failed to load judgments: %s", exc)

    # 2. Score and rank judgments
    scored_judgments = []
    for j in all_judgments:
        rel_score = _score_judgment_relevance(j, keywords)
        # Boost if context matches inferred context
        if j.get("context") == inferred_context:
            rel_score += 2.0
        scored_judgments.append((rel_score, j))

    scored_judgments.sort(key=lambda x: x[0], reverse=True)
    top_judgments = scored_judgments[:top_k]

    # 3. Search wiki pages as fallback/supplement
    all_pages: list[dict[str, Any]] = []
    try:
        from search_backend import search_index
        search_results = search_index(wiki_root, scenario, limit=top_k * 2)
        all_pages = search_results
    except Exception as exc:
        logger.warning("Wiki search failed: %s", exc)

    scored_pages = []
    for page in all_pages:
        rel_score = _score_page_relevance(page, keywords)
        scored_pages.append((rel_score, page))

    scored_pages.sort(key=lambda x: x[0], reverse=True)
    top_pages = scored_pages[:top_k]

    # 4. Identify high-priority items (warnings or unresolved)
    priority_items: list[dict[str, Any]] = []
    for score, j in top_judgments:
        if j.get("unresolved") or "⚠️" in j.get("usage_notes", ""):
            priority_items.append({
                "type": "judgment",
                "entity": j.get("entity"),
                "parameter": j.get("parameter"),
                "reason": "unresolved_conflict" if j.get("unresolved") else "warning_note",
                "message": "建议立即处理" if j.get("unresolved") else "注意使用限制",
            })

    return {
        "status": "done",
        "scenario": scenario,
        "inferred_context": inferred_context,
        "keywords": sorted(keywords),
        "judgments": [j for _, j in top_judgments],
        "pages": [p for _, p in top_pages],
        "priority_items": priority_items,
    }


def route_with_judgment_search(
    scenario: str,
    wiki_root: str,
    top_k: int = 5,
) -> dict[str, Any]:
    """Enhanced route that also searches judgment parameter names directly.

    This is the primary MCP-facing entry point.
    """
    result = route(scenario, wiki_root, top_k)

    # If no judgments matched, try broader keyword search in judgment files
    if not result["judgments"]:
        try:
            from judgment_generator import list_judgments
            all_j = list_judgments(wiki_root=wiki_root).get("judgments", [])
            keywords = _extract_keywords(scenario)
            # Broader match: any keyword overlap
            matched = []
            for j in all_j:
                j_text = f"{j.get('parameter', '')} {j.get('entity', '')} {j.get('context', '')}".lower()
                if any(kw in j_text for kw in keywords):
                    matched.append(j)
            # Sort by confidence
            matched.sort(key=lambda x: x.get("confidence", 0), reverse=True)
            result["judgments"] = matched[:top_k]
        except Exception as exc:
            logger.warning("Broad judgment search failed: %s", exc)

    return result
