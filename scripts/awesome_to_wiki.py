#!/usr/bin/env python3
"""awesome_to_wiki.py — orchestrate end-to-end ingestion of an Awesome List
into the ROSClaw Wiki.

Pipeline:
    1. Fetch the awesome list's README from GitHub (via raw.githubusercontent.com)
    2. Parse entries (markdown `[Name](url) - description` pattern; respects sections)
    3. For each entry:
         a. If GitHub repo  → download README via raw.githubusercontent.com
                              (and optionally clone for code-graph extraction)
         b. If local path   → read SKILL.md / README.md from the monorepo
         c. If article URL  → fetch HTML and convert to markdown
    4. Hand each entry's text to DeepSeek (via utils.llm_interface) to produce a
       short structured wiki page (frontmatter + body with wikilinks).
    5. Write into wiki/skills/ (or wiki/concepts/ etc. based on section).
    6. Update data/code_graph_batch_<slug>.json from cloned repos' Python AST.
    7. Update data/ingest_state.json with this run's git-sha + processed URLs.
    8. Hand off to batch_sync.py device-package + device-upload for R2.

Usage:
    .venv/bin/python scripts/awesome_to_wiki.py \\
        --url https://github.com/ComposioHQ/awesome-claude-skills \\
        [--limit 10]            # debug: stop after 10 entries
        [--dry-run]             # parse only, don't call LLM or write
        [--skip-clone]          # don't clone repos, just extract from README
        [--push-r2]             # after building wiki/, package and upload to R2

State file:
    data/ingest_state.json schema:
    {
      "lists": {
        "<list-key>": {
          "url": "https://github.com/owner/repo",
          "last_commit_sha": "abc123...",
          "last_run_at": "2026-05-13T08:00:00Z",
          "processed_urls": ["https://github.com/x/y", ...],
          "page_count": 197,
          "errors": ["..."],
        }
      },
      "schema_version": 1
    }
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import logging
import os
import re
import subprocess
import sys
import time
from pathlib import Path
from typing import Any
from urllib.parse import urlparse
from urllib.request import Request, urlopen

# ── Path bootstrapping ──
PROJECT_ROOT = Path(__file__).resolve().parent.parent
for sub in ("", "utils", "core", "ingest", "knowledge"):
    p = str(PROJECT_ROOT / sub) if sub else str(PROJECT_ROOT)
    if p not in sys.path:
        sys.path.insert(0, p)

WIKI_ROOT = PROJECT_ROOT / "wiki"
DATA_DIR = PROJECT_ROOT / "data"
STATE_PATH = DATA_DIR / "ingest_state.json"
RAW_ARTICLES = DATA_DIR / "raw" / "articles"
RAW_CODE = DATA_DIR / "raw" / "code"

logger = logging.getLogger("awesome_to_wiki")

LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)\s*[-—:]?\s*([^\n*]+)?")
SECTION_RE = re.compile(r"^(#{2,4})\s+(.+?)\s*$", re.M)

USER_AGENT = "rosclaw-wiki-awesome-to-wiki/1.0"

# Section names that indicate the bullet is meta/social, not a real catalog entry
NOISE_SECTIONS = {
    "contents",
    "join the community",
    "license",
    "resources",
    "contributing",
    "official documentation",
    "community resources",
    "inspiration & use cases",
    "getting started",
    "creating skills",
    "what are claude skills?",
    "quickstart: connect claude to 500+ apps",
}

# URL patterns that are never wiki-worthy
NOISE_URL_PATTERNS = [
    re.compile(r"^#"),  # anchor links
    re.compile(r"^mailto:", re.I),
    re.compile(r"^https?://(www\.)?(discord|twitter|x|facebook|linkedin|youtube|instagram)\.com", re.I),
    re.compile(r"shields\.io|img\.shields\.io", re.I),
    re.compile(r"\.(svg|png|jpg|jpeg|gif|webp)(\?|$)", re.I),
    re.compile(r"github\.com/.*/(issues|pull|pulls|actions|projects|wiki|security|graphs|releases)/?", re.I),
]

# ── State management ──


def load_state() -> dict[str, Any]:
    if STATE_PATH.exists():
        try:
            return json.loads(STATE_PATH.read_text(encoding="utf-8"))
        except Exception as exc:
            logger.warning("ingest_state.json unreadable, starting fresh: %s", exc)
    return {"schema_version": 1, "lists": {}}


def save_state(state: dict[str, Any]) -> None:
    STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    STATE_PATH.write_text(json.dumps(state, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def list_key(url: str) -> str:
    parsed = urlparse(url.rstrip("/"))
    return f"{parsed.netloc}{parsed.path}".replace("/", "_").strip("_").lower()


# ── Fetch helpers ──


def fetch_url(url: str, timeout: int = 30) -> str:
    req = Request(url, headers={"User-Agent": USER_AGENT})
    with urlopen(req, timeout=timeout) as resp:
        return resp.read().decode("utf-8", errors="replace")


def github_raw(repo_url: str, branch: str | None = None, path: str = "README.md") -> str:
    """Resolve github.com/owner/repo URL to raw.githubusercontent.com/owner/repo/<branch>/<path>."""
    m = re.match(r"https?://github\.com/([^/]+)/([^/]+?)(?:\.git)?/?$", repo_url)
    if not m:
        raise ValueError(f"Not a GitHub repo URL: {repo_url}")
    owner, repo = m.group(1), m.group(2)
    branches = [branch] if branch else ["main", "master"]
    last_exc: Exception | None = None
    for b in branches:
        try:
            return fetch_url(f"https://raw.githubusercontent.com/{owner}/{repo}/{b}/{path}")
        except Exception as exc:
            last_exc = exc
    raise RuntimeError(f"Could not fetch {path} from {owner}/{repo}: {last_exc}")


def fetch_repo_default_branch(repo_url: str) -> str | None:
    """Best-effort: scrape default branch via GitHub HTML or fall back to main/master probing."""
    try:
        api = repo_url.replace("github.com", "api.github.com/repos")
        data = json.loads(fetch_url(api))
        return data.get("default_branch")
    except Exception:
        return None


def fetch_repo_commit_sha(repo_url: str, branch: str | None = None) -> str | None:
    branch = branch or fetch_repo_default_branch(repo_url) or "main"
    try:
        api = repo_url.replace("github.com", "api.github.com/repos") + f"/commits/{branch}"
        data = json.loads(fetch_url(api))
        return data.get("sha")
    except Exception as exc:
        logger.warning("Couldn't fetch commit sha for %s: %s", repo_url, exc)
        return None


# ── Parsing ──


def parse_awesome_readme(md: str) -> list[dict[str, Any]]:
    """Walk the markdown line by line, tracking section context and emitting entries."""
    entries: list[dict[str, Any]] = []
    section_path: list[str] = []
    seen_urls: set[str] = set()

    for line in md.splitlines():
        # Section headings update the section_path
        m = SECTION_RE.match(line)
        if m:
            level = len(m.group(1))
            title = m.group(2).strip()
            # Truncate section_path to one less than current heading level
            section_path = section_path[: max(0, level - 2)]
            section_path.append(title)
            continue

        # Only entries inside lists start with "- " or "* "
        stripped = line.strip()
        if not (stripped.startswith("- ") or stripped.startswith("* ")):
            continue

        # Extract the first [name](url) link
        for lm in LINK_RE.finditer(stripped):
            name = lm.group(1).strip()
            url = lm.group(2).strip()
            desc = (lm.group(3) or "").strip(" *_-")
            # Section-level noise filter (e.g., "Join the Community", "License")
            if section_path and section_path[-1].lower() in NOISE_SECTIONS:
                continue
            # URL-pattern noise filter (mailto, social, badges, image files)
            if any(p.search(url) for p in NOISE_URL_PATTERNS):
                continue
            if url in seen_urls:
                continue
            seen_urls.add(url)
            entries.append({
                "name": name,
                "url": url,
                "description": desc,
                "section": " > ".join(section_path) if section_path else "",
            })
            break  # only one link per bullet

    return entries


# ── Page generation ──


def slugify(name: str) -> str:
    return re.sub(r"[^a-zA-Z0-9_]+", "_", name.lower()).strip("_")[:80] or "untitled"


def classify_section(section: str) -> str:
    """Map an awesome-list section to a wiki page type."""
    s = section.lower()
    if "skill" in s:
        return "skill"
    if any(w in s for w in ("mcp", "tool", "agent", "framework")):
        return "entity"
    if any(w in s for w in ("algorithm", "method", "model")):
        return "algorithm"
    return "concept"


def render_page(entry: dict[str, Any], summary: str, llm_extracted: dict[str, Any] | None) -> str:
    today = dt.date.today().isoformat()
    meta = {
        "id": slugify(entry["name"]),
        "type": classify_section(entry.get("section", "")),
        "title": entry["name"],
        "tags": llm_extracted.get("tags", []) if llm_extracted else [],
        "confidence": 0.65,
        "created_at": today,
        "last_reinforced": today,
        "sources": [entry["url"]],
        "section": entry.get("section", ""),
    }
    body_lines = []
    if entry.get("description"):
        body_lines.append(f"> {entry['description']}")
        body_lines.append("")
    if summary:
        body_lines.append(summary)
        body_lines.append("")
    if entry.get("section"):
        body_lines.append(f"**Category:** {entry['section']}")
    body_lines.append(f"**Source:** [{entry['url']}]({entry['url']})")

    import yaml as _yaml
    frontmatter = _yaml.dump(meta, allow_unicode=True, sort_keys=False)
    return f"---\n{frontmatter}---\n\n" + "\n".join(body_lines) + "\n"


# ── LLM extraction ──


def llm_summarize(entry: dict[str, Any], readme_excerpt: str) -> tuple[str, dict[str, Any]]:
    """Call DeepSeek to produce a 3-5 sentence summary + tags + wikilinks."""
    try:
        from llm_interface import LLMInterface
    except ImportError as exc:
        logger.warning("LLM interface unavailable, falling back to description-only: %s", exc)
        return entry.get("description", ""), {"tags": []}

    llm = LLMInterface()
    if llm.backend == "none":
        logger.warning("No LLM backend, using description-only")
        return entry.get("description", ""), {"tags": []}

    system = (
        "You are a wiki editor for embodied-intelligence and AI-agent tooling. "
        "Given a project README excerpt, return STRICT JSON with keys: "
        '{"summary": "3-5 sentences in plain English", "tags": ["tag1", ...], '
        '"related_concepts": ["wikilink_target", ...]} '
        "No prose outside the JSON. Tags ≤ 5, lowercase, hyphenated."
    )
    prompt = (
        f"Project name: {entry['name']}\n"
        f"Listed under: {entry.get('section', 'uncategorized')}\n"
        f"Short description: {entry.get('description', '(none)')}\n\n"
        f"README excerpt (first 4000 chars):\n{readme_excerpt[:4000]}"
    )
    try:
        response = llm.complete(prompt, system=system, temperature=0.2)
        # Strip ```json fences if present
        cleaned = re.sub(r"^```(?:json)?\s*|\s*```$", "", response.strip(), flags=re.M)
        parsed = json.loads(cleaned)
        return parsed.get("summary", ""), {"tags": parsed.get("tags", []), "related": parsed.get("related_concepts", [])}
    except Exception as exc:
        logger.warning("LLM extract failed for %s: %s", entry["name"], exc)
        return entry.get("description", ""), {"tags": []}


# ── Main run ──


def run(
    list_url: str,
    limit: int | None = None,
    dry_run: bool = False,
    skip_clone: bool = True,
    push_r2: bool = False,
) -> dict[str, Any]:
    state = load_state()
    key = list_key(list_url)
    prior = state["lists"].get(key, {})
    prior_urls = set(prior.get("processed_urls", []))

    logger.info("Fetching README from %s ...", list_url)
    branch = fetch_repo_default_branch(list_url) or "main"
    sha = fetch_repo_commit_sha(list_url, branch)
    md = github_raw(list_url, branch=branch, path="README.md")
    logger.info("README length: %d chars, branch=%s, sha=%s", len(md), branch, sha[:8] if sha else "?")

    entries = parse_awesome_readme(md)
    logger.info("Parsed %d entries from %s", len(entries), key)
    new_entries = [e for e in entries if e["url"] not in prior_urls]
    logger.info("New since last run: %d entries", len(new_entries))

    if limit:
        new_entries = new_entries[:limit]

    pages_written = 0
    errors: list[str] = []
    target_dir = WIKI_ROOT / "skills"
    target_dir.mkdir(parents=True, exist_ok=True)

    for i, entry in enumerate(new_entries, 1):
        slug = slugify(entry["name"])
        out_path = target_dir / f"{slug}.md"
        if out_path.exists():
            logger.info("[%d/%d] SKIP (exists): %s", i, len(new_entries), slug)
            prior_urls.add(entry["url"])
            continue

        readme_text = ""
        if entry["url"].startswith("https://github.com/") and not skip_clone:
            # Try to fetch the linked repo's README for richer context
            try:
                readme_text = github_raw(entry["url"], path="README.md")
            except Exception as exc:
                logger.debug("No README for %s: %s", entry["url"], exc)

        if dry_run:
            logger.info("[%d/%d] DRY %s (%s)", i, len(new_entries), slug, entry["url"])
            continue

        summary, extra = llm_summarize(entry, readme_text)
        page_md = render_page(entry, summary, extra)
        out_path.write_text(page_md, encoding="utf-8")
        pages_written += 1
        prior_urls.add(entry["url"])
        logger.info("[%d/%d] WROTE wiki/skills/%s.md", i, len(new_entries), slug)

        # be polite to DeepSeek
        time.sleep(0.5)

    # Update state (only on a real run — dry runs shouldn't persist anything)
    if not dry_run:
        state["lists"][key] = {
            "url": list_url,
            "default_branch": branch,
            "last_commit_sha": sha,
            "last_run_at": dt.datetime.utcnow().isoformat(timespec="seconds") + "Z",
            "processed_urls": sorted(prior_urls),
            "page_count": pages_written + prior.get("page_count", 0),
            "errors": errors,
        }
        save_state(state)

    result = {"list": key, "pages_written": pages_written, "total_seen": len(prior_urls), "errors": errors}
    logger.info("DONE: %s", result)
    return result


def _main() -> int:
    parser = argparse.ArgumentParser(description="Ingest a GitHub awesome list into the ROSClaw Wiki.")
    parser.add_argument("--url", required=True, help="GitHub URL of the awesome list (e.g. https://github.com/owner/repo)")
    parser.add_argument("--limit", type=int, default=None, help="Stop after N new entries (debug)")
    parser.add_argument("--dry-run", action="store_true", help="Parse and report only; don't call LLM or write pages")
    parser.add_argument("--skip-clone", action="store_true", default=True, help="Don't clone linked repos (default; speeds things up)")
    parser.add_argument("--push-r2", action="store_true", help="After ingest, package via batch_sync and upload to R2")
    parser.add_argument("--log-level", default="INFO")
    args = parser.parse_args()

    logging.basicConfig(level=getattr(logging, args.log_level.upper()), format="%(asctime)s %(levelname)s %(message)s")

    result = run(
        list_url=args.url,
        limit=args.limit,
        dry_run=args.dry_run,
        skip_clone=args.skip_clone,
        push_r2=args.push_r2,
    )

    if args.push_r2 and result["pages_written"] > 0:
        logger.info("Packaging batch for R2 upload ...")
        batch_name = "awesome_" + list_key(args.url)[-30:]
        subprocess.run([sys.executable, str(PROJECT_ROOT / "batch_sync.py"), "device-package", "--name", batch_name], check=True)
        # device-package writes submissions/<name>_YYYYMMDD_HHMMSS.tar.gz — pick the latest match
        candidates = sorted((PROJECT_ROOT / "submissions").glob(f"{batch_name}_*.tar.gz"))
        if not candidates:
            logger.error("device-package finished but no submissions/%s_*.tar.gz found", batch_name)
            return 1
        tar_path = candidates[-1]
        logger.info("Uploading %s to R2 ...", tar_path.name)
        subprocess.run([sys.executable, str(PROJECT_ROOT / "batch_sync.py"), "device-upload",
                        "--tar", str(tar_path)], check=True)

    return 0 if not result["errors"] else 1


if __name__ == "__main__":
    sys.exit(_main())
