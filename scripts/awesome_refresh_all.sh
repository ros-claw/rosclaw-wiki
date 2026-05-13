#!/usr/bin/env bash
# scripts/awesome_refresh_all.sh
# Iterate every list in data/awesome_lists.txt and run the ingest +
# R2-upload pipeline for each. Already-processed entries are skipped
# automatically via data/ingest_state.json.
#
# Usage:
#   bash scripts/awesome_refresh_all.sh
#   bash scripts/awesome_refresh_all.sh --skip-url https://github.com/ComposioHQ/awesome-claude-skills

set -uo pipefail

cd "$(dirname "$0")/.."

LOG=/tmp/awesome_refresh_all.log
LIST_FILE=data/awesome_lists.txt
SKIP_URLS=()

while [[ $# -gt 0 ]]; do
    case "$1" in
        --skip-url) SKIP_URLS+=("$2"); shift 2;;
        *) echo "Unknown arg: $1" >&2; exit 64;;
    esac
done

if [[ ! -f "$LIST_FILE" ]]; then
    echo "Missing $LIST_FILE" >&2
    exit 1
fi

if [[ -z "${DEEPSEEK_API_KEY:-}" ]]; then
    echo "DEEPSEEK_API_KEY not set in env" >&2
    exit 1
fi
if [[ -z "${R2_ENDPOINT:-}" || -z "${R2_ACCESS_KEY_ID:-}" || -z "${R2_SECRET_ACCESS_KEY:-}" ]]; then
    echo "R2 credentials not set in env" >&2
    exit 1
fi

echo "==== awesome refresh started at $(date -u +%FT%TZ) ====" | tee -a "$LOG"

total=0
ok=0
failed=0
skipped=0

while IFS= read -r raw; do
    line="$(printf '%s' "$raw" | sed -E 's/^[[:space:]]+|[[:space:]]+$//g')"
    [[ -z "$line" || "$line" == \#* ]] && continue
    total=$((total + 1))

    skip_this=0
    for skip in "${SKIP_URLS[@]:-}"; do
        if [[ "$line" == "$skip" ]]; then
            skip_this=1
            break
        fi
    done
    if [[ $skip_this -eq 1 ]]; then
        echo ">>> [SKIP] $line"            | tee -a "$LOG"
        skipped=$((skipped + 1))
        continue
    fi

    echo ">>> [$total] ingesting $line at $(date -u +%FT%TZ)" | tee -a "$LOG"

    if .venv/bin/python scripts/awesome_to_wiki.py --url "$line" --push-r2 2>&1 | tee -a "$LOG"; then
        ok=$((ok + 1))
        echo "<<< [$total] OK $line at $(date -u +%FT%TZ)"  | tee -a "$LOG"
    else
        failed=$((failed + 1))
        echo "!!! [$total] FAILED $line at $(date -u +%FT%TZ)" | tee -a "$LOG"
    fi
done < "$LIST_FILE"

echo "==== awesome refresh finished at $(date -u +%FT%TZ): total=$total ok=$ok failed=$failed skipped=$skipped ====" | tee -a "$LOG"
exit 0
