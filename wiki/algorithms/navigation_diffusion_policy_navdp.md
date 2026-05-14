---
id: navigation_diffusion_policy_navdp
title: Navigation Diffusion Policy (NavDP)
type: algorithm
tags: []
confidence: 0.8
created_at: '2026-04-29T21:31:09'
last_reinforced: '2026-04-29T21:31:09'
supersedes: []
sources:
- papers/2505.08712.pdf
source_type: arxiv_paper
---

## Navigation Diffusion Policy (NavDP)

**Navigation Diffusion Policy (NavDP)** is a transformer-based ⚠️ algorithm that jointly learns trajectory generation and trajectory evaluation for mobile robot navigation. It takes as input a local RGB-D observation ⚠️ and outputs both a generated trajectory and its predicted safety value (critic score). NavDP is trained end-to-end in simulation ⚠️ and achieves zero-shot sim-to-real ⚠️ transfer across diverse environments and robot embodiments.

### Capabilities

- **Joint trajectory generation and evaluation** – simultaneously produces motion plans and judges their safety via critic values, enabling the policy to distinguish between safe and dangerous behaviors.
- **Zero-shot sim-to-real transfer** – directly deployed on real robots without fine-tuning, succeeding across different platforms and scene layouts.
- **End-to-end learning** – no hand-crafted cost functions or separate planning–evaluation stacks; the entire pipeline is learned from data.

### Architecture

NavDP is built on a **transformer-based architecture** that processes local RGB-D images and outputs:

- a **trajectory** (sequence of waypoints or controls)
- a **critic value** that scores the trajectory’s safety and feasibility

The architecture is designed to reason over both spatial context and temporal dependencies through attention mechanisms.

### Training Details

NavDP is trained **exclusively in simulation** using a large-scale dataset of **over one million meters** of navigation experience across **3,000 unique scenes**. It leverages privileged information ⚠️ ⚠️ available only in simulation (e.g., ground‑truth occupancy, exact dynamics) to supervise critic values for **contrastive trajectory samples** – pairs of safe and unsafe trajectories that teach the model to evaluate risk.

The learning objective combines:

- behavior cloning ⚠️ for trajectory generation
- contrastive loss over critic values for trajectory evaluation

Training uses simulation data ⚠️ ⚠️ and does not require any real-world interaction.

### Evaluation

Empirical experiments in both simulated and real-world environments show NavDP **significantly outperforms prior state‑of‑the‑art methods** on metrics such as success rate, collision avoidance, and path efficiency. It generalizes to unseen obstacles, varying lighting conditions, and different robot embodiments (e.g., differential drive, omnidirectional).

### Relationships

- **uses**: simulation data ⚠️ ⚠️, privileged information ⚠️ ⚠️, contrastive trajectory samples ⚠️
- **depends_on**: (none explicitly required; standalone algorithm)
- **implements**: end-to-end learning for navigation
- **capable_of**: zero-shot sim-to-real transfer, joint generation and evaluation
- **related_to**: Diffusion Policy ⚠️, Imitation Learning for Navigation ⚠️, Safety-Critical Control ⚠️