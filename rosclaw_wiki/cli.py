"""ROSClaw Wiki CLI — Knowledge forging and upload tool."""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
import tarfile
from pathlib import Path

import requests

API_BASE = os.environ.get("ROSCLAW_API_BASE", "https://api.rosclaw.io")


def _ensure_input_exists(input_path: str) -> None:
    p = Path(input_path)
    if not p.exists():
        print(f"Error: Input path does not exist: {input_path}")
        sys.exit(1)


def forge(args: argparse.Namespace) -> None:
    """Local forge: transform papers/code folder into a Wiki Pack."""
    _ensure_input_exists(args.input)
    print(f"Forge: {args.input} -> {args.name}")

    # Call Phase 18 local processing pipeline
    cmd = [
        "bash", "scripts/local_processing_pipeline.sh",
        "--input", args.input,
        "--name", args.name,
    ]
    if args.awesome_url:
        cmd.extend(["--awesome-url", args.awesome_url])
    subprocess.run(cmd, check=True)

    # Pack
    tar_name = f"{args.name}.tar.gz"
    print(f"Packing: {tar_name}")
    with tarfile.open(tar_name, "w:gz") as tf:
        for path in ["wiki", "data/seekdb_import.jsonl", "data/code_graph.json", "data/judgments"]:
            p = Path(path)
            if p.exists():
                tf.add(p, arcname=p.name)
    print(f"Forge complete: {tar_name}")


def push(args: argparse.Namespace) -> None:
    """Upload Wiki Pack to ROSClaw cloud."""
    api_key = args.api_key or os.environ.get("ROSCLAW_API_KEY")
    if not api_key:
        print("Error: ROSCLAW_API_KEY not set. Set via --api-key or ROSCLAW_API_KEY env var.")
        sys.exit(1)

    file_path = Path(f"{args.name}.tar.gz")
    if not file_path.exists():
        print(f"Error: Pack not found: {file_path}")
        sys.exit(1)

    file_size = file_path.stat().st_size

    # 1. Request upload URL
    print("Requesting upload URL...")
    r = requests.post(
        f"{API_BASE}/wiki/v1/upload/request",
        json={
            "file_name": file_path.name,
            "file_size": file_size,
            "wiki_name": args.name,
        },
        headers={"X-API-Key": api_key},
        timeout=30,
    )
    r.raise_for_status()
    upload_info = r.json()

    # 2. Upload directly to R2 (S3 credentials never exposed to user)
    print(f"Uploading to cloud storage ({file_size / 1024 / 1024:.1f} MB)...")
    with file_path.open("rb") as f:
        r = requests.put(upload_info["presigned_url"], data=f, timeout=300)
    r.raise_for_status()

    # 3. Notify server to import
    print("Notifying server...")
    r = requests.post(
        f"{API_BASE}/wiki/v1/upload/complete",
        json={"upload_id": upload_info["upload_id"]},
        headers={"X-API-Key": api_key},
        timeout=60,
    )
    r.raise_for_status()
    result = r.json()
    print(f"Done: {result.get('pages_imported', 0)} pages, {result.get('judgments_added', 0)} judgments added.")


def main() -> int:
    parser = argparse.ArgumentParser(description="ROSClaw Wiki — Steward of Embodied Physical Reality")
    subparsers = parser.add_subparsers(dest="command")

    # forge
    forge_parser = subparsers.add_parser("forge", help="Forge a Wiki from papers/code")
    forge_parser.add_argument("--input", required=True, help="Path to papers/code folder")
    forge_parser.add_argument("--name", required=True, help="Wiki name")
    forge_parser.add_argument("--awesome-url", help="GitHub Awesome List URL")
    forge_parser.add_argument("--push", action="store_true", help="Push after forging")
    forge_parser.add_argument("--api-key", help="ROSClaw API Key")

    # push
    push_parser = subparsers.add_parser("push", help="Push a Wiki to ROSClaw cloud")
    push_parser.add_argument("--name", required=True, help="Wiki name")
    push_parser.add_argument("--api-key", help="ROSClaw API Key")

    args = parser.parse_args()

    if args.command == "forge":
        forge(args)
        if args.push:
            push(args)
    elif args.command == "push":
        push(args)
    else:
        parser.print_help()
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
