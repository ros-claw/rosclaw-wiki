"""ROSClaw QA Engine — answer questions with citations and conflict detection.

Retrieves relevant wiki pages, synthesizes an answer with [[wikilink]] citations,
and actively warns about data conflicts between sources.
"""

from __future__ import annotations

import json
import logging
import re
from datetime import datetime
from pathlib import Path
from typing import Any, Callable

import wiki_engine as engine
from llm_interface import LLMInterface

logger = logging.getLogger("rosclaw.qa")


def _search_pages(wiki_root: str, query: str, top_k: int = 5) -> list[dict[str, Any]]:
    """Hybrid search for candidate pages."""
    try:
        from vector_index import search_hybrid

        results = search_hybrid(wiki_root, query, top_k=top_k)
        if results:
            return results
    except Exception as exc:
        logger.warning("Hybrid search failed, falling back to grep: %s", exc)

    # Fallback: tokenized grep
    root = Path(wiki_root)
    query_lower = query.lower()
    # Tokenize query, dropping short/common stop words
    stop_words = {"what", "is", "the", "a", "an", "of", "in", "on", "at", "to", "for", "with", "and", "or", "how", "does", "do", "are", "was", "were", "be", "been", "have", "has", "had", "will", "would", "could", "should", "can", "may", "might", "about", "from", "by", "it", "its", "this", "that", "these", "those", "i", "you", "he", "she", "we", "they", "me", "him", "her", "us", "them", "my", "your", "his", "our", "their"}
    query_tokens = [t for t in re.findall(r"[a-z0-9一-鿿]+", query_lower) if len(t) > 1 and t not in stop_words]
    if not query_tokens:
        query_tokens = [query_lower]
    matches: list[dict[str, Any]] = []
    for md_file in root.rglob("*.md"):
        if md_file.name in ("index.md", "log.md", "Admin_Dashboard.md"):
            continue
        try:
            text = md_file.read_text(encoding="utf-8")
            meta, body = engine.parse_frontmatter(text)
            title = meta.get("title", md_file.stem)
            title_lower = title.lower()
            body_lower = body.lower()
            score = 0
            matched_tokens = 0
            for token in query_tokens:
                if token in title_lower:
                    score += 10
                if token in body_lower:
                    score += 2
                    matched_tokens += 1
            # Boost if a high proportion of query tokens matched
            if query_tokens and matched_tokens / len(query_tokens) >= 0.5:
                score += 5
            if score > 0:
                matches.append({
                    "file_path": str(md_file.relative_to(root)),
                    "title": title,
                    "score": score,
                })
        except Exception:
            continue
    matches.sort(key=lambda x: x["score"], reverse=True)
    return matches[:top_k]


def _read_page_fulltext(wiki_root: str, rel_path: str) -> tuple[str, str]:
    """Read a wiki page and return (title, full_body)."""
    path = Path(wiki_root) / rel_path
    if not path.exists():
        return rel_path, ""
    try:
        text = path.read_text(encoding="utf-8")
        meta, body = engine.parse_frontmatter(text)
        return meta.get("title", path.stem), body
    except Exception:
        return path.stem, ""


def _build_qa_prompt(question: str, pages: list[dict[str, str]]) -> str:
    """Construct the LLM prompt with context, citation rules, and conflict alert."""
    parts = [
        "You are a knowledgeable research assistant for the ROSClaw embodied-intelligence wiki.\n",
        f"USER QUESTION: {question}\n",
        "Retrieved context from the wiki:\n",
        "=" * 60,
    ]

    for i, p in enumerate(pages, 1):
        parts.append(f"\n--- Source {i}: {p['title']} ---\n")
        parts.append(p["body"][:3000])

    parts.extend([
        "\n" + "=" * 60,
        "\nINSTRUCTIONS:",
        "1. Answer the user's question based ONLY on the retrieved sources above.",
        "2. For EVERY key claim, fact, or numerical value in your answer,",
        "   you MUST attach a citation in the format [[Page Title]].",
        "3. If the retrieved sources contain CONTRADICTIONS (e.g., different",
        "   values for the same parameter, conflicting conclusions), do NOT",
        "   try to resolve them yourself. Instead, prominently highlight the",
        "   conflict using the following format:",
        "   > [!WARNING] 数据冲突",
        "   > - 来源 A claims X [[Source A Title]]",
        "   > - 来源 B claims Y [[Source B Title]]",
        "4. If the sources do not contain enough information to answer,",
        "   clearly state that the information is missing.",
        "5. Return ONLY the answer text (markdown). No YAML frontmatter.",
    ])

    return "\n".join(parts)


