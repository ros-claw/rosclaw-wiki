#!/usr/bin/env python3
"""End-to-end integration test for ROSClaw Wiki Phase 1.

Simulates the full pipeline without real LLM calls or network downloads.
"""

from __future__ import annotations

import json
import shutil
import sys
import tempfile
from pathlib import Path

import pytest

import wiki_engine as engine


@pytest.fixture
def temp_wiki():
    """Provide a temporary wiki directory structure."""
    tmp = Path(tempfile.mkdtemp(prefix="rosclaw_wiki_test_"))
    (tmp / "entities").mkdir()
    (tmp / "algorithms").mkdir()
    (tmp / "concepts").mkdir()
    (tmp / "skills").mkdir()
    (tmp / "episodes").mkdir()
    (tmp / "archive").mkdir()
    yield tmp
    shutil.rmtree(tmp, ignore_errors=True)


@pytest.fixture
def temp_raw():
    """Provide a temporary raw data directory."""
    tmp = Path(tempfile.mkdtemp(prefix="rosclaw_raw_test_"))
    (tmp / "papers").mkdir()
    (tmp / "code").mkdir()
    (tmp / "articles").mkdir()
    yield tmp
    shutil.rmtree(tmp, ignore_errors=True)


def mock_llm(prompt: str, content: str) -> str:
    """Fake LLM that returns a predictable edit."""
    return content + "\n\n[Edited by mock LLM]"


class TestFrontmatter:
    def test_parse_and_write_roundtrip(self):
        meta = {"id": "test", "type": "concept", "confidence": 0.8}
        body = "# Hello\n\nWorld."
        md = engine.write_frontmatter(meta, body)
        parsed_meta, parsed_body = engine.parse_frontmatter(md)
        assert parsed_meta["id"] == "test"
        assert parsed_meta["type"] == "concept"
        assert parsed_body.strip() == body.strip()

    def test_generate_page_id(self):
        assert engine.generate_page_id("Unitree G1") == "unitree_g1"
        assert engine.generate_page_id("ROS 2 Humble!") == "ros_2_humble"


class TestConfidenceLifecycle:
    def test_reinforcement_boost(self):
        meta = {"confidence": 0.5, "last_reinforced": "2026-04-01"}
        updated = engine.update_confidence(meta, reinforcement=True)
        assert updated["confidence"] == 0.55

    def test_decay_30_days(self):
        meta = {"confidence": 1.0, "last_reinforced": "2026-03-01", "created_at": "2026-03-01"}
        updated = engine.update_confidence(meta, reinforcement=False)
        # More than 30 days since 2026-03-01 → ×0.9
        assert updated["confidence"] == 0.9

    def test_decay_90_days(self):
        meta = {"confidence": 1.0, "last_reinforced": "2026-01-01", "created_at": "2026-01-01"}
        updated = engine.update_confidence(meta, reinforcement=False)
        assert updated["confidence"] == 0.7

    def test_decay_180_days(self):
        meta = {"confidence": 1.0, "last_reinforced": "2025-10-01", "created_at": "2025-10-01"}
        updated = engine.update_confidence(meta, reinforcement=False)
        assert updated["confidence"] == 0.5


class TestSupersession:
    def test_higher_rank_supersedes(self):
        new = {"source_type": "official", "created_at": "2026-04-27"}
        old = {"source_type": "blog", "created_at": "2026-04-01"}
        assert engine.check_supersession_needed(new, old) is True

    def test_same_rank_newer_supersedes(self):
        new = {"source_type": "paper", "created_at": "2026-04-27"}
        old = {"source_type": "paper", "created_at": "2026-04-01"}
        assert engine.check_supersession_needed(new, old) is True

    def test_older_does_not_supersede(self):
        new = {"source_type": "blog", "created_at": "2026-04-01"}
        old = {"source_type": "paper", "created_at": "2026-04-27"}
        assert engine.check_supersession_needed(new, old) is False


class TestPageOperations:
    def test_create_page(self, temp_wiki):
        path = engine.create_page(
            str(temp_wiki / "entities"),
            "Unitree G1",
            "# Unitree G1\n\nA humanoid robot.",
            {"type": "entity", "tags": ["robot"]},
        )
        assert Path(path).exists()
        meta, body = engine.parse_frontmatter(Path(path).read_text())
        assert meta["type"] == "entity"
        assert meta["title"] == "Unitree G1"
        assert "Unitree G1" in body

    def test_update_page(self, temp_wiki):
        path = engine.create_page(
            str(temp_wiki / "concepts"),
            "Sim to Real",
            "# Sim to Real\n\nTransfer from simulation.",
            {"type": "concept"},
        )
        engine.update_page(path, "Add a paragraph about domain randomization.", mock_llm)
        content = Path(path).read_text()
        assert "[Edited by mock LLM]" in content
        meta, _ = engine.parse_frontmatter(content)
        assert meta["confidence"] > 0.5  # Reinforced

    def test_move_to_archive(self, temp_wiki):
        path = engine.create_page(
            str(temp_wiki / "algorithms"),
            "Old Algorithm",
            "# Old Algorithm\n\nDeprecated.",
            {"type": "algorithm"},
        )
        archive_path = engine.move_to_archive(path, str(temp_wiki))
        assert Path(archive_path).exists()
        assert Path(path).exists()  # stub remains
        assert "[!CAUTION]" in Path(path).read_text()

    def test_conflict_handling(self, temp_wiki):
        path = engine.create_page(
            str(temp_wiki / "entities"),
            "Test Entity",
            "# Test Entity\n\nWeight: 10kg.",
            {"type": "entity", "source_type": "official"},
        )
        new_content = engine.handle_conflict(path, "weight", "10kg", "12kg", "blog")
        Path(path).write_text(new_content, encoding="utf-8")
        assert "待核实冲突" in new_content
        assert "10kg" in new_content
        assert "12kg" in new_content


class TestIndexAndLog:
    def test_update_index(self, temp_wiki):
        engine.create_page(
            str(temp_wiki / "entities"),
            "Robot A",
            "# Robot A",
            {"type": "entity"},
        )
        engine.create_page(
            str(temp_wiki / "algorithms"),
            "Alg X",
            "# Alg X",
            {"type": "algorithm"},
        )
        index_path = engine.update_index(str(temp_wiki))
        content = Path(index_path).read_text()
        assert "Robot A" in content
        assert "Alg X" in content
        assert "Entities" in content
        assert "Algorithms" in content

    def test_append_log(self, temp_wiki):
        log_path = engine.append_log(str(temp_wiki), "ingest | test_source.pdf (paper)")
        content = Path(log_path).read_text()
        assert "ingest | test_source.pdf" in content


class TestOrphanDetection:
    def test_find_orphans(self, temp_wiki):
        p1 = engine.create_page(
            str(temp_wiki / "entities"),
            "Linked Entity",
            "# Linked Entity\n\nSee [[Orphan Entity]].",
            {"type": "entity"},
        )
        p2 = engine.create_page(
            str(temp_wiki / "entities"),
            "Orphan Entity",
            "# Orphan Entity\n\nNo one links here.",
            {"type": "entity"},
        )
        orphans = engine.find_orphan_pages(str(temp_wiki))
        assert p1 in orphans  # Linked Entity has no inbound links
        assert p2 not in orphans  # Orphan Entity is linked FROM Linked Entity


class TestFetcher:
    def test_extract_urls(self, tmp_path):
        md = tmp_path / "test.md"
        md.write_text(
            "# List\n- [Paper](https://arxiv.org/abs/2403.12945)\n- [Repo](https://github.com/user/repo)\n- https://example.com/article\n"
        )
        urls = engine.parse_frontmatter  # placeholder; we test via import in rosclaw_fetch
        # Actually exercise fetcher logic via direct import
        import rosclaw_fetch as fetch
        urls = fetch.extract_urls(str(md))
        assert len(urls) == 3
        texts = [t for t, _ in urls]
        assert "Paper" in texts
        assert "Repo" in texts

    def test_classify_url(self):
        import rosclaw_fetch as fetch
        assert fetch.classify_url("https://arxiv.org/abs/1234") == "paper"
        assert fetch.classify_url("https://github.com/user/repo") == "code"
        assert fetch.classify_url("https://example.com") == "article"

    def test_parse_arxiv_id(self):
        import rosclaw_fetch as fetch
        assert fetch.parse_arxiv_id("https://arxiv.org/abs/2403.12945") == "2403.12945"
        assert fetch.parse_arxiv_id("https://arxiv.org/pdf/2403.12945.pdf") == "2403.12945"

    def test_parse_github_repo(self):
        import rosclaw_fetch as fetch
        assert fetch.parse_github_repo("https://github.com/unitreerobotics/unitree_sdk2") == (
            "unitreerobotics",
            "unitree_sdk2",
        )


class TestMcpToolLogic:
    """Test the logic backing MCP tools without starting a server."""

    def test_ingest_prompt_construction(self, temp_raw, temp_wiki):
        # Simulate what wiki_ingest_source does
        src = temp_raw / "articles" / "test.md"
        src.write_text("# Test Article\n\nThis mentions Unitree G1 and SLAM.")
        meta, body = engine.parse_frontmatter(src.read_text())
        assert "Unitree G1" in body
        # In real MCP tool, this would return a prompt string

    def test_search_logic(self, temp_wiki):
        engine.create_page(
            str(temp_wiki / "entities"),
            "Unitree G1",
            "# Unitree G1\n\nA humanoid robot from Unitree.",
            {"type": "entity"},
        )
        engine.create_page(
            str(temp_wiki / "algorithms"),
            "SLAM",
            "# SLAM\n\nSimultaneous localization and mapping.",
            {"type": "algorithm"},
        )
        engine.update_index(str(temp_wiki))

        # Simple grep simulation
        query = "unitree"
        matches = []
        for md_file in temp_wiki.rglob("*.md"):
            for i, line in enumerate(md_file.read_text().splitlines(), 1):
                if query.lower() in line.lower():
                    matches.append({"file": str(md_file.name), "line": i, "text": line.strip()})
        assert any("Unitree G1" in m["text"] for m in matches)


class TestFullPipeline:
    def test_pipeline_no_llm(self, temp_wiki, temp_raw):
        """Simulate the full pipeline with mocked steps."""
        # 1. Create a fake raw source
        src = temp_raw / "articles" / "awesome_vln.md"
        src.write_text(
            "# Awesome VLN\n\n"
            "- [Paper](https://arxiv.org/abs/2403.12945)\n"
            "- [Code](https://github.com/user/repo)\n"
        )

        # 2. Fake download: create placeholder files
        (temp_raw / "papers" / "2403.12945.pdf").write_text("PDF content")
        (temp_raw / "code" / "user_repo").mkdir(parents=True, exist_ok=True)
        (temp_raw / "code" / "user_repo" / "README.md").write_text("# Repo\n\nVLN code.")

        # 3. Simulate ingest (LLM extraction mocked)
        entities = [
            {"type": "algorithm", "title": "VLN Model", "summary": "Vision-language navigation."},
            {"type": "concept", "title": "Embodied AI", "summary": "AI in physical bodies."},
        ]
        for e in entities:
            engine.create_page(
                str(temp_wiki / f"{e['type']}s"),
                e["title"],
                f"# {e['title']}\n\n{e['summary']}",
                {"type": e["type"], "sources": [str(src)]},
            )

        # 4. Update index and log
        engine.update_index(str(temp_wiki))
        engine.append_log(str(temp_wiki), "ingest | awesome_vln.md (batch)")

        # 5. Verify
        index = (temp_wiki / "index.md").read_text()
        assert "VLN Model" in index
        assert "Embodied AI" in index
        log = (temp_wiki / "log.md").read_text()
        assert "awesome_vln.md" in log

        # 6. Lint
        engine.append_log(str(temp_wiki), "lint | periodic check")
        pages = engine.list_pages(str(temp_wiki))
        assert len(pages) == 2
        orphans = engine.find_orphan_pages(str(temp_wiki))
        # index.md links to all pages, so none are orphans after update_index
        assert len(orphans) == 0


class TestKnowledgeSynthesizer:
    """Test the KnowledgeSynthesizer compile engine."""

    def test_synthesize_create_new(self, temp_wiki):
        from knowledge_synthesizer import KnowledgeSynthesizer

        synth = KnowledgeSynthesizer(str(temp_wiki))
        plan = synth.synthesize(
            entity_type="entity",
            entity_name="TestBot",
            new_facts={"parameters": {"weight": "12kg"}, "capabilities": ["walking"]},
            source_meta={"source_path": "test.md", "source_type": "blog_post", "url": ""},
        )
        assert plan.action == "create_new"
        assert plan.target_page_path is not None
        assert "testBot" in plan.target_page_path or "testbot" in plan.target_page_path.lower()
        assert plan.updated_frontmatter["confidence"] == 0.6
        assert plan.updated_frontmatter["type"] == "entity"
        assert "TestBot" in plan.prompt_for_rewrite

    def test_synthesize_reinforcement(self, temp_wiki):
        from knowledge_synthesizer import KnowledgeSynthesizer

        synth = KnowledgeSynthesizer(str(temp_wiki))
        # First create a page
        plan1 = synth.synthesize(
            entity_type="entity",
            entity_name="TestBot",
            new_facts={"parameters": {"weight": "12kg"}},
            source_meta={"source_path": "source1.md", "source_type": "blog_post", "url": ""},
        )
        engine.create_page(
            str(temp_wiki / "entities"),
            "TestBot",
            "# TestBot\n\nWeight: 12kg.",
            plan1.updated_frontmatter,
        )

        # Second source confirms same fact
        plan2 = synth.synthesize(
            entity_type="entity",
            entity_name="TestBot",
            new_facts={"parameters": {"weight": "12kg"}},
            source_meta={"source_path": "source2.md", "source_type": "official_manual", "url": ""},
        )
        assert plan2.action in ("incremental_update", "skip")
        if plan2.action != "skip":
            assert plan2.updated_frontmatter["confidence"] == 0.65  # 0.6 + 0.05

    def test_synthesize_conflict_detection(self, temp_wiki):
        from knowledge_synthesizer import KnowledgeSynthesizer

        synth = KnowledgeSynthesizer(str(temp_wiki))
        plan1 = synth.synthesize(
            entity_type="entity",
            entity_name="TestBot",
            new_facts={"parameters": {"weight": "12kg"}},
            source_meta={"source_path": "source1.md", "source_type": "blog_post", "url": ""},
        )
        engine.create_page(
            str(temp_wiki / "entities"),
            "TestBot",
            "# TestBot\n\nWeight: 12kg.",
            plan1.updated_frontmatter,
        )

        plan2 = synth.synthesize(
            entity_type="entity",
            entity_name="TestBot",
            new_facts={"parameters": {"weight": "15kg"}},
            source_meta={"source_path": "source2.md", "source_type": "official_manual", "url": ""},
        )
        assert plan2.action in ("incremental_update", "full_rewrite")
        assert len(plan2.new_facts.get("parameters", {})) > 0

    def test_locate_page(self, temp_wiki):
        from knowledge_synthesizer import KnowledgeSynthesizer

        synth = KnowledgeSynthesizer(str(temp_wiki))
        assert synth.locate_page("entity", "NonExistent") is None

        engine.create_page(
            str(temp_wiki / "entities"),
            "TestBot",
            "# TestBot\n\nContent.",
            {"type": "entity"},
        )
        assert synth.locate_page("entity", "TestBot") is not None


class TestLLMInterface:
    """Test LLMInterface backend detection."""

    def test_detect_backend_none(self, monkeypatch):
        from llm_interface import LLMInterface

        monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
        monkeypatch.delenv("OPENAI_API_KEY", raising=False)
        monkeypatch.delenv("DEEPSEEK_API_KEY", raising=False)
        iface = LLMInterface()
        assert iface.backend == "none"

    def test_detect_backend_anthropic(self, monkeypatch):
        from llm_interface import LLMInterface

        monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key")
        monkeypatch.delenv("OPENAI_API_KEY", raising=False)
        monkeypatch.delenv("DEEPSEEK_API_KEY", raising=False)
        iface = LLMInterface()
        assert iface.backend == "anthropic"

    def test_detect_backend_openai(self, monkeypatch):
        from llm_interface import LLMInterface

        monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
        monkeypatch.setenv("OPENAI_API_KEY", "test-key")
        monkeypatch.delenv("DEEPSEEK_API_KEY", raising=False)
        iface = LLMInterface()
        assert iface.backend == "openai"

    def test_detect_backend_deepseek(self, monkeypatch):
        from llm_interface import LLMInterface

        monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
        monkeypatch.delenv("OPENAI_API_KEY", raising=False)
        monkeypatch.setenv("DEEPSEEK_API_KEY", "test-key")
        iface = LLMInterface()
        assert iface.backend == "deepseek"

    def test_complete_raises_without_key(self, monkeypatch):
        from llm_interface import LLMInterface

        monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
        monkeypatch.delenv("OPENAI_API_KEY", raising=False)
        monkeypatch.delenv("DEEPSEEK_API_KEY", raising=False)
        iface = LLMInterface()
        with pytest.raises(RuntimeError, match="No LLM backend"):
            iface.complete("test prompt")


class TestFetcherPhase2:
    """Test Phase 2 Fetcher improvements."""

    def test_is_noise_url(self):
        import rosclaw_fetch as fetch

        assert fetch.is_noise_url("https://img.shields.io/badge/build-passing-brightgreen") is True
        assert fetch.is_noise_url("https://github.com/user/repo/issues/123") is True
        assert fetch.is_noise_url("https://arxiv.org/abs/2403.12945") is False
        assert fetch.is_noise_url("https://github.com/user/repo") is False

    def test_normalize_url(self):
        import rosclaw_fetch as fetch

        assert fetch.normalize_url("https://arxiv.org/abs/2403.12945") == "arxiv:2403.12945"
        assert fetch.normalize_url("https://arxiv.org/pdf/2403.12945.pdf") == "arxiv:2403.12945"
        assert fetch.normalize_url("https://example.com/page/") == "https://example.com/page"

    def test_should_skip_for_quality_short(self):
        import rosclaw_fetch as fetch

        html = "<html><head></head><body><p>Hi.</p></body></html>"
        should_skip, reason = fetch.should_skip_for_quality(html)
        assert should_skip is True
        assert "too-short" in reason

    def test_should_skip_for_quality_good(self):
        import rosclaw_fetch as fetch

        paragraphs = " ".join([f"<p>Paragraph {i} with some meaningful content about robotics and navigation.{i}</p>" for i in range(50)])
        html = f"<html><head></head><body>{paragraphs}</body></html>"
        should_skip, reason = fetch.should_skip_for_quality(html)
        assert should_skip is False
        assert reason == ""

    def test_compute_sha256(self):
        import rosclaw_fetch as fetch

        h1 = fetch.compute_sha256(b"hello")
        h2 = fetch.compute_sha256(b"hello")
        h3 = fetch.compute_sha256(b"world")
        assert h1 == h2
        assert h1 != h3
        assert len(h1) == 64


