"""ROSClaw Code Repo Scanner — scan local code repositories and generate wiki entities.

Scans `data/raw/code/` for cloned repositories, parses their READMEs and Python files,
and creates structured wiki pages under `wiki/entities/` for each important component.

Usage:
    python code_repo_scanner.py --input data/raw/code/ --output wiki/entities/
"""

from __future__ import annotations

import argparse
import ast
import logging
import re
from pathlib import Path
from typing import Any

import wiki_engine as engine

logger = logging.getLogger("rosclaw.code_scanner")


def _extract_repo_info(readme_path: Path) -> dict[str, Any]:
    """Parse a README.md to extract repo metadata."""
    text = readme_path.read_text(encoding="utf-8", errors="ignore")

    # Extract title (first # heading)
    title_match = re.search(r"^#\s+(.+)$", text, re.MULTILINE)
    title = title_match.group(1).strip() if title_match else readme_path.parent.name

    # Extract description (first paragraph after title)
    desc_match = re.search(r"^#\s+.+\n+(.+?)(?:\n\n|\n##)", text, re.DOTALL | re.MULTILINE)
    description = desc_match.group(1).strip() if desc_match else ""

    # Extract key sections
    sections: dict[str, str] = {}
    for header, content in re.findall(r"##+\s+(.+?)\n(.*?)(?=\n##+\s+|\Z)", text, re.DOTALL):
        sections[header.strip().lower()] = content.strip()[:500]

    # Try to find GitHub URL from text
    url_match = re.search(r"https?://github\.com/[^\s\)\"\']+", text)
    url = url_match.group(0) if url_match else ""

    # Find language mentions
    languages: list[str] = []
    if re.search(r"\bpython\b", text, re.I):
        languages.append("Python")
    if re.search(r"\bC\+\+\b", text):
        languages.append("C++")
    if re.search(r"\bros\b", text, re.I):
        languages.append("ROS/ROS2")

    return {
        "title": title,
        "description": description,
        "url": url,
        "languages": languages,
        "sections": sections,
        "folder_name": readme_path.parent.name,
    }


def _scan_python_files(repo_path: Path) -> list[dict[str, Any]]:
    """Scan Python files for classes, functions, and constants."""
    components: list[dict[str, Any]] = []

    for py_file in repo_path.rglob("*.py"):
        if "/venv/" in str(py_file) or "/.venv/" in str(py_file):
            continue
        try:
            source = py_file.read_text(encoding="utf-8", errors="ignore")
            tree = ast.parse(source)
        except SyntaxError:
            continue
        except Exception:
            continue

        rel_path = py_file.relative_to(repo_path)
        for node in ast.iter_child_nodes(tree):
            if isinstance(node, ast.ClassDef):
                # Extract docstring
                docstring = ast.get_docstring(node) or ""
                components.append({
                    "type": "class",
                    "name": node.name,
                    "file": str(rel_path),
                    "docstring": docstring[:200],
                    "lineno": node.lineno,
                })
            elif isinstance(node, ast.FunctionDef) and not node.name.startswith("_"):
                docstring = ast.get_docstring(node) or ""
                components.append({
                    "type": "function",
                    "name": node.name,
                    "file": str(rel_path),
                    "docstring": docstring[:200],
                    "lineno": node.lineno,
                })

    # Sort by importance heuristic: classes first, then by docstring length
    components.sort(key=lambda c: (0 if c["type"] == "class" else 1, -len(c["docstring"])))
    return components[:15]  # Top 15 components per repo


def _find_related_wiki_pages(wiki_root: Path, repo_title: str, description: str) -> list[str]:
    """Find existing wiki pages that might be related to this repo."""
    related: list[str] = []
    keywords = set(re.findall(r"\b[A-Z][a-zA-Z0-9_]+\b", repo_title + " " + description))

    for md_file in wiki_root.rglob("*.md"):
        if md_file.name in ("index.md", "log.md"):
            continue
        try:
            meta, body = engine.parse_frontmatter(md_file.read_text(encoding="utf-8"))
            title = meta.get("title", md_file.stem)
            for kw in keywords:
                if kw.lower() in title.lower() or kw.lower() in body.lower()[:500]:
                    related.append(title)
                    break
        except Exception:
            continue

    return related[:5]


