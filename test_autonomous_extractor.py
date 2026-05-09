"""Tests for autonomous_extractor.py and auto_judgment_pipeline.py.

Uses mock LLM to avoid real API calls.
"""

from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path

import pytest

from autonomous_extractor import (
    ConfidenceLevel,
    ExtractedParameter,
    LLMExtractor,
    ValidationEngine,
    _coerce_numeric,
    _name_in_text,
    _regex_extract,
    dual_phase_extract,
    extract_from_page,
)
from auto_judgment_pipeline import (
    AutoJudgmentPipeline,
    PipelineConfig,
    _hint_to_numeric,
    run_for_page,
    run_pipeline,
)
from judgment_generator import Judgment


# ── Fixtures ──

@pytest.fixture
def mock_llm():
    """Return a mock LLM function that returns a fixed JSON array."""
    def _llm(prompt: str, system: str | None = None) -> str:
        # Parse what the prompt is asking for and return appropriate mock data
        prompt_lower = prompt.lower()
        if "step height" in prompt_lower or "terrain" in prompt_lower:
            return json.dumps([
                {
                    "parameter": "step_height",
                    "value": 0.12,
                    "unit": "m",
                    "context": "locomotion_control",
                    "confidence_hint": "high",
                    "hardware_limit": 0.15,
                    "source_text": "The step height is 0.12 m for terrain.",
                }
            ])
        if "peak torque" in prompt_lower or "237" in prompt:
            return json.dumps([
                {
                    "parameter": "max_torque",
                    "value": 237,
                    "unit": "N·m",
                    "context": "hardware",
                    "confidence_hint": "high",
                    "hardware_limit": 250,
                    "source_text": "The peak torque of G1 is approximately 237 Newton-meters",
                }
            ])
        if "scientific" in prompt_lower or "2.37e2" in prompt:
            return json.dumps([
                {
                    "parameter": "max_torque",
                    "value": 237,
                    "unit": "N·m",
                    "context": "hardware",
                    "confidence_hint": "high",
                    "hardware_limit": None,
                    "source_text": "扭矩上限设定为 2.37e2 N·m",
                }
            ])
        if "multiple" in prompt_lower or "static" in prompt_lower:
            return json.dumps([
                {
                    "parameter": "max_torque_static",
                    "value": 237,
                    "unit": "N·m",
                    "context": "hardware",
                    "confidence_hint": "high",
                    "hardware_limit": None,
                    "source_text": "max torque: 237 (static) N·m",
                },
                {
                    "parameter": "max_torque_dynamic",
                    "value": 300,
                    "unit": "N·m",
                    "context": "hardware",
                    "confidence_hint": "medium",
                    "hardware_limit": None,
                    "source_text": "max torque: 300 (dynamic) N·m",
                },
            ])
        if "step height" in prompt_lower or "terrain" in prompt_lower:
            return json.dumps([
                {
                    "parameter": "step_height",
                    "value": 0.12,
                    "unit": "m",
                    "context": "locomotion_control",
                    "confidence_hint": "high",
                    "hardware_limit": 0.15,
                    "source_text": "The step height is 0.12 m for terrain.",
                }
            ])
        # Default: extract common robotics params
        return json.dumps([
            {
                "parameter": "step_height",
                "value": 0.12,
                "unit": "m",
                "context": "locomotion_control",
                "confidence_hint": "high",
                "hardware_limit": 0.15,
                "source_text": "Step height is 0.12 m",
            }
        ])
    return _llm


@pytest.fixture
def tmp_wiki(tmp_path):
    """Create a minimal wiki structure."""
    wiki = tmp_path / "wiki"
    wiki.mkdir()
    (wiki / "index.md").write_text("# Index\n", encoding="utf-8")
    (wiki / "log.md").write_text("# Log\n", encoding="utf-8")
    (wiki / "judgments").mkdir()
    return str(wiki)


# ── Test ExtractedParameter dataclass ──

