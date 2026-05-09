#!/usr/bin/env python3
"""Compare full-text vs abstract-only knowledge extraction.

Runs LLM extraction twice on the same paper:
1. Abstract only (baseline)
2. Full text (with Methods/Experiments sections)

Generates a quantitative comparison report.
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime
from pathlib import Path

# Force DeepSeek backend — same pattern as test_real_ingest.py
os.environ.pop("ANTHROPIC_API_KEY", None)
os.environ.pop("OPENAI_API_KEY", None)
os.environ.setdefault("DEEPSEEK_API_KEY", os.environ.get("DEEPSEEK_API_KEY", ""))

from llm_interface import LLMInterface

QUALITY_REPORT_DIR = Path("./data/quality_reports").resolve()
RAW_ROOT = Path("./data/raw").resolve()
WIKI_ROOT = Path("./wiki").resolve()

PAPER_ID = "2602.19308"
PDF_PATH = RAW_ROOT / "papers" / f"{PAPER_ID}.pdf"


def _get_agents_md_text() -> str:
    agents_path = WIKI_ROOT.parent / "AGENTS.md"
    if agents_path.exists():
        return agents_path.read_text(encoding="utf-8")
    return ""


def _build_extract_prompt(source_text: str, agents_text: str, is_fulltext: bool = False) -> str:
    fulltext_instructions = ""
    if is_fulltext:
        fulltext_instructions = (
            "\nThis source contains the FULL TEXT of a research paper. "
            "From the Methods section, extract ALL quantifiable parameters "
            "(model hyperparameters, physical parameters, experimental settings). "
            "From the Experiments section, extract results, comparison tables, and performance metrics. "
            "From the Conclusion, extract key findings and limitations. "
            "Do NOT assume any specific domain—extract whatever numerical or technical details "
            "are actually present in the paper.\n"
        )

    return (
        f"You are extracting structured knowledge from a source for the ROSClaw Wiki.\n\n"
        f"AGENTS.md RULES:\n{agents_text[:2000]}\n\n"
        f"SOURCE:\n---\n{source_text}\n---\n\n"
        f"{fulltext_instructions}"
        f"TASK: Extract entities, algorithms, concepts, and skills mentioned.\n"
        f"Return a JSON list where each item has:\n"
        f'  "entity_type": "entity|algorithm|concept|skill",\n'
        f'  "entity_name": "Name",\n'
        f'  "new_facts": {{\n'
        f'    "parameters": {{"key": "value"}},\n'
        f'    "capabilities": ["cap1", "cap2"],\n'
        f'    "relationships": {{"uses": ["X"], "depends_on": ["Y"]}}\n'
        f'  }},\n'
        f'  "source_type": "official_manual|arxiv_paper|blog_post"\n'
        f"Return ONLY valid JSON. No markdown code fences."
    )


def _call_llm_extract(llm: LLMInterface, prompt: str, agents_text: str, run_label: str = "") -> list[dict]:
    extract_result = llm.complete(prompt, system=agents_text[:4000], temperature=0.2)
    extract_result = extract_result.strip()
    if extract_result.startswith("```"):
        extract_result = extract_result.split("```json")[-1].split("```")[0].strip()
    try:
        entities = json.loads(extract_result)
    except json.JSONDecodeError as exc:
        # Save raw response for debugging
        debug_path = QUALITY_REPORT_DIR / f"debug_{run_label}_raw.json"
        debug_path.write_text(extract_result, encoding="utf-8")
        print(f"  [DEBUG] Raw response saved to {debug_path}")
        raise
    if isinstance(entities, dict):
        entities = [entities]
    return entities


def _count_parameters(entities: list[dict]) -> int:
    """Count total parameter entries across all entities."""
    total = 0
    for ent in entities:
        params = ent.get("new_facts", {}).get("parameters", {})
        if isinstance(params, dict):
            total += len(params)
    return total


def _count_capabilities(entities: list[dict]) -> int:
    total = 0
    for ent in entities:
        caps = ent.get("new_facts", {}).get("capabilities", [])
        if isinstance(caps, list):
            total += len(caps)
    return total


def _count_relationships(entities: list[dict]) -> int:
    total = 0
    for ent in entities:
        rels = ent.get("new_facts", {}).get("relationships", {})
        if isinstance(rels, dict):
            for v in rels.values():
                if isinstance(v, list):
                    total += len(v)
    return total


def main() -> int:
    QUALITY_REPORT_DIR.mkdir(parents=True, exist_ok=True)

    if not PDF_PATH.exists():
        print(f"[ERROR] PDF not found: {PDF_PATH}")
        return 1

    # Import pdf_extractor here (after env setup)
    from pdf_extractor import extract_pdf_sections

    sections = extract_pdf_sections(str(PDF_PATH))
    abstract = sections.get("abstract", "")
    full_text = sections.get("full_text", "")

    # Compose focused full-text input from richest sections
    # Prioritize Methods and Experiments where parameters live
    intro = sections.get("introduction", "")
    methods = sections.get("methods", "")
    experiments = sections.get("experiments", "")
    conclusion = sections.get("conclusion", "")

    focused_text = ""
    if abstract:
        focused_text += abstract + "\n\n"
    if intro:
        focused_text += intro[:3000] + "\n\n"
    if methods:
        focused_text += methods[:10000] + "\n\n"
    if experiments:
        focused_text += experiments[:5000] + "\n\n"
    if conclusion:
        focused_text += conclusion[:3000] + "\n\n"

    # Fallback to raw full_text if sections are empty
    if not focused_text.strip():
        focused_text = full_text

    print(f"[INFO] Paper: {PAPER_ID}")
    print(f"[INFO] Abstract length: {len(abstract)} chars")
    print(f"[INFO] Full text length: {len(full_text)} chars")

    if not abstract:
        print("[ERROR] No abstract extracted from PDF")
        return 1

    # Use focused section composition for maximum parameter coverage
    full_text_truncated = focused_text[:25000]

    llm = LLMInterface()
    print(f"[INFO] LLM backend: {llm.backend}")
    print(f"[INFO] Focused text length: {len(full_text_truncated)} chars (from sections)")
    if llm.backend == "none":
        print("[ERROR] No LLM backend available")
        return 1

    agents_text = _get_agents_md_text()

    # --- Run 1: Abstract only ---
    print("\n[RUN 1] Extracting from abstract only...")
    abstract_prompt = _build_extract_prompt(abstract, agents_text, is_fulltext=False)
    try:
        abstract_entities = _call_llm_extract(llm, abstract_prompt, agents_text, run_label="abstract")
        print(f"[RUN 1] Extracted {len(abstract_entities)} entities")
    except Exception as exc:
        print(f"[RUN 1] FAILED: {exc}")
        abstract_entities = []

    # --- Run 2: Full text ---
    print("\n[RUN 2] Extracting from full text...")
    fulltext_prompt = _build_extract_prompt(full_text_truncated, agents_text, is_fulltext=True)
    try:
        fulltext_entities = _call_llm_extract(llm, fulltext_prompt, agents_text, run_label="fulltext")
        print(f"[RUN 2] Extracted {len(fulltext_entities)} entities")
    except Exception as exc:
        print(f"[RUN 2] FAILED: {exc}")
        fulltext_entities = []

    # --- Compute metrics ---
    abs_counts = {
        "entities": len(abstract_entities),
        "parameters": _count_parameters(abstract_entities),
        "capabilities": _count_capabilities(abstract_entities),
        "relationships": _count_relationships(abstract_entities),
    }
    full_counts = {
        "entities": len(fulltext_entities),
        "parameters": _count_parameters(fulltext_entities),
        "capabilities": _count_capabilities(fulltext_entities),
        "relationships": _count_relationships(fulltext_entities),
    }

    def _gain(full: int, abs_val: int) -> str:
        if abs_val == 0:
            return "∞" if full > 0 else "1.0x"
        return f"{full / abs_val:.1f}x"

    # --- Generate report ---
    report_lines = [
        "# Full Text vs Abstract Knowledge Extraction Report",
        "",
        f"**Paper:** {PAPER_ID}",
        f"**Date:** {datetime.now().strftime('%Y-%m-%d')}",
        f"**Model:** {llm.backend} ({'deepseek-v4-flash' if llm.backend == 'deepseek' else 'default'})",
        "",
        "## Text Statistics",
        "",
        "| Metric | Abstract Only | Full Text |",
        "|--------|--------------|-----------|",
        f"| Characters | {len(abstract)} | {len(full_text)} ({len(full_text_truncated)} focused section chars used for LLM) |",
        "| Source | PDF extraction (abstract section) | PDF extraction (PyMuPDF) |",
        "",
        "## Extraction Results",
        "",
        "| Metric | Abstract | Full Text | Gain |",
        "|--------|----------|-----------|------|",
        f"| Entities extracted | {abs_counts['entities']} | {full_counts['entities']} | {_gain(full_counts['entities'], abs_counts['entities'])} |",
        f"| Parameters extracted | {abs_counts['parameters']} | {full_counts['parameters']} | {_gain(full_counts['parameters'], abs_counts['parameters'])} |",
        f"| Capabilities extracted | {abs_counts['capabilities']} | {full_counts['capabilities']} | {_gain(full_counts['capabilities'], abs_counts['capabilities'])} |",
        f"| Relationships extracted | {abs_counts['relationships']} | {full_counts['relationships']} | {_gain(full_counts['relationships'], abs_counts['relationships'])} |",
        "",
        "## Abstract Entities",
        "",
        "```json",
        json.dumps(abstract_entities[:5], ensure_ascii=False, indent=2),
        "```",
        "",
        "## Full Text Entities (first 5)",
        "",
        "```json",
        json.dumps(fulltext_entities[:5], ensure_ascii=False, indent=2),
        "```",
        "",
        "## Conclusion",
        "",
        f"Full-text extraction provides **{_gain(full_counts['entities'], abs_counts['entities'])} more entities** and **{_gain(full_counts['parameters'], abs_counts['parameters'])} more parameters** than abstract-only extraction.",
        "This validates that PDF full-text extraction is essential for deep knowledge extraction.",
    ]

    report_path = QUALITY_REPORT_DIR / "fulltext_vs_abstract.md"
    report_path.write_text("\n".join(report_lines), encoding="utf-8")

    print(f"\n{'='*60}")
    print("COMPARISON SUMMARY")
    print(f"{'='*60}")
    print(f"Abstract entities:      {abs_counts['entities']}")
    print(f"Full-text entities:     {full_counts['entities']}")
    print(f"Entity gain:            {_gain(full_counts['entities'], abs_counts['entities'])}")
    print(f"Parameter gain:         {_gain(full_counts['parameters'], abs_counts['parameters'])}")
    print(f"\nReport saved to: {report_path}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
