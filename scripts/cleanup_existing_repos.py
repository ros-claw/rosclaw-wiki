#!/usr/bin/env python3
"""Phase 18: Clean up existing cloned repos by applying SKIP_PATTERNS.

Usage:
    python scripts/cleanup_existing_repos.py --dir data/raw/code/
"""

from __future__ import annotations

import argparse
import os
import shutil
import sys
from pathlib import Path

# Replicate SKIP_PATTERNS from rosclaw_fetch.py
SKIP_PATTERNS = [
    "*.bin", "*.pth", "*.pt", "*.onnx", "*.pb", "*.h5", "*.ckpt",
    "*.weights", "*.safetensors", "*.tar", "*.tar.gz", "*.zip",
    "data/", "datasets/", "models/", "checkpoints/", "logs/",
    "wandb/", "mlruns/", "runs/", "outputs/",
    "node_modules/", ".git/", "__pycache__/", "*.pyc",
    "notebooks/", "examples/", "demos/", "assets/",
    "*.gitattributes",
]


def get_dir_size(path: Path) -> int:
    total = 0
    for entry in path.rglob("*"):
        if entry.is_file():
            total += entry.stat().st_size
    return total


def cleanup_repo(repo_dir: Path) -> dict[str, int]:
    """Apply SKIP_PATTERNS to a single repo. Returns stats."""
    removed_files = 0
    removed_dirs = 0
    bytes_saved = 0

    for pattern in SKIP_PATTERNS:
        if pattern.endswith("/"):
            dir_name = pattern.rstrip("/")
            for subdir in list(repo_dir.rglob(dir_name)):
                if subdir.is_dir():
                    size = get_dir_size(subdir)
                    try:
                        shutil.rmtree(subdir)
                        removed_dirs += 1
                        bytes_saved += size
                    except Exception:
                        pass
        else:
            for fp in list(repo_dir.rglob(pattern)):
                if fp.is_file():
                    size = fp.stat().st_size
                    try:
                        fp.unlink()
                        removed_files += 1
                        bytes_saved += size
                    except Exception:
                        pass

    return {
        "removed_files": removed_files,
        "removed_dirs": removed_dirs,
        "bytes_saved": bytes_saved,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Clean up existing repos")
    parser.add_argument("--dir", default="data/raw/code", help="Code repos directory")
    args = parser.parse_args()

    root = Path(args.dir)
    if not root.exists():
        print(f"Directory not found: {root}")
        return 1

    total_before = 0
    total_after = 0
    total_files_removed = 0
    total_dirs_removed = 0

    for repo_dir in sorted(root.iterdir()):
        if not repo_dir.is_dir():
            continue
        before = get_dir_size(repo_dir)
        stats = cleanup_repo(repo_dir)
        after = get_dir_size(repo_dir)

        total_before += before
        total_after += after
        total_files_removed += stats["removed_files"]
        total_dirs_removed += stats["removed_dirs"]

        saved_mb = (before - after) / (1024 * 1024)
        print(f"  {repo_dir.name}: {before / (1024*1024):.1f} MB -> {after / (1024*1024):.1f} MB (saved {saved_mb:.1f} MB, {stats['removed_files']} files, {stats['removed_dirs']} dirs)")

    print(f"\nTotal: {total_before / (1024*1024):.1f} MB -> {total_after / (1024*1024):.1f} MB")
    print(f"Saved: {(total_before - total_after) / (1024*1024):.1f} MB ({(1 - total_after/total_before)*100:.1f}% reduction)")
    print(f"Removed: {total_files_removed} files, {total_dirs_removed} directories")
    return 0


if __name__ == "__main__":
    sys.exit(main())
