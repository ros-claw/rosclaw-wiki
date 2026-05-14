---
id: td_stp_target_driven_structured_transformer_planner
title: TD-STP (Target-Driven Structured Transformer Planner)
type: algorithm
tags: []
confidence: 0.8
created_at: '2026-04-29T21:14:57'
last_reinforced: '2026-04-29T21:14:57'
supersedes: []
sources:
- papers/2207.11201.pdf
source_type: arxiv_paper
---

# TD-STP (Target-Driven Structured Transformer Planner)

## Overview

TD-STP is a transformer-based planner for vision-language navigation (VLN) that explicitly estimates long-term navigation targets and incorporates room layout into attention for global planning. By jointly reasoning about future waypoints and spatial context, it improves both goal-guided exploration and spatial awareness in complex indoor environments.

## Capabilities

- **Long-horizon goal-guided navigation** — plans over extended sequences by predicting intermediate targets.
- **Room layout-aware navigation** — leverages structured attention over room-level features to adapt to building geometry.
- **Structured global planning** — uses a hierarchical transformer architecture to map language instructions to navigable trajectories.

## Relationships

- **Uses**: Imaginary Scene Tokenization ⚠️, Structured Transformer Planner ⚠️
- **Depends on**: Vision-Language Navigation

## Results

On standard VLN benchmarks, TD-STP achieves a +2% success rate improvement on **R2R** and a +5% improvement on **REVERIE** compared to previous best methods, demonstrating the effectiveness of target-driven structured planning.