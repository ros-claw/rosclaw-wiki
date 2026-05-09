---
id: capability_conditioned_navigation
title: Capability-Conditioned Navigation
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-29T21:19:12'
last_reinforced: '2026-04-29T21:19:12'
supersedes: []
sources:
- papers/2602.18424.pdf
source_type: arxiv_paper
---

## Capability-Conditioned Navigation

### Overview

Capability-Conditioned Navigation refers to the evaluation paradigm introduced by the **CapNav** benchmark, which tests [[Vision-Language Models]] ⚠️ ⚠️ ⚠️ (VLMs) on indoor navigation tasks that are explicitly conditioned on the physical and mobility constraints of an embodied agent. The benchmark bridges the gap between typical vision-language navigation and real‑world robot deployment, where agents vary in size, shape, and locomotion abilities. CapNav is a part of the broader field of **[[Embodied AI]]** and directly **uses** [[Vision-Language Navigation]] as its core task framework.

### Benchmark Design

CapNav comprises:
- **45** indoor scenes
- **473** navigation tasks
- **2,365** question‑answer pairs
- **5** distinct agent types (both human and robot)
- **13** state‑of‑the‑art VLM models evaluated

The benchmark **depends on** [[Vision-Language Models]] ⚠️ ⚠️ ⚠️ to interpret visual scenes and language instructions, and then to plan a path that respects the agent’s unique capabilities.

### Capabilities

CapNav is designed to:
- Evaluate VLM navigation performance under explicit mobility constraints.
- Define agent-specific physical and operational capabilities (e.g., maximum turning radius, floor clearance, reach height).
- Test spatial reasoning for obstacle avoidance by requiring models to consider whether an agent can physically traverse, duck under, or navigate around obstacles.

### Agent Types

Five representative agents are defined in the benchmark, each differing in dimensions, mobility, and interaction abilities:

- **Human adult** (standard walking and reaching)
- **Child** (smaller stature, tighter clearance)
- **Wheeled robot** (e.g., TurtleBot – limited turning radius, no stair climbing)
- **Legged robot** (e.g., Spot – can step over low obstacles)
- **Aerial drone** (narrow passages, no ground contact)

Each agent has a formalized **capability profile** that the VLMs must internalize to answer navigation queries correctly.

### Evaluation Results

The study revealed that VLM performance drops sharply when constraints become more restrictive (e.g., a wheelchair‑like agent with a wide turn radius). Even the best models struggle with reasoning about spatial dimensions relative to the agent’s body. For instance, they frequently misjudge whether an agent can fit through a doorway or pass under a low shelf. These findings highlight a fundamental weakness in current VLMs regarding **embodied spatial reasoning** under capability constraints.

### Relationships

- **uses** → [[Vision-Language Navigation]]
- **depends_on** → [[Vision-Language Models]] ⚠️ ⚠️ ⚠️
- **part_of** → [[Embodied AI]]

**Cross-references**: See also [[Spatial Reasoning]] ⚠️, [[Sim-to-Real Transfer]], and [[Mobility Constraints]] ⚠️ for related concepts in embodied intelligence.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Capability-Conditioned Navigation` --[[related_to]] ⚠️--> `Embodied AI`
