#!/bin/bash
# ROSClaw Wiki — Knowledge Asset Upload Script
# Uploads locally processed knowledge assets to the cloud server.
#
# Usage:
#   export ROSCLAW_CLOUD_HOST="api.rosclaw.io"
#   export ROSCLAW_CLOUD_USER="root"
#   export ROSCLAW_CLOUD_PATH="/opt/rosclaw-wiki"
#   ./scripts/upload_to_cloud.sh

set -e

CLOUD_HOST="${ROSCLAW_CLOUD_HOST:-api.rosclaw.io}"
CLOUD_USER="${ROSCLAW_CLOUD_USER:-root}"
CLOUD_PATH="${ROSCLAW_CLOUD_PATH:-/opt/rosclaw-wiki}"
OUTPUT_DIR="${OUTPUT_DIR:-data/pipeline_output}"

echo "=== Uploading Knowledge Assets to Cloud Server ==="
echo "Target: ${CLOUD_USER}@${CLOUD_HOST}:${CLOUD_PATH}"

# Ensure target directory exists
ssh "${CLOUD_USER}@${CLOUD_HOST}" "mkdir -p ${CLOUD_PATH}/data ${CLOUD_PATH}/wiki/.vector_index"

# 1. Wiki Pack
echo "[1/4] Uploading wiki pack..."
if [ -f "awesome_vln_wiki_pack.json" ]; then
    scp awesome_vln_wiki_pack.json "${CLOUD_USER}@${CLOUD_HOST}:${CLOUD_PATH}/data/"
fi

# 2. SeekDB import data
echo "[2/4] Uploading SeekDB import data..."
if [ -f "${OUTPUT_DIR}/seekdb_import.jsonl" ]; then
    scp "${OUTPUT_DIR}/seekdb_import.jsonl" "${CLOUD_USER}@${CLOUD_HOST}:${CLOUD_PATH}/data/"
fi

# 3. Physical ontology
echo "[3/4] Uploading physical ontology..."
if [ -f "${OUTPUT_DIR}/physical_ontology.json" ]; then
    scp "${OUTPUT_DIR}/physical_ontology.json" "${CLOUD_USER}@${CLOUD_HOST}:${CLOUD_PATH}/data/"
fi

# 4. Code graph
echo "[4/4] Uploading code graph..."
if [ -f "${OUTPUT_DIR}/code_graph.json" ]; then
    scp "${OUTPUT_DIR}/code_graph.json" "${CLOUD_USER}@${CLOUD_HOST}:${CLOUD_PATH}/data/"
fi

echo ""
echo "=== Upload Complete ==="
echo "SSH into ${CLOUD_HOST} and run:"
echo "  cd ${CLOUD_PATH}"
echo "  ./scripts/import_from_upload.sh"