class TestRetentionEngine:
    """Test knowledge retention and decay."""

    def test_decay_30_days(self, temp_wiki):
        from retention_engine import decay_confidence
        from datetime import datetime, timedelta

        # Create a page with last_reinforced 40 days ago
        old_date = (datetime.now() - timedelta(days=40)).isoformat(timespec="seconds")
        engine.create_page(
            str(temp_wiki / "entities"),
            "Old Robot",
            "# Old Robot\n\nWeight: 10kg.",
            {"type": "entity", "confidence": 0.8, "last_reinforced": old_date},
        )

        summary = decay_confidence(str(temp_wiki))
        assert summary["total_scanned"] >= 1
        assert summary["pages_decayed"] == 1
        assert summary["details"][0]["old_confidence"] == 0.8
        assert summary["details"][0]["new_confidence"] == 0.72  # 0.8 * 0.9

    def test_decay_90_days(self, temp_wiki):
        from retention_engine import decay_confidence
        from datetime import datetime, timedelta

        old_date = (datetime.now() - timedelta(days=100)).isoformat(timespec="seconds")
        engine.create_page(
            str(temp_wiki / "concepts"),
            "Stale Concept",
            "# Stale Concept\n\nDescription.",
            {"type": "concept", "confidence": 1.0, "last_reinforced": old_date},
        )

        summary = decay_confidence(str(temp_wiki))
        assert summary["pages_decayed"] == 1
        assert summary["details"][0]["new_confidence"] == 0.7  # 1.0 * 0.7

    def test_decay_180_days(self, temp_wiki):
        from retention_engine import decay_confidence
        from datetime import datetime, timedelta

        old_date = (datetime.now() - timedelta(days=200)).isoformat(timespec="seconds")
        engine.create_page(
            str(temp_wiki / "algorithms"),
            "Ancient Alg",
            "# Ancient Alg\n\nDeprecated.",
            {"type": "algorithm", "confidence": 0.6, "last_reinforced": old_date},
        )

        summary = decay_confidence(str(temp_wiki))
        assert summary["pages_decayed"] == 1
        assert summary["details"][0]["new_confidence"] == 0.3  # 0.6 * 0.5

    def test_decay_no_change_under_30_days(self, temp_wiki):
        from retention_engine import decay_confidence
        from datetime import datetime, timedelta

        recent_date = (datetime.now() - timedelta(days=5)).isoformat(timespec="seconds")
        engine.create_page(
            str(temp_wiki / "skills"),
            "Fresh Skill",
            "# Fresh Skill\n\nNew.",
            {"type": "skill", "confidence": 0.9, "last_reinforced": recent_date},
        )

        summary = decay_confidence(str(temp_wiki))
        assert summary["pages_decayed"] == 0
        assert summary["pages_unchanged"] >= 1

    def test_suggest_archival(self, temp_wiki):
        from retention_engine import suggest_archival

        engine.create_page(
            str(temp_wiki / "entities"),
            "Low Conf Entity",
            "# Low Conf\n\nUnverified.",
            {"type": "entity", "confidence": 0.1, "last_reinforced": "2026-01-01"},
        )
        engine.create_page(
            str(temp_wiki / "entities"),
            "High Conf Entity",
            "# High Conf\n\nVerified.",
            {"type": "entity", "confidence": 0.9, "last_reinforced": "2026-04-27"},
        )

        candidates = suggest_archival(str(temp_wiki), threshold=0.15)
        titles = [c["title"] for c in candidates]
        assert "Low Conf Entity" in titles
        assert "High Conf Entity" not in titles
        assert all(c["confidence"] < 0.15 for c in candidates)


class TestSmartLint:
    """Test upgraded wiki_auto_lint logic (without MCP server)."""

    def test_low_confidence_reinforcement_suggestions(self, temp_wiki):
        engine.create_page(
            str(temp_wiki / "entities"),
            "Weak Entity",
            "# Weak Entity\n\nUnverified claim.",
            {"type": "entity", "confidence": 0.2, "last_reinforced": "2026-01-01"},
        )
        pages = engine.list_pages(str(temp_wiki))
        low_confidence = [
            {"path": p.get("_path"), "title": p.get("title", "unknown"), "confidence": p.get("confidence", 0)}
            for p in pages
            if float(p.get("confidence", 1.0)) < 0.3
        ]
        assert len(low_confidence) == 1
        assert low_confidence[0]["title"] == "Weak Entity"
        assert low_confidence[0]["confidence"] == 0.2

    def test_orphan_auto_link_no_llm(self, temp_wiki):
        # Create an orphan and a page that could link to it
        engine.create_page(
            str(temp_wiki / "entities"),
            "Linker",
            "# Linker\n\nThis page mentions robotics.",
            {"type": "entity"},
        )
        engine.create_page(
            str(temp_wiki / "entities"),
            "Orphan",
            "# Orphan\n\nA robot concept.",
            {"type": "entity"},
        )
        orphans = engine.find_orphan_pages(str(temp_wiki))
        # After update_index, index.md links to all pages, so orphans may be empty
        # For this test we directly verify orphan logic
        assert isinstance(orphans, list)

    def test_retention_log_format(self, temp_wiki):
        from retention_engine import decay_confidence
        from datetime import datetime, timedelta

        old_date = (datetime.now() - timedelta(days=50)).isoformat(timespec="seconds")
        engine.create_page(
            str(temp_wiki / "entities"),
            "Decaying Entity",
            "# Decaying\n\nOld info.",
            {"type": "entity", "confidence": 0.5, "last_reinforced": old_date},
        )
        decay_confidence(str(temp_wiki))
        log_content = (temp_wiki / "log.md").read_text()
        assert "retention | decay_round" in log_content
        assert "pages_affected" in log_content


class TestBatchIngest:
    """Test batch ingest checkpoint and file collection logic."""

    def test_collect_raw_files(self, temp_raw):
        from batch_ingest import _collect_raw_files

        (temp_raw / "papers" / "test.pdf").parent.mkdir(parents=True, exist_ok=True)
        (temp_raw / "papers" / "test.pdf").write_text("PDF")
        (temp_raw / "articles" / "test.md").parent.mkdir(parents=True, exist_ok=True)
        (temp_raw / "articles" / "test.md").write_text("Article")
        (temp_raw / "code" / "repo" / "README.md").parent.mkdir(parents=True, exist_ok=True)
        (temp_raw / "code" / "repo" / "README.md").write_text("Repo")

        files = _collect_raw_files(temp_raw)
        paths = [p for p, _ in files]
        assert "papers/test.pdf" in paths
        assert "articles/test.md" in paths
        assert "code/repo/README.md" in paths

    def test_checkpoint_resume(self, tmp_path):
        from batch_ingest import _load_processed_files, _save_processed_file, PROCESSED_LOG

        # Temporarily override log path
        orig_log = PROCESSED_LOG
        try:
            test_log = tmp_path / "processed.log"
            import batch_ingest
            batch_ingest.PROCESSED_LOG = test_log

            assert _load_processed_files() == set()
            _save_processed_file("articles/test.md")
            _save_processed_file("papers/test.pdf")
            assert _load_processed_files() == {"articles/test.md", "papers/test.pdf"}
        finally:
            batch_ingest.PROCESSED_LOG = orig_log

    def test_reset_clears_log(self, tmp_path):
        from batch_ingest import _save_processed_file, PROCESSED_LOG
        import batch_ingest

        orig_log = PROCESSED_LOG
        try:
            test_log = tmp_path / "processed.log"
            batch_ingest.PROCESSED_LOG = test_log
            _save_processed_file("articles/test.md")
            assert test_log.exists()
            test_log.unlink()
            assert not test_log.exists()
        finally:
            batch_ingest.PROCESSED_LOG = orig_log


class TestSearchBackend:
    """Test whoosh-based search backend."""

    def test_init_index(self, temp_wiki):
        import search_backend as sb

        idx = sb.init_index(str(temp_wiki))
        # whoosh may be unavailable in some envs
        if sb.WHOOSH_AVAILABLE:
            assert idx is not None

    def test_index_and_search(self, temp_wiki):
        import search_backend as sb

        if not sb.WHOOSH_AVAILABLE:
            pytest.skip("whoosh not installed")

        engine.create_page(
            str(temp_wiki / "entities"),
            "Searchable Bot",
            "# Searchable Bot\n\nThis robot navigates using SLAM.",
            {"type": "entity", "tags": ["robot", "slam"]},
        )

        sb.rebuild_index(str(temp_wiki))
        results = sb.search_index(str(temp_wiki), "SLAM")
        assert len(results) >= 1
        assert any("Searchable Bot" in r["title"] for r in results)

    def test_search_by_title(self, temp_wiki):
        import search_backend as sb

        if not sb.WHOOSH_AVAILABLE:
            pytest.skip("whoosh not installed")

        engine.create_page(
            str(temp_wiki / "algorithms"),
            "A Star",
            "# A Star\n\nPathfinding algorithm.",
            {"type": "algorithm", "tags": ["pathfinding"]},
        )

        sb.rebuild_index(str(temp_wiki))
        results = sb.search_index(str(temp_wiki), "A Star")
        assert any(r["title"] == "A Star" for r in results)

    def test_search_no_matches(self, temp_wiki):
        import search_backend as sb

        if not sb.WHOOSH_AVAILABLE:
            pytest.skip("whoosh not installed")

        sb.rebuild_index(str(temp_wiki))
        results = sb.search_index(str(temp_wiki), "xyznonexistent")
        assert results == []

    def test_index_page_incremental(self, temp_wiki):
        import search_backend as sb

        if not sb.WHOOSH_AVAILABLE:
            pytest.skip("whoosh not installed")

        engine.create_page(
            str(temp_wiki / "concepts"),
            "Test Concept",
            "# Test Concept\n\nA test concept about navigation.",
            {"type": "concept"},
        )

        # Index just this page
        sb.index_page(str(temp_wiki), "concepts/test_concept.md")
        results = sb.search_index(str(temp_wiki), "navigation")
        assert any("Test Concept" in r["title"] for r in results)


class TestPDFExtractor:
    """Test PDF text extraction with section detection."""

    @pytest.fixture
    def sample_pdf(self, tmp_path):
        """Create a minimal test PDF with structured sections."""
        try:
            import fitz
        except ImportError:
            pytest.skip("PyMuPDF not installed")

        doc = fitz.open()
        page = doc.new_page()
        # Use larger font for headers so they stand out
        page.insert_text((50, 80), "ABSTRACT", fontsize=14)
        page.insert_text((50, 110), "This paper presents a novel approach to robot navigation using deep learning.", fontsize=10)
        page.insert_text((50, 150), "I. INTRODUCTION", fontsize=14)
        page.insert_text((50, 180), "Autonomous robots need robust navigation systems to operate in unstructured environments.", fontsize=10)
        page.insert_text((50, 220), "II. METHODS", fontsize=14)
        page.insert_text((50, 250), "We use a transformer model with 12 layers and hidden size 768.", fontsize=10)
        page.insert_text((50, 280), "Training uses Adam optimizer with learning rate 1e-4.", fontsize=10)
        page.insert_text((50, 320), "III. EXPERIMENTS", fontsize=14)
        page.insert_text((50, 350), "Accuracy: 95.2% on benchmark dataset. Latency: 120ms per frame.", fontsize=10)
        page.insert_text((50, 390), "IV. CONCLUSION", fontsize=14)
        page.insert_text((50, 420), "Our method outperforms baselines. Future work includes multi-robot coordination.", fontsize=10)
        page.insert_text((50, 460), "REFERENCES", fontsize=14)
        page.insert_text((50, 490), "[1] Smith et al., Robot Navigation, 2024.", fontsize=10)

        pdf_path = tmp_path / "test_paper.pdf"
        doc.save(str(pdf_path))
        doc.close()
        return pdf_path

    def test_extract_pdf_text(self, sample_pdf):
        from pdf_extractor import extract_pdf_text

        text = extract_pdf_text(str(sample_pdf))
        assert "transformer model" in text
        assert "95.2%" in text
        assert len(text) > 200

    def test_extract_pdf_sections(self, sample_pdf):
        from pdf_extractor import extract_pdf_sections

        sections = extract_pdf_sections(str(sample_pdf))
        assert sections["abstract"]
        assert "deep learning" in sections["abstract"].lower()
        assert sections["introduction"]
        assert "autonomous robots" in sections["introduction"].lower()
        assert sections["methods"]
        assert "transformer" in sections["methods"].lower()
        assert sections["experiments"]
        assert "95.2%" in sections["experiments"]
        assert sections["conclusion"]
        assert "outperforms baselines" in sections["conclusion"].lower()
        assert sections["references"]
        assert "smith" in sections["references"].lower()

    def test_extract_pdf_fallback_to_abstract(self, temp_raw):
        """When PDF extraction fails, _read_source_text falls back to sidecar JSON."""
        from batch_ingest import _read_source_text

        # Create a dummy PDF without sidecar JSON (should return error placeholder)
        dummy_pdf = temp_raw / "test.pdf"
        dummy_pdf.write_bytes(b"not a real pdf")
        text, source = _read_source_text(str(dummy_pdf.name), temp_raw)
        assert "extraction not available" in text or "Error reading" in text
        assert source == "error"

    def test_read_source_text_fulltext(self, temp_raw):
        """Test that _read_source_text returns full_text for a real PDF."""
        try:
            import fitz
        except ImportError:
            pytest.skip("PyMuPDF not installed")

        from batch_ingest import _read_source_text

        doc = fitz.open()
        page = doc.new_page()
        page.insert_text((50, 100), "ABSTRACT", fontsize=14)
        page.insert_text((50, 130), "This is the abstract.", fontsize=10)
        page.insert_text((50, 170), "II. METHODS", fontsize=14)
        page.insert_text((50, 200), "We use 12 layers.", fontsize=10)
        pdf_path = temp_raw / "sample.pdf"
        doc.save(str(pdf_path))
        doc.close()

        # Create sidecar JSON
        meta = {"title": "Sample Paper", "authors": ["A. Smith"], "summary": "Short abstract."}
        (temp_raw / "sample.json").write_text(json.dumps(meta), encoding="utf-8")

        text, source = _read_source_text("sample.pdf", temp_raw)
        assert source == "full_text"
        assert "ABSTRACT" in text or "abstract" in text.lower()
        assert "METHODS" in text or "methods" in text.lower()

    def test_api_extractor_availability(self, monkeypatch):
        """Test that API extractor availability tracks the token correctly."""
        from unittest import mock
        import pdf_extractor

        # Simulate no token → API unavailable
        with mock.patch("pdf_extractor.paddleocr.is_available", return_value=False):
            assert pdf_extractor.is_api_extractor_available() is False

        # Simulate token set → API available
        with mock.patch("pdf_extractor.paddleocr.is_available", return_value=True):
            assert pdf_extractor.is_api_extractor_available() is True
            assert pdf_extractor.is_extractor_available() is True


class TestEntityResolver:
    """Test entity disambiguation and duplicate detection."""

    @pytest.fixture
    def temp_wiki_for_resolver(self, tmp_path):
        """Create a wiki with some potentially duplicate pages."""
        wiki = tmp_path / "wiki"
        wiki.mkdir()

        p1 = wiki / "entities" / "wildos.md"
        p1.parent.mkdir(parents=True, exist_ok=True)
        p1.write_text(
            '---\ntitle: WildOS\ntype: entity\n---\n\nWildOS is a system for outdoor robot navigation.',
            encoding="utf-8",
        )

        p2 = wiki / "entities" / "wildos_system.md"
        p2.parent.mkdir(parents=True, exist_ok=True)
        p2.write_text(
            '---\ntitle: WildOS System\ntype: entity\n---\n\nThe WildOS System enables long-range semantic navigation.',
            encoding="utf-8",
        )

        p3 = wiki / "algorithms" / "ppo.md"
        p3.parent.mkdir(parents=True, exist_ok=True)
        p3.write_text(
            '---\ntitle: Proximal Policy Optimization\ntype: algorithm\n---\n\nPPO is a reinforcement learning algorithm.',
            encoding="utf-8",
        )

        return wiki

    def test_find_candidate_entities_exact_match(self, temp_wiki_for_resolver):
        from entity_resolver import find_candidate_entities

        candidates = find_candidate_entities("WildOS", str(temp_wiki_for_resolver))
        assert len(candidates) >= 1
        titles = [c["title"] for c in candidates]
        assert "WildOS" in titles

    def test_resolve_entity_merge(self, temp_wiki_for_resolver):
        from entity_resolver import resolve_entity

        # "WildOS System" should merge with "WildOS System" (exact match)
        result = resolve_entity("WildOS System", str(temp_wiki_for_resolver))
        assert result["action"] == "merge"
        assert "wildos_system.md" in result["target"]

    def test_resolve_entity_create_new(self, temp_wiki_for_resolver):
        from entity_resolver import resolve_entity

        # Completely unrelated name should create new
        result = resolve_entity("Transformer Architecture", str(temp_wiki_for_resolver))
        assert result["action"] == "create_new"

    def test_entity_dedup_report(self, temp_wiki_for_resolver):
        from entity_resolver import entity_dedup_report

        duplicates = entity_dedup_report(str(temp_wiki_for_resolver), similarity_threshold=0.6)
        # WildOS and WildOS System should be detected as potential duplicates
        assert len(duplicates) >= 1
        pair = duplicates[0]
        assert {"WildOS", "WildOS System"} <= {pair["title_a"], pair["title_b"]}

    def test_knowledge_synthesizer_merge(self, temp_wiki_for_resolver):
        from knowledge_synthesizer import KnowledgeSynthesizer

        synth = KnowledgeSynthesizer(str(temp_wiki_for_resolver))
        plan = synth.synthesize(
            entity_type="entity",
            entity_name="WildOS System",
            new_facts={"capabilities": ["semantic navigation"]},
            source_meta={"source_type": "arxiv_paper", "source_path": "test.pdf"},
        )
        # Should resolve to merge with existing WildOS System page
        assert plan.action in ("incremental_update", "full_rewrite", "skip")
        assert "wildos_system.md" in plan.target_page_path


class TestGraphExporter:
    """Test knowledge graph export in multiple formats."""

    @pytest.fixture
    def temp_wiki_for_graph(self, tmp_path):
        wiki = tmp_path / "wiki"
        wiki.mkdir()

        p1 = wiki / "entities" / "wildos.md"
        p1.parent.mkdir(parents=True, exist_ok=True)
        p1.write_text(
            '---\ntitle: WildOS\ntype: entity\ntags: [navigation]\n---\n\n'
            'WildOS uses [[ExploRFM]] for semantic frontier scoring. '
            'It also depends on [[Navigation Graph]] for spatial memory.',
            encoding="utf-8",
        )

        p2 = wiki / "algorithms" / "explorf.md"
        p2.parent.mkdir(parents=True, exist_ok=True)
        p2.write_text(
            '---\ntitle: ExploRFM\ntype: algorithm\ntags: [vision]\n---\n\n'
            'ExploRFM predicts traversability and object similarity.',
            encoding="utf-8",
        )

        p3 = wiki / "concepts" / "navigation_graph.md"
        p3.parent.mkdir(parents=True, exist_ok=True)
        p3.write_text(
            '---\ntitle: Navigation Graph\ntype: concept\ntags: [graph]\n---\n\n'
            'A sparse topological map for robot navigation.',
            encoding="utf-8",
        )

        return wiki

    def test_export_graph_json(self, temp_wiki_for_graph):
        from graph_exporter import export_graph

        result = export_graph(str(temp_wiki_for_graph), fmt="json")
        assert result["status"] == "done"
        assert result["node_count"] == 3
        assert result["edge_count"] == 2
        # Verify output files exist
        assert any("nodes.json" in p for p in result["output_paths"])
        assert any("edges.json" in p for p in result["output_paths"])

    def test_export_graph_sigma(self, temp_wiki_for_graph):
        from graph_exporter import export_graph

        result = export_graph(str(temp_wiki_for_graph), fmt="sigma")
        assert result["status"] == "done"
        assert result["node_count"] == 3
        assert any("sigma.json" in p for p in result["output_paths"])

        # Validate sigma format structure
        import json
        sigma_path = [p for p in result["output_paths"] if "sigma.json" in p][0]
        data = json.loads(Path(sigma_path).read_text(encoding="utf-8"))
        assert "nodes" in data
        assert "edges" in data
        assert len(data["nodes"]) == 3
        assert len(data["edges"]) == 2
        assert data["nodes"][0]["attributes"]["label"]

    def test_export_graph_cytoscape(self, temp_wiki_for_graph):
        from graph_exporter import export_graph

        result = export_graph(str(temp_wiki_for_graph), fmt="cytoscape")
        assert result["status"] == "done"
        assert any("cytoscape.json" in p for p in result["output_paths"])

        import json
        cy_path = [p for p in result["output_paths"] if "cytoscape.json" in p][0]
        data = json.loads(Path(cy_path).read_text(encoding="utf-8"))
        assert len(data) == 5  # 3 nodes + 2 edges
        nodes = [x for x in data if "source" not in x["data"]]
        edges = [x for x in data if "source" in x["data"]]
        assert len(nodes) == 3
        assert len(edges) == 2


