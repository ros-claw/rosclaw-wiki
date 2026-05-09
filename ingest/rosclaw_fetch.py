#!/usr/bin/env python3
"""ROSClaw Awesome Fetcher 2.0 — clean, deduplicated, noise-filtered resource downloader.

Usage:
    python rosclaw_fetch.py --input awesome.md --output-dir data/raw [--max-repo-size 500]
"""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import logging
import os
import re
import sqlite3
import subprocess
import sys
import time
from pathlib import Path
from typing import Optional
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

logger = logging.getLogger("rosclaw.fetcher")

# Regex to extract Markdown links [text](url)
LINK_RE = re.compile(r"\[([^\]]+)\]\((https?://[^\s)]+)\)")
_URL_RE = re.compile(r"https?://[^\s\)\]\>\"\']+")

ARXIV_ID_RE = re.compile(r"arxiv\.org/(?:abs|pdf)/(\d+\.\d+)(?:\.pdf)?")
GITHUB_REPO_RE = re.compile(r"github\.com/([^/]+)/([^/]+)/?")

# Noise URL patterns
NOISE_PATTERNS = [
    re.compile(r"shields\.io", re.I),
    re.compile(r"img\.shields\.io", re.I),
    re.compile(r"github\.com/.*/issues", re.I),
    re.compile(r"github\.com/.*/pull", re.I),
    re.compile(r"github\.com/.*/pulls", re.I),
    re.compile(r"github\.com/.*/actions", re.I),
    re.compile(r"github\.com/.*/projects", re.I),
    re.compile(r"github\.com/.*/wiki", re.I),
    re.compile(r"github\.com/.*/security", re.I),
    re.compile(r"github\.com/.*/graphs", re.I),
    re.compile(r"badge\.(svg|png)", re.I),
    re.compile(r"license\.(svg|png)", re.I),
    re.compile(r"travis-ci\.(com|org)", re.I),
    re.compile(r"codecov\.io", re.I),
]

# ── Phase 18: Smart clone filtering ──

REPO_SIZE_LIMITS = {
    "default": 500,
    "research": 200,
    "ros": 1000,
    "driver": 300,
}

ALLOWED_FILE_EXTENSIONS = [
    # Source code
    ".py", ".cpp", ".c", ".h", ".hpp", ".rs", ".go", ".ts", ".js",
    # Build & config
    "CMakeLists.txt", "package.xml", "setup.py", "setup.cfg", "pyproject.toml",
    "Makefile", "meson.build", "Cargo.toml",
    # Documentation (top-level only)
    "README.md", "README", "LICENSE", "CHANGELOG.md",
    # URDF / robot models
    ".urdf", ".xacro", ".sdf", ".srdf",
    # Config files
    ".yaml", ".yml", ".json",
]

SKIP_PATTERNS = [
    # Large binary files
    "*.bin", "*.pth", "*.pt", "*.onnx", "*.pb", "*.h5", "*.ckpt",
    "*.weights", "*.safetensors", "*.tar", "*.tar.gz", "*.zip",
    # Dataset and model output
    "data/", "datasets/", "models/", "checkpoints/", "logs/",
    "wandb/", "mlruns/", "runs/", "outputs/",
    # Irrelevant directories
    "node_modules/", ".git/", "__pycache__/", "*.pyc",
    "notebooks/", "examples/", "demos/", "assets/",
    # Git LFS pointer files
    "*.gitattributes",
]


def _setup_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def _slugify(text: str) -> str:
    """Convert text to a filesystem-safe slug."""
    slug = re.sub(r"[^\w\s-]", "", text.lower().strip())
    slug = re.sub(r"[\s-]+", "_", slug)
    return slug or "untitled"


# ── Source Manifest (SQLite deduplication) ──


