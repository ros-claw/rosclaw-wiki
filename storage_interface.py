"""Storage Interface Abstraction Layer — unified storage for Phase 10.

Provides StorageInterface protocol with FileSystemStorageImpl.
Phase 11 will add SeekDBStorageImpl without changing upper-layer code.
"""

from __future__ import annotations

import logging
import shutil
from abc import ABC, abstractmethod
from collections.abc import Callable
from datetime import datetime
from pathlib import Path
from typing import Any

import wiki_engine as engine

logger = logging.getLogger("rosclaw.storage_interface")


class StorageInterface(ABC):
    """Abstract storage interface. Upper-layer code must use this, not wiki_engine directly."""

    @abstractmethod
    def read_page(self, page_path: str) -> dict[str, Any]:
        """Read a page and return {meta, body, path}.

        Returns:
            Dict with keys: meta (dict), body (str), path (str).
            Raises FileNotFoundError if page does not exist.
        """
        ...

    @abstractmethod
    def write_page(self, page_path: str, content: str, metadata: dict[str, Any] | None = None) -> bool:
        """Write (or overwrite) a page.

        Args:
            page_path: Target path for the page.
            content: Full markdown content (with or without frontmatter).
            metadata: Optional metadata dict to prepend as frontmatter.

        Returns:
            True if written successfully.
        """
        ...

    @abstractmethod
    def delete_page(self, page_path: str) -> bool:
        """Delete a page.

        Returns:
            True if deleted (or not present).
        """
        ...

    @abstractmethod
    def list_pages(self, directory: str | None = None) -> list[dict[str, Any]]:
        """List all pages, optionally filtered by subdirectory.

        Returns:
            List of dicts with meta + _path for each page.
        """
        ...

    @abstractmethod
    def create_page(self, dir_path: str, title: str, body: str, meta: dict[str, Any]) -> str:
        """Create a new page with auto-generated ID and frontmatter.

        Returns:
            Absolute path to the created page.
        """
        ...

    @abstractmethod
    def update_page(self, path: str, instruction: str, llm_func: Callable[[str, str], str]) -> str:
        """Update a page via LLM-generated edit.

        Returns:
            Updated full page content.
        """
        ...

    @abstractmethod
    def move_to_archive(self, source_path: str) -> str:
        """Move a page to archive and leave a stub.

        Returns:
            Path to the archived file.
        """
        ...

    @abstractmethod
    def update_index(self) -> str:
        """Rebuild wiki/index.md.

        Returns:
            Path to the updated index file.
        """
        ...

    @abstractmethod
    def append_log(self, entry: str) -> str:
        """Append a timestamped entry to wiki/log.md.

        Returns:
            Path to the log file.
        """
        ...


class FileSystemStorageImpl(StorageInterface):
    """File-system backed storage using wiki_engine functions."""

    def __init__(self, wiki_root: str) -> None:
        self.wiki_root = Path(wiki_root)

    # ── CRUD ──

    def read_page(self, page_path: str) -> dict[str, Any]:
        p = Path(page_path)
        if not p.exists():
            raise FileNotFoundError(f"Page not found: {page_path}")
        content = p.read_text(encoding="utf-8")
        meta, body = engine.parse_frontmatter(content)
        return {"meta": meta, "body": body, "path": str(p)}

    def write_page(self, page_path: str, content: str, metadata: dict[str, Any] | None = None) -> bool:
        p = Path(page_path)
        p.parent.mkdir(parents=True, exist_ok=True)
        if metadata is not None:
            content = engine.write_frontmatter(metadata, content)
        p.write_text(content, encoding="utf-8")
        return True

    def delete_page(self, page_path: str) -> bool:
        p = Path(page_path)
        if p.exists():
            p.unlink()
            return True
        return False

    def list_pages(self, directory: str | None = None) -> list[dict[str, Any]]:
        if directory is None:
            directory = str(self.wiki_root)
        root = Path(directory)
        results: list[dict[str, Any]] = []
        for md_file in root.rglob("*.md"):
            if md_file.name in ("index.md", "log.md"):
                continue
            try:
                content = md_file.read_text(encoding="utf-8")
                meta, _ = engine.parse_frontmatter(content)
                meta["_path"] = str(md_file)
                results.append(meta)
            except Exception as exc:
                logger.warning("Failed to read %s: %s", md_file, exc)
        return results

    # ─- wiki_engine delegates ──

    def create_page(self, dir_path: str, title: str, body: str, meta: dict[str, Any]) -> str:
        return engine.create_page(dir_path, title, body, meta)

    def update_page(self, path: str, instruction: str, llm_func: Callable[[str, str], str]) -> str:
        return engine.update_page(path, instruction, llm_func)

    def move_to_archive(self, source_path: str) -> str:
        return engine.move_to_archive(source_path, str(self.wiki_root))

    def update_index(self) -> str:
        return engine.update_index(str(self.wiki_root))

    def append_log(self, entry: str) -> str:
        return engine.append_log(str(self.wiki_root), entry)


def get_storage_impl(wiki_root: str, backend: str | None = None) -> StorageInterface:
    """Factory for storage implementations.

    Args:
        wiki_root: Path to wiki root.
        backend: "filesystem" (default) or "seekdb" (Phase 11).
            If None, reads from WIKI_BACKEND env var.
    """
    import os

    if backend is None:
        backend = os.environ.get("WIKI_BACKEND", "filesystem")
    if backend == "filesystem":
        return FileSystemStorageImpl(wiki_root)
    if backend == "seekdb":
        from seekdb_storage_impl import SeekDBStorageImpl
        return SeekDBStorageImpl(wiki_root)
    raise ValueError(f"Unknown storage backend: {backend}")


__all__ = [
    "StorageInterface",
    "FileSystemStorageImpl",
    "get_storage_impl",
]
