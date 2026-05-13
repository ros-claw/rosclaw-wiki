"""ROSClaw Wiki Web UI — Flask + SocketIO real-time backend.

Serves the Sigma.js frontend, exposes REST APIs, and pushes real-time
events via WebSocket (page updates, ingest progress, conflict alerts).
"""

from __future__ import annotations

import json
import logging
import os
import sys
import threading
import time
from pathlib import Path
from typing import Any

# Pre-load stdlib 'code' before sys.path gets polluted by project root
import code as _stdlib_code  # noqa: F401

_SCRIPT_DIR = Path(__file__).parent.resolve()
_PROJECT_ROOT = _SCRIPT_DIR.parent
sys.path.insert(0, str(_PROJECT_ROOT))

from flask import Flask, jsonify, request, send_from_directory
from flask_socketio import SocketIO

import wiki_engine as engine
from graph_exporter import export_graph
from research_advisor import identify_knowledge_gaps
from event_bus import tail_events

logger = logging.getLogger("rosclaw.web_ui")

app = Flask(__name__, static_folder=str(_SCRIPT_DIR / "static"))
app.config["SECRET_KEY"] = os.environ.get("FLASK_SECRET_KEY", "rosclaw-dev-secret")

# Use threading async mode (no eventlet/gevent required for local dev)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="threading")

WIKI_ROOT = os.environ.get("WIKI_ROOT", str(_PROJECT_ROOT / "wiki"))


def _get_wiki_root() -> Path:
    return Path(os.environ.get("WIKI_ROOT", str(_PROJECT_ROOT / "wiki"))).resolve()


# ── REST API Routes ──


@app.route("/api/graph")
def api_graph() -> dict[str, Any]:
    """Export current wiki as knowledge graph."""
    try:
        out_dir = _get_wiki_root().parent / "data" / "graph_export"
        result = export_graph(str(_get_wiki_root()), output_dir=str(out_dir), fmt="json")
        nodes_path = [p for p in result["output_paths"] if "nodes.json" in p][0]
        edges_path = [p for p in result["output_paths"] if "edges.json" in p][0]
        nodes = json.loads(Path(nodes_path).read_text(encoding="utf-8"))
        edges = json.loads(Path(edges_path).read_text(encoding="utf-8"))
        return jsonify({"status": "done", "nodes": nodes, "edges": edges})
    except Exception as exc:
        logger.exception("api_graph failed")
        return jsonify({"status": "error", "message": str(exc)}), 500


@app.route("/api/stats")
def api_stats() -> dict[str, Any]:
    """Return knowledge health statistics."""
    try:
        wiki = _get_wiki_root()
        pages = engine.list_pages(str(wiki))

        low_confidence = [
            {"title": p.get("title", "?"), "confidence": p.get("confidence", 0), "path": p.get("_path", "")}
            for p in pages
            if float(p.get("confidence", 1.0)) < 0.5
        ]

        from datetime import datetime, timedelta

        now = datetime.now().date()
        expired = []
        for p in pages:
            last = p.get("last_reinforced", "")
            if not last:
                continue
            try:
                last_date = datetime.fromisoformat(last).date()
                if (now - last_date).days > 30:
                    expired.append({
                        "title": p.get("title", "?"),
                        "days_since": (now - last_date).days,
                        "path": p.get("_path", ""),
                    })
            except Exception:
                continue

        gaps = identify_knowledge_gaps(str(wiki))

        return jsonify({
            "status": "done",
            "total_pages": len(pages),
            "low_confidence": {
                "count": len(low_confidence),
                "pages": low_confidence,
            },
            "expired": {
                "count": len(expired),
                "pages": expired[:20],
            },
            "gaps": {
                "isolated_count": len(gaps["isolated_nodes"]),
                "low_density_count": len(gaps["low_density_topics"]),
            },
        })
    except Exception as exc:
        logger.exception("api_stats failed")
        return jsonify({"status": "error", "message": str(exc)}), 500


@app.route("/api/search")
def api_search() -> dict[str, Any]:
    """Search wiki pages via SearchInterface abstraction."""
    from search_interface import get_search_impl

    query = request.args.get("q", "")
    search_type = request.args.get("type", "hybrid")
    limit = int(request.args.get("limit", 20))

    if not query:
        return jsonify({"status": "error", "message": "Missing query parameter 'q'"}), 400

    try:
        search_impl = get_search_impl(str(_get_wiki_root()))
        matches = search_impl.search(query, search_type=search_type, top_k=limit)
        return jsonify({"status": "done", "query": query, "search_type": search_type, "matches": matches})
    except Exception as exc:
        logger.exception("api_search failed")
        return jsonify({"status": "error", "message": str(exc)}), 500


