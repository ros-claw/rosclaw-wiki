"""ROSClaw Fragment Detector — identify scattered information about the same topic.

Uses semantic similarity to detect when a single concept is fragmented
across multiple wiki pages.
"""

from __future__ import annotations

import difflib
import logging
from pathlib import Path
from typing import Any

import wiki_engine as engine
from entity_resolver import find_candidate_entities

logger = logging.getLogger("rosclaw.fragment")

_FRAGMENT_SIM_THRESHOLD = 0.7


def detect_fragmentation(entity_name: str, wiki_root: str) -> list[dict[str, Any]]:
    """Find pages that are semantically similar and scattered across the wiki.

    Searches for pages that mention ``entity_name`` (by title or body),
    then clusters them by semantic similarity. If 3+ pages cluster with
    similarity > 0.7, they are returned as fragments.

    Returns:
        List of fragment page dicts (path, title, body_preview) if >= 3
        fragments found; otherwise empty list.
    """
    root = Path(wiki_root)
    query_lower = entity_name.lower()

    # 1. Collect candidate pages via entity_resolver + body search
    candidates = find_candidate_entities(entity_name, wiki_root)

    seen_paths: set[str] = set()
    all_pages: list[dict[str, Any]] = []

    for c in candidates:
        path = c.get("path", "")
        if path and path not in seen_paths:
            seen_paths.add(path)
            page_path = root / path
            if page_path.exists():
                try:
                    content = page_path.read_text(encoding="utf-8")
                    meta, body = engine.parse_frontmatter(content)
                    all_pages.append({
                        "path": path,
                        "title": meta.get("title", page_path.stem),
                        "body": body[:2000],
                    })
                except Exception:
                    pass

    # Also search by body content mention
    for md_file in root.rglob("*.md"):
        if md_file.name in ("index.md", "log.md", "Admin_Dashboard.md"):
            continue
        rel = str(md_file.relative_to(root))
        if rel in seen_paths:
            continue
        try:
            content = md_file.read_text(encoding="utf-8")
            meta, body = engine.parse_frontmatter(content)
            title = meta.get("title", md_file.stem)
            title_lower = title.lower()
            body_lower = body.lower()
            # Relaxed matching: all query words appear in title or body
            query_words = query_lower.split()
            matched = query_lower in title_lower or query_lower in body_lower
            if not matched and query_words:
                matched = all(
                    word in title_lower or word in body_lower for word in query_words
                )
            if matched:
                seen_paths.add(rel)
                all_pages.append({
                    "path": rel,
                    "title": title,
                    "body": body[:2000],
                })
        except Exception:
            continue

    if len(all_pages) < 3:
        return []

    # 2. Compute pairwise similarity (semantic first, fallback to difflib)
    try:
        import numpy as np
        from sentence_transformers import SentenceTransformer

        model = SentenceTransformer("all-MiniLM-L6-v2")
        texts = [f"{p['title']}\n{p['body']}" for p in all_pages]
        embeddings = model.encode(texts, show_progress_bar=False)

        norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
        embeddings_norm = embeddings / (norms + 1e-10)
        sim_matrix = np.dot(embeddings_norm, embeddings_norm.T)

        n = len(all_pages)
        for i in range(n):
            cluster = [i]
            for j in range(n):
                if i != j and sim_matrix[i, j] > _FRAGMENT_SIM_THRESHOLD:
                    cluster.append(j)
            if len(cluster) >= 3:
                return [all_pages[idx] for idx in cluster[:5]]
    except Exception:
        pass

    # Fallback: difflib
    n = len(all_pages)
    for i in range(n):
        cluster = [i]
        for j in range(n):
            if i != j:
                text_i = f"{all_pages[i]['title']} {all_pages[i]['body']}"
                text_j = f"{all_pages[j]['title']} {all_pages[j]['body']}"
                sim = difflib.SequenceMatcher(
                    None, text_i.lower(), text_j.lower()
                ).ratio()
                if sim > _FRAGMENT_SIM_THRESHOLD:
                    cluster.append(j)
        if len(cluster) >= 3:
            return [all_pages[idx] for idx in cluster[:5]]

    return []


def generate_consolidation_prompt(entity_name: str, fragments: list[dict[str, Any]]) -> str:
    """Generate an LLM prompt for merging fragmented pages."""
    parts = [
        "你是一位知识库整理专家。以下多个 Wiki 页面包含了关于同一主题"
        f"'{entity_name}' 的碎片化信息。请将它们整合为一个统一、结构清晰的专题页面。\n\n"
    ]
    for i, frag in enumerate(fragments, 1):
        parts.append(f"--- 页面 {i}: {frag['title']} ({frag['path']}) ---\n")
        parts.append(frag["body"][:1500])
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
    return "".join(parts)


def dedup_information(wiki_root: str, similarity_threshold: float = 0.85) -> list[dict[str, Any]]:
    """Find different wiki pages with highly similar body content.

    Uses vector semantic similarity (with difflib fallback) to identify
    potential duplicate pages.

    Returns:
        List of duplicate pairs with similarity score.
    """
    root = Path(wiki_root)
    pages: list[dict[str, Any]] = []

    for md_file in root.rglob("*.md"):
        if md_file.name in ("index.md", "log.md", "Admin_Dashboard.md"):
            continue
        try:
            content = md_file.read_text(encoding="utf-8")
            meta, body = engine.parse_frontmatter(content)
            pages.append({
                "path": str(md_file.relative_to(root)),
                "title": meta.get("title", md_file.stem),
                "body": body,
            })
        except Exception:
            continue

    duplicates: list[dict[str, Any]] = []
    n = len(pages)

    # Try semantic comparison first
    try:
        import numpy as np
        from sentence_transformers import SentenceTransformer

        model = SentenceTransformer("all-MiniLM-L6-v2")
        texts = [f"{p['title']}\n{p['body']}" for p in pages]
        embeddings = model.encode(texts, show_progress_bar=False)
        norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
        embeddings_norm = embeddings / (norms + 1e-10)
        sim_matrix = np.dot(embeddings_norm, embeddings_norm.T)

        for i in range(n):
            for j in range(i + 1, n):
                sim = float(sim_matrix[i, j])
                if sim >= similarity_threshold:
                    duplicates.append({
                        "page_a": pages[i]["path"],
                        "title_a": pages[i]["title"],
                        "page_b": pages[j]["path"],
                        "title_b": pages[j]["title"],
                        "similarity": round(sim, 3),
                        "method": "semantic",
                    })
    except Exception:
        # Fallback to difflib
        for i in range(n):
            for j in range(i + 1, n):
                sim = difflib.SequenceMatcher(
                    None,
                    pages[i]["body"].lower(),
                    pages[j]["body"].lower(),
                ).ratio()
                if sim >= similarity_threshold:
                    duplicates.append({
                        "page_a": pages[i]["path"],
                        "title_a": pages[i]["title"],
                        "page_b": pages[j]["path"],
                        "title_b": pages[j]["title"],
                        "similarity": round(sim, 3),
                        "method": "difflib",
                    })

    duplicates.sort(key=lambda x: x["similarity"], reverse=True)
    return duplicates


__all__ = [
    "detect_fragmentation",
    "generate_consolidation_prompt",
    "dedup_information",
]