def test_extracted_parameter_roundtrip():
    ep = ExtractedParameter(
        parameter="max_torque",
        value=237,
        unit="N·m",
        context="hardware",
        confidence_hint="high",
        hardware_limit=250,
        confidence_level=ConfidenceLevel.EXTRACTED,
        source_text="Peak torque is 237 Nm",
        deviation_pct=None,
    )
    d = ep.to_dict()
    assert d["parameter"] == "max_torque"
    assert d["confidence_level"] == "extracted"
    ep2 = ExtractedParameter.from_dict(d)
    assert ep2.parameter == ep.parameter
    assert ep2.confidence_level == ep.confidence_level


def test_extracted_parameter_ambiguous():
    ep = ExtractedParameter(
        parameter="max_torque",
        value=300,
        unit="N·m",
        context="hardware",
        confidence_hint="medium",
        hardware_limit=250,
        confidence_level=ConfidenceLevel.AMBIGUOUS,
        deviation_pct=26.6,
    )
    assert ep.to_dict()["deviation_pct"] == 26.6


# ── Test LLMExtractor ──

def test_llm_extractor_parse_json_array(mock_llm):
    extractor = LLMExtractor(llm_func=mock_llm)
    text = "The peak torque of G1 is approximately 237 Newton-meters"
    results = extractor.extract(text)
    assert len(results) == 1
    assert results[0].parameter == "max_torque"
    assert results[0].value == 237
    assert results[0].unit == "N·m"
    assert results[0].hardware_limit == 250


def test_llm_extractor_parse_markdown_fenced(mock_llm):
    extractor = LLMExtractor()
    raw = "```json\n[{\"parameter\": \"foo\", \"value\": 1.0}]\n```"
    results = extractor._parse_llm_response(raw)
    assert len(results) == 1
    assert results[0].parameter == "foo"


def test_llm_extractor_parse_single_object(mock_llm):
    extractor = LLMExtractor()
    raw = '{"parameter": "bar", "value": 42}'
    results = extractor._parse_llm_response(raw)
    assert len(results) == 1
    assert results[0].parameter == "bar"


def test_llm_extractor_invalid_json():
    extractor = LLMExtractor()
    results = extractor._parse_llm_response("not json at all")
    assert results == []


def test_llm_extractor_scientific_notation(mock_llm):
    extractor = LLMExtractor(llm_func=mock_llm)
    text = "扭矩上限设定为 2.37e2 N·m"
    results = extractor.extract(text)
    assert len(results) == 1
    assert results[0].value == 237


# ── Test ValidationEngine ──

def test_validate_name_in_text():
    validator = ValidationEngine()
    ep = ExtractedParameter(
        parameter="max_torque",
        value=237,
        unit="N·m",
        context="hardware",
        confidence_hint="high",
        hardware_limit=None,
    )
    is_valid, issues = validator.validate(ep, "The max torque is 237 Nm")
    assert is_valid
    assert issues == []


def test_validate_name_not_in_text():
    validator = ValidationEngine()
    ep = ExtractedParameter(
        parameter="obscure_param_xyz",
        value=100,
        unit="m",
        context="hardware",
        confidence_hint="high",
        hardware_limit=None,
    )
    is_valid, issues = validator.validate(ep, "The max torque is 237 Nm")
    assert not is_valid
    assert any("not found" in i for i in issues)


def test_validate_range_check():
    validator = ValidationEngine()
    ep = ExtractedParameter(
        parameter="max_torque",
        value=50000,
        unit="N·m",
        context="hardware",
        confidence_hint="high",
        hardware_limit=None,
    )
    is_valid, issues = validator.validate(ep, "max_torque = 50000 N·m")
    assert not is_valid
    assert any("out of reasonable range" in i for i in issues)


