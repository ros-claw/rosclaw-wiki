#!/bin/bash
set -e

echo "=== ROSClaw Wiki Phase 8: Awesome-VLN Demo ==="

# Step 1: Pull Awesome-VLN repo
if [ ! -d "/tmp/awesome-vln" ]; then
    echo "[1/5] Cloning Awesome-VLN..."
    git clone https://github.com/KwanWaiPang/Awesome-VLN.git /tmp/awesome-vln --depth=1
else
    echo "[1/5] Awesome-VLN already cloned, skipping..."
fi

# Step 2: Generate Fetcher-compatible YAML
echo "[2/5] Generating awesome_vln.yml..."
python generate_awesome_list.py --input /tmp/awesome-vln/README.md --output awesome_vln.yml

# Step 3: Fetch all resources
echo "[3/5] Downloading papers, code repos, articles..."
python rosclaw_fetch.py --input awesome_vln.yml --output-dir data/raw/ --max-repo-size 500 --concurrency 10

# Step 4: Run full workflow
echo "[4/5] Running auto-ingest, entity linking, conflict resolution, judgment generation..."
python workflow_orchestrator.py --run-all --concurrency 10

# Step 5: Generate Wiki Pack and Test Report
echo "[5/5] Generating Wiki Pack and Test Report..."
python wiki_hub.py pack --name "Awesome-VLN-Wiki" --output awesome_vln_wiki_pack.json

echo "=== Demo Complete ==="
echo "Wiki pages: $(find wiki/ -name '*.md' | wc -l)"
echo "Judgments:  $(ls wiki/judgments/ 2>/dev/null | wc -l)"
echo "Wiki Pack:  awesome_vln_wiki_pack.json"
echo "Test Report: TEST_REPORT_VLN_DEMO.md"
