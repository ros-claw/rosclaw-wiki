"""Generate performance comparison report between Phase 10 and Phase 11."""
from __future__ import annotations

import json
import os
from pathlib import Path


def _avg(latencies: list[float]) -> float:
    return round(sum(latencies) / len(latencies), 2) if latencies else 0.0


def _pct_change(old: float, new: float) -> str:
    if old == 0:
        return "N/A"
    change = ((new - old) / old) * 100
    sign = "+" if change > 0 else ""
    return f"{sign}{change:.1f}%"


def generate() -> None:
    base = Path(__file__).parent / "data" / "benchmarks"
    p10_path = base / "phase10_baseline.json"
    p11_path = base / "phase11_seekdb.json"

    with open(p10_path, "r", encoding="utf-8") as f:
        p10 = json.load(f)
    with open(p11_path, "r", encoding="utf-8") as f:
        p11 = json.load(f)

    # Group by query type
    def group(queries: list[dict]) -> dict[str, list[float]]:
        g: dict[str, list[float]] = {}
        for q in queries:
            g.setdefault(q["type"], []).append(q["latency_ms"])
        return g

    g10 = group(p10["queries"])
    g11 = group(p11["queries"])

    lines: list[str] = []
    lines.append("# Performance Comparison: Phase 10 vs Phase 11")
    lines.append("")
    lines.append("| Metric | Phase 10 (Filesystem) | Phase 11 (SeekDB/SQLite) | Change |")
    lines.append("|--------|----------------------|--------------------------|--------|")

    s10 = p10["summary"]
    s11 = p11["summary"]
    lines.append(
        f"| Overall Avg | {s10['avg_latency_ms']}ms | {s11['avg_latency_ms']}ms | {_pct_change(s10['avg_latency_ms'], s11['avg_latency_ms'])} |"
    )
    lines.append(
        f"| Max | {s10['max_latency_ms']}ms | {s11['max_latency_ms']}ms | {_pct_change(s10['max_latency_ms'], s11['max_latency_ms'])} |"
    )
    lines.append(
        f"| Min | {s10['min_latency_ms']}ms | {s11['min_latency_ms']}ms | {_pct_change(s10['min_latency_ms'], s11['min_latency_ms'])} |"
    )
    lines.append("")

    lines.append("## By Query Type")
    lines.append("")
    lines.append("| Type | Phase 10 Avg | Phase 11 Avg | Change | Queries |")
    lines.append("|------|-------------|-------------|--------|---------|")
    for qtype in sorted(set(g10.keys()) | set(g11.keys())):
        a10 = _avg(g10.get(qtype, []))
        a11 = _avg(g11.get(qtype, []))
        n = len(g10.get(qtype, []))
        lines.append(
            f"| {qtype} | {a10}ms | {a11}ms | {_pct_change(a10, a11)} | {n} |"
        )
    lines.append("")

    lines.append("## Key Observations")
    lines.append("")
    lines.append("1. **Overall latency increase**: SeekDB SQLite backend is ~45% slower on average.")
    lines.append("2. **Keyword search**: Slightly slower due to FTS5 overhead vs direct file reads.")
    lines.append("3. **Semantic search**: Similar latency (both use sentence-transformers in-memory).")
    lines.append("4. **Hybrid search**: ~2x slower due to RRF fusion across keyword + vector results.")
    lines.append("5. **Judgment queries**: Sub-millisecond in both backends (SQLite indexed lookup).")
    lines.append("6. **Trade-off**: SeekDB backend provides structured storage, ACID transactions, and")
    lines.append("   horizontal scalability path — acceptable latency cost for production features.")
    lines.append("")

    lines.append("## Environment")
    lines.append(f"- Phase 10 timestamp: {s10['timestamp']}")
    lines.append(f"- Phase 11 timestamp: {s11['timestamp']}")
    lines.append(f"- Total queries per run: {s10['total_queries']}")
    lines.append("")

    out_path = base / "perf_comparison.md"
    out_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"Generated {out_path}")


if __name__ == "__main__":
    generate()
