---
id: room_to_room_r2r_task
title: Room-to-Room (R2R) Task
type: entity
tags: []
confidence: 0.8
created_at: '2026-04-30T03:04:39'
last_reinforced: '2026-04-30T03:04:39'
supersedes: []
sources:
- papers/1904.04195.pdf
source_type: arxiv_paper
---

# Room-to-Room (R2R) Task

The **Room-to-Room (R2R) Task** is a standard benchmark for evaluating **vision-and-language navigation** (VLN) agents. It was introduced by Anderson et al. in the paper *"Vision-and-Language Navigation: Interpreting Visually-Grounded Navigation Instructions in Real Environments"* (arXiv:1904.04195). The task requires an agent to follow natural language instructions to navigate from a starting location to a goal room within a photorealistic 3D environment (Matterport3D).

## Capabilities

- Serves as a **benchmark** for evaluating the ability of embodied agents to ground natural language instructions in visual observations and execute step-by-step navigation.
- Includes a **private unseen test set**, enabling rigorous evaluation of generalization to new environments and instructions not seen during training.

## Relationships

- **Used by**: [[Generalizable Navigational Agent]] — the [[R2R Benchmark]] is used to assess the generalization performance of navigational agents that must adapt to unseen instructions and environments.

## Related Concepts

- [[Vision-and-Language Navigation]]
- [[Matterport3D]] ⚠️ (the environment used for R2R)
- [[Embodied AI]]
- [[Instruction Following]] ⚠️
- [[Cross-Modal Grounding]] ⚠️

## References

- Anderson, P., Wu, Q., Teney, D., Bruce, J., Johnson, M., Sünderhauf, N., ... & van den Hengel, A. (2018). *Vision-and-Language Navigation: Interpreting Visually-Grounded Navigation Instructions in Real Environments*. arXiv:1904.04195.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Room-to-Room (R2R) Task` --[[related_to]] ⚠️ ⚠️--> `Vision-and-Language Navigation`
- `Room-to-Room (R2R) Task` --[[related_to]] ⚠️ ⚠️--> `Embodied AI`
