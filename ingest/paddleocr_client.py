"""PaddleOCR API Client — layout-aware PDF extraction (v2 async API).

Encapsulates the PaddleOCR-VL v2 async API with:
  - Job submission (local file multipart upload)
  - Polling until completion
  - JSONL result download and markdown text extraction

Reference: paddleOCR_test.py (PaddleOCR-VL v2 API)
"""

from __future__ import annotations

import json
import logging
import os
import time
from pathlib import Path
from typing import Any

try:
    import requests
except ImportError:
    requests = None  # type: ignore[assignment]

try:
    import fitz  # PyMuPDF — required for chunked extraction
except ImportError:
    fitz = None  # type: ignore[misc, assignment]

logger = logging.getLogger("rosclaw.paddleocr")

def _load_env_file() -> None:
    """Manually load key=value pairs from .env file without external deps."""
    # Search for .env in current file's directory and parents
    current = Path(__file__).resolve().parent
    for path in [current / ".env", current.parent / ".env"]:
        if path.exists():
            try:
                with open(path, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if not line or line.startswith("#"):
                            continue
                        if "=" in line:
                            key, val = line.split("=", 1)
                            key = key.strip()
                            val = val.strip().strip('"').strip("'")
                            if key not in os.environ:
                                os.environ[key] = val
            except Exception:
                pass
            break


_load_env_file()

DEFAULT_API_URL = os.environ.get(
    "PADDLEOCR_API_URL",
    "https://paddleocr.aistudio-app.com/api/v2/ocr/jobs",
)
DEFAULT_API_TOKEN = os.environ.get("PADDLEOCR_API_TOKEN", "")
DEFAULT_MODEL = os.environ.get("PADDLEOCR_MODEL", "PaddleOCR-VL")
_POLL_INTERVAL = 5  # seconds


def is_available() -> bool:
    """Return True if the client is usable (requests installed + API token set)."""
    return requests is not None and bool(os.environ.get("PADDLEOCR_API_TOKEN", ""))


def _submit_job(
    pdf_path: str,
    api_url: str,
    api_token: str,
    use_chart: bool = False,
) -> str:
    """Submit a PDF to the PaddleOCR v2 API and return jobId.

    Uses multipart/form-data upload for local files.
    """
    if requests is None:
        raise RuntimeError("requests library not installed")

    headers = {"Authorization": f"bearer {api_token}"}
    optional_payload = {
        "useDocOrientationClassify": False,
        "useDocUnwarping": False,
        "useChartRecognition": use_chart,
    }

    path = Path(pdf_path)
    if not path.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    with open(path, "rb") as f:
        data = {
            "model": DEFAULT_MODEL,
            "optionalPayload": json.dumps(optional_payload),
        }
        files = {"file": (path.name, f, "application/pdf")}
        resp = requests.post(api_url, headers=headers, data=data, files=files)

    if resp.status_code != 200:
        raise RuntimeError(
            f"PaddleOCR API submit failed: {resp.status_code} - {resp.text[:200]}"
        )

    resp_data = resp.json()
    job_id = resp_data.get("data", {}).get("jobId")
    if not job_id:
        raise RuntimeError(f"PaddleOCR API did not return jobId: {resp_data}")

    logger.info("PaddleOCR job submitted: %s (jobId=%s)", path.name, job_id)
    return job_id


def _poll_job(
    job_id: str,
    api_url: str,
    api_token: str,
    timeout: int = 300,
) -> str:
    """Poll a job until completion and return the JSONL result URL.

    Args:
        job_id: The job ID returned by _submit_job.
        api_url: Base API URL.
        api_token: API bearer token.
        timeout: Maximum total polling time in seconds.

    Returns:
        URL to the JSONL result file.

    Raises:
        RuntimeError: If the job fails or times out.
    """
    if requests is None:
        raise RuntimeError("requests library not installed")

    url = f"{api_url.rstrip('/')}/{job_id}"
    headers = {"Authorization": f"bearer {api_token}"}

    start_time = time.time()
    while True:
        elapsed = time.time() - start_time
        if elapsed > timeout:
            raise RuntimeError(
                f"PaddleOCR job {job_id} timed out after {timeout}s"
            )

        resp = requests.get(url, headers=headers)
        resp.raise_for_status()
        resp_data = resp.json()
        data = resp_data.get("data", {})

        state = data.get("state", "unknown")
        if state == "pending":
            logger.debug("PaddleOCR job %s pending... (elapsed %.0fs)", job_id, elapsed)
        elif state == "running":
            progress = data.get("extractProgress", {})
            total = progress.get("totalPages", "?")
            extracted = progress.get("extractedPages", "?")
            logger.info(
                "PaddleOCR job %s running: %s/%s pages (elapsed %.0fs)",
                job_id, extracted, total, elapsed,
            )
        elif state == "done":
            progress = data.get("extractProgress", {})
            extracted = progress.get("extractedPages", "?")
            logger.info(
                "PaddleOCR job %s done: %s pages extracted (total %.0fs)",
                job_id, extracted, elapsed,
            )
            result_url = data.get("resultUrl", {})
            jsonl_url = result_url.get("jsonUrl")
            if not jsonl_url:
                raise RuntimeError(f"PaddleOCR job {job_id} done but no jsonUrl")
            return jsonl_url
        elif state == "failed":
            error_msg = data.get("errorMsg", "Unknown error")
            raise RuntimeError(f"PaddleOCR job {job_id} failed: {error_msg}")
        else:
            logger.warning("PaddleOCR job %s unknown state: %s", job_id, state)

        time.sleep(_POLL_INTERVAL)


def _download_and_parse(jsonl_url: str) -> str:
    """Download JSONL results and extract markdown text.

    Args:
        jsonl_url: URL to the JSONL result file.

    Returns:
        Concatenated markdown text from all pages.

    Raises:
        RuntimeError: If no text could be extracted.
    """
    if requests is None:
        raise RuntimeError("requests library not installed")

    resp = requests.get(jsonl_url)
    resp.raise_for_status()

    lines = resp.text.strip().split("\n")
    parts: list[str] = []

    for line in lines:
        line = line.strip()
        if not line:
            continue
        try:
            result = json.loads(line)["result"]
            for res in result.get("layoutParsingResults", []):
                md_text = res.get("markdown", {}).get("text", "")
                if md_text:
                    parts.append(md_text)
        except (json.JSONDecodeError, KeyError) as exc:
            logger.warning("Failed to parse JSONL line: %s", exc)
            continue

    if not parts:
        raise RuntimeError("PaddleOCR API returned no text")

    return "\n\n".join(parts)


def extract_pdf(
    pdf_path: str,
    *,
    api_url: str | None = None,
    api_token: str | None = None,
    timeout: int = 300,
    use_chart: bool = False,
) -> str:
    """Extract text from a PDF using the PaddleOCR v2 async API.

    Args:
        pdf_path: Path to the PDF file.
        api_url: Override the API endpoint. Defaults to env PADDLEOCR_API_URL.
        api_token: Override the API token. Defaults to env PADDLEOCR_API_TOKEN.
        timeout: Maximum total time (submit + poll) in seconds.
        use_chart: Enable chart recognition mode.

    Returns:
        Extracted markdown text.

    Raises:
        RuntimeError: If requests is not installed, token is missing, or API fails.
    """
    url = api_url or DEFAULT_API_URL
    token = api_token or DEFAULT_API_TOKEN
    if not token:
        raise RuntimeError("PaddleOCR API token not configured. Set PADDLEOCR_API_TOKEN.")

    job_id = _submit_job(pdf_path, url, token, use_chart=use_chart)
    jsonl_url = _poll_job(job_id, url, token, timeout=timeout)
    text = _download_and_parse(jsonl_url)
    logger.info("Content extracted via PaddleOCR v2: %s", Path(pdf_path).name)
    return text


def extract_pdf_chunked(
    pdf_path: str,
    *,
    pages_per_chunk: int = 10,
    api_url: str | None = None,
    api_token: str | None = None,
    timeout: int = 300,
    use_chart: bool = False,
) -> str:
    """Extract text from a large PDF using chunked PaddleOCR v2 API uploads.

    Splits the PDF into chunks of ``pages_per_chunk`` pages, submits each
    chunk as a separate job, polls until completion, and concatenates the
    markdown results.

    Args:
        pdf_path: Path to the PDF file.
        pages_per_chunk: Number of pages per chunk.
        api_url: Override the API endpoint.
        api_token: Override the API token.
        timeout: Total timeout shared across all chunks.
        use_chart: Enable chart recognition mode.

    Returns:
        Concatenated markdown text from all chunks.
    """
    if fitz is None:
        raise RuntimeError("PyMuPDF not installed for PDF chunking")

    url = api_url or DEFAULT_API_URL
    token = api_token or DEFAULT_API_TOKEN
    if not token:
        raise RuntimeError("PaddleOCR API token not configured. Set PADDLEOCR_API_TOKEN.")

    path = Path(pdf_path)
    doc = fitz.open(str(path))
    total_pages = len(doc)
    all_parts: list[str] = []

    num_chunks = (total_pages + pages_per_chunk - 1) // pages_per_chunk
    chunk_timeout = max(timeout // num_chunks, 120)

    import tempfile

    for start in range(0, total_pages, pages_per_chunk):
        end = min(start + pages_per_chunk, total_pages)
        chunk_doc = fitz.open()
        for i in range(start, end):
            chunk_doc.insert_pdf(doc, from_page=i, to_page=i)

        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
            tmp_path = tmp.name
            chunk_doc.save(tmp_path)
        chunk_doc.close()

        try:
            job_id = _submit_job(tmp_path, url, token, use_chart=use_chart)
            jsonl_url = _poll_job(job_id, url, token, timeout=chunk_timeout)
            text = _download_and_parse(jsonl_url)
            all_parts.append(text)
            logger.info(
                "PaddleOCR v2 chunk %d-%d/%d extracted: %s",
                start + 1,
                end,
                total_pages,
                path.name,
            )
        finally:
            os.unlink(tmp_path)

    doc.close()

    if not all_parts:
        raise RuntimeError("PaddleOCR API chunked extraction returned no text")

    logger.info(
        "Content extracted via PaddleOCR v2 (chunked, %d chunks): %s",
        num_chunks,
        path.name,
    )
    return "\n\n".join(all_parts)


__all__ = [
    "is_available",
    "extract_pdf",
    "extract_pdf_chunked",
    "DEFAULT_API_URL",
    "DEFAULT_API_TOKEN",
]
