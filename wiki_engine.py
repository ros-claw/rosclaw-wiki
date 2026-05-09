"""ROSClaw Wiki Engine — core logic for wiki lifecycle management.

Pure Python, no external LLM calls. LLM interaction is injected via callbacks.
"""

from __future__ import annotations

import json
import logging
import re
import shutil
from collections.abc import Callable
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Optional

import yaml

logger = logging.getLogger("rosclaw.engine")

_FRONTMATTER_RE = re.compile(r"\A---[ \t]*\n(.+?\n)---[ \t]*\n", re.DOTALL)
_WIKILINK_RE = re.compile(r"\[\[([^\]]+)\]\]")

# Source-type confidence initials
SOURCE_CONFIDENCE: dict[str, float] = {
    "official": 0.9,
    "paper": 0.8,
    "blog": 0.5,
    "article": 0.5,
    "unknown": 0.5,
}

VALID_TYPES = {"entity", "algorithm", "concept", "skill", "episode", "index", "log"}

_TYPE_DIRS = {
    "entity": "entities",
    "algorithm": "algorithms",
    "concept": "concepts",
    "skill": "skills",
    "episode": "episodes",
    "index": "",
    "log": "",
}


def get_type_dir(page_type: str) -> str:
    """Return the subdirectory name for a given page type."""
    return _TYPE_DIRS.get(page_type, f"{page_type}s")


# ── 3.1 YAML Frontmatter ──


def parse_frontmatter(content: str) -> tuple[dict[str, Any], str]:
    """Extract YAML frontmatter and body from markdown content.

    Returns:
        (meta_dict, body_string)
    """
    m = _FRONTMATTER_RE.match(content)
    if not m:
        return {}, content
    try:
        meta = yaml.safe_load(m.group(1))
    except Exception as exc:
        logger.warning("Failed to parse frontmatter: %s", exc)
        return {}, content
    if not isinstance(meta, dict):
        return {}, content
    body = content[m.end() :]
    return meta, body


def write_frontmatter(meta: dict[str, Any], body: str) -> str:
    """Serialize meta + body into a markdown string with YAML frontmatter."""
    # Ensure standard fields exist with defaults
    defaults = {
        "tags": [],
        "confidence": 0.5,
        "supersedes": [],
        "sources": [],
    }
    for key, val in defaults.items():
        meta.setdefault(key, val)
    yaml_str = yaml.safe_dump(meta, allow_unicode=True, sort_keys=False, default_flow_style=False)
    return f"---\n{yaml_str}---\n\n{body.lstrip()}"


def generate_page_id(title: str) -> str:
    """Generate a URL-safe slug from a title."""
    slug = re.sub(r"[^\w\s-]", "", title.lower().strip())
    slug = re.sub(r"[\s-]+", "_", slug)
    return slug or "untitled"


# ── 3.2 Confidence & Lifecycle ──


def update_confidence(meta: dict[str, Any], reinforcement: bool = False) -> dict[str, Any]:
    """Update confidence in meta dict.

    If reinforcement=True, boost by +0.05 (cap 1.0).
    Otherwise apply Ebbinghaus-style decay based on days since last_reinforced.
    Always updates last_reinforced to today.
    """
    meta = dict(meta)  # copy
    today = datetime.now().date()
    last_str = meta.get("last_reinforced") or meta.get("created_at", today.isoformat())
    try:
        last = datetime.fromisoformat(last_str).date()
    except Exception:
        last = today
    days = (today - last).days

    confidence = float(meta.get("confidence", 0.5))

    if reinforcement:
        confidence = min(1.0, confidence + 0.05)
        logger.debug("Confidence reinforced: %.2f", confidence)
    else:
        if days > 180:
            confidence *= 0.5
        elif days > 90:
            confidence *= 0.7
        elif days > 30:
            confidence *= 0.9
        logger.debug("Confidence decayed after %d days: %.2f", days, confidence)

    meta["confidence"] = round(confidence, 2)
    meta["last_reinforced"] = today.isoformat()
    return meta