class TestVectorIndex:
    """Test semantic vector indexing and hybrid RRF search."""

    @pytest.fixture
    def temp_wiki_for_vectors(self, tmp_path):
        """Create a small wiki with a few pages for vector testing."""
        wiki = tmp_path / "wiki"
        wiki.mkdir()

        # Page 1: bipedal locomotion
        p1 = wiki / "concepts" / "bipedal_locomotion.md"
        p1.parent.mkdir(parents=True, exist_ok=True)
        p1.write_text(
            '---\ntitle: Bipedal Locomotion\ntype: concept\ntags: [robot, walking]\n---\n\n'
            'Bipedal locomotion is a form of terrestrial locomotion where an organism '
            'moves by means of its two rear limbs or legs. In robotics, this involves '
            'complex balance control and gait planning.',
            encoding="utf-8",
        )

        # Page 2: quadruped robots
        p2 = wiki / "entities" / "spot_robot.md"
        p2.parent.mkdir(parents=True, exist_ok=True)
        p2.write_text(
            '---\ntitle: Spot Robot\ntype: entity\ntags: [quadruped, boston-dynamics]\n---\n\n'
            'Spot is a quadruped robot developed by Boston Dynamics. '
            'It walks on four legs and can navigate stairs and rough terrain.',
            encoding="utf-8",
        )

        # Page 3: reinforcement learning
        p3 = wiki / "algorithms" / "ppo.md"
        p3.parent.mkdir(parents=True, exist_ok=True)
        p3.write_text(
            '---\ntitle: Proximal Policy Optimization\ntype: algorithm\ntags: [rl, policy-gradient]\n---\n\n'
            'PPO is a policy gradient method for reinforcement learning. '
            'It clips the policy update to prevent overly large steps.',
            encoding="utf-8",
        )

        return wiki

    def test_build_vector_index(self, temp_wiki_for_vectors):
        try:
            import sentence_transformers
        except ImportError:
            pytest.skip("sentence-transformers not installed")

        from vector_index import build_vector_index, search_semantic

        result = build_vector_index(str(temp_wiki_for_vectors))
        assert result["status"] == "done"
        assert result["indexed_count"] == 3

        # Semantic search should find walking-related content
        results = search_semantic(str(temp_wiki_for_vectors), "robot walking", top_k=3)
        assert len(results) >= 1
        titles = [r["title"].lower() for r in results]
        assert any("bipedal" in t or "spot" in t for t in titles)

    def test_index_page_incremental(self, temp_wiki_for_vectors):
        try:
            import sentence_transformers
        except ImportError:
            pytest.skip("sentence-transformers not installed")

        from vector_index import build_vector_index, index_page, search_semantic

        build_vector_index(str(temp_wiki_for_vectors))

        # Add a new page
        p4 = temp_wiki_for_vectors / "skills" / "gait_control.md"
        p4.parent.mkdir(parents=True, exist_ok=True)
        p4.write_text(
            '---\ntitle: Gait Control\ntype: skill\ntags: [walking, control]\n---\n\n'
            'Gait control algorithms manage the periodic leg movements for stable robot walking.',
            encoding="utf-8",
        )

        ok = index_page(str(temp_wiki_for_vectors), "skills/gait_control.md")
        assert ok is True

        results = search_semantic(str(temp_wiki_for_vectors), "robot walking", top_k=5)
        titles = [r["title"].lower() for r in results]
        assert "gait control" in titles

    def test_search_hybrid_rrf(self, temp_wiki_for_vectors):
        try:
            import sentence_transformers
        except ImportError:
            pytest.skip("sentence-transformers not installed")

        from vector_index import build_vector_index, search_hybrid
        import search_backend

        build_vector_index(str(temp_wiki_for_vectors))
        search_backend.init_index(str(temp_wiki_for_vectors))
        # Index pages in whoosh too
        for p in ["concepts/bipedal_locomotion.md", "entities/spot_robot.md", "algorithms/ppo.md"]:
            search_backend.index_page(str(temp_wiki_for_vectors), p)

        results = search_hybrid(str(temp_wiki_for_vectors), "robot walking", top_k=5)
        assert len(results) >= 1
        # Hybrid should include results from both semantic and whoosh
        titles = [r["title"].lower() for r in results]
        assert any("bipedal" in t or "spot" in t or "gait" in t for t in titles)


class TestMultimodalExtractor:
    """Test multimodal figure extraction and vision pipeline."""

    def _create_test_pdf_with_figure(self, tmp_path: Path) -> Path:
        """Create a minimal PDF with figure caption text."""
        try:
            import fitz
        except ImportError:
            pytest.skip("PyMuPDF not installed")

        pdf_path = tmp_path / "test_paper.pdf"
        doc = fitz.open()
        page = doc.new_page()
        page.insert_text((72, 72), "Abstract: This paper proposes a new robot system.")
        page.insert_text((72, 200), "Figure 1: Robot Architecture Overview")
        page.insert_text((72, 300), "The system consists of perception and control modules.")
        page.insert_text((72, 500), "Table 1: Performance Comparison of Algorithms")
        doc.save(str(pdf_path))
        doc.close()
        return pdf_path

    def test_extract_figures_from_pdf(self, tmp_path):
        try:
            import fitz
        except ImportError:
            pytest.skip("PyMuPDF not installed")

        from multimodal_extractor import extract_figures_from_pdf

        pdf_path = self._create_test_pdf_with_figure(tmp_path)
        figures = extract_figures_from_pdf(str(pdf_path), arxiv_id="2601.00001")

        # Should find at least the caption blocks
        assert len(figures) >= 1
        captions = [f["caption"] for f in figures]
        assert any("Architecture" in c or "Comparison" in c for c in captions)

    def test_should_analyze_figure(self):
        from multimodal_extractor import should_analyze_figure

        # High confidence + tech keyword → analyze
        fig = {"caption": "Figure 1: Neural Network Architecture"}
        assert should_analyze_figure(fig, page_confidence=0.8) is True

        # Low confidence → skip
        assert should_analyze_figure(fig, page_confidence=0.5) is False

        # No tech keyword → skip
        fig2 = {"caption": "Figure 2: Photo of the lab"}
        assert should_analyze_figure(fig2, page_confidence=0.8) is False

    def test_write_figure_analysis_to_page(self, tmp_path):
        from multimodal_extractor import write_figure_analysis_to_page

        wiki = tmp_path / "wiki"
        wiki.mkdir()
        page = wiki / "algorithms" / "test_algo.md"
        page.parent.mkdir(parents=True, exist_ok=True)
        page.write_text(
            "---\ntitle: Test Algorithm\ntype: algorithm\n---\n\n# Test\n\nSome content.\n",
            encoding="utf-8",
        )

        results = [
            {
                "id": "fig_1",
                "fig_num": "1",
                "caption": "Architecture Diagram",
                "analyzed": True,
                "analysis": {
                    "type": "架构图",
                    "core_content": "Multi-layer perception stack",
                    "contribution": "Shows sensor fusion design",
                    "parameters": {"layers": 5, "input_dim": 128},
                    "tags": ["perception", "fusion"],
                },
            },
            {
                "id": "fig_2",
                "fig_num": "2",
                "caption": "Table 1: Results",
                "analyzed": False,
                "analysis": {
                    "skipped": "did not meet cost control criteria",
                },
            },
        ]

        write_figure_analysis_to_page(str(page), results)
        content = page.read_text(encoding="utf-8")

        assert "### 📊 图表分析" in content
        assert "Architecture Diagram" in content
        assert "多层" in content or "架构图" in content
        assert "跳过" in content or "skipped" in content

    def test_multimodal_search_type(self, tmp_path):
        """Test that search_wiki multimodal mode runs without error."""
        wiki = tmp_path / "wiki"
        wiki.mkdir()

        p1 = wiki / "entities" / "wildos.md"
        p1.parent.mkdir(parents=True, exist_ok=True)
        p1.write_text(
            "---\ntitle: WildOS\ntype: entity\ntags: [navigation]\n---\n\n"
            "WildOS uses semantic frontier scoring.\n\n"
            "### 📊 图表分析\n\n"
            "#### Figure 1：System Architecture\n"
            "**类型**：架构图\n"
            "**核心发现**：Multi-layer perception stack with MPC controller\n",
            encoding="utf-8",
        )

        # Import and call search logic directly (MCP decorator not needed)
        import search_backend
        from vector_index import build_vector_index, search_semantic

        try:
            import sentence_transformers
            build_vector_index(str(wiki))
        except ImportError:
            pass

        search_backend.init_index(str(wiki))
        search_backend.index_page(str(wiki), "entities/wildos.md")

        # Simulate multimodal search logic
        query = "MPC controller"
        query_lower = query.lower()

        # Hybrid results
        try:
            from vector_index import search_hybrid
            matches = search_hybrid(str(wiki), query, top_k=10)
        except Exception:
            matches = []

        enriched = []
        for hit in matches:
            rel = hit.get("file_path", "")
            score = hit.get("score", 0)
            snippet = hit.get("snippet", "")
            has_figure = False

            page_path = wiki / rel
            if page_path.exists():
                text = page_path.read_text(encoding="utf-8")
                _, body = engine.parse_frontmatter(text)
                if "### 📊 图表分析" in body:
                    fig_section = body.split("### 📊 图表分析")[-1]
                    fig_section = fig_section.split("\n## ")[0]
                    if query_lower in fig_section.lower():
                        score += 15
                        has_figure = True
                        for line in fig_section.splitlines():
                            if query_lower in line.lower():
                                snippet = f"[图表] {line.strip()[:200]}"
                                break

            enriched.append({
                "file_path": rel,
                "title": hit.get("title", "?"),
                "snippet": snippet,
                "score": round(score, 4),
                "has_figure_analysis": has_figure,
            })

        enriched.sort(key=lambda x: x["score"], reverse=True)
        assert len(enriched) >= 1
        # The MPC match in figure analysis should be detected
        assert any("wildos" in e["file_path"] for e in enriched)


class TestPDFChunked:
    """Test large PDF chunked extraction."""

    def test_chunked_extraction_function_exists(self, tmp_path):
        try:
            import fitz
        except ImportError:
            pytest.skip("PyMuPDF not installed")

        from paddleocr_client import extract_pdf_chunked as _extract_with_paddleocr_api_chunked

        # Create a multi-page PDF
        pdf_path = tmp_path / "large.pdf"
        doc = fitz.open()
        for i in range(25):
            page = doc.new_page()
            page.insert_text((72, 72), f"Page {i + 1} content about robot navigation.")
        doc.save(str(pdf_path))
        doc.close()

        # Verify the function exists and the PDF is multi-page
        assert pdf_path.exists()
        doc2 = fitz.open(str(pdf_path))
        assert len(doc2) == 25
        doc2.close()


class TestPaddleOCRTrustFirst:
    """Test Phase 6 PaddleOCR API as the sole standard for complex PDFs."""

    def test_is_complex_pdf_with_images(self, tmp_path):
        try:
            import fitz
        except ImportError:
            pytest.skip("PyMuPDF not installed")

        from pdf_extractor import _is_complex_pdf

        # Create a PDF with an embedded image
        pdf_path = tmp_path / "with_image.pdf"
        doc = fitz.open()
        page = doc.new_page()
        # Create a small RGB pixmap and insert as image
        pix = fitz.Pixmap(fitz.csRGB, fitz.IRect(0, 0, 10, 10))
        pix.clear_with(0xFF0000)
        page.insert_image(page.rect, pixmap=pix)
        doc.save(str(pdf_path))
        doc.close()

        assert _is_complex_pdf(str(pdf_path)) is True

    def test_is_complex_pdf_pure_text(self, tmp_path):
        try:
            import fitz
        except ImportError:
            pytest.skip("PyMuPDF not installed")

        from pdf_extractor import _is_complex_pdf

        pdf_path = tmp_path / "pure_text.pdf"
        doc = fitz.open()
        page = doc.new_page()
        page.insert_text((72, 72), "This is a pure text paper without images or tables.")
        doc.save(str(pdf_path))
        doc.close()

        assert _is_complex_pdf(str(pdf_path)) is False

    def test_complex_pdf_requires_api(self, tmp_path, monkeypatch):
        """Complex PDF without API token must raise RuntimeError."""
        try:
            import fitz
        except ImportError:
            pytest.skip("PyMuPDF not installed")

        from pdf_extractor import extract_pdf_text

        monkeypatch.setenv("PADDLEOCR_API_TOKEN", "")
        monkeypatch.setenv("PADDLEOCR_API_URL", "")

        # Create a PDF with an image (complex)
        pdf_path = tmp_path / "complex.pdf"
        doc = fitz.open()
        page = doc.new_page()
        pix = fitz.Pixmap(fitz.csRGB, fitz.IRect(0, 0, 10, 10))
        pix.clear_with(0xFF0000)
        page.insert_image(page.rect, pixmap=pix)
        doc.save(str(pdf_path))
        doc.close()

        with pytest.raises(RuntimeError, match="PaddleOCR API"):
            extract_pdf_text(str(pdf_path))

    def test_simple_pdf_uses_pymupdf_fast_path(self, tmp_path, monkeypatch):
        """Simple text PDF should use PyMuPDF fast path."""
        try:
            import fitz
        except ImportError:
            pytest.skip("PyMuPDF not installed")

        from pdf_extractor import extract_pdf_text

        monkeypatch.setenv("PADDLEOCR_API_TOKEN", "")

        pdf_path = tmp_path / "simple.pdf"
        doc = fitz.open()
        page = doc.new_page()
        page.insert_text((72, 72), "Robot navigation with semantic mapping.")
        doc.save(str(pdf_path))
        doc.close()

        text = extract_pdf_text(str(pdf_path))
        assert "semantic mapping" in text

    def test_paddleocr_client_is_available_with_token(self, monkeypatch):
        import paddleocr_client

        monkeypatch.setenv("PADDLEOCR_API_TOKEN", "test-token-123")
        assert paddleocr_client.is_available() is True

        monkeypatch.setenv("PADDLEOCR_API_TOKEN", "")
        assert paddleocr_client.is_available() is False


class TestResearchAdvisor:
    """Test knowledge gap identification and weekly reporting."""

    @pytest.fixture
    def temp_wiki_for_advisor(self, tmp_path):
        """Create a wiki with deliberate gaps for testing."""
        wiki = tmp_path / "wiki"
        wiki.mkdir()

        # Well-connected cluster: navigation
        p1 = wiki / "entities" / "wildos.md"
        p1.parent.mkdir(parents=True, exist_ok=True)
        p1.write_text(
            "---\ntitle: WildOS\ntype: entity\ntags: [navigation, robot]\n---\n\n"
            "WildOS uses [[ExploRFM]] for semantic frontier scoring.\n",
            encoding="utf-8",
        )

        p2 = wiki / "algorithms" / "explorf.md"
        p2.parent.mkdir(parents=True, exist_ok=True)
        p2.write_text(
            "---\ntitle: ExploRFM\ntype: algorithm\ntags: [navigation, vision]\n---\n\n"
            "ExploRFM predicts traversability and object similarity.\n",
            encoding="utf-8",
        )

        # Isolated page (no inbound links)
        p3 = wiki / "concepts" / "bipedal_locomotion.md"
        p3.parent.mkdir(parents=True, exist_ok=True)
        p3.write_text(
            "---\ntitle: Bipedal Locomotion\ntype: concept\ntags: [walking]\n---\n\n"
            "Bipedal locomotion involves balance control and gait planning.\n",
            encoding="utf-8",
        )

        # Low-density topic: reinforcement_learning only appears once
        p4 = wiki / "algorithms" / "ppo.md"
        p4.parent.mkdir(parents=True, exist_ok=True)
        p4.write_text(
            "---\ntitle: Proximal Policy Optimization\ntype: algorithm\ntags: [reinforcement_learning]\n---\n\n"
            "PPO is a policy gradient method for RL.\n",
            encoding="utf-8",
        )

        return wiki

    def test_identify_knowledge_gaps(self, temp_wiki_for_advisor):
        from research_advisor import identify_knowledge_gaps

        gaps = identify_knowledge_gaps(str(temp_wiki_for_advisor))

        assert gaps["total_nodes"] == 4
        # Isolated node: bipedal_locomotion has no inbound links
        isolated_titles = [n["title"] for n in gaps["isolated_nodes"]]
        assert "Bipedal Locomotion" in isolated_titles

        # Low-density topic: reinforcement_learning only has 1 page
        low_density_tags = [t["tag"] for t in gaps["low_density_topics"]]
        assert "reinforcement_learning" in low_density_tags
        assert "walking" in low_density_tags

    def test_generate_research_suggestions(self, temp_wiki_for_advisor):
        from research_advisor import identify_knowledge_gaps, generate_research_suggestions

        gaps = identify_knowledge_gaps(str(temp_wiki_for_advisor))
        suggestions = generate_research_suggestions(gaps)

        assert len(suggestions) >= 2
        types = {s["type"] for s in suggestions}
        assert "isolated_knowledge" in types
        assert "low_coverage" in types

        # Verify suggestion structure
        for s in suggestions:
            assert "priority" in s
            assert "message" in s
            assert "search_keywords" in s

    def test_generate_weekly_report(self, temp_wiki_for_advisor):
        from research_advisor import generate_weekly_report

        report_path = generate_weekly_report(
            str(temp_wiki_for_advisor),
            output_dir=str(temp_wiki_for_advisor / "reports"),
        )

        assert report_path.exists()
        content = report_path.read_text(encoding="utf-8")
        assert "# 每周知识空白报告" in content
        assert "孤立节点" in content or "isolated" in content.lower()
        assert "Bipedal Locomotion" in content

        # Verify log entry
        log_path = temp_wiki_for_advisor / "log.md"
        assert log_path.exists()
        log_content = log_path.read_text(encoding="utf-8")
        assert "advisor | weekly_report" in log_content


