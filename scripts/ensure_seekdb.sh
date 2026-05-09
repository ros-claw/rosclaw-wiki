#!/bin/bash
# Phase 13 Environment Check Script
set -e

echo "=== ROSClaw Wiki Phase 13 Environment Check ==="

# 1. Python version
echo "Python: $(python --version 2>&1)"

# 2. pyseekdb
if python -c "import pyseekdb" 2>/dev/null; then
    echo "pyseekdb: OK ($(python -c 'import pyseekdb; print(pyseekdb.__version__)'))"
else
    echo "pyseekdb: MISSING"
    if [ -f ".venv/bin/python" ]; then
        echo "  Hint: Use .venv/bin/python which has pyseekdb installed"
        echo "  Run: .venv/bin/python -m pytest test_e2e.py"
    else
        echo "  Run: pip install -U pyseekdb"
    fi
    exit 1
fi

# 3. SeekDB health check
python -c "
from seekdb_collection_client import health_check
h = health_check()
assert h.get('status') == 'ok', f'Health check failed: {h}'
print(f'SeekDB: OK (collections: {h.get(\"collections\", 0)}, pages: {h.get(\"wiki_pages\", 0)}, judgments: {h.get(\"judgments\", 0)})')
"

# 4. Warm-up
python -c "
from seekdb_search_impl import SeekDBSearchImpl
SeekDBSearchImpl.warmup('./wiki')
print('Warm-up: OK')
"

echo "=== Environment ready for Phase 13 ==="
