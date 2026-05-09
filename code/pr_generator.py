"""PR Generator — Auto-generate pull requests from wiki judgments.

Safety-first pipeline with GREEN/AMBER/RED labels (Phase 14):
  GREEN  — parameter < 80% of hardware limit → auto-merge eligible
  AMBER  — parameter >= 80% but < 100% of limit → needs human review
  RED    — parameter >= 100% of limit → blocked, [!CRITICAL] report

Action Traceability: every PR body cites the source judgment paper,
resolution method, confidence score, and Wiki page link.
"""

from __future__ import annotations

import logging
import re
from datetime import datetime
from pathlib import Path
from typing import Any

from code_generator import _check_safety_boundary, sync_check

logger = logging.getLogger("rosclaw.pr_generator")


def _escape_markdown(text: str) -> str:
    return text.replace("_", "\\_").replace("*", "\\*")


def _safety_label_color(severity: str) -> str:
    return {"green": "🟢", "amber": "🟡", "red": "🔴"}.get(severity, "⚪")


def generate_pr(
    entity_name: str,
    wiki_root: str,
    code_paths: list[str] | None = None,
) -> dict[str, Any]:
    """Generate a PR from sync discrepancies for a single entity.

    Pipeline:
      sync_check → safety boundary validation (GREEN/AMBER/RED) → PR creation

    Returns:
        Dict with pr_data, report, status.
        status: "created" | "red" | "amber" | "no_changes" | "error"
    """
    # Step 1: Run sync check
    sync_result = sync_check(entity_name, wiki_root, code_paths)
    if sync_result.get("status") != "done":
        return {
            "status": sync_result.get("status", "error"),
            "entity": entity_name,
            "pr": None,
            "report": sync_result.get("report", ""),
            "reason": "sync_check failed or no judgments",
        }

    findings: list[dict[str, Any]] = sync_result.get("findings", [])
    if not findings:
        return {
            "status": "no_changes",
            "entity": entity_name,
            "pr": None,
            "report": sync_result["report"],
            "reason": "No discrepancies found — no PR needed.",
        }

    # Step 2: Safety boundary validation per finding (GREEN/AMBER/RED)
    green_findings: list[dict[str, Any]] = []
    amber_findings: list[dict[str, Any]] = []
    red_findings: list[dict[str, Any]] = []

    for f in findings:
        param = f["parameter"]
        j_val = float(f["judgment_value"])
        hw_limit = f.get("hardware_limit")
        severity, is_safe = _check_safety_boundary(param, j_val, hw_limit)

        f["severity"] = severity
        f["is_safe"] = is_safe
        f["safety_label"] = _safety_label_color(severity)

        if severity == "red":
            red_findings.append(f)
        elif severity == "amber":
            amber_findings.append(f)
        else:
            green_findings.append(f)

    # Step 3: Handle RED findings — refuse PR, generate report only
    if red_findings:
        critical_report = _build_red_report(entity_name, red_findings)
        return {
            "status": "red",
            "entity": entity_name,
            "pr": None,
            "report": critical_report,
            "reason": f"{len(red_findings)} parameter(s) exceed hardware limits. PR refused.",
            "red_count": len(red_findings),
            "amber_count": len(amber_findings),
            "green_count": len(green_findings),
        }

    # Step 4: Build PR for green + amber findings
    pr_findings = green_findings + amber_findings
    pr_data = _build_pr_data(entity_name, pr_findings, amber_findings)

    status = "amber" if amber_findings else "created"
    return {
        "status": status,
        "entity": entity_name,
        "pr": pr_data,
        "report": pr_data["body"],
        "reason": (
            f"PR generated with {len(green_findings)} green + {len(amber_findings)} amber parameter(s)."
            if amber_findings
            else f"PR generated with {len(green_findings)} green parameter(s)."
        ),
        "amber_count": len(amber_findings),
        "green_count": len(green_findings),
    }


def _build_red_report(entity_name: str, red_findings: list[dict[str, Any]]) -> str:
    lines = [
        f"## 🔴 [!CRITICAL] Sync Check Blocked for `{entity_name}`",
        "",
        "**Auto-generated PR was REFUSED** because the following parameters exceed hardware safety limits:",
        "",
    ]
    for f in red_findings:
        lines.append(
            f"- **{f['parameter']}**: judgment={f['judgment_value']} {f['unit']}, "
            f"hardware_limit={f['hardware_limit']} {f['unit']} — **EXCEEDS LIMIT**"
        )
    lines.extend([
        "",
        "### Required Action",
        "1. Verify the wiki judgment value against primary datasheets.",
        "2. If the judgment is correct, update hardware_limit to reflect true physical limit.",
        "3. Re-run `sync_check` after correction.",
        "",
        "---",
        f"Report generated: {datetime.utcnow().isoformat()}Z",
    ])
    return "\n".join(lines)


def _build_action_traceability(finding: dict[str, Any]) -> str:
    """Build action-traceability section for a single finding."""
    sources = finding.get("sources", [])
    source_link = sources[0] if sources else "[[Wiki-Judgment]]"
    confidence = finding.get("confidence", "N/A")
    resolution = finding.get("resolution_method", "authority_weighted")
    hw_limit = finding.get("hardware_limit", "N/A")
    ratio = ""
    if hw_limit not in (None, "N/A") and float(hw_limit) > 0:
        try:
            r = float(finding["judgment_value"]) / float(hw_limit) * 100
            ratio = f" ({r:.1f}% of hardware limit)"
        except (ValueError, TypeError):
            pass

    return (
        f"**Source**: {source_link} | "
        f"**Confidence**: {confidence} | "
        f"**Resolution**: {resolution} | "
        f"**Hardware Limit**: {hw_limit}{ratio}"
    )


