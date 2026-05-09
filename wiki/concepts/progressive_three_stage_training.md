---
id: progressive_three_stage_training
title: Progressive Three-Stage Training
type: concept
tags: []
confidence: 0.85
created_at: '2026-04-29T20:44:34'
last_reinforced: '2026-04-30'
supersedes: []
sources:
- papers/2512.15258.json
- papers/2512.15258.pdf
source_type: arxiv_paper
---

## Progressive Three-Stage Training

**Progressive Three-Stage Training** is a pedagogical framework for embodied AI systems that sequentially reinforces capabilities from foundational to advanced levels. Designed as part of the [[VLA-AN]] architecture, this training regimen decomposes complex skill acquisition into three incremental stages, ensuring robust learning and transfer.

### Training Stages

The framework is structured as a staged curriculum:

1. **Scene comprehension** – The agent learns to perceive and understand its environment, including object detection, spatial layout, and context recognition. This stage builds a foundational representation of the world.

2. **Core flight skills** – Basic locomotion, navigation, and low-level control policies are trained. For aerial platforms, this includes hovering, trajectory following, and obstacle avoidance in controlled settings.

3. **Complex navigation capabilities** – The agent synthesizes scene understanding and core skills to perform advanced tasks such as autonomous exploration, dynamic obstacle negotiation, and goal-directed planning in unstructured environments.

### Purpose

The progressive approach avoids the instability of end-to-end training on complex tasks by providing a staged curriculum. Each stage acts as a prerequisite for the next, enabling the agent to master simpler behaviors before integrating them into higher-level reasoning. This method achieves **sequential reinforcement of navigation abilities**, systematically stacking skills so that each stage builds upon the prior one.

### Relationships

- **Part of** [[VLA-AN]] — This training scheme is a core component of the VLA-AN framework, which combines vision-language-action models with adaptive navigation.
- **Used by** [[VLA-AN]] — The training regimen is applied within VLA-AN to teach embodied agents progressively.
- **Depends on** [[Sim-to-Real Transfer Techniques]] ⚠️ — To ensure skills learned in simulation generalize to real-world deployment.
- **Implements** [[Curriculum Learning]] ⚠️ principles — By ordering tasks from easy to hard, progressive training aligns with established curriculum learning theory.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker and are reinforced by the latest source._

- `Progressive Three-Stage Training` ––[[part_of]] ⚠️––> `[[VLA-AN]]` _(confirmed)_
- `Progressive Three-Stage Training` ––[[used_by]] ⚠️––> `[[VLA-AN]]` _(confirmed)_