@app.route("/api/page/<page_id>")
def api_page(page_id: str) -> dict[str, Any]:
    """Return a single wiki page by ID (slug)."""
    wiki = _get_wiki_root()
    for subdir in ["entities", "algorithms", "concepts", "skills", "episodes", "archive"]:
        candidate = wiki / subdir / f"{page_id}.md"
        if candidate.exists():
            try:
                content = candidate.read_text(encoding="utf-8")
                meta, body = engine.parse_frontmatter(content)
                return jsonify({
                    "status": "done",
                    "path": str(candidate.relative_to(wiki)),
                    "meta": meta,
                    "body": body,
                })
            except Exception as exc:
                return jsonify({"status": "error", "message": str(exc)}), 500

    for md_file in wiki.rglob("*.md"):
        if md_file.stem == page_id:
            try:
                content = md_file.read_text(encoding="utf-8")
                meta, body = engine.parse_frontmatter(content)
                return jsonify({
                    "status": "done",
                    "path": str(md_file.relative_to(wiki)),
                    "meta": meta,
                    "body": body,
                })
            except Exception as exc:
                return jsonify({"status": "error", "message": str(exc)}), 500

    return jsonify({"status": "error", "message": f"Page not found: {page_id}"}), 404


@app.route("/api/code-graph")
def api_code_graph() -> dict[str, Any]:
    """Return code knowledge graph (multi-language via tree-sitter)."""
    try:
        graph_path = _get_wiki_root().parent / "data" / "code_graph.json"
        if not graph_path.exists():
            return jsonify({"status": "empty", "nodes": [], "edges": [], "message": "No code graph found. Run: python -c 'from code_knowledge_graph import build_code_graph; build_code_graph(\\'data/raw/code\\')'"})

        graph = json.loads(graph_path.read_text(encoding="utf-8"))
        return jsonify({
            "status": "done",
            "repo_count": graph.get("repo_count", 0),
            "node_count": graph.get("node_count", 0),
            "edge_count": graph.get("edge_count", 0),
            "constraint_edge_count": graph.get("constraint_edge_count", 0),
            "nodes": graph.get("nodes", [])[:500],  # Cap for performance
            "edges": graph.get("edges", [])[:500],
        })
    except Exception as exc:
        logger.exception("api_code_graph failed")
        return jsonify({"status": "error", "message": str(exc)}), 500


@app.route("/api/gaps")
def api_gaps() -> dict[str, Any]:
    """Return gap heatmap data."""
    try:
        from visualize_gaps import generate_gap_heatmap

        out_dir = _get_wiki_root().parent / "data" / "graph_export"
        gaps_path = generate_gap_heatmap(str(_get_wiki_root()), output_dir=str(out_dir))
        data = json.loads(gaps_path.read_text(encoding="utf-8"))
        return jsonify({"status": "done", **data})
    except Exception as exc:
        logger.exception("api_gaps failed")
        return jsonify({"status": "error", "message": str(exc)}), 500


# ── SocketIO Events ──


@socketio.on("connect")
def handle_connect() -> None:
    logger.info("WebSocket client connected")
    socketio.emit("server_ready", {"message": "ROSClaw Wiki real-time feed active"})


@socketio.on("disconnect")
def handle_disconnect() -> None:
    logger.info("WebSocket client disconnected")


# ── Background event tailer ──

_tailer_running = False
_tailer_last_check = 0.0


def _event_tailer() -> None:
    """Background thread: tail event log and push to all connected clients."""
    global _tailer_last_check
    while True:
        try:
            time.sleep(1.0)
            events = tail_events(since=_tailer_last_check)
            if events:
                _tailer_last_check = events[-1]["t"]
                for evt in events:
                    socketio.emit(evt["type"], evt["payload"])
        except Exception as exc:
            logger.warning("Event tailer error: %s", exc)
            time.sleep(2.0)


# ── Frontend ──


@app.route("/")
def index() -> Any:
    """Serve the main HTML page."""
    return send_from_directory(_SCRIPT_DIR, "index.html")


@app.route("/static/<path:filename>")
def static_files(filename: str) -> Any:
    return send_from_directory(_SCRIPT_DIR / "static", filename)


@app.route("/<path:page_path>")
def wiki_page(page_path: str) -> Any:
    """Serve the SPA for any wiki page path (client-side routing)."""
    return send_from_directory(_SCRIPT_DIR, "index.html")


def main() -> int:
    logging.basicConfig(level=logging.INFO)
    global _tailer_running
    if not _tailer_running:
        _tailer_running = True
        threading.Thread(target=_event_tailer, daemon=True).start()
    socketio.run(app, host="0.0.0.0", port=5000, debug=False, use_reloader=False, allow_unsafe_werkzeug=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