class SourceManifest:
    """SQLite-backed manifest for content-level deduplication."""

    def __init__(self, db_path: str = "data/Source_Manifest.db"):
        self.db_path = db_path
        self._ensure_table()

    def _ensure_table(self) -> None:
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS sources (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    url TEXT UNIQUE,
                    file_path TEXT,
                    sha256_hash TEXT,
                    downloaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
            )

    def is_duplicate(self, url: str, sha256: str | None = None) -> bool:
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.execute("SELECT 1 FROM sources WHERE url = ? LIMIT 1", (url,))
            if cur.fetchone():
                return True
            if sha256:
                cur = conn.execute(
                    "SELECT 1 FROM sources WHERE sha256_hash = ? LIMIT 1", (sha256,)
                )
                if cur.fetchone():
                    return True
        return False

    def record(
        self, url: str, file_path: str, sha256: str | None = None
    ) -> None:
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "INSERT OR REPLACE INTO sources (url, file_path, sha256_hash) VALUES (?, ?, ?)",
                (url, file_path, sha256),
            )


# ── URL helpers ──


def normalize_url(url: str) -> str:
    """Normalize URL for deduplication."""
    arxiv_id = parse_arxiv_id(url)
    if arxiv_id:
        return f"arxiv:{arxiv_id}"
    # Strip trailing slash and fragment
    url = url.split("#")[0].rstrip("/")
    return url


def is_noise_url(url: str) -> bool:
    """Check if URL is noise (badges, issues, etc.)."""
    for pattern in NOISE_PATTERNS:
        if pattern.search(url):
            return True
    return False


def extract_urls(markdown_path: str) -> list[tuple[str, str]]:
    """Extract all (text, url) tuples from a markdown file, filtering noise."""
    content = Path(markdown_path).read_text(encoding="utf-8")
    links = LINK_RE.findall(content)
    result = [(text.strip(), url) for text, url in links if not is_noise_url(url)]
    seen = {url for _, url in result}

    # Find bare URLs not inside markdown links
    for line in content.splitlines():
        if LINK_RE.search(line):
            continue
        for match in _URL_RE.finditer(line):
            url = match.group(0)
            if not is_noise_url(url) and url not in seen:
                result.append((url, url))
                seen.add(url)
    return result


def classify_url(url: str) -> str:
    """Classify a URL into one of: paper, code, article."""
    netloc = urlparse(url).netloc.lower()
    if "arxiv.org" in netloc:
        return "paper"
    if "github.com" in netloc:
        return "code"
    return "article"


def parse_arxiv_id(url: str) -> Optional[str]:
    """Extract arXiv ID from URL."""
    m = ARXIV_ID_RE.search(url)
    return m.group(1) if m else None


def parse_github_repo(url: str) -> Optional[tuple[str, str]]:
    """Extract (owner, repo) from GitHub URL."""
    m = GITHUB_REPO_RE.search(url)
    return (m.group(1), m.group(2)) if m else None


# ── Network helpers with retry ──


def fetch_with_retry(
    url: str,
    timeout: int = 60,
    max_retries: int = 2,
    headers: dict | None = None,
) -> requests.Response:
    """Fetch URL with retry logic."""
    default_headers = {
        "User-Agent": "ROSClaw-Fetcher/2.0 (Research Bot)",
    }
    if headers:
        default_headers.update(headers)

    last_exc: Exception | None = None
    for attempt in range(max_retries + 1):
        try:
            resp = requests.get(url, timeout=timeout, headers=default_headers)
            resp.raise_for_status()
            return resp
        except requests.RequestException as exc:
            last_exc = exc
            logger.warning("Fetch attempt %d failed for %s: %s", attempt + 1, url, exc)
            if attempt < max_retries:
                time.sleep(2 ** attempt)
    raise last_exc  # type: ignore[misc]


def compute_sha256(data: bytes) -> str:
    """Compute SHA256 hex digest of bytes."""
    return hashlib.sha256(data).hexdigest()


# ── Download implementations ──


