"""ROSClaw Search Backend — whoosh-based full-text indexing with grep fallback.

Supports incremental indexing and relevance-scored search.
Semantic search is reserved for Phase 4.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

try:
    from whoosh import index as whoosh_index
    from whoosh.fields import ID, KEYWORD, TEXT, Schema
    from whoosh.qparser import MultifieldParser, OrGroup, QueryParser
    from whoosh.query import Every

    WHOOSH_AVAILABLE = True
except ImportError:
    WHOOSH_AVAILABLE = False

import wiki_engine as engine

logger = logging.getLogger("rosclaw.search")

_DEFAULT_SCHEMA = Schema(
    path=ID(stored=True, unique=True),
    title=TEXT(stored=True),
    tags=KEYWORD(stored=True, commas=True, lowercase=True),
    body=TEXT(stored=True),
)


def _get_index_dir(wiki_root: str) -> Path:
    # Use data dir for index to support read-only wiki mounts in production
    return Path(wiki_root).parent / "data" / ".search_index"


def init_index(wiki_root: str) -> Any:
    """Create or open the whoosh index. Returns the Index object or None."""
    if not WHOOSH_AVAILABLE:
        logger.warning("whoosh not installed; search will use grep fallback")
        return None

    idx_dir = _get_index_dir(wiki_root)
    try:
        idx_dir.mkdir(parents=True, exist_ok=True)
    except OSError:
        logger.warning("Cannot create whoosh index dir (read-only fs); search will use grep fallback")
        return None

    if whoosh_index.exists_in(str(idx_dir)):
        return whoosh_index.open_dir(str(idx_dir))

    return whoosh_index.create_in(str(idx_dir), _DEFAULT_SCHEMA)


def index_page(wiki_root: str, rel_path: str) -> bool:
    """Incrementally index (or re-index) a single wiki page.

    Args:
        wiki_root: Path to wiki root.
        rel_path: Relative path to the .md file (e.g., "algorithms/wildos.md").

    Returns:
        True if indexed successfully, False otherwise.
    """
    if not WHOOSH_AVAILABLE:
        return False

    idx = init_index(wiki_root)
    if idx is None:
        return False

    page_path = Path(wiki_root) / rel_path
    if not page_path.exists():
        return False

    try:
        content = page_path.read_text(encoding="utf-8")
        meta, body = engine.parse_frontmatter(content)
    except Exception as exc:
        logger.warning("Failed to parse %s for indexing: %s", page_path, exc)
        return False

    title = meta.get("title", page_path.stem)
    tags = ",".join(str(t) for t in meta.get("tags", []))

    writer = idx.writer()
    writer.update_document(
        path=rel_path,
        title=title,
        tags=tags,
        body=body,
    )
    writer.commit()
    return True


def rebuild_index(wiki_root: str) -> dict[str, Any]:
    """Rebuild the entire search index from all wiki pages.

    Returns:
        Summary dict with indexed_count and errors.
    """
    if not WHOOSH_AVAILABLE:
        return {"status": "unavailable", "reason": "whoosh not installed"}

    root = Path(wiki_root)
    idx_dir = _get_index_dir(wiki_root)
    if idx_dir.exists():
        import shutil

        shutil.rmtree(idx_dir)
    idx_dir.mkdir(parents=True, exist_ok=True)
    idx = whoosh_index.create_in(str(idx_dir), _DEFAULT_SCHEMA)

    indexed = 0
    errors = 0
    writer = idx.writer()

    for md_file in root.rglob("*.md"):
        if md_file.name in ("index.md", "log.md", "Admin_Dashboard.md"):
            continue
        try:
            content = md_file.read_text(encoding="utf-8")
            meta, body = engine.parse_frontmatter(content)
            rel = str(md_file.relative_to(root))
            title = meta.get("title", md_file.stem)
            tags = ",".join(str(t) for t in meta.get("tags", []))
            writer.add_document(
                path=rel,
                title=title,
                tags=tags,
                body=body,
            )
            indexed += 1
        except Exception as exc:
            logger.warning("Index error for %s: %s", md_file, exc)
            errors += 1

    writer.commit()
    logger.info("Index rebuilt: %d pages indexed, %d errors", indexed, errors)
    return {"status": "done", "indexed_count": indexed, "errors": errors}


def _grep_fallback(wiki_root: str, query: str, limit: int = 20) -> list[dict[str, Any]]:
    """Simple text scan fallback when whoosh index is empty."""
    root = Path(wiki_root)
    query_lower = query.lower()
    output: list[dict[str, Any]] = []
    for md_file in root.rglob("*.md"):
        if md_file.name in ("index.md", "log.md", "Admin_Dashboard.md"):
            continue
        try:
            content = md_file.read_text(encoding="utf-8")
            meta, body = engine.parse_frontmatter(content)
            title = meta.get("title", md_file.stem)
            text = f"{title}\n{body}".lower()
            if query_lower in text:
                # Simple scoring: count occurrences
                score = text.count(query_lower)
                # Find snippet around first match
                idx = text.find(query_lower)
                start = max(0, idx - 80)
                end = min(len(body), idx + len(query) + 80)
                snippet = body[start:end].replace("\n", " ")
                output.append({
                    "file_path": str(md_file.relative_to(root)),
                    "title": title,
                    "snippet": snippet,
                    "score": score,
                })
        except Exception:
            continue
    output.sort(key=lambda x: x["score"], reverse=True)
    return output[:limit]


def search_index(wiki_root: str, query: str, limit: int = 20) -> list[dict[str, Any]]:
    """Search the whoosh index and return scored results.

    Returns:
        List of dicts with file_path, title, snippet, score.
        Empty list if whoosh is unavailable or no matches.
    """
    if not WHOOSH_AVAILABLE:
        return _grep_fallback(wiki_root, query, limit)

    idx = init_index(wiki_root)
    if idx is None:
        return _grep_fallback(wiki_root, query, limit)

    with idx.searcher() as searcher:
        if searcher.doc_count() == 0:
            return _grep_fallback(wiki_root, query, limit)

        # Try multifield search first (title, tags, body) with OR group for better
        # tolerance of stop-words and multi-term queries.
        parser = MultifieldParser(["title", "tags", "body"], idx.schema, group=OrGroup)
        try:
            q = parser.parse(query)
        except Exception:
            # Fallback to simple term parser
            parser = QueryParser("body", idx.schema, group=OrGroup)
            q = parser.parse(query)

        results = searcher.search(q, limit=limit)
        output = []
        for hit in results:
            output.append({
                "file_path": hit["path"],
                "title": hit["title"],
                "snippet": hit.highlights("body") or hit["body"][:200],
                "score": hit.score,
            })
        return output


def _rrf_fuse(result_lists: list[list[dict[str, Any]]], k: int = 60) -> list[dict[str, Any]]:
    """Reciprocal Rank Fusion across multiple ranked result lists.

    Args:
        result_lists: Each list is ordered by relevance (best first).
        k: RRF constant (default 60).

    Returns:
        Fused list sorted by RRF score descending.
    """
    scores: dict[str, float] = {}
    metadata: dict[str, dict[str, Any]] = {}

    for results in result_lists:
        for rank, hit in enumerate(results):
            key = hit.get("file_path", hit.get("id", str(rank)))
            scores[key] = scores.get(key, 0.0) + 1.0 / (k + rank + 1)
            if key not in metadata:
                metadata[key] = hit

    fused = []
    for key, score in sorted(scores.items(), key=lambda x: x[1], reverse=True):
        item = dict(metadata[key])
        item["rrf_score"] = round(score, 4)
        fused.append(item)

    return fused


def search_wiki(
    wiki_root: str,
    query: str,
    search_type: str = "default",
    limit: int = 20,
    llm_func: Any | None = None,
) -> dict[str, Any]:
    """Unified wiki search with multiple search modes.

    Args:
        wiki_root: Path to wiki root.
        query: Search query string.
        search_type: "default" | "expanded" | "judgment"
        limit: Max results to return.
        llm_func: Optional LLM callback for query expansion.
            Signature: llm_func(prompt: str) -> str (JSON array of query variants)

    Returns:
        Dict with status, query, results.
    """
    if search_type == "default":
        results = search_index(wiki_root, query, limit)
        return {"status": "done", "query": query, "search_type": "default", "results": results}

    if search_type == "expanded":
        if llm_func is None:
            # Without LLM, fall back to simple synonym expansion
            variants = _simple_query_expansion(query)
        else:
            variants = _llm_query_expansion(query, llm_func)

        result_lists: list[list[dict[str, Any]]] = []
        for variant in variants:
            result_lists.append(search_index(wiki_root, variant, limit))

        fused = _rrf_fuse(result_lists)
        return {
            "status": "done",
            "query": query,
            "search_type": "expanded",
            "variants": variants,
            "results": fused[:limit],
        }

    if search_type == "judgment":
        try:
            from judgment_generator import list_judgments
            result = list_judgments(wiki_root=wiki_root)
            # Filter by query if provided
            filtered = [
                j for j in result.get("judgments", [])
                if query.lower() in j.get("parameter", "").lower()
                or query.lower() in j.get("entity", "").lower()
                or query.lower() in j.get("context", "").lower()
            ]
            return {
                "status": "done",
                "query": query,
                "search_type": "judgment",
                "results": filtered[:limit],
            }
        except Exception as exc:
            logger.warning("judgment search failed: %s", exc)
            return {"status": "error", "query": query, "search_type": "judgment", "results": [], "error": str(exc)}

    return {"status": "error", "query": query, "search_type": search_type, "results": [], "error": "Unknown search_type"}


def _simple_query_expansion(query: str) -> list[str]:
    """Lightweight deterministic query expansion (zero LLM).

    Returns original + stemmed + keyword-only variants.
    """
    variants = [query]
    # Drop common stop words for a broader variant
    stop_words = {"the", "a", "an", "is", "are", "was", "were", "what", "how", "does", "do", "in", "on", "of", "for", "to", "and", "or"}
    tokens = query.lower().split()
    filtered = [t for t in tokens if t not in stop_words]
    if filtered and " ".join(filtered) != query.lower():
        variants.append(" ".join(filtered))
    return variants


def _llm_query_expansion(query: str, llm_func: Any) -> list[str]:
    """Use LLM to generate query variants. Falls back to simple expansion on failure."""
    prompt = (
        f"Generate 3 different ways to search for this query. "
        f"Return ONLY a JSON array of strings.\n\nQuery: {query}"
    )
    try:
        import json
        response = llm_func(prompt)
        variants = json.loads(response)
        if isinstance(variants, list) and len(variants) >= 2:
            # Ensure original is included
            if query not in variants:
                variants.insert(0, query)
            return variants[:4]  # cap at 4
    except Exception as exc:
        logger.warning("LLM query expansion failed: %s", exc)
    return _simple_query_expansion(query)
