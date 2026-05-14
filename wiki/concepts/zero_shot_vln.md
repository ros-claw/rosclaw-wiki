---
id: zero_shot_vln
title: Zero-shot VLN
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-30T02:18:36'
last_reinforced: '2026-04-30T02:18:36'
supersedes: []
sources:
- papers/2211.16649.pdf
source_type: arxiv_paper
---

# Zero-shot VLN

**Zero-shot VLN** is a paradigm in Vision-Language Navigation (VLN) where an agent performs navigation tasks without any task-specific fine-tuning. Instead of relying on supervised training on navigation datasets, zero-shot VLN leverages pre-trained Vision-Language Models ⚠️ (VLMs) and general world knowledge to follow natural-language instructions in unseen environments.

This approach extends VLN ⚠️ (implements `extends`) by removing the requirement for expensive, domain-specific training data. The core capability is **VLN without task-specific fine-tuning**, enabled by strong multimodal alignment and embodied reasoning from large-scale pretraining.

The concept is explored in the paper *"Towards Zero-Shot Vision-Language Navigation"* (arXiv:2211.16649 ⚠️), which demonstrates that agents can generalize to new instructions and scenes zero-shot by combining pre-trained components like CLIP or GPT-based Scene Graph ⚠️ with classical sim-to-real techniques.

Key ideas include:
- Using a frozen VLM ⚠️ for instruction–scene grounding.
- Repurposing language models for high-level planning (LLM-as-Planner ⚠️).
- Exploiting Embodied AI knowledge without fine-tuning.

Zero-shot VLN is closely related to Open-Vocabulary Navigation ⚠️ and Generalist Embodied Agents ⚠️ concepts.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Zero-shot VLN` --related_to ⚠️ ⚠️--> `Embodied AI`
**Pending review:**
- `Zero-shot VLN` --related_to ⚠️ ⚠️--> `CLIP` _(wikilink)_
