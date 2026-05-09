"""ROSClaw Conflict Resolution Engine — weighted adjudication of knowledge conflicts.

Resolves parameter/value conflicts using:
  - Source authority weighting
  - Recency decay (exponential, 2-year half-life)
  - Majority validation
  - Multi-round extraction stability (H800 compute)

Writes adjudicated results back to page sections.
"""

from __future__ import annotations

import json
import logging
import math
import re
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

import wiki_engine as engine

logger = logging.getLogger("rosclaw.conflict_resolver")

# ── Authority Weights ──
AUTHORITY_WEIGHTS: dict[str, float] = {
    "official_manual": 1.0,
    "official": 1.0,
    "arxiv_paper": 0.8,
    "paper": 0.8,
    "peer_reviewed": 0.85,
    "blog_post": 0.5,
    "blog": 0.5,
    "article": 0.5,
    "unknown": 0.5,
}

# Recency: exponential decay with 2-year half-life
_RECENCY_HALFLIFE_DAYS = 730

# Adjudication threshold: top score must exceed runner-up by this much
_RESOLUTION_GAP_THRESHOLD = 0.3

# Regex to parse conflict lines in "### 待核实冲突" section (legacy format)
_CONFLICT_LINE_RE = re.compile(
    r"^\s*-\s*\*\*(.+?)\*\*\s*—\s*old:\s*`(.+?)`\s*\(from\s+(.+?)\)\s+vs\s+new:\s*`(.+?)`\s*\(from\s+(.+?)\)"
)

# Regex to parse CONFLICT_START...CONFLICT_END blocks (Phase 9 structured format)
_CONFLICT_BLOCK_RE = re.compile(
    r"CONFLICT_START\n"
    r"field:\s*(.+?)\n"
    r"old_value:\s*(.+?)\s*\|\s*old_source:\s*(.+?)\n"
    r"new_value:\s*(.+?)\s*\|\s*new_source:\s*(.+?)\n"
    r"CONFLICT_END",
    re.MULTILINE,
)

# Regex to find already-resolved conflicts (to avoid re-processing)
_RESOLVED_HEADER = "### 已裁决冲突"
_PENDING_HEADER = "### 待核实冲突"


@dataclass
class Claim:
    """A single claim about a parameter value."""

    field: str
    value: str
    source: str
    date: datetime | None = None
    extraction_stable: bool = True  # False if multi-round validation failed


@dataclass
class Adjudication:
    """Result of adjudicating a single field's conflicting claims."""

    field: str
    winner_value: str
    winner_score: float
    runner_up_value: str | None
    runner_up_score: float
    resolved: bool  # True if gap > threshold
    reasoning: str
    claims: list[Claim] = field(default_factory=list)
    merge_logs: list[dict[str, Any]] = field(default_factory=list)
    resolution_method: str = "authority_weighted"  # or "resolved_by_tolerance", "unanimous"


def _parse_source_type(source_str: str) -> str:
    """Map a raw source string to canonical source type."""
    s = source_str.lower().strip()
    if "official" in s or "manual" in s:
        return "official_manual"
    if "arxiv" in s or "paper" in s or "journal" in s:
        return "arxiv_paper"
    if "blog" in s:
        return "blog_post"
    return "unknown"


def _authority_score(source_type: str) -> float:
    """Return authority weight for a source type."""
    return AUTHORITY_WEIGHTS.get(source_type, 0.5)


def _recency_score(date: datetime | None, reference: datetime | None = None) -> float:
    """Compute recency score using exponential decay.

    Half-life = 2 years (730 days). Recent dates score near 1.0;
    very old dates approach 0.0.
    """
    if date is None:
        return 0.5  # neutral when date unknown
    ref = reference or datetime.now()
    days = (ref - date).days
    if days < 0:
        days = 0
    # decay factor: 2^(-days / halflife)
    decay = math.pow(2.0, -days / _RECENCY_HALFLIFE_DAYS)
    return decay


def _weighted_score(authority: float, recency: float) -> float:
    """Combine authority and recency into final score."""
    return authority * 0.6 + recency * 0.4