def _fetch_arxiv_metadata(arxiv_id: str) -> dict | None:
    """Fetch arXiv metadata via direct API query with long delays."""
    api_url = f"https://export.arxiv.org/api/query?id_list={arxiv_id}"
    try:
        time.sleep(5)  # Respect arXiv rate limits
        resp = fetch_with_retry(api_url, timeout=30, max_retries=2)
        import xml.etree.ElementTree as ET

        root = ET.fromstring(resp.text.encode("utf-8"))
        ns = {"atom": "http://www.w3.org/2005/Atom", "arxiv": "http://arxiv.org/schemas/atom"}
        entry = root.find("atom:entry", ns)
        if entry is None:
            return None
        title = entry.findtext("atom:title", "", ns)
        summary = entry.findtext("atom:summary", "", ns)
        published = entry.findtext("atom:published", "", ns)
        authors = [a.findtext("atom:name", "", ns) for a in entry.findall("atom:author", ns)]
        cat = entry.find("atom:category", ns)
        primary = cat.get("term") if cat is not None else ""
        all_cats = [c.get("term") for c in entry.findall("atom:category", ns) if c.get("term")]
        doi_elem = entry.find("arxiv:doi", ns)
        doi = doi_elem.text if doi_elem is not None else None
        return {
            "title": title.strip() if title else "",
            "authors": [a for a in authors if a],
            "summary": summary.strip() if summary else "",
            "published": published.strip() if published else "",
            "primary_category": primary,
            "categories": all_cats,
            "doi": doi,
        }
    except Exception as exc:
        logger.warning("Failed to fetch arXiv metadata for %s: %s", arxiv_id, exc)
        return None


def download_arxiv_paper(
    url: str, output_dir: Path, manifest: SourceManifest
) -> Optional[Path]:
    """Download an arXiv paper via direct PDF URL to avoid API rate limits."""
    arxiv_id = parse_arxiv_id(url)
    if not arxiv_id:
        logger.warning("Could not parse arXiv ID from %s", url)
        return None

    norm_url = f"arxiv:{arxiv_id}"
    if manifest.is_duplicate(norm_url):
        logger.info("[SKIP] Duplicate arXiv paper: %s", arxiv_id)
        return None

    pdf_path = output_dir / f"{arxiv_id}.pdf"
    meta_path = output_dir / f"{arxiv_id}.json"

    if pdf_path.exists():
        logger.info("[SKIP] Existing arXiv paper: %s", pdf_path.name)
        manifest.record(norm_url, str(pdf_path))
        return pdf_path

    logger.info("Downloading arXiv paper: %s", arxiv_id)
    try:
        # Direct PDF download (bypasses arXiv API rate limits)
        pdf_url = f"https://arxiv.org/pdf/{arxiv_id}.pdf"
        resp = fetch_with_retry(pdf_url, timeout=120, max_retries=3)
        pdf_path.write_bytes(resp.content)
        logger.info("Saved PDF: %s", pdf_path)

        # Try to fetch metadata (best effort, with long delays)
        meta = {
            "arxiv_id": arxiv_id,
            "url": url,
            "pdf_url": pdf_url,
        }
        fetched = _fetch_arxiv_metadata(arxiv_id)
        if fetched:
            meta.update(fetched)
            logger.info("Fetched metadata for %s: %s", arxiv_id, fetched.get("title", "")[:60])
        else:
            logger.warning("Could not fetch metadata for %s (proceeding anyway)", arxiv_id)

        meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
        logger.info("Saved metadata: %s", meta_path)

        # Record in manifest
        pdf_hash = compute_sha256(pdf_path.read_bytes())
        manifest.record(norm_url, str(pdf_path), pdf_hash)
    except Exception as exc:
        logger.error("Failed to download arXiv paper %s: %s", arxiv_id, exc)
        return None

    time.sleep(1)
    return pdf_path


# ── Phase 18: Smart clone helpers ──

