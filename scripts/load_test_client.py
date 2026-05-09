"""Load test ROSClaw Wiki API using FastAPI TestClient (no server needed).

Usage:
    python scripts/load_test_client.py --concurrency 50 --duration 30
"""
from __future__ import annotations

import argparse
import asyncio
import json
import statistics
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from fastapi.testclient import TestClient

from commercial_api import app

client = TestClient(app)

QUERIES = [
    {"query": "visual language navigation", "search_type": "keyword"},
    {"query": "robot torque control", "search_type": "semantic"},
    {"query": "G1 gait parameters", "search_type": "hybrid"},
    {"query": "R2R dataset navigation", "search_type": "expanded"},
]

API_KEY = "rw_P7-wfcUELEaMo_aICGcxsseDgJO0bLrbOGZ6-SSWBfM"


def _request(body: dict) -> tuple[float, int, str]:
    """Make a single request, return (latency_ms, status, error)."""
    start = time.time()
    try:
        resp = client.post(
            "/v1/search",
            json=body,
            headers={"X-API-Key": API_KEY},
        )
        latency = (time.time() - start) * 1000
        return latency, resp.status_code, ""
    except Exception as exc:
        latency = (time.time() - start) * 1000
        return latency, 0, str(exc)


def run_load_test(concurrency: int, duration: float) -> dict:
    results: list[float] = []
    errors: list[str] = []
    total_requests = 0

    # Warm-up
    try:
        r = client.get("/v1/health")
        print(f"Health check: {r.status_code}")
    except Exception as exc:
        print(f"Health check failed: {exc}")
        return {"error": str(exc)}

    start = time.time()
    end_time = start + duration

    with ThreadPoolExecutor(max_workers=concurrency) as executor:
        futures = []
        while time.time() < end_time:
            body = QUERIES[total_requests % len(QUERIES)]
            futures.append(executor.submit(_request, body))
            total_requests += 1
            # Don't overwhelm the executor queue
            if len(futures) > concurrency * 4:
                done = [f for f in futures if f.done()]
                for f in done:
                    lat, status, err = f.result()
                    if err:
                        errors.append(err)
                    elif status != 200:
                        errors.append(f"HTTP {status}")
                    else:
                        results.append(lat)
                    futures.remove(f)

        # Drain remaining
        for f in futures:
            lat, status, err = f.result()
            if err:
                errors.append(err)
            elif status != 200:
                errors.append(f"HTTP {status}")
            else:
                results.append(lat)

    elapsed = time.time() - start
    results.sort()
    total = len(results)
    error_count = len(errors)

    if total == 0:
        return {"error": "No successful requests", "errors": errors[:10]}

    p50 = results[int(total * 0.50)]
    p90 = results[int(total * 0.90)]
    p99 = results[int(total * 0.99)]
    mean = statistics.mean(results)
    rps = total / elapsed

    return {
        "total_requests": total,
        "errors": error_count,
        "error_rate": round(error_count / (total + error_count) * 100, 2),
        "duration_sec": round(elapsed, 2),
        "rps": round(rps, 2),
        "latency_ms": {
            "mean": round(mean, 2),
            "p50": round(p50, 2),
            "p90": round(p90, 2),
            "p99": round(p99, 2),
            "min": round(results[0], 2),
            "max": round(results[-1], 2),
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Load test ROSClaw Wiki API")
    parser.add_argument("--concurrency", type=int, default=50)
    parser.add_argument("--duration", type=float, default=30)
    args = parser.parse_args()

    print(f"Load test: {args.concurrency} concurrent, {args.duration}s duration")
    print("Using FastAPI TestClient (no external server needed)")

    result = run_load_test(args.concurrency, args.duration)
    print(json.dumps(result, indent=2))

    p99 = result.get("latency_ms", {}).get("p99", float("inf"))
    error_rate = result.get("error_rate", 100)
    if p99 < 500 and error_rate == 0:
        print("\n✅ PASS: P99 < 500ms, 0% error rate")
        return 0
    else:
        print(f"\n❌ FAIL: P99={p99}ms, error_rate={error_rate}%")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