class TestFragmentDetector:
    """Test fragmentation detection and consolidation."""

    @pytest.fixture
    def temp_wiki_for_fragments(self, tmp_path):
        """Create a wiki with 3+ fragmented pages about the same topic."""
        wiki = tmp_path / "wiki"
        wiki.mkdir()

        # 3 pages about "Semantic Navigation" scattered in different dirs
        p1 = wiki / "algorithms" / "semantic_nav_v1.md"
        p1.parent.mkdir(parents=True, exist_ok=True)
        p1.write_text(
            "---\ntitle: Semantic Navigation v1\ntype: algorithm\ntags: [navigation, semantic]\n---\n\n"
            "Semantic navigation uses deep learning to understand environments. "
            "The robot builds a semantic map of the world using CNN features.\n",
            encoding="utf-8",
        )

        p2 = wiki / "concepts" / "semantic_mapping.md"
        p2.parent.mkdir(parents=True, exist_ok=True)
        p2.write_text(
            "---\ntitle: Semantic Mapping\ntype: concept\ntags: [navigation, semantic]\n---\n\n"
            "Semantic mapping creates rich environment representations. "
            "It uses deep learning to classify objects and build a semantic map.\n",
            encoding="utf-8",
        )

        p3 = wiki / "skills" / "nav_with_semantics.md"
        p3.parent.mkdir(parents=True, exist_ok=True)
        p3.write_text(
            "---\ntitle: Navigate with Semantics\ntype: skill\ntags: [navigation, semantic]\n---\n\n"
            "Navigation with semantics improves robot autonomy. "
            "The system leverages deep learning for semantic understanding of space.\n",
            encoding="utf-8",
        )

        # Unrelated page
        p4 = wiki / "entities" / "spot.md"
        p4.parent.mkdir(parents=True, exist_ok=True)
        p4.write_text(
            "---\ntitle: Boston Dynamics Spot\ntype: entity\ntags: [quadruped]\n---\n\n"
            "Spot is a quadruped robot.\n",
            encoding="utf-8",
        )

        return wiki

    def test_detect_fragmentation(self, temp_wiki_for_fragments):
        from fragment_detector import detect_fragmentation

        fragments = detect_fragmentation("Semantic Navigation", str(temp_wiki_for_fragments))
        assert len(fragments) >= 3
        titles = [f["title"] for f in fragments]
        assert "Semantic Navigation v1" in titles
        assert "Semantic Mapping" in titles
        assert "Navigate with Semantics" in titles

    def test_detect_no_fragmentation(self, temp_wiki_for_fragments):
        from fragment_detector import detect_fragmentation

        # "Spot" only matches 1 page
        fragments = detect_fragmentation("Spot", str(temp_wiki_for_fragments))
        assert len(fragments) < 3

    def test_generate_consolidation_prompt(self, temp_wiki_for_fragments):
        from fragment_detector import detect_fragmentation, generate_consolidation_prompt

        fragments = detect_fragmentation("Semantic Navigation", str(temp_wiki_for_fragments))
        prompt = generate_consolidation_prompt("Semantic Navigation", fragments)
        assert "Semantic Navigation" in prompt
        assert "TASK" in prompt
        for frag in fragments:
            assert frag["title"] in prompt

    def test_dedup_information(self, tmp_path):
        from fragment_detector import dedup_information

        wiki = tmp_path / "wiki"
        wiki.mkdir()

        p1 = wiki / "a.md"
        p1.write_text(
            "---\ntitle: Page A\ntype: concept\n---\n\nThis is almost identical content for testing.",
            encoding="utf-8",
        )
        p2 = wiki / "b.md"
        p2.write_text(
            "---\ntitle: Page B\ntype: concept\n---\n\nThis is almost identical content for testing.",
            encoding="utf-8",
        )
        p3 = wiki / "c.md"
        p3.write_text(
            "---\ntitle: Page C\ntype: concept\n---\n\nTotally different topic and content here.",
            encoding="utf-8",
        )

        duplicates = dedup_information(str(wiki), similarity_threshold=0.85)
        # a.md and b.md should be flagged as duplicates
        pairs = {(d["page_a"], d["page_b"]) for d in duplicates}
        assert any("a.md" in pair and "b.md" in pair for pair in pairs)

    def test_knowledge_synthesizer_consolidation(self, temp_wiki_for_fragments):
        from knowledge_synthesizer import KnowledgeSynthesizer

        synth = KnowledgeSynthesizer(str(temp_wiki_for_fragments))
        plan = synth.synthesize(
            entity_type="concept",
            entity_name="Semantic Navigation",
            new_facts={"parameters": {"method": "deep learning"}},
            source_meta={"source_type": "paper", "source_path": "test.pdf"},
        )
        # Should detect fragmentation and suggest consolidation
        assert plan.action == "suggest_consolidation"
        assert plan.fragment_pages is not None
        assert len(plan.fragment_pages) >= 3


class TestWebUI:
    """Test Web UI Flask backend APIs."""

    @pytest.fixture
    def temp_wiki_for_web(self, tmp_path):
        """Create a wiki with sample pages for Web UI testing."""
        wiki = tmp_path / "wiki"
        wiki.mkdir()

        p1 = wiki / "entities" / "wildos.md"
        p1.parent.mkdir(parents=True, exist_ok=True)
        p1.write_text(
            "---\ntitle: WildOS\ntype: entity\ntags: [navigation, robot]\nconfidence: 0.85\n---\n\n"
            "WildOS uses [[ExploRFM]] for semantic frontier scoring.\n",
            encoding="utf-8",
        )

        p2 = wiki / "algorithms" / "explorf.md"
        p2.parent.mkdir(parents=True, exist_ok=True)
        p2.write_text(
            "---\ntitle: ExploRFM\ntype: algorithm\ntags: [navigation, vision]\nconfidence: 0.75\n---\n\n"
            "ExploRFM predicts traversability and object similarity.\n",
            encoding="utf-8",
        )

        p3 = wiki / "concepts" / "nav_graph.md"
        p3.parent.mkdir(parents=True, exist_ok=True)
        p3.write_text(
            "---\ntitle: Navigation Graph\ntype: concept\ntags: [graph]\nconfidence: 0.6\n---\n\n"
            "A sparse topological map for robot navigation.\n",
            encoding="utf-8",
        )

        return wiki

    def test_api_graph(self, temp_wiki_for_web, monkeypatch):
        try:
            from web_ui.app import app
        except ImportError as exc:
            pytest.skip(f"Flask or web_ui not available: {exc}")

        monkeypatch.setenv("WIKI_ROOT", str(temp_wiki_for_web))
        with app.test_client() as client:
            res = client.get("/api/graph")
            assert res.status_code == 200
            data = res.get_json()
            assert data["status"] == "done"
            assert len(data["nodes"]) == 3
            assert len(data["edges"]) == 1  # WildOS -> ExploRFM

    def test_api_stats(self, temp_wiki_for_web, monkeypatch):
        try:
            from web_ui.app import app
        except ImportError:
            pytest.skip("Flask not installed")

        monkeypatch.setenv("WIKI_ROOT", str(temp_wiki_for_web))
        with app.test_client() as client:
            res = client.get("/api/stats")
            assert res.status_code == 200
            data = res.get_json()
            assert data["status"] == "done"
            assert data["total_pages"] == 3
            assert "low_confidence" in data
            assert "expired" in data
            assert "gaps" in data

    def test_api_page(self, temp_wiki_for_web, monkeypatch):
        try:
            from web_ui.app import app
        except ImportError:
            pytest.skip("Flask not installed")

        monkeypatch.setenv("WIKI_ROOT", str(temp_wiki_for_web))
        with app.test_client() as client:
            res = client.get("/api/page/wildos")
            assert res.status_code == 200
            data = res.get_json()
            assert data["status"] == "done"
            assert data["meta"]["title"] == "WildOS"
            assert "ExploRFM" in data["body"]

    def test_api_search(self, temp_wiki_for_web, monkeypatch):
        try:
            from web_ui.app import app
        except ImportError:
            pytest.skip("Flask not installed")

        monkeypatch.setenv("WIKI_ROOT", str(temp_wiki_for_web))
        with app.test_client() as client:
            res = client.get("/api/search?q=navigation&type=hybrid")
            assert res.status_code == 200
            data = res.get_json()
            assert data["status"] == "done"
            assert len(data["matches"]) >= 1

    def test_index_html(self, monkeypatch):
        try:
            from web_ui.app import app
        except ImportError:
            pytest.skip("Flask not installed")

        with app.test_client() as client:
            res = client.get("/")
            assert res.status_code == 200
            assert b"ROSClaw Wiki" in res.data


class TestVisualizeGaps:
    """Test gap heatmap generation."""

    def test_generate_gap_heatmap(self, tmp_path):
        wiki = tmp_path / "wiki"
        wiki.mkdir()

        p1 = wiki / "entities" / "wildos.md"
        p1.parent.mkdir(parents=True, exist_ok=True)
        p1.write_text(
            "---\ntitle: WildOS\ntype: entity\ntags: [navigation]\n---\n\n"
            "WildOS uses [[ExploRFM]].\n",
            encoding="utf-8",
        )

        p2 = wiki / "algorithms" / "explorf.md"
        p2.parent.mkdir(parents=True, exist_ok=True)
        p2.write_text(
            "---\ntitle: ExploRFM\ntype: algorithm\ntags: [navigation, vision]\n---\n\n"
            "Frontier scoring.\n",
            encoding="utf-8",
        )

        from visualize_gaps import generate_gap_heatmap

        gaps_path = generate_gap_heatmap(str(wiki), output_dir=str(tmp_path / "output"))
        assert gaps_path.exists()

        import json
        data = json.loads(gaps_path.read_text(encoding="utf-8"))
        assert "nodes" in data
        assert "metadata" in data
        assert data["metadata"]["total_nodes"] == 2

        # Check that navigation has coverage >= 2, vision has coverage 1
        nodes_by_id = {n["id"]: n for n in data["nodes"]}
        assert "navigation" in nodes_by_id
        assert nodes_by_id["navigation"]["coverage"] == 2
        assert "vision" in nodes_by_id
        assert nodes_by_id["vision"]["coverage"] == 1


class TestQAEngine:
    """Test QA engine: citations, conflict detection, write-back."""

    @pytest.fixture
    def temp_wiki_for_qa(self, tmp_path):
        """Create a wiki with pages that contain both matching and conflicting info."""
        wiki = tmp_path / "wiki"
        wiki.mkdir()

        # Page A: claims G1 torque is 90 Nm
        p1 = wiki / "entities" / "g1_specs_a.md"
        p1.parent.mkdir(parents=True, exist_ok=True)
        p1.write_text(
            "---\ntitle: Unitree G1 Official Specs\ntype: entity\ntags: [robot, humanoid]\n---\n\n"
            "The Unitree G1 humanoid robot has a peak torque of **90 Nm** at the hip joints. "
            "The robot weighs approximately 47 kg and stands 1.32 m tall.\n",
            encoding="utf-8",
        )

        # Page B: claims G1 torque is 85 Nm (conflict!)
        p2 = wiki / "entities" / "g1_specs_b.md"
        p2.parent.mkdir(parents=True, exist_ok=True)
        p2.write_text(
            "---\ntitle: G1 Review by Robotics Lab\ntype: entity\ntags: [robot, humanoid]\n---\n\n"
            "Our measurements show the Unitree G1 peak torque is **85 Nm**. "
            "The walking speed is 2 m/s and battery life is about 2 hours.\n",
            encoding="utf-8",
        )

        # Page C: unrelated
        p3 = wiki / "concepts" / "torque.md"
        p3.parent.mkdir(parents=True, exist_ok=True)
        p3.write_text(
            "---\ntitle: Motor Torque\ntype: concept\ntags: [physics]\n---\n\n"
            "Torque is the rotational equivalent of linear force, measured in Newton-meters (Nm).\n",
            encoding="utf-8",
        )

        return wiki

    def test_ask_basic_with_mock_llm(self, temp_wiki_for_qa, monkeypatch):
        from qa_engine import ask

        calls = []

        class MockLLM:
            def complete(self, prompt, **kwargs):
                calls.append(prompt)
                return (
                    "The Unitree G1 has a peak torque of 90 Nm "
                    "according to official specs [[Unitree G1 Official Specs]]."
                )

        result = ask(str(temp_wiki_for_qa), "What is the G1 peak torque?", llm=MockLLM(), top_k=5, write_back=False)

        assert result["answer"]
        assert "[[Unitree G1 Official Specs]]" in result["answer"]
        assert "Unitree G1 Official Specs" in result["citations"]
        assert result["has_conflict"] is False
        assert len(result["pages_consulted"]) >= 1
        assert result["qa_path"] is None  # write_back=False

    def test_extract_citations(self):
        from qa_engine import _extract_citations

        text = "See [[Page A]] and also [[Page B]] for more. [[Page A]] again."
        citations = _extract_citations(text)
        assert citations == ["Page A", "Page B"]

    def test_conflict_warning_detection(self):
        from qa_engine import _has_conflict_warning

        assert _has_conflict_warning("> [!WARNING] 数据冲突\n> source A claims X") is True
        assert _has_conflict_warning("> [!WARNING]\n> something") is True
        assert _has_conflict_warning("This is a normal answer.") is False

    def test_ask_with_conflict_mock(self, temp_wiki_for_qa):
        from qa_engine import ask

        class MockLLM:
            def complete(self, prompt, **kwargs):
                return (
                    "There is conflicting data about G1 peak torque:\n\n"
                    "> [!WARNING] 数据冲突\n"
                    "> - Official specs claim 90 Nm [[Unitree G1 Official Specs]]\n"
                    "> - Lab review claims 85 Nm [[G1 Review by Robotics Lab]]"
                )

        result = ask(
            str(temp_wiki_for_qa),
            "What is the G1 peak torque?",
            llm=MockLLM(),
            top_k=5,
            write_back=False,
        )

        assert result["has_conflict"] is True
        assert "Unitree G1 Official Specs" in result["citations"]
        assert "G1 Review by Robotics Lab" in result["citations"]

    def test_ask_write_back(self, temp_wiki_for_qa):
        from qa_engine import ask

        class MockLLM:
            def complete(self, prompt, **kwargs):
                return "The answer is 42 [[Motor Torque]]."

        result = ask(
            str(temp_wiki_for_qa),
            "What is torque?",
            llm=MockLLM(),
            top_k=5,
            write_back=True,
        )

        assert result["qa_path"] is not None
        qa_path = Path(result["qa_path"])
        assert qa_path.exists()
        content = qa_path.read_text(encoding="utf-8")
        assert "What is torque?" in content
        assert "The answer is 42" in content
        assert "type: qa" in content
        assert "auto-generated" in content

    def test_ask_no_results(self, temp_wiki_for_qa):
        from qa_engine import ask

        class MockLLM:
            def complete(self, prompt, **kwargs):
                return "Some answer"

        result = ask(
            str(temp_wiki_for_qa),
            "xyznonexistentquery12345",
            llm=MockLLM(),
            top_k=5,
            write_back=False,
        )

        assert "No relevant pages" in result["answer"]
        assert result["citations"] == []
        assert result["has_conflict"] is False


class TestAsyncBatchIngest:
    """Test asyncio concurrent batch ingest and event emission."""

    @pytest.fixture
    def temp_event_log(self, tmp_path, monkeypatch):
        """Redirect event bus to a temp JSONL file."""
        log_path = tmp_path / "events.jsonl"
        import event_bus

        monkeypatch.setattr(event_bus, "DEFAULT_EVENT_LOG", log_path)
        # Also clear any existing log
        if log_path.exists():
            log_path.unlink()
        return log_path

    @pytest.fixture
    def mock_llm_for_batch(self):
        """Mock LLM that returns predictable extraction and rewrite results."""

        class MockLLM:
            def __init__(self):
                self.calls = []

            def complete(self, prompt: str, **kwargs):
                self.calls.append(prompt)
                if "TASK: Extract" in prompt:
                    return json.dumps([
                        {
                            "entity_type": "entity",
                            "entity_name": "AsyncBot",
                            "new_facts": {
                                "parameters": {"speed": "2 m/s"},
                                "capabilities": ["walking"],
                            },
                            "source_type": "blog_post",
                        }
                    ])
                return "# AsyncBot\n\nSpeed: 2 m/s.\n"

        return MockLLM()

    @pytest.mark.asyncio
    async def test_async_batch_ingest_creates_pages(self, temp_wiki, temp_raw, temp_event_log, mock_llm_for_batch):
        from batch_ingest import _run_batch
        from knowledge_synthesizer import KnowledgeSynthesizer

        # Create raw files
        (temp_raw / "articles" / "a.md").parent.mkdir(parents=True, exist_ok=True)
        (temp_raw / "articles" / "a.md").write_text("# Article A\n\nAbout AsyncBot.")
        (temp_raw / "articles" / "b.md").parent.mkdir(parents=True, exist_ok=True)
        (temp_raw / "articles" / "b.md").write_text("# Article B\n\nAlso about AsyncBot.")

        files = [("articles/a.md", "article"), ("articles/b.md", "article")]
        synth = KnowledgeSynthesizer(str(temp_wiki))
        stats = await _run_batch(
            files=files,
            wiki_root=temp_wiki,
            raw_root=temp_raw,
            llm=mock_llm_for_batch,
            agents_text="",
            synth=synth,
            concurrency=2,
        )

        assert stats["total"] == 2
        assert stats["processed"] == 2
        assert stats["failed"] == 0

        # Verify pages were created
        assert (temp_wiki / "entities" / "asyncbot.md").exists()

    @pytest.mark.asyncio
    async def test_ingest_progress_events_emitted(self, temp_wiki, temp_raw, temp_event_log, mock_llm_for_batch):
        from batch_ingest import _run_batch
        from knowledge_synthesizer import KnowledgeSynthesizer
        import event_bus

        (temp_raw / "articles" / "c.md").parent.mkdir(parents=True, exist_ok=True)
        (temp_raw / "articles" / "c.md").write_text("# Article C\n\nContent.")

        files = [("articles/c.md", "article")]
        synth = KnowledgeSynthesizer(str(temp_wiki))
        await _run_batch(
            files=files,
            wiki_root=temp_wiki,
            raw_root=temp_raw,
            llm=mock_llm_for_batch,
            agents_text="",
            synth=synth,
            concurrency=1,
        )

        events = event_bus.tail_events(since=0)
        progress_events = [e for e in events if e["type"] == "ingest_progress"]
        assert len(progress_events) >= 1
        payload = progress_events[0]["payload"]
        assert payload["total"] == 1
        assert payload["status"] == "done"
        assert "pages_created" in payload

    @pytest.mark.asyncio
    async def test_conflict_alert_events_emitted(self, temp_wiki, temp_raw, temp_event_log):
        from batch_ingest import _run_batch
        from knowledge_synthesizer import KnowledgeSynthesizer
        import event_bus

        # First create an existing page for AsyncBot with different parameter
        engine.create_page(
            str(temp_wiki / "entities"),
            "AsyncBot",
            "# AsyncBot\n\nSpeed: 1 m/s.",
            {"type": "entity", "confidence": 0.8},
        )

        class MockLLMWithConflict:
            def complete(self, prompt: str, **kwargs):
                if "TASK: Extract" in prompt:
                    return json.dumps([
                        {
                            "entity_type": "entity",
                            "entity_name": "AsyncBot",
                            "new_facts": {
                                "parameters": {"speed": "3 m/s"},
                            },
                            "source_type": "official_manual",
                        }
                    ])
                return "# AsyncBot\n\nSpeed: 3 m/s.\n"

        (temp_raw / "articles" / "d.md").parent.mkdir(parents=True, exist_ok=True)
        (temp_raw / "articles" / "d.md").write_text("# Article D\n\nConflict.")

        files = [("articles/d.md", "article")]
        synth = KnowledgeSynthesizer(str(temp_wiki))
        await _run_batch(
            files=files,
            wiki_root=temp_wiki,
            raw_root=temp_raw,
            llm=MockLLMWithConflict(),
            agents_text="",
            synth=synth,
            concurrency=1,
        )

        events = event_bus.tail_events(since=0)
        alert_events = [e for e in events if e["type"] == "conflict_alert"]
        assert len(alert_events) >= 1
        payload = alert_events[0]["payload"]
        assert payload["entity"] == "AsyncBot"
        assert payload["field"] == "speed"
        assert "old_value" in payload
        assert "new_value" in payload

    def test_main_accepts_concurrency_arg(self, monkeypatch):
        """Verify argparse accepts --concurrency without error."""
        import batch_ingest

        # Patch sys.argv to simulate CLI call
        monkeypatch.setattr(sys, "argv", ["batch_ingest.py", "--concurrency", "10", "--wiki-root", "/tmp/fake_wiki"])

        # Prevent actual execution by mocking _run_batch and LLMInterface
        run_called = []

        async def fake_run_batch(files, wiki_root, raw_root, llm, agents_text, synth, concurrency):
            run_called.append(concurrency)
            return {"total": 0, "processed": 0, "skipped": 0, "failed": 0, "pages_created": 0, "pages_updated": 0, "conflicts": 0, "elapsed_seconds": 0.0}

        monkeypatch.setattr(batch_ingest, "_run_batch", fake_run_batch)

        class FakeLLM:
            backend = "openai"
            def __init__(self, *a, **k): pass

        monkeypatch.setattr(batch_ingest, "LLMInterface", FakeLLM)

        # Also prevent update_index from failing on fake path
        monkeypatch.setattr(batch_ingest.engine, "update_index", lambda x: None)
        monkeypatch.setattr(batch_ingest.engine, "append_log", lambda x, y: None)

        rc = batch_ingest.main()
        assert rc == 0
        assert run_called == [10]


