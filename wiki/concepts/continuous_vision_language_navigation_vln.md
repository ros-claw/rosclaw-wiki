---
id: continuous_vision_language_navigation_vln
title: Continuous Vision-Language Navigation (VLN)
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-30T00:56:11'
last_reinforced: '2026-04-30T00:56:11'
supersedes: []
sources:
- papers/2407.05890.pdf
source_type: arxiv_paper
---

# Continuous Vision-Language Navigation (VLN)

**Continuous Vision-Language Navigation (VLN)** is a setting in [[Embodied AI]] where an agent must follow natural language instructions to navigate through **continuous, unstructured environments** (as opposed to discretized graph-based settings). Unlike classic VLN benchmarks that assume navigation on predefined node graphs, continuous VLN requires the agent to perform **low-level motion control** (e.g., steering, acceleration) alongside high-level semantic understanding and planning.

## Characteristics

- **Domain:** [[Embodied AI]]
- **Setting:** Continuous environment; the agent receives language commands and must execute smooth, collision-free motion in real-world-like spaces.
- **Capabilities:** Requires integration of **high-level planning** (route comprehension, landmark recognition) and **low-level motion control** (velocity, turning, obstacle avoidance). The agent must interpret instructions like "go past the sofa and turn left" while continuously adjusting its physical trajectory.

## Key Benchmarks

Continuous VLN is commonly evaluated using extensions of classic discrete benchmarks:

- **[[R2R-CE]]** – Continuous variant of the Room-to-Room (R2R) dataset, where agents navigate in the Matterport3D simulator with continuous action spaces.
- **[[RxR-CE]]** – Continuous extension of the Room-across-Room (RxR) dataset, offering more complex instructions and longer paths.

## Relationship to Planners

Continuous VLN agents often rely on modular architectures that separate language grounding and path planning from motion execution. One such framework is **[[AO-Planner]]** (Action-Oriented Planner), which implements a two-stage process: first generating a coarse path from language, then using a low-level controller to follow it. The AO-Planner [depends_on :: [[Continuous VLN]] ⚠️] by design, as it explicitly bridges the gap between high-level instruction interpretation and continuous motion.

## See Also

- [[Sim-to-Real Transfer]] – Many continuous VLN methods aim to transfer policies from simulation to physical robots.
- [[Low-Level Control]] ⚠️ – The motion execution layer in continuous VLN agents.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Continuous Vision-Language Navigation (VLN)` --[[related_to]] ⚠️ ⚠️--> `Embodied AI`
- `Continuous Vision-Language Navigation (VLN)` --[[applies_to]] ⚠️ ⚠️--> `R2R-CE`
- `Continuous Vision-Language Navigation (VLN)` --[[applies_to]] ⚠️ ⚠️--> `RxR-CE`
**Pending review:**
- `Continuous Vision-Language Navigation (VLN)` --[[related_to]] ⚠️ ⚠️--> `AO-Planner` _(wikilink)_
