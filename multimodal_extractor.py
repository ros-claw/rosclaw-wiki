"""ROSClaw Multimodal Extractor — figure/table extraction and visual understanding.

Extracts images, diagrams, and tables from PDFs, then analyzes them with
vision-capable LLMs to produce structured technical descriptions.
"""

from __future__ import annotations

import base64
import io
import json
import logging
import os
import re
from pathlib import Path
from typing import Any

try:
    import fitz  # PyMuPDF
except ImportError:
    fitz = None  # type: ignore[assignment]

try:
    import requests
except ImportError:
    requests = None  # type: ignore[assignment]

import wiki_engine as engine

logger = logging.getLogger("rosclaw.multimodal")

# ── Cost-control thresholds ──

_MERGE_THRESHOLD = 0.7

_TECH_KEYWORDS: set[str] = {
    "architecture",
    "framework",
    "pipeline",
    "algorithm",
    "result",
    "comparison",
    "table",
    "system",
    "overview",
    "model",
    "structure",
    "diagram",
    "flow",
    "network",
    "module",
    "component",
    "design",
    "configuration",
    "setup",
    "experimental",
    "evaluation",
    "performance",
    "accuracy",
    "metric",
}

_VISION_PROMPT = (
    "你是一位具身智能与机器人学专家。请分析这张图表，输出以下结构化信息：\n"
    "1. 图表类型：架构图 / 实验对比图 / 算法流程图 / 数据表 / 其他\n"
    "2. 核心内容：图表展示什么技术/实验/逻辑\n"
    "3. 对机器人研究的具体贡献：这张图说明了什么关键发现、算法细节或硬件设计\n"
    "4. 可提取的参数（如有）：所有数值、阈值、配置\n"
    "5. 关键词标签：5-10 个技术关键词\n"
    "严禁输出“图中有一个坐标轴”这类空泛描述。必须挖掘技术实质。\n"
    "Return ONLY valid JSON with keys: type, core_content, contribution, parameters (dict), tags (list)."
)

# ── Figure extraction ──


def extract_figures_from_pdf(pdf_path: str, arxiv_id: str = "") -> list[dict[str, Any]]:
    """Extract figure/table metadata with bounding boxes from a PDF.

    Uses PyMuPDF to locate images and their associated captions.

    Returns:
        List of dicts with keys: id, page_num, fig_num, caption, bbox, xref.
    """
    if fitz is None:
        raise RuntimeError("PyMuPDF not installed")

    doc = fitz.open(pdf_path)
    figures: list[dict[str, Any]] = []

    for page_num in range(len(doc)):
        page = doc[page_num]

        # 1. Find caption text blocks
        blocks = page.get_text("blocks")
        caption_blocks: list[tuple[float, float, float, float, str]] = []
        for b in blocks:
            x0, y0, x1, y1, text, *_ = b
            if re.search(r"\b(Fig(?:ure)?|Table)\s*\d+[.:]?", text, re.I):
                caption_blocks.append((x0, y0, x1, y1, text.strip()))

        # 2. Find images on the page
        img_list = page.get_images(full=True)

        if img_list:
            for img_index, img in enumerate(img_list):
                xref = img[0]
                img_rects = page.get_image_rects(xref)

                for rect in img_rects:
                    # Find nearest caption (typically below the image)
                    best_caption = ""
                    best_dist = float("inf")
                    for cx0, cy0, cx1, cy1, ctext in caption_blocks:
                        if cy0 > rect.y1:
                            dist = cy0 - rect.y1
                            if dist < best_dist:
                                best_dist = dist
                                best_caption = ctext

                    fig_num_match = re.search(
                        r"\b(?:Fig(?:ure)?|Table)\s*(\d+)", best_caption, re.I
                    )
                    fig_num = fig_num_match.group(1) if fig_num_match else str(img_index + 1)

                    fig_id = (
                        f"{arxiv_id}_{page_num + 1}_{fig_num}"
                        if arxiv_id
                        else f"page{page_num + 1}_{fig_num}"
                    )

                    figures.append({
                        "id": fig_id,
                        "page_num": page_num + 1,
                        "fig_num": fig_num,
                        "caption": best_caption,
                        "bbox": (rect.x0, rect.y0, rect.x1, rect.y1),
                        "xref": xref,
                    })
        elif caption_blocks:
            # Fallback: no embedded images but captions exist (vector figures, etc.)
            for cb_index, (cx0, cy0, cx1, cy1, ctext) in enumerate(caption_blocks):
                fig_num_match = re.search(
                    r"\b(?:Fig(?:ure)?|Table)\s*(\d+)", ctext, re.I
                )
                fig_num = fig_num_match.group(1) if fig_num_match else str(cb_index + 1)

                fig_id = (
                    f"{arxiv_id}_{page_num + 1}_{fig_num}"
                    if arxiv_id
                    else f"page{page_num + 1}_{fig_num}"
                )

                figures.append({
                    "id": fig_id,
                    "page_num": page_num + 1,
                    "fig_num": fig_num,
                    "caption": ctext,
                    "bbox": (cx0, cy0, cx1, cy1),
                    "xref": 0,
                })

    doc.close()
    return figures


