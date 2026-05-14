---
id: high_level_action_prediction
title: high-level action prediction
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-29T21:03:31'
last_reinforced: '2026-04-29T21:03:31'
supersedes: []
sources:
- papers/2408.10388.pdf
source_type: arxiv_paper
---

# High-Level Action Prediction

**High-level action prediction** is a conceptual approach in embodied AI where an agent selects a coarse behavioral goal—such as a viewing direction or a waypoint—rather than specifying exact low-level motor commands. This technique simplifies the action space and is commonly employed in **Vision and Language Navigation in the Continuous Environment (VLN-CE) ⚠️ ⚠️** to reduce computational complexity.

## Role

High-level action prediction selects a viewing direction or waypoint, but does not incorporate fine-grained control. This paper proposes joint training with low-level actions to address the gap. By integrating both levels, the system can leverage efficient high-level reasoning while learning the precise spatial movements required for successful navigation.

## Capabilities

- **View selection task in VLN-CE**: The predictor outputs a target viewpoint or heading, which is then executed by a lower-level controller (e.g., a motion planner or a low-level policy).

## Relationships

- **part_of**: `High-level action prediction` is a component of `Vision and Language Navigation in the Continuous Environment (VLN-CE) ⚠️ ⚠️`.
- **limitation**: This approach ignores crucial spatial reasoning within low-level action movements. Spatial reasoning ⚠️ in fine-grained motion (e.g., obstacle avoidance, precise turning angles, and velocity control) is not addressed by purely high‑level predictions.

## Source

- *Beyond High-Level Action Prediction: Combining Low-Level Action Training for Vision-and-Language Navigation* (arXiv:2408.10388) – Critiques the above limitation and proposes joint low‑level action training to bridge the gap.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `high-level action prediction` --related_to ⚠️--> `VLN-CE`