def test_validate_deviation_within_threshold():
    existing = {
        "Unitree-G1": {
            "max_torque": {"recommended_value": "250", "confidence": 0.92},
        }
    }
    validator = ValidationEngine(existing)
    ep = ExtractedParameter(
        parameter="max_torque",
        value=245,
        unit="N·m",
        context="hardware",
        confidence_hint="high",
        hardware_limit=None,
    )
    is_valid, issues = validator.validate(ep, "max torque = 245", entity_name="Unitree-G1")
    assert is_valid
    assert ep.deviation_pct is not None
    assert abs(ep.deviation_pct) < 20


def test_validate_deviation_exceeds_threshold():
    existing = {
        "Unitree-G1": {
            "max_torque": {"recommended_value": "250", "confidence": 0.92},
        }
    }
    validator = ValidationEngine(existing)
    ep = ExtractedParameter(
        parameter="max_torque",
        value=400,
        unit="N·m",
        context="hardware",
        confidence_hint="high",
        hardware_limit=None,
    )
    is_valid, issues = validator.validate(ep, "max torque = 400", entity_name="Unitree-G1")
    assert not is_valid
    assert any("Deviation" in i for i in issues)
    assert ep.deviation_pct is not None
    assert abs(ep.deviation_pct) > 20


# ── Test confidence level assignment ──

def test_assign_confidence_code_constant():
    validator = ValidationEngine()
    ep = ExtractedParameter(
        parameter="max_torque", value=237, unit="N·m",
        context="hardware", confidence_hint="medium", hardware_limit=None,
    )
    level = validator.assign_confidence_level(ep, is_code_constant=True)
    assert level == ConfidenceLevel.EXTRACTED


def test_assign_confidence_ambiguous_deviation():
    validator = ValidationEngine()
    ep = ExtractedParameter(
        parameter="max_torque", value=400, unit="N·m",
        context="hardware", confidence_hint="high", hardware_limit=None,
    )
    ep.deviation_pct = 60.0
    level = validator.assign_confidence_level(ep)
    assert level == ConfidenceLevel.AMBIGUOUS


def test_assign_confidence_extracted_with_hw_limit():
    validator = ValidationEngine()
    ep = ExtractedParameter(
        parameter="max_torque", value=237, unit="N·m",
        context="hardware", confidence_hint="high", hardware_limit=250,
    )
    level = validator.assign_confidence_level(ep)
    assert level == ConfidenceLevel.EXTRACTED


def test_assign_confidence_inferred_default():
    validator = ValidationEngine()
    ep = ExtractedParameter(
        parameter="max_torque", value=237, unit="N·m",
        context="hardware", confidence_hint="medium", hardware_limit=None,
    )
    level = validator.assign_confidence_level(ep)
    assert level == ConfidenceLevel.INFERRED


# ── Test _coerce_numeric ──

def test_coerce_numeric_int():
    assert _coerce_numeric("42") == 42


def test_coerce_numeric_float():
    assert _coerce_numeric("3.14") == 3.14


def test_coerce_numeric_scientific():
    assert _coerce_numeric("2.37e2") == 237.0
    assert _coerce_numeric("1.5E-3") == 0.0015


def test_coerce_numeric_none():
    assert _coerce_numeric(None) is None
    assert _coerce_numeric("abc") is None


# ── Test _name_in_text ──

def test_name_in_text_exact():
    assert _name_in_text("max_torque", "The max_torque is 237")


def test_name_in_text_words():
    assert _name_in_text("max_torque", "The max torque is 237")


def test_name_in_text_partial():
    assert _name_in_text("joint_limit_hip_roll", "The hip roll limit is 45 deg")


def test_name_not_in_text():
    assert not _name_in_text("foo_bar_xyz", "The max torque is 237")


# ── Test regex extraction ──

def test_regex_extract_basic():
    text = "max_torque = 237 N·m\nstep_height: 0.12 m"
    results = _regex_extract(text)
    params = {r.parameter for r in results}
    assert "max_torque" in params
    assert "step_height" in params


def test_regex_extract_confidence_extracted():
    text = "MAX_VELOCITY = 3.5 m/s"
    results = _regex_extract(text)
    assert len(results) == 1
    assert results[0].confidence_level == ConfidenceLevel.EXTRACTED


