---
id: spatial_temporal_aware_transformer_start
title: Spatial-Temporal Aware Transformer (START)
type: algorithm
tags: []
confidence: 0.8
created_at: '2026-04-29T20:34:29'
last_reinforced: '2026-04-29T20:34:29'
supersedes: []
sources:
- papers/2603.16166.json
source_type: arxiv_paper
---

# Spatial-Temporal Aware Transformer (START)

**START** is a transformer-based algorithm designed for end-to-end decision-making in the Sign Navigation (SignNav) task. It interprets semantic hints from physical signage and enables real-world deployment without reliance on pre-built maps.

## Architecture

START consists of two core modules:

- **Spatial-Aware Module**: Grounds semantic hints from signage into the physical world, mapping visual cues to actionable spatial information.
- **Temporal-Aware Module**: Captures long-range dependencies between historical states and the current observation, enabling coherent navigation over time.

The combination allows the model to understand both where to look and how past decisions influence future actions.

## Training Strategy

START employs a **two-stage training** procedure using **Dataset Aggregation (DAgger)**. This interactive imitation learning approach iteratively collects expert demonstrations on the policy's own state distribution, improving robustness and generalization.

## Performance

| Metric | Value (val-unseen split) |
|--------|---------------------------|
| Success Rate (SR) | 80% |
| Normalized Dynamic Time Warping (NDTW) | 0.74 |

Real-world deployment confirms the algorithm's practicality, successfully navigating environments with signage without any pre-built map.

## Capabilities

- End-to-end decision-making for SignNav
- Interprets semantic hints from signage
- Works in real-world deployment without pre-built maps
- Achieves state-of-the-art results on the SignNav benchmark

## Relationships

- **uses**: Dataset Aggregation (DAgger)
- **depends_on**: spatial grounding ⚠️, temporal dependencies ⚠️

## Related Pages

- SignNav
- Dataset Aggregation (DAgger)
- Spatial Grounding ⚠️
- Temporal Dependencies ⚠️

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Spatial-Temporal Aware Transformer (START)` --based_on ⚠️--> `SignNav`
- `Spatial-Temporal Aware Transformer (START)` --extends ⚠️--> `Dataset Aggregation (DAgger)`
