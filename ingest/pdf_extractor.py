"""ROSClaw PDF Extractor — full-text extraction with section detection.

**Phase 6 Trust-First Architecture:**
- Complex documents (images, tables, formulas) → PaddleOCR API ONLY.
- Pure-text papers → PyMuPDF fast path.
- NO local downgrade for complex content.
"""

from __future__ import annotations

import logging
import os
import re
from pathlib import Path
from typing import Any

import paddleocr_client as paddleocr

logger = logging.getLogger("rosclaw.pdf")

# PyMuPDF for fast pure-text extraction and complexity detection
try:
    import fitz  # PyMuPDF
except ImportError:
    fitz = None  # type: ignore[misc, assignment]

# Optional PaddleOCR API for layout-aware extraction (v2 async API)
_PADDLEOCR_API_URL = os.environ.get(
    "PADDLEOCR_API_URL",
    "https://paddleocr.aistudio-app.com/api/v2/ocr/jobs",
)
_PADDLEOCR_API_TOKEN = os.environ.get("PADDLEOCR_API_TOKEN", "")

# Common section headers in academic papers (case-insensitive)
_ROMAN_NUM = r"[IVXivx]+"


def _make_section_pattern(keyword_alternatives: str) -> re.Pattern:
    return re.compile(
        rf"(?:#+\s+)?\b({_ROMAN_NUM}|\d+)?\s*\.?\s*({keyword_alternatives})\b",
        re.I,
    )


_SECTION_PATTERNS: list[tuple[str, re.Pattern]] = [
    ("abstract", _make_section_pattern("abstract|summary")),
    ("introduction", _make_section_pattern("introduction")),
    ("methods", _make_section_pattern("methods?|methodology|approach|model|architecture")),
    ("experiments", _make_section_pattern(r"experiments?(?:\s+&\s+discussion)?|experimental|evaluation|results?|empirical")),
    ("conclusion", _make_section_pattern("conclusions?|discussion|future work")),
    ("references", _make_section_pattern("references?|bibliography")),
]


def _clean_text(text: str) -> str:
    """Clean extracted text: merge broken lines, remove excessive whitespace."""
    # Remove isolated page numbers
    text = re.sub(r"^\s*\d+\s*$", "", text, flags=re.M)

    lines = text.splitlines()
    deduped: list[str] = []
    seen_short: set[str] = set()
    for line in lines:
        stripped = line.strip()
        if not stripped:
            deduped.append("")
            continue
        if re.match(r"^\d+$", stripped):
            continue
        if len(stripped) < 30:
            if stripped in seen_short:
                continue
            seen_short.add(stripped)
        deduped.append(stripped)

    # Merge hyphenated line breaks
    merged = []
    for i, line in enumerate(deduped):
        if line.endswith("-") and i + 1 < len(deduped):
            merged.append(line[:-1] + deduped[i + 1])
            deduped[i + 1] = ""
        else:
            merged.append(line)

    # Rejoin with proper paragraph breaks
    result_lines: list[str] = []
    para_buffer: list[str] = []
    for line in merged:
        if not line.strip():
            if para_buffer:
                result_lines.append(" ".join(para_buffer))
                para_buffer = []
            result_lines.append("")
        else:
            para_buffer.append(line.strip())
    if para_buffer:
        result_lines.append(" ".join(para_buffer))

    return "\n".join(result_lines).strip()


def _detect_sections(text: str) -> dict[str, str]:
    """Detect standard sections in academic paper text."""
    raw_matches: list[tuple[str, int, str]] = []
    for section_name, pattern in _SECTION_PATTERNS:
        for m in pattern.finditer(text):
            raw_matches.append((section_name, m.start(), m.group(0)))

    section_positions: list[tuple[str, int]] = []
    for name, pos, matched_text in raw_matches:
        core_word = matched_text.strip().split()[-1] if matched_text.strip() else ""
        preceded_by_break = pos == 0 or text[pos - 1] == "\n"
        is_all_caps = core_word.isupper() and len(core_word) > 2
        has_roman_prefix = pos >= 4 and re.search(r"[IVX]+\.\s*$", text[max(0, pos - 10):pos])
        if preceded_by_break or is_all_caps or has_roman_prefix:
            section_positions.append((name, pos))

    section_positions.sort(key=lambda x: x[1])

    deduped: list[tuple[str, int]] = []
    seen_pos: set[int] = set()
    for name, pos in section_positions:
        if pos in seen_pos:
            continue
        too_close = any(abs(pos - kept_pos) < 30 for _, kept_pos in deduped)
        if too_close:
            continue
        deduped.append((name, pos))
        seen_pos.add(pos)
    section_positions = deduped

    sections: dict[str, str] = {}
    for idx, (name, start_pos) in enumerate(section_positions):
        end_pos = section_positions[idx + 1][1] if idx + 1 < len(section_positions) else len(text)
        content = text[start_pos:end_pos].strip()
        first_newline = content.find("\n")
        if first_newline != -1 and first_newline < 200:
            content = content[first_newline + 1:].strip()
        elif first_newline != -1:
            header_end = 0
            for _pattern in _SECTION_PATTERNS:
                if _pattern[0] == name:
                    m = _pattern[1].search(content)
                    if m:
                        header_end = m.end()
                    break
            content = content[header_end:].strip()
        else:
            header_end = 0
            for _pattern in _SECTION_PATTERNS:
                if _pattern[0] == name:
                    m = _pattern[1].search(content)
                    if m:
                        header_end = m.end()
                    break
            content = content[header_end:].strip()
        if name in sections:
            sections[name] = sections[name] + "\n\n" + content
        else:
            sections[name] = content

    return sections


