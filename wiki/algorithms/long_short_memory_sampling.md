---
id: long_short_memory_sampling
title: Long-Short Memory Sampling
type: algorithm
tags: []
confidence: 0.8
created_at: '2026-04-30T00:17:15'
last_reinforced: '2026-04-30T00:17:15'
supersedes: []
sources:
- papers/2506.17221.pdf
source_type: arxiv_paper
---

# Long-Short Memory Sampling

## Overview

**Long-Short Memory Sampling** is a memory sampling algorithm designed to balance historical and current observations during training. It enables effective learning by drawing samples from both long-term memory (storing past experiences) and short-term memory (capturing recent observations), thus maintaining a robust distribution of training data across time.

## Purpose

The primary purpose of Long-Short Memory Sampling is to prevent catastrophic forgetting and improve sample efficiency in sequential decision-making tasks. By mixing old and new observations, the algorithm ensures that the model does not overfit to recent data while still adapting to new scenarios.

## Capabilities

- **Balanced observation usage**: Combines long-term historical data with short-term current observations in a single training batch.
- **Effective training**: Facilitates stable and efficient training of models that rely on temporally extended contexts, particularly in navigation and reinforcement learning settings.

## Relationships

- **Used by** → VLN-R1: The algorithm is employed by the Vision-Language Navigation model VLN-R1 to sample training trajectories from its memory buffers, allowing it to learn from both past episodes and ongoing interactions.

---

*This page is part of the ROSClaw Wiki. See also: Memory Sampling ⚠️, Training ⚠️, Vision-Language Navigation.*

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Long-Short Memory Sampling` --extends ⚠️--> `VLN-R1`
