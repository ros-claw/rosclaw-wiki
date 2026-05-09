#!/usr/bin/env python3
"""Real auto_ingest test with DeepSeek LLM — Phase 3 Module 1 validation."""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

# Use DeepSeek API — unset others to force deepseek detection
os.environ.pop("ANTHROPIC_API_KEY", None)
os.environ.pop("OPENAI_API_KEY", None)
os.environ.setdefault("DEEPSEEK_API_KEY", os.environ.get("DEEPSEEK_API_KEY", ""))

import wiki_engine as engine
from knowledge_synthesizer import KnowledgeSynthesizer
from llm_interface import LLMInterface, DEFAULT_DEEPSEEK_MODEL

WIKI_ROOT = Path("./wiki").resolve()
RAW_ROOT = Path("./data/raw").resolve()
SOURCE_PATH = "articles/wildos.md"
QUALITY_REPORT_DIR = Path("./data/quality_reports").resolve()


def _read_source_text(source_path: str, raw_root: Path) -> str:
    src = Path(source_path)
    if not src.is_absolute():
        src = raw_root / source_path
    if not src.exists():
        return ""
    return src.read_text(encoding="utf-8", errors="ignore")[:12000]


def _get_agents_md_text(wiki_root: Path) -> str:
    agents_path = wiki_root.parent / "AGENTS.md"
    if agents_path.exists():
        return agents_path.read_text(encoding="utf-8")
    return ""


def main() -> int:
    WIKI_ROOT.mkdir(parents=True, exist_ok=True)
    QUALITY_REPORT_DIR.mkdir(parents=True, exist_ok=True)

    # Verify LLM is available
    llm = LLMInterface()
    print(f"[INFO] LLM backend: {llm.backend}, model: {DEFAULT_DEEPSEEK_MODEL if llm.backend == 'deepseek' else 'default'}")

    agents_text = _get_agents_md_text(WIKI_ROOT)
    source_text = _read_source_text(SOURCE_PATH, RAW_ROOT)
    if not source_text:
        print(f"[ERROR] Could not read source: {SOURCE_PATH}")
        return 1

    print(f"[INFO] Source text length: {len(source_text)} chars")

    # Step 1: LLM extraction
    extract_prompt = (
        f"You are extracting structured knowledge from a source for the ROSClaw Wiki.\n\n"
        f"AGENTS.md RULES:\n{agents_text[:2000]}\n\n"
        f"SOURCE:\n---\n{source_text}\n---\n\n"
        f"TASK: Extract entities, algorithms, concepts, and skills mentioned.\n"
        f"Return a JSON list where each item has:\n"
        f'  "entity_type": "entity|algorithm|concept|skill",\n'
        f'  "entity_name": "Name",\n'
        f'  "new_facts": {{\n'
        f'    "parameters": {{"key": "value"}},\n'
        f'    "capabilities": ["cap1", "cap2"],\n'
        f'    "relationships": {{"uses": ["X"], "depends_on": ["Y"]}},\n'
        f'    "new_sections": {{"Section Title": "Content..."}}\n'
        f'  }},\n'
        f'  "source_type": "official_manual|arxiv_paper|blog_post"\n'
        f"Return ONLY valid JSON. No markdown code fences."
    )

    print("[STEP 1] Calling LLM for entity extraction...")
    try:
        extract_result = llm.complete(
            extract_prompt,
            system=agents_text[:4000],
            temperature=0.2,
        )
        extract_result = extract_result.strip()
        if extract_result.startswith("```"):
            extract_result = extract_result.split("```json")[-1].split("```")[0].strip()
        entities = json.loads(extract_result)
        if isinstance(entities, dict):
            entities = [entities]
    except Exception as exc:
        print(f"[ERROR] LLM extraction failed: {exc}")
        return 1

    print(f"[STEP 1] Extracted {len(entities)} entities")

    # Save extraction result for quality review
    quality_report = {
        "source_path": SOURCE_PATH,
        "source_text_length": len(source_text),
        "backend": llm.backend,
        "model": DEFAULT_DEEPSEEK_MODEL if llm.backend == "deepseek" else "default",
        "extracted_entities": entities,
    }
    report_path = QUALITY_REPORT_DIR / "phase3_baseline.json"
    report_path.write_text(json.dumps(quality_report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[STEP 1] Quality report saved to: {report_path}")

    # Step 2-4: Synthesize and rewrite each entity
    synth = KnowledgeSynthesizer(str(WIKI_ROOT))
    summaries = []

    for ent in entities:
        entity_type = ent.get("entity_type", "entity")
        entity_name = ent.get("entity_name", "Unknown")
        new_facts = ent.get("new_facts", {})
        source_type = ent.get("source_type", "unknown")

        print(f"\n[ENTITY] {entity_name} ({entity_type})")

        plan = synth.synthesize(
            entity_type=entity_type,
            entity_name=entity_name,
            new_facts=new_facts,
            source_meta={
                "source_path": SOURCE_PATH,
                "source_type": source_type,
                "url": "",
            },
        )

        print(f"  [PLAN] action={plan.action}, target={plan.target_page_path}")

        if plan.action == "skip":
            summaries.append({"entity": entity_name, "action": "skip", "reason": "no new information"})
            continue

        # Step 3: LLM rewrite
        rewrite_prompt = plan.prompt_for_rewrite
        print(f"  [STEP 3] Calling LLM for rewrite...")
        try:
            new_body = llm.complete(
                rewrite_prompt,
                system=agents_text[:4000],
                temperature=0.3,
            )
            new_body = new_body.strip()
            if new_body.startswith("```"):
                new_body = new_body.split("```markdown")[-1].split("```")[0].strip()
        except Exception as exc:
            print(f"  [ERROR] LLM rewrite failed: {exc}")
            summaries.append({"entity": entity_name, "action": "error", "reason": str(exc)})
            continue

        # Step 4: Write page
        if plan.action == "create_new":
            target_dir = str(Path(plan.target_page_path).parent)
            engine.create_page(target_dir, entity_name, new_body, plan.updated_frontmatter)
        else:
            target = Path(plan.target_page_path)
            final_content = engine.write_frontmatter(plan.updated_frontmatter, new_body)
            target.write_text(final_content, encoding="utf-8")

        engine.append_log(
            str(WIKI_ROOT),
            f"ingest | {SOURCE_PATH} | entity: {entity_name} | action: {plan.action}",
        )
        summaries.append({
            "entity": entity_name,
            "action": plan.action,
            "confidence": plan.updated_frontmatter.get("confidence"),
            "path": plan.target_page_path,
        })
        print(f"  [WRITE] {plan.target_page_path}")

    # Update index
    engine.update_index(str(WIKI_ROOT))

    print(f"\n{'='*60}")
    print(f"[DONE] Processed {len(entities)} entities")
    for s in summaries:
        print(f"  - {s['entity']}: {s['action']} (confidence: {s.get('confidence', 'N/A')})")
    print(f"[INDEX] {WIKI_ROOT / 'index.md'}")
    print(f"[LOG] {WIKI_ROOT / 'log.md'}")
    print(f"[REPORT] {report_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
