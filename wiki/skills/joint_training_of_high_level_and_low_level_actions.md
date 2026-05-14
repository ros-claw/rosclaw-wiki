---
id: joint_training_of_high_level_and_low_level_actions
title: joint training of high-level and low-level actions
type: skill
tags: []
confidence: 0.8
created_at: '2026-04-29T21:04:08'
last_reinforced: '2026-04-29T21:04:08'
supersedes: []
sources:
- papers/2408.10388.pdf
source_type: arxiv_paper
---

# Joint Training of High-Level and Low-Level Actions

**Type:** Skill  
**Category:** Vision and Language Navigation / Embodied AI  
**Dependencies:** uses low-level action decoder, uses high-level action prediction  
**Used in:** Vision and Language Navigation in the Continuous Environment (VLN-CE) ⚠️ ⚠️

## Overview

Joint training of high-level and low-level actions is a skill in which both the selection of coarse spatial waypoints (high-level actions) and the execution of fine-grained control commands (low-level actions) are learned simultaneously using a shared optimization objective. This approach ensures that high-level planning and low-level execution are mutually informed, leading to more coherent and physically feasible navigation behaviors.

## Parameters

- **Training objective:** simultaneously optimize high-level view selection and low-level action decoder.

## Capabilities

- Improves navigation performance on both high-level and low-level metrics.
- Enhances grounding of visual features to physical actions — the model learns to map visual observations directly to actionable commands at multiple scales.

## Method

The agent is trained with a dual-objective loss that combines high-level waypoint prediction and low-level action decoding, allowing the model to learn spatial reasoning and action feasibility. During training, the network processes visual observations to predict both the next navigable waypoint (high-level) and the immediate motor commands (low-level). The loss function jointly penalises errors in waypoint prediction and action sequence execution, encouraging representations that capture both the topological structure of the environment and the physical constraints of the robot.

## Relationships

- **Uses** → low-level action decoder, high-level action prediction
- **Used in** → Vision and Language Navigation in the Continuous Environment (VLN-CE) ⚠️ ⚠️ where it has been shown to outperform decoupled training approaches.
- **Depends on** → an end-to-end trainable architecture that shares parameters between the high-level and low-level modules, as described in the source paper (arxiv: 2408.10388).

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `joint training of high-level and low-level actions` --uses ⚠️--> `low-level action decoder`
**Pending review:**
- `joint training of high-level and low-level actions` --related_to ⚠️--> `high-level action prediction` _(wikilink)_