def render_figure_region(
    pdf_path: str,
    page_num: int,
    bbox: tuple[float, float, float, float],
    zoom: float = 2.0,
) -> bytes:
    """Render a specific region of a PDF page to PNG bytes."""
    if fitz is None:
        raise RuntimeError("PyMuPDF not installed")

    doc = fitz.open(pdf_path)
    page = doc[page_num - 1]
    rect = fitz.Rect(bbox)
    # Expand slightly for context
    margin = 10
    rect = fitz.Rect(
        max(0, rect.x0 - margin),
        max(0, rect.y0 - margin),
        min(page.rect.width, rect.x1 + margin),
        min(page.rect.height, rect.y1 + margin),
    )
    mat = fitz.Matrix(zoom, zoom)
    pix = page.get_pixmap(matrix=mat, clip=rect)
    png_bytes = pix.tobytes("png")
    doc.close()
    return png_bytes


# ── Cost control ──


def should_analyze_figure(figure_meta: dict[str, Any], page_confidence: float = 0.5) -> bool:
    """Return True if the figure warrants a vision-model call.

    Criteria:
        1. Wiki page confidence >= 0.7
        2. Caption contains at least one technical keyword.
    """
    if page_confidence < _MERGE_THRESHOLD:
        return False
    caption_lower = figure_meta.get("caption", "").lower()
    return any(kw in caption_lower for kw in _TECH_KEYWORDS)


# ── Vision model backends ──


def _encode_image(image_bytes: bytes) -> str:
    return base64.b64encode(image_bytes).decode("ascii")


def _parse_vision_json(text: str) -> dict[str, Any]:
    """Clean markdown fences and parse JSON from vision model output."""
    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.split("```json")[-1].split("```")[0].strip()
    try:
        return json.loads(cleaned)
    except Exception:
        return {
            "type": "其他",
            "core_content": text[:800],
            "contribution": "",
            "parameters": {},
            "tags": [],
        }


def _call_claude_vision(image_b64: str, api_key: str | None = None) -> dict[str, Any]:
    """Call Claude 3.5 Sonnet Vision API."""
    key = api_key or os.environ.get("ANTHROPIC_API_KEY")
    if not key:
        raise RuntimeError("ANTHROPIC_API_KEY not set")
    if requests is None:
        raise RuntimeError("requests library not installed")

    model = os.environ.get("ANTHROPIC_VISION_MODEL", "claude-3-5-sonnet-20241022")
    url = "https://api.anthropic.com/v1/messages"
    headers = {
        "x-api-key": key,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json",
    }
    payload = {
        "model": model,
        "max_tokens": 4096,
        "temperature": 0.2,
        "messages": [{
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": "image/png",
                        "data": image_b64,
                    },
                },
                {"type": "text", "text": _VISION_PROMPT},
            ],
        }],
    }

    resp = requests.post(url, headers=headers, json=payload, timeout=120)
    resp.raise_for_status()
    data = resp.json()
    text = data["content"][0]["text"]
    return _parse_vision_json(text)


def _call_openai_vision(image_b64: str, api_key: str | None = None) -> dict[str, Any]:
    """Call GPT-4o Vision API."""
    key = api_key or os.environ.get("OPENAI_API_KEY")
    if not key:
        raise RuntimeError("OPENAI_API_KEY not set")
    if requests is None:
        raise RuntimeError("requests library not installed")

    model = os.environ.get("OPENAI_VISION_MODEL", "gpt-4o")
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "authorization": f"Bearer {key}",
        "content-type": "application/json",
    }
    payload = {
        "model": model,
        "temperature": 0.2,
        "max_tokens": 4096,
        "messages": [{
            "role": "user",
            "content": [
                {"type": "text", "text": _VISION_PROMPT},
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/png;base64,{image_b64}"},
                },
            ],
        }],
    }

    resp = requests.post(url, headers=headers, json=payload, timeout=120)
    resp.raise_for_status()
    data = resp.json()
    text = data["choices"][0]["message"]["content"]
    return _parse_vision_json(text)


def analyze_figure(
    image_bytes: bytes,
    backend: str | None = None,
    api_key: str | None = None,
) -> dict[str, Any]:
    """Analyze a figure image using a vision model.

    Args:
        image_bytes: Raw PNG/JPEG bytes.
        backend: "anthropic", "openai", or auto-detect from env.
        api_key: Optional API key override.

    Returns:
        Parsed JSON dict with type, core_content, contribution, parameters, tags.
    """
    image_b64 = _encode_image(image_bytes)

    if backend is None:
        if os.environ.get("ANTHROPIC_API_KEY"):
            backend = "anthropic"
        elif os.environ.get("OPENAI_API_KEY"):
            backend = "openai"
        else:
            raise RuntimeError(
                "No vision backend configured. Set ANTHROPIC_API_KEY or OPENAI_API_KEY."
            )

    if backend == "anthropic":
        return _call_claude_vision(image_b64, api_key)
    if backend == "openai":
        return _call_openai_vision(image_b64, api_key)
    raise ValueError(f"Unknown vision backend: {backend}")