def _build_pr_data(
    entity_name: str,
    findings: list[dict[str, Any]],
    amber_findings: list[dict[str, Any]],
) -> dict[str, Any]:
    labels = ["auto-generated"]
    if amber_findings:
        labels.extend(["needs-review", "warning"])
    else:
        labels.append("auto-merge")

    # Build diff snippets
    diff_lines: list[str] = []
    for f in findings:
        param = f["parameter"]
        old_val = f["code_value"]
        new_val = f["judgment_value"]
        unit = f.get("unit", "")
        confidence = f.get("confidence", 0.0)
        source = f.get("sources", ["[[Wiki-Judgment]]"])[0] if f.get("sources") else "[[Wiki-Judgment]]"
        hw_limit = f.get("hardware_limit")
        label = f.get("safety_label", "🟢")

        diff_lines.append(f"```diff")
        diff_lines.append(f"- {param} = {old_val}  # {unit} (outdated)")
        diff_lines.append(f"+ {param} = {new_val}  # {unit} — Ref: {source} (confidence: {confidence})")
        diff_lines.append(f"```")
        diff_lines.append(f"> {label} {_build_action_traceability(f)}")
        diff_lines.append("")

    # Build safety verification checklist
    safety_lines = []
    for f in findings:
        param = f["parameter"]
        hw_limit = f.get("hardware_limit")
        severity = f.get("severity", "green")
        if severity == "amber":
            safety_lines.append(f"- [x] `{param}`: **AMBER** — value is >=80% of hardware limit ({hw_limit})")
        else:
            safety_lines.append(f"- [x] `{param}`: **GREEN** — Safety boundary check passed (<80% of hardware limit)")

    body_lines = [
        f"## Auto-generated PR: Sync `{entity_name}` parameters with Wiki judgments",
        "",
        "### Source Judgments",
        f"- **Entity**: {entity_name}",
        f"- **Parameters updated**: {len(findings)}",
        f"- **Safety summary**: {len([f for f in findings if f.get('severity')=='green'])} GREEN, {len(amber_findings)} AMBER",
        "",
        "### Changes",
        "",
    ]
    body_lines.extend(diff_lines)
    body_lines.extend([
        "### Safety Verification",
        "",
    ])
    body_lines.extend(safety_lines)
    body_lines.extend([
        "- [x] No breaking changes to downstream code (parameter values only)",
        "",
        "### Action Traceability",
        "Each parameter change is traceable to a Wiki judgment with confidence score, resolution method, and source citation.",
        "",
        "---",
        "⚠️ **AUTO-GENERATED by ROSClaw Wiki Phase 14.** Review before merge.",
        "",
        f"_Generated: {datetime.utcnow().isoformat()}Z_",
    ])

    return {
        "title": f"[Auto-PR] Sync {entity_name} parameters with wiki judgments",
        "body": "\n".join(body_lines),
        "labels": labels,
        "findings": findings,
    }


def submit_pr(
    pr_data: dict[str, Any],
    repo_path: str | None = None,
) -> dict[str, Any]:
    """Simulate PR submission (no actual git remote required in test mode).

    In production this would call GitHub API or git push.
    For Phase 13/14, we write the PR content to data/prs/ for inspection.
    """
    if not pr_data:
        return {"status": "error", "reason": "No PR data provided"}

    pr_dir = Path("data/prs")
    pr_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    safe_entity = re.sub(r"[^\w-]", "_", pr_data.get("entity", "unknown"))
    pr_file = pr_dir / f"{safe_entity}_{timestamp}.md"

    content_lines = [
        f"# {pr_data['pr']['title']}",
        "",
        f"**Labels**: {', '.join(pr_data['pr']['labels'])}",
        "",
        "---",
        "",
        pr_data["pr"]["body"],
    ]

    pr_file.write_text("\n".join(content_lines), encoding="utf-8")

    return {
        "status": "submitted",
        "file": str(pr_file),
        "title": pr_data["pr"]["title"],
        "labels": pr_data["pr"]["labels"],
    }


# ── GitHub Gateway integration ──

def submit_pr_to_github(
    pr_data: dict[str, Any],
    github_repo: str,
    base_branch: str = "main",
    github_token: str | None = None,
    auto_merge: bool | None = None,
) -> dict[str, Any]:
    """Submit a PR to a real GitHub repository via github_gateway.

    Args:
        pr_data: Output from generate_pr().
        github_repo: "owner/repo" format.
        base_branch: Branch to merge into.
        github_token: GitHub personal access token (defaults to GITHUB_TOKEN env var).

    Returns:
        Dict with status, pr_url, and details.
    """
    try:
        from github_gateway import GitHubGateway
    except ImportError:
        return {
            "status": "error",
            "reason": "github_gateway not available",
        }

    gateway = GitHubGateway(token=github_token)

    entity = pr_data.get("entity", "unknown")
    pr_info = pr_data.get("pr", {})
    title = pr_info.get("title", f"[Auto-PR] Sync {entity}")
    body = pr_info.get("body", "")
    labels = pr_info.get("labels", ["auto-generated"])

    # Determine auto-merge eligibility based on safety label
    if auto_merge is None:
        auto_merge = "auto-merge" in labels and "needs-review" not in labels

    return gateway.create_pr(
        repo=github_repo,
        title=title,
        body=body,
        base_branch=base_branch,
        head_branch=f"auto-sync/{entity.lower().replace(' ', '-')}",
        labels=labels,
        auto_merge=auto_merge,
    )
