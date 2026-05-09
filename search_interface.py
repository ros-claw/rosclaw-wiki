"""Search Interface Abstraction Layer — unified search for Phase 10.

Provides SearchInterface protocol with FileSystemSearchImpl.
Phase 11 will add SeekDBSearchImpl without changing upper-layer code.
"""

from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

logger = logging.getLogger("rosclaw.search_interface")


class SearchInterface(ABC):
    """Abstract search interface. Upper-layer code must use this, not backend modules directly."""

    @abstractmethod
    def search(self, query: str, search_type: str = "hybrid", top_k: int = 10, **kwargs: Any) -> list[dict[str, Any]]:
        """Unified search entry.

        Args:
            query: Search query string.
            search_type: "keyword" | "semantic" | "hybrid" | "expanded" | "judgment"
            top_k: Max results to return.
            **kwargs: Additional backend-specific params.

        Returns:
            List of result dicts with file_path, title, snippet, score.
        """
        ...

    @abstractmethod
    def index_page(self, page_path: str, content: str | None = None) -> bool:
        """Index (or re-index) a single page incrementally.

        Args:
            page_path: Absolute or relative path to the .md file.
            content: Optional pre-read content to avoid double read.

        Returns:
            True if indexed successfully.
        """
        ...

    @abstractmethod
    def rebuild_index(self) -> dict[str, Any]:
        """Full rebuild of all indexes (whoosh + vector).

        Returns:
            Summary dict with status and counts.
        """
        ...

    @abstractmethod
    def delete_from_index(self, page_path: str) -> bool:
        """Remove a page from all indexes.

        Args:
            page_path: Path to the .md file.

        Returns:
            True if removed (or not present).
        """
        ...

    @abstractmethod
    def health(self) -> dict[str, Any]:
        """Return backend health/status info."""
        ...


