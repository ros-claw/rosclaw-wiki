"""ROSClaw Vector Semantic Search — sentence-transformers based indexing.

Uses all-MiniLM-L6-v2 for lightweight local embeddings.
Supports incremental updates and Reciprocal Rank Fusion (RRF) with whoosh.
"""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any

import numpy as np

import search_backend
import wiki_engine as engine

logger = logging.getLogger("rosclaw.vector_search")

# Lazy-loaded model singleton
_model = None
_EMBEDDING_DIM = 384


def _get_model():
    """Lazy-load the sentence-transformers model."""
    global _model
    if _model is None:
        from sentence_transformers import SentenceTransformer

        _model = SentenceTransformer(
            "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
        )
    return _model


def _get_index_dir(wiki_root: str) -> Path:
    return Path(wiki_root) / ".vector_index"


def _cosine_similarity(query_emb: np.ndarray, doc_matrix: np.ndarray) -> np.ndarray:
    """Compute cosine similarity between query and all docs."""
    query_norm = query_emb / (np.linalg.norm(query_emb) + 1e-10)
    doc_norm = doc_matrix / (np.linalg.norm(doc_matrix, axis=1, keepdims=True) + 1e-10)
    return np.dot(doc_norm, query_norm)


def build_vector_index(wiki_root: str) -> dict[str, Any]:
    """Rebuild the full vector index from all wiki pages.

    Returns:
        Summary dict with indexed_count.
    """
    model = _get_model()
    root = Path(wiki_root)
    index_dir = _get_index_dir(wiki_root)
    index_dir.mkdir(parents=True, exist_ok=True)

    docs: list[dict[str, str]] = []
    embeddings: list[np.ndarray] = []

    for md_file in root.rglob("*.md"):
        if md_file.name in ("index.md", "log.md", "Admin_Dashboard.md"):
            continue
        try:
            content = md_file.read_text(encoding="utf-8")
            meta, body = engine.parse_frontmatter(content)
            title = meta.get("title", md_file.stem)
            text = f"{title}\n{body[:2000]}"
            emb = model.encode(text, show_progress_bar=False)
            rel = str(md_file.relative_to(root))
            docs.append({"path": rel, "title": title, "text": text[:300]})
            embeddings.append(emb)
        except Exception as exc:
            logger.warning("Vector index error for %s: %s", md_file, exc)

    if embeddings:
        matrix = np.stack(embeddings).astype(np.float32)
        np.save(index_dir / "embeddings.npy", matrix)
        (index_dir / "docs.json").write_text(
            json.dumps(docs, ensure_ascii=False), encoding="utf-8"
        )
        logger.info("Vector index rebuilt: %d pages", len(docs))
    else:
        # Remove stale index files if no docs found
        for f in ("embeddings.npy", "docs.json"):
            fp = index_dir / f
            if fp.exists():
                fp.unlink()

    return {"status": "done", "indexed_count": len(docs)}


def index_page(wiki_root: str, rel_path: str) -> bool:
    """Incrementally add or update a single page in the vector index.

    Re-encodes the page and updates the stored matrix. This is a
    simple delete+insert approach (no full rebuild required).
    """
    page_path = Path(wiki_root) / rel_path
    if not page_path.exists():
        return False

    index_dir = _get_index_dir(wiki_root)
    emb_path = index_dir / "embeddings.npy"
    docs_path = index_dir / "docs.json"

    # Load existing index or create empty
    if emb_path.exists() and docs_path.exists():
        try:
            matrix = np.load(emb_path).astype(np.float32)
            docs: list[dict[str, str]] = json.loads(docs_path.read_text(encoding="utf-8"))
        except Exception:
            matrix = np.zeros((0, _EMBEDDING_DIM), dtype=np.float32)
            docs = []
    else:
        matrix = np.zeros((0, _EMBEDDING_DIM), dtype=np.float32)
        docs = []

    # Remove existing entry for this path
    keep_idx = [i for i, d in enumerate(docs) if d["path"] != rel_path]
    if len(keep_idx) != len(docs):
        matrix = matrix[keep_idx]
        docs = [docs[i] for i in keep_idx]

    # Encode and append new entry
    try:
        content = page_path.read_text(encoding="utf-8")
        meta, body = engine.parse_frontmatter(content)
        title = meta.get("title", page_path.stem)
        text = f"{title}\n{body[:2000]}"
        emb = _get_model().encode(text, show_progress_bar=False).astype(np.float32)

        matrix = np.vstack([matrix, emb.reshape(1, -1)])
        docs.append({"path": rel_path, "title": title, "text": text[:300]})
    except Exception as exc:
        logger.warning("Vector encode failed for %s: %s", rel_path, exc)
        return False

    # Save updated index
    index_dir.mkdir(parents=True, exist_ok=True)
    np.save(emb_path, matrix)
    docs_path.write_text(json.dumps(docs, ensure_ascii=False), encoding="utf-8")
    return True