def _generate_repo_page(repo_info: dict[str, Any], components: list[dict[str, Any]], related_pages: list[str]) -> str:
    """Generate markdown body for a code repository wiki page."""
    lines: list[str] = []

    lines.append(f"# {repo_info['title']}\n")
    lines.append(f"{repo_info['description']}\n")

    if repo_info.get("url"):
        lines.append(f"**Source:** [{repo_info['url']}]({repo_info['url']})\n")

    if repo_info.get("languages"):
        lines.append(f"**Languages:** {', '.join(repo_info['languages'])}\n")

    # Key sections from README
    for section_name, content in repo_info.get("sections", {}).items():
        if section_name in ("installation", "setup", "requirements", "dependencies"):
            lines.append(f"## {section_name.capitalize()}\n")
            lines.append(f"{content[:400]}\n")

    # Components
    if components:
        lines.append("## Key Components\n")
        for comp in components[:10]:
            lines.append(f"- `{comp['name']}` ({comp['type']}) — {comp['docstring'][:100]}\n")

    # Relationships
    if related_pages:
        lines.append("\n## Relationships\n")
        for page in related_pages:
            lines.append(f"- **Implements / Related to**: [[{page}]]\n")

    lines.append("\n## See Also\n")
    lines.append("- [[Code Repository]] — general code entity guidelines\n")
    if related_pages:
        for page in related_pages[:3]:
            lines.append(f"- [[{page}]]\n")

    return "".join(lines)


def scan_repos(input_dir: str, output_dir: str, wiki_root: str) -> dict[str, Any]:
    """Main entry point: scan all repos and create wiki pages.

    Returns:
        Summary dict with counts.
    """
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    wiki_path = Path(wiki_root)
    output_path.mkdir(parents=True, exist_ok=True)

    created = 0
    skipped = 0

    for repo_dir in input_path.iterdir():
        if not repo_dir.is_dir():
            continue

        readme = repo_dir / "README.md"
        if not readme.exists():
            logger.warning("No README in %s; skipping", repo_dir)
            skipped += 1
            continue

        repo_info = _extract_repo_info(readme)
        components = _scan_python_files(repo_dir)
        related = _find_related_wiki_pages(wiki_path, repo_info["title"], repo_info["description"])

        # Generate page
        body = _generate_repo_page(repo_info, components, related)
        slug = engine.generate_page_id(repo_info["title"])
        page_path = output_path / f"{slug}.md"

        # Avoid overwriting existing pages unless this is a code entity
        if page_path.exists():
            logger.info("Page already exists: %s; skipping", page_path)
            skipped += 1
            continue

        frontmatter = {
            "id": slug,
            "title": repo_info["title"],
            "type": "entity",
            "tags": ["code_repository"] + [t.lower().replace("/", "_") for t in repo_info.get("languages", [])],
            "confidence": 0.7,
            "sources": [f"code/{repo_dir.name}"],
            "source_type": "official_manual",
        }

        content = engine.write_frontmatter(frontmatter, body)
        page_path.write_text(content, encoding="utf-8")
        created += 1

        engine.append_log(wiki_root, f"code_scanner | created [[{repo_info['title']}]] from {repo_dir.name}")
        logger.info("Created code entity page: %s", page_path)

    return {
        "status": "done",
        "repos_scanned": created + skipped,
        "pages_created": created,
        "skipped": skipped,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="ROSClaw Code Repo Scanner")
    parser.add_argument("--input", default="data/raw/code", help="Directory with cloned repos")
    parser.add_argument("--output", default="wiki/entities", help="Wiki output directory")
    parser.add_argument("--wiki-root", default="wiki", help="Wiki root for indexing")
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")

    result = scan_repos(args.input, args.output, args.wiki_root)
    print(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