def _is_complex_pdf(pdf_path: str) -> bool:
    """Detect whether a PDF contains images, tables, or formulas.

    A PDF is considered "complex" if any page contains:
    - Embedded images (via page.get_images())
    - Dense table-like text blocks (many pipe characters or tabular layout)

    Complex documents MUST be processed by PaddleOCR API.
    """
    if fitz is None:
        # Without PyMuPDF we cannot inspect the PDF; treat as complex to be safe.
        return True

    doc = fitz.open(pdf_path)
    try:
        for page in doc:
            # Check for embedded images
            if page.get_images():
                return True

            # Check for table-like structures in text blocks
            blocks = page.get_text("blocks")
            for b in blocks:
                text = b[4] if len(b) > 4 else ""
                # Heuristic: many pipe chars suggest markdown tables
                pipe_count = text.count("|")
                if pipe_count >= 4:
                    return True
                # Heuristic: dense numeric/tabular lines
                lines = text.splitlines()
                table_like_lines = 0
                for line in lines:
                    cells = [c.strip() for c in line.split("|") if c.strip()]
                    if len(cells) >= 3:
                        table_like_lines += 1
                if table_like_lines >= 2:
                    return True
        return False
    finally:
        doc.close()


def _extract_with_pymupdf(pdf_path: str) -> str:
    """Extract text using PyMuPDF (pure-text fast path only)."""
    if fitz is None:
        raise RuntimeError("PyMuPDF not installed")
    doc = fitz.open(pdf_path)
    pages: list[str] = []
    for page in doc:
        text = page.get_text()
        pages.append(text)
    doc.close()
    return "\n".join(pages)


def extract_pdf_text(pdf_path: str) -> str:
    """Extract full text from a PDF file.

    **Phase 6 Trust-First Logic:**
    1. Detect if PDF is complex (images / tables / formulas).
    2. Complex PDF → PaddleOCR API ONLY. No local downgrade.
    3. Simple text PDF → PyMuPDF fast path.

    Args:
        pdf_path: Path to the PDF file.

    Returns:
        Cleaned plain text of the entire PDF.

    Raises:
        FileNotFoundError: If PDF does not exist.
        RuntimeError: If extraction fails or PaddleOCR API is required but unavailable.
    """
    path = Path(pdf_path)
    if not path.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    is_complex = _is_complex_pdf(pdf_path)
    file_size_mb = path.stat().st_size / (1024 * 1024)

    if is_complex:
        # Complex documents MUST use PaddleOCR API — no local downgrade.
        if not paddleocr.is_available():
            raise RuntimeError(
                f"Complex PDF '{path.name}' requires PaddleOCR API, "
                "but it is not available. Set PADDLEOCR_API_TOKEN."
            )

        if file_size_mb > 20:
            raw_text = paddleocr.extract_pdf_chunked(
                str(pdf_path),
                api_url=_PADDLEOCR_API_URL,
                api_token=_PADDLEOCR_API_TOKEN,
            )
        else:
            raw_text = paddleocr.extract_pdf(
                str(pdf_path),
                api_url=_PADDLEOCR_API_URL,
                api_token=_PADDLEOCR_API_TOKEN,
            )
        logger.info("Content extracted via PaddleOCR: %s", path.name)
        return _clean_text(raw_text)

    # Pure-text fast path
    raw_text = _extract_with_pymupdf(pdf_path)
    logger.info("Content extracted via PyMuPDF (pure-text fast path): %s", path.name)
    return _clean_text(raw_text)


def extract_pdf_sections(pdf_path: str) -> dict[str, Any]:
    """Extract PDF text with section detection.

    Returns:
        Dict with keys: abstract, introduction, methods, experiments,
        conclusion, references, full_text.
    """
    full_text = extract_pdf_text(pdf_path)
    sections = _detect_sections(full_text)

    result: dict[str, Any] = {
        "abstract": sections.get("abstract", ""),
        "introduction": sections.get("introduction", ""),
        "methods": sections.get("methods", ""),
        "experiments": sections.get("experiments", ""),
        "conclusion": sections.get("conclusion", ""),
        "references": sections.get("references", ""),
        "full_text": full_text,
    }

    found = [k for k, v in result.items() if v and k != "full_text"]
    logger.info("PDF %s: found sections: %s", Path(pdf_path).name, ", ".join(found) or "none")

    return result


def is_api_extractor_available() -> bool:
    """Return True if PaddleOCR API is configured."""
    return paddleocr.is_available()


def is_extractor_available() -> bool:
    """Return True if any PDF extraction backend is available.

    For complex PDFs, only PaddleOCR API counts as available.
    For simple text PDFs, PyMuPDF is sufficient.
    """
    return paddleocr.is_available() or fitz is not None