# ── Test dual_phase_extract ──

def test_dual_phase_combines_both(mock_llm):
    text = "max_torque = 237 N·m\nThe step height is 0.12 m for terrain."
    results = dual_phase_extract(text, LLMExtractor(mock_llm), ValidationEngine())
    params = {r.parameter for r in results}
    # Regex should catch max_torque
    assert "max_torque" in params
    # LLM should catch step_height
    assert "step_height" in params


def test_dual_phase_prefers_regex(mock_llm):
    text = "max_torque = 237 N·m"
    results = dual_phase_extract(text, LLMExtractor(mock_llm), ValidationEngine())
    max_t = [r for r in results if r.parameter == "max_torque"]
    assert len(max_t) == 1
    assert max_t[0].confidence_level == ConfidenceLevel.EXTRACTED


# ── Test _hint_to_numeric ──

def test_hint_to_numeric_extracted_high():
    assert _hint_to_numeric("high", ConfidenceLevel.EXTRACTED) == 1.0


def test_hint_to_numeric_inferred_medium():
    assert _hint_to_numeric("medium", ConfidenceLevel.INFERRED) == 0.70


def test_hint_to_numeric_ambiguous():
    assert _hint_to_numeric("high", ConfidenceLevel.AMBIGUOUS) == 0.50


def test_hint_to_numeric_low_hint():
    assert _hint_to_numeric("low", ConfidenceLevel.INFERRED) == pytest.approx(0.55, abs=0.01)


# ── Test AutoJudgmentPipeline ──

def test_pipeline_scans_pages(tmp_wiki, mock_llm):
    # Create a test page with explicit parameter
    page = Path(tmp_wiki) / "test_robot.md"
    page.write_text(
        "---\ntitle: Test-Robot\ntype: entity\n---\n\n"
        "max_torque = 237 N·m\n"
        "step_height: 0.12 m\n",
        encoding="utf-8",
    )

    config = PipelineConfig(wiki_root=tmp_wiki, min_confidence=0.5)
    pipeline = AutoJudgmentPipeline(config=config, llm_func=mock_llm)
    result = pipeline.run()

    assert result["status"] == "done"
    assert result["stats"]["pages_scanned"] >= 1
    assert result["new_judgments"] >= 1


def test_pipeline_deduplicates_existing(tmp_wiki, mock_llm):
    page = Path(tmp_wiki) / "Unitree-G1.md"
    page.write_text(
        "---\ntitle: Unitree-G1\ntype: entity\n---\n\n"
        "max_torque = 237 N·m\n",
        encoding="utf-8",
    )

    # Pre-seed an existing judgment (context must match regex inference: torque → locomotion_control)
    idx = Path(tmp_wiki) / "judgments" / "index.json"
    idx.write_text(
        json.dumps({
            "version": "2.0.0",
            "generated_at": "2026-01-01T00:00:00",
            "total_judgments": 1,
            "by_entity": {
                "Unitree-G1": {
                    "locomotion_control": {
                        "max_torque": {
                            "recommended_value": "237",
                            "confidence": 0.92,
                            "unit": "N·m",
                        }
                    }
                }
            },
            "by_context": {},
        }),
        encoding="utf-8",
    )

    config = PipelineConfig(wiki_root=tmp_wiki, min_confidence=0.5)
    pipeline = AutoJudgmentPipeline(config=config, llm_func=mock_llm)
    result = pipeline.run()

    assert result["stats"]["extractions_deduped"] >= 1


