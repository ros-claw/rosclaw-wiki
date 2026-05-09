"""Export for SeekDB — standardized JSONL export for Phase 11 migration.

Exports all wiki pages into a flat JSONL format ready for SeekDB ingestion.
"""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any

import wiki_engine as engine

logger = logging.getLogger("rosclaw.seekdb_export")


def _load_vector_for_page(page_path: str, wiki_root: str) -> list[float] | None:
    """Load the vector embedding for a page from the numpy index."""
    try:
        import numpy as np
        from vector_index import _get_index_dir

        index_dir = _get_index_dir(wiki_root)
        emb_path = index_dir / "embeddings.npy"
        docs_path = index_dir / "docs.json"
        if not emb_path.exists() or not docs_path.exists():
            return None

        rel = str(Path(page_path).relative_to(wiki_root))
        docs: list[dict[str, str]] = json.loads(docs_path.read_text(encoding="utf-8"))
        matrix = np.load(emb_path).astype(np.float32)

        for i, doc in enumerate(docs):
            if doc["path"] == rel:
                return [round(float(x), 6) for x in matrix[i].tolist()]
    except Exception as exc:
        logger.debug("Vector load failed for %s: %s", page_path, exc)
    return None


def _extract_wikilinks(body: str) -> list[str]:
    """Extract all [[Target]] wikilinks from body."""
    import re

    return [m.group(1).split("|")[0].strip() for m in re.finditer(r"\[\[([^\]]+)\]\]", body)]


def _load_judgments(wiki_root: str) -> list[dict[str, Any]]:
    """Load all judgments for embedding in page records."""
    try:
        from judgment_generator import list_judgments

        result = list_judgments(wiki_root=wiki_root)
        return result.get("judgments", [])
    except Exception:
        return []


def export_pages(wiki_root: str, output_path: str | None = None) -> dict[str, Any]:
    """Export all wiki pages to standardized JSONL.

    Args:
        wiki_root: Path to wiki root.
        output_path: Output file path. Defaults to data/seekdb_import.jsonl.

    Returns:
        Summary dict with exported_count, output_path.
    """
    root = Path(wiki_root)
    if output_path is None:
        output_path = "data/seekdb_import.jsonl"

    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)

    all_judgments = _load_judgments(wiki_root)
    exported = 0

    with out.open("w", encoding="utf-8") as f:
        for md_file in root.rglob("*.md"):
            if md_file.name in ("index.md", "log.md", "Admin_Dashboard.md"):
                continue
            try:
                content = md_file.read_text(encoding="utf-8")
                meta, body = engine.parse_frontmatter(content)
            except Exception as exc:
                logger.warning("Skip %s: %s", md_file, exc)
                continue

            rel = str(md_file.relative_to(root))
            vector = _load_vector_for_page(str(md_file), wiki_root)
            wikilinks = _extract_wikilinks(body)

            # Find judgments related to this page
            page_judgments = [
                j for j in all_judgments
                if j.get("entity") == meta.get("title", md_file.stem)
                or j.get("entity") == md_file.stem
            ]

            record = {
                "id": meta.get("id", md_file.stem),
                "type": meta.get("type", "episode"),
                "title": meta.get("title", md_file.stem),
                "body": body,
                "tags": meta.get("tags", []),
                "confidence": meta.get("confidence", 0.5),
                "created_at": meta.get("created_at", ""),
                "last_reinforced": meta.get("last_reinforced", ""),
                "sources": meta.get("sources", []),
                "vector": vector,
                "wikilinks": wikilinks,
                "judgments": page_judgments,
                "file_path": rel,
            }

            f.write(json.dumps(record, ensure_ascii=False) + "\n")
            exported += 1

    logger.info("SeekDB export: %d pages to %s", exported, out)
    return {"exported_count": exported, "output_path": str(out)}


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser(description="Export wiki to SeekDB JSONL")
    parser.add_argument("--wiki-root", default="wiki", help="Wiki root directory")
    parser.add_argument("--output", default="data/seekdb_import.jsonl", help="Output JSONL file")
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO)
    result = export_pages(args.wiki_root, args.output)
    print(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


__all__ = ["export_pages"]