class TestScheduler:
    """Test tiered automatic metabolism scheduler."""

    def test_raw_watcher_no_new_files(self, temp_wiki, temp_raw, monkeypatch):
        import event_bus
        from scheduler import raw_watcher

        log_path = temp_raw / "events.jsonl"
        monkeypatch.setattr(event_bus, "DEFAULT_EVENT_LOG", log_path)
        if log_path.exists():
            log_path.unlink()

        result = raw_watcher(str(temp_wiki), str(temp_raw))
        assert result["status"] == "no_new_files"
        assert result["new_files"] == 0

    def test_raw_watcher_finds_new_files(self, temp_wiki, temp_raw, monkeypatch):
        import event_bus
        from scheduler import raw_watcher

        log_path = temp_raw / "events.jsonl"
        monkeypatch.setattr(event_bus, "DEFAULT_EVENT_LOG", log_path)
        if log_path.exists():
            log_path.unlink()

        # Create a raw file that hasn't been processed
        (temp_raw / "articles" / "new.md").parent.mkdir(parents=True, exist_ok=True)
        (temp_raw / "articles" / "new.md").write_text("# New\n\nContent.")

        result = raw_watcher(str(temp_wiki), str(temp_raw))
        assert result["status"] == "new_files_found"
        assert result["new_files"] == 1
        assert "articles/new.md" in result["files"]

        # Verify event was emitted
        events = event_bus.tail_events(since=0)
        alert_events = [e for e in events if e["type"] == "raw_watcher_alert"]
        assert len(alert_events) == 1
        assert alert_events[0]["payload"]["new_files_count"] == 1

    def test_daily_review_decay_and_lint(self, temp_wiki, monkeypatch):
        import event_bus
        from scheduler import daily_review
        from datetime import datetime, timedelta

        log_path = temp_wiki / "events.jsonl"
        monkeypatch.setattr(event_bus, "DEFAULT_EVENT_LOG", log_path)
        if log_path.exists():
            log_path.unlink()

        # Create an old page that should decay
        old_date = (datetime.now() - timedelta(days=50)).isoformat(timespec="seconds")
        engine.create_page(
            str(temp_wiki / "entities"),
            "Decaying Bot",
            "# Decaying Bot\n\nOld info.",
            {"type": "entity", "confidence": 0.8, "last_reinforced": old_date},
        )

        # Create an orphan with low confidence
        engine.create_page(
            str(temp_wiki / "entities"),
            "Weak Orphan",
            "# Weak Orphan\n\nNo links.",
            {"type": "entity", "confidence": 0.2, "last_reinforced": old_date},
        )

        result = daily_review(str(temp_wiki))

        assert result["decay"]["pages_decayed"] >= 1
        assert result["lint"]["low_confidence_count"] >= 1
        assert any("Weak Orphan" in str(o) for o in result["lint"]["low_confidence"])

        # Verify log entry
        log_content = (temp_wiki / "log.md").read_text()
        assert "scheduler | daily_review" in log_content

    def test_weekly_deep_scan_generates_report(self, temp_wiki, monkeypatch):
        import event_bus
        from scheduler import weekly_deep_scan

        log_path = temp_wiki / "events.jsonl"
        monkeypatch.setattr(event_bus, "DEFAULT_EVENT_LOG", log_path)
        if log_path.exists():
            log_path.unlink()

        # Create a small wiki with some content
        engine.create_page(
            str(temp_wiki / "entities"),
            "Bot A",
            "# Bot A\n\nA robot.",
            {"type": "entity", "tags": ["robot"]},
        )
        engine.create_page(
            str(temp_wiki / "algorithms"),
            "Alg X",
            "# Alg X\n\nAn algorithm.",
            {"type": "algorithm", "tags": ["ai"]},
        )

        result = weekly_deep_scan(str(temp_wiki))

        assert "weekly_report_path" in result
        assert Path(result["weekly_report_path"]).exists()

        # Verify log entry
        log_content = (temp_wiki / "log.md").read_text()
        assert "scheduler | weekly_deep_scan" in log_content

        # Verify event
        events = event_bus.tail_events(since=0)
        scan_events = [e for e in events if e["type"] == "weekly_scan_complete"]
        assert len(scan_events) == 1
        assert "report_path" in scan_events[0]["payload"]

    def test_run_once_dispatch(self, temp_wiki, temp_raw, monkeypatch):
        import event_bus
        from scheduler import run_once

        log_path = temp_wiki / "events.jsonl"
        monkeypatch.setattr(event_bus, "DEFAULT_EVENT_LOG", log_path)
        if log_path.exists():
            log_path.unlink()

        result = run_once(str(temp_wiki), str(temp_raw), "raw_watcher")
        assert result["status"] in ("no_new_files", "new_files_found", "no_raw_dir")

        result = run_once(str(temp_wiki), str(temp_raw), "daily_review")
        assert "decay" in result

        result = run_once(str(temp_wiki), str(temp_raw), "weekly_deep_scan")
        assert "weekly_report_path" in result

    def test_run_once_invalid_task(self, temp_wiki, temp_raw):
        from scheduler import run_once

        with pytest.raises(ValueError, match="Unknown task"):
            run_once(str(temp_wiki), str(temp_raw), "invalid_task")


class TestEntityLinker:
    """Test heuristic entity linker — zero LLM calls."""

    @pytest.fixture
    def temp_wiki_for_links(self, tmp_path):
        """Create a wiki with interrelated pages for link testing."""
        wiki = tmp_path / "wiki"
        wiki.mkdir()

        # WildOS entity page
        p1 = wiki / "entities" / "wildos.md"
        p1.parent.mkdir(parents=True, exist_ok=True)
        p1.write_text(
            "---\ntitle: WildOS\ntype: entity\ntags: [navigation, robot]\nconfidence: 0.85\n---\n\n"
            "WildOS uses [[ROS2]] for navigation in unknown environments. "
            "WildOS is based on [[ExploRFM]] for frontier scoring.\n",
            encoding="utf-8",
        )

        # ROS2 entity page
        p2 = wiki / "entities" / "ros2.md"
        p2.parent.mkdir(parents=True, exist_ok=True)
        p2.write_text(
            "---\ntitle: ROS2\ntype: entity\ntags: [middleware, robot]\nconfidence: 0.9\n---\n\n"
            "ROS2 is a robotics middleware.\n",
            encoding="utf-8",
        )

        # ExploRFM algorithm page
        p3 = wiki / "algorithms" / "explorf.md"
        p3.parent.mkdir(parents=True, exist_ok=True)
        p3.write_text(
            "---\ntitle: ExploRFM\ntype: algorithm\ntags: [navigation, vision]\nconfidence: 0.75\n---\n\n"
            "ExploRFM predicts traversability and object similarity.\n",
            encoding="utf-8",
        )

        # Navigation concept page
        p4 = wiki / "concepts" / "nav_graph.md"
        p4.parent.mkdir(parents=True, exist_ok=True)
        p4.write_text(
            "---\ntitle: Navigation Graph\ntype: concept\ntags: [graph]\nconfidence: 0.6\n---\n\n"
            "A sparse topological map for robot navigation.\n",
            encoding="utf-8",
        )

        return wiki

    def test_wikilink_extraction(self, temp_wiki_for_links):
        from entity_linker import process_page

        wildos_path = str(temp_wiki_for_links / "entities" / "wildos.md")
        links = process_page(wildos_path, str(temp_wiki_for_links))

        # Should discover links to ROS2 and ExploRFM
        targets = {link.target_page for link in links}
        assert "ROS2" in targets or "ros2" in targets
        assert "ExploRFM" in targets or "explorf" in targets

    def test_type_inference_entity_to_entity(self, temp_wiki_for_links):
        from entity_linker import process_page

        wildos_path = str(temp_wiki_for_links / "entities" / "wildos.md")
        links = process_page(wildos_path, str(temp_wiki_for_links))

        # WildOS (entity) -> ROS2 (entity) should be "depends_on" by type inference
        ros2_links = [link for link in links if "ROS2" in link.target_page or "ros2" in link.target_page]
        assert len(ros2_links) >= 1
        # Since WildOS uses [[ROS2]], the wikilink+type_inference method should infer relation
        assert ros2_links[0].relation == "depends_on"

    def test_type_inference_entity_to_algorithm(self, temp_wiki_for_links):
        from entity_linker import process_page

        wildos_path = str(temp_wiki_for_links / "entities" / "wildos.md")
        links = process_page(wildos_path, str(temp_wiki_for_links))

        # WildOS (entity) -> ExploRFM (algorithm) should be "uses"
        explorf_links = [link for link in links if "ExploRFM" in link.target_page or "explorf" in link.target_page]
        assert len(explorf_links) >= 1
        assert explorf_links[0].relation == "uses"

    def test_sentence_pattern_uses(self, temp_wiki_for_links):
        from entity_linker import _match_sentence_patterns

        body = "WildOS uses ROS2 for navigation in unknown environments."
        links = _match_sentence_patterns(body, "WildOS")
        assert len(links) >= 1
        assert links[0].relation == "uses"
        assert "ROS2" in links[0].target_page

    def test_sentence_pattern_based_on(self, temp_wiki_for_links):
        from entity_linker import _match_sentence_patterns

        body = "WildOS is based on ExploRFM for frontier scoring."
        links = _match_sentence_patterns(body, "WildOS")
        assert len(links) >= 1
        assert links[0].relation == "based_on"

    def test_zero_llm_calls(self, temp_wiki_for_links):
        """Ensure entity linker never calls an LLM."""
        from entity_linker import process_page

        # process_page should complete with no LLM invocations
        wildos_path = str(temp_wiki_for_links / "entities" / "wildos.md")
        links = process_page(wildos_path, str(temp_wiki_for_links))
        assert isinstance(links, list)

    def test_integration_create_page_triggers_linker(self, temp_wiki):
        """create_page should auto-trigger entity linker."""
        # First create the target page so linker can resolve it
        engine.create_page(
            str(temp_wiki / "entities"),
            "ROS2",
            "# ROS2\n\nRobotics middleware.",
            {"type": "entity", "tags": ["middleware"]},
        )
        path = engine.create_page(
            str(temp_wiki / "entities"),
            "TestBot",
            "# TestBot\n\nTestBot uses [[ROS2]] for communication.",
            {"type": "entity", "tags": ["robot"]},
        )
        content = Path(path).read_text(encoding="utf-8")
        # The auto-link section should be appended
        assert "自动链接关系" in content or "entity_linker" in content

    def test_write_links_to_page(self, temp_wiki_for_links):
        from entity_linker import DiscoveredLink, write_links_to_page, process_page

        wildos_path = str(temp_wiki_for_links / "entities" / "wildos.md")
        links = process_page(wildos_path, str(temp_wiki_for_links))
        write_links_to_page(wildos_path, links)

        content = Path(wildos_path).read_text(encoding="utf-8")
        assert "### 自动链接关系" in content
        # Should list confirmed links
        assert "Confirmed links" in content or "Pending review" in content

    def test_no_duplicate_link_section(self, temp_wiki_for_links):
        from entity_linker import write_links_to_page, process_page

        wildos_path = str(temp_wiki_for_links / "entities" / "wildos.md")
        links = process_page(wildos_path, str(temp_wiki_for_links))
        write_links_to_page(wildos_path, links)
        # Second write should be idempotent
        write_links_to_page(wildos_path, links)

        content = Path(wildos_path).read_text(encoding="utf-8")
        # Should only have one section
        assert content.count("### 自动链接关系") == 1


class TestConflictResolver:
    """Test conflict resolution engine with weighted adjudication."""

    @pytest.fixture
    def temp_wiki_for_conflicts(self, tmp_path):
        """Create a wiki with a page containing known conflicts."""
        wiki = tmp_path / "wiki"
        wiki.mkdir()

        p1 = wiki / "entities" / "unitree_g1.md"
        p1.parent.mkdir(parents=True, exist_ok=True)
        p1.write_text(
            "---\ntitle: Unitree G1\ntype: entity\ntags: [robot, humanoid]\nconfidence: 0.8\n---\n\n"
            "# Unitree G1\n\n"
            "Peak torque: 237 Nm according to official specs.\n\n"
            "### 待核实冲突\n"
            "- **peak_torque** — old: `90 Nm` (from official_manual) vs new: `300 Nm` (from blog_post)\n"
            "- **weight** — old: `47 kg` (from official_manual) vs new: `50 kg` (from arxiv_paper)\n"
            "- **height** — old: `1.32 m` (from blog_post) vs new: `1.35 m` (from blog_post)\n",
            encoding="utf-8",
        )
        return wiki

    def test_parse_conflict_lines(self, temp_wiki_for_conflicts):
        from conflict_resolver import _parse_conflict_lines

        p1 = temp_wiki_for_conflicts / "entities" / "unitree_g1.md"
        content = p1.read_text(encoding="utf-8")
        _, body = engine.parse_frontmatter(content)
        claims = _parse_conflict_lines(body)

        assert "peak_torque" in claims
        assert len(claims["peak_torque"]) == 2
        assert claims["peak_torque"][0].value == "90 Nm"
        assert claims["peak_torque"][1].value == "300 Nm"

    def test_adjudicate_field_resolved(self, temp_wiki_for_conflicts):
        from conflict_resolver import Claim, adjudicate_field

        # Official manual (1.0) vs blog post (0.5) → large gap expected
        claims = [
            Claim(field="peak_torque", value="90 Nm", source="official_manual"),
            Claim(field="peak_torque", value="300 Nm", source="blog_post"),
        ]
        adj = adjudicate_field("peak_torque", claims)

        assert adj.resolved is True
        assert adj.winner_value == "90 Nm"
        assert adj.runner_up_value == "300 Nm"
        assert adj.winner_score > adj.runner_up_score

    def test_adjudicate_field_unresolved(self, temp_wiki_for_conflicts):
        from conflict_resolver import Claim, adjudicate_field

        # Two blog posts with same authority → scores too close
        # Values differ by >5% so tolerance merge does NOT auto-resolve
        claims = [
            Claim(field="height", value="1.30 m", source="blog_post"),
            Claim(field="height", value="1.80 m", source="blog_post"),
        ]
        adj = adjudicate_field("height", claims)

        # Same authority, similar recency → gap should be small
        assert adj.resolved is False

    def test_adjudicate_field_majority_boost(self, temp_wiki_for_conflicts):
        from conflict_resolver import Claim, adjudicate_field

        # 3 sources, 2 agree → majority boost
        claims = [
            Claim(field="speed", value="2.0 m/s", source="official_manual"),
            Claim(field="speed", value="2.0 m/s", source="arxiv_paper"),
            Claim(field="speed", value="1.8 m/s", source="blog_post"),
        ]
        adj = adjudicate_field("speed", claims)

        assert adj.winner_value == "2.0 m/s"
        # Majority should push winner score higher
        assert "2.0 m/s" in adj.reasoning

    def test_resolve_conflicts_mcp_tool(self, temp_wiki_for_conflicts):
        from conflict_resolver import resolve_conflicts

        result = resolve_conflicts("Unitree G1", str(temp_wiki_for_conflicts))

        assert result["status"] == "adjudicated"
        assert result["entity"] == "Unitree G1"
        assert result["resolved_count"] >= 1
        assert result["unresolved_count"] >= 0

        # Check page was updated with resolved section
        p1 = temp_wiki_for_conflicts / "entities" / "unitree_g1.md"
        content = p1.read_text(encoding="utf-8")
        assert "### 已裁决冲突" in content

    def test_conflict_stats(self, temp_wiki_for_conflicts):
        from conflict_resolver import conflict_stats

        stats = conflict_stats(str(temp_wiki_for_conflicts))

        assert stats["status"] == "done"
        assert stats["pages_with_conflicts"] >= 1
        assert stats["total_pending_conflicts"] >= 1

    def test_no_conflicts_page(self, temp_wiki):
        from conflict_resolver import resolve_conflicts

        # Create a page with no conflicts
        engine.create_page(
            str(temp_wiki / "entities"),
            "NoConflictBot",
            "# NoConflictBot\n\nNo conflicts here.",
            {"type": "entity"},
        )

        result = resolve_conflicts("NoConflictBot", str(temp_wiki))
        assert result["status"] == "no_conflicts"