def check_supersession_needed(new_meta: dict[str, Any], existing_meta: dict[str, Any]) -> bool:
    """Determine whether new info should supersede existing info.

    Rank by source type and recency. Newer + higher-or-equal rank wins.
    """
    new_source = new_meta.get("source_type", "unknown")
    old_source = existing_meta.get("source_type", "unknown")
    new_rank = SOURCE_CONFIDENCE.get(new_source, 0.5)
    old_rank = SOURCE_CONFIDENCE.get(old_source, 0.5)

    new_date_str = new_meta.get("created_at", "")
    old_date_str = existing_meta.get("created_at", "")
    try:
        new_date = datetime.fromisoformat(new_date_str)
    except Exception:
        new_date = datetime.min
    try:
        old_date = datetime.fromisoformat(old_date_str)
    except Exception:
        old_date = datetime.min

    if new_rank > old_rank:
        return True
    if new_rank == old_rank and new_date > old_date:
        return True
    return False


# ── 3.3 Conflict Handling ──


def handle_conflict(
    existing_page_path: str,
    field_name: str,
    old_value: Any,
    new_value: Any,
    new_source: str,
) -> str:
    """Append a conflict record to the existing page and return updated content.

    Preserves the old value in a ### 待核实冲突 section.
    """
    path = Path(existing_page_path)
    content = path.read_text(encoding="utf-8")
    meta, body = parse_frontmatter(content)

    # Determine old source for context
    old_source = meta.get("source_type", "unknown")
    conflict_line = (
        f"- **{field_name}** — old: `{old_value}` (from {old_source}) "
        f"vs new: `{new_value}` (from {new_source})"
    )

    # Inject or append to conflict section
    conflict_header = "### 待核实冲突"
    if conflict_header in body:
        body = body.replace(conflict_header, f"{conflict_header}\n{conflict_line}")
    else:
        body = body.rstrip() + f"\n\n{conflict_header}\n{conflict_line}\n"

    # Mark old field as superseded in meta
    superseded = meta.get("superseded_fields", {})
    if not isinstance(superseded, dict):
        superseded = {}
    superseded[field_name] = {"value": old_value, "source": old_source}
    meta["superseded_fields"] = superseded

    return write_frontmatter(meta, body)


# ── 3.4 File Operations ──


def create_page(dir_path: str, title: str, body: str, meta: dict[str, Any]) -> str:
    """Create a new wiki page with auto-generated ID and frontmatter.

    Returns:
        Absolute file path of the created page.
    """
    import file_lock

    target_dir = Path(dir_path)
    target_dir.mkdir(parents=True, exist_ok=True)

    page_id = meta.get("id") or generate_page_id(title)
    filename = f"{page_id}.md"
    filepath = target_dir / filename

    if filepath.exists():
        logger.warning("Page already exists, will not overwrite: %s", filepath)
        return str(filepath)

    today = datetime.now().isoformat(timespec="seconds")
    full_meta = {
        "id": page_id,
        "title": title,
        "type": meta.get("type", "episode"),
        "tags": meta.get("tags", []),
        "confidence": meta.get("confidence", 0.5),
        "created_at": meta.get("created_at", today),
        "last_reinforced": meta.get("last_reinforced", today),
        "supersedes": meta.get("supersedes", []),
        "sources": meta.get("sources", []),
    }
    # Merge any extra fields
    for k, v in meta.items():
        if k not in full_meta:
            full_meta[k] = v

    content = write_frontmatter(full_meta, body)
    with file_lock.acquire_lock(filepath):
        filepath.write_text(content, encoding="utf-8")
    logger.info("Created page: %s", filepath)

    # Phase 7: trigger heuristic entity linker
    try:
        import entity_linker
        entity_linker.process(str(target_dir.parent), str(filepath))
    except Exception as exc:
        logger.warning("Entity linker failed for new page %s: %s", filepath, exc)

    return str(filepath)


