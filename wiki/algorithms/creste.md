---
id: creste
title: CREStE
type: algorithm
tags: []
confidence: 0.85
created_at: '2026-04-29T21:45:48'
last_reinforced: '2026-04-29'
supersedes: []
sources:
- papers/2503.03921.pdf
source_type: arxiv_paper
---

# CREStE

**CREStE** is a scalable learning-based mapless navigation framework designed for open-world generalization and long-range autonomy in outdoor urban environments. It achieves kilometer-scale traversal with minimal human intervention by combining [[Visual Foundation Model (VFM) Distillation]] objectives with [[Counterfactual Inverse Reinforcement Learning]] ⚠️ to produce robust, expert-aligned navigation costs.

## Overview

CREStE addresses two key challenges in outdoor mapless navigation: (1) open-world generalization to novel semantic classes, terrains, and dynamic entities; and (2) reduction of costly human interventions during deployment. The framework learns perceptual representations through VFM distillation, enabling open-set structured bird's-eye-view scene understanding, then infers navigation costs via a counterfactual IRL formulation that actively reasons about critical environmental cues.

## Capabilities

- **Kilometer-scale mapless navigation** in urban, offroad, and residential environments
- Demonstrated **2 km mission** in an unseen environment with only **1 human intervention**
- **Open-world generalization** to novel semantic classes, terrains, and dynamic entities not seen during training
- Outperforms all state-of-the-art approaches on benchmark evaluations
- Achieves **70% fewer human interventions** compared to leading prior methods

## Components

1. **VFM Distillation Objective** – Distills knowledge from a pretrained visual foundation model into a lightweight encoder that produces open-set, structured bird's-eye-view perceptual representations. This enables the system to recognize and reason about previously unseen scene elements.

2. **Counterfactual IRL** – An active learning formulation for inverse reinforcement learning. The system generates counterfactual trajectory demonstrations to understand which environmental features are critical for correct navigation cost inference, enabling data-efficient alignment with expert driving behavior.

## Parameters

| Parameter | Value |
|-----------|-------|
| Framework type | Scalable learning-based mapless navigation |
| Demo reduction | 70% fewer human interventions vs. SOTA |

## Relationships

- **Uses** → [[Visual Foundation Model (VFM) Distillation Objective]], [[Counterfactual Inverse Reinforcement Learning (IRL)]]
- **Depends on** → [[Visual Foundation Model]] ⚠️ ⚠️, [[Inverse Reinforcement Learning]] ⚠️ ⚠️
- **Implements** → [[Mapless Navigation]]

## Related Pages

- [[Mapless Navigation]]
- [[Visual Foundation Model]] ⚠️ ⚠️
- [[Inverse Reinforcement Learning]] ⚠️ ⚠️
- [[Behavior Cloning]] ⚠️ (contrast with IRL-based approach)
- [[Sim-to-Real Transfer]] (relevant to open-world generalization)

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `CREStE` --[[extends]] ⚠️ ⚠️ ⚠️--> `Visual Foundation Model (VFM) Distillation`
- `CREStE` --[[extends]] ⚠️ ⚠️ ⚠️--> `Visual Foundation Model (VFM) Distillation Objective`
- `CREStE` --[[extends]] ⚠️ ⚠️ ⚠️--> `Counterfactual Inverse Reinforcement Learning (IRL)`
- `CREStE` --[[based_on]] ⚠️--> `Mapless Navigation`