def _parse_conflict_lines(body: str) -> dict[str, list[Claim]]:
    """Extract conflict claims from the ### 待核实冲突 section.

    Supports both Phase 9 structured format (CONFLICT_START/END blocks)
    and legacy line format. Returns dict mapping field_name -> list of Claim objects.
    """
    claims_by_field: dict[str, list[Claim]] = {}

    # Phase 9: Try structured CONFLICT_START/END blocks first
    block_matches = list(_CONFLICT_BLOCK_RE.finditer(body))
    if block_matches:
        for m in block_matches:
            field, old_val, old_src, new_val, new_src = m.groups()
            field = field.strip()
            old_val = old_val.strip()
            old_src = old_src.strip()
            new_val = new_val.strip()
            new_src = new_src.strip()
            # old claim
            claims_by_field.setdefault(field, []).append(
                Claim(field=field, value=old_val, source=old_src)
            )
            # new claim
            claims_by_field.setdefault(field, []).append(
                Claim(field=field, value=new_val, source=new_src)
            )
        return claims_by_field

    # Legacy: fall back to line-by-line parsing
    in_conflict_section = False
    for line in body.splitlines():
        if line.strip().startswith(_PENDING_HEADER):
            in_conflict_section = True
            continue
        if in_conflict_section:
            # Stop at next header
            if line.startswith("#"):
                break
            m = _CONFLICT_LINE_RE.match(line)
            if m:
                field, old_val, old_src, new_val, new_src = m.groups()
                # old claim
                claims_by_field.setdefault(field, []).append(
                    Claim(field=field, value=old_val, source=old_src)
                )
                # new claim
                claims_by_field.setdefault(field, []).append(
                    Claim(field=field, value=new_val, source=new_src)
                )
    return claims_by_field


def _group_claims_by_value(claims: list[Claim]) -> dict[str, list[Claim]]:
    """Group claims by their asserted value."""
    groups: dict[str, list[Claim]] = {}
    for c in claims:
        groups.setdefault(c.value, []).append(c)
    return groups


def _majority_boost(claims_for_value: list[Claim], total_claims: int) -> float:
    """Return a confidence boost when a majority of sources agree."""
    count = len(claims_for_value)
    if total_claims >= 3 and count >= math.ceil(total_claims / 2):
        return 0.1  # majority consensus bonus
    if total_claims == 2 and count == 2:
        return 0.05  # unanimous
    return 0.0


# ── Value equivalence with tolerance ──

_VALUE_NUM_RE = re.compile(r"[-+]?\d*\.?\d+")


def _are_values_equivalent(val_a: str, val_b: str, tolerance: float = 0.05) -> bool:
    """Check if two values are equivalent within relative tolerance.

    Extracts numeric parts from strings like "237 N·m" and "236.5 Nm",
    then checks if abs(a - b) / max(|a|, |b|) < tolerance.
    """
    nums_a = _VALUE_NUM_RE.findall(val_a)
    nums_b = _VALUE_NUM_RE.findall(val_b)

    if not nums_a or not nums_b:
        return False

    try:
        a = float(nums_a[0])
        b = float(nums_b[0])
    except ValueError:
        return False

    if a == b:
        return True

    max_val = max(abs(a), abs(b))
    if max_val == 0:
        return True

    relative_diff = abs(a - b) / max_val
    return relative_diff < tolerance


def _merge_equivalent_claims(claims: list[Claim], tolerance: float = 0.05) -> tuple[list[Claim], list[dict[str, Any]]]:
    """Merge claims whose values are numerically equivalent within tolerance.

    Returns:
        (merged_claims, merge_log_entries)
    """
    if not claims:
        return [], []

    merged: list[Claim] = []
    merge_logs: list[dict[str, Any]] = []
    consumed: set[int] = set()

    for i, c1 in enumerate(claims):
        if i in consumed:
            continue
        group = [c1]
        consumed.add(i)
        for j, c2 in enumerate(claims):
            if j in consumed or j == i:
                continue
            if _are_values_equivalent(c1.value, c2.value, tolerance):
                group.append(c2)
                consumed.add(j)

        if len(group) > 1:
            # Merge: keep the most authoritative source type as the representative value
            best = max(group, key=lambda c: _authority_score(_parse_source_type(c.source)))
            merged_claim = Claim(
                field=best.field,
                value=best.value,
                source=best.source,
                date=best.date,
                extraction_stable=all(c.extraction_stable for c in group),
            )
            merged.append(merged_claim)
            # Log the merge
            values = [c.value for c in group]
            sources = [c.source for c in group]
            nums = [_VALUE_NUM_RE.findall(v)[0] for v in values if _VALUE_NUM_RE.findall(v)]
            if len(nums) >= 2:
                try:
                    a, b = float(nums[0]), float(nums[1])
                    max_val = max(abs(a), abs(b))
                    diff = abs(a - b) / max_val if max_val else 0.0
                except ValueError:
                    diff = 0.0
            else:
                diff = 0.0
            merge_logs.append({
                "field": best.field,
                "values": values,
                "sources": sources,
                "relative_diff": round(diff, 4),
                "reason": f"relative_diff < {tolerance * 100:.0f}%",
            })
        else:
            merged.append(c1)

    return merged, merge_logs


