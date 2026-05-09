"""SeekDB Storage Implementation — StorageInterface backed by real pyseekdb.

Uses pyseekdb collections for CRUD operations.
Auth/billing remains in SQLite (seekdb_client.py).
"""
from __future__ import annotations

import json
import logging
from collections.abc import Callable
from pathlib import Path
from typing import Any

import wiki_engine as engine
from storage_interface import StorageInterface

logger = logging.getLogger("rosclaw.seekdb_storage")


class SeekDBStorageImpl(StorageInterface):
    """SeekDB-backed storage using pyseekdb collections."""

    def __init__(self, wiki_root: str = "wiki") -> None:
        self.wiki_root = Path(wiki_root)

    def _wiki_collection(self):
        from seekdb_collection_client import get_wiki_collection
        return get_wiki_collection()

    # ── CRUD ──

    def read_page(self, page_path: str) -> dict[str, Any]:
        page_id = Path(page_path).stem
        coll = self._wiki_collection()
        try:
            results = coll.get(
                ids=[page_id],
                include=["documents", "metadatas"],
            )
        except Exception as exc:
            raise FileNotFoundError(f"Page not found: {page_path}") from exc

        ids = results.get("ids", [])
        if not ids:
            raise FileNotFoundError(f"Page not found: {page_path}")

        meta = results.get("metadatas", [{}])[0] if results.get("metadatas") else {}
        body = results.get("documents", [""])[0] if results.get("documents") else ""

        return {
            "meta": {
                "id": page_id,
                "type": meta.get("type", "episode"),
                "title": meta.get("title", page_id),
                "tags": meta.get("tags", "").split(",") if meta.get("tags") else [],
                "confidence": meta.get("confidence", 0.5),
                "created_at": meta.get("created_at", ""),
                "last_reinforced": meta.get("last_reinforced", ""),
                "sources": json.loads(meta.get("sources", "[]")) if meta.get("sources") else [],
            },
            "body": body or "",
            "path": page_path,
        }

    def write_page(self, page_path: str, content: str, metadata: dict[str, Any] | None = None) -> bool:
        page_id = Path(page_path).stem
        if metadata is not None:
            body = content
        else:
            meta, body = engine.parse_frontmatter(content)
            metadata = meta

        title = metadata.get("title", page_id)
        page_type = metadata.get("type", "episode")
        tags = ",".join(metadata.get("tags", []))
        confidence = metadata.get("confidence", 0.5)
        created_at = metadata.get("created_at", "")
        last_reinforced = metadata.get("last_reinforced", "")
        sources = json.dumps(metadata.get("sources", []), ensure_ascii=False)

        coll = self._wiki_collection()
        try:
            coll.upsert(
                ids=[page_id],
                documents=[body],
                metadatas=[{
                    "type": page_type,
                    "title": title,
                    "tags": tags,
                    "confidence": confidence,
                    "created_at": created_at,
                    "last_reinforced": last_reinforced,
                    "sources": sources,
                }],
            )
            return True
        except Exception as exc:
            logger.warning("Write page error for %s: %s", page_id, exc)
            return False

    def delete_page(self, page_path: str) -> bool:
        page_id = Path(page_path).stem
        coll = self._wiki_collection()
        try:
            coll.delete(ids=[page_id])
            return True
        except Exception as exc:
            logger.warning("Delete page error for %s: %s", page_id, exc)
            return False

    def list_pages(self, directory: str | None = None) -> list[dict[str, Any]]:
        coll = self._wiki_collection()
        try:
            results = coll.get(
                limit=10000,
                include=["metadatas"],
            )
        except Exception as exc:
            logger.warning("List pages error: %s", exc)
            return []

        ids = results.get("ids", [])
        metadatas = results.get("metadatas", [])

        if ids and isinstance(ids[0], list):
            ids = ids[0]
            metadatas = metadatas[0] if metadatas else []

        results_list = []
        for i, doc_id in enumerate(ids):
            meta = metadatas[i] if i < len(metadatas) else {}
            results_list.append({
                "id": doc_id,
                "type": meta.get("type", "episode"),
                "title": meta.get("title", doc_id),
                "tags": meta.get("tags", "").split(",") if meta.get("tags") else [],
                "confidence": meta.get("confidence", 0.5),
                "created_at": meta.get("created_at", ""),
                "last_reinforced": meta.get("last_reinforced", ""),
                "sources": json.loads(meta.get("sources", "[]")) if meta.get("sources") else [],
                "_path": str(self.wiki_root / f"{doc_id}.md"),
            })
        return results_list

    def create_page(self, dir_path: str, title: str, body: str, meta: dict[str, Any]) -> str:
        path = engine.create_page(dir_path, title, body, meta)
        self.index_page(path)
        return path

    def update_page(self, path: str, instruction: str, llm_func: Callable[[str, str], str]) -> str:
        return engine.update_page(path, instruction, llm_func)

    def move_to_archive(self, source_path: str) -> str:
        return engine.move_to_archive(source_path, str(self.wiki_root))

    def update_index(self) -> str:
        return engine.update_index(str(self.wiki_root))

    def append_log(self, entry: str) -> str:
        return engine.append_log(str(self.wiki_root), entry)

    def index_page(self, page_path: str) -> bool:
        from seekdb_search_impl import SeekDBSearchImpl
        search = SeekDBSearchImpl(str(self.wiki_root))
        return search.index_page(page_path)


__all__ = ["SeekDBStorageImpl"]