def test_pipeline_skip_low_confidence(tmp_wiki):
    """Extractions with confidence below min_confidence should be skipped."""
    page = Path(tmp_wiki) / "low_conf.md"
    # Use prose format so regex won't catch it; LLM must extract
    page.write_text(
        "---\ntitle: Low-Conf\ntype: entity\n---\n\n"
        "The estimated clearance gap is approximately 1.0 meters.\n",
        encoding="utf-8",
    )

    # Mock LLM returns low-confidence extraction
    def low_conf_llm(prompt: str, system: str | None = None) -> str:
        return json.dumps([
            {
                "parameter": "clearance_gap",
                "value": 1.0,
                "unit": "m",
                "context": "general",
                "confidence_hint": "low",
                "hardware_limit": None,
                "source_text": "The estimated clearance gap is approximately 1.0 meters.",
            }
        ])

    config = PipelineConfig(wiki_root=tmp_wiki, min_confidence=0.60)
    pipeline = AutoJudgmentPipeline(config=config, llm_func=low_conf_llm)
    result = pipeline.run()

    assert result["stats"]["judgments_skipped_low_confidence"] >= 1


# ── Test run_for_page ──

def test_run_for_page_single(tmp_wiki, mock_llm):
    page = Path(tmp_wiki) / "single.md"
    page.write_text(
        "---\ntitle: Single-Robot\ntype: entity\n---\n\n"
        "step_height = 0.12 m\n",
        encoding="utf-8",
    )

    result = run_for_page(str(page), wiki_root=tmp_wiki, llm_func=mock_llm)
    assert result["status"] == "done"
    assert result["entity"] == "Single-Robot"


def test_run_for_page_missing():
    result = run_for_page("/nonexistent/page.md")
    assert result["status"] == "error"


# ── Test extract_from_page convenience ──

def test_extract_from_page(mock_llm):
    text = "max_torque = 237 N·m"
    results = extract_from_page(text, llm_func=mock_llm)
    assert len(results) >= 1
    assert any(r.parameter == "max_torque" for r in results)


# ── Integration: judgment creation with hardware_limit ──

def test_judgment_has_hardware_limit(tmp_wiki, mock_llm):
    page = Path(tmp_wiki) / "hw_test.md"
    page.write_text(
        "---\ntitle: HW-Test\ntype: entity\n---\n\n"
        "max_torque = 237 N·m\n",
        encoding="utf-8",
    )

    result = run_for_page(str(page), wiki_root=tmp_wiki, llm_func=mock_llm)
    assert result["status"] == "done"

    # Check that judgments were saved with hardware_limit
    idx = Path(tmp_wiki) / "judgments" / "index.json"
    if idx.exists():
        data = json.loads(idx.read_text(encoding="utf-8"))
        for entity, contexts in data.get("by_entity", {}).items():
            for ctx, params in contexts.items():
                for param, info in params.items():
                    assert "hardware_limit" in info


# ── Test conflict detection in pipeline ──

def test_pipeline_detects_conflict(tmp_wiki):
    page = Path(tmp_wiki) / "conflict.md"
    page.write_text(
        "---\ntitle: Conflict-Bot\ntype: entity\n---\n\n"
        "max_torque = 400 N·m\n",
        encoding="utf-8",
    )

    # Pre-seed with different value (context must match regex inference)
    idx = Path(tmp_wiki) / "judgments" / "index.json"
    idx.write_text(
        json.dumps({
            "version": "2.0.0",
            "generated_at": "2026-01-01T00:00:00",
            "total_judgments": 1,
            "by_entity": {
                "Conflict-Bot": {
                    "locomotion_control": {
                        "max_torque": {
                            "recommended_value": "250",
                            "confidence": 0.92,
                            "unit": "N·m",
                        }
                    }
                }
            },
            "by_context": {},
        }),
        encoding="utf-8",
    )

    def mock_llm_conflict(prompt: str, system: str | None = None) -> str:
        return json.dumps([
            {
                "parameter": "max_torque",
                "value": 400,
                "unit": "N·m",
                "context": "hardware",
                "confidence_hint": "high",
                "hardware_limit": None,
                "source_text": "max_torque = 400 N·m",
            }
        ])

    config = PipelineConfig(wiki_root=tmp_wiki, min_confidence=0.5)
    pipeline = AutoJudgmentPipeline(config=config, llm_func=mock_llm_conflict)
    result = pipeline.run()

    assert result["stats"]["extractions_conflicts"] >= 1
