#!/usr/bin/env bash
# ROSClaw Wiki — One-Click Deployment Script (Phase 15)
# Usage: bash scripts/setup.sh [--mode=embedded|server]
#
# Performs:
#   1. Python version check (>=3.10)
#   2. Virtual environment creation
#   3. Dependency installation
#   4. SeekDB server startup (default: server mode)
#   5. SeekDB initialization & health check
#   6. Vector index build
#   7. Code knowledge graph pre-scan (multi-language via tree-sitter)
#   8. Search warmup
#   9. Final health verification

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
VENV_DIR="${PROJECT_ROOT}/.venv"
WIKI_ROOT="${PROJECT_ROOT}/wiki"
DATA_DIR="${PROJECT_ROOT}/data"
REQUIREMENTS="${PROJECT_ROOT}/requirements.txt"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log_info() { echo -e "${GREEN}[INFO]${NC} $*"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $*"; }
log_error() { echo -e "${RED}[ERROR]${NC} $*"; }

# ── Mode selection ──
SEEKDB_MODE="server"
for arg in "$@"; do
    case "$arg" in
        --mode=embedded)
            SEEKDB_MODE="embedded"
            log_info "SeekDB mode: embedded (local .so, single-process only)"
            ;;
        --mode=server)
            SEEKDB_MODE="server"
            log_info "SeekDB mode: server (single-node, 50+ concurrent)"
            ;;
    esac
done

export SEEKDB_MODE

# ── Step 1: Python version check ──
log_info "Checking Python version..."
PYTHON_CMD=""
for cmd in python3.11 python3.10 python3 python; do
    if command -v "$cmd" >/dev/null 2>&1; then
        version=$($cmd --version 2>&1 | awk '{print $2}')
        major=$(echo "$version" | cut -d. -f1)
        minor=$(echo "$version" | cut -d. -f2)
        if [ "$major" -gt 3 ] || { [ "$major" -eq 3 ] && [ "$minor" -ge 10 ]; }; then
            PYTHON_CMD=$cmd
            log_info "Found Python $version ($cmd)"
            break
        fi
    fi
done

if [ -z "$PYTHON_CMD" ]; then
    log_error "Python 3.10+ is required but not found."
    exit 1
fi

# ── Step 2: Virtual environment ──
log_info "Setting up virtual environment..."
if [ ! -d "$VENV_DIR" ]; then
    $PYTHON_CMD -m venv "$VENV_DIR"
    log_info "Created virtual environment at $VENV_DIR"
else
    log_warn "Virtual environment already exists at $VENV_DIR"
fi

# shellcheck source=/dev/null
source "$VENV_DIR/bin/activate"

# ── Step 3: Dependency installation ──
log_info "Installing dependencies..."
pip install --quiet --upgrade pip setuptools wheel

if [ -f "$REQUIREMENTS" ]; then
    pip install --quiet -r "$REQUIREMENTS"
    log_info "Installed dependencies from requirements.txt"
else
    log_warn "requirements.txt not found; installing core packages only"
    pip install --quiet fastapi uvicorn requests pyyaml html2text pytest
fi

# Optional: tree-sitter + language parsers (multi-language AST)
if pip install --quiet tree-sitter tree-sitter-python tree-sitter-cpp tree-sitter-go tree-sitter-javascript tree-sitter-typescript 2>/dev/null; then
    log_info "tree-sitter + language parsers installed"
else
    log_warn "tree-sitter installation partial (some languages will use Python ast fallback)"
fi

# Optional: sentence-transformers for vector indexing
if pip install --quiet sentence-transformers 2>/dev/null; then
    log_info "sentence-transformers installed"
else
    log_warn "sentence-transformers installation skipped (vector search disabled)"
fi

# Optional: pyseekdb
if pip install --quiet pyseekdb 2>/dev/null; then
    log_info "pyseekdb installed"
else
    log_warn "pyseekdb not available; using SQLite compatibility mode"
fi

# ── Step 4: Directory structure ──
log_info "Ensuring directory structure..."
mkdir -p "$DATA_DIR"/raw/{papers,code,articles}
mkdir -p "$DATA_DIR"/prs
mkdir -p "$WIKI_ROOT"/{entities,algorithms,concepts,skills,episodes,archive}

if [ ! -f "$WIKI_ROOT/index.md" ]; then
    cat > "$WIKI_ROOT/index.md" <<'EOF'
---
id: index
type: index
created_at: 2024-01-01
---

# ROSClaw Wiki Index

Welcome to the ROSClaw embodied-intelligence knowledge engine.

## Catalog

- [[Entities]]
- [[Algorithms]]
- [[Concepts]]
- [[Skills]]
- [[Episodes]]
EOF
    log_info "Created wiki/index.md"
fi

if [ ! -f "$WIKI_ROOT/log.md" ]; then
    cat > "$WIKI_ROOT/log.md" <<'EOF'
---
id: log
type: log
created_at: 2024-01-01
---

# ROSClaw Wiki Log

EOF
    log_info "Created wiki/log.md"
fi

