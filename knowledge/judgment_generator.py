"""ROSClaw Judgment Generator — turn resolved knowledge into actionable criteria.

Reads adjudicated conflicts and page content to produce structured judgments
that agents can consume directly. Each judgment includes:
  - recommended_value with confidence score
  - source citations
  - resolved conflicts (with reasoning)
  - usage_notes for contextual warnings

Inspired by GBrain's context routing and the "brain-first lookup protocol."
"""

from __future__ import annotations

import json
import logging
import re
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any

import wiki_engine as engine

logger = logging.getLogger("rosclaw.judgment_generator")

_JUDGMENTS_DIR = "judgments"

# Regex to extract parameter declarations from page body
# e.g., "Peak torque: 237 Nm" or "peak_torque = 237 Nm"
_PARAM_EXTRACT_RE = re.compile(
    r"(?i)(?:^|\n|\s)([\w\s_]+?)\s*[:=]\s*([0-9.]+)\s*([a-zA-Z°/%·]+)(?:\s|$|\n)",
    re.MULTILINE,
)

# Regex to read resolved conflicts from ### 已裁决冲突 section
_RESOLVED_LINE_RE = re.compile(
    r"^\s*-\s*\*\*(.+?)\*\*\s*→\s*`(.+?)`\s*\(confidence:\s*([0-9.]+)\)",
    re.MULTILINE,
)

# Regex to read unresolved conflicts
_UNRESOLVED_LINE_RE = re.compile(
    r"^\s*-\s*\*\*(.+?)\*\*\s*—\s*status:\s*`unresolved`",
    re.MULTILINE,
)

# Context inference: map tags/keywords to context names
_CONTEXT_KEYWORDS: dict[str, list[str]] = {
    "locomotion_control": ["torque", "speed", "gait", "walking", "velocity"],
    "manipulation": ["grasp", "gripper", "arm", "dexterity", "force"],
    "perception": ["vision", "lidar", "camera", "sensor", "detection"],
    "navigation": ["map", "path", "slam", "localization", "planning"],
    "safety": ["limit", "emergency", "collision", "shutdown", "threshold"],
    "power": ["battery", "voltage", "current", "watt", "power"],
}


@dataclass
class Judgment:
    """A structured judgment about a parameter for a specific context."""

    context: str
    entity: str
    parameter: str
    recommended_value: float | str
    unit: str
    confidence: float
    sources: list[str] = field(default_factory=list)
    conflicts_resolved: list[str] = field(default_factory=list)
    usage_notes: str = ""
    unresolved: bool = False
    hardware_limit: float | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "context": self.context,
            "entity": self.entity,
            "parameter": self.parameter,
            "recommended_value": self.recommended_value,
            "unit": self.unit,
            "confidence": round(self.confidence, 2),
            "sources": self.sources,
            "conflicts_resolved": self.conflicts_resolved,
            "usage_notes": self.usage_notes,
            "unresolved": self.unresolved,
            "hardware_limit": self.hardware_limit,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Judgment":
        return cls(
            context=data["context"],
            entity=data["entity"],
            parameter=data["parameter"],
            recommended_value=data["recommended_value"],
            unit=data["unit"],
            confidence=data["confidence"],
            sources=data.get("sources", []),
            conflicts_resolved=data.get("conflicts_resolved", []),
            usage_notes=data.get("usage_notes", ""),
            unresolved=data.get("unresolved", False),
            hardware_limit=data.get("hardware_limit"),
        )


def _infer_context(parameter: str, body: str, tags: list[str]) -> str:
    """Infer the operational context from parameter name, body text, and tags."""
    text = f"{parameter} {body} {' '.join(tags)}".lower()
    scores: dict[str, int] = {}
    for ctx, keywords in _CONTEXT_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw in text)
        if score > 0:
            scores[ctx] = score
    if scores:
        return max(scores.items(), key=lambda x: x[1])[0]
    return "general"


def _extract_unit(value_str: str) -> tuple[str | float, str]:
    """Split a value string like '237 Nm' into (237.0, 'Nm').

    Returns:
        (numeric_value_or_original_string, unit_string)
    """
    m = re.match(r"^([0-9.]+)\s*(.+)$", value_str.strip())
    if not m:
        return value_str, ""
    num_str, unit = m.groups()
    try:
        if "." in num_str:
            return float(num_str), unit.strip()
        return int(num_str), unit.strip()
    except ValueError:
        return value_str, unit.strip()


