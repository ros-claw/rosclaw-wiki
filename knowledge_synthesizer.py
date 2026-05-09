"""ROSClaw Knowledge Synthesizer — compile extracted knowledge into the Wiki.

Pure Python logic. No direct LLM calls. LLM integration happens at the MCP layer.
"""

from __future__ import annotations

import json
import logging
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import wiki_engine as engine
from entity_resolver import resolve_entity

logger = logging.getLogger("rosclaw.synthesizer")

# Initial confidence by source type
SOURCE_CONFIDENCE: dict[str, float] = {
    "official_manual": 0.95,
    "official": 0.95,
    "arxiv_paper": 0.8,
    "paper": 0.8,
    "blog_post": 0.6,
    "blog": 0.6,
    "article": 0.6,
    "unknown": 0.5,
}


@dataclass
class SynthesisPlan:
    """A plan describing how to integrate new facts into the wiki."""

    action: str  # "create_new", "incremental_update", "full_rewrite", "skip", "suggest_consolidation"
    target_page_path: str | None
    existing_body: str | None
    new_facts: dict[str, Any]
    prompt_for_rewrite: str
    updated_frontmatter: dict[str, Any]
    fragment_pages: list[dict[str, Any]] | None = None
    conflicts: list[dict] | None = None


class KnowledgeSynthesizer:
    """Compile structured knowledge into wiki pages following v2 lifecycle rules."""

    def __init__(self, wiki_root: str, engine_module: Any = engine):
        self.wiki_root = Path(wiki_root).resolve()
        self.engine = engine_module
        self.wiki_root.mkdir(parents=True, exist_ok=True)

    # ── Public API ──

    def synthesize(
        self,
        entity_type: str,
        entity_name: str,
        new_facts: dict[str, Any],
        source_meta: dict[str, Any],
    ) -> SynthesisPlan:
        """Determine how to integrate new_facts about an entity into the wiki.

        Args:
            entity_type: One of "entity", "algorithm", "concept", "skill".
            entity_name: Human-readable name, e.g. "Unitree G1".
            new_facts: Structured facts from LLM extraction.
            source_meta: {"source_path", "source_type", "url"}.

        Returns:
            SynthesisPlan describing the action to take.
        """
        source_type = source_meta.get("source_type", "unknown")
        source_path = source_meta.get("source_path", "")
        initial_confidence = SOURCE_CONFIDENCE.get(source_type, 0.5)

        # Entity disambiguation: check for duplicates before locating page
        resolution = resolve_entity(entity_name, str(self.wiki_root))
        if resolution["action"] == "merge":
            existing_path = str(self.wiki_root / resolution["target"])
            logger.info(
                "Entity merge: '%s' matches existing '%s' (sim=%.2f)",
                entity_name,
                resolution.get("title", ""),
                resolution.get("similarity", 0),
            )
        else:
            existing_path = self.locate_page(entity_type, entity_name)
            if resolution["action"] == "llm_required":
                logger.info(
                    "Entity disambiguation required for '%s' (best sim=%.2f)",
                    entity_name,
                    resolution.get("best_similarity", 0),
                )

        # Check for fragmentation before any page-level action
        from fragment_detector import detect_fragmentation, generate_consolidation_prompt

        fragments = detect_fragmentation(entity_name, str(self.wiki_root))
        if len(fragments) >= 3:
            logger.info(
                "Fragmentation detected for '%s': %d scattered pages",
                entity_name,
                len(fragments),
            )
            return SynthesisPlan(
                action="suggest_consolidation",
                target_page_path=None,
                existing_body=None,
                new_facts=new_facts,
                prompt_for_rewrite=generate_consolidation_prompt(
                    entity_name, fragments
                ),
                updated_frontmatter={
                    "title": entity_name,
                    "type": entity_type,
                    "confidence": initial_confidence,
                    "sources": [source_path],
                    "source_type": source_type,
                },
                fragment_pages=fragments,
            )

        if not existing_path:
            # Brand new page
            logger.info("Creating new page: %s (%s)", entity_name, entity_type)
            frontmatter = {
                "title": entity_name,
                "type": entity_type,
                "confidence": initial_confidence,
                "sources": [source_path],
                "source_type": source_type,
            }
            prompt = self._generate_creation_prompt(entity_name, entity_type, new_facts, source_meta)
            return SynthesisPlan(
                action="create_new",
                target_page_path=str(self._page_path_for(entity_type, entity_name)),
                existing_body=None,
                new_facts=new_facts,
                prompt_for_rewrite=prompt,
                updated_frontmatter=frontmatter,
            )

        # Page exists — parse and compare
        existing_content = Path(existing_path).read_text(encoding="utf-8")
        meta, body = self.engine.parse_frontmatter(existing_content)

        # Detect conflicts
        conflicts, reinforcements = self._compare_facts(new_facts, body, meta)

        # Determine action based on conflict severity
        if not new_facts or (not conflicts and not reinforcements):
            logger.info("SKIP — no new information for %s", entity_name)
            return SynthesisPlan(
                action="skip",
                target_page_path=existing_path,
                existing_body=body,
                new_facts=new_facts,
                prompt_for_rewrite="",
                updated_frontmatter=meta,
            )

        # Update confidence
        if conflicts:
            # New information challenges existing — moderate confidence adjustment
            updated_meta = self.engine.update_confidence(dict(meta), reinforcement=False)
        else:
            # Reinforcement
            updated_meta = self.engine.update_confidence(dict(meta), reinforcement=True)

        # Add source to list
        sources = list(updated_meta.get("sources", []))
        if source_path and source_path not in sources:
            sources.append(source_path)
        updated_meta["sources"] = sources

        # Decide action severity
        if len(conflicts) >= 2:
            action = "full_rewrite"
        else:
            action = "incremental_update"

        prompt = self._generate_update_prompt(
            entity_name, entity_type, body, new_facts, conflicts, reinforcements, source_meta
        )

        logger.info(
            "Plan for %s: action=%s, conflicts=%d, reinforcements=%d",
            entity_name, action, len(conflicts), len(reinforcements),
        )

        return SynthesisPlan(
            action=action,
            target_page_path=existing_path,
            existing_body=body,
            new_facts=new_facts,
            prompt_for_rewrite=prompt,
            updated_frontmatter=updated_meta,
            conflicts=conflicts,
        )

    def locate_page(self, entity_type: str, entity_name: str) -> str | None:
        """Return the path to an existing page, or None if not found."""
        page_path = self._page_path_for(entity_type, entity_name)
        if page_path.exists():
            return str(page_path)
        return None

    # ── Internal helpers ──

    def _page_path_for(self, entity_type: str, entity_name: str) -> Path:
        """Compute the expected filesystem path for a page."""
        slug = self.engine.generate_page_id(entity_name)
        subdir = self.wiki_root / self.engine.get_type_dir(entity_type)
        return subdir / f"{slug}.md"

    def _compare_facts(
        self, new_facts: dict[str, Any], existing_body: str, existing_meta: dict[str, Any]
    ) -> tuple[list[dict], list[dict]]:
        """Compare new_facts against existing content.

        Returns:
            (conflicts, reinforcements)
        """
        conflicts: list[dict] = []
        reinforcements: list[dict] = []

        parameters = new_facts.get("parameters", {})
        for key, new_val in parameters.items():
            # Very simple heuristic: if key appears in body with different value
            old_val = self._extract_param_from_body(existing_body, key)
            if old_val is not None and str(old_val).strip() != str(new_val).strip():
                conflicts.append(
                    {
                        "field": key,
                        "old": old_val,
                        "new": new_val,
                        "location": "parameters",
                    }
                )
            else:
                reinforcements.append({"field": key, "value": new_val, "location": "parameters"})

        # Also check relationships
        relationships = new_facts.get("relationships", {})
        for rel_type, targets in relationships.items():
            for target in targets:
                if f"[[{target}]]" not in existing_body and target.lower() not in existing_body.lower():
                    reinforcements.append(
                        {"field": rel_type, "value": target, "location": "relationships"}
                    )

        new_sections = new_facts.get("new_sections", {})
        for section_name, section_content in new_sections.items():
            if section_name.lower() not in existing_body.lower():
                reinforcements.append(
                    {"field": section_name, "value": section_content, "location": "new_sections"}
                )

        return conflicts, reinforcements

    def _extract_param_from_body(self, body: str, key: str) -> str | None:
        """Try to find a parameter value in the markdown body."""
        # Simple regex: key: value or key = value
        patterns = [
            re.compile(rf"^\s*[-*]?\s*\*?{re.escape(key)}\*?\s*[:=]\s*(.+)$", re.I | re.M),
            re.compile(rf"^\s*\|?\s*{re.escape(key)}\s*\|?\s*[:=]\s*(.+)$", re.I | re.M),
        ]
        for pat in patterns:
            m = pat.search(body)
            if m:
                val = m.group(1).strip()
                # Strip trailing sentence punctuation so "12kg." matches "12kg"
                val = re.sub(r"[.!?]+$", "", val)
                return val
        return None

    def _generate_creation_prompt(
        self,
        entity_name: str,
        entity_type: str,
        new_facts: dict[str, Any],
        source_meta: dict[str, Any],
    ) -> str:
        """Generate a prompt for LLM to write a new page."""
        source_desc = f"from {source_meta.get('source_type', 'unknown')} source: {source_meta.get('source_path', '')}"
        return (
            f"You are writing a wiki page for the ROSClaw knowledge base.\n\n"
            f"ENTITY: {entity_name}\n"
            f"TYPE: {entity_type}\n"
            f"SOURCE: {source_desc}\n\n"
            f"STRUCTURED FACTS:\n{json.dumps(new_facts, ensure_ascii=False, indent=2)}\n\n"
            f"TASK: Write a complete, well-structured markdown page.\n"
            f"- Start with a clear definition/overview.\n"
            f"- Include all facts from the structured data.\n"
            f"- Use [[Page Name]] wikilinks for related entities.\n"
            f"- Add relationship annotations (uses, depends_on, implements, etc.).\n"
            f"- Do NOT include YAML frontmatter — it will be added automatically.\n"
            f"Return ONLY the markdown body text."
        )

    def _generate_update_prompt(
        self,
        entity_name: str,
        entity_type: str,
        existing_body: str,
        new_facts: dict[str, Any],
        conflicts: list[dict],
        reinforcements: list[dict],
        source_meta: dict[str, Any],
    ) -> str:
        """Generate a prompt for LLM to update an existing page."""
        source_desc = f"from {source_meta.get('source_type', 'unknown')} source: {source_meta.get('source_path', '')}"
        parts = [
            f"You are updating a wiki page for the ROSClaw knowledge base.\n\n"
            f"ENTITY: {entity_name}\n"
            f"TYPE: {entity_type}\n"
            f"SOURCE: {source_desc}\n\n"
            f"CURRENT PAGE CONTENT:\n---\n{existing_body}\n---\n\n"
            f"NEW FACTS TO INTEGRATE:\n{json.dumps(new_facts, ensure_ascii=False, indent=2)}\n\n"
        ]
        if conflicts:
            parts.append("CONFLICTS DETECTED (preserve both sides in the text):\n")
            for c in conflicts:
                parts.append(f"  - {c['field']}: old='{c['old']}' vs new='{c['new']}'\n")
        if reinforcements:
            parts.append("REINFORCEMENTS (integrate smoothly):\n")
            for r in reinforcements:
                parts.append(f"  - {r['field']}: {r['value']}\n")
        parts.append(
            "\nTASK: Rewrite the page to incorporate the new facts.\n"
            "- Maintain logical flow and structure.\n"
            "- For conflicts, present both perspectives neutrally and note the discrepancy.\n"
            "- For reinforcements, seamlessly weave them into existing sections or add new sections.\n"
            "- Use [[Page Name]] wikilinks for related entities.\n"
            "- Do NOT include YAML frontmatter — it will be added automatically.\n"
        )
        if conflicts:
            parts.append(
                "\n## Conflict Reporting Format (MANDATORY)\n"
                "If conflicts are detected, append a '### 待核实冲突' section at the END of the page.\n"
                "Each conflict MUST use this EXACT structured format (one block per conflict):\n\n"
                "CONFLICT_START\n"
                "field: <parameter name>\n"
                "old_value: <old value> | old_source: <old source page or 'existing'>\n"
                "new_value: <new value> | new_source: <new source file>\n"
                "CONFLICT_END\n\n"
                "Do NOT use natural language to describe conflicts. Only use the block format above.\n"
            )
        parts.append("Return ONLY the updated markdown body text.")
        return "".join(parts)


# Re-export for convenience
__all__ = ["KnowledgeSynthesizer", "SynthesisPlan", "SOURCE_CONFIDENCE"]
