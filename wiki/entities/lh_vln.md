---
id: lh_vln
title: LH-VLN
type: entity
tags: []
confidence: 0.8
created_at: '2026-04-29T23:58:18'
last_reinforced: '2026-04-29T23:58:18'
supersedes: []
sources:
- papers/2601.13976.pdf
source_type: arxiv_paper
---

# LH-VLN

LH-VLN is a benchmark and dataset for **long-horizon Vision-and-Language Navigation** (VLN). It is designed to evaluate agents on sustained navigation tasks that require reasoning over extended sequences, multiple instructions, and complex environments.

## Description

LH-VLN provides a standardized evaluation framework for long-horizon VLN models. The benchmark includes a curated set of tasks that test an agent’s ability to follow natural language instructions over long trajectories, handle perceptual aliasing, and maintain spatial memory across many time steps.

## Capabilities

- Evaluates VLN methods on long-horizon navigation with extended language instructions.
- Serves as the primary testbed for FantasyVLN and similar approaches.
- Supports both simulated and real-world navigation scenarios (paper-specific details may vary).

## Relationships

- **Used by**: FantasyVLN uses LH-VLN for benchmarking and evaluation.

## Source

This page is derived from ArXiv paper 2601.13976, which introduces LH-VLN as part of the FantasyVLN framework.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `LH-VLN` --uses ⚠️--> `FantasyVLN`
