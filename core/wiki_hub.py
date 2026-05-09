"""ROSClaw Wiki Hub — push/pull protocol for knowledge distribution.

Implements a Git-friendly pack format for sharing wiki knowledge:
  - wiki_pack(): bundle wiki pages, judgments, and entity relations
  - wiki_unpack(): merge a pack into a target wiki
  - wiki_diff(): compare two packs or a pack vs local wiki
  - wiki_pull(): download and merge from a remote URL
"""

from __future__ import annotations

import json
import logging
import re
import shutil
import subprocess
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Any

import wiki_engine as engine

logger = logging.getLogger("rosclaw.wiki_hub")

# Pack format version
_PACK_FORMAT_VERSION = "1.0.0"

# Merge modes
MERGE_MODES = {"skip_existing", "overwrite", "ask"}


def _get_git_commit(wiki_root: str) -> str | None:
    """Try to get current git commit hash for the wiki directory."""
    try:
        result = subprocess.run(
            ["git", "-C", wiki_root, "rev-parse", "HEAD"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        if result.returncode == 0:
            return result.stdout.strip()[:8]
    except Exception:
        pass
    return None


def _auto_bump_version(previous: str | None, page_delta_pct: float) -> str:
    """Bump semantic version based on change magnitude."""
    if previous is None:
        return "1.0.0"

    parts = previous.split(".")
    if len(parts) != 3:
        return "1.0.0"

    try:
        major, minor, patch = int(parts[0]), int(parts[1]), int(parts[2])
    except ValueError:
        return "1.0.0"

    if page_delta_pct > 10.0:
        minor += 1
        patch = 0
    else:
        patch += 1

    return f"{major}.{minor}.{patch}"


def _extract_entity_relations(wiki_root: str) -> list[dict[str, str]]:
    """Scan all pages for auto-generated link relation sections."""
    root = Path(wiki_root)
    relations: list[dict[str, str]] = []
    seen: set[tuple[str, str, str]] = set()

    # Match entity_linker format: - `Source` --[[relation]]--> `Target`
    rel_pattern = re.compile(
        r"^\s*-\s*`([^`]+)`\s*--\[\[(.+?)\]\]-->\s*`([^`]+)`",
        re.MULTILINE,
    )

    for md_file in root.rglob("*.md"):
        if md_file.name in ("index.md", "log.md", "Admin_Dashboard.md"):
            continue
        try:
            content = md_file.read_text(encoding="utf-8")
            meta, body = engine.parse_frontmatter(content)
            source_slug = md_file.stem
            for match in rel_pattern.finditer(body):
                _source_name, rel_type, target = match.groups()
                target_slug = engine.generate_page_id(target.split("|")[0])
                key = (source_slug, target_slug, rel_type)
                if key not in seen:
                    seen.add(key)
                    relations.append({
                        "source": source_slug,
                        "target": target_slug,
                        "type": rel_type,
                    })
        except Exception:
            continue

    return relations


def _load_judgments(wiki_root: str) -> list[dict[str, Any]]:
    """Load all judgments from index.json or individual files."""
    root = Path(wiki_root)
    index_path = root / "judgments" / "index.json"
    if index_path.exists():
        try:
            data = json.loads(index_path.read_text(encoding="utf-8"))
            judgments: list[dict[str, Any]] = []
            for entity, contexts in data.get("by_entity", {}).items():
                for ctx, params in contexts.items():
                    for param, info in params.items():
                        judgments.append({
                            "entity": entity,
                            "context": ctx,
                            "parameter": param,
                            **info,
                        })
            return judgments
        except Exception:
            pass

    # Fallback: scan individual JSON files
    judgments = []
    judgments_dir = root / "judgments"
    if judgments_dir.exists():
        for json_file in judgments_dir.glob("*.json"):
            if json_file.name == "index.json":
                continue
            try:
                data = json.loads(json_file.read_text(encoding="utf-8"))
                judgments.extend(data)
            except Exception:
                continue
    return judgments


def wiki_pack(
    wiki_name: str,
    wiki_root: str,
    output_path: str | None = None,
    incremental: bool = False,
) -> dict[str, Any]:
    """Pack the current wiki into a wiki_pack.json file.

    Args:
        wiki_name: Name of the wiki (e.g., "Awesome-VLN-Wiki").
        wiki_root: Root directory of the wiki.
        output_path: Where to write the pack. Defaults to {wiki_root}/wiki_pack.json.
        incremental: If True, only include pages modified since last pack.

    Returns:
        Dict with pack summary.
    """
    root = Path(wiki_root)
    out_path = Path(output_path) if output_path else root / "wiki_pack.json"

    # Load previous pack for version bumping
    previous_version = None
    previous_count = 0
    if out_path.exists():
        try:
            prev = json.loads(out_path.read_text(encoding="utf-8"))
            previous_version = prev.get("meta", {}).get("version")
            previous_count = prev.get("meta", {}).get("total_pages", 0)
        except Exception:
            pass

    pages: list[dict[str, Any]] = []
    categories = {"entity": 0, "algorithm": 0, "concept": 0, "skill": 0, "episode": 0}

    for md_file in root.rglob("*.md"):
        if md_file.name in ("index.md", "log.md", "Admin_Dashboard.md"):
            continue
        try:
            rel = str(md_file.relative_to(root))
            content = md_file.read_text(encoding="utf-8")
            meta, body = engine.parse_frontmatter(content)

            if incremental and out_path.exists():
                # Check mtime against last pack
                mtime = md_file.stat().st_mtime
                pack_mtime = out_path.stat().st_mtime
                if mtime <= pack_mtime:
                    continue

            ptype = meta.get("type", "episode")
            categories[ptype] = categories.get(ptype, 0) + 1

            pages.append({
                "path": rel,
                "type": ptype,
                "title": meta.get("title", md_file.stem),
                "frontmatter": meta,
                "body": body,
            })
        except Exception as exc:
            logger.warning("Failed to pack %s: %s", md_file, exc)

    judgments = _load_judgments(wiki_root)
    relations = _extract_entity_relations(wiki_root)

    total_pages = len(pages)
    delta_pct = (
        abs(total_pages - previous_count) / max(previous_count, 1) * 100
        if previous_count > 0
        else 100.0
    )
    version = _auto_bump_version(previous_version, delta_pct)

    pack_data = {
        "meta": {
            "wiki_name": wiki_name,
            "version": version,
            "created_by": "ROSClaw Wiki v1.0",
            "created_at": datetime.now().isoformat(),
            "pack_format_version": _PACK_FORMAT_VERSION,
            "total_pages": total_pages,
            "total_entities": categories.get("entity", 0),
            "total_algorithms": categories.get("algorithm", 0),
            "total_concepts": categories.get("concept", 0),
            "total_skills": categories.get("skill", 0),
            "total_judgments": len(judgments),
            "git_commit": _get_git_commit(wiki_root),
        },
        "pages": pages,
        "judgments": judgments,
        "entity_relations": relations,
        "index": {
            "entities": [
                {"name": p["title"], "path": p["path"], "summary": ""}
                for p in pages if p["type"] == "entity"
            ],
            "algorithms": [
                {"name": p["title"], "path": p["path"], "summary": ""}
                for p in pages if p["type"] == "algorithm"
            ],
            "concepts": [
                {"name": p["title"], "path": p["path"], "summary": ""}
                for p in pages if p["type"] == "concept"
            ],
        },
    }

    out_path.write_text(
        json.dumps(pack_data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    logger.info("Wiki pack written: %s (%d pages, %d judgments)", out_path, total_pages, len(judgments))

    return {
        "status": "done",
        "output_path": str(out_path),
        "version": version,
        "total_pages": total_pages,
        "total_judgments": len(judgments),
        "total_relations": len(relations),
    }


def wiki_unpack(
    pack_path: str,
    target_wiki_root: str,
    merge_mode: str = "skip_existing",
) -> dict[str, Any]:
    """Unpack a wiki pack into a target wiki directory.

    Args:
        pack_path: Path to wiki_pack.json.
        target_wiki_root: Target wiki root directory.
        merge_mode: "skip_existing" | "overwrite" | "ask".

    Returns:
        Dict with merge summary.
    """
    if merge_mode not in MERGE_MODES:
        return {"status": "error", "message": f"Invalid merge_mode: {merge_mode}"}

    pack_file = Path(pack_path)
    if not pack_file.exists():
        return {"status": "error", "message": f"Pack not found: {pack_path}"}

    try:
        pack_data = json.loads(pack_file.read_text(encoding="utf-8"))
    except Exception as exc:
        return {"status": "error", "message": f"Failed to parse pack: {exc}"}

    target = Path(target_wiki_root)
    target.mkdir(parents=True, exist_ok=True)

    stats = {"pages_created": 0, "pages_skipped": 0, "pages_overwritten": 0, "judgments_merged": 0}

    # Unpack pages
    for page in pack_data.get("pages", []):
        rel_path = page["path"]
        target_file = target / rel_path
        target_file.parent.mkdir(parents=True, exist_ok=True)

        if target_file.exists():
            if merge_mode == "skip_existing":
                stats["pages_skipped"] += 1
                continue
            if merge_mode == "overwrite":
                stats["pages_overwritten"] += 1
            elif merge_mode == "ask":
                # In non-interactive mode, default to skip
                stats["pages_skipped"] += 1
                continue

        content = engine.write_frontmatter(page["frontmatter"], page["body"])
        target_file.write_text(content, encoding="utf-8")
        stats["pages_created"] += 1

    # Unpack judgments
    judgments = pack_data.get("judgments", [])
    if judgments:
        judgments_dir = target / "judgments"
        judgments_dir.mkdir(parents=True, exist_ok=True)

        # Write to index.json
        from judgment_generator import _build_index_data
        from judgment_generator import Judgment

        judgment_objects = []
        for j in judgments:
            judgment_objects.append(
                Judgment(
                    context=j.get("context", "general"),
                    entity=j.get("entity", ""),
                    parameter=j.get("parameter", ""),
                    recommended_value=j.get("recommended_value", ""),
                    unit=j.get("unit", ""),
                    confidence=j.get("confidence", 0.5),
                    sources=j.get("sources", []),
                    conflicts_resolved=j.get("conflicts_resolved", []),
                    usage_notes=j.get("usage_notes", ""),
                    unresolved=j.get("unresolved", False),
                )
            )

        index_data = _build_index_data(judgment_objects)
        index_path = judgments_dir / "index.json"
        index_path.write_text(
            json.dumps(index_data, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        stats["judgments_merged"] = len(judgments)

    engine.append_log(
        target_wiki_root,
        f"wiki_hub | unpack | {stats['pages_created']} created, {stats['pages_skipped']} skipped, {stats['judgments_merged']} judgments"
    )

    return {"status": "done", "merge_mode": merge_mode, **stats}


def wiki_diff(
    pack_a: str,
    pack_b: str | None = None,
    wiki_root: str | None = None,
) -> dict[str, Any]:
    """Compare two packs or a pack vs local wiki.

    Args:
        pack_a: Path to first wiki_pack.json.
        pack_b: Path to second pack. If None, compares pack_a against wiki_root.
        wiki_root: Local wiki root (used when pack_b is None).

    Returns:
        Dict with new_pages, updated_pages, missing_pages, conflicting_judgments.
    """
    try:
        data_a = json.loads(Path(pack_a).read_text(encoding="utf-8"))
    except Exception as exc:
        return {"status": "error", "message": f"Failed to load pack_a: {exc}"}

    if pack_b:
        try:
            data_b = json.loads(Path(pack_b).read_text(encoding="utf-8"))
        except Exception as exc:
            return {"status": "error", "message": f"Failed to load pack_b: {exc}"}
    elif wiki_root:
        # Pack the local wiki in-memory
        result = wiki_pack("local", wiki_root, output_path=None)
        if result["status"] != "done":
            return {"status": "error", "message": "Failed to pack local wiki"}
        local_pack_path = result["output_path"]
        data_b = json.loads(Path(local_pack_path).read_text(encoding="utf-8"))
    else:
        return {"status": "error", "message": "Either pack_b or wiki_root is required"}

    pages_a = {p["path"]: p for p in data_a.get("pages", [])}
    pages_b = {p["path"]: p for p in data_b.get("pages", [])}

    new_pages = [path for path in pages_b if path not in pages_a]
    missing_pages = [path for path in pages_a if path not in pages_b]
    updated_pages = []
    for path in pages_a:
        if path in pages_b:
            if pages_a[path]["body"] != pages_b[path]["body"]:
                updated_pages.append(path)

    judgments_a = {
        (j.get("entity"), j.get("context"), j.get("parameter")): j
        for j in data_a.get("judgments", [])
    }
    judgments_b = {
        (j.get("entity"), j.get("context"), j.get("parameter")): j
        for j in data_b.get("judgments", [])
    }

    conflicting_judgments = []
    for key, j_b in judgments_b.items():
        if key in judgments_a:
            j_a = judgments_a[key]
            if j_a.get("recommended_value") != j_b.get("recommended_value"):
                conflicting_judgments.append({
                    "entity": key[0],
                    "context": key[1],
                    "parameter": key[2],
                    "old_value": j_a.get("recommended_value"),
                    "new_value": j_b.get("recommended_value"),
                })

    return {
        "status": "done",
        "new_pages": new_pages,
        "updated_pages": updated_pages,
        "missing_pages": missing_pages,
        "conflicting_judgments": conflicting_judgments,
        "summary": {
            "new": len(new_pages),
            "updated": len(updated_pages),
            "missing": len(missing_pages),
            "judgment_conflicts": len(conflicting_judgments),
        },
    }


def wiki_pull(
    source_url: str,
    target_wiki_root: str,
    merge_mode: str = "skip_existing",
) -> dict[str, Any]:
    """Download a wiki pack from a URL and merge it into the local wiki.

    Args:
        source_url: URL to a wiki_pack.json file.
        target_wiki_root: Local wiki root directory.
        merge_mode: "skip_existing" | "overwrite" | "ask".

    Returns:
        Dict with merge summary.
    """
    import urllib.request

    try:
        with tempfile.NamedTemporaryFile(mode="w+b", delete=False, suffix=".json") as tmp:
            with urllib.request.urlopen(source_url, timeout=30) as resp:
                tmp.write(resp.read())
                tmp_path = tmp.name
    except Exception as exc:
        return {"status": "error", "message": f"Failed to download pack: {exc}"}

    result = wiki_unpack(tmp_path, target_wiki_root, merge_mode)
    Path(tmp_path).unlink(missing_ok=True)
    return result


# ── MCP-facing tools ──


def pack_wiki(wiki_name: str, output_path: str | None = None, wiki_root: str | None = None) -> dict[str, Any]:
    """MCP tool: pack the local wiki."""
    if wiki_root is None:
        return {"status": "error", "message": "wiki_root is required"}
    return wiki_pack(wiki_name, wiki_root, output_path)


def pull_wiki(source_url: str, merge_mode: str = "skip_existing", wiki_root: str | None = None) -> dict[str, Any]:
    """MCP tool: pull a remote wiki pack."""
    if wiki_root is None:
        return {"status": "error", "message": "wiki_root is required"}
    return wiki_pull(source_url, wiki_root, merge_mode)


def diff_with_pack(pack_path: str, wiki_root: str | None = None) -> dict[str, Any]:
    """MCP tool: compare local wiki with a pack."""
    if wiki_root is None:
        return {"status": "error", "message": "wiki_root is required"}
    return wiki_diff(pack_path, pack_b=None, wiki_root=wiki_root)


__all__ = [
    "wiki_pack",
    "wiki_unpack",
    "wiki_diff",
    "wiki_pull",
    "pack_wiki",
    "pull_wiki",
    "diff_with_pack",
    "MERGE_MODES",
]
