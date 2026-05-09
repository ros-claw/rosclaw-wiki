"""GitHub Gateway — real GitHub PR action loop for ROSClaw Wiki.

Wraps the GitHub REST API for:
  - Branch creation
  - File commit (create or update)
  - PR creation with labels
  - PR status query
  - PR merge (for GREEN auto-merge)

Requires GITHUB_TOKEN environment variable with repo scope.
"""

from __future__ import annotations

import base64
import logging
import os
from typing import Any

import requests

logger = logging.getLogger("rosclaw.github_gateway")

GITHUB_API_BASE = "https://api.github.com"


class GitHubGateway:
    """GitHub API gateway for automated PR workflows."""

    def __init__(self, token: str | None = None):
        self.token = token or os.environ.get("GITHUB_TOKEN")
        if not self.token:
            raise RuntimeError(
                "GitHub token required. Set GITHUB_TOKEN environment variable."
            )
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"token {self.token}",
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "rosclaw-wiki/1.0",
        })

    def _request(self, method: str, path: str, **kwargs) -> dict[str, Any]:
        """Make an authenticated GitHub API request."""
        url = f"{GITHUB_API_BASE}/{path.lstrip('/')}"
        try:
            resp = self.session.request(method, url, timeout=60, **kwargs)
            resp.raise_for_status()
            return resp.json() if resp.text else {}
        except requests.HTTPError as exc:
            logger.error("GitHub API error %s %s: %s", method, url, exc.response.text[:500])
            raise RuntimeError(f"GitHub API error: {exc.response.status_code} — {exc.response.text[:500]}")
        except requests.RequestException as exc:
            logger.error("GitHub request failed %s %s: %s", method, url, exc)
            raise RuntimeError(f"GitHub request failed: {exc}")

    def get_default_branch(self, repo: str) -> str:
        """Get the default branch for a repository."""
        data = self._request("GET", f"/repos/{repo}")
        return data.get("default_branch", "main")

    def get_branch_sha(self, repo: str, branch: str) -> str:
        """Get the commit SHA for a branch."""
        data = self._request("GET", f"/repos/{repo}/git/ref/heads/{branch}")
        return data["object"]["sha"]

    def create_branch(self, repo: str, new_branch: str, base_branch: str | None = None) -> dict[str, Any]:
        """Create a new branch from the latest commit of base_branch.

        Returns:
            API response dict.
        """
        base = base_branch or self.get_default_branch(repo)
        sha = self.get_branch_sha(repo, base)
        return self._request(
            "POST",
            f"/repos/{repo}/git/refs",
            json={"ref": f"refs/heads/{new_branch}", "sha": sha},
        )

    def get_file_sha(self, repo: str, path: str, branch: str | None = None) -> str | None:
        """Get the blob SHA of a file if it exists."""
        ref = f"?ref={branch}" if branch else ""
        try:
            data = self._request("GET", f"/repos/{repo}/contents/{path}{ref}")
            return data.get("sha")
        except RuntimeError:
            return None

    def commit_file(
        self,
        repo: str,
        path: str,
        content: str,
        message: str,
        branch: str,
    ) -> dict[str, Any]:
        """Create or update a file in a branch.

        Returns:
            API response dict with commit info.
        """
        existing_sha = self.get_file_sha(repo, path, branch)
        payload: dict[str, Any] = {
            "message": message,
            "content": base64.b64encode(content.encode("utf-8")).decode("ascii"),
            "branch": branch,
        }
        if existing_sha:
            payload["sha"] = existing_sha

        return self._request("PUT", f"/repos/{repo}/contents/{path}", json=payload)

    def create_pr(
        self,
        repo: str,
        title: str,
        body: str,
        head_branch: str,
        base_branch: str | None = None,
        labels: list[str] | None = None,
        draft: bool = False,
    ) -> dict[str, Any]:
        """Create a pull request.

        Returns:
            Dict with status, pr_number, pr_url, and api_response.
        """
        base = base_branch or self.get_default_branch(repo)
        payload = {
            "title": title,
            "body": body,
            "head": head_branch,
            "base": base,
            "draft": draft,
        }
        data = self._request("POST", f"/repos/{repo}/pulls", json=payload)

        pr_number = data.get("number")
        pr_url = data.get("html_url", "")

        # Add labels if provided
        if labels and pr_number:
            try:
                self._request(
                    "POST",
                    f"/repos/{repo}/issues/{pr_number}/labels",
                    json={"labels": labels},
                )
            except RuntimeError as exc:
                logger.warning("Failed to add labels to PR #%s: %s", pr_number, exc)

        return {
            "status": "created",
            "pr_number": pr_number,
            "pr_url": pr_url,
            "title": title,
            "labels": labels or [],
            "head_branch": head_branch,
            "base_branch": base,
            "api_response": data,
        }

    def get_pr_status(self, repo: str, pr_number: int) -> dict[str, Any]:
        """Get the current status of a pull request.

        Returns:
            Dict with state, mergeable, merged, and checks status.
        """
        pr_data = self._request("GET", f"/repos/{repo}/pulls/{pr_number}")

        # Check CI/status
        checks_data = self._request("GET", f"/repos/{repo}/pulls/{pr_number}/status")
        check_runs = self._request("GET", f"/repos/{repo}/commits/{pr_data.get('head', {}).get('sha', '')}/check-runs")

        return {
            "state": pr_data.get("state"),
            "merged": pr_data.get("merged", False),
            "mergeable": pr_data.get("mergeable"),
            "mergeable_state": pr_data.get("mergeable_state"),
            "title": pr_data.get("title"),
            "labels": [l["name"] for l in pr_data.get("labels", [])],
            "checks_status": checks_data.get("state", "unknown"),
            "check_runs_total": check_runs.get("total_count", 0),
            "check_runs_passed": sum(
                1 for r in check_runs.get("check_runs", [])
                if r.get("conclusion") == "success"
            ),
        }

    def merge_pr(
        self,
        repo: str,
        pr_number: int,
        commit_title: str | None = None,
        merge_method: str = "squash",
    ) -> dict[str, Any]:
        """Merge a pull request.

        Args:
            merge_method: "merge", "squash", or "rebase".

        Returns:
            API response dict.
        """
        payload: dict[str, Any] = {"merge_method": merge_method}
        if commit_title:
            payload["commit_title"] = commit_title

        return self._request("PUT", f"/repos/{repo}/pulls/{pr_number}/merge", json=payload)

    def create_pr_with_file(
        self,
        repo: str,
        file_path: str,
        file_content: str,
        pr_title: str,
        pr_body: str,
        commit_message: str | None = None,
        head_branch: str | None = None,
        base_branch: str | None = None,
        labels: list[str] | None = None,
        auto_merge: bool = False,
    ) -> dict[str, Any]:
        """Full workflow: create branch → commit file → create PR → optionally merge.

        Returns:
            Dict with full workflow result.
        """
        base = base_branch or self.get_default_branch(repo)
        branch = head_branch or f"rosclaw-auto/{pr_title.lower().replace(' ', '-')[:40]}"
        commit_msg = commit_message or pr_title

        # 1. Create branch
        try:
            self.create_branch(repo, branch, base)
        except RuntimeError as exc:
            if "Reference already exists" not in str(exc):
                raise
            logger.info("Branch %s already exists, reusing", branch)

        # 2. Commit file
        self.commit_file(repo, file_path, file_content, commit_msg, branch)

        # 3. Create PR
        pr_result = self.create_pr(
            repo=repo,
            title=pr_title,
            body=pr_body,
            head_branch=branch,
            base_branch=base,
            labels=labels,
        )

        # 4. Auto-merge if GREEN
        if auto_merge and pr_result.get("pr_number"):
            try:
                merge_resp = self.merge_pr(repo, pr_result["pr_number"])
                pr_result["auto_merged"] = merge_resp.get("merged", False)
                pr_result["merge_sha"] = merge_resp.get("sha")
            except RuntimeError as exc:
                logger.warning("Auto-merge failed for PR #%s: %s", pr_result["pr_number"], exc)
                pr_result["auto_merged"] = False
                pr_result["merge_error"] = str(exc)

        return pr_result


