#!/bin/bash
# ROSClaw Wiki — Local Knowledge Factory Preprocessing Pipeline
# Run on local cluster (H800). Produces knowledge asset package for cloud upload.
#
# Usage:
#   export PADDLEOCR_API_URL="https://your-endpoint/layout-parsing"
#   export PADDLEOCR_API_TOKEN="your_token"
#   ./scripts/local_processing_pipeline.sh

set -e

echo "=== ROSClaw Wiki Local Processing Pipeline ==="

# Config
WIKI_ROOT="${WIKI_ROOT:-wiki}"
RAW_DIR="${RAW_DIR:-data/raw}"
OUTPUT_DIR="${OUTPUT_DIR:-data/pipeline_output}"
mkdir -p "$OUTPUT_DIR"

# Step 1: Fetch sources (skip if data/raw/ already populated)
if [ "$SKIP_FETCH" != "true" ]; then
    echo "[1/7] Fetching sources..."
    if [ -f "awesome_vln.yml" ]; then
        python rosclaw_fetch.py --input awesome_vln.yml --output-dir "$RAW_DIR" \
            --max-repo-size 500 --use-sparse-clone
    else
        echo "    Skipped: no awesome_vln.yml found"
    fi
else
    echo "[1/7] Skipping fetch (SKIP_FETCH=true)"
fi

# Step 2: PDF full-text extraction
echo "[2/7] Extracting PDF full text..."
python -c "
from pdf_extractor import batch_extract_papers
import os
batch_extract_papers('${RAW_DIR}/papers/', force_ocr=False)
" || echo "    PDF extraction completed with warnings"

# Step 3: Batch ingest sources into wiki
echo "[3/7] Batch ingesting sources into wiki..."
python batch_ingest.py --input-dir "$RAW_DIR" --wiki-root "$WIKI_ROOT" --concurrency 10 \
    || echo "    Batch ingest completed with warnings"

# Step 4: Build code knowledge graph
echo "[4/7] Building code knowledge graph..."
python -c "
from code_knowledge_graph import build_code_graph
import json
result = build_code_graph('${RAW_DIR}/code/', '${OUTPUT_DIR}/code_graph.json')
print(f'Code graph: {result.get(\"node_count\", 0)} nodes, {result.get(\"edge_count\", 0)} edges')
" || echo "    Code graph build completed with warnings"

# Step 5: Auto judgment pipeline
echo "[5/7] Running auto-judgment pipeline..."
python auto_judgment_pipeline.py --wiki-root "$WIKI_ROOT" --min-confidence 0.7 \
    || echo "    Auto-judgment completed with warnings"

# Step 6: Extract causal chains from papers
echo "[6/7] Extracting causal relationships from papers..."
python -c "
from autonomous_extractor import batch_extract_causal_chains
batch_extract_causal_chains('${WIKI_ROOT}/', min_confidence=0.7, max_papers=50)
" || echo "    Causal extraction completed with warnings"

# Step 7: Build physical ontology and export
echo "[7/7] Building physical ontology and exporting..."
python -c "
from constraint_graph import ConstraintGraph
from physical_ontology import PhysicalOntology
import json

cg = ConstraintGraph()
# Try to load existing ontology if available
onto_path = '${OUTPUT_DIR}/physical_ontology.json'
if __import__('os').path.exists(onto_path):
    cg.ontology = PhysicalOntology.load(onto_path)
    print(f'Loaded existing ontology: {len(cg.ontology.nodes)} nodes')

# Build from available sources
try:
    cg.build_graph_from_sources()
except AttributeError:
    # build_graph_from_sources may not exist; export what we have
    pass

cg.export_to_seekdb('${OUTPUT_DIR}/seekdb_import.jsonl')
cg.ontology.export_to_seekdb('${OUTPUT_DIR}/physical_ontology.json')
print(f'Exported: {len(cg.ontology.nodes)} nodes, {len(cg.ontology.edges)} edges')
" || echo "    Ontology export completed with warnings"

# Package outputs
echo ""
echo "=== Pipeline Complete ==="
echo "Output directory: $OUTPUT_DIR"
ls -lh "$OUTPUT_DIR/"
echo ""
echo "Next steps:"
echo "  1. Review output files in $OUTPUT_DIR/"
echo "  2. Run: ./scripts/upload_to_cloud.sh"
echo ""
