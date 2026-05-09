---
id: fsr_vln
title: FSR-VLN
type: algorithm
tags: []
confidence: 0.85
created_at: '2026-04-29T20:52:10'
last_reinforced: '2026-04-30'
supersedes: []
sources:
- papers/2509.13733.pdf
source_type: arxiv_paper
---

## Overview

**FSR-VLN** (Fast-to-Slow Reasoning for Vision-Language Navigation) is a framework that combines a [[Hierarchical Multi-modal Scene Graph]] (HMSG) with [[Fast-to-Slow Navigation Reasoning]] (FSR). Built on a VLM base model, the system first activates a fast matching mechanism for immediate spatial understanding; only when this fast intuition fails does it fall back to slower, more expensive VLM-driven refinement. This hybrid approach dramatically reduces inference latency while maintaining state-of-the-art retrieval success rates.

## Approach

FSR-VLN operates in two stages:

1. **Hierarchical Multi-modal Scene Graph (HMSG)** – A multi-modal map representation that supports progressive retrieval, from coarse room-level localization down to fine-grained goal view and object identification.
2. **Fast-to-Slow Navigation Reasoning (FSR)** – Building on the HMSG, FSR first performs fast matching to efficiently select candidate rooms, views, and objects. When the fast output is uncertain, a VLM-driven refinement step is invoked for final goal selection.

This design trades off a small number of VLM calls for a large overall speed gain, making the system suitable for real‑time robotic deployment.

## Key Capabilities

- **Long‑range spatial reasoning** – capable of interpreting complex, extended environments from tour videos.
- **Reduced inference latency** – achieves an 82% reduction in response time compared to pure VLM‑based methods on tour video benchmarks.
- **State-of-the-art retrieval success rate** – matches or exceeds pure VLM performance.
- **Selective slow reasoning** – activates slow VLM refinement only when fast intuition fails, preserving efficiency.

## Performance

| Metric | Value |
|--------|-------|
| Response time reduction (vs. VLM‑based) | **82%** |
| Retrieval success rate | **State‑of‑the‑art** |

## Architecture

The core components of FSR-VLN are:

1. **[[Hierarchical Multi-modal Scene Graph]]** – a structured representation that pools visual, spatial, and semantic information at multiple granularities.
2. **[[Fast‑to‑Slow Navigation Reasoning]] ⚠️ ⚠️** – a two‑stage inference pipeline that prioritises fast matching (a lightweight learned model) and only invokes a heavy VLM when the fast output is uncertain.

## Integration with Unitree G1

FSR-VLN has been fully integrated with the [[Unitree G1]] humanoid platform. The reasoning outputs are directly fed into the robot's speech, planning, and control stacks, enabling natural‑language querying of visual environments and autonomous navigation actions.

## Relationships

- **`uses`**: [[Hierarchical Multi-modal Scene Graph]], [[Fast‑to‑Slow Navigation Reasoning]] ⚠️ ⚠️
- **`depends_on`**: [[VLM]] ⚠️, [[Unitree G1]]
- **`part_of`**: [[Vision‑Language Navigation]] ⚠️

## Source

The framework is introduced in paper 2509.13733 and demonstrated on tour‑video navigation tasks.