def _parse_resolved_conflicts(body: str) -> dict[str, dict[str, Any]]:
    """Parse the ### 已裁决冲突 section into a dict of field -> resolution info."""
    resolved: dict[str, dict[str, Any]] = {}
    in_section = False
    for line in body.splitlines():
        if line.strip().startswith("### 已裁决冲突"):
            in_section = True
            continue
        if in_section and line.startswith("#"):
            break
        if in_section:
            m = _RESOLVED_LINE_RE.match(line)
            if m:
                field, value, confidence = m.groups()
                resolved[field] = {
                    "value": value,
                    "confidence": float(confidence),
                }
    return resolved


def _parse_unresolved_conflicts(body: str) -> list[str]:
    """Parse the ### 已裁决冲突 section for still-unresolved fields."""
    unresolved: list[str] = []
    in_section = False
    for line in body.splitlines():
        if line.strip().startswith("### 已裁决冲突"):
            in_section = True
            continue
        if in_section and line.startswith("#"):
            break
        if in_section:
            m = _UNRESOLVED_LINE_RE.match(line)
            if m:
                unresolved.append(m.group(1))
    return unresolved


def _extract_sources_from_body(body: str) -> list[str]:
    """Find [[Page Title]] citations in body text."""
    citations: set[str] = set()
    for match in re.finditer(r"\[\[([^\]|]+)(?:\|[^\]]+)?\]\]", body):
        citations.add(f"[[{match.group(1).strip()}]]")
    return sorted(citations)


def generate_judgments_for_page(page_path: str, wiki_root: str) -> list[Judgment]:
    """Generate judgments for all adjudicated parameters on a page.

    Returns:
        List of Judgment objects.
    """
    path = Path(page_path)
    if not path.exists():
        return []

    try:
        content = path.read_text(encoding="utf-8")
        meta, body = engine.parse_frontmatter(content)
    except Exception as exc:
        logger.warning("Failed to parse %s: %s", page_path, exc)
        return []

    entity = meta.get("title", path.stem)
    tags = meta.get("tags", [])
    judgments: list[Judgment] = []

    # 1. From resolved conflicts
    resolved = _parse_resolved_conflicts(body)
    for field, info in resolved.items():
        context = _infer_context(field, body, tags)
        value, unit = _extract_unit(info["value"])
        sources = _extract_sources_from_body(body)
        judgments.append(
            Judgment(
                context=context,
                entity=entity,
                parameter=field,
                recommended_value=value,
                unit=unit,
                confidence=info["confidence"],
                sources=sources if sources else [f"[[{entity}]]"],
                conflicts_resolved=[f"Resolved via conflict resolver (score={info['confidence']})"],
            )
        )

    # 2. From unresolved conflicts — generate warning judgments
    unresolved = _parse_unresolved_conflicts(body)
    for field in unresolved:
        context = _infer_context(field, body, tags)
        judgments.append(
            Judgment(
                context=context,
                entity=entity,
                parameter=field,
                recommended_value="UNKNOWN",
                unit="",
                confidence=0.0,
                sources=[],
                conflicts_resolved=[],
                usage_notes="⚠️ This parameter has unresolved conflicts. Do not use for code generation.",
                unresolved=True,
            )
        )

    return judgments