def search_semantic(wiki_root: str, query: str, top_k: int = 10) -> list[dict[str, Any]]:
    """Search wiki pages by semantic similarity.

    Returns:
        List of dicts with file_path, title, snippet, score.
        Empty list if index is not available.
    """
    index_dir = _get_index_dir(wiki_root)
    emb_path = index_dir / "embeddings.npy"
    docs_path = index_dir / "docs.json"

    if not emb_path.exists() or not docs_path.exists():
        return []

    try:
        matrix = np.load(emb_path).astype(np.float32)
        docs: list[dict[str, str]] = json.loads(docs_path.read_text(encoding="utf-8"))
    except Exception as exc:
        logger.warning("Failed to load vector index: %s", exc)
        return []

    if matrix.shape[0] == 0:
        return []

    query_emb = _get_model().encode(query, show_progress_bar=False).astype(np.float32)
    scores = _cosine_similarity(query_emb, matrix)

    top_indices = np.argsort(scores)[::-1][:top_k]
    results = []
    for idx in top_indices:
        if scores[idx] <= 0.05:
            continue
        results.append({
            "file_path": docs[idx]["path"],
            "title": docs[idx]["title"],
            "snippet": docs[idx].get("text", "")[:200],
            "score": round(float(scores[idx]), 4),
        })
    return results


def search_hybrid(
    wiki_root: str, query: str, top_k: int = 10, k: int = 60
) -> list[dict[str, Any]]:
    """Hybrid search combining whoosh full-text and semantic search via RRF.

    Reciprocal Rank Fusion formula:
        score(doc) = sum_i( 1 / (k + rank_i(doc)) )

    Args:
        wiki_root: Path to wiki root.
        query: Search query.
        top_k: Number of results to return.
        k: RRF constant (default 60).

    Returns:
        Re-ranked list of dicts with file_path, title, snippet, score.
    """
    # Gather results from both sources
    whoosh_results = search_backend.search_index(wiki_root, query, limit=top_k * 2)
    semantic_results = search_semantic(wiki_root, query, top_k=top_k * 2)

    rrf_scores: dict[str, float] = {}
    meta_store: dict[str, dict[str, Any]] = {}

    for rank, hit in enumerate(whoosh_results):
        doc_id = hit["file_path"]
        rrf_scores[doc_id] = rrf_scores.get(doc_id, 0.0) + 1.0 / (k + rank + 1)
        if doc_id not in meta_store:
            meta_store[doc_id] = hit

    for rank, hit in enumerate(semantic_results):
        doc_id = hit["file_path"]
        rrf_scores[doc_id] = rrf_scores.get(doc_id, 0.0) + 1.0 / (k + rank + 1)
        if doc_id not in meta_store:
            meta_store[doc_id] = hit

    # Sort by RRF score descending
    sorted_docs = sorted(rrf_scores.items(), key=lambda x: x[1], reverse=True)[:top_k]

    results = []
    for doc_id, score in sorted_docs:
        meta = meta_store.get(doc_id, {})
        results.append({
            "file_path": doc_id,
            "title": meta.get("title", Path(doc_id).stem),
            "snippet": meta.get("snippet", meta.get("text", "")[:200]),
            "score": round(score, 4),
        })
    return results
