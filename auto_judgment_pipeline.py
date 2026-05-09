"""Auto Judgment Pipeline — autonomous parameter extraction → judgment generation.

Inspired by Graphify's --mode deep dual-phase flow:
  INITIAL pass: regex extracts high-confidence declarations (zero LLM cost)
  DEEP pass:    LLM extracts semantic relationships (fills the ~15% gap)

Pipeline:
  scan pages → dual_phase_extract → validate → dedup → conflict_check →
  convert_to_judgment → save → update_index

Designed to run daily via cron or manual trigger.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable

import wiki_engine as engine
from autonomous_extractor import (
    ConfidenceLevel,
    ExtractedParameter,
    LLMExtractor,
    ValidationEngine,
    dual_phase_extract,
)
from judgment_generator import Judgment, save_judgments

logger = logging.getLogger("rosclaw.auto_judgment_pipeline")


# ── Confidence mapping ──

def _hint_to_numeric(hint: str, level: ConfidenceLevel) -> float:
    """Map confidence hint + level to numeric confidence score."""
    base_scores = {
        ConfidenceLevel.EXTRACTED: 0.95,
        ConfidenceLevel.INFERRED: 0.70,
        ConfidenceLevel.AMBIGUOUS: 0.40,
    }
    base = base_scores.get(level, 0.70)
    adjustments = {
        "high": 0.10,
        "medium": 0.00,
        "low": -0.15,
    }
    adj = adjustments.get(hint, 0.00)
    return min(1.0, max(0.0, base + adj))


# ── Pipeline Config ──

@dataclass
class PipelineConfig:
    """Configuration for the auto judgment pipeline."""

    wiki_root: str = "wiki"
    min_confidence: float = 0.50   # Skip judgments below this
    conflict_threshold_pct: float = 20.0
    skip_entities: list[str] = field(default_factory=list)
    require_hardware_limit: bool = False


# ── Pipeline ──

class AutoJudgmentPipeline:
    """Orchestrates autonomous judgment generation from wiki pages."""

    def __init__(
        self,
        config: PipelineConfig | None = None,
        llm_func: Callable[[str, str | None], str] | None = None,
    ):
        self.config = config or PipelineConfig()
        self.extractor = LLMExtractor(llm_func=llm_func)
        self.validator: ValidationEngine | None = None

    def run(self) -> dict[str, Any]:
        """Execute the full pipeline.

        Returns:
            Summary dict with counts, new judgments, issues.
        """
        pages = self._scan_pages()
        existing = self._load_existing_judgments()
        self.validator = ValidationEngine(existing)

        new_judgments: list[Judgment] = []
        stats = {
            "pages_scanned": 0,
            "pages_with_extractions": 0,
            "extractions_total": 0,
            "extractions_valid": 0,
            "extractions_deduped": 0,
            "extractions_conflicts": 0,
            "judgments_created": 0,
            "judgments_skipped_low_confidence": 0,
        }

        for page_path, entity_name, page_text in pages:
            if entity_name in self.config.skip_entities:
                continue

            stats["pages_scanned"] += 1
            extractions = dual_phase_extract(
                page_text,
                llm_extractor=self.extractor,
                validator=self.validator,
                entity_name=entity_name,
            )

            if not extractions:
                continue

            stats["pages_with_extractions"] += 1
            stats["extractions_total"] += len(extractions)

            for ex in extractions:
                # Validate (computes deviation_pct)
                is_valid, issues = self.validator.validate(
                    ex, page_text, entity_name
                )
                # Re-assign confidence now that deviation is known
                ex.confidence_level = self.validator.assign_confidence_level(ex)

                # Count AMBIGUOUS conflicts even if structurally invalid
                if ex.confidence_level == ConfidenceLevel.AMBIGUOUS:
                    stats["extractions_conflicts"] += 1
                    logger.warning(
                        "AMBIGUOUS extraction: %s/%s = %s (deviation %.1f%%)",
                        entity_name, ex.parameter, ex.value, ex.deviation_pct or 0
                    )

                if not is_valid:
                    logger.debug(
                        "Validation failed for %s/%s: %s",
                        entity_name, ex.parameter, issues
                    )
                    continue

                stats["extractions_valid"] += 1

                # Deduplicate against existing (same entity + parameter)
                entity_params = existing.get(entity_name, {})
                if ex.parameter in entity_params:
                    stats["extractions_deduped"] += 1
                    continue

                # Convert to Judgment
                confidence = _hint_to_numeric(ex.confidence_hint, ex.confidence_level)
                if confidence < self.config.min_confidence:
                    stats["judgments_skipped_low_confidence"] += 1
                    continue

                judgment = self._to_judgment(ex, entity_name, page_path)
                new_judgments.append(judgment)
                stats["judgments_created"] += 1

        # Save
        written: list[str] = []
        if new_judgments:
            written = save_judgments(self.config.wiki_root, new_judgments)

        # Log
        engine.append_log(
            self.config.wiki_root,
            f"auto_judgment_pipeline | {stats['pages_scanned']} pages, "
            f"{stats['judgments_created']} new judgments"
        )

        return {
            "status": "done",
            "stats": stats,
            "new_judgments": len(new_judgments),
            "written_files": written,
        }

    def _scan_pages(self) -> list[tuple[str, str, str]]:
        """Scan wiki for pages to process.

        Returns:
            List of (page_path, entity_name, page_text).
        """
        root = Path(self.config.wiki_root)
        results: list[tuple[str, str, str]] = []

        for md_file in root.rglob("*.md"):
            if md_file.name in ("index.md", "log.md"):
                continue
            try:
                content = md_file.read_text(encoding="utf-8")
                meta, body = engine.parse_frontmatter(content)
                entity = meta.get("title", md_file.stem)
                # Prefer body for extraction; include frontmatter title
                text = f"{entity}\n{body}"
                results.append((str(md_file), entity, text))
            except Exception as exc:
                logger.warning("Failed to read %s: %s", md_file, exc)

        return results

    def _load_existing_judgments(self) -> dict[str, dict[str, dict[str, Any]]]:
        """Load existing judgments for deduplication and deviation checks.

        Returns:
            Map of entity_name -> {parameter -> judgment_dict}.
        """
        root = Path(self.config.wiki_root)
        index_path = root / "judgments" / "index.json"
        result: dict[str, dict[str, dict[str, Any]]] = {}

        if not index_path.exists():
            return result

        try:
            data = index_path.read_text(encoding="utf-8")
            import json
            index = json.loads(data)
            for entity, contexts in index.get("by_entity", {}).items():
                for context, params in contexts.items():
                    for param, info in params.items():
                        result.setdefault(entity, {})[param] = info
        except Exception as exc:
            logger.warning("Failed to load existing judgments: %s", exc)

        return result

    @staticmethod
    def _to_judgment(
        ex: ExtractedParameter,
        entity_name: str,
        page_path: str,
    ) -> Judgment:
        """Convert ExtractedParameter to Judgment."""
        confidence = _hint_to_numeric(ex.confidence_hint, ex.confidence_level)

        usage_notes = ""
        if ex.confidence_level == ConfidenceLevel.EXTRACTED:
            usage_notes = "Auto-extracted with high confidence. Verified against source text."
        elif ex.confidence_level == ConfidenceLevel.INFERRED:
            usage_notes = "Auto-extracted via LLM. Please verify before use in production."
        elif ex.confidence_level == ConfidenceLevel.AMBIGUOUS:
            usage_notes = (
                f"⚠️ AMBIGUOUS: deviation {ex.deviation_pct:.1f}% from existing judgment. "
                f"Requires manual review."
            )

        return Judgment(
            context=ex.context,
            entity=entity_name,
            parameter=ex.parameter,
            recommended_value=ex.value,
            unit=ex.unit,
            confidence=round(confidence, 2),
            sources=[f"[[{entity_name}]]", f"Auto-extracted from {Path(page_path).name}"],
            conflicts_resolved=[],
            usage_notes=usage_notes,
            unresolved=ex.confidence_level == ConfidenceLevel.AMBIGUOUS,
            hardware_limit=ex.hardware_limit,
        )


# ── Convenience entry points ──

def run_pipeline(
    wiki_root: str = "wiki",
    llm_func: Callable[[str, str | None], str] | None = None,
    min_confidence: float = 0.50,
) -> dict[str, Any]:
    """One-shot pipeline run.

    Args:
        wiki_root: Path to wiki directory.
        llm_func: Optional LLM callable(prompt, system) -> text.
        min_confidence: Minimum confidence to create a judgment.

    Returns:
        Pipeline summary dict.
    """
    config = PipelineConfig(
        wiki_root=wiki_root,
        min_confidence=min_confidence,
    )
    pipeline = AutoJudgmentPipeline(config=config, llm_func=llm_func)
    return pipeline.run()


def run_for_page(
    page_path: str,
    wiki_root: str = "wiki",
    llm_func: Callable[[str, str | None], str] | None = None,
    min_confidence: float = 0.50,
) -> dict[str, Any]:
    """Run pipeline for a single page only.

    Returns:
        Dict with extracted parameters and generated judgments.
    """
    path = Path(page_path)
    if not path.exists():
        return {"status": "error", "reason": f"Page not found: {page_path}"}

    content = path.read_text(encoding="utf-8")
    meta, body = engine.parse_frontmatter(content)
    entity = meta.get("title", path.stem)
    text = f"{entity}\n{body}"

    # Load existing for validation
    config = PipelineConfig(wiki_root=wiki_root, min_confidence=min_confidence)
    pipeline = AutoJudgmentPipeline(config=config, llm_func=llm_func)
    existing = pipeline._load_existing_judgments()
    validator = ValidationEngine(existing)
    extractor = LLMExtractor(llm_func=llm_func)

    extractions = dual_phase_extract(text, extractor, validator, entity)

    judgments: list[Judgment] = []
    for ex in extractions:
        is_valid, issues = validator.validate(ex, text, entity)
        ex.confidence_level = validator.assign_confidence_level(ex)
        if not is_valid:
            continue
        confidence = _hint_to_numeric(ex.confidence_hint, ex.confidence_level)
        if confidence < min_confidence:
            continue
        judgments.append(AutoJudgmentPipeline._to_judgment(ex, entity, page_path))

    if judgments:
        save_judgments(wiki_root, judgments)

    return {
        "status": "done",
        "entity": entity,
        "extractions_count": len(extractions),
        "judgments_created": len(judgments),
        "judgments": [j.to_dict() for j in judgments],
    }
