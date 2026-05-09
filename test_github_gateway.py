"""Mock-based tests for github_gateway.py — Phase 14 Module 3."""

from __future__ import annotations

import json
from unittest.mock import MagicMock, patch

import pytest

from github_gateway import GitHubGateway, submit_pr_to_github


@pytest.fixture
def gateway():
    """Gateway with a dummy token."""
    return GitHubGateway(token="test-token-123")


class FakeResponse:
    """Minimal requests.Response stand-in."""

    def __init__(self, status_code: int, json_data: dict | None = None, text: str = ""):
        self.status_code = status_code
        self._json = json_data or {}
        self.text = text or json.dumps(self._json)

    def json(self):
        return self._json

    def raise_for_status(self):
        if self.status_code >= 400:
            from requests import HTTPError
            exc = HTTPError(f"{self.status_code}")
            exc.response = self
            raise exc


def test_gateway_requires_token():
    """Gateway raises if no token provided."""
    with patch.dict("os.environ", {}, clear=True):
        with pytest.raises(RuntimeError, match="GitHub token required"):
            GitHubGateway()


def test_get_default_branch(gateway):
    """get_default_branch parses default_branch from repo payload."""
    resp = FakeResponse(200, {"default_branch": "develop"})
    with patch.object(gateway.session, "request", return_value=resp):
        assert gateway.get_default_branch("owner/repo") == "develop"


def test_get_branch_sha(gateway):
    """get_branch_sha extracts SHA from git ref payload."""
    resp = FakeResponse(200, {"object": {"sha": "abc123"}})
    with patch.object(gateway.session, "request", return_value=resp):
        assert gateway.get_branch_sha("owner/repo", "main") == "abc123"


def test_create_branch(gateway):
    """create_branch posts a new git ref."""
    default_resp = FakeResponse(200, {"default_branch": "main"})
    ref_resp = FakeResponse(200, {"object": {"sha": "sha1"}})
    create_resp = FakeResponse(201, {"ref": "refs/heads/feature-x"})

    def side_effect(method, url, **kwargs):
        if "git/ref/heads/main" in url:
            return ref_resp
        if "git/refs" in url and method == "POST":
            return create_resp
        return default_resp

    with patch.object(gateway.session, "request", side_effect=side_effect):
        result = gateway.create_branch("owner/repo", "feature-x")
        assert result["ref"] == "refs/heads/feature-x"


def test_get_file_sha_found(gateway):
    """get_file_sha returns SHA when file exists."""
    resp = FakeResponse(200, {"sha": "blob-sha"})
    with patch.object(gateway.session, "request", return_value=resp):
        assert gateway.get_file_sha("owner/repo", "path/to/file.py", "main") == "blob-sha"


def test_get_file_sha_not_found(gateway):
    """get_file_sha returns None for missing file."""
    err_resp = FakeResponse(404, {"message": "Not Found"})
    with patch.object(gateway.session, "request", return_value=err_resp):
        assert gateway.get_file_sha("owner/repo", "missing.py", "main") is None


def test_commit_file_create(gateway):
    """commit_file creates a new file when no existing SHA."""
    not_found = FakeResponse(404, {"message": "Not Found"})
    created = FakeResponse(201, {"content": {"sha": "new-sha"}})

    def side_effect(method, url, **kwargs):
        if method == "GET":
            return not_found
        return created

    with patch.object(gateway.session, "request", side_effect=side_effect):
        result = gateway.commit_file("owner/repo", "test.py", "print(1)", "init", "main")
        assert result["content"]["sha"] == "new-sha"


def test_commit_file_update(gateway):
    """commit_file updates existing file when SHA present."""
    found = FakeResponse(200, {"sha": "old-sha"})
    updated = FakeResponse(200, {"content": {"sha": "new-sha"}})

    def side_effect(method, url, **kwargs):
        if method == "GET":
            return found
        return updated

    with patch.object(gateway.session, "request", side_effect=side_effect):
        result = gateway.commit_file("owner/repo", "test.py", "print(2)", "update", "main")
        assert result["content"]["sha"] == "new-sha"