def _get_dir_size(path: Path) -> int:
    """Return total size of directory in bytes."""
    total = 0
    for entry in path.rglob("*"):
        if entry.is_file():
            total += entry.stat().st_size
    return total


def _count_source_files(path: Path) -> int:
    """Count files matching ALLOWED_FILE_EXTENSIONS."""
    count = 0
    for ext in ALLOWED_FILE_EXTENSIONS:
        if ext.startswith("."):
            count += len(list(path.rglob(f"*{ext}")))
        else:
            count += len(list(path.rglob(ext)))
    return count


def _cleanup_skipped_files(repo_dir: Path) -> None:
    """Remove files and directories matching SKIP_PATTERNS."""
    removed = 0
    for pattern in SKIP_PATTERNS:
        if pattern.endswith("/"):
            # Directory pattern
            for subdir in repo_dir.rglob(pattern.rstrip("/")):
                if subdir.is_dir():
                    try:
                        import shutil
                        shutil.rmtree(subdir)
                        removed += 1
                    except Exception:
                        pass
        else:
            # File pattern (glob-style)
            for fp in repo_dir.rglob(pattern):
                if fp.is_file():
                    try:
                        fp.unlink()
                        removed += 1
                    except Exception:
                        pass
    if removed:
        logger.info("Cleaned up %d skipped files/dirs in %s", removed, repo_dir.name)


def _sparse_clone_repo(repo_url: str, repo_dir: Path) -> bool:
    """Sparse-clone a large repo: only checkout allowed file types."""
    try:
        # Step 1: clone file tree only (no blobs)
        subprocess.run(
            ["git", "clone", "--filter=blob:none", "--no-checkout", "--depth=1", repo_url, str(repo_dir)],
            check=True, capture_output=True, text=True, timeout=300,
        )
        # Step 2: configure sparse-checkout
        sparse_file = repo_dir / ".git" / "info" / "sparse-checkout"
        sparse_file.parent.mkdir(parents=True, exist_ok=True)
        lines = []
        for ext in ALLOWED_FILE_EXTENSIONS:
            if ext.startswith("."):
                lines.append(f"*{ext}")
            else:
                lines.append(ext)
        sparse_file.write_text("\n".join(lines) + "\n", encoding="utf-8")
        # Step 3: enable sparse-checkout and checkout
        subprocess.run(
            ["git", "-C", str(repo_dir), "config", "core.sparseCheckout", "true"],
            check=True, capture_output=True, text=True,
        )
        subprocess.run(
            ["git", "-C", str(repo_dir), "checkout", "HEAD"],
            check=True, capture_output=True, text=True, timeout=120,
        )
        # Step 4: cleanup
        _cleanup_skipped_files(repo_dir)
        return True
    except subprocess.CalledProcessError as exc:
        logger.error("Sparse clone failed for %s: %s", repo_url, exc.stderr or exc)
        return False
    except subprocess.TimeoutExpired:
        logger.error("Sparse clone timeout for %s", repo_url)
        return False


def get_repo_size_mb(owner: str, repo: str) -> float | None:
    """Query GitHub API for repo size in MB."""
    api_url = f"https://api.github.com/repos/{owner}/{repo}"
    try:
        resp = fetch_with_retry(api_url, timeout=15, max_retries=1)
        data = resp.json()
        size_kb = data.get("size", 0)
        return size_kb / 1024.0
    except Exception as exc:
        logger.warning("Could not query GitHub API for %s/%s: %s", owner, repo, exc)
        return None