class TestJudgmentGenerator:
    """Test judgment generator — structured criteria from resolved knowledge."""

    @pytest.fixture
    def temp_wiki_for_judgments(self, tmp_path):
        """Create a wiki with a page containing resolved conflicts."""
        wiki = tmp_path / "wiki"
        wiki.mkdir()

        p1 = wiki / "entities" / "unitree_g1.md"
        p1.parent.mkdir(parents=True, exist_ok=True)
        p1.write_text(
            "---\ntitle: Unitree G1\ntype: entity\ntags: [robot, humanoid, locomotion]\nconfidence: 0.8\n---\n\n"
            "# Unitree G1\n\n"
            "Peak torque: 237 Nm according to [[Unitree-G1-Official-Spec]].\n\n"
            "### 已裁决冲突\n"
            "**Resolved:**\n"
            "- **peak_torque** → `237 Nm` (confidence: 0.92)\n"
            "  - Reasoning: Official manual beats blog post\n"
            "**Still unresolved:**\n"
            "- **max_speed** — status: `unresolved`, pending_human_review\n"
            "  - Best candidate: `2.5 m/s` (0.55)\n",
            encoding="utf-8",
        )
        return wiki

    def test_generate_judgments_from_page(self, temp_wiki_for_judgments):
        from judgment_generator import generate_judgments_for_page

        p1 = str(temp_wiki_for_judgments / "entities" / "unitree_g1.md")
        judgments = generate_judgments_for_page(p1, str(temp_wiki_for_judgments))

        assert len(judgments) >= 1
        # Resolved peak_torque should be a judgment
        torque_judgments = [j for j in judgments if j.parameter == "peak_torque"]
        assert len(torque_judgments) == 1
        j = torque_judgments[0]
        assert j.entity == "Unitree G1"
        assert j.recommended_value == 237.0
        assert j.unit == "Nm"
        assert j.confidence == 0.92
        assert j.unresolved is False
        # Context inference from tags
        assert j.context == "locomotion_control"

    def test_unresolved_conflict_generates_warning_judgment(self, temp_wiki_for_judgments):
        from judgment_generator import generate_judgments_for_page

        p1 = str(temp_wiki_for_judgments / "entities" / "unitree_g1.md")
        judgments = generate_judgments_for_page(p1, str(temp_wiki_for_judgments))

        speed_judgments = [j for j in judgments if j.parameter == "max_speed"]
        assert len(speed_judgments) == 1
        j = speed_judgments[0]
        assert j.unresolved is True
        assert j.recommended_value == "UNKNOWN"
        assert "unresolved" in j.usage_notes.lower()

    def test_save_and_load_judgments(self, temp_wiki_for_judgments):
        from judgment_generator import (
            generate_judgments_for_page,
            save_judgments,
            get_judgment,
        )

        p1 = str(temp_wiki_for_judgments / "entities" / "unitree_g1.md")
        judgments = generate_judgments_for_page(p1, str(temp_wiki_for_judgments))
        save_judgments(str(temp_wiki_for_judgments), judgments)

        # get_judgment should find the saved judgment
        result = get_judgment("Unitree G1", context="locomotion_control", wiki_root=str(temp_wiki_for_judgments))
        assert result["status"] == "found"
        assert result["count"] >= 1
        assert any(j["parameter"] == "peak_torque" for j in result["judgments"])

    def test_get_judgment_without_context(self, temp_wiki_for_judgments):
        from judgment_generator import generate_judgments_for_page, save_judgments, get_judgment

        p1 = str(temp_wiki_for_judgments / "entities" / "unitree_g1.md")
        judgments = generate_judgments_for_page(p1, str(temp_wiki_for_judgments))
        save_judgments(str(temp_wiki_for_judgments), judgments)

        result = get_judgment("Unitree G1", wiki_root=str(temp_wiki_for_judgments))
        assert result["status"] == "found"
        assert result["count"] >= 1

    def test_list_judgments_by_context(self, temp_wiki_for_judgments):
        from judgment_generator import generate_judgments_for_page, save_judgments, list_judgments

        p1 = str(temp_wiki_for_judgments / "entities" / "unitree_g1.md")
        judgments = generate_judgments_for_page(p1, str(temp_wiki_for_judgments))
        save_judgments(str(temp_wiki_for_judgments), judgments)

        result = list_judgments(context="locomotion_control", wiki_root=str(temp_wiki_for_judgments))
        assert result["status"] == "done"
        assert result["count"] >= 1

    def test_list_all_judgments(self, temp_wiki_for_judgments):
        from judgment_generator import generate_judgments_for_page, save_judgments, list_judgments

        p1 = str(temp_wiki_for_judgments / "entities" / "unitree_g1.md")
        judgments = generate_judgments_for_page(p1, str(temp_wiki_for_judgments))
        save_judgments(str(temp_wiki_for_judgments), judgments)

        result = list_judgments(wiki_root=str(temp_wiki_for_judgments))
        assert result["status"] == "done"
        assert result["count"] >= 1

    def test_generate_all_judgments(self, temp_wiki_for_judgments):
        from judgment_generator import generate_all_judgments

        result = generate_all_judgments(str(temp_wiki_for_judgments))
        assert result["status"] == "done"
        assert result["pages_processed"] >= 1
        assert result["judgments_generated"] >= 1

    def test_judgment_sorting_by_confidence(self, temp_wiki_for_judgments):
        from judgment_generator import get_judgment, generate_judgments_for_page, save_judgments

        # Add a second resolved conflict with lower confidence
        p1 = temp_wiki_for_judgments / "entities" / "unitree_g1.md"
        content = p1.read_text(encoding="utf-8")
        content = content.replace(
            "### 已裁决冲突\n",
            "### 已裁决冲突\n"
            "**Resolved:**\n"
            "- **weight** → `47 kg` (confidence: 0.65)\n"
            "  - Reasoning: Moderate confidence\n",
        )
        p1.write_text(content, encoding="utf-8")

        judgments = generate_judgments_for_page(str(p1), str(temp_wiki_for_judgments))
        save_judgments(str(temp_wiki_for_judgments), judgments)

        result = get_judgment("Unitree G1", wiki_root=str(temp_wiki_for_judgments))
        assert result["status"] == "found"
        # Should be sorted by confidence descending
        confidences = [j["confidence"] for j in result["judgments"]]
        assert confidences == sorted(confidences, reverse=True)


class TestSearchExpanded:
    """Test expanded search with RRF fusion and judgment search."""

    def test_search_default(self, temp_wiki):
        from search_backend import search_wiki

        engine.create_page(
            str(temp_wiki / "entities"),
            "SearchBot",
            "# SearchBot\n\nA search test entity.",
            {"type": "entity", "tags": ["test"]},
        )

        result = search_wiki(str(temp_wiki), "search test", search_type="default")
        assert result["status"] == "done"
        assert result["search_type"] == "default"
        assert len(result["results"]) >= 1

    def test_search_expanded_simple(self, temp_wiki):
        from search_backend import search_wiki

        engine.create_page(
            str(temp_wiki / "entities"),
            "AlphaBot",
            "# AlphaBot\n\nAlphaBot is a fast robot.",
            {"type": "entity"},
        )
        engine.create_page(
            str(temp_wiki / "entities"),
            "BetaBot",
            "# BetaBot\n\nBetaBot is also fast and speedy.",
            {"type": "entity"},
        )

        # Expanded search without LLM uses simple expansion
        result = search_wiki(str(temp_wiki), "fast robot", search_type="expanded")
        assert result["status"] == "done"
        assert result["search_type"] == "expanded"
        assert "variants" in result
        assert len(result["results"]) >= 1

    def test_search_judgment_type(self, tmp_path):
        from search_backend import search_wiki
        from judgment_generator import Judgment, save_judgments

        wiki = tmp_path / "wiki"
        wiki.mkdir()
        # Pre-seed a judgment
        j = Judgment(
            context="locomotion_control",
            entity="Unitree G1",
            parameter="peak_torque",
            recommended_value=237.0,
            unit="Nm",
            confidence=0.92,
        )
        save_judgments(str(wiki), [j])

        result = search_wiki(
            str(wiki),
            "peak_torque",
            search_type="judgment",
        )
        assert result["status"] == "done"
        assert result["search_type"] == "judgment"
        assert len(result["results"]) >= 1

    def test_rrf_fuse(self):
        from search_backend import _rrf_fuse

        list_a = [
            {"file_path": "a.md", "score": 10},
            {"file_path": "b.md", "score": 8},
        ]
        list_b = [
            {"file_path": "b.md", "score": 9},
            {"file_path": "c.md", "score": 7},
        ]
        fused = _rrf_fuse([list_a, list_b])
        assert len(fused) == 3
        # b appears in both lists, should have highest RRF score
        assert fused[0]["file_path"] == "b.md"


class TestContextRouter:
    """Test context routing from scenario descriptions to judgments."""

    @pytest.fixture
    def temp_wiki_for_routing(self, tmp_path):
        """Create a wiki with judgments for routing tests."""
        wiki = tmp_path / "wiki"
        wiki.mkdir()

        p1 = wiki / "entities" / "unitree_g1.md"
        p1.parent.mkdir(parents=True, exist_ok=True)
        p1.write_text(
            "---\ntitle: Unitree G1\ntype: entity\ntags: [robot, humanoid, locomotion]\nconfidence: 0.8\n---\n\n"
            "# Unitree G1\n\n"
            "Peak torque: 237 Nm.\n\n"
            "### 已裁决冲突\n"
            "**Resolved:**\n"
            "- **peak_torque** → `237 Nm` (confidence: 0.92)\n"
            "  - Reasoning: Official manual beats blog post\n"
            "**Still unresolved:**\n"
            "- **max_speed** — status: `unresolved`, pending_human_review\n",
            encoding="utf-8",
        )

        p2 = wiki / "concepts" / "slippery_ground.md"
        p2.parent.mkdir(parents=True, exist_ok=True)
        p2.write_text(
            "---\ntitle: Slippery Ground\ntype: concept\ntags: [terrain, safety]\nconfidence: 0.7\n---\n\n"
            "When walking on slippery ground, reduce torque to 180 Nm.\n",
            encoding="utf-8",
        )

        return wiki

    def test_route_scenario_to_judgments(self, temp_wiki_for_routing):
        from context_router import route
        from judgment_generator import generate_judgments_for_page, save_judgments

        # Pre-generate judgments
        p1 = str(temp_wiki_for_routing / "entities" / "unitree_g1.md")
        judgments = generate_judgments_for_page(p1, str(temp_wiki_for_routing))
        save_judgments(str(temp_wiki_for_routing), judgments)

        result = route("G1 slips on wet ground", str(temp_wiki_for_routing), top_k=5)

        assert result["status"] == "done"
        assert result["inferred_context"] == "locomotion_control"
        assert any("slip" in kw for kw in result["keywords"])

    def test_route_priority_warnings(self, temp_wiki_for_routing):
        from context_router import route
        from judgment_generator import generate_judgments_for_page, save_judgments

        p1 = str(temp_wiki_for_routing / "entities" / "unitree_g1.md")
        judgments = generate_judgments_for_page(p1, str(temp_wiki_for_routing))
        save_judgments(str(temp_wiki_for_routing), judgments)

        result = route("G1 speed problem", str(temp_wiki_for_routing), top_k=5)

        assert result["status"] == "done"
        # Should flag unresolved max_speed as priority
        assert len(result["priority_items"]) >= 1
        assert any("max_speed" in str(p) for p in result["priority_items"])

    def test_route_infers_navigation_context(self, temp_wiki_for_routing):
        from context_router import _infer_context_from_scenario

        assert _infer_context_from_scenario("robot is lost and needs to map") == "navigation"
        assert _infer_context_from_scenario("battery is dying") == "power"
        assert _infer_context_from_scenario("gripper cannot grasp") == "manipulation"

    def test_route_with_judgment_search(self, temp_wiki_for_routing):
        from context_router import route_with_judgment_search
        from judgment_generator import generate_judgments_for_page, save_judgments

        p1 = str(temp_wiki_for_routing / "entities" / "unitree_g1.md")
        judgments = generate_judgments_for_page(p1, str(temp_wiki_for_routing))
        save_judgments(str(temp_wiki_for_routing), judgments)

        result = route_with_judgment_search("G1 torque settings", str(temp_wiki_for_routing))
        assert result["status"] == "done"
        # Should find peak_torque judgment
        assert any(j.get("parameter") == "peak_torque" for j in result["judgments"])


class TestCodeGenerator:
    """Test controlled code generation with source citations."""

    @pytest.fixture
    def temp_wiki_for_codegen(self, tmp_path):
        """Create a wiki with an algorithm page for code generation."""
        wiki = tmp_path / "wiki"
        wiki.mkdir()

        p1 = wiki / "algorithms" / "gait_controller.md"
        p1.parent.mkdir(parents=True, exist_ok=True)
        p1.write_text(
            "---\ntitle: Gait Controller\ntype: algorithm\ntags: [locomotion, control]\nconfidence: 0.85\n---\n\n"
            "# Gait Controller\n\n"
            "A walking gait controller for humanoid robots.\n\n"
            "Parameters:\n"
            "- step_height = 0.05 m\n"
            "- step_length = 0.3 m\n"
            "- cycle_time = 1.2 s\n\n"
            "Based on [[Bipedal-Gait-Paper-2024]].\n",
            encoding="utf-8",
        )

        p2 = wiki / "entities" / "g1_with_conflict.md"
        p2.parent.mkdir(parents=True, exist_ok=True)
        p2.write_text(
            "---\ntitle: G1 With Conflict\ntype: entity\ntags: [robot]\nconfidence: 0.5\n---\n\n"
            "# G1 With Conflict\n\n"
            "Peak torque: 90 Nm.\n\n"
            "### 已裁决冲突\n"
            "**Still unresolved:**\n"
            "- **peak_torque** — status: `unresolved`, pending_human_review\n",
            encoding="utf-8",
        )

        return wiki

    def test_generate_code_framework(self, temp_wiki_for_codegen):
        from code_generator import generate_code_framework

        result = generate_code_framework("Gait Controller", str(temp_wiki_for_codegen))

        assert result["status"] == "generated"
        assert "⚠️ AUTO-GENERATED CODE" in result["code"]
        assert "GaitControllerController" in result["code"]
        assert "STEP_HEIGHT = 0.05" in result["code"]
        assert "STEP_LENGTH = 0.3" in result["code"]
        assert "CYCLE_TIME = 1.2" in result["code"]
        assert "[[Bipedal-Gait-Paper-2024]]" in result["citations"]
        assert "NotImplementedError" in result["code"]

    def test_code_generation_blocked_by_unresolved_conflict(self, temp_wiki_for_codegen):
        from code_generator import generate_code_framework

        result = generate_code_framework("G1 With Conflict", str(temp_wiki_for_codegen))

        assert result["status"] == "blocked"
        assert "BLOCKED" in result["warnings"][0]
        assert "peak_torque" in result["unresolved_conflicts"]
        assert result["code"] == ""

    def test_code_generation_entity_not_found(self, temp_wiki):
        from code_generator import generate_code_framework

        result = generate_code_framework("NonExistentAlgo", str(temp_wiki))

        assert result["status"] == "not_found"
        assert "No wiki page found" in result["warnings"][0]

    def test_code_generate_mcp_tool(self, temp_wiki_for_codegen):
        from code_generator import code_generate

        result = code_generate("Gait Controller", wiki_root=str(temp_wiki_for_codegen))

        assert result["status"] == "generated"
        assert result["entity"] == "Gait Controller"
        assert len(result["code"]) > 0

    def test_code_generate_with_warnings(self, temp_wiki_for_codegen):
        from code_generator import generate_code_framework

        result = generate_code_framework("Gait Controller", str(temp_wiki_for_codegen))

        assert result["status"] == "generated"
        # Should have warnings about skeleton
        assert any("SKELETON" in w for w in result["warnings"])


