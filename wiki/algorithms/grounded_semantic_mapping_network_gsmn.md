---
id: grounded_semantic_mapping_network_gsmn
title: Grounded Semantic Mapping Network (GSMN)
type: algorithm
tags: []
confidence: 0.85
created_at: '2026-04-29T21:19:16'
last_reinforced: '2026-04-30'
supersedes: []
sources:
- papers/1806.00047.pdf
source_type: arxiv_paper
---

---

## Grounded Semantic Mapping Network (GSMN)

The **Grounded Semantic Mapping Network (GSMN)** is a [[fully-differentiable neural network]] ⚠️ architecture for end-to-end visual navigation. It translates high-level language instructions and raw visual observations directly into continuous low-level velocity commands. The key innovation is the explicit construction of a **semantic map in the world reference frame**, which enables the network to reason about spatial relationships and maintain interpretable internal representations.

---

### Summary

The GSMN is introduced for following high-level navigation instructions via [[Imitation Learning]]. It uses an explicit mapping module and a grounding mechanism to achieve near-expert performance. The original paper evaluates the network in a simulated environment — either a quadcopter or a mobile robot (see platform discrepancy below).

> **⚠ Platform discrepancy**: The current page states GSMN operates on a mobile robot, while new source information indicates evaluation in a **simulated quadcopter environment**. Both platforms may have been tested; the exact evaluation setup needs to be confirmed from the original publication.

---

### Architecture

GSMN is a **fully-differentiable neural network** that operates in real time. It combines CNNs for visual feature extraction, a language encoder for instruction processing, and a pose estimation module. A differentiable mapping module projects pixel-wise semantic predictions into an allocentric (world-centered) grid map using a [[Pinhole Camera Projection Model]]. This explicit map is then fed into a control policy to generate continuous velocity commands.

### Input & Output

- **Input**: RGB images, natural language navigation instructions, and **pose estimates** (e.g., from odometry, localization, or an onboard estimator).
- **Output**: Continuous low-level velocity commands (linear and angular velocities) that can be directly executed on a robot.

### Capabilities

- Maps from images, instructions, and pose estimates to continuous low-level velocity commands.
- Builds an **explicit semantic map in the world reference frame** during inference.
- Incorporates a **pinhole camera projection model within the network** to enable differentiable projection.
- Produces **interpretable instruction-following representations** — the intermediate semantic map can be visualized and inspected.
- Follows high-level navigation instructions (e.g., “go to the kitchen and tell me how many chairs are there”).
- Operates in **real time** on a mobile robot (or quadcopter — see platform note above).

---

### Training

GSMN is trained using **[[DAggerFM]]**, a variant of the [[DAgger]] algorithm tailored for this architecture. DAggerFM improves training speed and reduces memory consumption by using a fixed-memory replay buffer and selective querying of the expert policy during imitation learning.

GSMN depends on **[[Imitation Learning]]** for its training paradigm; it learns from expert demonstrations collected offline or online via DAggerFM.

---

### Relationships

- **Uses**: [[DAggerFM]] (for training), [[Pinhole Camera Projection Model]] (for mapping), [[Pose Estimates]] ⚠️ (as input).
- **Depends on**: [[Imitation Learning]], [[Pinhole Camera Projection Model]].
- **Related**: [[Semantic Mapping]] ⚠️, [[End-to-End Navigation]], [[Visual Language Navigation]] ⚠️.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Grounded Semantic Mapping Network (GSMN)` --[[extends]] ⚠️--> `DAggerFM`