def update_page(
    path: str,
    instruction: str,
    llm_func: Callable[[str, str], str],
) -> str:
    """Update a page by applying an LLM-generated edit.

    Args:
        path: Path to the markdown page.
        instruction: Natural-language edit instruction.
        llm_func: Callback that receives (prompt, current_content) and returns new body.

    Returns:
        The updated full page content.
    """
    import file_lock

    filepath = Path(path)
    if not filepath.exists():
        raise FileNotFoundError(f"Page not found: {path}")

    with file_lock.acquire_lock(filepath):
        content = filepath.read_text(encoding="utf-8")
        meta, body = parse_frontmatter(content)

        prompt = (
            f"You are editing a wiki page. Follow this instruction exactly:\n"
            f"INSTRUCTION: {instruction}\n\n"
            f"Current page content (do not modify YAML frontmatter):\n\n{body}\n\n"
            f"Return ONLY the new page body text, without frontmatter."
        )
        new_body = llm_func(prompt, body)

        # Update confidence / last_reinforced
        meta = update_confidence(meta, reinforcement=True)
        new_content = write_frontmatter(meta, new_body)
        filepath.write_text(new_content, encoding="utf-8")
    logger.info("Updated page: %s", filepath)

    # Phase 7: trigger heuristic entity linker
    try:
        import entity_linker
        entity_linker.process(str(filepath.parent.parent), str(filepath))
    except Exception as exc:
        logger.warning("Entity linker failed for updated page %s: %s", filepath, exc)

    return new_content


def move_to_archive(source_path: str, wiki_root: str) -> str:
    """Move a page to wiki/archive/ and leave a stub behind.

    Returns:
        Path to the archived file.
    """
    src = Path(source_path)
    root = Path(wiki_root)
    archive_dir = root / "archive"
    archive_dir.mkdir(parents=True, exist_ok=True)

    archive_path = archive_dir / src.name
    counter = 1
    while archive_path.exists():
        archive_path = archive_dir / f"{src.stem}_{counter}{src.suffix}"
        counter += 1

    shutil.move(str(src), str(archive_path))
    logger.info("Archived page: %s -> %s", src, archive_path)

    # Leave stub
    stub_content = (
        f"> [!CAUTION] 此知识已被归档\n> "
        f"原页面已移至 [[archive/{archive_path.stem}]]。\n"
    )
    src.write_text(stub_content, encoding="utf-8")
    return str(archive_path)


# ── 3.5 Index & Log ──


def update_index(wiki_root: str) -> str:
    """Rebuild wiki/index.md from all pages under wiki_root.

    Returns:
        Path to the updated index file.
    """
    root = Path(wiki_root)
    index_path = root / "index.md"

    categories: dict[str, list[tuple[str, str, str]]] = {
        "entity": [],
        "algorithm": [],
        "concept": [],
        "skill": [],
        "episode": [],
    }

    for md_file in sorted(root.rglob("*.md")):
        if md_file.name == "index.md" or md_file.name == "log.md":
            continue
        try:
            content = md_file.read_text(encoding="utf-8")
            meta, _ = parse_frontmatter(content)
            ptype = meta.get("type", "episode")
            title = meta.get("title", md_file.stem.replace("_", " ").title())
            rel = md_file.relative_to(root)
            link = f"[[{rel.with_suffix('').as_posix()}|{title}]]"
            categories.setdefault(ptype, []).append((title, link, "<!-- TODO -->"))
        except Exception as exc:
            logger.warning("Failed to index %s: %s", md_file, exc)

    lines = [
        "---",
        "id: index",
        "type: index",
        "tags: [meta]",
        "confidence: 1.0",
        f"created_at: {datetime.now().isoformat(timespec='seconds')}",
        f"last_reinforced: {datetime.now().isoformat(timespec='seconds')}",
        "supersedes: []",
        "sources: []",
        "---",
        "",
        "# ROSClaw Wiki Index",
        "",
        "Auto-generated catalog of the knowledge base.",
        "",
    ]

    _PLURALS = {
        "entity": "Entities",
        "algorithm": "Algorithms",
        "concept": "Concepts",
        "skill": "Skills",
        "episode": "Episodes",
    }
    for cat in ["entity", "algorithm", "concept", "skill", "episode"]:
        lines.append(f"## {_PLURALS[cat]}")
        lines.append("")
        items = categories.get(cat, [])
        if items:
            for title, link, summary in items:
                lines.append(f"- {link} — {summary}")
        else:
            lines.append("_No entries yet._")
        lines.append("")

    index_path.write_text("\n".join(lines), encoding="utf-8")
    logger.info("Updated index: %s", index_path)
    return str(index_path)


