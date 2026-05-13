"""SeekDB Search Implementation — SearchInterface backed by real pyseekdb.

Uses pyseekdb collections with native HNSW vector index + fulltext + hybrid search.
"""
from __future__ import annotations

import json
import logging
import time
from typing import Any

import numpy as np

from search_interface import SearchInterface

logger = logging.getLogger("rosclaw.seekdb_search")


def _cosine_similarity(q: np.ndarray, docs: np.ndarray) -> np.ndarray:
    qn = q / (np.linalg.norm(q) + 1e-10)
    dn = docs / (np.linalg.norm(docs, axis=1, keepdims=True) + 1e-10)
    return np.dot(dn, qn)


class SeekDBSearchImpl(SearchInterface):
    """SeekDB-backed search using pyseekdb collections."""

    _model: Any | None = None
    _warmed_up: bool = False

    def __init__(self, wiki_root: str = "wiki") -> None:
        self.wiki_root = wiki_root
        # Simple LRU cache for hybrid search: {query: (results, timestamp)}
        self._hybrid_cache: dict[str, tuple[list[dict[str, Any]], float]] = {}
        self._cache_max_size = 100
        self._cache_ttl_seconds = 300

    def _get_model(self) -> Any:
        if SeekDBSearchImpl._model is None:
            from sentence_transformers import SentenceTransformer
            SeekDBSearchImpl._model = SentenceTransformer("all-MiniLM-L6-v2")
        return SeekDBSearchImpl._model

    @classmethod
    def warmup(cls, wiki_root: str = "wiki") -> None:
        """Warm-up fulltext index and embedding model (call once at process startup)."""
        if cls._warmed_up:
            return
        impl = cls(wiki_root)
        # Warm-up fulltext index
        try:
            _ = impl.search("warmup", search_type="keyword", top_k=1)
        except Exception:
            pass
        # Warm-up embedding model + vector index
        try:
            _ = impl.search("warmup", search_type="semantic", top_k=1)
        except Exception:
            pass
        # Warm-up judgments collection fulltext index
        try:
            _ = impl.search("warmup", search_type="judgment", top_k=1)
        except Exception:
            pass
        cls._warmed_up = True
        logger.info("SeekDBSearchImpl warm-up complete")

    # ── Search ──

    def search(self, query: str, search_type: str = "hybrid", top_k: int = 10, **kwargs: Any) -> list[dict[str, Any]]:
        if search_type == "keyword":
            return self._search_keyword(query, top_k)
        if search_type == "semantic":
            return self._search_semantic(query, top_k)
        if search_type == "hybrid":
            cache_key = f"{query}:{top_k}"
            cached = self._hybrid_cache.get(cache_key)
            if cached and (time.time() - cached[1]) < self._cache_ttl_seconds:
                return list(cached[0])
            results = self._search_hybrid(query, top_k)
            self._hybrid_cache[cache_key] = (results, time.time())
            # Trim cache if too large
            if len(self._hybrid_cache) > self._cache_max_size:
                oldest = min(self._hybrid_cache, key=lambda k: self._hybrid_cache[k][1])
                del self._hybrid_cache[oldest]
            return results
        if search_type == "expanded":
            llm_func = kwargs.get("llm_func")
            return self._search_expanded(query, top_k, llm_func)
        if search_type == "judgment":
            return self._search_judgment(query, top_k)
        logger.warning("Unknown search_type '%s', falling back to keyword", search_type)
        return self._search_keyword(query, top_k)

    def _search_keyword(self, query: str, top_k: int) -> list[dict[str, Any]]:
        coll = self._wiki_collection()
        try:
            results = coll.get(
                where_document={"$contains": query},
                limit=top_k * 2,
                include=["documents", "metadatas"],
            )
        except Exception as exc:
            logger.warning("Keyword search error: %s", exc)
            return []
        return self._format_results(results)

    def _search_semantic(self, query: str, top_k: int) -> list[dict[str, Any]]:
        try:
            model = self._get_model()
            q_emb = model.encode(query, show_progress_bar=False).astype(np.float32)
        except Exception as exc:
            logger.warning("Semantic search failed (model unavailable): %s", exc)
            return []

        coll = self._wiki_collection()
        try:
            results = coll.query(
                query_embeddings=[q_emb.tolist()],
                n_results=top_k,
                include=["documents", "metadatas", "distances"],
            )
        except Exception as exc:
            logger.warning("Semantic query error: %s", exc)
            return []
        return self._format_results(results, distance_key="distances")

    def _search_hybrid(self, query: str, top_k: int) -> list[dict[str, Any]]:
        try:
            model = self._get_model()
            q_emb = model.encode(query, show_progress_bar=False).astype(np.float32)
        except Exception as exc:
            logger.warning("Hybrid search fallback to keyword: %s", exc)
            return self._search_keyword(query, top_k)

        coll = self._wiki_collection()
        try:
            results = coll.hybrid_search(
                query={"where_document": {"$contains": query}, "n_results": top_k * 2},
                knn={"query_embeddings": [q_emb.tolist()], "n_results": top_k * 2},
                rank={"rrf": {}},
                n_results=top_k,
                include=["documents", "metadatas"],
            )
        except Exception as exc:
            logger.warning("Hybrid search error, fallback to keyword: %s", exc)
            return self._search_keyword(query, top_k)
        return self._format_results(results)

    def _search_expanded(self, query: str, top_k: int, llm_func: Any) -> list[dict[str, Any]]:
        variants = [query]
        if llm_func is not None:
            try:
                import json as _json
                prompt = f"Generate 3 variants of this search query. Return JSON array of strings only.\nQuery: {query}"
                response = llm_func(prompt, "")
                parsed = _json.loads(response)
                if isinstance(parsed, list):
                    variants = [query] + [v for v in parsed if v != query][:3]
            except Exception:
                pass

        # Keyword search each variant, then RRF fuse
        k = 60
        scores: dict[str, float] = {}
        meta: dict[str, dict[str, Any]] = {}
        for variant in variants:
            for rank, hit in enumerate(self._search_keyword(variant, top_k)):
                key = hit["file_path"]
                scores[key] = scores.get(key, 0.0) + 1.0 / (k + rank + 1)
                if key not in meta:
                    meta[key] = hit

        fused = []
        for key, score in sorted(scores.items(), key=lambda x: x[1], reverse=True)[:top_k]:
            item = dict(meta[key])
            item["rrf_score"] = round(score, 4)
            fused.append(item)
        return fused

    def _search_judgment(self, query: str, top_k: int) -> list[dict[str, Any]]:
        coll = self._judgments_collection()
        try:
            results = coll.get(
                where_document={"$contains": query},
                limit=top_k,
                include=["documents", "metadatas"],
            )
        except Exception as exc:
            logger.warning("Judgment search error: %s", exc)
            return []
        return self._format_judgment_results(results)

    # ── Graph queries ──

    def query_graph(self, entity_name: str, radius: int = 2) -> dict[str, Any]:
        """Query code graph for callers/callees of a named entity.

        Args:
            entity_name: Function/class name to look up.
            radius: 1 = direct callers/callees, 2 = indirect.

        Returns:
            Dict with "node", "callers", "callees", "centrality".
        """
        import json as _json
        from pathlib import Path

        graph_path = Path("data/code_graph.json")
        if not graph_path.exists():
            return {"node": None, "callers": [], "callees": [], "centrality": {}}

        graph = _json.loads(graph_path.read_text(encoding="utf-8"))
        node_by_id = {n["id"]: n for n in graph.get("nodes", [])}

        # Find node(s) matching entity_name
        matches = [n for n in graph.get("nodes", []) if n.get("name") == entity_name]
        if not matches:
            return {"node": None, "callers": [], "callees": [], "centrality": {}}

        target = matches[0]
        target_id = target["id"]

        # Build edge index
        callers: list[dict[str, Any]] = []
        callees: list[dict[str, Any]] = []
        for edge in graph.get("edges", []):
            if edge.get("target") == target_id or edge.get("target") == entity_name:
                src_id = edge.get("source", "")
                src_node = node_by_id.get(src_id)
                if src_node:
                    callers.append({"id": src_id, **src_node, "edge_type": edge.get("type", "calls")})
            if edge.get("source") == target_id:
                tgt_name = edge.get("target", "")
                tgt_node = next((n for n in graph.get("nodes", []) if n.get("id") == tgt_name or n.get("name") == tgt_name), None)
                if tgt_node:
                    callees.append({"id": tgt_name, **tgt_node, "edge_type": edge.get("type", "calls")})

        # If radius >= 2, gather indirect relationships
        if radius >= 2:
            indirect_callers: list[dict[str, Any]] = []
            indirect_callees: list[dict[str, Any]] = []
            caller_ids = {c["id"] for c in callers}
            callee_ids = {c["id"] for c in callees}
            for edge in graph.get("edges", []):
                if edge.get("target") in caller_ids:
                    src_id = edge.get("source", "")
                    src_node = node_by_id.get(src_id)
                    if src_node and src_id != target_id:
                        indirect_callers.append({"id": src_id, **src_node, "edge_type": "indirect_calls"})
                if edge.get("source") in callee_ids:
                    tgt_name = edge.get("target", "")
                    tgt_node = next((n for n in graph.get("nodes", []) if n.get("id") == tgt_name or n.get("name") == tgt_name), None)
                    if tgt_node and tgt_name != target_id:
                        indirect_callees.append({"id": tgt_name, **tgt_node, "edge_type": "indirect_calls"})
            callers.extend(indirect_callers)
            callees.extend(indirect_callees)

        # Sort by centrality score if available
        centrality = target.get("centrality", {})
        callers.sort(key=lambda x: x.get("centrality", {}).get("in_degree", 0), reverse=True)
        callees.sort(key=lambda x: x.get("centrality", {}).get("in_degree", 0), reverse=True)

        return {
            "node": target,
            "callers": callers[:20],
            "callees": callees[:20],
            "centrality": centrality,
        }

    # ── Index management ──

    def index_page(self, page_path: str, content: str | None = None) -> bool:
        import wiki_engine as engine
        from pathlib import Path

        path = Path(page_path)
        if content is None:
            if not path.exists():
                return False
            content = path.read_text(encoding="utf-8")

        meta, body = engine.parse_frontmatter(content)
        page_id = meta.get("id", path.stem)
        title = meta.get("title", path.stem)
        page_type = meta.get("type", "episode")
        tags = ",".join(meta.get("tags", []))
        confidence = meta.get("confidence", 0.5)
        created_at = str(meta.get("created_at", ""))
        last_reinforced = str(meta.get("last_reinforced", ""))
        def _json_default(obj: Any) -> str:
            if hasattr(obj, "isoformat"):
                return obj.isoformat()
            return str(obj)

        sources = json.dumps(meta.get("sources", []), ensure_ascii=False, default=_json_default)
        wikilinks = ",".join(
            [m.group(1).split("|")[0].strip() for m in __import__("re").finditer(r"\[\[([^\]]+)\]\]", body)]
        )

        # Load vector if available
        embedding = None
        try:
            from vector_index import _get_index_dir
            idx_dir = _get_index_dir(self.wiki_root)
            emb_path = idx_dir / "embeddings.npy"
            docs_path = idx_dir / "docs.json"
            if emb_path.exists() and docs_path.exists():
                rel = str(path.relative_to(self.wiki_root)) if path.is_absolute() else str(path)
                docs = json.loads(docs_path.read_text(encoding="utf-8"))
                matrix = np.load(emb_path).astype(np.float32)
                for i, doc in enumerate(docs):
                    if doc["path"] == rel:
                        embedding = [round(float(x), 6) for x in matrix[i].tolist()]
                        break
        except Exception:
            pass

        # Fallback: generate embedding on the fly if no pre-computed vector
        if embedding is None:
            try:
                model = self._get_model()
                emb = model.encode(body, show_progress_bar=False).astype(np.float32)
                embedding = [round(float(x), 6) for x in emb.tolist()]
            except Exception as exc:
                logger.warning("Embedding generation failed for %s: %s", page_id, exc)

        coll = self._wiki_collection()
        try:
            coll.upsert(
                ids=[page_id],
                documents=[body],
                embeddings=[embedding] if embedding else None,
                metadatas=[{
                    "type": page_type,
                    "title": title,
                    "tags": tags,
                    "confidence": confidence,
                    "created_at": created_at,
                    "last_reinforced": last_reinforced,
                    "sources": sources,
                    "wikilinks": wikilinks,
                }],
            )
            return True
        except Exception as exc:
            logger.warning("Index page error for %s: %s", page_id, exc)
            return False

    def rebuild_index(self) -> dict[str, Any]:
        from pathlib import Path
        import wiki_engine as engine

        root = Path(self.wiki_root)
        indexed = 0
        errors = 0
        for md_file in root.rglob("*.md"):
            if md_file.name in ("index.md", "log.md", "Admin_Dashboard.md"):
                continue
            try:
                if self.index_page(str(md_file)):
                    indexed += 1
                else:
                    errors += 1
            except Exception as exc:
                logger.warning("Index error for %s: %s", md_file, exc)
                errors += 1

        return {"status": "done", "indexed_count": indexed, "errors": errors, "backend": "pyseekdb"}

    def delete_from_index(self, page_path: str) -> bool:
        from pathlib import Path
        page_id = Path(page_path).stem
        coll = self._wiki_collection()
        try:
            coll.delete(ids=[page_id])
            return True
        except Exception as exc:
            logger.warning("Delete from index error: %s", exc)
            return False

    def health(self) -> dict[str, Any]:
        from seekdb_collection_client import health_check
        return health_check()

    # ── Helpers ──

    def _wiki_collection(self):
        from seekdb_collection_client import get_wiki_collection
        return get_wiki_collection()

    def _judgments_collection(self):
        from seekdb_collection_client import get_judgments_collection
        return get_judgments_collection()

    def _format_results(self, results: dict[str, Any], distance_key: str | None = None) -> list[dict[str, Any]]:
        ids = results.get("ids", [])
        documents = results.get("documents", [])
        metadatas = results.get("metadatas", [])
        distances = results.get(distance_key, []) if distance_key else []

        # Handle nested list structure (batch results)
        if ids and isinstance(ids[0], list):
            ids = ids[0]
            documents = documents[0] if documents else []
            metadatas = metadatas[0] if metadatas else []
            distances = distances[0] if distances else []

        formatted = []
        for i, doc_id in enumerate(ids):
            meta = metadatas[i] if i < len(metadatas) else {}
            doc = documents[i] if i < len(documents) else ""
            score = distances[i] if (distance_key and i < len(distances)) else 1.0
            formatted.append({
                "file_path": doc_id,
                "title": meta.get("title", doc_id),
                "snippet": (doc or "")[:200],
                "score": round(float(score), 4) if distance_key else round(float(score), 4),
            })
        return formatted

    def _format_judgment_results(self, results: dict[str, Any]) -> list[dict[str, Any]]:
        ids = results.get("ids", [])
        documents = results.get("documents", [])
        metadatas = results.get("metadatas", [])

        if ids and isinstance(ids[0], list):
            ids = ids[0]
            documents = documents[0] if documents else []
            metadatas = metadatas[0] if metadatas else []

        formatted = []
        for i, doc_id in enumerate(ids):
            meta = metadatas[i] if i < len(metadatas) else {}
            doc = documents[i] if i < len(documents) else ""
            formatted.append({
                "file_path": f"judgments/{doc_id}",
                "title": f"Judgment: {meta.get('parameter', doc_id)}",
                "snippet": f"{meta.get('entity', '')} — {doc}",
                "score": meta.get("confidence", 0.0),
            })
        return formatted


__all__ = ["SeekDBSearchImpl"]
