---
id: rl_policy_for_locomotion
title: RL policy for locomotion
type: algorithm
tags: []
confidence: 0.8
created_at: '2026-04-29T21:30:23'
last_reinforced: '2026-04-29T21:30:23'
supersedes: []
sources:
- papers/2512.09537.pdf
source_type: arxiv_paper
---

# RL Policy for Locomotion

A **RL policy for locomotion** is a learned controller that provides low-level locomotion control for legged robots. It is a core component of the [[REASAN]] framework, where it handles the fundamental task of generating stable and adaptive gaits without relying on hand-crafted heuristics or policy-switching mechanisms.

## Capabilities

- **Low-level locomotion control**: Generates joint-level commands to achieve stable walking, running, and other legged motions on various terrains.
- **Adaptability**: Through [[reinforcement learning]] training, the policy can generalize to unseen environments and perturbations.

## Training

The policy is trained using standard reinforcement learning practices, enhanced with:

- **Targeted [[reward shaping]]**: Reward terms are carefully designed to encourage desired behaviors (e.g., forward velocity, energy efficiency, foot clearance) while avoiding undesirable ones.
- **[[Curriculum design]]**: Training difficulty is gradually increased — for example, starting on flat ground and introducing slopes, stairs, or obstacles — to build robust motor skills.

No heuristics or policy-switching mechanisms are used; the policy learns end-to-end to handle the full range of locomotion tasks.

## Relationships

- **`part_of`** [[REASAN]] – the overall architecture that combines this policy with a high-level skill selector.
- **`depends_on`**:
  - [[reinforcement learning]] – the learning paradigm used to optimize the policy.
  - [[reward shaping]] – to provide informative learning signals.
  - [[curriculum design]] – to structure training progression.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `RL policy for locomotion` --[[extends]] ⚠️--> `REASAN`
