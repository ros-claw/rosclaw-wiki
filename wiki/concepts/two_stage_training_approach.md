---
id: two_stage_training_approach
title: Two-stage training approach
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-30T00:38:52'
last_reinforced: '2026-04-30T00:38:52'
supersedes: []
sources:
- papers/2506.17221.pdf
source_type: arxiv_paper
---

# Two-stage training approach

The **two-stage training approach** is a machine learning paradigm that first aligns a model's behavior with expert demonstrations using supervised learning, then refines its policy through reinforcement learning to optimize long-term reward. This hybrid method is widely used in Visual Language Navigation ⚠️ (VLN) and embodied AI to bridge the gap between imitation and goal-directed exploration.

## Stages

The approach consists of two sequential phases:

1. **Supervised fine-tuning ⚠️ ⚠️ (SFT)** — The model is trained on a dataset of expert trajectories (e.g., human demonstrations or high-fidelity simulators) to minimize prediction error. This initial phase provides a strong behavioral prior.

2. **Reinforcement fine-tuning ⚠️ (RFT)** — Starting from the SFT checkpoint, the model interacts with an environment and receives rewards (e.g., task completion, collision avoidance). Policy gradient methods (e.g., PPO) are used to maximize expected cumulative reward, correcting systematic flaws from pure imitation.

## Usage

This technique is employed by VLN-R1, a model that applies the two-stage pipeline to improve visual language navigation ⚠️ policies. SFT instills basic instruction-following ability, while RFT enhances robustness to unseen environments and instruction ambiguity.

## Relationship annotations

- **depends_on**: Supervised fine-tuning ⚠️ ⚠️, Reinforcement learning
- **used_by**: VLN-R1
- **implements**: Curriculum learning ⚠️ (loosely, due to stage ordering)

## See also

- Sim-to-real transfer
- Reinforcement learning from human feedback ⚠️

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Pending review:**
- `Two-stage training approach` --related_to ⚠️--> `VLN-R1` _(wikilink)_