# ── Step 4b: SeekDB server startup (server mode only) ──
if [ "$SEEKDB_MODE" = "server" ]; then
    log_info "Starting SeekDB single-node server..."
    SEEKDB_DATA="${PROJECT_ROOT}/seekdb_data"
    mkdir -p "$SEEKDB_DATA"

    # Check if observer binary exists
    SEEKDB_OBSERVER="${PROJECT_ROOT}/seekdb/bin/observer"
    if [ ! -f "$SEEKDB_OBSERVER" ]; then
        log_warn "SeekDB observer binary not found at ${SEEKDB_OBSERVER}"
        log_warn "Please compile SeekDB first: cd seekdb && bash build.sh debug --init --make"
        log_warn "Falling back to SQLite compatibility mode"
        SEEKDB_MODE="embedded"
        export SEEKDB_MODE
    else
        if ! pgrep -f "seekdb.*-p 2881" >/dev/null 2>&1; then
            nohup "$SEEKDB_OBSERVER" -p 2881 -d "$SEEKDB_DATA" >"${SEEKDB_DATA}/observer.log" 2>&1 &
            log_info "SeekDB server starting on port 2881 (log: ${SEEKDB_DATA}/observer.log)"
            sleep 3
            if mysql -h127.0.0.1 -P2881 -uroot -e "SELECT 1" >/dev/null 2>&1; then
                log_info "SeekDB server ready"
            else
                log_warn "SeekDB server may still be initializing; will retry on first connection"
            fi
        else
            log_info "SeekDB server already running on port 2881"
        fi
    fi
else
    log_info "SeekDB embedded mode selected (single-process, no server startup)"
fi

# ── Step 5: SeekDB initialization ──
log_info "Initializing SeekDB / SQLite compatibility layer..."
python3 <<PYEOF
import sys, os
sys.path.insert(0, "${PROJECT_ROOT}")
os.chdir("${PROJECT_ROOT}")
from seekdb_client import SeekDBClient
client = SeekDBClient()
health = client.health()
print(f"Backend: {health['backend']}, Pages: {health.get('pages', 0)}")
PYEOF

# ── Step 6: Vector index build ──
log_info "Building vector index (if sentence-transformers available)..."
python3 <<PYEOF
import sys, os, warnings
sys.path.insert(0, "${PROJECT_ROOT}")
os.chdir("${PROJECT_ROOT}")
try:
    from vector_index import build_vector_index
    count = build_vector_index("${WIKI_ROOT}")
    print(f"Indexed {count} pages")
except Exception as exc:
    print(f"Vector index skipped: {exc}")
PYEOF

# ── Step 7: Code knowledge graph pre-scan ──
log_info "Pre-scanning code knowledge graph..."
python3 <<PYEOF
import sys, os
sys.path.insert(0, "${PROJECT_ROOT}")
os.chdir("${PROJECT_ROOT}")
try:
    from code_knowledge_graph import build_code_graph
    graph = build_code_graph("data/raw/code", "data/code_graph.json")
    print(f"Nodes: {graph['node_count']}, Edges: {graph['edge_count']}, Repos: {graph['repo_count']}")
except Exception as exc:
    print(f"Code graph scan skipped: {exc}")
PYEOF

# ── Step 8: Search warmup ──
log_info "Warming up search backend..."
python3 <<PYEOF
import sys, os
sys.path.insert(0, "${PROJECT_ROOT}")
os.chdir("${PROJECT_ROOT}")
try:
    from seekdb_search_impl import SeekDBSearchImpl
    SeekDBSearchImpl.warmup("${WIKI_ROOT}")
    print("Search backend warmed up")
except Exception as exc:
    print(f"Search warmup skipped: {exc}")
PYEOF

# ── Step 9: Health verification ──
log_info "Running health check..."
python3 <<PYEOF
import sys, os, json
sys.path.insert(0, "${PROJECT_ROOT}")
os.chdir("${PROJECT_ROOT}")
from seekdb_client import health_check
h = health_check()
print(json.dumps(h, indent=2))

# Also verify collection client mode
from seekdb_collection_client import health_check as coll_health
ch = coll_health()
print(f"Collection client: {ch.get('mode', 'unknown')} mode, status={ch.get('status')}")
PYEOF

# ── Step 10: Test suite ──
log_info "Running test suite..."
cd "$PROJECT_ROOT"
if python3 -m pytest --ignore=data --ignore=scripts -q --tb=line 2>&1 | tail -5; then
    log_info "Test suite completed"
else
    log_warn "Some tests failed (see output above)"
fi

# ── Done ──
log_info "========================================"
log_info "ROSClaw Wiki setup complete!"
log_info "Project root: ${PROJECT_ROOT}"
log_info "Virtual env:  ${VENV_DIR}"
log_info "Activate:     source ${VENV_DIR}/bin/activate"
log_info "SeekDB mode:  ${SEEKDB_MODE}"
log_info "Run API:      uvicorn commercial_api:app --reload"
log_info "Run tests:    pytest --ignore=data --ignore=scripts"
log_info "Web UI:       python web_ui/app.py"
log_info "========================================"
