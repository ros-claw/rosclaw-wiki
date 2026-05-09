#!/usr/bin/env python3
"""ROSClaw MCP Wiki Server 2.0 — full-auto knowledge ingestion via FastMCP.

Usage:
    ANTHROPIC_API_KEY=xxx python mcp_wiki_server.py --wiki-root ./wiki
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import sys
from pathlib import Path

# Add subdirectories to path so modules can be imported flat (legacy compat)
_PROJECT_ROOT = Path(__file__).parent
for _pkg_dir in ["api", "core", "search", "ingest", "knowledge", "code", "robot", "utils", "dream", "tests"]:
    _pkg_path = _PROJECT_ROOT / _pkg_dir
    if str(_pkg_path) not in sys.path:
        sys.path.insert(0, str(_pkg_path))

try:
    from mcp.server.fastmcp import FastMCP
except ImportError as _import_err:
    FastMCP = None  # type: ignore[misc, assignment]

import wiki_engine as engine
from knowledge_synthesizer import KnowledgeSynthesizer, SOURCE_CONFIDENCE
import retention_engine as retention
import search_backend as search
import vector_index
import qa_engine as qa

logger = logging.getLogger("rosclaw.mcp")

# Lazy import llm_interface — may not be available if no API key
_llm_interface_loaded = False


def _load_llm():
    global _llm_interface_loaded
    if _llm_interface_loaded:
        return
    try:
        from llm_interface import LLMInterface
        _llm_interface_loaded = True
        return LLMInterface
    except Exception as exc:
        logger.warning("LLM interface not available: %s", exc)
        return None


def _setup_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def _read_source_text(source_path: str, raw_root: Path) -> tuple[str, str]:
    """Read a raw source and return (text_content, text_source).

    text_source is one of: "full_text", "abstract_only", "raw_text", "error"
    """
    src = Path(source_path)
    if not src.is_absolute():
        src = raw_root / source_path

    if not src.exists():
        return "", "error"

    if src.suffix == ".pdf":
        # Try full-text extraction first
        try:
            from pdf_extractor import extract_pdf_sections, is_extractor_available

            if is_extractor_available():
                sections = extract_pdf_sections(str(src))
                meta_path = src.with_suffix(".json")
                meta = {}
                if meta_path.exists():
                    try:
                        meta = json.loads(meta_path.read_text(encoding="utf-8"))
                    except Exception:
                        pass

                parts = [f"# {meta.get('title', 'Untitled Paper')}"]
                if meta.get("authors"):
                    parts.append(f"**Authors:** {', '.join(meta['authors'])}")

                abstract = sections.get("abstract", "")
                if not abstract and meta.get("summary"):
                    abstract = meta["summary"]
                if abstract:
                    parts.append("**Abstract:**\n" + abstract)

                for section in ("introduction", "methods", "experiments", "conclusion"):
                    content = sections.get(section, "")
                    if content:
                        parts.append("## " + section.capitalize() + "\n" + content)

                return "\n\n".join(parts), "full_text"
        except Exception as exc:
            logger.warning("Full-text extraction failed for %s: %s", src, exc)

        # Fallback to sidecar JSON abstract
        meta_path = src.with_suffix(".json")
        if meta_path.exists():
            try:
                meta = json.loads(meta_path.read_text(encoding="utf-8"))
                parts = [f"# {meta.get('title', 'Untitled Paper')}"]
                if meta.get("authors"):
                    parts.append(f"**Authors:** {', '.join(meta['authors'])}")
                if meta.get("summary"):
                    parts.append(f"**Abstract:** {meta.get('summary')}")
                return "\n\n".join(parts), "abstract_only"
            except Exception:
                pass
        return f"[PDF file at {src}; text extraction not available in this environment.]", "error"

    try:
        return src.read_text(encoding="utf-8", errors="ignore")[:12000], "raw_text"
    except Exception as exc:
        return f"[Error reading {src}: {exc}]", "error"


def _get_agents_md_text(wiki_root: Path) -> str:
    """Read AGENTS.md for system prompt context."""
    agents_path = wiki_root.parent / "AGENTS.md"
    if agents_path.exists():
        return agents_path.read_text(encoding="utf-8")
    return ""


def main() -> int:
    if FastMCP is None:
        print(
            "ERROR: The 'mcp' package is required to run the MCP server.\n"
            "Install it with: pip install mcp  (requires Python 3.10+)\n",
            file=sys.stderr,
        )
        return 1
    _setup_logging()
    parser = argparse.ArgumentParser(description="ROSClaw MCP Wiki Server 2.0")
    parser.add_argument("--wiki-root", default="./wiki", help="Path to wiki directory")
    parser.add_argument("--raw-root", default="./data/raw", help="Path to raw data directory")
    args = parser.parse_args()

    wiki_root = Path(args.wiki_root).resolve()
    raw_root = Path(args.raw_root).resolve()
    wiki_root.mkdir(parents=True, exist_ok=True)
    raw_root.mkdir(parents=True, exist_ok=True)

    synth = KnowledgeSynthesizer(str(wiki_root))
    agents_text = _get_agents_md_text(wiki_root)

    mcp = FastMCP(
        name="ROSClaw Wiki",
        instructions=(
            "You are the ROSClaw knowledge curator. Use the wiki tools to ingest sources, "
            "create and update pages, manage the knowledge lifecycle, and keep the wiki index current. "
            "Always follow AGENTS.md rules: add YAML frontmatter, use [[wikilinks]], "
            "track confidence, and log all operations."
        ),
    )

    # ── Tool 1: auto_ingest ──

    @mcp.tool()
    def auto_ingest(source_path: str) -> dict:
        """Fully automatic ingestion: read source → LLM extract → synthesize → write wiki.

        Requires ANTHROPIC_API_KEY or OPENAI_API_KEY in environment.
        """
        LLMInterface = _load_llm()
        if not LLMInterface:
            return {"error": "LLM interface not available. Set ANTHROPIC_API_KEY or OPENAI_API_KEY."}

        llm = LLMInterface()
        source_text, text_source = _read_source_text(source_path, raw_root)
        if not source_text:
            return {"error": f"Could not read source: {source_path}"}

        # Step 1: LLM extraction
        fulltext_instructions = ""
        if text_source == "full_text":
            fulltext_instructions = (
                "\nThis source contains the FULL TEXT of a research paper. "
                "From the Methods section, extract ALL quantifiable parameters "
                "(model hyperparameters, physical parameters, experimental settings). "
                "From the Experiments section, extract results, comparison tables, and performance metrics. "
                "From the Conclusion, extract key findings and limitations. "
                "Do NOT assume any specific domain—extract whatever numerical or technical details "
                "are actually present in the paper.\n"
            )

        extract_prompt = (
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
            f'    "relationships": {{"uses": ["X"], "depends_on": ["Y"]}},\n'
            f'    "new_sections": {{"Section Title": "Content..."}}\n'
            f'  }},\n'
            f'  "source_type": "official_manual|arxiv_paper|blog_post"\n'
            f"Return ONLY valid JSON. No markdown code fences."
        )

        try:
            extract_result = llm.complete(
                extract_prompt,
                system=agents_text[:4000],
                temperature=0.2,
            )
            # Clean up JSON
            extract_result = extract_result.strip()
            if extract_result.startswith("```"):
                extract_result = extract_result.split("```json")[-1].split("```")[0].strip()
            entities = json.loads(extract_result)
            if isinstance(entities, dict):
                entities = [entities]
        except Exception as exc:
            logger.exception("LLM extraction failed")
            return {"error": f"LLM extraction failed: {exc}", "raw": extract_result if 'extract_result' in dir() else ""}

        # Step 2: Synthesize each entity
        summaries = []
        for ent in entities:
            entity_type = ent.get("entity_type", "entity")
            entity_name = ent.get("entity_name", "Unknown")
            new_facts = ent.get("new_facts", {})
            source_type = ent.get("source_type", "unknown")

            plan = synth.synthesize(
                entity_type=entity_type,
                entity_name=entity_name,
                new_facts=new_facts,
                source_meta={
                    "source_path": source_path,
                    "source_type": source_type,
                    "url": "",
                },
            )

            if plan.action == "skip":
                summaries.append({
                    "entity": entity_name,
                    "action": "skip",
                    "reason": "no new information",
                })
                continue

            # Step 3: LLM rewrite
            if plan.action == "create_new":
                rewrite_prompt = plan.prompt_for_rewrite
            else:
                rewrite_prompt = plan.prompt_for_rewrite

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
                logger.exception("LLM rewrite failed for %s", entity_name)
                summaries.append({
                    "entity": entity_name,
                    "action": "error",
                    "reason": str(exc),
                })
                continue

            # Step 4: Write page
            if plan.action == "create_new":
                engine.create_page(
                    str(Path(plan.target_page_path).parent),
                    entity_name,
                    new_body,
                    plan.updated_frontmatter,
                )
            else:
                # Overwrite existing page with new frontmatter + body
                target = Path(plan.target_page_path)
                final_content = engine.write_frontmatter(plan.updated_frontmatter, new_body)
                target.write_text(final_content, encoding="utf-8")

            # Step 4b: Incremental search index
            rel_path = str(Path(plan.target_page_path).relative_to(wiki_root))
            search.index_page(str(wiki_root), rel_path)
            vector_index.index_page(str(wiki_root), rel_path)

            engine.append_log(
                str(wiki_root),
                f"ingest | {source_path} | entity: {entity_name} | action: {plan.action}",
            )
            summaries.append({
                "entity": entity_name,
                "action": plan.action,
                "confidence": plan.updated_frontmatter.get("confidence"),
                "path": plan.target_page_path,
            })

        engine.update_index(str(wiki_root))
        return {"status": "done", "entities_processed": len(entities), "summaries": summaries}

    # ── Tool 2: wiki_create_page ──

    @mcp.tool()
    def wiki_create_page(
        type: str,
        title: str,
        content: str,
        meta: dict | None = None,
    ) -> dict:
        """Create a new wiki page in the appropriate subdirectory."""
        if type not in engine.VALID_TYPES:
            return {"error": f"Invalid type '{type}'. Must be one of: {engine.VALID_TYPES}"}

        meta = meta or {}
        meta["title"] = title
        meta["type"] = type
        target_dir = wiki_root / engine.get_type_dir(type)
        if type in ("index", "log"):
            target_dir = wiki_root

        source_type = meta.get("source_type", "unknown")
        meta.setdefault("confidence", SOURCE_CONFIDENCE.get(source_type, 0.5))

        try:
            path = engine.create_page(str(target_dir), title, content, meta)
            engine.update_index(str(wiki_root))
            # Incremental search index
            rel = str(Path(path).relative_to(wiki_root))
            search.index_page(str(wiki_root), rel)
            vector_index.index_page(str(wiki_root), rel)
            engine.append_log(str(wiki_root), f"create | {title} ({type})")
            return {"status": "created", "path": path}
        except Exception as exc:
            logger.exception("wiki_create_page failed")
            return {"error": str(exc)}

    # ── Tool 3: wiki_update_page ──

    @mcp.tool()
    def wiki_update_page(path: str, instruction: str) -> dict:
        """Update a page using an LLM-generated rewrite."""
        LLMInterface = _load_llm()
        if not LLMInterface:
            return {"error": "LLM interface not available."}

        page_path = Path(path)
        if not page_path.is_absolute():
            page_path = wiki_root / path

        if not page_path.exists():
            return {"error": f"Page not found: {page_path}"}

        try:
            content = page_path.read_text(encoding="utf-8")
            meta, body = engine.parse_frontmatter(content)
        except Exception as exc:
            return {"error": f"Failed to read page: {exc}"}

        prompt = (
            f"You are editing a ROSClaw Wiki page.\n\n"
            f"PAGE: {page_path.name}\n"
            f"TYPE: {meta.get('type', 'unknown')}\n"
            f"INSTRUCTION: {instruction}\n\n"
            f"CURRENT CONTENT (no frontmatter):\n---\n{body}\n---\n\n"
            f"Return ONLY the new page body text (markdown), without YAML frontmatter."
        )

        try:
            llm = LLMInterface()
            new_body = llm.complete(prompt, system=_get_agents_md_text(wiki_root)[:4000])
            new_body = new_body.strip()
            if new_body.startswith("```"):
                new_body = new_body.split("```markdown")[-1].split("```")[0].strip()

            meta = engine.update_confidence(dict(meta), reinforcement=True)
            final = engine.write_frontmatter(meta, new_body)
            page_path.write_text(final, encoding="utf-8")
            engine.update_index(str(wiki_root))
            # Incremental search index
            rel = str(page_path.relative_to(wiki_root))
            search.index_page(str(wiki_root), rel)
            vector_index.index_page(str(wiki_root), rel)
            return {"status": "updated", "path": str(page_path)}
        except Exception as exc:
            logger.exception("wiki_update_page failed")
            return {"error": str(exc)}

    # ── Tool 4: wiki_supersede ──

    @mcp.tool()
    def wiki_supersede(old_page_path: str, new_page_path: str) -> dict:
        """Archive an old page and mark the new page as its replacement."""
        old = Path(old_page_path)
        new = Path(new_page_path)
        if not old.is_absolute():
            old = wiki_root / old_page_path
        if not new.is_absolute():
            new = wiki_root / new_page_path

        if not old.exists():
            return {"error": f"Old page not found: {old}"}
        if not new.exists():
            return {"error": f"New page not found: {new}"}

        try:
            archive_path = engine.move_to_archive(str(old), str(wiki_root))

            new_content = new.read_text(encoding="utf-8")
            new_meta, new_body = engine.parse_frontmatter(new_content)
            old_id = engine.parse_frontmatter(old.read_text(encoding="utf-8"))[0].get("id", old.stem)
            supersedes = list(new_meta.get("supersedes", []))
            if old_id not in supersedes:
                supersedes.append(old_id)
            new_meta["supersedes"] = supersedes
            new.write_text(engine.write_frontmatter(new_meta, new_body), encoding="utf-8")

            engine.update_index(str(wiki_root))
            engine.append_log(str(wiki_root), f"supersede | {old.stem} -> {new.stem}")
            return {"status": "superseded", "archive": archive_path, "new_page": str(new)}
        except Exception as exc:
            logger.exception("wiki_supersede failed")
            return {"error": str(exc)}

    # ── Tool 5: wiki_auto_lint ──

    def _search_wiki_internal(query: str, exclude_path: str | None = None) -> list[dict]:
        """Internal search helper for lint auto-fix. Returns top matches by simple grep."""
        query_lower = query.lower()
        results: list[dict] = []
        for md_file in wiki_root.rglob("*.md"):
            if md_file.name in ("index.md", "log.md", "Admin_Dashboard.md"):
                continue
            if exclude_path and str(md_file) == exclude_path:
                continue
            try:
                text = md_file.read_text(encoding="utf-8")
                meta, body = engine.parse_frontmatter(text)
                title = meta.get("title", md_file.stem)
                score = 0
                if query_lower in title.lower():
                    score += 10
                tags = meta.get("tags", [])
                for tag in tags:
                    if query_lower in str(tag).lower():
                        score += 5
                if query_lower in body.lower():
                    score += 2
                if score > 0:
                    results.append({
                        "file_path": str(md_file.relative_to(wiki_root)),
                        "title": title,
                        "score": score,
                        "body_preview": body[:300],
                    })
            except Exception:
                continue
        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:5]

    @mcp.tool()
    def wiki_auto_lint(auto_fix: bool = False) -> dict:
        """Scan wiki for low-confidence and orphan pages. Write findings to log.

        Args:
            auto_fix: If True, attempt to auto-link orphan pages using LLM.
        """
        try:
            pages = engine.list_pages(str(wiki_root))
            low_confidence = [
                {"path": p.get("_path"), "title": p.get("title", "unknown"), "confidence": p.get("confidence", 0)}
                for p in pages
                if float(p.get("confidence", 1.0)) < 0.3
            ]
            orphans = engine.find_orphan_pages(str(wiki_root))

            # Low-confidence reinforcement suggestions
            reinforcement_suggestions: list[str] = []
            if low_confidence:
                for page_info in low_confidence:
                    title = page_info.get("title", "unknown")
                    conf = page_info.get("confidence", 0)
                    reinforcement_suggestions.append(
                        f"- 页面 {title} (置信度: {conf}): 建议搜索关键词以寻找新来源强化。"
                    )

            # Orphan auto-fix
            fix_results: list[dict] = []
            if auto_fix and orphans:
                LLMInterface = _load_llm()
                if LLMInterface:
                    llm = LLMInterface()
                    for orphan_path in orphans[:10]:
                        orphan_file = Path(orphan_path)
                        try:
                            content = orphan_file.read_text(encoding="utf-8")
                            meta, body = engine.parse_frontmatter(content)
                            title = meta.get("title", orphan_file.stem)
                            keywords = f"{title} {' '.join(meta.get('tags', []))} {body[:500]}"
                            candidates = _search_wiki_internal(keywords, exclude_path=str(orphan_file))

                            if not candidates:
                                engine.append_log(
                                    str(wiki_root),
                                    f"auto-fix | orphan: {title} | linked_from: [] | reason: unresolved (no candidates)",
                                )
                                fix_results.append({"orphan": title, "status": "unresolved", "reason": "no candidates"})
                                continue

                            candidate_text = "\n".join(
                                f"{i+1}. {c['title']} ({c['file_path']}): {c['body_preview'][:150]}"
                                for i, c in enumerate(candidates)
                            )
                            prompt = (
                                f"You are a knowledge curator. An orphan page '{title}' needs inbound links.\n\n"
                                f"ORPHAN CONTENT:\n{body[:500]}\n\n"
                                f"CANDIDATE PAGES:\n{candidate_text}\n\n"
                                f"TASK: Select the Top 3 candidate pages that are MOST relevant to link to '{title}'.\n"
                                f"Return ONLY a JSON list of objects with:\n"
                                f'  {{"title": "Page Title", "reason": "brief reason"}}\n'
                                f"Return empty list [] if none are relevant. No markdown code fences."
                            )
                            try:
                                resp = llm.complete(prompt, temperature=0.2)
                                resp = resp.strip()
                                if resp.startswith("```"):
                                    resp = resp.split("```json")[-1].split("```")[0].strip()
                                selected = json.loads(resp)
                                if not isinstance(selected, list):
                                    selected = []
                            except Exception:
                                selected = []

                            linked_from = []
                            for sel in selected:
                                sel_title = sel.get("title", "")
                                # Find candidate by title
                                for cand in candidates:
                                    if cand["title"].lower() == sel_title.lower():
                                        cand_path = wiki_root / cand["file_path"]
                                        if cand_path.exists():
                                            try:
                                                c_meta, c_body = engine.parse_frontmatter(cand_path.read_text(encoding="utf-8"))
                                                # Append link
                                                c_body = c_body.rstrip() + f"\n\n- [[{title}]]\n"
                                                cand_path.write_text(
                                                    engine.write_frontmatter(dict(c_meta), c_body),
                                                    encoding="utf-8",
                                                )
                                                linked_from.append(cand["title"])
                                            except Exception:
                                                pass
                                        break

                            if linked_from:
                                reason = "; ".join(f"{s.get('title')}: {s.get('reason', '')}" for s in selected)
                                engine.append_log(
                                    str(wiki_root),
                                    f"auto-fix | orphan: {title} | linked_from: {linked_from} | reason: {reason}",
                                )
                                fix_results.append({"orphan": title, "status": "fixed", "linked_from": linked_from})
                            else:
                                engine.append_log(
                                    str(wiki_root),
                                    f"auto-fix | orphan: {title} | linked_from: [] | reason: unresolved (LLM found no match)",
                                )
                                fix_results.append({"orphan": title, "status": "unresolved", "reason": "LLM no match"})
                        except Exception as exc:
                            logger.warning("Auto-fix failed for %s: %s", orphan_path, exc)
                            fix_results.append({"orphan": str(orphan_path), "status": "error", "reason": str(exc)})

            report_lines = []
            if low_confidence:
                report_lines.append(f"Low confidence: {len(low_confidence)} pages")
            if orphans:
                report_lines.append(f"Orphan pages: {len(orphans)}")
            if auto_fix:
                fixed = sum(1 for r in fix_results if r["status"] == "fixed")
                report_lines.append(f"Auto-fixed: {fixed}/{len(fix_results)}")
            if not low_confidence and not orphans:
                report_lines.append("Wiki healthy")

            engine.append_log(
                str(wiki_root),
                f"lint | {', '.join(report_lines)}",
            )

            result: dict = {
                "status": "done",
                "low_confidence": low_confidence,
                "orphans": orphans,
            }
            if reinforcement_suggestions:
                result["reinforcement_suggestions"] = reinforcement_suggestions
            if fix_results:
                result["fix_results"] = fix_results
            return result
        except Exception as exc:
            logger.exception("wiki_auto_lint failed")
            return {"error": str(exc)}

    # ── Tool 6: search_wiki ──

    @mcp.tool()
    def search_wiki(query: str, search_type: str = "hybrid", limit: int = 20) -> dict:
        """Search the wiki by tags/titles, full text, semantic similarity, and figure captions.

        Args:
            query: Search query string.
            search_type: "hybrid" (whoosh + semantic RRF), "fulltext" (grep only),
                         "semantic" (vector embedding similarity),
                         "multimodal" (hybrid + figure analysis text boost).
            limit: Max results to return.
        """
        if search_type == "semantic":
            try:
                matches = vector_index.search_semantic(str(wiki_root), query, top_k=limit)
                return {"status": "done", "query": query, "search_type": "semantic", "matches": matches}
            except Exception as exc:
                logger.warning("Semantic search failed: %s", exc)
                return {"status": "error", "query": query, "search_type": "semantic", "message": str(exc), "matches": []}

        if search_type == "hybrid":
            try:
                matches = vector_index.search_hybrid(str(wiki_root), query, top_k=limit)
                return {"status": "done", "query": query, "search_type": "hybrid", "matches": matches}
            except Exception as exc:
                logger.warning("Hybrid search failed: %s", exc)
                # Fall through to legacy hybrid (whoosh + grep)

        # Multimodal: hybrid search with figure-analysis boost
        if search_type == "multimodal":
            try:
                matches = vector_index.search_hybrid(str(wiki_root), query, top_k=limit * 2)
            except Exception as exc:
                logger.warning("Hybrid search failed for multimodal: %s", exc)
                matches = []

            query_lower = query.lower()
            enriched: list[dict] = []
            for hit in matches:
                rel = hit.get("file_path", "")
                score = hit.get("score", 0)
                snippet = hit.get("snippet", "")
                has_figure = False

                # Check for figure-analysis matches and boost
                page_path = wiki_root / rel
                if page_path.exists():
                    try:
                        text = page_path.read_text(encoding="utf-8")
                        _, body = engine.parse_frontmatter(text)
                        if "### 📊 图表分析" in body:
                            fig_section = body.split("### 📊 图表分析")[-1]
                            fig_section = fig_section.split("\n## ")[0]
                            if query_lower in fig_section.lower():
                                score += 15  # strong boost for figure match
                                has_figure = True
                                # Extract matching line as snippet
                                for line in fig_section.splitlines():
                                    if query_lower in line.lower():
                                        snippet = f"[📊图表] {line.strip()[:200]}"
                                        break
                    except Exception:
                        pass

                enriched.append({
                    "file_path": rel,
                    "title": hit.get("title", Path(rel).stem),
                    "snippet": snippet,
                    "score": round(score, 4),
                    "has_figure_analysis": has_figure,
                })

            enriched.sort(key=lambda x: x["score"], reverse=True)
            return {"status": "done", "query": query, "search_type": "multimodal", "matches": enriched[:limit]}

        results: list[dict] = []
        seen: set[str] = set()

        # Try whoosh first (hybrid mode)
        if search_type in ("hybrid", "multimodal"):
            try:
                whoosh_results = search.search_index(str(wiki_root), query, limit=limit)
                for hit in whoosh_results:
                    rel = hit["file_path"]
                    if rel not in seen:
                        seen.add(rel)
                        results.append({
                            "file_path": rel,
                            "title": hit["title"],
                            "snippet": hit["snippet"],
                            "score": hit["score"],
                        })
            except Exception as exc:
                logger.warning("whoosh search failed, falling back to grep: %s", exc)

        # Grep fallback for any missed files or if whoosh is unavailable
        query_lower = query.lower()
        for md_file in wiki_root.rglob("*.md"):
            if md_file.name in ("index.md", "log.md", "Admin_Dashboard.md"):
                continue
            try:
                rel = str(md_file.relative_to(wiki_root))
                if rel in seen:
                    continue
                text = md_file.read_text(encoding="utf-8")
                meta, body = engine.parse_frontmatter(text)
                title = meta.get("title", md_file.stem)
                score = 0
                snippet = ""

                if query_lower in title.lower():
                    score += 10
                    snippet = body[:200].replace("\n", " ")
                if query_lower in body.lower():
                    score += 2
                    if not snippet:
                        for line in body.splitlines():
                            if query_lower in line.lower():
                                snippet = line.strip()[:200]
                                break

                tags = meta.get("tags", [])
                for tag in tags:
                    if query_lower in str(tag).lower():
                        score += 5
                        if not snippet:
                            snippet = body[:200].replace("\n", " ")

                if score > 0:
                    seen.add(rel)
                    results.append({
                        "file_path": rel,
                        "title": title,
                        "snippet": snippet,
                        "score": score,
                    })
            except Exception:
                continue

        results.sort(key=lambda x: x["score"], reverse=True)
        return {"status": "done", "query": query, "search_type": search_type, "matches": results[:limit]}

    # ── Tool 7: find_orphan_pages ──

    @mcp.tool()
    def find_orphan_pages() -> dict:
        """Find pages with no inbound wikilinks."""
        orphans = engine.find_orphan_pages(str(wiki_root))
        if orphans:
            engine.append_log(str(wiki_root), f"lint | {len(orphans)} orphan pages found")
        return {"status": "done", "orphans": orphans}

    # ── Tool 8: retention_decay ──

    @mcp.tool()
    def retention_decay() -> dict:
        """Trigger a global confidence decay pass based on time since last_reinforced."""
        try:
            summary = retention.decay_confidence(str(wiki_root))
            return {"status": "done", **summary}
        except Exception as exc:
            logger.exception("retention_decay failed")
            return {"error": str(exc)}

    # ── Tool 9: retention_suggest_archival ──

    @mcp.tool()
    def retention_suggest_archival(threshold: float = 0.15) -> dict:
        """Suggest pages for archival based on low confidence."""
        try:
            candidates = retention.suggest_archival(str(wiki_root), threshold)
            return {"status": "done", "threshold": threshold, "candidates": candidates}
        except Exception as exc:
            logger.exception("retention_suggest_archival failed")
            return {"error": str(exc)}

    # ── Tool 10: wiki_export_graph ──

    @mcp.tool()
    def wiki_export_graph(fmt: str = "json") -> dict:
        """Export the wiki as a knowledge graph.

        Args:
            fmt: Output format — "json", "sigma", or "cytoscape".
        """
        try:
            from graph_exporter import export_graph

            return export_graph(str(wiki_root), fmt=fmt)
        except Exception as exc:
            logger.exception("wiki_export_graph failed")
            return {"error": str(exc)}

    # ── Tool 11: wiki_consolidate ──

    @mcp.tool()
    def wiki_consolidate(topic: str, fragment_pages: list[str]) -> dict:
        """Consolidate fragmented pages into a unified topic page.

        Args:
            topic: Unified topic title (used for new page name).
            fragment_pages: List of relative paths to fragment pages.
        """
        LLMInterface = _load_llm()
        if not LLMInterface:
            return {"error": "LLM interface not available."}

        if len(fragment_pages) < 2:
            return {"error": "Need at least 2 fragment pages to consolidate."}

        # Read all fragment pages
        fragments: list[dict] = []
        for rel in fragment_pages:
            p = wiki_root / rel
            if not p.exists():
                return {"error": f"Fragment page not found: {rel}"}
            try:
                content = p.read_text(encoding="utf-8")
                meta, body = engine.parse_frontmatter(content)
                fragments.append({
                    "path": rel,
                    "title": meta.get("title", p.stem),
                    "body": body,
                })
            except Exception as exc:
                return {"error": f"Failed to read {rel}: {exc}"}

        # Build consolidation prompt
        parts = [
            f"你是一位知识库整理专家。以下多个 Wiki 页面包含了关于同一主题"
            f"'{topic}' 的碎片化信息。请将它们整合为一个统一、结构清晰的专题页面。\n\n"
        ]
        for i, frag in enumerate(fragments, 1):
            parts.append(f"--- 页面 {i}: {frag['title']} ({frag['path']}) ---\n")
            parts.append(frag["body"][:2000])
            parts.append("\n\n")
        parts.append(
            "TASK: 生成一个统合的 markdown 页面正文，要求:\n"
            "- 逻辑清晰，分节明确\n"
            "- 消除重复信息\n"
            "- 保留所有重要事实和参数\n"
            "- 使用 [[Page Name]] wikilinks 引用相关概念\n"
            "- 不要包含 YAML frontmatter\n"
            "Return ONLY the markdown body text."
        )
        prompt = "".join(parts)

        # Call LLM
        try:
            llm = LLMInterface()
            unified_body = llm.complete(prompt, temperature=0.3)
            unified_body = unified_body.strip()
            if unified_body.startswith("```"):
                unified_body = unified_body.split("```markdown")[-1].split("```")[0].strip()
        except Exception as exc:
            return {"error": f"LLM consolidation failed: {exc}"}

        # Determine target type and directory
        target_type = "concept"
        target_dir = wiki_root / engine.get_type_dir(target_type)
        target_dir.mkdir(parents=True, exist_ok=True)

        # Write unified page
        unified_meta = {
            "title": topic,
            "type": target_type,
            "confidence": 0.75,
            "sources": fragment_pages,
        }
        try:
            unified_path = engine.create_page(
                str(target_dir), topic, unified_body, unified_meta
            )
        except Exception as exc:
            return {"error": f"Failed to create unified page: {exc}"}

        # Update fragment pages with cross-reference note
        unified_slug = engine.generate_page_id(topic)
        for frag in fragments:
            frag_path = wiki_root / frag["path"]
            try:
                content = frag_path.read_text(encoding="utf-8")
                meta, body = engine.parse_frontmatter(content)
                note = f"\n\n> [!NOTE] 相关内容已整合至 [[{topic}]]\n"
                if note.strip() not in body:
                    body = body.rstrip() + note
                    frag_path.write_text(
                        engine.write_frontmatter(meta, body),
                        encoding="utf-8",
                    )
            except Exception as exc:
                logger.warning("Failed to update fragment %s: %s", frag["path"], exc)

        # Update index and log
        engine.update_index(str(wiki_root))
        engine.append_log(
            str(wiki_root),
            f"consolidate | {topic} | merged: {', '.join(fragment_pages)}",
        )

        return {
            "status": "done",
            "unified_page": unified_path,
            "fragments_updated": len(fragment_pages),
        }

    # ── Tool 12: qa_ask ──

    @mcp.tool()
    def qa_ask(question: str, top_k: int = 5) -> dict:
        """Ask a question using the wiki knowledge base and return a cited answer.

        Args:
            question: The user's question.
            top_k: Number of pages to retrieve for context.

        Returns:
            Dict with keys: answer, citations, pages_consulted, has_conflict, qa_path.
        """
        LLMInterface = _load_llm()
        if not LLMInterface:
            return {"error": "LLM interface not available. Set ANTHROPIC_API_KEY or OPENAI_API_KEY."}

        try:
            llm = LLMInterface()
            result = qa.ask(str(wiki_root), question, llm=llm, top_k=top_k, write_back=True)
            return {"status": "done", **result}
        except Exception as exc:
            logger.exception("qa_ask failed")
            return {"error": str(exc)}

    logger.info("Starting ROSClaw MCP Wiki Server 2.0 — wiki_root=%s", wiki_root)
    mcp.run(transport="stdio")
    return 0


if __name__ == "__main__":
    sys.exit(main())
