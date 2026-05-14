---
id: agile_locomotion
title: Agile Locomotion
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-30T04:10:09'
last_reinforced: '2026-04-30T04:10:09'
supersedes: []
sources:
- papers/2505.11164.pdf
source_type: arxiv_paper
---

# Agile Locomotion

**Agile locomotion** refers to the ability of Legged Robots to move quickly and adaptively across varied terrains. It combines reactive control with learned policies to maintain stability, speed, and manoeuvrability even in unstructured environments.

## Key Components

Agile locomotion systems rely on three primary building blocks:

- **Depth images** – used as exteroceptive input to perceive terrain geometry and obstacles. This enables the robot to anticipate changes in footholds and adjust its gait accordingly.
- **Multi-expert distillation** – a training technique where multiple specialized expert policies (e.g., for different terrain types) are distilled into a single unified network, preserving robustness while reducing computational overhead.
- **RL fine-tuning** – after distillation, the policy is further refined via reinforcement learning in simulation to improve generalization and close the sim-to-real gap.

## Capabilities

Systems designed for agile locomotion can:

- Navigate diverse unstructured terrains (e.g., rubble, slopes, stairs, vegetation).
- Demonstrate robust generalisation to unseen environments without explicit re-training.

## Related Entities

- **Applied to**: ANYmal D – the quadrupedal platform on which this approach has been deployed.
- **Uses**: Depth Images ⚠️ as exteroceptive input; implements Multi-Expert Distillation and Reinforcement Learning (RL fine-tuning).
- **Depends on**: Sim-to-Real Transfer techniques to bridge simulation and hardware; Legged Locomotion ⚠️ as the broader domain.

## References

- **Source**: arXiv paper 2505.11164 – introduces the depth-image-driven multi-expert distillation framework for agile locomotion on ANYmal D.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Agile Locomotion` --applies_to ⚠️ ⚠️--> `legged robots`
- `Agile Locomotion` --applies_to ⚠️ ⚠️--> `ANYmal D`
**Pending review:**
- `Agile Locomotion` --related_to ⚠️--> `Multi-Expert Distillation` _(wikilink)_