def clone_github_repo(
    url: str,
    output_dir: Path,
    manifest: SourceManifest,
    max_repo_size_mb: float,
    use_sparse_clone: bool = False,
) -> Optional[Path]:
    """Shallow-clone a GitHub repository with size protection and optional sparse-checkout."""
    parsed = parse_github_repo(url)
    if not parsed:
        logger.warning("Could not parse GitHub repo from %s", url)
        return None
    owner, repo_name = parsed
    repo_dir = output_dir / f"{owner}_{repo_name}"

    norm_url = f"github:{owner}/{repo_name}"
    if manifest.is_duplicate(norm_url):
        logger.info("[SKIP] Duplicate repo: %s/%s", owner, repo_name)
        return None

    if repo_dir.exists():
        logger.info("[SKIP] Existing repo: %s", repo_dir.name)
        manifest.record(norm_url, str(repo_dir))
        return repo_dir

    # Size check
    size_mb = get_repo_size_mb(owner, repo_name)
    if size_mb is not None and size_mb > max_repo_size_mb and not use_sparse_clone:
        logger.warning(
            "[SKIP] Repo too large: %s/%s (%.1f MB > %.1f MB limit)",
            owner, repo_name, size_mb, max_repo_size_mb,
        )
        return None

    clone_url = f"https://github.com/{owner}/{repo_name}.git"

    # Decide clone strategy
    if use_sparse_clone and size_mb is not None and size_mb > max_repo_size_mb:
        logger.info(
            "Sparse-cloning large repo: %s/%s (%.1f MB)",
            owner, repo_name, size_mb,
        )
        success = _sparse_clone_repo(clone_url, repo_dir)
        if not success:
            return None
    else:
        logger.info("Cloning repo: %s/%s", owner, repo_name)
        try:
            subprocess.run(
                ["git", "clone", "--depth=1", clone_url, str(repo_dir)],
                check=True,
                capture_output=True,
                text=True,
                timeout=300,
            )
            logger.info("Cloned to: %s", repo_dir)
            _cleanup_skipped_files(repo_dir)
        except subprocess.CalledProcessError as exc:
            logger.error("Failed to clone %s/%s: %s", owner, repo_name, exc.stderr or exc)
            return None
        except FileNotFoundError:
            logger.error("git not found on PATH")
            return None
        except subprocess.TimeoutExpired:
            logger.error("Clone timeout for %s/%s", owner, repo_name)
            return None

    # Ensure README.md is at repo root
    readme_candidates = list(repo_dir.rglob("README.md"))
    if readme_candidates:
        root_readme = repo_dir / "README.md"
        if not root_readme.exists():
            root_readme.write_text(readme_candidates[0].read_text(encoding="utf-8"), encoding="utf-8")
            logger.info("Copied README.md to repo root")

    manifest.record(norm_url, str(repo_dir))

    # Log savings
    final_size_mb = _get_dir_size(repo_dir) / (1024 * 1024)
    logger.info(
        "Repo %s final size: %.1f MB (%.0f%% retained vs estimated %.1f MB)",
        repo_dir.name, final_size_mb,
        (final_size_mb / size_mb * 100) if size_mb else 100,
        size_mb or 0,
    )
    return repo_dir


def should_skip_for_quality(html_content: str) -> tuple[bool, str]:
    """Evaluate whether a web page has enough substantive content.

    Returns:
        (should_skip, reason)
    """
    try:
        soup = BeautifulSoup(html_content, "html.parser")
    except Exception:
        return False, "parser-error"

    # Remove non-content tags
    for tag in soup.find_all(["script", "style", "nav", "footer", "aside", "header"]):
        tag.decompose()

    body_text = soup.get_text(separator=" ", strip=True)
    full_text = soup.get_text(separator=" ", strip=True)

    body_len = len(body_text)
    full_len = len(full_text) or 1
    ratio = body_len / full_len

    if body_len < 200:
        return True, f"too-short ({body_len} chars)"
    if ratio < 0.30:
        return True, f"low-body-ratio ({ratio:.1%})"
    return False, ""


