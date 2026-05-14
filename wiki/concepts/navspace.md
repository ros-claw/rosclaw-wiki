---
id: navspace
title: NavSpace
type: concept
tags: []
confidence: 0.95
created_at: '2026-04-30T04:44:26'
last_reinforced: '2026-04-30T04:44:26'
supersedes: []
sources:
- code/TidalHarley_NavSpace/README.md
source_type: official_manual
---

# NavSpace

## Overview

**NavSpace** is a benchmark for evaluating spatial perception and reasoning in instruction-following navigation for embodied agents. It was introduced as the first comprehensive benchmark dedicated to spatial intelligence in embodied navigation, comprising 1,228 trajectory-instruction pairs across six distinct spatial subtasks. NavSpace evaluates 22 different navigation agents to measure their understanding of spatial relationships, viewpoint shifting, vertical perception, and precise movement.

The benchmark leverages Habitat-Sim and the HM3D dataset for simulation and scene data. The baseline model is **SNav**, fine-tuned from LLaVA-Video ⚠️ ⚠️ ⚠️ ⚠️-7B-Qwen2, which achieves state-of-the-art performance on the benchmark.

## Capabilities

- First benchmark for spatial intelligence in embodied navigation
- Evaluates 22 navigation agents across diverse spatial reasoning tasks

## Task Categories

NavSpace defines six subtask categories to probe distinct aspects of spatial understanding:

| Category | Description |
|---|---|
| Environment State | Understanding the current state and layout of the environment |
| Space Structure | Reasoning about the spatial organization of objects and rooms |
| Precise Movement | Following directions that require exact positioning |
| Viewpoint Shifting | Recognizing how the appearance changes from different perspectives |
| Vertical Perception | Understanding height, depth, and elevation changes |
| Spatial Relationship | Comprehending relative positions (e.g., behind, left, under) |

## Action Space

The agent can perform seven discrete actions during navigation:

- `forward` — move forward one step
- `left` — turn left
- `right` — turn right
- `look-up` — tilt camera upward
- `look-down` — tilt camera downward
- `backward` — move backward one step
- `stop` — end navigation

## Data Format

Data in NavSpace is provided in three formats for different stages of processing and evaluation:

- **VLN JSON** — original trajectory-instruction pairs in the standard Vision-and-Language Navigation format
- **action JSON** — sequences of agent actions for reproducibility
- **tokenized JSON** — pre-tokenized versions suitable for transformer-based models

## Baseline Model: SNav

**SNav** (Spatial Navigation) is the proposed baseline model that achieves state-of-the-art results on NavSpace. It is fine-tuned from LLaVA-Video ⚠️ ⚠️ ⚠️ ⚠️-7B-Qwen2, a large multimodal model originally designed for video understanding. SNav leverages spatiotemporal visual features from LLaVA-Video ⚠️ ⚠️ ⚠️ ⚠️ to reason about camera viewpoints and spatial cues in the navigation episodes.

## Relationships

- **Uses**: Habitat-Sim, HM3D, LLaVA-Video ⚠️ ⚠️ ⚠️ ⚠️
- **Depends on**: Habitat-Sim (simulation backend), HM3D (3D scene dataset)