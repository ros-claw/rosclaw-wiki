"""Autonomous Extractor — LLM-driven semantic parameter extraction.

Inspired by Graphify's dual-phase extraction and three-level confidence labels:
  EXTRACTED  → high-confidence (explicit declaration or code constant)
  INFERRED   → LLM-extracted from text (needs verification)
  AMBIGUOUS  → deviation >20% from existing high-confidence judgment

Pipeline:
  page text → LLM semantic scan → structured JSON → validation → confidence label
"""

from __future__ import annotations

import json
import logging
import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable

logger = logging.getLogger("rosclaw.autonomous_extractor")


class ConfidenceLevel(Enum):
    """Three-level confidence label system."""

    EXTRACTED = "extracted"    # 100%可信: explicit declaration or AST-confirmed
    INFERRED = "inferred"      # LLM推断: needs human verification
    AMBIGUOUS = "ambiguous"    # 与已有高置信度judgment偏差>20%


@dataclass
class ExtractedParameter:
    """A parameter extracted from page text."""

    parameter: str
    value: float | int | str
    unit: str
    context: str
    confidence_hint: str          # LLM-provided hint: "high" | "medium" | "low"
    hardware_limit: float | None
    confidence_level: ConfidenceLevel = ConfidenceLevel.INFERRED
    source_text: str = ""         # The sentence/paragraph it came from
    deviation_pct: float | None = None  # Deviation from existing judgment

    def to_dict(self) -> dict[str, Any]:
        return {
            "parameter": self.parameter,
            "value": self.value,
            "unit": self.unit,
            "context": self.context,
            "confidence_hint": self.confidence_hint,
            "hardware_limit": self.hardware_limit,
            "confidence_level": self.confidence_level.value,
            "source_text": self.source_text,
            "deviation_pct": self.deviation_pct,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ExtractedParameter":
        return cls(
            parameter=data["parameter"],
            value=data["value"],
            unit=data.get("unit", ""),
            context=data.get("context", "general"),
            confidence_hint=data.get("confidence_hint", "medium"),
            hardware_limit=data.get("hardware_limit"),
            confidence_level=ConfidenceLevel(data.get("confidence_level", "inferred")),
            source_text=data.get("source_text", ""),
            deviation_pct=data.get("deviation_pct"),
        )


# ── Prompt Templates ──

_EXTRACTION_SYSTEM_PROMPT = """You are a physical parameter extraction specialist for robotics and embodied intelligence research.

Your task: scan the provided text and extract ALL numerical physical parameters.

Rules:
1. Parameter names must be in snake_case (e.g., max_torque, step_height).
2. Values must be numeric. Use scientific notation if needed.
3. Units must be standard SI or common robotics units (N·m, m/s, kg, deg, Hz, rad/s, A, V, W).
4. Context must be one of: hardware, locomotion_control, manipulation, perception, navigation, safety, power, general.
5. confidence_hint: "high" if explicitly stated with units, "medium" if inferred from context, "low" if uncertain.
6. hardware_limit: the physical safety limit mentioned in text, or null.
7. Include the exact source sentence in source_text.

Return ONLY a JSON array. No markdown, no explanation."""

_EXTRACTION_USER_TEMPLATE = """Extract physical parameters from the following text:

---
{text}
---

Return a JSON array of objects with these fields:
- parameter: str (snake_case)
- value: number
- unit: str
- context: str
- confidence_hint: "high" | "medium" | "low"
- hardware_limit: number | null
- source_text: str (exact sentence/paragraph)

JSON output:"""


# ── Extraction Engine ──

class LLMExtractor:
    """Extract parameters from text using an LLM."""

    def __init__(
        self,
        llm_func: Callable[[str, str | None], str] | None = None,
    ):
        """Args:
            llm_func: A callable(prompt, system_prompt) -> response_text.
                      If None, uses LLMInterface from llm_interface module.
        """
        self.llm_func = llm_func

    def _call_llm(self, prompt: str, system: str | None = None) -> str:
        if self.llm_func is not None:
            return self.llm_func(prompt, system)
        # Lazy import to avoid circular dependency and allow test mocking
        from llm_interface import LLMInterface

        iface = LLMInterface()
        return iface.complete(prompt, system=system, temperature=0.1)

    def extract(self, page_text: str) -> list[ExtractedParameter]:
        """Run LLM extraction on page text.

        Returns:
            List of ExtractedParameter objects. Empty list on failure.
        """
        prompt = _EXTRACTION_USER_TEMPLATE.format(text=page_text[:8000])
        try:
            raw = self._call_llm(prompt, _EXTRACTION_SYSTEM_PROMPT)
        except Exception as exc:
            logger.warning("LLM extraction failed: %s", exc)
            return []

        return self._parse_llm_response(raw)

    @staticmethod
    def _parse_llm_response(raw: str) -> list[ExtractedParameter]:
        """Parse JSON array from LLM response."""
        # Strip markdown code fences if present
        text = raw.strip()
        if text.startswith("```"):
            lines = text.splitlines()
            if lines[0].startswith("```"):
                lines = lines[1:]
            if lines and lines[-1].startswith("```"):
                lines = lines[:-1]
            text = "\n".join(lines).strip()

        # Try to find JSON array in the text
        start = text.find("[")
        end = text.rfind("]")
        if start == -1 or end == -1 or end <= start:
            # Maybe it's a single object wrapped in something
            start = text.find("{")
            end = text.rfind("}")
            if start != -1 and end != -1 and end > start:
                text = "[" + text[start : end + 1] + "]"
            else:
                logger.warning("No JSON array found in LLM response: %s", raw[:200])
                return []
        else:
            text = text[start : end + 1]

        try:
            data = json.loads(text)
        except json.JSONDecodeError as exc:
            logger.warning("JSON parse error: %s — response: %s", exc, raw[:200])
            return []

        if isinstance(data, dict):
            data = [data]
        if not isinstance(data, list):
            logger.warning("Expected JSON array, got %s", type(data).__name__)
            return []

        results: list[ExtractedParameter] = []
        for item in data:
            if not isinstance(item, dict):
                continue
            param = item.get("parameter", "").strip()
            if not param:
                continue
            val = item.get("value")
            if val is None:
                continue
            # Coerce value to numeric if possible
            if isinstance(val, str):
                val = _coerce_numeric(val)
                if val is None:
                    continue
            results.append(
                ExtractedParameter(
                    parameter=param,
                    value=val,
                    unit=item.get("unit", "").strip(),
                    context=item.get("context", "general").strip().lower(),
                    confidence_hint=item.get("confidence_hint", "medium").strip().lower(),
                    hardware_limit=_coerce_numeric(item.get("hardware_limit")),
                    source_text=item.get("source_text", "").strip(),
                )
            )
        return results


# ── Validation Engine ──

class ValidationEngine:
    """Validate extracted parameters against source text and existing judgments."""

    # Reasonable ranges for common robotics parameters (min, max)
    _RANGE_CHECKS: dict[str, tuple[float, float]] = {
        "torque": (0.0, 10000.0),
        "force": (0.0, 100000.0),
        "velocity": (0.0, 100.0),
        "speed": (0.0, 100.0),
        "height": (0.0, 10.0),
        "width": (0.0, 10.0),
        "mass": (0.0, 10000.0),
        "weight": (0.0, 10000.0),
        "current": (0.0, 1000.0),
        "voltage": (0.0, 10000.0),
        "power": (0.0, 100000.0),
        "frequency": (0.0, 100000.0),
        "angle": (-360.0, 360.0),
        "temperature": (-273.0, 1000.0),
    }

    def __init__(self, existing_judgments: dict[str, dict[str, Any]] | None = None):
        """Args:
            existing_judgments: Map of entity_name -> {param_name -> judgment_dict}
        """
        self.existing = existing_judgments or {}

    def validate(
        self,
        extracted: ExtractedParameter,
        page_text: str,
        entity_name: str = "",
    ) -> tuple[bool, list[str]]:
        """Validate a single extraction. Returns (is_valid, issues)."""
        issues: list[str] = []

        # 1. Parameter name must appear in page text
        if not _name_in_text(extracted.parameter, page_text):
            issues.append(f"Parameter '{extracted.parameter}' not found in page text")

        # 2. Value must be in reasonable range
        range_issue = self._check_range(extracted)
        if range_issue:
            issues.append(range_issue)

        # 3. Check deviation from existing judgment
        deviation = self._check_deviation(extracted, entity_name)
        extracted.deviation_pct = deviation
        if deviation is not None and abs(deviation) > 20:
            issues.append(
                f"Deviation {deviation:.1f}% from existing judgment "
                f"(threshold: 20%)"
            )

        return len(issues) == 0, issues

    def _check_range(self, extracted: ExtractedParameter) -> str:
        """Check if value is in reasonable range."""
        val = extracted.value
        if not isinstance(val, (int, float)):
            return ""
        param_lower = extracted.parameter.lower()
        for keyword, (min_val, max_val) in self._RANGE_CHECKS.items():
            if keyword in param_lower:
                if val < min_val or val > max_val:
                    return (
                        f"Value {val} out of reasonable range "
                        f"[{min_val}, {max_val}] for '{keyword}'"
                    )
                return ""
        return ""

    def _check_deviation(
        self,
        extracted: ExtractedParameter,
        entity_name: str,
    ) -> float | None:
        """Compute deviation percentage from existing judgment."""
        if not entity_name:
            return None
        entity_judgments = self.existing.get(entity_name, {})
        existing = entity_judgments.get(extracted.parameter)
        if not existing:
            return None
        try:
            existing_val = float(existing.get("recommended_value", 0))
            new_val = float(extracted.value)
            if existing_val == 0:
                return None
            return ((new_val - existing_val) / abs(existing_val)) * 100
        except (ValueError, TypeError):
            return None

    def assign_confidence_level(
        self,
        extracted: ExtractedParameter,
        is_code_constant: bool = False,
    ) -> ConfidenceLevel:
        """Assign confidence level based on extraction quality and existing data."""
        if is_code_constant:
            return ConfidenceLevel.EXTRACTED

        if extracted.deviation_pct is not None and abs(extracted.deviation_pct) > 20:
            return ConfidenceLevel.AMBIGUOUS

        # EXTRACTED if high hint and has hardware limit
        if extracted.confidence_hint == "high" and extracted.hardware_limit is not None:
            return ConfidenceLevel.EXTRACTED

        # INFERRED otherwise
        return ConfidenceLevel.INFERRED


# ── Dual-Phase Extraction (Graphify-inspired) ──

def dual_phase_extract(
    page_text: str,
    llm_extractor: LLMExtractor | None = None,
    validator: ValidationEngine | None = None,
    entity_name: str = "",
) -> list[ExtractedParameter]:
    """Two-phase extraction: rule-based INITIAL + LLM DEEP.

    Phase 1 (INITIAL): Regex scan for explicit parameter declarations (zero LLM cost).
    Phase 2 (DEEP): LLM semantic extraction for everything regex missed.

    Returns:
        Combined list with confidence levels assigned.
    """
    extractor = llm_extractor or LLMExtractor()
    validator = validator or ValidationEngine()

    # Phase 1: Regex extraction (fast, deterministic)
    initial_results = _regex_extract(page_text)
    for r in initial_results:
        r.confidence_level = ConfidenceLevel.EXTRACTED

    # Phase 2: LLM extraction (semantic, fills gaps)
    deep_results = extractor.extract(page_text)

    # Deduplicate: prefer Phase 1 results
    seen_params = {r.parameter.lower() for r in initial_results}
    for dr in deep_results:
        if dr.parameter.lower() in seen_params:
            continue
        is_valid, _ = validator.validate(dr, page_text, entity_name)
        if is_valid:
            dr.confidence_level = validator.assign_confidence_level(dr)
            initial_results.append(dr)

    return initial_results


# ── Helpers ──

def _coerce_numeric(val: Any) -> float | int | None:
    """Try to convert a value to int or float."""
    if val is None:
        return None
    if isinstance(val, (int, float)):
        return val
    if isinstance(val, str):
        val = val.strip()
        # Handle scientific notation like "2.37e2"
        try:
            if "e" in val.lower():
                return float(val)
            if "." in val:
                return float(val)
            return int(val)
        except ValueError:
            return None
    return None


def _name_in_text(parameter: str, text: str) -> bool:
    """Check if parameter name or its variants appear in text."""
    text_lower = text.lower()
    # Exact snake_case
    if parameter.lower() in text_lower:
        return True
    # Convert snake_case to words
    words = parameter.replace("_", " ").lower()
    if words in text_lower:
        return True
    # Check each word
    for word in parameter.split("_"):
        if len(word) > 2 and word.lower() in text_lower:
            return True
    return False


# Regex for explicit parameter declarations in text
_REGEX_PARAM_RE = re.compile(
    r"(?i)(?:^|\n|\s)([\w_]+?)\s*[:=]\s*([0-9.eE+-]+)\s*([a-zA-Z°/%·/\s]+)?(?:\s|$|\n)",
    re.MULTILINE,
)

# Context inference keywords
_CONTEXT_KEYWORDS: dict[str, list[str]] = {
    "locomotion_control": ["torque", "speed", "gait", "walking", "velocity", "step"],
    "manipulation": ["grasp", "gripper", "arm", "dexterity", "force"],
    "perception": ["vision", "lidar", "camera", "sensor", "detection"],
    "navigation": ["map", "path", "slam", "localization", "planning"],
    "safety": ["limit", "emergency", "collision", "shutdown", "threshold"],
    "power": ["battery", "voltage", "current", "watt", "power"],
    "hardware": ["motor", "joint", "actuator", "encoder", "imu"],
}


def _infer_context_from_param(parameter: str) -> str:
    """Infer operational context from parameter name."""
    p_lower = parameter.lower()
    scores: dict[str, int] = {}
    for ctx, keywords in _CONTEXT_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw in p_lower)
        if score > 0:
            scores[ctx] = score
    if scores:
        return max(scores.items(), key=lambda x: x[1])[0]
    return "general"


