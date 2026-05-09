"""Code Watcher — Git change monitor for Phase 10.

Monitors data/raw/code/ repositories for new commits, auto-updates wiki pages,
and emits events via the event_bus.
"""

from __future__ import annotations

import json
import logging
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Any

logger = logging.getLogger("rosclaw.code_watcher")

_STATE_FILE = Path("data/code_watcher_state.json")


def _load_state() -> dict[str, Any]:
    """Load last-known commit hashes for each repo."""
    if _STATE_FILE.exists():
        return json.loads(_STATE_FILE.read_text(encoding="utf-8"))
    return {}


def _save_state(state: dict[str, Any]) -> None:
    """Persist watcher state."""
    _STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    _STATE_FILE.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")


def _git_latest_commit(repo_path: Path) -> str | None:
    """Get the latest commit hash for a repo."""
    try:
        result = subprocess.run(
            ["git", "-C", str(repo_path), "rev-parse", "HEAD"],
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        return None
    except FileNotFoundError:
        logger.warning("git not found")
        return None


def _git_pull(repo_path: Path) -> bool:
    """Pull latest changes. Returns True if successful."""
    try:
        subprocess.run(
            ["git", "-C", str(repo_path), "pull", "--ff-only"],
            capture_output=True,
            text=True,
            check=True,
        )
        return True
    except subprocess.CalledProcessError as exc:
        logger.warning("git pull failed for %s: %s", repo_path, exc.stderr)
        return False


def _git_diff_stats(repo_path: Path, old_commit: str) -> dict[str, Any]:
    """Get diff stats between old_commit and HEAD."""
    try:
        result = subprocess.run(
            ["git", "-C", str(repo_path), "diff", "--stat", f"{old_commit}..HEAD"],
            capture_output=True,
            text=True,
            check=True,
        )
        lines = result.stdout.strip().split("\n")
        files_changed = 0
        insertions = 0
        deletions = 0
        for line in lines:
            if "|" in line:
                files_changed += 1
                if "insertion" in line:
                    nums = [int(s) for s in line.split() if s.isdigit()]
                    if nums:
                        insertions += nums[-1]
                if "deletion" in line:
                    nums = [int(s) for s in line.split() if s.isdigit()]
                    if nums:
                        deletions += nums[-1]
        return {
            "files_changed": files_changed,
            "insertions": insertions,
            "deletions": deletions,
            "summary": lines[-1] if lines else "",
        }
    except subprocess.CalledProcessError:
        return {"files_changed": 0, "insertions": 0, "deletions": 0, "summary": ""}


def check_repos(code_root: str = "data/raw/code") -> dict[str, Any]:
    """Check all repos for changes and return a report.

    Returns:
        Dict with repos_checked, changed_repos (list), details.
    """
    root = Path(code_root)
    state = _load_state()
    changed: list[dict[str, Any]] = []
    checked = 0

    if not root.exists():
        return {"repos_checked": 0, "changed_repos": [], "details": {}}

    for repo_dir in root.iterdir():
        if not repo_dir.is_dir() or repo_dir.name.startswith("."):
            continue
        if not (repo_dir / ".git").exists():
            continue

        checked += 1
        repo_name = repo_dir.name
        latest = _git_latest_commit(repo_dir)
        if latest is None:
            continue

        old_commit = state.get(repo_name)
        if old_commit and old_commit != latest:
            stats = _git_diff_stats(repo_dir, old_commit)
            changed.append({
                "repo": repo_name,
                "old_commit": old_commit,
                "new_commit": latest,
                "stats": stats,
            })
            logger.info("Detected changes in %s: %s", repo_name, stats.get("summary", ""))

        state[repo_name] = latest

    _save_state(state)
    return {"repos_checked": checked, "changed_repos": changed, "details": {r["repo"]: r for r in changed}}


def sync_changed_repos(
    code_root: str = "data/raw/code",
    wiki_root: str = "wiki",
    auto_pull: bool = True,
) -> dict[str, Any]:
    """Detect changes, optionally pull, rebuild code graph, and emit events.

    Returns:
        Summary dict with pulled, scanned, events_emitted.
    """
    import code_knowledge_graph as ckg
    import code_repo_scanner as crs

    report = check_repos(code_root)
    pulled: list[str] = []
    scanned: list[str] = []
    events: list[dict[str, Any]] = []

    for change in report["changed_repos"]:
        repo_name = change["repo"]
        repo_path = Path(code_root) / repo_name

        if auto_pull:
            if _git_pull(repo_path):
                pulled.append(repo_name)

        # Rebuild code graph
        try:
            graph = ckg.scan_repo(repo_path, repo_name)
            scanned.append(repo_name)
        except Exception as exc:
            logger.warning("Code graph scan failed for %s: %s", repo_name, exc)
            continue

        # Check for function signature changes
        _check_signature_changes(repo_path, repo_name, wiki_root, change, events)

        # Emit event
        try:
            import event_bus
            event_bus.publish("code_repo_updated", {
                "repo": repo_name,
                "old_commit": change["old_commit"],
                "new_commit": change["new_commit"],
                "files_changed": change["stats"]["files_changed"],
            })
            events.append({"type": "code_repo_updated", "repo": repo_name})
        except Exception as exc:
            logger.warning("Event bus publish failed: %s", exc)

    # Rebuild full graph
    if report["changed_repos"]:
        try:
            ckg.build_code_graph(code_root)
        except Exception as exc:
            logger.warning("Full code graph rebuild failed: %s", exc)

    return {
        "repos_checked": report["repos_checked"],
        "changed": len(report["changed_repos"]),
        "pulled": pulled,
        "scanned": scanned,
        "events_emitted": events,
    }


def _check_signature_changes(
    repo_path: Path,
    repo_name: str,
    wiki_root: str,
    change: dict[str, Any],
    events: list[dict[str, Any]],
) -> None:
    """Detect function/class signature changes and add warnings to wiki pages."""
    import wiki_engine as engine

    root = Path(wiki_root)
    # Find the wiki page for this repo
    repo_slug = engine.generate_page_id(repo_name)
    repo_page = root / "entities" / f"{repo_slug}.md"
    if not repo_page.exists():
        return

    try:
        content = repo_page.read_text(encoding="utf-8")
        meta, body = engine.parse_frontmatter(content)
    except Exception:
        return

    # Add warning block if not already present
    warning = (
        f"> [!WARNING] 代码变更检测\n> "
        f"仓库 `{repo_name}` 于 {datetime.now().isoformat(timespec='minutes')} 检测到新提交 "
        f"({change['old_commit'][:7]} → {change['new_commit'][:7]})。"
        f"请核实相关实现是否仍与 Wiki 描述一致。\n"
    )

    if "代码变更检测" in body:
        # Update existing warning
        lines = body.split("\n")
        new_lines: list[str] = []
        skip = False
        for line in lines:
            if "> [!WARNING] 代码变更检测" in line:
                skip = True
                new_lines.append(warning.rstrip())
                continue
            if skip and not line.startswith(">"):
                skip = False
            if not skip:
                new_lines.append(line)
        body = "\n".join(new_lines)
    else:
        body = body.rstrip() + "\n\n" + warning + "\n"

    new_content = engine.write_frontmatter(meta, body)
    repo_page.write_text(new_content, encoding="utf-8")
    events.append({"type": "wiki_warning_added", "repo": repo_name, "page": str(repo_page)})
    logger.info("Added code-change warning to %s", repo_page)


__all__ = [
    "check_repos",
    "sync_changed_repos",
]
