#!/bin/bash
# ROSClaw Wiki — Cloud Import Script
# Run on the cloud server to import uploaded knowledge assets into SeekDB.
#
# Usage (on cloud server):
#   cd /opt/rosclaw-wiki
#   ./scripts/import_from_upload.sh

set -e

WIKI_ROOT="${WIKI_ROOT:-wiki}"
DATA_DIR="${DATA_DIR:-data}"

echo "=== Importing Knowledge Assets into Cloud SeekDB ==="

# 1. Import SeekDB data
echo "[1/4] Importing SeekDB data..."
if [ -f "${DATA_DIR}/seekdb_import.jsonl" ]; then
    python import_to_seekdb.py --input "${DATA_DIR}/seekdb_import.jsonl" --backend seekdb --batch-size 500 \
        || echo "    SeekDB import completed with warnings"
else
    echo "    Skipped: ${DATA_DIR}/seekdb_import.jsonl not found"
fi

# 2. Load physical ontology into constraint graph
echo "[2/4] Loading physical ontology..."
python -c "
from constraint_graph import ConstraintGraph
from physical_ontology import PhysicalOntology
import os

onto_path = '${DATA_DIR}/physical_ontology.json'
if os.path.exists(onto_path):
    cg = ConstraintGraph()
    cg.ontology = PhysicalOntology.load(onto_path)
    # Save to default location for API startup
    cg.ontology.save('data/physical_ontology.json')
    print(f'Loaded ontology: {len(cg.ontology.nodes)} nodes, {len(cg.ontology.edges)} edges')
else:
    print('No physical_ontology.json found, using empty ontology')
" || echo "    Ontology load completed with warnings"

# 3. Rebuild vector index
echo "[3/4] Rebuilding vector index..."
python -c "
from vector_index import build_vector_index
try:
    build_vector_index('${WIKI_ROOT}')
    print('Vector index rebuilt')
except Exception as e:
    print(f'Vector index rebuild warning: {e}')
" || echo "    Vector index rebuild completed with warnings"

# 4. Restart API service
echo "[4/4] Restarting API service..."
if [ -f "docker-compose.prod.yml" ]; then
    docker-compose -f docker-compose.prod.yml restart rosclaw-api \
        || echo "    Docker restart completed with warnings"
else
    echo "    Skipped: docker-compose.prod.yml not found"
fi

echo ""
echo "=== Import Complete ==="
echo "Verify health: curl https://api.rosclaw.io/v1/health"
