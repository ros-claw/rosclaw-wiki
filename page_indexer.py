"""Page Indexer — tree-structured chapter index for long PDFs (Phase 10).

Builds a hierarchical index for PDFs >20 pages, enabling chapter-level
selective reading by LLMs.
"""

from __future__ import annotations

import json
import logging
import re
from pathlib import Path
from typing import Any

try:
    import fitz  # PyMuPDF
except ImportError:
    fitz = None  # type: ignore[misc, assignment]

logger = logging.getLogger("rosclaw.page_indexer")

# Common academic section header patterns
_SECTION_RE = re.compile(
    r"^(?:\d+(?:\.\d+)*\s+)?"
    r"(Abstract|Introduction|Related Work|Background|Methods?|Methodology|"
    r"Approach|Model|Architecture|Experiments?|Experimental|Evaluation|"
    r"Results?|Empirical|Analysis|Discussion|Conclusions?|Future Work|"
    r"References?|Bibliography|Appendix|Acknowledgments?)"
    r"\s*$",
    re.IGNORECASE,
)


def _extract_toc_from_bookmarks(pdf_path: str) -> list[dict[str, Any]]:
    """Extract TOC from PDF embedded bookmarks."""
    if fitz is None:
        return []
    doc = fitz.open(pdf_path)
    try:
        toc = doc.get_toc()
        result: list[dict[str, Any]] = []
        for item in toc:
            level, title, page = item
            result.append({
                "level": level,
                "title": title.strip(),
                "page": page,
                "type": "bookmark",
            })
        return result
    finally:
        doc.close()


def _extract_toc_from_text(pdf_path: str) -> list[dict[str, Any]]:
    """Extract TOC by scanning page text for section headers."""
    if fitz is None:
        return []
    doc = fitz.open(pdf_path)
    try:
        sections: list[dict[str, Any]] = []
        for page_num in range(len(doc)):
            text = doc[page_num].get_text()
            for line in text.splitlines():
                line_stripped = line.strip()
                if _SECTION_RE.match(line_stripped):
                    sections.append({
                        "level": 1,
                        "title": line_stripped,
                        "page": page_num + 1,
                        "type": "heuristic",
                    })
        # Deduplicate adjacent identical titles
        deduped: list[dict[str, Any]] = []
        for s in sections:
            if deduped and deduped[-1]["title"] == s["title"]:
                continue
            deduped.append(s)
        return deduped
    finally:
        doc.close()


def build_page_index(pdf_path: str, output_path: str | None = None) -> dict[str, Any]:
    """Build a tree-structured page index for a PDF.

    Args:
        pdf_path: Path to the PDF file.
        output_path: Optional path to write JSON output.

    Returns:
        Dict with chapters, page_count, source.
    """
    if fitz is None:
        raise RuntimeError("PyMuPDF not installed")

    doc = fitz.open(pdf_path)
    total_pages = len(doc)
    doc.close()

    # Try bookmarks first, fall back to text heuristics
    chapters = _extract_toc_from_bookmarks(pdf_path)
    source = "bookmark"
    if not chapters:
        chapters = _extract_toc_from_text(pdf_path)
        source = "heuristic"

    # Add page ranges
    for i, ch in enumerate(chapters):
        if i + 1 < len(chapters):
            ch["end_page"] = chapters[i + 1]["page"] - 1
        else:
            ch["end_page"] = total_pages
        ch["page_count"] = ch["end_page"] - ch["page"] + 1

    result = {
        "source": source,
        "total_pages": total_pages,
        "chapter_count": len(chapters),
        "chapters": chapters,
        "pdf_path": pdf_path,
    }

    if output_path:
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        Path(output_path).write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
        logger.info("Page index saved: %s (%d chapters)", output_path, len(chapters))

    return result


def extract_chapter_text(pdf_path: str, start_page: int, end_page: int) -> str:
    """Extract text from a specific page range.

    Args:
        pdf_path: Path to PDF.
        start_page: 1-indexed start page.
        end_page: 1-indexed end page (inclusive).

    Returns:
        Extracted text.
    """
    if fitz is None:
        raise RuntimeError("PyMuPDF not installed")

    doc = fitz.open(pdf_path)
    try:
        parts: list[str] = []
        for i in range(start_page - 1, min(end_page, len(doc))):
            parts.append(doc[i].get_text())
        return "\n".join(parts)
    finally:
        doc.close()


def should_index(pdf_path: str, min_pages: int = 20) -> bool:
    """Check if a PDF should get a PageIndex (long enough)."""
    if fitz is None:
        return False
    try:
        doc = fitz.open(pdf_path)
        pages = len(doc)
        doc.close()
        return pages >= min_pages
    except Exception:
        return False


__all__ = [
    "build_page_index",
    "extract_chapter_text",
    "should_index",
]