def test_create_pr(gateway):
    """create_pr returns PR number and URL."""
    default_resp = FakeResponse(200, {"default_branch": "main"})
    pr_resp = FakeResponse(201, {"number": 42, "html_url": "https://github.com/owner/repo/pull/42"})
    label_resp = FakeResponse(200, {})

    def side_effect(method, url, **kwargs):
        if "/pulls" in url:
            return pr_resp
        if "/labels" in url:
            return label_resp
        return default_resp

    with patch.object(gateway.session, "request", side_effect=side_effect):
        result = gateway.create_pr("owner/repo", "Title", "Body", "feature-x", labels=["auto-generated"])
        assert result["status"] == "created"
        assert result["pr_number"] == 42
        assert result["pr_url"] == "https://github.com/owner/repo/pull/42"
        assert "auto-generated" in result["labels"]


def test_get_pr_status(gateway):
    """get_pr_status aggregates PR and checks data."""
    pr_resp = FakeResponse(200, {
        "state": "open",
        "merged": False,
        "mergeable": True,
        "mergeable_state": "clean",
        "head": {"sha": "head-sha"},
        "labels": [{"name": "auto-generated"}],
    })
    status_resp = FakeResponse(200, {"state": "success"})
    checks_resp = FakeResponse(200, {
        "total_count": 2,
        "check_runs": [
            {"conclusion": "success"},
            {"conclusion": "failure"},
        ],
    })

    def side_effect(method, url, **kwargs):
        if "/pulls/1" in url and "/status" not in url:
            return pr_resp
        if "/status" in url:
            return status_resp
        if "/check-runs" in url:
            return checks_resp
        return FakeResponse(200)

    with patch.object(gateway.session, "request", side_effect=side_effect):
        result = gateway.get_pr_status("owner/repo", 1)
        assert result["state"] == "open"
        assert result["checks_status"] == "success"
        assert result["check_runs_total"] == 2
        assert result["check_runs_passed"] == 1


def test_merge_pr(gateway):
    """merge_pr calls the merge endpoint."""
    resp = FakeResponse(200, {"merged": True, "sha": "merge-sha"})
    with patch.object(gateway.session, "request", return_value=resp):
        result = gateway.merge_pr("owner/repo", 42, merge_method="squash")
        assert result["merged"] is True
        assert result["sha"] == "merge-sha"


def _match_url(method: str, url: str, responses: list) -> FakeResponse:
    """Ordered URL matcher: return first exact-ish match."""
    for (m, path), resp in responses:
        if method == m and path in url:
            return resp
    return FakeResponse(200)


def test_create_pr_with_file_full_workflow(gateway):
    """create_pr_with_file orchestrates branch, commit, PR creation."""
    default_resp = FakeResponse(200, {"default_branch": "main"})
    ref_resp = FakeResponse(200, {"object": {"sha": "base-sha"}})
    branch_created = FakeResponse(201, {"ref": "refs/heads/auto/test"})
    not_found = FakeResponse(404, {"message": "Not Found"})
    commit_resp = FakeResponse(201, {"content": {"sha": "file-sha"}})
    pr_resp = FakeResponse(201, {"number": 7, "html_url": "https://github.com/owner/repo/pull/7"})
    label_resp = FakeResponse(200, {})

    # Ordered list: more specific paths first
    responses = [
        (("GET", "/repos/owner/repo/git/ref/heads/main"), ref_resp),
        (("POST", "/repos/owner/repo/git/refs"), branch_created),
        (("GET", "/repos/owner/repo/contents/src%2Ffile.py"), not_found),
        (("PUT", "/repos/owner/repo/contents/src%2Ffile.py"), commit_resp),
        (("POST", "/repos/owner/repo/pulls"), pr_resp),
        (("POST", "/repos/owner/repo/issues/7/labels"), label_resp),
        (("GET", "/repos/owner/repo"), default_resp),
    ]

    def side_effect(method, url, **kwargs):
        return _match_url(method, url, responses)

    with patch.object(gateway.session, "request", side_effect=side_effect):
        result = gateway.create_pr_with_file(
            repo="owner/repo",
            file_path="src/file.py",
            file_content="# test",
            pr_title="Test PR",
            pr_body="Body",
        )
        assert result["status"] == "created"
        assert result["pr_number"] == 7
        assert result.get("auto_merged") is None or result.get("auto_merged") is False