def adjudicate_field(field: str, claims: list[Claim]) -> Adjudication:
    """Adjudicate a single field's conflicting claims.

    Returns Adjudication with winner, scores, and reasoning.
    """
    if not claims:
        return Adjudication(
            field=field,
            winner_value="",
            winner_score=0.0,
            runner_up_value=None,
            runner_up_score=0.0,
            resolved=False,
            reasoning="No claims to adjudicate.",
        )

    # Phase 8: merge numerically equivalent values before adjudication
    claims, merge_logs = _merge_equivalent_claims(claims)

    # If only one unique value after tolerance merge, auto-resolve
    unique_values = {c.value for c in claims}
    if len(unique_values) == 1:
        reasoning = "All sources agree on the value."
        resolution_method = "unanimous"
        if merge_logs:
            log = merge_logs[0]
            reasoning = (
                f"Resolved by tolerance merge: values {log['values']} are equivalent "
                f"({log['reason']}, relative_diff={log['relative_diff']})."
            )
            resolution_method = "resolved_by_tolerance"
        return Adjudication(
            field=field,
            winner_value=claims[0].value,
            winner_score=1.0,
            runner_up_value=None,
            runner_up_score=0.0,
            resolved=True,
            reasoning=reasoning,
            claims=claims,
            merge_logs=merge_logs,
            resolution_method=resolution_method,
        )

    # Score each value
    value_scores: dict[str, float] = {}
    value_reasons: dict[str, list[str]] = {}
    total_claims = len(claims)

    value_groups = _group_claims_by_value(claims)
    for value, value_claims in value_groups.items():
        score = 0.0
        reasons: list[str] = []
        for claim in value_claims:
            src_type = _parse_source_type(claim.source)
            auth = _authority_score(src_type)
            rec = _recency_score(claim.date)
            if not claim.extraction_stable:
                auth *= 0.7  # penalize unstable extractions
                reasons.append(f"{claim.source}: unstable extraction (penalized)")
            val_score = _weighted_score(auth, rec)
            score += val_score
            reasons.append(
                f"{claim.source}: authority={auth:.2f}, recency={rec:.2f}, weighted={val_score:.2f}"
            )

        # Apply majority boost
        boost = _majority_boost(value_claims, total_claims)
        if boost > 0:
            score += boost
            reasons.append(f"majority boost: +{boost:.2f}")

        value_scores[value] = score
        value_reasons[value] = reasons

    # Rank values by score
    ranked = sorted(value_scores.items(), key=lambda x: x[1], reverse=True)
    winner_value, winner_score = ranked[0]
    runner_up_value = None
    runner_up_score = 0.0
    if len(ranked) > 1:
        runner_up_value, runner_up_score = ranked[1]

    gap = winner_score - runner_up_score
    resolved = gap > _RESOLUTION_GAP_THRESHOLD

    reasoning_lines = [
        f"Field '{field}': {len(claims)} claim(s) across {len(unique_values)} value(s).",
        f"Winner: `{winner_value}` (score={winner_score:.2f})",
    ]
    if runner_up_value is not None:
        reasoning_lines.append(f"Runner-up: `{runner_up_value}` (score={runner_up_score:.2f})")
        reasoning_lines.append(f"Gap: {gap:.2f} (threshold={_RESOLUTION_GAP_THRESHOLD:.2f})")
    for value, reasons in value_reasons.items():
        reasoning_lines.append(f"  Value `{value}`:")
        for r in reasons:
            reasoning_lines.append(f"    - {r}")
    if resolved:
        reasoning_lines.append("Result: RESOLVED — winner exceeds threshold.")
    else:
        reasoning_lines.append("Result: UNRESOLVED — scores too close to call.")

    # Determine resolution method
    resolution_method = "authority_weighted"
    if resolved and merge_logs:
        resolution_method = "resolved_by_tolerance"

    return Adjudication(
        field=field,
        winner_value=winner_value,
        winner_score=winner_score,
        runner_up_value=runner_up_value,
        runner_up_score=runner_up_score,
        resolved=resolved,
        reasoning="\n".join(reasoning_lines),
        claims=claims,
        merge_logs=merge_logs,
        resolution_method=resolution_method,
    )


