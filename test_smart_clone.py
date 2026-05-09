"""Tests for Phase 18 smart clone filtering in rosclaw_fetch.py."""

from __future__ import annotations

import tempfile
from pathlib import Path

import pytest

from rosclaw_fetch import (
    ALLOWED_FILE_EXTENSIONS,
    SKIP_PATTERNS,
    _cleanup_skipped_files,
    _count_source_files,
    _get_dir_size,
)


class TestCleanupSkippedFiles:
    """Customer story: 'I cloned a repo but it has model weights and datasets I don't need.'"""

    def test_removes_binary_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp) / "test_repo"
            repo.mkdir()
            (repo / "model.pth").write_text("fake weights")
            (repo / "checkpoint.ckpt").write_text("fake ckpt")
            (repo / "config.yaml").write_text("robot: true")

            _cleanup_skipped_files(repo)

            assert not (repo / "model.pth").exists()
            assert not (repo / "checkpoint.ckpt").exists()
            assert (repo / "config.yaml").exists()

    def test_removes_skipped_directories(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp) / "test_repo"
            repo.mkdir()
            datasets = repo / "datasets"
            datasets.mkdir()
            (datasets / "imagenet.zip").write_text("fake")
            (repo / "src" / "main.py").parent.mkdir(parents=True)
            (repo / "src" / "main.py").write_text("print('hello')")

            _cleanup_skipped_files(repo)

            assert not datasets.exists()
            assert (repo / "src" / "main.py").exists()

    def test_keeps_allowed_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp) / "test_repo"
            repo.mkdir()
            (repo / "README.md").write_text("# Robot")
            (repo / "setup.py").write_text("setup()")
            (repo / "CMakeLists.txt").write_text("cmake")
            (repo / "config.urdf").write_text("<robot/>")
            (repo / "package.xml").write_text("<package/>")

            _cleanup_skipped_files(repo)

            assert (repo / "README.md").exists()
            assert (repo / "setup.py").exists()
            assert (repo / "CMakeLists.txt").exists()
            assert (repo / "config.urdf").exists()
            assert (repo / "package.xml").exists()


class TestDirSizeAndCount:
    def test_get_dir_size(self):
        with tempfile.TemporaryDirectory() as tmp:
            d = Path(tmp)
            (d / "a.txt").write_text("hello")
            (d / "b.txt").write_text("world")
            (d / "sub").mkdir()
            (d / "sub" / "c.txt").write_text("!")
            assert _get_dir_size(d) == 11  # hello + world + !

    def test_count_source_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            d = Path(tmp)
            (d / "a.py").write_text("x")
            (d / "b.cpp").write_text("x")
            (d / "c.bin").write_text("x")
            (d / "README.md").write_text("x")
            count = _count_source_files(d)
            assert count >= 3  # py, cpp, README.md


class TestFilteringConstants:
    def test_allowed_extensions_not_empty(self):
        assert len(ALLOWED_FILE_EXTENSIONS) > 0
        assert ".py" in ALLOWED_FILE_EXTENSIONS
        assert ".urdf" in ALLOWED_FILE_EXTENSIONS
        assert "README.md" in ALLOWED_FILE_EXTENSIONS

    def test_skip_patterns_cover_binaries(self):
        patterns = SKIP_PATTERNS
        assert any("*.pth" in p for p in patterns)
        assert any("datasets/" in p for p in patterns)
        assert any("__pycache__/" in p for p in patterns)
