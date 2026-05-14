# Tutorial: Ingesting a GitHub Awesome List into ROSClaw Wiki

> End-to-end recipe — from a GitHub awesome-list URL to fresh wiki pages on
> `api.rosclaw.io`, with weekly incremental refresh. Reproducible by humans
> and other agents.

This tutorial walks one list through the full closed loop:

```
awesome-list URL
   ↓ scripts/awesome_to_wiki.py
parse + LLM extract (DeepSeek)
   ↓
wiki/skills/<slug>.md  (one Markdown page per entry)
data/ingest_state.json (records "what was processed when")
   ↓ batch_sync.py device-package
submissions/<batch>.tar.gz
   ↓ batch_sync.py device-upload
R2: submissions/<batch>.tar.gz
   ↓ admin UI "Batch Sync → Merge"
production wiki/ + SQLite + seekdb
   ↓
https://www.rosclaw.io/hub/wiki  (page count updates)
```

---

## Prerequisites

1. **Python 3.11** active (`source .venv/bin/activate`)
2. **DeepSeek API key** in `.env`:
   ```bash
   DEEPSEEK_API_KEY=sk-...
   ```
3. **R2 credentials** in `.env` (only needed if you'll `--push-r2`):
   ```bash
   R2_ENDPOINT=https://<account-id>.r2.cloudflarestorage.com
   R2_ACCESS_KEY_ID=...
   R2_SECRET_ACCESS_KEY=...
   R2_BUCKET=rosclaw-wiki
   ```

Verify the LLM backend is wired:

```bash
.venv/bin/python -c "
import sys; sys.path.insert(0, 'utils')
from llm_interface import LLMInterface
print('backend:', LLMInterface().backend)"
# expect: backend: deepseek
```

---

## Step 1 — Pick a list and dry-run

```bash
.venv/bin/python scripts/awesome_to_wiki.py \
    --url https://github.com/ComposioHQ/awesome-claude-skills \
    --dry-run
```

The dry run **never calls the LLM or writes any file**. It just parses the README
and reports what would be ingested. Expected tail of output:

```
INFO Parsed 160 entries from github.com_composiohq_awesome-claude-skills
INFO [160/160] DRY zoom_automation (./zoom-automation/)
INFO DONE: {'list': 'github.com_composiohq_awesome-claude-skills', 'pages_written': 0, 'total_seen': 0, 'errors': []}
```

### Auto-detected source formats

The orchestrator tries three parsers in order and automatically picks the one
that yields entries:

1. **Bullet-list** (default) — `-[*] [Name](url) - description` under `##` headings
2. **Markdown-table** — `| [Name](url) | Description |` rows under `##` headings  
   *Used by:* `hesamsheikh/awesome-openclaw-usecases`
3. **CSV table** — `THE_RESOURCES_TABLE.csv` in repo root  
   *Used by:* `hesreallyhim/awesome-claude-code`

If the bullet parser returns 0 entries, the orchestrator automatically falls back
to the table and CSV parsers — no manual intervention needed.

**If the parsed count looks too high (1000+) or too low (< 10)**, look at the
noise filters in `scripts/awesome_to_wiki.py`:
- `NOISE_SECTIONS` — bullet sections that aren't real catalog entries
- `NOISE_URL_PATTERNS` — anchor links, social media, badges, images

Adjust those if the list has a different shape.

---

## Step 2 — Real run, small batch first

Always validate end-to-end on a few entries before committing the rest:

```bash
.venv/bin/python scripts/awesome_to_wiki.py \
    --url https://github.com/ComposioHQ/awesome-claude-skills \
    --limit 5
```

Expected: ~5-10 seconds per entry (LLM call + write). Output like:

```
INFO [1/5] WROTE wiki/skills/skill_creator.md
INFO [2/5] WROTE wiki/skills/template_skill.md
...
INFO DONE: {'pages_written': 5, 'total_seen': 5, 'errors': []}
```

Inspect one of the generated pages:

```bash
cat wiki/skills/skill_creator.md
```

You should see well-formed YAML frontmatter (id, type, title, tags,
confidence, sources, section) plus a 3-5 sentence summary in the body.

**If the summary looks generic or wrong**, the LLM didn't have enough
context. Pass `--skip-clone=false` (default is `true`) to also pull each
linked repo's README into the prompt.

---

## Step 3 — Full run

Remove the `--limit` and let it process every new entry. For ~160 entries
expect ~15-25 minutes wall-clock at DeepSeek's typical throughput.

```bash
.venv/bin/python scripts/awesome_to_wiki.py \
    --url https://github.com/ComposioHQ/awesome-claude-skills
```

The script is **resumable** — `data/ingest_state.json` tracks which URLs
have already been processed. Killing the run and restarting picks up
where it left off.

Existing wiki pages with the same slug are **skipped** (not overwritten).
To rebuild a specific page, `rm wiki/skills/<slug>.md` first, then re-run.

---

## Step 4 — Package and push to R2

After the wiki is updated locally, build a tarball and push to R2:

```bash
.venv/bin/python batch_sync.py device-package \
    --name composiohq_awesome_claude_skills

# expected output: submissions/composiohq_awesome_claude_skills_YYYYMMDD_HHMMSS.tar.gz

.venv/bin/python batch_sync.py device-upload \
    --tar submissions/composiohq_awesome_claude_skills_*.tar.gz
```

Or do both in one shot via the orchestrator's `--push-r2` flag:

```bash
.venv/bin/python scripts/awesome_to_wiki.py \
    --url https://github.com/ComposioHQ/awesome-claude-skills \
    --push-r2
```

---

## Step 5 — Merge on production

1. Open https://www.rosclaw.io/admin → **Batch Sync** tab
2. The new batch should appear under "Pending"
3. Click **Preview** to see the manifest (file count, device id, created_at)
4. Click **Merge** — synchronous response in ~10s; background task syncs
   embeddings into seekdb
5. After merge, the tarball moves to `submissions/processed/` in R2 (so it
   no longer shows as pending). The Hub stats refresh next page load.

Verify:

```bash
curl -s https://api.rosclaw.io/v1/health | jq
# wiki_pages count should have increased by the batch's page count

curl -s https://api.rosclaw.io/wiki/v1/hub/stats | jq .global_stats
```

---

## Step 6 — Weekly incremental refresh (optional)

The pipeline supports incremental updates: only entries new since the last
run are processed. State lives in `data/ingest_state.json`:

```json
{
  "schema_version": 1,
  "lists": {
    "github.com_composiohq_awesome-claude-skills": {
      "url": "https://github.com/ComposioHQ/awesome-claude-skills",
      "default_branch": "master",
      "last_commit_sha": "f2b5e29b...",
      "last_run_at": "2026-05-13T08:00:00Z",
      "processed_urls": ["https://github.com/x/y", "..."],
      "page_count": 157,
      "errors": []
    }
  }
}
```

To schedule a weekly refresh, install the bundled GitHub Action:

```bash
# Already shipped at: .github/workflows/awesome-weekly-refresh.yml
# Runs every Monday 02:13 UTC against all lists in data/awesome_lists.txt.
```

`data/awesome_lists.txt` is a plain list of awesome-list URLs (one per line,
comments with `#` allowed). The workflow loops over it, calls the
orchestrator with `--push-r2`, and commits `data/ingest_state.json` back so
the state is persisted across CI runs.

---

## Scaling to multiple lists

Process several lists sequentially:

```bash
while IFS= read -r url; do
    [ -z "$url" ] && continue
    [[ "$url" == "#"* ]] && continue
    echo ">>> ingesting $url"
    .venv/bin/python scripts/awesome_to_wiki.py --url "$url" --push-r2
done < data/awesome_lists.txt
```

Plan for **2-4 hours per ~200-entry list** at DeepSeek's typical
throughput, plus 30-60s for R2 upload. Run overnight or on CI.

---

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| `Parsed 0 entries` | README uses tables or CSV instead of bullet lists | The orchestrator auto-detects markdown tables and `THE_RESOURCES_TABLE.csv`; if still 0, inspect README manually |
| LLM call hangs > 60s | DeepSeek rate-limit | Add `time.sleep(2)` between entries or back off in `llm_interface.py` |
| Pages have generic summaries | LLM only had the bullet's short description as context | Run with `--skip-clone=false` so the linked repo's README is also passed |
| `Failed to fetch README` | Repo was renamed, deleted, or made private | The orchestrator skips the entry and logs the error; safe to ignore |
| `RuntimeError: R2 credentials not configured` | `.env` missing | Fill in `R2_*` in `.env`; docker compose / cron loads it automatically |
| Admin UI shows "Merge failed: Read-only file system" | `./wiki:/app/wiki:ro` in docker-compose | Drop the `:ro` flag — see `docs/ADMIN_BATCH_SYNC.md` |
| `Seekdb upsert failed` | Old batch_sync.py signature | Upgrade past commit `2abcfc3`; the signature is now `upsert(ids=, documents=, metadatas=, embeddings=)` |

---

## File map (everything created by this pipeline)

```
rosclaw-wiki/
├── scripts/
│   └── awesome_to_wiki.py        ← orchestrator (this tutorial walks through it)
├── data/
│   ├── ingest_state.json         ← persistent state, "what's been processed"
│   ├── awesome_lists.txt         ← list of URLs to process weekly
│   └── raw/articles/             ← downloaded HTML/Markdown (if --skip-clone=false)
├── wiki/
│   └── skills/                   ← generated wiki pages (one per entry)
├── submissions/
│   └── <batch>.tar.gz            ← pre-upload bundles (local cache)
├── .github/workflows/
│   └── awesome-weekly-refresh.yml ← CI schedule
└── docs/
    └── TUTORIAL_AWESOME_INGEST.md ← this file
```

---

## Related

- [docs/DEPLOY.md](DEPLOY.md) — production Docker Compose layout
- [docs/ADMIN_BATCH_SYNC.md](ADMIN_BATCH_SYNC.md) — device → R2 → admin merge protocol
- [docs/ENVIRONMENT.md](ENVIRONMENT.md) — every env var and where it's read
- [`.claude/skills/rosclaw-wiki-deploy/SKILL.md`](../.claude/skills/rosclaw-wiki-deploy/SKILL.md) — operator runbook
