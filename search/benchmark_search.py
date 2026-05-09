"""Search Benchmark — performance baseline for Phase 10.

Runs 30 representative queries across keyword, semantic, hybrid, expanded,
and judgment search types. Records latency and stores to JSON.
"""

from __future__ import annotations

import json
import logging
import time
from pathlib import Path
from typing import Any

logger = logging.getLogger("rosclaw.benchmark")

# 30 representative embodied-intelligence queries
BENCHMARK_QUERIES: list[dict[str, Any]] = [
    # Keyword-heavy
    {"query": "robot locomotion", "type": "keyword"},
    {"query": "grasping policy", "type": "keyword"},
    {"query": "simulation to real", "type": "keyword"},
    {"query": "reinforcement learning humanoid", "type": "keyword"},
    {"query": "tactile sensing", "type": "keyword"},
    {"query": "motion planning", "type": "keyword"},
    {"query": "ROS2 navigation", "type": "keyword"},
    {"query": "imitation learning", "type": "keyword"},
    {"query": "depth estimation", "type": "keyword"},
    {"query": "collision avoidance", "type": "keyword"},
    # Semantic
    {"query": "how do robots learn to walk", "type": "semantic"},
    {"query": "vision language model for manipulation", "type": "semantic"},
    {"query": "embodied AI architecture", "type": "semantic"},
    {"query": "end-to-end robot control", "type": "semantic"},
    {"query": "zero-shot generalization robotics", "type": "semantic"},
    # Hybrid
    {"query": "quadruped walking controller", "type": "hybrid"},
    {"query": "dexterous hand grasp", "type": "hybrid"},
    {"query": "bipedal balance control", "type": "hybrid"},
    {"query": "autonomous navigation indoor", "type": "hybrid"},
    {"query": "multi-modal perception robot", "type": "hybrid"},
    # Expanded (no LLM, uses simple expansion)
    {"query": "what is the best walking gait", "type": "expanded"},
    {"query": "how does VLN work", "type": "expanded"},
    {"query": "reward shaping for robot learning", "type": "expanded"},
    {"query": "domain randomization simulation", "type": "expanded"},
    {"query": "locomotion policy transfer", "type": "expanded"},
    # Judgment
    {"query": "step_height", "type": "judgment"},
    {"query": "max_velocity", "type": "judgment"},
    {"query": "joint_limit", "type": "judgment"},
    {"query": "safety_margin", "type": "judgment"},
    {"query": "control_frequency", "type": "judgment"},
    # Code-aware
    {"query": "ROS2 controller implementation", "type": "keyword"},
    {"query": "gym environment wrapper", "type": "keyword"},
    {"query": "MCP tool server", "type": "keyword"},
    {"query": "vector index build", "type": "keyword"},
    {"query": "wiki engine update page", "type": "keyword"},
]


def benchmark_search(wiki_root: str, output_path: str | None = None) -> dict[str, Any]:
    """Run benchmark suite and save results.

    Args:
        wiki_root: Path to wiki root.
        output_path: Where to save results. Defaults to data/benchmarks/phase10_baseline.json.

    Returns:
        Summary with results list and aggregate stats.
    """
    if output_path is None:
        output_path = "data/benchmarks/phase10_baseline.json"

    from search_interface import FileSystemSearchImpl

    search = FileSystemSearchImpl(wiki_root)
    results: list[dict[str, Any]] = []

    for item in BENCHMARK_QUERIES:
        start = time.perf_counter()
        try:
            hits = search.search(item["query"], search_type=item["type"], top_k=10)
            status = "ok"
            result_count = len(hits)
        except Exception as exc:
            status = "error"
            result_count = 0
            logger.warning("Benchmark query failed: %s", exc)

        latency_ms = round((time.perf_counter() - start) * 1000, 2)
        results.append({
            "query": item["query"],
            "type": item["type"],
            "latency_ms": latency_ms,
            "status": status,
            "result_count": result_count,
        })

    # Aggregate stats
    latencies = [r["latency_ms"] for r in results if r["status"] == "ok"]
    summary = {
        "total_queries": len(results),
        "successful": len(latencies),
        "failed": len(results) - len(latencies),
        "avg_latency_ms": round(sum(latencies) / len(latencies), 2) if latencies else 0,
        "max_latency_ms": max(latencies) if latencies else 0,
        "min_latency_ms": min(latencies) if latencies else 0,
        "backend": "filesystem",
        "timestamp": __import__("datetime").datetime.now().isoformat(),
    }

    output = {
        "summary": summary,
        "queries": results,
    }

    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
    logger.info("Benchmark saved: %s", out)
    return output


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser(description="Search performance benchmark")
    parser.add_argument("--wiki-root", default="wiki", help="Wiki root")
    parser.add_argument("--output", default="data/benchmarks/phase10_baseline.json", help="Output JSON")
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO)
    result = benchmark_search(args.wiki_root, args.output)
    print(f"Benchmark complete: {result['summary']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


__all__ = ["benchmark_search", "BENCHMARK_QUERIES"]