def resolve_page_conflicts(page_path: str) -> list[Adjudication]:
    """Read a page, adjudicate all pending conflicts, return results.

    Does NOT write back to the page — caller decides.
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

    claims_by_field = _parse_conflict_lines(body)
    if not claims_by_field:
        return []

    results: list[Adjudication] = []
    for field, claims in claims_by_field.items():
        adj = adjudicate_field(field, claims)
        results.append(adj)

    return results


def write_adjudication_to_page(page_path: str, adjudications: list[Adjudication]) -> None:
    """Append or update the ### 已裁决冲突 section on a page.

    Also updates the ### 待核实冲突 section to mark resolved items.
    """
    if not adjudications:
        return

    path = Path(page_path)
    try:
        content = path.read_text(encoding="utf-8")
        meta, body = engine.parse_frontmatter(content)
    except Exception:
        return

    # Build adjudication section
    lines: list[str] = []
    lines.append(f"\n{_RESOLVED_HEADER}\n")
    lines.append("_These conflicts were adjudicated by the conflict resolution engine._\n")

    unresolved_items: list[str] = []
    resolved_items: list[str] = []

    for adj in adjudications:
        if adj.resolved:
            resolved_items.append(
                f"- **{adj.field}** → `{adj.winner_value}` (confidence: {adj.winner_score:.2f})\n"
            )
            resolved_items.append(f"  - Reasoning: {adj.reasoning.split(chr(10))[0]}\n")
        else:
            unresolved_items.append(
                f"- **{adj.field}** — status: `unresolved`, pending_human_review\n"
            )
            unresolved_items.append(f"  - Best candidate: `{adj.winner_value}` ({adj.winner_score:.2f})\n")
            if adj.runner_up_value:
                unresolved_items.append(
                    f"  - Runner-up: `{adj.runner_up_value}` ({adj.runner_up_score:.2f})\n"
                )

    if resolved_items:
        lines.append("**Resolved:**\n")
        lines.extend(resolved_items)

    if unresolved_items:
        lines.append("**Still unresolved:**\n")
        lines.extend(unresolved_items)

    # Replace existing resolved section or append
    if _RESOLVED_HEADER in body:
        # Simple replacement: find section and replace to end of file or next top-level header
        pattern = re.compile(
            rf"({_RESOLVED_HEADER}\n)(.*?)(?=\n#{1,3}\s|\Z)", re.DOTALL
        )
        new_section = "".join(lines)
        body = pattern.sub(new_section, body)
    else:
        body = body.rstrip() + "\n" + "".join(lines)

    new_content = engine.write_frontmatter(meta, body)
    path.write_text(new_content, encoding="utf-8")
    logger.info("Wrote adjudication to %s (%d resolved, %d unresolved)", page_path, len(resolved_items), len(unresolved_items))


def resolve_conflicts(entity_name: str, wiki_root: str) -> dict[str, Any]:
    """MCP-facing tool: resolve all pending conflicts for a given entity.

    Args:
        entity_name: Title or slug of the entity page.
        wiki_root: Root directory of the wiki.

    Returns:
        Dict with adjudication results.
    """
    # Find the page
    root = Path(wiki_root)
    page_path: Path | None = None

    # Try slug match first
    slug = engine.generate_page_id(entity_name)
    for md_file in root.rglob("*.md"):
        if md_file.stem == slug:
            page_path = md_file
            break

    if not page_path:
        return {"status": "not_found", "entity": entity_name, "adjudications": []}

    adjudications = resolve_page_conflicts(str(page_path))
    if not adjudications:
        return {"status": "no_conflicts", "entity": entity_name, "adjudications": []}

    write_adjudication_to_page(str(page_path), adjudications)

    resolved_count = sum(1 for a in adjudications if a.resolved)
    unresolved_count = len(adjudications) - resolved_count

    # Log tolerance merges
    for adj in adjudications:
        for log in adj.merge_logs:
            engine.append_log(
                wiki_root,
                f"tolerance-merge | field: {log['field']} | values: {log['values']} | reason: {log['reason']}"
            )

    # Log to wiki log
    engine.append_log(
        wiki_root,
        f"conflict_resolver | resolved={resolved_count}, unresolved={unresolved_count} | [[{entity_name}]]"
    )

    # Phase 8: emit conflict resolution complete event
    try:
        import event_bus
        event_bus.emit(
            "conflict_resolution_complete",
            {
                "entity": entity_name,
                "resolved": resolved_count,
                "unresolved": unresolved_count,
                "timestamp": datetime.now().isoformat(),
            },
        )
    except Exception:
        pass

    return {
        "status": "adjudicated",
        "entity": entity_name,
        "page_path": str(page_path),
        "resolved_count": resolved_count,
        "unresolved_count": unresolved_count,
        "adjudications": [
            {
                "field": a.field,
                "winner_value": a.winner_value,
                "winner_score": round(a.winner_score, 2),
                "resolved": a.resolved,
                "reasoning": a.reasoning,
            }
            for a in adjudications
        ],
    }


def conflict_stats(wiki_root: str) -> dict[str, Any]:
    """MCP-facing tool: return global conflict statistics.

    Returns:
        Dict with total pages scanned, total conflicts, resolved, unresolved.
    """
    root = Path(wiki_root)
    total_pages = 0
    pages_with_conflicts = 0
    total_pending = 0
    total_resolved = 0

    for md_file in root.rglob("*.md"):
        if md_file.name in ("index.md", "log.md"):
            continue
        total_pages += 1
        try:
            content = md_file.read_text(encoding="utf-8")
            _, body = engine.parse_frontmatter(content)
        except Exception:
            continue

        if _PENDING_HEADER in body:
            pages_with_conflicts += 1
            # Rough count of conflict lines
            in_section = False
            for line in body.splitlines():
                if line.strip().startswith(_PENDING_HEADER):
                    in_section = True
                    continue
                if in_section and line.startswith("#"):
                    break
                if in_section and line.strip().startswith("-"):
                    total_pending += 1

        if _RESOLVED_HEADER in body:
            in_section = False
            for line in body.splitlines():
                if line.strip().startswith(_RESOLVED_HEADER):
                    in_section = True
                    continue
                if in_section and line.startswith("#"):
                    break
                if in_section and line.strip().startswith("-") and "status: unresolved" not in line:
                    total_resolved += 1

    return {
        "status": "done",
        "total_pages": total_pages,
        "pages_with_conflicts": pages_with_conflicts,
        "total_pending_conflicts": total_pending,
        "total_resolved_conflicts": total_resolved,
    }


# ── Multi-round extraction validation (H800 compute) ──

async def validate_extraction_stability(
    source_text: str,
    parameter: str,
    llm_func: Any,
    temperatures: list[float] | None = None,
) -> dict[str, Any]:
    """Run multi-round extraction with varying temperatures to test stability.

    Args:
        source_text: The text to extract from.
        parameter: The parameter to extract.
        llm_func: Async function accepting (prompt, temperature) -> extracted_value.
        temperatures: List of temperatures to use. Defaults to [0.0, 0.5, 1.0].

    Returns:
        Dict with stability assessment.
    """
    temps = temperatures or [0.0, 0.5, 1.0]
    results: list[dict[str, Any]] = []

    for temp in temps:
        prompt = (
            f"Extract the exact value of '{parameter}' from the following text. "
            f"Respond with ONLY the value, no explanation.\n\n{source_text}"
        )
        try:
            value = await llm_func(prompt, temperature=temp)
            results.append({"temperature": temp, "value": value.strip() if value else None})
        except Exception as exc:
            results.append({"temperature": temp, "value": None, "error": str(exc)})

    values = [r["value"] for r in results if r.get("value") is not None]
    unique_values = set(values)

    stable = len(unique_values) <= 1 and len(values) == len(temps)

    return {
        "parameter": parameter,
        "stable": stable,
        "unique_values": list(unique_values),
        "run_count": len(temps),
        "results": results,
        "recommendation": "trust" if stable else "reduce_authority",
    }