def _regex_extract(page_text: str) -> list[ExtractedParameter]:
    """Fast regex-based extraction for Phase 1 (INITIAL)."""
    results: list[ExtractedParameter] = []
    for match in _REGEX_PARAM_RE.finditer(page_text):
        name, value_str, unit = match.groups()
        val = _coerce_numeric(value_str)
        if val is None:
            continue
        param = name.strip().lower().replace(" ", "_")
        results.append(
            ExtractedParameter(
                parameter=param,
                value=val,
                unit=(unit or "").strip(),
                context=_infer_context_from_param(param),
                confidence_hint="high",
                hardware_limit=None,
                confidence_level=ConfidenceLevel.EXTRACTED,
                source_text=match.group(0).strip(),
            )
        )
    return results


# ── High-level convenience ──

def extract_from_page(
    page_text: str,
    llm_func: Callable[[str, str | None], str] | None = None,
    existing_judgments: dict[str, dict[str, Any]] | None = None,
    entity_name: str = "",
) -> list[ExtractedParameter]:
    """One-shot extraction with validation and confidence labeling.

    Args:
        page_text: Full page text to analyze.
        llm_func: Optional LLM callable(prompt, system) -> text.
        existing_judgments: Existing judgments for conflict detection.
        entity_name: Entity name for deviation checking.

    Returns:
        List of validated ExtractedParameter with confidence levels.
    """
    extractor = LLMExtractor(llm_func=llm_func)
    validator = ValidationEngine(existing_judgments)
    return dual_phase_extract(page_text, extractor, validator, entity_name)
