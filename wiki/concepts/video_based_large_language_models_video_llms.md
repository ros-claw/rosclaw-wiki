---
id: video_based_large_language_models_video_llms
title: Video-based Large Language Models (Video-LLMs)
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-30T00:36:31'
last_reinforced: '2026-04-30T00:36:31'
supersedes: []
sources:
- papers/2507.05240.pdf
source_type: arxiv_paper
---

## Video-based Large Language Models (Video-LLMs)

**Video-based Large Language Models (Video-LLMs)** are a class of foundation models that extend the language understanding of Large Language Models (LLMs) to dynamic visual inputs — specifically, video streams. By aligning temporally-encoded video representations with text embeddings, Video-LLMs can process sequential frames alongside natural language instructions, enabling tasks that require both visual perception over time and linguistic reasoning.

### Capabilities

- **Process video streams and language instructions**  
  Video-LLMs accept continuous video (or sampled frames) and accompanying text prompts, producing coherent responses grounded in the visual-temporal content.
- **Drive progress in Vision-and-Language Navigation tasks**  
  In embodied settings such as Vision-and-Language Navigation (VLN) ⚠️, these models allow agents to interpret real-time camera feeds and follow high-level linguistic commands, bridging the gap between perception and action.

### Relationships

- **Used by**: StreamVLN — the StreamVLN framework leverages Video-LLMs as its core perception backbone, using them to encode video observations and generate navigation decisions conditioned on language instructions.

### Relevant Concepts

- Vision-Language Models (VLMs) ⚠️
- Embodied AI
- Temporal Video Understanding ⚠️
- Large Language Models (LLMs)

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Video-based Large Language Models (Video-LLMs)` --related_to ⚠️ ⚠️--> `Embodied AI`
- `Video-based Large Language Models (Video-LLMs)` --applies_to ⚠️--> `Large Language Models (LLMs)`
**Pending review:**
- `Video-based Large Language Models (Video-LLMs)` --related_to ⚠️ ⚠️--> `StreamVLN` _(wikilink)_
