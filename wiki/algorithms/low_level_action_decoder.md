---
id: low_level_action_decoder
title: low-level action decoder
type: algorithm
tags: []
confidence: 0.8
created_at: '2026-04-29T21:03:06'
last_reinforced: '2026-04-29T21:03:06'
supersedes: []
sources:
- papers/2408.10388.pdf
source_type: arxiv_paper
---

# Low-Level Action Decoder

## Overview

The **low-level action decoder** is a neural network component that bridges the gap between high-level view selection and low-level motor commands. It is trained jointly with the [[high-level action prediction]] policy, enabling the system to ground selected visual views directly to executable controls. This joint training allows the decoder to learn spatial reasoning within low-level movements, rather than treating high-level planning and low-level control as separate modules.

## Capabilities

- **Jointly trained with high-level action prediction** – The decoder is not a separate post-hoc controller; it is optimized together with the high-level policy, ensuring coherent gradient flow between planning and execution.
- **Grounds selected visual views to low-level controls** – Converts abstract visual representations (e.g., keyframes or object-centric views) into continuous motor commands.
- **Enables learning of spatial reasoning within low-level movements** – Because the decoder is aware of the high-level goals, it can incorporate spatial constraints (e.g., reaching, avoidance) directly into the action space.

## Relationships

| Type | Related Entity |
|------|----------------|
| `depends_on` | [[high-level action prediction]] – The decoder receives the high-level policy’s output (e.g., selected views) as input. |
| `uses` | [[visual representations with rich semantic information]] ⚠️ – The decoder operates on visual features that encode object identities, spatial layouts, and task‑relevant cues. |

## Implementation

The low-level action decoder is introduced to bridge the gap between high-level view selection and low-level motor commands. It is trained jointly with the high-level policy, meaning gradients from the decoder’s loss (e.g., imitation or reinforcement learning) flow back to the view‑selection network. This architecture promotes end‑to‑end learning of both *where to look* and *how to move*.

During training, the decoder receives:
- Selected visual views (encoded as feature maps or latent vectors)
- The latent state from the high‑level predictor
- Optional proprioceptive feedback

It outputs continuous action vectors (joint angles, velocities, or end‑effector targets) that respect the robot’s kinematic and dynamic constraints. The implementation uses a lightweight MLP with skip connections, regularized to prevent overfitting to single‑view policies.

*Source: arXiv 2408.10388*

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `low-level action decoder` --[[based_on]] ⚠️--> `high-level action prediction`
