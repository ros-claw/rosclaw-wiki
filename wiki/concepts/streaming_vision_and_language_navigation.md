---
id: streaming_vision_and_language_navigation
title: Streaming Vision-and-Language Navigation
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-29T20:55:04'
last_reinforced: '2026-04-29T20:55:04'
supersedes: []
sources:
- papers/2507.05240.pdf
source_type: arxiv_paper
---

## Streaming Vision-and-Language Navigation

**Streaming Vision-and-Language Navigation (Streaming VLN)** is a paradigm for embodied agents that operate in real-world environments, processing continuous visual streams and generating actions with low latency, all grounded in natural language instructions.

### Overview

Traditional [[Vision-and-Language Navigation (VLN)]] ⚠️ often assumes discrete snapshots or static observations. In contrast, Streaming VLN addresses the challenge of continuous perception and action in dynamic real-world settings. Agents must interpret a constant video feed while executing movement commands derived from human language, requiring tight integration of perception, reasoning, and control under strict latency constraints.

### Task Definition

- **Goal**: Agents process continuous visual streams and generate actions with low latency, grounded in language instructions.
- **Core requirement**: Real-time responsiveness to changes in the environment while maintaining alignment with the given language command.

### Capabilities

- Real-world navigation requires processing continuous visual streams (e.g., from an onboard camera), rather than discrete frames.
- Low latency action generation is essential to avoid collisions, handle moving obstacles, and react to instruction corrections.

### Implemented By

- **[[StreamVLN]]** — a specific system or framework that realizes the Streaming VLN paradigm.

### Uses

- **[[Video-LLMs]]** — large language models trained on video data, which can process continuous visual input and generate language-grounded outputs for action selection.

### Related Concepts

- [[Embodied AI]] — the broader field of agents that perceive and act in physical environments.
- [[Sim-to-Real Transfer]] — techniques to bridge simulated training and real-world deployment, relevant to Streaming VLN's low-latency requirements.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Streaming Vision-and-Language Navigation` --[[applies_to]] ⚠️--> `Video-LLMs`
**Pending review:**
- `Streaming Vision-and-Language Navigation` --[[related_to]] ⚠️--> `StreamVLN` _(wikilink)_
