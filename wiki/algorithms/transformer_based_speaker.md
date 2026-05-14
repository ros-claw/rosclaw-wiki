---
id: transformer_based_speaker
title: Transformer-based Speaker
type: algorithm
tags: []
confidence: 0.8
created_at: '2026-04-30T02:05:10'
last_reinforced: '2026-04-30T02:05:10'
supersedes: []
sources:
- papers/2103.00852.pdf
source_type: arxiv_paper
---

# Transformer-based Speaker

**Transformer-based Speaker** is a neural network algorithm within the Double Back-Translation framework. It generates natural language navigation instructions from input path representations (e.g., sequences of waypoints or spatial coordinates).

## Overview

Building on the Transformer architecture Transformer Architecture ⚠️ ⚠️ (Vaswani et al., 2017), the Transformer-based Speaker maps a planned route (typically encoded as a sequence of grid cells or metric coordinates) to a sequence of words describing how to follow that route. It is trained jointly with a **Listener** model as part of the Double Back‑Translation loop, where the Speaker produces instructions that the Listener must reconstruct the original path from. This cycle enforces instruction‑path consistency and improves instruction quality through iterative refinement.

## Capabilities

- Generates navigation instructions from path inputs, bridging the gap between geometric planning and human‑readable language.
- Learns to produce diverse, referentially valid instructions by optimizing via back‑translation.
- Can be adapted to different environment representations (grids, graphs, or continuous coordinates) by changing the input encoding.

## Relationships

- **Part of** → Double Back-Translation
- **Uses** → Transformer Architecture ⚠️ ⚠️ (attention mechanisms for sequence generation)
- **Depends on** → Path representation ⚠️ (input format), Vocabulary ⚠️ (output tokens)
- **Interacts with** → Listener ⚠️ (partner in back‑translation), Navigation instruction dataset ⚠️
- **Implements** → Instruction generation from geometric plans

## Source

- ArXiv paper: *Double Back‑Translation for Vision‑and‑Language Navigation* (2103.00852) – describes the Transformer-based Speaker as a core component of the iterative refinement pipeline.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Transformer-based Speaker` --extends ⚠️--> `Double Back-Translation`