def download_article(
    url: str, output_dir: Path, manifest: SourceManifest
) -> Optional[Path]:
    """Download a web article and convert to Markdown with quality filtering."""
    try:
        import html2text
    except ImportError:
        logger.error("html2text not installed; cannot convert articles")
        return None

    slug = _slugify(urlparse(url).path.rstrip("/").split("/")[-1] or "article")
    md_path = output_dir / f"{slug}.md"

    norm_url = normalize_url(url)
    if manifest.is_duplicate(norm_url):
        logger.info("[SKIP] Duplicate article: %s", url)
        return None

    if md_path.exists():
        logger.info("[SKIP] Existing article: %s", md_path.name)
        manifest.record(norm_url, str(md_path))
        return md_path

    logger.info("Downloading article: %s", url)
    try:
        resp = fetch_with_retry(url, timeout=60)
    except requests.RequestException as exc:
        logger.error("Failed to download article %s: %s", url, exc)
        return None

    # Quality check
    should_skip, reason = should_skip_for_quality(resp.text)
    if should_skip:
        logger.warning("[SKIP] Article %s rejected: %s", url, reason)
        return None

    try:
        h = html2text.HTML2Text()
        h.ignore_links = False
        h.ignore_images = True
        h.body_width = 0
        markdown = h.handle(resp.text)
        content = f"# Source\n\nURL: {url}\n\n---\n\n{markdown}"
        md_path.write_text(content, encoding="utf-8")
        logger.info("Saved article: %s", md_path)
    except Exception as exc:
        logger.error("Failed to convert article %s: %s", url, exc)
        return None

    content_hash = compute_sha256(md_path.read_bytes())
    manifest.record(norm_url, str(md_path), content_hash)
    time.sleep(0.5)
    return md_path


# ── Main entry ──


def fetch_all(
    input_path: str, output_dir: str, max_repo_size_mb: float, use_sparse_clone: bool = False
) -> dict[str, list[Path]]:
    """Main entry: parse markdown and download all linked resources."""
    out = Path(output_dir)
    (out / "papers").mkdir(parents=True, exist_ok=True)
    (out / "code").mkdir(parents=True, exist_ok=True)
    (out / "articles").mkdir(parents=True, exist_ok=True)

    manifest = SourceManifest(os.path.join(output_dir, "..", "Source_Manifest.db"))

    urls = extract_urls(input_path)
    logger.info("Found %d unique URLs in %s", len(urls), input_path)

    results: dict[str, list[Path]] = {"paper": [], "code": [], "article": []}

    for text, url in urls:
        kind = classify_url(url)
        logger.info("[%s] %s — %s", kind, text[:60], url)

        if kind == "paper":
            path = download_arxiv_paper(url, out / "papers", manifest)
        elif kind == "code":
            path = clone_github_repo(url, out / "code", manifest, max_repo_size_mb, use_sparse_clone)
        else:
            path = download_article(url, out / "articles", manifest)

        if path:
            results[kind].append(path)

    return results


def main() -> int:
    _setup_logging()
    parser = argparse.ArgumentParser(description="ROSClaw Awesome Fetcher 2.0")
    parser.add_argument("--input", required=True, help="Path to Awesome List markdown file")
    parser.add_argument("--output-dir", default="data/raw", help="Output directory for raw resources")
    parser.add_argument(
        "--max-repo-size",
        type=float,
        default=500,
        help="Maximum repo size in MB to clone (default: 500)",
    )
    parser.add_argument(
        "--use-sparse-clone",
        action="store_true",
        help="Use sparse-checkout for large repos to save disk (Phase 18)",
    )
    args = parser.parse_args()

    if not Path(args.input).exists():
        logger.error("Input file not found: %s", args.input)
        return 1

    results = fetch_all(args.input, args.output_dir, args.max_repo_size, args.use_sparse_clone)
    total = sum(len(v) for v in results.values())
    logger.info(
        "Done. Downloaded %d resources: %d papers, %d repos, %d articles",
        total,
        len(results["paper"]),
        len(results["code"]),
        len(results["article"]),
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
