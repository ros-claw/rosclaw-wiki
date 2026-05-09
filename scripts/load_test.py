"""Python load tester for ROSClaw Wiki API.

Usage:
    # Terminal 1: start server
    python -m uvicorn commercial_api:app --host 127.0.0.1 --port 8000

    # Terminal 2: run load test
    python scripts/load_test.py --concurrency 50 --duration 30
"""
from __future__ import annotations

import argparse
import asyncio
import json
import statistics
import sys
import time
from pathlib import Path

import aiohttp

sys.path.insert(0, str(Path(__file__).parent.parent))

QUERIES = [
    '{"query": "visual language navigation", "search_type": "keyword"}',
    '{"query": "robot torque control", "search_type": "semantic"}',
    '{"query": "G1 gait parameters", "search_type": "hybrid"}',
    '{"query": "R2R dataset navigation", "search_type": "expanded"}',
]

API_KEY = "rw_P7-wfcUELEaMo_aICGcxsseDgJO0bLrbOGZ6-SSWBfM"


async def _worker(
    session: aiohttp.ClientSession,
    url: str,
    duration: float,
    results: list[float],
    errors: list[str],
) -> None:
    end_time = time.time() + duration
    while time.time() < end_time:
        body = QUERIES[int(time.time() * 1000) % len(QUERIES)]
        start = time.time()
        try:
            async with session.post(
                url,
                data=body,
                headers={"X-API-Key": API_KEY, "Content-Type": "application/json"},
            ) as resp:
                await resp.read()
                latency = (time.time() - start) * 1000
                results.append(latency)
                if resp.status != 200:
                    errors.append(f"HTTP {resp.status}")
        except Exception as exc:
            errors.append(str(exc))
            await asyncio.sleep(0.1)


async def run_load_test(url: str, concurrency: int, duration: float) -> dict:
    results: list[float] = []
    errors: list[str] = []

    timeout = aiohttp.ClientTimeout(total=30)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        # Warm-up
        try:
            async with session.get(url.replace("/v1/search", "/v1/health")) as resp:
                await resp.read()
                print(f"Health check: {resp.status}")
        except Exception as exc:
            print(f"Health check failed: {exc}")
            return {"error": str(exc)}

        tasks = [
            asyncio.create_task(_worker(session, url, duration, results, errors))
            for _ in range(concurrency)
        ]
        start = time.time()
        await asyncio.gather(*tasks)
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
    parser.add_argument("--url", default="http://127.0.0.1:8000/v1/search")
    parser.add_argument("--concurrency", type=int, default=50)
    parser.add_argument("--duration", type=float, default=30)
    args = parser.parse_args()

    print(f"Load test: {args.concurrency} concurrent, {args.duration}s duration")
    print(f"Target: {args.url}")

    result = asyncio.run(run_load_test(args.url, args.concurrency, args.duration))
    print(json.dumps(result, indent=2))

    # Pass/fail criteria
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