# ── Convenience functions ──

def submit_pr_to_github(
    pr_data: dict[str, Any],
    github_repo: str,
    base_branch: str = "main",
    github_token: str | None = None,
    auto_merge: bool | None = None,
) -> dict[str, Any]:
    """Submit a ROSClaw PR dict to GitHub.

    Args:
        pr_data: Output from pr_generator.generate_pr().
        github_repo: "owner/repo" format.
        base_branch: Target branch.
        github_token: GitHub PAT (or GITHUB_TOKEN env var).
        auto_merge: Override auto-merge. If None, inferred from labels.

    Returns:
        Dict with status, pr_url, and details.
    """
    gateway = GitHubGateway(token=github_token)

    entity = pr_data.get("entity", "unknown")
    pr_info = pr_data.get("pr", {})
    title = pr_info.get("title", f"[Auto-PR] Sync {entity}")
    body = pr_info.get("body", "")
    labels = pr_info.get("labels", ["auto-generated"])

    if auto_merge is None:
        auto_merge = "auto-merge" in labels and "needs-review" not in labels

    return gateway.create_pr(
        repo=github_repo,
        title=title,
        body=body,
        head_branch=f"auto-sync/{entity.lower().replace(' ', '-')}",
        base_branch=base_branch,
        labels=labels,
    )