class FileSystemSearchImpl(SearchInterface):
    """File-system backed search using whoosh + numpy vectors."""

    def __init__(self, wiki_root: str) -> None:
        self.wiki_root = Path(wiki_root)
        self._whoosh_ok: bool | None = None
        self._vector_ok: bool | None = None

    def _check_backends(self) -> None:
        """Lazy-check which backends are available."""
        if self._whoosh_ok is not None:
            return
        try:
            import search_backend as sb

            self._whoosh_ok = sb.WHOOSH_AVAILABLE
        except Exception:
            self._whoosh_ok = False
        try:
            import vector_index as vi

            _ = vi._EMBEDDING_DIM
            self._vector_ok = True
        except Exception:
            self._vector_ok = False

    # ── Search ──

    def search(self, query: str, search_type: str = "hybrid", top_k: int = 10, **kwargs: Any) -> list[dict[str, Any]]:
        self._check_backends()

        if search_type == "keyword":
            return self._search_keyword(query, top_k)
        if search_type == "semantic":
            return self._search_semantic(query, top_k)
        if search_type == "hybrid":
            return self._search_hybrid(query, top_k)
        if search_type == "expanded":
            llm_func = kwargs.get("llm_func")
            return self._search_expanded(query, top_k, llm_func)
        if search_type == "judgment":
            return self._search_judgment(query, top_k)

        logger.warning("Unknown search_type '%s', falling back to hybrid", search_type)
        return self._search_hybrid(query, top_k)

    def _search_keyword(self, query: str, top_k: int) -> list[dict[str, Any]]:
        import search_backend as sb

        return sb.search_index(str(self.wiki_root), query, limit=top_k)

    def _search_semantic(self, query: str, top_k: int) -> list[dict[str, Any]]:
        import vector_index as vi

        return vi.search_semantic(str(self.wiki_root), query, top_k=top_k)

    def _search_hybrid(self, query: str, top_k: int) -> list[dict[str, Any]]:
        import vector_index as vi

        return vi.search_hybrid(str(self.wiki_root), query, top_k=top_k)

    def _search_expanded(self, query: str, top_k: int, llm_func: Any) -> list[dict[str, Any]]:
        import search_backend as sb

        return sb.search_wiki(str(self.wiki_root), query, search_type="expanded", limit=top_k, llm_func=llm_func)["results"]

    def _search_judgment(self, query: str, top_k: int) -> list[dict[str, Any]]:
        import search_backend as sb

        result = sb.search_wiki(str(self.wiki_root), query, search_type="judgment", limit=top_k)
        return result.get("results", [])

    # ── Index management ──

    def index_page(self, page_path: str, content: str | None = None) -> bool:
        self._check_backends()
        rel = self._to_rel(page_path)
        if rel is None:
            return False

        ok_whoosh = False
        ok_vector = False

        if self._whoosh_ok:
            import search_backend as sb

            try:
                ok_whoosh = sb.index_page(str(self.wiki_root), rel)
            except Exception as exc:
                logger.warning("Whoosh index_page failed: %s", exc)

        if self._vector_ok:
            import vector_index as vi

            try:
                ok_vector = vi.index_page(str(self.wiki_root), rel)
            except Exception as exc:
                logger.warning("Vector index_page failed: %s", exc)

        return ok_whoosh or ok_vector

    def rebuild_index(self) -> dict[str, Any]:
        self._check_backends()
        summary: dict[str, Any] = {"status": "done", "whoosh": None, "vector": None}

        if self._whoosh_ok:
            import search_backend as sb

            try:
                summary["whoosh"] = sb.rebuild_index(str(self.wiki_root))
            except Exception as exc:
                logger.warning("Whoosh rebuild failed: %s", exc)
                summary["whoosh"] = {"status": "error", "error": str(exc)}

        if self._vector_ok:
            import vector_index as vi

            try:
                summary["vector"] = vi.build_vector_index(str(self.wiki_root))
            except Exception as exc:
                logger.warning("Vector rebuild failed: %s", exc)
                summary["vector"] = {"status": "error", "error": str(exc)}

        return summary

    def delete_from_index(self, page_path: str) -> bool:
        self._check_backends()
        rel = self._to_rel(page_path)
        if rel is None:
            return False

        # Whoosh: update_document with empty body effectively removes
        if self._whoosh_ok:
            import search_backend as sb

            try:
                idx = sb.init_index(str(self.wiki_root))
                if idx is not None:
                    writer = idx.writer()
                    writer.delete_by_term("path", rel)
                    writer.commit()
            except Exception as exc:
                logger.warning("Whoosh delete failed: %s", exc)

        # Vector: load matrix, filter out, save
        if self._vector_ok:
            import vector_index as vi

            try:
                index_dir = vi._get_index_dir(str(self.wiki_root))
                emb_path = index_dir / "embeddings.npy"
                docs_path = index_dir / "docs.json"
                if emb_path.exists() and docs_path.exists():
                    import json
                    import numpy as np

                    matrix = np.load(emb_path).astype(np.float32)
                    docs: list[dict[str, str]] = json.loads(docs_path.read_text(encoding="utf-8"))
                    keep_idx = [i for i, d in enumerate(docs) if d["path"] != rel]
                    if len(keep_idx) != len(docs):
                        matrix = matrix[keep_idx]
                        docs = [docs[i] for i in keep_idx]
                        np.save(emb_path, matrix)
                        docs_path.write_text(json.dumps(docs, ensure_ascii=False), encoding="utf-8")
            except Exception as exc:
                logger.warning("Vector delete failed: %s", exc)

        return True

    def health(self) -> dict[str, Any]:
        self._check_backends()
        return {
            "backend": "filesystem",
            "whoosh_available": self._whoosh_ok,
            "vector_available": self._vector_ok,
            "wiki_root": str(self.wiki_root),
        }

    # ── Helpers ──

    def _to_rel(self, page_path: str) -> str | None:
        """Convert absolute or relative path to wiki-relative path."""
        p = Path(page_path)
        try:
            return str(p.relative_to(self.wiki_root))
        except ValueError:
            # Already relative or outside wiki
            if p.is_absolute():
                return None
            return str(p).replace("\\", "/")


def get_search_impl(wiki_root: str, backend: str | None = None) -> SearchInterface:
    """Factory for search implementations.

    Args:
        wiki_root: Path to wiki root.
        backend: "filesystem" (default) or "seekdb" (Phase 11).
            If None, reads from WIKI_BACKEND env var.
    """
    import os

    if backend is None:
        backend = os.environ.get("WIKI_BACKEND", "filesystem")
    if backend == "filesystem":
        return FileSystemSearchImpl(wiki_root)
    if backend == "seekdb":
        from seekdb_search_impl import SeekDBSearchImpl
        return SeekDBSearchImpl(wiki_root)
    raise ValueError(f"Unknown search backend: {backend}")


__all__ = [
    "SearchInterface",
    "FileSystemSearchImpl",
    "get_search_impl",
]