# ── High-level orchestration ──


def extract_and_analyze_pdf_figures(
    pdf_path: str,
    arxiv_id: str = "",
    page_confidence: float = 0.5,
    vision_backend: str | None = None,
    max_figures: int = 20,
) -> list[dict[str, Any]]:
    """Extract figures from PDF and analyze them with vision model.

    Args:
        pdf_path: Path to the PDF file.
        arxiv_id: arXiv ID for figure ID generation.
        page_confidence: Confidence threshold for cost control.
        vision_backend: Vision model backend (anthropic/openai).
        max_figures: Max number of figures to analyze (safety limit).

    Returns:
        List of figure analysis results.
    """
    figures = extract_figures_from_pdf(pdf_path, arxiv_id)
    results: list[dict[str, Any]] = []

    for fig in figures[:max_figures]:
        fig_result = {
            "id": fig["id"],
            "page_num": fig["page_num"],
            "fig_num": fig["fig_num"],
            "caption": fig["caption"],
            "analyzed": False,
            "analysis": {},
        }

        if should_analyze_figure(fig, page_confidence):
            try:
                png_bytes = render_figure_region(
                    pdf_path, fig["page_num"], fig["bbox"]
                )
                analysis = analyze_figure(png_bytes, backend=vision_backend)
                fig_result["analyzed"] = True
                fig_result["analysis"] = analysis
            except Exception as exc:
                logger.warning("Vision analysis failed for %s: %s", fig["id"], exc)
                fig_result["analysis"] = {"error": str(exc)}
        else:
            fig_result["analysis"] = {
                "skipped": "did not meet cost control criteria (confidence<0.7 or no tech keywords)"
            }

        results.append(fig_result)

    return results


def write_figure_analysis_to_page(
    wiki_page_path: str,
    figure_results: list[dict[str, Any]],
) -> None:
    """Append or replace figure analysis on a wiki page.

    Inserts/updates a `### 📊 图表分析` section.
    """
    page_path = Path(wiki_page_path)
    if not page_path.exists():
        raise FileNotFoundError(f"Wiki page not found: {wiki_page_path}")

    content = page_path.read_text(encoding="utf-8")
    meta, body = engine.parse_frontmatter(content)

    lines: list[str] = ["### 📊 图表分析"]

    for fig in figure_results:
        fig_num = fig.get("fig_num", "?")
        caption = fig.get("caption", "Untitled")
        analysis = fig.get("analysis", {})

        lines.append(f"\n#### Figure {fig_num}：{caption}")

        if analysis.get("skipped"):
            lines.append(f"**状态**：跳过（{analysis['skipped']}）")
            continue
        if analysis.get("error"):
            lines.append(f"**状态**：分析失败 — {analysis['error']}")
            continue

        lines.append(f"**类型**：{analysis.get('type', '未知')}")
        lines.append(f"**核心发现**：{analysis.get('core_content', '')}")
        if analysis.get("contribution"):
            lines.append(f"**技术贡献**：{analysis['contribution']}")
        if analysis.get("parameters"):
            params = ", ".join(
                f"{k}={v}" for k, v in analysis["parameters"].items()
            )
            lines.append(f"**参数**：{params}")
        if analysis.get("tags"):
            lines.append(f"**关键词**：{', '.join(analysis['tags'])}")

    analysis_section = "\n".join(lines)

    if "### 📊 图表分析" in body:
        pattern = re.compile(
            r"### 📊 图表分析.*?(?=\n## |\n### |\Z)", re.DOTALL
        )
        body = pattern.sub(analysis_section, body)
    else:
        body = body.rstrip() + "\n\n" + analysis_section + "\n"

    page_path.write_text(engine.write_frontmatter(meta, body), encoding="utf-8")
    logger.info(
        "Updated figure analysis on %s (%d figures)",
        page_path,
        len(figure_results),
    )


# ── Utility ──


def is_multimodal_available() -> bool:
    """Return True if vision backend is configured."""
    return bool(
        os.environ.get("ANTHROPIC_API_KEY") or os.environ.get("OPENAI_API_KEY")
    )


__all__ = [
    "extract_figures_from_pdf",
    "render_figure_region",
    "should_analyze_figure",
    "analyze_figure",
    "extract_and_analyze_pdf_figures",
    "write_figure_analysis_to_page",
    "is_multimodal_available",
]