def _extract_citations(answer_text: str) -> list[str]:
    """Extract [[Page Title]] citations from answer text."""
    pattern = re.compile(r"\[\[(.+?)\]\]")
    return list(dict.fromkeys(pattern.findall(answer_text)))


def _has_conflict_warning(answer_text: str) -> bool:
    """Check if answer contains a conflict warning block."""
    return "[!WARNING]" in answer_text or "[!WARNING] 数据冲突" in answer_text


def ask(
    wiki_root: str,
    question: str,
    llm: LLMInterface | None = None,
    top_k: int = 5,
    write_back: bool = True,
) -> dict[str, Any]:
    """Answer a question using the wiki knowledge base.

    Args:
        wiki_root: Path to the wiki root directory.
        question: The user's question.
        llm: LLMInterface instance. If None, a new one is created.
        top_k: Number of pages to retrieve.
        write_back: If True, save the Q&A pair to wiki/qa/.

    Returns:
        Dict with keys: answer, citations, pages_consulted, has_conflict, qa_path.
    """
    wiki_root_path = Path(wiki_root)

    # Step 1: Retrieve candidate pages
    search_results = _search_pages(wiki_root, question, top_k=top_k)
    if not search_results:
        return {
            "answer": "No relevant pages found in the wiki to answer this question.",
            "citations": [],
            "pages_consulted": [],
            "has_conflict": False,
            "qa_path": None,
        }

    # Step 2: Read full text of top pages
    pages: list[dict[str, str]] = []
    pages_consulted: list[str] = []
    for hit in search_results:
        title, body = _read_page_fulltext(wiki_root, hit["file_path"])
        if body.strip():
            pages.append({"title": title, "body": body, "path": hit["file_path"]})
            pages_consulted.append(hit["file_path"])

    if not pages:
        return {
            "answer": "Retrieved pages have no readable content.",
            "citations": [],
            "pages_consulted": pages_consulted,
            "has_conflict": False,
            "qa_path": None,
        }

    # Step 3: Build prompt and call LLM
    prompt = _build_qa_prompt(question, pages)

    if llm is None:
        llm = LLMInterface()

    try:
        answer = llm.complete(prompt, temperature=0.3)
    except Exception as exc:
        logger.exception("QA LLM call failed")
        return {
            "answer": f"Error generating answer: {exc}",
            "citations": [],
            "pages_consulted": pages_consulted,
            "has_conflict": False,
            "qa_path": None,
        }

    # Step 4: Post-process
    citations = _extract_citations(answer)
    has_conflict = _has_conflict_warning(answer)

    if has_conflict:
        logger.warning("Data conflict detected in QA answer for: %s", question)

    # Step 5: Write Q&A page to wiki/qa/
    qa_path: str | None = None
    if write_back:
        qa_dir = wiki_root_path / "qa"
        qa_dir.mkdir(parents=True, exist_ok=True)

        slug = engine.generate_page_id(question)[:50]
        qa_title = f"Q: {question[:80]}"
        qa_body = (
            f"## Question\n\n{question}\n\n"
            f"## Answer\n\n{answer}\n\n"
            f"## Sources Consulted\n\n"
            + "\n".join(f"- [[{p['title']}]]" for p in pages)
        )
        qa_meta = {
            "title": qa_title,
            "type": "qa",
            "tags": ["qa", "auto-generated"],
            "confidence": 0.7,
            "sources": pages_consulted,
        }
        try:
            qa_path = engine.create_page(str(qa_dir), qa_title, qa_body, qa_meta)
            # Index in search backends
            try:
                import search_backend as search
                import vector_index

                rel = str(Path(qa_path).relative_to(wiki_root_path))
                search.index_page(wiki_root, rel)
                vector_index.index_page(wiki_root, rel)
            except Exception as idx_exc:
                logger.warning("Failed to index QA page: %s", idx_exc)

            engine.append_log(
                wiki_root,
                f"qa | {question[:60]} | conflict: {has_conflict} | pages: {len(pages_consulted)}",
            )

            # Emit page_created event for Web UI graph refresh
            try:
                import event_bus
                rel_qa = str(Path(qa_path).relative_to(wiki_root_path))
                event_bus.emit("page_created", {"path": rel_qa, "title": qa_title})
            except Exception as exc:
                logger.warning("Failed to emit page_created event: %s", exc)
        except Exception as exc:
            logger.warning("Failed to write QA page: %s", exc)

    return {
        "answer": answer,
        "citations": citations,
        "pages_consulted": pages_consulted,
        "has_conflict": has_conflict,
        "qa_path": qa_path,
    }


__all__ = ["ask", "_extract_citations", "_has_conflict_warning"]
