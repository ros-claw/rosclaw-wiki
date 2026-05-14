---
id: video_llms
title: Video-LLMs
type: entity
tags: []
confidence: 0.8
created_at: '2026-04-29T20:54:53'
last_reinforced: '2026-04-29T20:54:53'
supersedes: []
sources:
- papers/2507.05240.pdf
source_type: arxiv_paper
---

# Video-LLMs

**Video-LLMs** (Video-based Large Language Models) are a class of multimodal foundation models that process both video frames and natural language inputs, enabling understanding of temporal dynamics across visual sequences. These models extend traditional LLMs by incorporating visual encoders, temporal alignment modules, and cross-modal fusion mechanisms to handle the spatiotemporal structure of video data.

## Role

Video-LLMs serve as the backbone for current vision-and-language navigation (VLN) methods, but face inherent trade-offs among fine-grained visual understanding, long-term context modeling, and computational efficiency. In streaming navigation scenarios, the model must continuously interpret real-time video feeds while maintaining memory of past observations—a challenge that Video-LLMs address through architectures such as stream buffers, token compression, or frame selection strategies.

## Capabilities

- Drive recent progress in Vision-and-Language Navigation (VLN) ⚠️ by providing a unified framework for perceiving visual environments and grounding language instructions.
- Enable zero-shot generalization to unseen environments when trained on large-scale video-language datasets.
- Support interactive, real-time navigation through natural language commands in embodied agents.

## Relationships

- **Used by**: StreamVLN — StreamVLN leverages Video-LLMs as its core reasoning engine to perform streaming vision-and-language navigation.
- **Related to**: Streaming Vision-and-Language Navigation — Video-LLMs provide the multimodal understanding necessary for agents to navigate while processing continuous video input on-the-fly.

## Key Characteristics

| Aspect | Description |
|--------|-------------|
| Modality | Video + text (can include audio in some variants) |
| Temporal resolution | Handles sequences of frames (short to long clips) |
| Common architectures | Visual encoder (e.g., ViT) → temporal aggregator → LLM decoder |
| Key challenge | Balancing frame count, memory usage, and inference latency |

## Limitations

- High computational cost for long video sequences.
- Difficulty capturing fine-grained object interactions across many frames.
- Trade-off between maintaining long-term context and real-time inference speed (central to StreamVLN research).

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Video-LLMs` --uses ⚠️--> `StreamVLN`
