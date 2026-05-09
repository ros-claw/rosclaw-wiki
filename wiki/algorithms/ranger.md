---
id: ranger
title: RANGER
type: algorithm
tags: []
confidence: 0.8
created_at: '2026-04-29T21:29:03'
last_reinforced: '2026-04-29T21:29:03'
supersedes: []
sources:
- papers/2512.24212.pdf
source_type: arxiv_paper
---

# RANGER

**Type:** Algorithm  
**Tags:** `zero-shot`, `open-vocabulary`, `navigation`, `visual-in-context-learning`, `VLM`

**RANGER** is a zero-shot, open-vocabulary semantic navigation framework that operates using only a monocular camera, eliminating the need for ground-truth depth, pose sensors, or environment-specific training. It leverages **[[3D foundation models]] ⚠️ ⚠️** and **visual in-context learning** to adapt to unseen environments from a short traversal video.

## Overview

RANGER achieves **open-vocabulary object goal navigation** (ObjectNav) without any prior knowledge of the target environment. The agent receives a brief video of the environment (recorded at human walking speed) and learns to navigate to any specified object category described in natural language. The system relies entirely on **monocular camera input** and performs **keyframe-based 3D reconstruction** to build a **semantic point cloud**, which is then used by a **Vision-Language Model (VLM)** to plan exploration and select waypoints.

## Components

The framework integrates five main components:

1. **Keyframe-based 3D reconstruction** – Extracts geometrically and semantically meaningful keyframes from the input video to reconstruct a sparse 3D representation of the environment.
2. **Semantic point cloud generation** – Projects 2D semantic features from the VLM onto the 3D point cloud, creating a semantically annotated map.
3. **VLM-driven exploration value estimation** – Uses a VLM to evaluate the exploration value of candidate viewpoints by reasoning over the semantic point cloud and the target object description.
4. **High-level adaptive waypoint selection** – Chooses the next-best waypoint based on exploration values, balancing coverage and goal-relevance.
5. **Low-level action execution** – Translates selected waypoints into motor commands to navigate the robot through the environment.

## Dependencies & Evaluation

- **Depends on:** [[HM3D benchmark]] ⚠️ for quantitative evaluation.
- **Uses:** [[3D foundation models]] ⚠️ ⚠️ (e.g., DUSt3R, MASt3R), [[Vision-Language Model (VLM)]] (e.g., LLaVA, GPT-4V), and standard depth-free reconstruction pipelines.

## Experiments

RANGER was evaluated on the **HM3D benchmark** and in real-world environments. It achieved competitive navigation success rates and exploration efficiency compared to fully-supervised baselines, despite having no access to depth or pose sensors and no environment-specific training. The zero-shot generalization across diverse indoor scenes demonstrates the effectiveness of visual in-context learning for embodied navigation.

## Key Properties

| Property | Value |
|----------|-------|
| Modality | Monocular camera only |
| Dependency on depth/pose | None |
| Environment prior | None (zero-shot) |
| Input | Short video of target environment |
| Goal specification | Open-vocabulary natural language |

## Related Pages

- [[Object Goal Navigation]]
- [[Zero-shot Navigation]]
- [[Visual In-Context Learning]] ⚠️
- [[Semantic Point Cloud]] ⚠️
- [[3D Foundation Models]] ⚠️
- [[Vision-Language Model (VLM)]]

## References

- ArXiv paper: *RANGER: Zero-shot Open-vocabulary Object Goal Navigation using Visual In-context Learning* (arXiv:2512.24212)

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `RANGER` --[[based_on]] ⚠️--> `Vision-Language Model (VLM)`
