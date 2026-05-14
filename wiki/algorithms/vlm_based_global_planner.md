---
id: vlm_based_global_planner
title: VLM-based Global Planner
type: algorithm
tags: []
confidence: 0.8
created_at: '2026-04-29T20:51:46'
last_reinforced: '2026-04-29T20:51:46'
supersedes: []
sources:
- papers/2512.08186.pdf
source_type: arxiv_paper
---

# VLM-based Global Planner

## Overview

The **VLM-based Global Planner** is a high-level reasoning module that acts as **System 2** within the DualVLN architecture (part_of). It leverages vision-language models ⚠️ ⚠️ ⚠️ (uses) to perform image-grounded reasoning and generate mid-term waypoint goals for embodied navigation tasks.

## Description

In DualVLN, the VLM-based Global Planner is responsible for deliberative, slower-paced planning. It takes in visual observations from the environment and, through grounding with natural language instructions, predicts explicit pixel-level waypoints and latent feature representations. These outputs are passed to the System 1 component (the VLA-based Local Controller ⚠️) as goals and conditioning signals, enabling robust closed-loop control.

## Capabilities

- **Predicts mid-term waypoint goals**: Instead of low-level actions, the planner outputs intermediate spatial targets that guide the robot over moderate horizons.
- **Performs image-grounded reasoning**: Uses visual context and language directives to resolve ambiguities, handle unseen obstacles, or adapt to instruction phrasing.
- **Provides explicit pixel goals and latent features** to System 1 (local controller), enriching the lower-level policy with semantic and spatial cues.

## Relationships

| Relationship | Entity |
|--------------|--------|
| part_of | DualVLN |
| uses | vision-language models ⚠️ ⚠️ ⚠️ |
| supersedes? | – |
| depends_on | vision-language models ⚠️ ⚠️ ⚠️, perception pipeline ⚠️ |
| implemented_by | [to be filled] |

## Reference

- Source: arxiv paper `2512.08186` — *DualVLN: Scaling Vision-Language-Action Models with Dual System Architectures*

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `VLM-based Global Planner` --extends ⚠️--> `DualVLN`