def save_judgments(wiki_root: str, judgments: list[Judgment]) -> list[str]:
    """Save judgments to wiki/judgments/ as JSON files and update index.json.

    Returns:
        List of written file paths.
    """
    root = Path(wiki_root)
    judgments_dir = root / _JUDGMENTS_DIR
    judgments_dir.mkdir(parents=True, exist_ok=True)

    written: list[str] = []
    for j in judgments:
        filename = f"{engine.generate_page_id(j.entity)}_{j.context}.json"
        filepath = judgments_dir / filename

        # Merge with existing if present
        existing: list[dict[str, Any]] = []
        if filepath.exists():
            try:
                existing = json.loads(filepath.read_text(encoding="utf-8"))
            except Exception:
                existing = []

        # Replace judgment for same parameter if exists
        existing = [e for e in existing if e.get("parameter") != j.parameter]
        existing.append(j.to_dict())

        filepath.write_text(
            json.dumps(existing, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        written.append(str(filepath))

    # Phase 8: update unified index
    _update_index(wiki_root, judgments)

    return written


def _build_index_data(all_judgments: list[Judgment]) -> dict[str, Any]:
    """Build the unified index structure from a list of Judgments."""
    by_entity: dict[str, dict[str, dict[str, dict[str, Any]]]] = {}
    by_context: dict[str, dict[str, list[str]]] = {}

    for j in all_judgments:
        entity = j.entity
        context = j.context
        param = j.parameter

        by_entity.setdefault(entity, {}).setdefault(context, {})[param] = {
            "recommended_value": j.recommended_value,
            "confidence": j.confidence,
            "unit": j.unit,
            "hardware_limit": j.hardware_limit,
            "sources": j.sources,
            "conflicts_resolved": j.conflicts_resolved,
            "resolution_method": getattr(j, "resolution_method", "authority_weighted"),
            "usage_notes": j.usage_notes,
        }

        by_context.setdefault(context, {}).setdefault(entity, []).append(param)

    return {
        "version": "2.0.0",
        "generated_at": datetime.now().isoformat(),
        "total_judgments": len(all_judgments),
        "by_entity": by_entity,
        "by_context": by_context,
    }


def _update_index(wiki_root: str, new_judgments: list[Judgment]) -> None:
    """Incrementally update wiki/judgments/index.json with new judgments."""
    root = Path(wiki_root)
    index_path = root / _JUDGMENTS_DIR / "index.json"

    existing_judgments: list[Judgment] = []
    if index_path.exists():
        try:
            data = json.loads(index_path.read_text(encoding="utf-8"))
            for entity, contexts in data.get("by_entity", {}).items():
                for context, params in contexts.items():
                    for param, info in params.items():
                        existing_judgments.append(
                            Judgment(
                                context=context,
                                entity=entity,
                                parameter=param,
                                recommended_value=info["recommended_value"],
                                unit="",
                                confidence=info["confidence"],
                                sources=info.get("sources", []),
                                conflicts_resolved=info.get("conflicts_resolved", []),
                                usage_notes=info.get("usage_notes", ""),
                            )
                        )
        except Exception:
            pass

    # Merge: replace existing judgments for same entity+context+parameter
    key_to_judgment: dict[tuple[str, str, str], Judgment] = {}
    for j in existing_judgments:
        key_to_judgment[(j.entity, j.context, j.parameter)] = j
    for j in new_judgments:
        key_to_judgment[(j.entity, j.context, j.parameter)] = j

    merged = list(key_to_judgment.values())
    index_data = _build_index_data(merged)

    index_path.write_text(
        json.dumps(index_data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def rebuild_index(wiki_root: str) -> dict[str, Any]:
    """Rebuild the unified index from all individual judgment JSON files.

    Returns:
        Summary dict with count.
    """
    root = Path(wiki_root)
    judgments_dir = root / _JUDGMENTS_DIR
    all_judgments: list[Judgment] = []

    if judgments_dir.exists():
        for json_file in judgments_dir.glob("*.json"):
            if json_file.name == "index.json":
                continue
            try:
                data = json.loads(json_file.read_text(encoding="utf-8"))
                for item in data:
                    all_judgments.append(Judgment.from_dict(item))
            except Exception:
                continue

    index_data = _build_index_data(all_judgments)
    index_path = judgments_dir / "index.json"
    index_path.write_text(
        json.dumps(index_data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    return {
        "status": "done",
        "total_judgments": len(all_judgments),
        "index_path": str(index_path),
    }


def generate_all_judgments(wiki_root: str) -> dict[str, Any]:
    """Scan all wiki pages and generate judgments for any with resolved conflicts.

    Returns:
        Summary dict with counts and written paths.
    """
    root = Path(wiki_root)
    all_judgments: list[Judgment] = []
    pages_processed = 0

    for md_file in root.rglob("*.md"):
        if md_file.name in ("index.md", "log.md"):
            continue
        try:
            content = md_file.read_text(encoding="utf-8")
            if "### 已裁决冲突" not in content:
                continue
            judgments = generate_judgments_for_page(str(md_file), wiki_root)
            if judgments:
                all_judgments.extend(judgments)
                pages_processed += 1
        except Exception as exc:
            logger.warning("Failed to process %s: %s", md_file, exc)

    written = save_judgments(wiki_root, all_judgments)

    # Log
    engine.append_log(
        wiki_root,
        f"judgment_generator | {pages_processed} page(s), {len(all_judgments)} judgment(s)"
    )

    # Phase 8: emit judgment generation complete event
    try:
        import event_bus
        event_bus.emit(
            "judgment_generation_complete",
            {
                "pages_processed": pages_processed,
                "new_judgments": len(all_judgments),
                "timestamp": datetime.now().isoformat(),
            },
        )
    except Exception:
        pass

    return {
        "status": "done",
        "pages_processed": pages_processed,
        "judgments_generated": len(all_judgments),
        "written_paths": written,
    }


def _judgment_exists(entity: str, parameter: str, wiki_root: str) -> bool:
    """Check if a judgment already exists for entity+parameter."""
    index_data = _load_index(wiki_root)
    if index_data and "by_entity" in index_data:
        for ent_name, contexts in index_data["by_entity"].items():
            if ent_name == entity:
                for ctx, params in contexts.items():
                    if parameter in params:
                        return True
    return False


def scan_pages_for_parameters(wiki_root: str, min_confidence: float = 0.7) -> list[dict[str, Any]]:
    """Scan all wiki pages for extractable parameter declarations.

    Returns list of dicts with entity, parameter, value, unit, confidence, source_page.
    """
    root = Path(wiki_root)
    found: list[dict[str, Any]] = []

    for md_file in root.rglob("*.md"):
        if md_file.name in ("index.md", "log.md"):
            continue
        try:
            content = md_file.read_text(encoding="utf-8")
            meta, body = engine.parse_frontmatter(content)
            confidence = meta.get("confidence", 0.5)
            if confidence < min_confidence:
                continue

            entity = meta.get("title", md_file.stem)
            tags = meta.get("tags", [])
            sources = _extract_sources_from_body(body)
            if not sources:
                sources = [f"[[{entity}]]"]

            # Extract parameters from body
            seen: set[str] = set()
            for match in _PARAM_EXTRACT_RE.finditer(body):
                param_name = match.group(1).strip().replace(" ", "_")
                value_str = match.group(2).strip()
                unit = match.group(3).strip() if match.group(3) else ""

                # Skip if already has judgment
                if _judgment_exists(entity, param_name, wiki_root):
                    continue
                # Skip duplicates within same page
                key = f"{entity}:{param_name}"
                if key in seen:
                    continue
                seen.add(key)

                # Infer context
                context = _infer_context(param_name, body, tags)

                found.append({
                    "entity": entity,
                    "parameter": param_name,
                    "value": value_str,
                    "unit": unit,
                    "confidence": confidence,
                    "context": context,
                    "source_page": str(md_file),
                    "sources": sources,
                })
        except Exception as exc:
            logger.warning("Failed to scan %s: %s", md_file, exc)

    return found


def generate_judgment_from_scan(param_info: dict[str, Any], wiki_root: str) -> Judgment | None:
    """Create a Judgment from scanned parameter info and save it."""
    try:
        value, unit = _extract_unit(f"{param_info['value']} {param_info['unit']}")
    except Exception:
        value = param_info["value"]
        unit = param_info.get("unit", "")

    j = Judgment(
        context=param_info.get("context", "general"),
        entity=param_info["entity"],
        parameter=param_info["parameter"],
        recommended_value=value,
        unit=unit,
        confidence=param_info["confidence"],
        sources=param_info.get("sources", []),
        conflicts_resolved=["Auto-extracted from wiki page"],
        usage_notes=f"Auto-extracted from {Path(param_info['source_page']).name}",
    )

    save_judgments(wiki_root, [j])
    return j


# ── MCP-facing tools ──


def _load_index(wiki_root: str) -> dict[str, Any] | None:
    """Load wiki/judgments/index.json if it exists. Uses Redis/shared cache."""
    from cache_client import cache_get, cache_set

    candidates = [
        Path(wiki_root) / _JUDGMENTS_DIR / "index.json",
        Path("wiki") / _JUDGMENTS_DIR / "index.json",
    ]
    for index_path in candidates:
        if index_path.exists():
            try:
                cache_key = f"judgments:index:{index_path}"
                mtime = index_path.stat().st_mtime
                cached = cache_get(cache_key)
                if cached and cached.get("mtime") == mtime:
                    return cached.get("data")
                data = json.loads(index_path.read_text(encoding="utf-8"))
                cache_set(cache_key, {"mtime": mtime, "data": data}, ttl=600)
                return data
            except Exception:
                pass
    return None


def get_judgment(entity: str, context: str | None = None, wiki_root: str | None = None, limit: int = 50) -> dict[str, Any]:
    """Retrieve judgment(s) for a specific entity and optional context.

    Phase 8:优先从 index.json 读取。
    """
    if wiki_root is None:
        return {"status": "error", "message": "wiki_root is required"}

    # Phase 8: try unified index first
    index_data = _load_index(wiki_root)
    slug = engine.generate_page_id(entity)
    matches: list[dict[str, Any]] = []

    if index_data and "by_entity" in index_data:
        for ent_name, contexts in index_data["by_entity"].items():
            if ent_name == entity or engine.generate_page_id(ent_name) == slug:
                for ctx, params in contexts.items():
                    if context is None or ctx == context:
                        for param, info in params.items():
                            matches.append({
                                "context": ctx,
                                "entity": ent_name,
                                "parameter": param,
                                "recommended_value": info["recommended_value"],
                                "confidence": info["confidence"],
                                "unit": info.get("unit", ""),
                                "hardware_limit": info.get("hardware_limit"),
                                "sources": info.get("sources", []),
                                "conflicts_resolved": info.get("conflicts_resolved", []),
                                "resolution_method": info.get("resolution_method", "authority_weighted"),
                                "usage_notes": info.get("usage_notes", ""),
                            })

    if matches:
        matches.sort(key=lambda x: x["confidence"], reverse=True)
        total = len(matches)
        if limit > 0 and total > limit:
            matches = matches[:limit]
        return {
            "status": "found",
            "entity": entity,
            "context": context,
            "count": total,
            "returned": len(matches),
            "judgments": matches,
        }

    # Fallback to individual JSON files
    root = Path(wiki_root)
    judgments_dir = root / _JUDGMENTS_DIR
    judgment_matches: list[Judgment] = []

    if judgments_dir.exists():
        for json_file in judgments_dir.glob("*.json"):
            if json_file.name == "index.json":
                continue
            try:
                data = json.loads(json_file.read_text(encoding="utf-8"))
                for item in data:
                    j = Judgment.from_dict(item)
                    if j.entity == entity or engine.generate_page_id(j.entity) == slug:
                        if context is None or j.context == context:
                            judgment_matches.append(j)
            except Exception:
                continue

    # Fallback: scan pages directly
    if not judgment_matches:
        for md_file in root.rglob("*.md"):
            if md_file.name in ("index.md", "log.md"):
                continue
            try:
                meta, _ = engine.parse_frontmatter(md_file.read_text(encoding="utf-8"))
                title = meta.get("title", md_file.stem)
                if title == entity or engine.generate_page_id(title) == slug:
                    judgments = generate_judgments_for_page(str(md_file), wiki_root)
                    for j in judgments:
                        if context is None or j.context == context:
                            judgment_matches.append(j)
            except Exception:
                continue

    if not judgment_matches:
        return {"status": "not_found", "entity": entity, "context": context, "judgments": []}

    judgment_matches.sort(key=lambda j: j.confidence, reverse=True)
    return {
        "status": "found",
        "entity": entity,
        "context": context,
        "count": len(judgment_matches),
        "judgments": [j.to_dict() for j in judgment_matches],
    }


def list_judgments(context: str | None = None, wiki_root: str | None = None) -> dict[str, Any]:
    """List all judgments, optionally filtered by context.

    Phase 8:优先从 index.json 读取。
    """
    if wiki_root is None:
        return {"status": "error", "message": "wiki_root is required"}

    # Phase 8: try unified index first
    index_data = _load_index(wiki_root)
    matches: list[dict[str, Any]] = []

    if index_data and "by_entity" in index_data:
        for ent_name, contexts in index_data["by_entity"].items():
            for ctx, params in contexts.items():
                if context is None or ctx == context:
                    for param, info in params.items():
                        matches.append({
                            "context": ctx,
                            "entity": ent_name,
                            "parameter": param,
                            "recommended_value": info["recommended_value"],
                            "confidence": info["confidence"],
                            "unit": info.get("unit", ""),
                            "hardware_limit": info.get("hardware_limit"),
                            "sources": info.get("sources", []),
                            "conflicts_resolved": info.get("conflicts_resolved", []),
                            "resolution_method": info.get("resolution_method", "authority_weighted"),
                            "usage_notes": info.get("usage_notes", ""),
                        })

    if matches:
        matches.sort(key=lambda x: x["confidence"], reverse=True)
        return {
            "status": "done",
            "context": context,
            "count": len(matches),
            "judgments": matches,
        }

    # Fallback to individual JSON files
    root = Path(wiki_root)
    judgments_dir = root / _JUDGMENTS_DIR
    all_judgments: list[Judgment] = []

    if judgments_dir.exists():
        for json_file in judgments_dir.glob("*.json"):
            if json_file.name == "index.json":
                continue
            try:
                data = json.loads(json_file.read_text(encoding="utf-8"))
                for item in data:
                    j = Judgment.from_dict(item)
                    if context is None or j.context == context:
                        all_judgments.append(j)
            except Exception:
                continue

    all_judgments.sort(key=lambda j: j.confidence, reverse=True)
    return {
        "status": "done",
        "context": context,
        "count": len(all_judgments),
        "judgments": [j.to_dict() for j in all_judgments],
    }


def search_judgments(query: str, wiki_root: str | None = None) -> dict[str, Any]:
    """Search judgments by entity, context, parameter, or usage_notes.

    Phase 8 MCP tool: full-text search over the unified judgment index.
    """
    if wiki_root is None:
        return {"status": "error", "message": "wiki_root is required"}

    index_data = _load_index(wiki_root)
    query_lower = query.lower()
    matches: list[dict[str, Any]] = []

    if index_data and "by_entity" in index_data:
        for ent_name, contexts in index_data["by_entity"].items():
            for ctx, params in contexts.items():
                for param, info in params.items():
                    searchable = f"{ent_name} {ctx} {param} {info.get('usage_notes', '')}"
                    if query_lower in searchable.lower():
                        matches.append({
                            "context": ctx,
                            "entity": ent_name,
                            "parameter": param,
                            "recommended_value": info["recommended_value"],
                            "confidence": info["confidence"],
                            "unit": info.get("unit", ""),
                            "hardware_limit": info.get("hardware_limit"),
                            "sources": info.get("sources", []),
                            "conflicts_resolved": info.get("conflicts_resolved", []),
                            "resolution_method": info.get("resolution_method", "authority_weighted"),
                            "usage_notes": info.get("usage_notes", ""),
                        })

    matches.sort(key=lambda x: x["confidence"], reverse=True)
    return {
        "status": "done",
        "query": query,
        "count": len(matches),
        "judgments": matches,
    }


def export_judgments(format: str = "json", wiki_root: str | None = None) -> dict[str, Any]:
    """Export all judgments as JSON or Markdown.

    Phase 8 MCP tool.
    """
    if wiki_root is None:
        return {"status": "error", "message": "wiki_root is required"}

    index_data = _load_index(wiki_root)
    if not index_data:
        # Try rebuild from individual files
        rebuild_result = rebuild_index(wiki_root)
        if rebuild_result["status"] != "done":
            return {"status": "error", "message": "No judgments found"}
        index_data = _load_index(wiki_root)

    if format.lower() == "json":
        return {
            "status": "done",
            "format": "json",
            "data": index_data,
        }

    if format.lower() == "markdown":
        lines: list[str] = [
            "# Judgment Export",
            "",
            f"Generated at: {index_data.get('generated_at', 'unknown')}",
            f"Total judgments: {index_data.get('total_judgments', 0)}",
            "",
        ]
        by_entity = index_data.get("by_entity", {})
        for entity in sorted(by_entity.keys()):
            lines.append(f"## {entity}")
            lines.append("")
            for context in sorted(by_entity[entity].keys()):
                lines.append(f"### {context}")
                lines.append("")
                for param, info in by_entity[entity][context].items():
                    lines.append(f"- **{param}** → `{info['recommended_value']}` (confidence: {info['confidence']})")
                    if info.get("usage_notes"):
                        lines.append(f"  - {info['usage_notes']}")
                    lines.append("")
        return {
            "status": "done",
            "format": "markdown",
            "data": "\n".join(lines),
        }

    return {"status": "error", "message": f"Unknown format: {format}"}