def test_create_pr_with_file_auto_merge(gateway):
    """create_pr_with_file auto-merges when auto_merge=True."""
    default_resp = FakeResponse(200, {"default_branch": "main"})
    ref_resp = FakeResponse(200, {"object": {"sha": "base-sha"}})
    branch_created = FakeResponse(201, {})
    not_found = FakeResponse(404, {"message": "Not Found"})
    commit_resp = FakeResponse(201, {})
    pr_resp = FakeResponse(201, {"number": 8, "html_url": "https://github.com/owner/repo/pull/8"})
    label_resp = FakeResponse(200, {})
    merge_resp = FakeResponse(200, {"merged": True, "sha": "merge-sha"})

    responses = [
        (("GET", "/repos/owner/repo/git/ref/heads/main"), ref_resp),
        (("POST", "/repos/owner/repo/git/refs"), branch_created),
        (("GET", "/repos/owner/repo/contents/src%2Ffile.py"), not_found),
        (("PUT", "/repos/owner/repo/contents/src%2Ffile.py"), commit_resp),
        (("POST", "/repos/owner/repo/pulls"), pr_resp),
        (("POST", "/repos/owner/repo/issues/8/labels"), label_resp),
        (("PUT", "/repos/owner/repo/pulls/8/merge"), merge_resp),
        (("GET", "/repos/owner/repo"), default_resp),
    ]

    def side_effect(method, url, **kwargs):
        return _match_url(method, url, responses)

    with patch.object(gateway.session, "request", side_effect=side_effect):
        result = gateway.create_pr_with_file(
            repo="owner/repo",
            file_path="src/file.py",
            file_content="# test",
            pr_title="Test PR",
            pr_body="Body",
            auto_merge=True,
        )
        assert result["auto_merged"] is True
        assert result["merge_sha"] == "merge-sha"


def test_create_pr_with_file_existing_branch(gateway):
    """create_pr_with_file reuses branch if it already exists."""
    default_resp = FakeResponse(200, {"default_branch": "main"})
    ref_resp = FakeResponse(200, {"object": {"sha": "base-sha"}})
    branch_exists_err = FakeResponse(422, {"message": "Reference already exists"})
    not_found = FakeResponse(404, {"message": "Not Found"})
    commit_resp = FakeResponse(201, {})
    pr_resp = FakeResponse(201, {"number": 9, "html_url": "https://github.com/owner/repo/pull/9"})
    label_resp = FakeResponse(200, {})

    responses = [
        (("GET", "/repos/owner/repo/git/ref/heads/main"), ref_resp),
        (("POST", "/repos/owner/repo/git/refs"), branch_exists_err),
        (("GET", "/repos/owner/repo/contents/src%2Ffile.py"), not_found),
        (("PUT", "/repos/owner/repo/contents/src%2Ffile.py"), commit_resp),
        (("POST", "/repos/owner/repo/pulls"), pr_resp),
        (("POST", "/repos/owner/repo/issues/9/labels"), label_resp),
        (("GET", "/repos/owner/repo"), default_resp),
    ]

    def side_effect(method, url, **kwargs):
        return _match_url(method, url, responses)

    with patch.object(gateway.session, "request", side_effect=side_effect):
        result = gateway.create_pr_with_file(
            repo="owner/repo",
            file_path="src/file.py",
            file_content="# test",
            pr_title="Test PR",
            pr_body="Body",
        )
        assert result["status"] == "created"


def test_submit_pr_to_github():
    """submit_pr_to_github convenience function creates a PR."""
    pr_data = {
        "entity": "Unitree-G1",
        "pr": {
            "title": "[Auto-PR] Sync Unitree-G1",
            "body": "Body",
            "labels": ["auto-generated", "auto-merge"],
        },
    }
    default_resp = FakeResponse(200, {"default_branch": "main"})
    pr_resp = FakeResponse(201, {"number": 10, "html_url": "https://github.com/owner/repo/pull/10"})
    label_resp = FakeResponse(200, {})

    def side_effect(method, url, **kwargs):
        if "/pulls" in url:
            return pr_resp
        if "/labels" in url:
            return label_resp
        return default_resp

    # Patch GitHubGateway so the convenience function uses our mocked session
    mock_gateway = MagicMock()
    mock_instance = MagicMock()
    mock_instance.session.request.side_effect = side_effect
    mock_instance.get_default_branch.return_value = "main"
    mock_instance.create_pr.return_value = {
        "status": "created",
        "pr_number": 10,
        "pr_url": "https://github.com/owner/repo/pull/10",
    }
    mock_gateway.return_value = mock_instance

    with patch("github_gateway.GitHubGateway", mock_gateway):
        result = submit_pr_to_github(pr_data, "owner/repo", github_token="tok")
        assert result["status"] == "created"
        assert result["pr_url"] == "https://github.com/owner/repo/pull/10"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