def append_log(wiki_root: str, entry: str) -> str:
    """Append a timestamped entry to wiki/log.md.

    Returns:
        The full log file path.
    """
    root = Path(wiki_root)
    log_path = root / "log.md"

    if not log_path.exists():
        log_path.write_text(
            "---\nid: log\ntype: log\ntags: [meta]\nconfidence: 1.0\ncreated_at: "
            + datetime.now().isoformat(timespec="seconds")
            + "\nlast_reinforced: "
            + datetime.now().isoformat(timespec="seconds")
            + "\nsupersedes: []\nsources: []\n---\n\n# ROSClaw Wiki Log\n\n",
            encoding="utf-8",
        )

    timestamp = datetime.now().isoformat(timespec="seconds")
    line = f"## [{timestamp}] {entry}\n\n"
    with log_path.open("a", encoding="utf-8") as f:
        f.write(line)
    logger.info("Appended to log: %s", entry)
    return str(log_path)


# ── Utilities ──


def list_pages(wiki_root: str) -> list[dict[str, Any]]:
    """Return a list of all page metadata dicts under wiki_root."""
    root = Path(wiki_root)
    results: list[dict[str, Any]] = []
    for md_file in root.rglob("*.md"):
        if md_file.name in ("index.md", "log.md"):
            continue
        try:
            content = md_file.read_text(encoding="utf-8")
            meta, _ = parse_frontmatter(content)
            meta["_path"] = str(md_file)
            results.append(meta)
        except Exception as exc:
            logger.warning("Failed to read %s: %s", md_file, exc)
    return results


def find_orphan_pages(wiki_root: str) -> list[str]:
    """Find pages with no inbound wikilinks."""
    root = Path(wiki_root)
    all_links: set[str] = set()
    all_pages: dict[str, Path] = {}
    page_slugs: dict[str, str] = {}  # slug -> rel path

    for md_file in root.rglob("*.md"):
        rel = md_file.relative_to(root).with_suffix("").as_posix()
        all_pages[rel] = md_file
        page_slugs[generate_page_id(md_file.stem)] = rel
        # Also index by title if present in frontmatter
        try:
            meta, _ = parse_frontmatter(md_file.read_text(encoding="utf-8"))
            if meta.get("title"):
                page_slugs[generate_page_id(meta["title"])] = rel
        except Exception:
            pass
        content = md_file.read_text(encoding="utf-8")
        for match in _WIKILINK_RE.finditer(content):
            link_target = match.group(1).split("|")[0].strip()
            all_links.add(link_target)
            # Also add slugified version for matching
            all_links.add(generate_page_id(link_target))

    orphans = []
    for rel, path in all_pages.items():
        if rel in ("index", "log"):
            continue
        # Check if any link matches this page by rel path, slug, or title
        linked = False
        for link in all_links:
            if link == rel or link == path.stem or link == generate_page_id(path.stem):
                linked = True
                break
        if not linked:
            orphans.append(str(path))
    return orphans
