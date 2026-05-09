#!/usr/bin/env python3
"""Parse an Awesome List README and generate a standardized YAML for the Fetcher.

Usage:
    python generate_awesome_list.py --input /tmp/awesome-vln/README.md --output awesome_vln.yml
"""

from __future__ import annotations

import argparse
import logging
import re
from pathlib import Path
from typing import Any

import yaml

logger = logging.getLogger("rosclaw.generate_awesome_list")

# Blacklist patterns
_BLACKLIST_URLS = {
    "shields.io",
    "img.shields.io",
    "github.com/KwanWaiPang/Awesome-VLN",
    "/issues/",
    "/pull/",
    "github.com/KwanWaiPang/Awesome-Transformer",
    "github.com/KwanWaiPang/Awesome-VLA",
    "github.com/KwanWaiPang/Awesome-ES",
    "github.com/KwanWaiPang/Awesome-Learning-based-Navigation",
}

# Regex patterns
_ARXIV_RE = re.compile(r"arxiv\.org/(?:abs|pdf)/(\d{4}\.\d{4,5})")
_GITHUB_RE = re.compile(r"github\.com/([^/\s]+/[^/\s]+)")
_URL_RE = re.compile(r"https?://[^\s\)\]\|]+")


def _is_blacklisted(url: str) -> bool:
    """Check if a URL should be excluded."""
    for pattern in _BLACKLIST_URLS:
        if pattern in url:
            return True
    return False


def _extract_arxiv_id(url: str) -> str | None:
    """Extract arXiv ID from URL."""
    m = _ARXIV_RE.search(url)
    return m.group(1) if m else None


def _extract_github_repo(url: str) -> str | None:
    """Extract GitHub repo name from URL."""
    m = _GITHUB_RE.search(url)
    return m.group(1) if m else None


def _clean_title(title: str) -> str:
    """Clean markdown formatting from paper title."""
    # Remove markdown links [text](url) → text
    title = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", title)
    # Remove bold/italic markers
    title = title.replace("**", "").replace("*", "")
    title = title.strip()
    return title


def parse_awesome_readme(readme_path: str) -> dict[str, Any]:
    """Parse an Awesome List README and extract structured resource list.

    Returns:
        Dict with keys: papers, code_repos, articles.
    """
    content = Path(readme_path).read_text(encoding="utf-8")
    lines = content.splitlines()

    papers: list[dict[str, str]] = []
    code_repos: list[dict[str, str]] = []
    articles: list[dict[str, str]] = []

    seen_papers: set[str] = set()
    seen_repos: set[str] = set()
    seen_articles: set[str] = set()

    in_table = False
    table_header_count = 0

    for line in lines:
        stripped = line.strip()

        # Detect table start (lines starting with |)
        if stripped.startswith("|") and "---" not in stripped and "Year" not in stripped:
            in_table = True
        elif not stripped.startswith("|") and in_table:
            in_table = False
            continue

        if not in_table:
            # Also look for standalone links outside tables
            for url in _URL_RE.findall(stripped):
                if _is_blacklisted(url):
                    continue
                arxiv_id = _extract_arxiv_id(url)
                if arxiv_id and arxiv_id not in seen_papers:
                    seen_papers.add(arxiv_id)
                    papers.append({
                        "title": f"arXiv:{arxiv_id}",
                        "arxiv_id": arxiv_id,
                        "url": url,
                    })
                github_repo = _extract_github_repo(url)
                if github_repo and github_repo not in seen_repos:
                    seen_repos.add(github_repo)
                    code_repos.append({
                        "name": github_repo.split("/")[-1],
                        "url": url,
                    })
            continue

        # Parse table row
        cells = [c.strip() for c in stripped.split("|")]
        # Remove empty first/last cells caused by leading/trailing |
        cells = [c for c in cells if c]
        if len(cells) < 3:
            continue

        # Typical Awesome-VLN table: Year | Venue | Paper Title | Repository | Note
        # Paper title is usually cell 2, Repository is cell 3, Note is cell 4
        title_cell = cells[2] if len(cells) > 2 else ""
        repo_cell = cells[3] if len(cells) > 3 else ""
        note_cell = cells[4] if len(cells) > 4 else ""

        title = _clean_title(title_cell)

        # Extract arXiv link from title cell
        arxiv_url = None
        for url in _URL_RE.findall(title_cell):
            if "arxiv.org" in url:
                arxiv_url = url
                break

        if arxiv_url:
            arxiv_id = _extract_arxiv_id(arxiv_url)
            if arxiv_id and arxiv_id not in seen_papers:
                seen_papers.add(arxiv_id)
                papers.append({
                    "title": title or f"arXiv:{arxiv_id}",
                    "arxiv_id": arxiv_id,
                    "url": arxiv_url,
                })

        # Extract GitHub repos from repository cell
        for url in _URL_RE.findall(repo_cell):
            if _is_blacklisted(url):
                continue
            github_repo = _extract_github_repo(url)
            if github_repo and github_repo not in seen_repos:
                seen_repos.add(github_repo)
                code_repos.append({
                    "name": github_repo.split("/")[-1],
                    "url": url,
                })

        # Extract other links from note cell
        for url in _URL_RE.findall(note_cell):
            if _is_blacklisted(url):
                continue
            arxiv_id = _extract_arxiv_id(url)
            if arxiv_id:
                if arxiv_id not in seen_papers:
                    seen_papers.add(arxiv_id)
                    papers.append({
                        "title": f"arXiv:{arxiv_id}",
                        "arxiv_id": arxiv_id,
                        "url": url,
                    })
                continue
            github_repo = _extract_github_repo(url)
            if github_repo:
                if github_repo not in seen_repos:
                    seen_repos.add(github_repo)
                    code_repos.append({
                        "name": github_repo.split("/")[-1],
                        "url": url,
                    })
                continue
            if url not in seen_articles:
                seen_articles.add(url)
                articles.append({
                    "title": url.split("/")[-1] or url,
                    "url": url,
                })

    return {
        "papers": papers,
        "code_repos": code_repos,
        "articles": articles,
    }


def main() -> int:
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    parser = argparse.ArgumentParser(description="Parse Awesome List README → YAML")
    parser.add_argument("--input", required=True, help="Path to README.md")
    parser.add_argument("--output", required=True, help="Output YAML path")
    args = parser.parse_args()

    result = parse_awesome_readme(args.input)

    # Write YAML
    output_path = Path(args.output)
    output_path.write_text(
        yaml.safe_dump(result, allow_unicode=True, sort_keys=False),
        encoding="utf-8",
    )

    logger.info("Generated %s", output_path)
    logger.info("  Papers: %d", len(result["papers"]))
    logger.info("  Code repos: %d", len(result["code_repos"]))
    logger.info("  Articles: %d", len(result["articles"]))

    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