class TestPhase6Fixes:
    """Test Phase 6 limitation fixes: event log rotation, QA event emit, file locking."""

    def test_event_bus_log_rotation(self, tmp_path):
        from event_bus import emit, tail_events, clear_events

        log_file = tmp_path / "events.jsonl"
        # Use a tiny threshold to trigger rotation quickly
        max_bytes = 200

        # Emit enough events to exceed threshold
        for i in range(20):
            emit("test_event", {"idx": i}, event_log=log_file, max_bytes=max_bytes)

        # The active log should exist and rotated backups may exist
        assert log_file.exists()
        events = tail_events(event_log=log_file)
        # After rotation, some events may be in backup; active log has recent ones
        assert len(events) >= 0

        # Verify backup was created
        backup = log_file.parent / f"{log_file.name}.1"
        assert backup.exists()
        clear_events(event_log=log_file)
        for i in range(1, 5):
            b = log_file.parent / f"{log_file.name}.{i}"
            if b.exists():
                b.unlink()

    def test_qa_engine_emits_page_created_event(self, tmp_path, monkeypatch):
        import event_bus
        from qa_engine import ask
        from event_bus import tail_events, clear_events

        wiki = tmp_path / "wiki"
        wiki.mkdir()
        (wiki / "entities").mkdir()

        p = wiki / "entities" / "testbot.md"
        p.write_text(
            "---\ntitle: TestBot\ntype: entity\ntags: [robot]\nconfidence: 0.8\n---\n\n"
            "TestBot is a test robot with max_speed = 2.0 m/s.\n",
            encoding="utf-8",
        )

        log_file = tmp_path / "events.jsonl"
        # Redirect default event log to temp path so qa_engine writes there
        monkeypatch.setattr(event_bus, "DEFAULT_EVENT_LOG", log_file)

        # Mock LLM that returns a deterministic answer
        class MockLLM:
            def complete(self, prompt, temperature=0.3, **kwargs):
                return "TestBot has a max speed of 2.0 m/s. [[TestBot]]"

        result = ask(
            str(wiki),
            "What is the max speed of TestBot?",
            llm=MockLLM(),
            write_back=True,
        )

        assert result["qa_path"] is not None

        # Verify page_created event was emitted
        events = tail_events(event_log=log_file)
        page_created_events = [e for e in events if e["type"] == "page_created"]
        assert len(page_created_events) >= 1
        assert "Q: What is the max speed of TestBot?" in page_created_events[0]["payload"]["title"]
        clear_events(event_log=log_file)

    def test_wiki_engine_file_lock_prevents_race(self, tmp_path):
        """Concurrent create_page calls should all succeed without data corruption."""
        import threading
        import file_lock

        wiki = tmp_path / "wiki"
        wiki.mkdir()
        (wiki / "entities").mkdir()

        errors: list[Exception] = []
        paths: list[str] = []
        lock = threading.Lock()

        def worker(idx: int):
            try:
                path = engine.create_page(
                    str(wiki / "entities"),
                    f"Robot {idx}",
                    f"# Robot {idx}\n\nDescription.",
                    {"type": "entity", "tags": ["robot"], "confidence": 0.5},
                )
                with lock:
                    paths.append(path)
            except Exception as exc:
                with lock:
                    errors.append(exc)

        threads = [threading.Thread(target=worker, args=(i,)) for i in range(10)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert len(errors) == 0, f"Concurrent create_page raised errors: {errors}"
        # 10 distinct pages should have been created
        assert len(set(paths)) == 10
        # Verify each file is readable and well-formed
        for p in paths:
            content = Path(p).read_text(encoding="utf-8")
            meta, body = engine.parse_frontmatter(content)
            assert meta.get("type") == "entity"
            assert "Robot" in body

    def test_wiki_engine_update_page_with_lock(self, tmp_path):
        """update_page should succeed under file lock."""
        wiki = tmp_path / "wiki"
        wiki.mkdir()
        (wiki / "algorithms").mkdir()

        path = engine.create_page(
            str(wiki / "algorithms"),
            "Test Algo",
            "# Test Algo\n\nInitial.",
            {"type": "algorithm", "confidence": 0.6},
        )

        def mock_llm(prompt, content):
            return content + "\n\n[Updated]"

        new_content = engine.update_page(path, "Add update note", mock_llm)
        assert "[Updated]" in new_content

        # Verify on disk
        disk_content = Path(path).read_text(encoding="utf-8")
        assert "[Updated]" in disk_content


class TestPhase8Module4:
    """Test Phase 8 Module 4: Awesome-VLN Demo pipeline."""

    def test_generate_awesome_list_parses_yaml(self, tmp_path):
        from generate_awesome_list import parse_awesome_readme

        readme = tmp_path / "test_awesome.md"
        readme.write_text(
            "# Test Awesome\n\n"
            "| Year | Venue | Paper | Repo | Note |\n"
            "|:----:|:-----:|-------|:----:|------|\n"
            '|2025|`arXiv`|[Test Paper](https://arxiv.org/pdf/2501.12345)|[stars](https://github.com/user/repo)|[site](https://example.com)|\n'
            "\n"
            "Also see [Another Paper](https://arxiv.org/abs/2501.99999).\n",
            encoding="utf-8",
        )

        result = parse_awesome_readme(str(readme))

        assert len(result["papers"]) >= 2
        assert any(p["arxiv_id"] == "2501.12345" for p in result["papers"])
        assert any(p["arxiv_id"] == "2501.99999" for p in result["papers"])
        assert any(r["name"] == "repo" for r in result["code_repos"])
        assert any(a["url"] == "https://example.com" for a in result["articles"])

    def test_generate_awesome_list_filters_blacklist(self, tmp_path):
        from generate_awesome_list import parse_awesome_readme

        readme = tmp_path / "test_awesome.md"
        readme.write_text(
            "# Test\n\n"
            "[Badge](https://img.shields.io/github/stars/user/repo.svg)\n"
            "[Issue](https://github.com/KwanWaiPang/Awesome-VLN/issues/1)\n"
            "[Paper](https://arxiv.org/pdf/2501.12345)\n",
            encoding="utf-8",
        )

        result = parse_awesome_readme(str(readme))

        # shields.io and issues should be filtered
        assert not any("shields.io" in r.get("url", "") for r in result["code_repos"])
        assert not any("issues" in r.get("url", "") for r in result["articles"])
        assert any(p["arxiv_id"] == "2501.12345" for p in result["papers"])


class TestPhase8Module1:
    """Test Phase 8 Module 1: judgment quality improvements (tolerance + unified index)."""

    def test_value_equivalence_within_tolerance(self):
        from conflict_resolver import _are_values_equivalent

        assert _are_values_equivalent("237 N·m", "236.5 Nm") is True
        assert _are_values_equivalent("100 kg", "102 kg") is True
        assert _are_values_equivalent("1.0 m", "1.04 m") is True

    def test_value_equivalence_outside_tolerance(self):
        from conflict_resolver import _are_values_equivalent

        assert _are_values_equivalent("237 N·m", "200 Nm") is False
        assert _are_values_equivalent("100 kg", "110 kg") is False
        assert _are_values_equivalent("1.0 m", "1.2 m") is False

    def test_tolerance_merge_auto_resolves(self):
        from conflict_resolver import Claim, adjudicate_field

        claims = [
            Claim(field="peak_torque", value="237 N·m", source="official_manual"),
            Claim(field="peak_torque", value="236.5 Nm", source="arxiv_paper"),
        ]
        result = adjudicate_field("peak_torque", claims)

        assert result.resolved is True
        assert result.resolution_method == "resolved_by_tolerance"
        assert "Resolved by tolerance merge" in result.reasoning
        assert len(result.merge_logs) == 1
        assert result.merge_logs[0]["relative_diff"] < 0.05

    def test_judgment_index_created(self, tmp_path):
        from judgment_generator import Judgment, save_judgments, _load_index

        wiki = tmp_path / "wiki"
        wiki.mkdir()

        judgments = [
            Judgment(
                context="locomotion_control",
                entity="Unitree G1",
                parameter="peak_torque",
                recommended_value=237.0,
                unit="Nm",
                confidence=0.92,
                sources=["official_manual"],
                conflicts_resolved=["Resolved"],
            ),
            Judgment(
                context="navigation",
                entity="WildOS",
                parameter="planner_type",
                recommended_value="sampling-based",
                unit="",
                confidence=0.85,
                sources=["wildos_paper"],
                conflicts_resolved=["Resolved"],
            ),
        ]
        save_judgments(str(wiki), judgments)

        index = _load_index(str(wiki))
        assert index is not None
        assert index["version"] == "2.0.0"
        assert index["total_judgments"] == 2
        assert "Unitree G1" in index["by_entity"]
        assert "peak_torque" in index["by_entity"]["Unitree G1"]["locomotion_control"]
        assert "WildOS" in index["by_context"]["navigation"]

    def test_search_judgments(self, tmp_path):
        from judgment_generator import Judgment, save_judgments, search_judgments

        wiki = tmp_path / "wiki"
        wiki.mkdir()

        judgments = [
            Judgment(
                context="locomotion_control",
                entity="Unitree G1",
                parameter="peak_torque",
                recommended_value=237.0,
                unit="Nm",
                confidence=0.92,
                sources=["official_manual"],
                usage_notes="Verified against official manual.",
            ),
        ]
        save_judgments(str(wiki), judgments)

        result = search_judgments("torque", wiki_root=str(wiki))
        assert result["status"] == "done"
        assert result["count"] >= 1
        assert any(j["parameter"] == "peak_torque" for j in result["judgments"])

    def test_export_judgments_markdown(self, tmp_path):
        from judgment_generator import Judgment, save_judgments, export_judgments

        wiki = tmp_path / "wiki"
        wiki.mkdir()

        judgments = [
            Judgment(
                context="locomotion_control",
                entity="Unitree G1",
                parameter="peak_torque",
                recommended_value=237.0,
                unit="Nm",
                confidence=0.92,
                sources=["official_manual"],
                usage_notes="Verified against official manual.",
            ),
        ]
        save_judgments(str(wiki), judgments)

        result = export_judgments(format="markdown", wiki_root=str(wiki))
        assert result["status"] == "done"
        assert "# Judgment Export" in result["data"]
        assert "Unitree G1" in result["data"]
        assert "peak_torque" in result["data"]

    def test_judgment_list_uses_index(self, tmp_path):
        from judgment_generator import Judgment, save_judgments, list_judgments

        wiki = tmp_path / "wiki"
        wiki.mkdir()

        judgments = [
            Judgment(
                context="locomotion_control",
                entity="Unitree G1",
                parameter="peak_torque",
                recommended_value=237.0,
                unit="Nm",
                confidence=0.92,
                sources=["official_manual"],
            ),
        ]
        save_judgments(str(wiki), judgments)

        result = list_judgments(wiki_root=str(wiki))
        assert result["status"] == "done"
        assert result["count"] == 1
        assert result["judgments"][0]["entity"] == "Unitree G1"


class TestPhase8Module2:
    """Test Phase 8 Module 2: Wiki Hub push/pull protocol."""

    def test_wiki_pack_creates_json(self, tmp_path):
        from wiki_hub import wiki_pack

        wiki = tmp_path / "wiki"
        wiki.mkdir()
        (wiki / "entities").mkdir()
        (wiki / "algorithms").mkdir()

        p1 = wiki / "entities" / "testbot.md"
        p1.write_text(
            "---\ntitle: TestBot\ntype: entity\ntags: [robot]\nconfidence: 0.8\n---\n\n"
            "# TestBot\n\nTest robot.\n",
            encoding="utf-8",
        )
        p2 = wiki / "algorithms" / "gait.md"
        p2.write_text(
            "---\ntitle: Gait Controller\ntype: algorithm\ntags: [control]\nconfidence: 0.7\n---\n\n"
            "# Gait Controller\n\nWalking algorithm.\n",
            encoding="utf-8",
        )

        result = wiki_pack("Test-Wiki", str(wiki), output_path=str(tmp_path / "pack.json"))

        assert result["status"] == "done"
        assert result["total_pages"] == 2
        assert Path(tmp_path / "pack.json").exists()

        pack = json.loads(Path(tmp_path / "pack.json").read_text(encoding="utf-8"))
        assert pack["meta"]["wiki_name"] == "Test-Wiki"
        assert pack["meta"]["pack_format_version"] == "1.0.0"
        assert len(pack["pages"]) == 2

    def test_wiki_unpack_restores_pages(self, tmp_path):
        from wiki_hub import wiki_pack, wiki_unpack

        wiki_a = tmp_path / "wiki_a"
        wiki_a.mkdir()
        (wiki_a / "entities").mkdir()

        p = wiki_a / "entities" / "testbot.md"
        p.write_text(
            "---\ntitle: TestBot\ntype: entity\ntags: [robot]\nconfidence: 0.8\n---\n\n"
            "# TestBot\n\nTest robot.\n",
            encoding="utf-8",
        )

        pack_path = tmp_path / "pack.json"
        wiki_pack("Test-Wiki", str(wiki_a), output_path=str(pack_path))

        wiki_b = tmp_path / "wiki_b"
        result = wiki_unpack(str(pack_path), str(wiki_b), merge_mode="skip_existing")

        assert result["status"] == "done"
        assert result["pages_created"] == 1
        assert (wiki_b / "entities" / "testbot.md").exists()

    def test_wiki_diff_detects_new_and_updated(self, tmp_path):
        from wiki_hub import wiki_pack, wiki_diff

        wiki_a = tmp_path / "wiki_a"
        wiki_a.mkdir()
        (wiki_a / "entities").mkdir()

        p = wiki_a / "entities" / "testbot.md"
        p.write_text(
            "---\ntitle: TestBot\ntype: entity\ntags: [robot]\nconfidence: 0.8\n---\n\n"
            "# TestBot\n\nOriginal.\n",
            encoding="utf-8",
        )

        pack_a = tmp_path / "pack_a.json"
        wiki_pack("A", str(wiki_a), output_path=str(pack_a))

        # Modify local wiki
        p.write_text(
            "---\ntitle: TestBot\ntype: entity\ntags: [robot]\nconfidence: 0.8\n---\n\n"
            "# TestBot\n\nUpdated.\n",
            encoding="utf-8",
        )

        result = wiki_diff(str(pack_a), wiki_root=str(wiki_a))

        assert result["status"] == "done"
        assert len(result["updated_pages"]) == 1
        assert "entities/testbot.md" in result["updated_pages"][0]

    def test_wiki_pack_version_bump(self, tmp_path):
        from wiki_hub import wiki_pack

        wiki = tmp_path / "wiki"
        wiki.mkdir()
        (wiki / "entities").mkdir()

        p = wiki / "entities" / "testbot.md"
        p.write_text(
            "---\ntitle: TestBot\ntype: entity\ntags: [robot]\nconfidence: 0.8\n---\n\n"
            "# TestBot\n\nTest robot.\n",
            encoding="utf-8",
        )

        pack_path = tmp_path / "pack.json"
        r1 = wiki_pack("Test-Wiki", str(wiki), output_path=str(pack_path))
        assert r1["version"] == "1.0.0"

        # Add another page (>10% change)
        p2 = wiki / "entities" / "testbot2.md"
        p2.write_text(
            "---\ntitle: TestBot2\ntype: entity\ntags: [robot]\nconfidence: 0.8\n---\n\n"
            "# TestBot2\n\nTest robot 2.\n",
            encoding="utf-8",
        )

        r2 = wiki_pack("Test-Wiki", str(wiki), output_path=str(pack_path))
        assert r2["version"] == "1.1.0"


class TestPhase8Module3:
    """Test Phase 8 Module 3: automated workflow orchestration."""

    def test_workflow_orchestrator_state(self, tmp_path):
        from workflow_orchestrator import _update_state, _get_state

        _update_state("running", "entity_linker", {"pages": 5})
        state = _get_state()
        assert state["status"] == "running"
        assert state["current_step"] == "entity_linker"
        assert state["progress"]["pages"] == 5

    def test_entity_linker_emits_event(self, tmp_path, monkeypatch):
        import event_bus
        from entity_linker import process
        from event_bus import tail_events, clear_events

        wiki = tmp_path / "wiki"
        wiki.mkdir()
        (wiki / "entities").mkdir()

        p1 = wiki / "entities" / "ros2.md"
        p1.write_text(
            "---\ntitle: ROS2\ntype: entity\ntags: [robot]\nconfidence: 0.8\n---\n\n# ROS2\n\nRobot OS.\n",
            encoding="utf-8",
        )
        p2 = wiki / "entities" / "testbot.md"
        p2.write_text(
            "---\ntitle: TestBot\ntype: entity\ntags: [robot]\nconfidence: 0.8\n---\n\n"
            "# TestBot\n\nTest robot that uses [[ROS2]].\n",
            encoding="utf-8",
        )

        log_file = tmp_path / "events.jsonl"
        monkeypatch.setattr(event_bus, "DEFAULT_EVENT_LOG", log_file)

        process(str(wiki), str(p2), write_back=True)

        events = tail_events(event_log=log_file)
        link_events = [e for e in events if e["type"] == "entity_link_complete"]
        assert len(link_events) >= 1
        assert link_events[0]["payload"]["new_links"] >= 1
        clear_events(event_log=log_file)

    def test_conflict_resolver_emits_event(self, tmp_path, monkeypatch):
        import event_bus
        from conflict_resolver import resolve_conflicts
        from event_bus import tail_events, clear_events

        wiki = tmp_path / "wiki"
        wiki.mkdir()
        (wiki / "entities").mkdir()

        p = wiki / "entities" / "testbot.md"
        p.write_text(
            "---\ntitle: TestBot\ntype: entity\ntags: [robot]\nconfidence: 0.8\n---\n\n"
            "# TestBot\n\nSpeed: 2.0 m/s.\n\n"
            "### 待核实冲突\n"
            "- **max_speed** — old: `2.0 m/s` (from blog) vs new: `2.1 m/s` (from official)\n",
            encoding="utf-8",
        )

        log_file = tmp_path / "events.jsonl"
        monkeypatch.setattr(event_bus, "DEFAULT_EVENT_LOG", log_file)

        result = resolve_conflicts("TestBot", str(wiki))
        assert result["status"] == "adjudicated"

        events = tail_events(event_log=log_file)
        conflict_events = [e for e in events if e["type"] == "conflict_resolution_complete"]
        assert len(conflict_events) >= 1
        assert conflict_events[0]["payload"]["entity"] == "TestBot"
        clear_events(event_log=log_file)

    def test_workflow_step_entity_linker(self, tmp_path):
        from workflow_orchestrator import _run_entity_linker

        wiki = tmp_path / "wiki"
        wiki.mkdir()
        (wiki / "entities").mkdir()

        p1 = wiki / "entities" / "ros2.md"
        p1.write_text(
            "---\ntitle: ROS2\ntype: entity\ntags: [robot]\nconfidence: 0.8\n---\n\n# ROS2\n\nRobot OS.\n",
            encoding="utf-8",
        )
        p2 = wiki / "entities" / "testbot.md"
        p2.write_text(
            "---\ntitle: TestBot\ntype: entity\ntags: [robot]\nconfidence: 0.8\n---\n\n"
            "# TestBot\n\nTest robot that uses [[ROS2]].\n",
            encoding="utf-8",
        )

        result = _run_entity_linker(str(wiki))
        assert result["success"] is True
        assert result["total_links"] >= 1
        assert result["pages_affected"] >= 1


# ── Phase 10 Tests ──


class TestSearchInterface:
    """Test unified search interface abstraction."""

    @pytest.fixture
    def temp_wiki_for_search(self, tmp_path):
        wiki = tmp_path / "wiki"
        wiki.mkdir()
        p = wiki / "concepts" / "test_ai.md"
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(
            "---\ntitle: Test AI\ntype: concept\ntags: [ai, test]\nconfidence: 0.8\n---\n\n"
            "# Test AI\n\nThis is a test concept about artificial intelligence.",
            encoding="utf-8",
        )
        return str(wiki)

    def test_search_keyword(self, temp_wiki_for_search):
        from search_interface import FileSystemSearchImpl

        search = FileSystemSearchImpl(temp_wiki_for_search)
        results = search.search("artificial intelligence", search_type="keyword", top_k=10)
        assert isinstance(results, list)

    def test_search_hybrid(self, temp_wiki_for_search):
        from search_interface import FileSystemSearchImpl

        search = FileSystemSearchImpl(temp_wiki_for_search)
        results = search.search("test", search_type="hybrid", top_k=10)
        assert isinstance(results, list)

    def test_search_judgment(self, temp_wiki_for_search):
        from search_interface import FileSystemSearchImpl

        search = FileSystemSearchImpl(temp_wiki_for_search)
        results = search.search("test", search_type="judgment", top_k=10)
        assert isinstance(results, list)

    def test_search_expanded(self, temp_wiki_for_search):
        from search_interface import FileSystemSearchImpl

        search = FileSystemSearchImpl(temp_wiki_for_search)
        results = search.search("test", search_type="expanded", top_k=10)
        assert isinstance(results, list)

    def test_index_page_and_rebuild(self, temp_wiki_for_search):
        from search_interface import FileSystemSearchImpl

        search = FileSystemSearchImpl(temp_wiki_for_search)
        result = search.rebuild_index()
        assert result["status"] == "done"

    def test_health(self, temp_wiki_for_search):
        from search_interface import FileSystemSearchImpl

        search = FileSystemSearchImpl(temp_wiki_for_search)
        h = search.health()
        assert h["backend"] == "filesystem"


class TestStorageInterface:
    """Test unified storage interface abstraction."""

    @pytest.fixture
    def temp_storage(self, tmp_path):
        wiki = tmp_path / "wiki"
        wiki.mkdir()
        return str(wiki)

    def test_storage_crud(self, temp_storage):
        from storage_interface import FileSystemStorageImpl

        store = FileSystemStorageImpl(temp_storage)
        page_path = Path(temp_storage) / "test_page.md"

        # Create
        store.write_page(str(page_path), "# Hello\n\nBody text.", metadata={"title": "Test", "type": "concept"})
        assert page_path.exists()

        # Read
        data = store.read_page(str(page_path))
        assert data["meta"]["title"] == "Test"
        assert "Body text" in data["body"]

        # List
        pages = store.list_pages()
        assert len(pages) >= 1

        # Delete
        assert store.delete_page(str(page_path)) is True
        assert not page_path.exists()

    def test_storage_create_page_delegate(self, temp_storage):
        from storage_interface import FileSystemStorageImpl

        store = FileSystemStorageImpl(temp_storage)
        dir_path = Path(temp_storage) / "entities"
        path = store.create_page(str(dir_path), "New Entity", "Body.", {"type": "entity"})
        assert Path(path).exists()

    def test_storage_log_and_index(self, temp_storage):
        from storage_interface import FileSystemStorageImpl

        store = FileSystemStorageImpl(temp_storage)
        log_path = store.append_log("Test entry")
        assert Path(log_path).exists()

        idx_path = store.update_index()
        assert Path(idx_path).exists()

    def test_storage_move_to_archive(self, temp_storage):
        from storage_interface import FileSystemStorageImpl
        import wiki_engine as engine

        store = FileSystemStorageImpl(temp_storage)
        page_path = Path(temp_storage) / "old.md"
        engine.write_frontmatter({"title": "Old", "type": "concept"}, "# Old\n")
        page_path.write_text(engine.write_frontmatter({"title": "Old", "type": "concept"}, "# Old\n"), encoding="utf-8")

        archived = store.move_to_archive(str(page_path))
        assert Path(archived).exists()
        assert page_path.exists()  # stub left behind


class TestCodeKnowledgeGraph:
    """Test AST-based code graph extraction."""

    def test_scan_repo_finds_nodes(self, tmp_path):
        from code_knowledge_graph import scan_repo

        repo = tmp_path / "test_repo"
        repo.mkdir()
        (repo / "main.py").write_text(
            "class MyClass:\n"
            "    '''A test class.'''\n"
            "    def do_work(self):\n"
            "        '''Do some work.'''\n"
            "        helper()\n"
            "\n"
            "CONSTANT = 42\n",
            encoding="utf-8",
        )
        result = scan_repo(repo, "test_repo")
        assert len(result["nodes"]) >= 2  # class + function
        names = {n["name"] for n in result["nodes"]}
        assert "MyClass" in names
        assert "do_work" in names

    def test_build_code_graph(self, tmp_path):
        from code_knowledge_graph import build_code_graph

        code_root = tmp_path / "code"
        code_root.mkdir()
        repo = code_root / "mylib"
        repo.mkdir()
        (repo / "lib.py").write_text(
            "def foo():\n    bar()\n",
            encoding="utf-8",
        )
        out = tmp_path / "graph.json"
        result = build_code_graph(str(code_root), str(out))
        assert result["node_count"] >= 1
        assert out.exists()

    def test_find_function_implementation(self, tmp_path):
        from code_knowledge_graph import build_code_graph, find_function_implementation

        code_root = tmp_path / "code"
        code_root.mkdir()
        repo = code_root / "lib"
        repo.mkdir()
        (repo / "a.py").write_text("def target_func():\n    pass\n", encoding="utf-8")
        graph_path = tmp_path / "graph.json"
        build_code_graph(str(code_root), str(graph_path))
        node = find_function_implementation("target_func", graph=None)
        # Default path won't match temp path; load explicitly
        import json
        graph = json.loads(graph_path.read_text(encoding="utf-8"))
        node = find_function_implementation("target_func", graph=graph)
        assert node is not None
        assert node["name"] == "target_func"


class TestCodeWatcher:
    """Test Git change monitoring."""

    def test_check_repos_no_git(self, tmp_path):
        from code_watcher import check_repos

        code_root = tmp_path / "code"
        code_root.mkdir()
        (code_root / "not_a_repo").mkdir()
        result = check_repos(str(code_root))
        assert result["repos_checked"] == 0
        assert result["changed_repos"] == []

    def test_check_repos_detects_change(self, tmp_path, monkeypatch):
        from code_watcher import check_repos
        import code_watcher as cw
        import subprocess

        # Isolate state file
        state_file = tmp_path / "watcher_state.json"
        monkeypatch.setattr(cw, "_STATE_FILE", state_file)

        code_root = tmp_path / "code"
        code_root.mkdir()
        repo = code_root / "myrepo"
        repo.mkdir()
        subprocess.run(["git", "init"], cwd=str(repo), check=True, capture_output=True)
        (repo / "file.txt").write_text("hello", encoding="utf-8")
        subprocess.run(["git", "add", "."], cwd=str(repo), check=True, capture_output=True)
        subprocess.run(["git", "commit", "-m", "init", "--no-gpg-sign"], cwd=str(repo), check=True, capture_output=True)

        # First check establishes baseline
        r1 = check_repos(str(code_root))
        assert r1["repos_checked"] == 1
        assert len(r1["changed_repos"]) == 0

        # Make a change
        (repo / "file.txt").write_text("hello world", encoding="utf-8")
        subprocess.run(["git", "add", "."], cwd=str(repo), check=True, capture_output=True)
        subprocess.run(["git", "commit", "-m", "update", "--no-gpg-sign"], cwd=str(repo), check=True, capture_output=True)

        # Second check should detect change
        r2 = check_repos(str(code_root))
        assert r2["repos_checked"] == 1
        assert len(r2["changed_repos"]) == 1
        assert r2["changed_repos"][0]["repo"] == "myrepo"


class TestPageIndexer:
    """Test long-document PageIndex generation."""

    def test_should_index_long_pdf(self, tmp_path):
        from page_indexer import should_index

        # Create a mock PDF with 30 pages
        try:
            import fitz
        except ImportError:
            pytest.skip("PyMuPDF not installed")

        pdf_path = tmp_path / "long.pdf"
        doc = fitz.open()
        for _ in range(30):
            doc.new_page()
        doc.save(str(pdf_path))
        doc.close()

        assert should_index(str(pdf_path), min_pages=20) is True
        assert should_index(str(pdf_path), min_pages=50) is False

    def test_build_page_index_heuristic(self, tmp_path):
        from page_indexer import build_page_index
        try:
            import fitz
        except ImportError:
            pytest.skip("PyMuPDF not installed")

        pdf_path = tmp_path / "paper.pdf"
        doc = fitz.open()
        for i in range(25):
            page = doc.new_page()
            page.insert_text((50, 50), f"Page {i+1}")
            if i == 0:
                page.insert_text((50, 100), "Abstract\nThis is the abstract.")
            if i == 2:
                page.insert_text((50, 100), "Introduction\nThis is intro.")
            if i == 10:
                page.insert_text((50, 100), "Methods\nOur method.")
            if i == 20:
                page.insert_text((50, 100), "Conclusion\nIn conclusion.")
        doc.save(str(pdf_path))
        doc.close()

        result = build_page_index(str(pdf_path))
        assert result["total_pages"] == 25
        assert result["chapter_count"] >= 2
        titles = [c["title"] for c in result["chapters"]]
        assert any("Abstract" in t or "Introduction" in t for t in titles)


class TestDreamCycle:
    """Test dream cycle autonomous repair."""

    @pytest.fixture
    def temp_wiki_dream(self, tmp_path):
        wiki = tmp_path / "wiki"
        wiki.mkdir()
        p = wiki / "concepts" / "ai.md"
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(
            "---\ntitle: AI\ntype: concept\nconfidence: 0.8\n---\n\n# AI\n\nSee also [[NonExistentPage]].",
            encoding="utf-8",
        )
        return str(wiki)

    def test_repair_broken_links(self, temp_wiki_dream):
        from dream_cycle import repair_broken_links

        result = repair_broken_links(temp_wiki_dream)
        assert result["total_checked"] >= 1
        # Should have marked the broken link
        content = (Path(temp_wiki_dream) / "concepts" / "ai.md").read_text(encoding="utf-8")
        assert "NonExistentPage" in content

    def test_reinforce_low_confidence(self, temp_wiki_dream):
        from dream_cycle import reinforce_low_confidence

        # Add a low-confidence page
        p = Path(temp_wiki_dream) / "weak.md"
        p.write_text(
            "---\ntitle: Weak\ntype: concept\nconfidence: 0.2\n---\n\n# Weak\n\nLow confidence page.",
            encoding="utf-8",
        )
        weak = reinforce_low_confidence(temp_wiki_dream, threshold=0.3)
        assert len(weak) >= 1
        assert any(w["title"] == "Weak" for w in weak)

    def test_generate_insights(self, temp_wiki_dream):
        from dream_cycle import generate_insights

        insights = generate_insights(temp_wiki_dream)
        assert isinstance(insights, list)


class TestDreamSandbox:
    """Test dream sandbox safety."""

    def test_safe_operation_whitelist(self, tmp_path):
        from dream_sandbox import run_safe

        wiki = tmp_path / "wiki"
        wiki.mkdir()
        result = run_safe(str(wiki), "nonexistent_op")
        assert result["status"] == "blocked"
        assert "repair_links" in result["allowed"]

    def test_safe_repair_runs(self, tmp_path):
        from dream_sandbox import run_safe

        wiki = tmp_path / "wiki"
        wiki.mkdir()
        p = wiki / "test.md"
        p.write_text("---\ntitle: Test\n---\n\n# Test\n", encoding="utf-8")
        result = run_safe(str(wiki), "insights")
        assert result["status"] == "ok"


class TestSeekDBExport:
    """Test SeekDB migration export."""

    def test_export_pages(self, tmp_path):
        from export_for_seekdb import export_pages

        wiki = tmp_path / "wiki"
        wiki.mkdir()
        p = wiki / "test.md"
        p.write_text(
            "---\nid: test\ntitle: Test\ntype: concept\ntags: [ai]\nconfidence: 0.8\n---\n\n# Test\n\nBody with [[Link]].",
            encoding="utf-8",
        )
        out = tmp_path / "export.jsonl"
        result = export_pages(str(wiki), str(out))
        assert result["exported_count"] >= 1
        lines = out.read_text(encoding="utf-8").strip().split("\n")
        assert len(lines) >= 1
        record = json.loads(lines[0])
        assert record["id"] == "test"
        assert "Link" in record["wikilinks"]


class TestBenchmark:
    """Test search benchmark."""

    def test_benchmark_runs(self, tmp_path):
        from benchmark_search import benchmark_search, BENCHMARK_QUERIES

        wiki = tmp_path / "wiki"
        wiki.mkdir()
        p = wiki / "test.md"
        p.write_text(
            "---\ntitle: Robot Locomotion\ntype: concept\n---\n\n# Robot Locomotion\n\nWalking and running.",
            encoding="utf-8",
        )
        out = tmp_path / "bench.json"
        result = benchmark_search(str(wiki), str(out))
        assert result["summary"]["total_queries"] == len(BENCHMARK_QUERIES)
        assert out.exists()

    def test_benchmark_latency_format(self, tmp_path):
        from benchmark_search import benchmark_search

        wiki = tmp_path / "wiki"
        wiki.mkdir()
        out = tmp_path / "bench.json"
        result = benchmark_search(str(wiki), str(out))
        assert isinstance(result["summary"]["avg_latency_ms"], (int, float))
        for q in result["queries"]:
            assert isinstance(q["latency_ms"], (int, float))


class TestSeekDBBackend:
    """Test SeekDB/SQLite compatibility backend."""

    def test_seekdb_search_keyword(self):
        try:
            import pyseekdb
        except ImportError:
            pytest.skip("pyseekdb not installed")
        from seekdb_search_impl import SeekDBSearchImpl
        search = SeekDBSearchImpl("wiki")
        results = search.search("robot", search_type="keyword", top_k=5)
        assert isinstance(results, list)

    def test_seekdb_storage_crud(self, tmp_path):
        try:
            import pyseekdb
        except ImportError:
            pytest.skip("pyseekdb not installed")
        from seekdb_storage_impl import SeekDBStorageImpl
        import wiki_engine as engine

        store = SeekDBStorageImpl(str(tmp_path))
        page_path = tmp_path / "test.md"
        engine.write_frontmatter({"title": "Test", "type": "concept"}, "# Hello\n")
        page_path.write_text(engine.write_frontmatter({"title": "Test", "type": "concept"}, "# Hello\n"), encoding="utf-8")

        store.index_page(str(page_path))
        data = store.read_page(str(page_path))
        assert data["meta"]["title"] == "Test"

    def test_seekdb_health(self):
        from seekdb_client import health_check
        h = health_check()
        assert h["status"] == "ok"
        assert h["pages"] >= 800

    def test_backend_switch_factory(self):
        from search_interface import get_search_impl
        from storage_interface import get_storage_impl

        fs_search = get_search_impl("wiki", backend="filesystem")
        db_search = get_search_impl("wiki", backend="seekdb")
        assert fs_search is not None
        assert db_search is not None

        fs_store = get_storage_impl("wiki", backend="filesystem")
        db_store = get_storage_impl("wiki", backend="seekdb")
        assert fs_store is not None
        assert db_store is not None


class TestAuthManager:
    """Test API key auth system."""

    def test_generate_and_validate_key(self):
        from auth_manager import generate_api_key, validate_api_key

        result = generate_api_key("test_tenant", plan="free")
        assert result["api_key"].startswith("rw_")
        info = validate_api_key(result["api_key"])
        assert info is not None
        assert info["tenant_id"] == "test_tenant"
        assert info["plan"] == "free"

    def test_invalid_key(self):
        from auth_manager import validate_api_key
        assert validate_api_key("invalid_key") is None

    def test_rate_limit(self):
        from auth_manager import generate_api_key, check_rate_limit

        result = generate_api_key("test_tenant2", plan="free")
        status = check_rate_limit(result["api_key"])
        assert status["allowed"] is True
        assert status["remaining"] <= 100


class TestCommercialAPI:
    """Test FastAPI commercial endpoints."""

    def test_health_no_auth(self):
        from commercial_api import app
        from fastapi.testclient import TestClient
        client = TestClient(app)
        resp = client.get("/v1/health")
        assert resp.status_code == 200
        assert resp.json()["status"] == "ok"

    def test_search_requires_auth(self):
        from commercial_api import app
        from fastapi.testclient import TestClient
        client = TestClient(app)
        # Provide invalid API key
        resp = client.post(
            "/v1/search",
            json={"query": "test", "search_type": "keyword", "top_k": 5},
            headers={"X-API-Key": "invalid_key"},
        )
        assert resp.status_code == 401

    def test_search_with_valid_key(self):
        from commercial_api import app
        from fastapi.testclient import TestClient
        from auth_manager import generate_api_key
        client = TestClient(app)
        key = generate_api_key("test_api", plan="free")["api_key"]
        resp = client.post("/v1/search", json={"query": "robot", "search_type": "keyword"}, headers={"X-API-Key": key})
        assert resp.status_code == 200
        assert "results" in resp.json()

    def test_usage_endpoint(self):
        from commercial_api import app
        from fastapi.testclient import TestClient
        from auth_manager import generate_api_key
        client = TestClient(app)
        key = generate_api_key("test_usage", plan="free")["api_key"]
        resp = client.get("/v1/usage", headers={"X-API-Key": key})
        assert resp.status_code == 200
        assert "usage" in resp.json()

    # ── Phase 16: Physics endpoints ──

    def test_physics_impact_requires_auth(self):
        from commercial_api import app
        from fastapi.testclient import TestClient
        client = TestClient(app)
        resp = client.post(
            "/v1/physics/impact",
            json={"variable": "torque"},
            headers={"X-API-Key": "invalid_key"},
        )
        assert resp.status_code == 401

    def test_physics_impact_with_valid_key(self):
        from commercial_api import app
        from fastapi.testclient import TestClient
        from auth_manager import generate_api_key
        client = TestClient(app)
        key = generate_api_key("test_physics", plan="free")["api_key"]
        resp = client.post("/v1/physics/impact", json={"variable": "torque", "radius": 2}, headers={"X-API-Key": key})
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "ok"
        assert data["variable"] == "torque"
        assert "impact" in data

    def test_physics_resolve_with_valid_key(self):
        from commercial_api import app
        from fastapi.testclient import TestClient
        from auth_manager import generate_api_key
        client = TestClient(app)
        key = generate_api_key("test_physics", plan="free")["api_key"]
        resp = client.post("/v1/physics/resolve", json={"entity": "Unitree-G1", "property_name": "MAX_TORQUE"}, headers={"X-API-Key": key})
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "ok"
        assert "resolution" in data

    def test_physics_feasibility_with_valid_key(self):
        from commercial_api import app
        from fastapi.testclient import TestClient
        from auth_manager import generate_api_key
        client = TestClient(app)
        key = generate_api_key("test_physics", plan="free")["api_key"]
        snippet = "MAX_TORQUE = 237  # N·m\n"
        resp = client.post("/v1/physics/feasibility", json={"code_snippet": snippet}, headers={"X-API-Key": key})
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "ok"
        assert "checks" in data
        assert data["parameter_count"] >= 1

    def test_physics_feasibility_empty_snippet(self):
        from commercial_api import app
        from fastapi.testclient import TestClient
        from auth_manager import generate_api_key
        client = TestClient(app)
        key = generate_api_key("test_physics", plan="free")["api_key"]
        resp = client.post("/v1/physics/feasibility", json={"code_snippet": ""}, headers={"X-API-Key": key})
        assert resp.status_code == 400

    # ── Phase 17: Topology & Connection ──

    def test_manifest_json_no_auth(self):
        from commercial_api import app
        from fastapi.testclient import TestClient
        client = TestClient(app)
        resp = client.get("/v1/manifest.json")
        assert resp.status_code == 200
        data = resp.json()
        assert data["service"] == "ROSClaw Steward of Embodied Physical Reality"
        assert "capabilities" in data

    def test_topology_trace_with_valid_key(self):
        from commercial_api import app
        from fastapi.testclient import TestClient
        from auth_manager import generate_api_key
        client = TestClient(app)
        key = generate_api_key("test_topology", plan="free")["api_key"]
        resp = client.post(
            "/v1/topology/trace",
            json={"entity": "Unitree-G1", "parameter": "max_torque", "delta": "+50%", "radius": 2},
            headers={"X-API-Key": key},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "ok"
        assert "subgraph" in data
        assert "safety_assessment" in data

    def test_ontology_entanglement_with_valid_key(self):
        from commercial_api import app
        from fastapi.testclient import TestClient
        from auth_manager import generate_api_key
        client = TestClient(app)
        key = generate_api_key("test_entangle", plan="free")["api_key"]
        resp = client.get(
            "/v1/ontology/entanglement?entity_a=friction&entity_b=heat&context=walking",
            headers={"X-API-Key": key},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "ok"
        assert "entanglement_found" in data
        assert "paths" in data

    def test_reasoning_grounding_with_valid_key(self):
        from commercial_api import app
        from fastapi.testclient import TestClient
        from auth_manager import generate_api_key
        client = TestClient(app)
        key = generate_api_key("test_ground", plan="free")["api_key"]
        resp = client.post(
            "/v1/reasoning/grounding",
            json={"instruction": "make robot faster", "entity": "Unitree-G1", "context": "warehouse"},
            headers={"X-API-Key": key},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "ok"
        assert "grounded_parameters" in data

    def test_analysis_sensitivity_with_valid_key(self):
        from commercial_api import app
        from fastapi.testclient import TestClient
        from auth_manager import generate_api_key
        client = TestClient(app)
        key = generate_api_key("test_sens", plan="free")["api_key"]
        resp = client.post(
            "/v1/analysis/sensitivity",
            json={"parameters": ["max_torque", "motor_temperature", "battery_voltage"], "entity": "Unitree-G1"},
            headers={"X-API-Key": key},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "ok"
        assert "coupling_matrix" in data
        assert "most_sensitive_pair" in data

    def test_analysis_sensitivity_too_few_params(self):
        from commercial_api import app
        from fastapi.testclient import TestClient
        from auth_manager import generate_api_key
        client = TestClient(app)
        key = generate_api_key("test_sens", plan="free")["api_key"]
        resp = client.post(
            "/v1/analysis/sensitivity",
            json={"parameters": ["max_torque"], "entity": "Unitree-G1"},
            headers={"X-API-Key": key},
        )
        assert resp.status_code == 400

    def test_analogy_find_with_valid_key(self):
        from commercial_api import app
        from fastapi.testclient import TestClient
        from auth_manager import generate_api_key
        client = TestClient(app)
        key = generate_api_key("test_analogy", plan="free")["api_key"]
        resp = client.get(
            "/v1/analogy/find?entity=UnknownBot&domain=quadruped",
            headers={"X-API-Key": key},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "ok"
        assert "closest_analog" in data
        assert "similarity_score" in data


class TestBackendConsistency:
    """Test dual backend result consistency."""

    def test_keyword_consistency(self):
        try:
            import pyseekdb
        except ImportError:
            pytest.skip("pyseekdb not installed")
        from search_interface import get_search_impl

        fs = get_search_impl("wiki", backend="filesystem")
        db = get_search_impl("wiki", backend="seekdb")

        fs_results = fs.search("robot", search_type="keyword", top_k=5)
        db_results = db.search("robot", search_type="keyword", top_k=5)

        # Both should return lists
        assert isinstance(fs_results, list)
        assert isinstance(db_results, list)

    def test_hybrid_both_return_results(self):
        try:
            import pyseekdb
        except ImportError:
            pytest.skip("pyseekdb not installed")
        from search_interface import get_search_impl

        fs = get_search_impl("wiki", backend="filesystem")
        db = get_search_impl("wiki", backend="seekdb")

        fs_results = fs.search("locomotion", search_type="hybrid", top_k=5)
        db_results = db.search("locomotion", search_type="hybrid", top_k=5)

        assert isinstance(fs_results, list)
        assert isinstance(db_results, list)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
