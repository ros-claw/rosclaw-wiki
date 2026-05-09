---
id: navspace_benchmark
title: NavSpace benchmark
type: concept
tags: []
confidence: 0.85
created_at: '2026-04-29T20:34:16'
last_reinforced: '2026-04-29'
supersedes: []
sources:
- papers/2510.08173.json
- code/TidalHarley_NavSpace/README.md
source_type: arxiv_paper
---

# NavSpace Benchmark

**NavSpace** is a benchmark designed to systematically evaluate spatial intelligence in instruction-following navigation. Published at **ICRA 2026**, it contains **six task categories** and **1,228 trajectory-instruction pairs**, specifically targeting the spatial perception and reasoning abilities of embodied navigation agents. The benchmark evaluates **22 navigation agents** across its subtasks.

## Overview

NavSpace probes the spatial intelligence of [[navigation agents]] ⚠️ ⚠️ by providing a diverse set of trajectory-instruction pairs across multiple task categories. The benchmark aims to isolate and measure the core spatial reasoning capabilities required for grounding natural language instructions to physical movement in real or simulated environments. It is built on the [[VLN framework]] ⚠️ ⚠️ and uses [[Habitat-Sim]] as the simulator with [[HM3D]] scenes.

## Parameters

| Metric | Value |
|--------|-------|
| Total episodes | 1,228 |
| Task categories | 6 |
| Environment state | 200 episodes |
| Space structure | 200 episodes |
| Precise movement | 201 episodes |
| Viewpoint shifting | 207 episodes |
| Vertical perception | 208 episodes |
| Spatial relationship | 212 episodes |
| Evaluated agents | 22 |
| Publication | ICRA 2026 |

## Task Categories

The six subtasks cover distinct facets of spatial intelligence:

1. **Environment state** (200 episodes) — understanding the current configuration of the environment.
2. **Space structure** (200 episodes) — reasoning about the layout and geometry of the space.
3. **Precise movement** (201 episodes) — following instructions that require exact positioning and orientation.
4. **Viewpoint shifting** (207 episodes) — accommodating changes in perspective or orientation.
5. **Vertical perception** (208 episodes) — navigating in environments with height changes (stairs, ramps, elevated objects).
6. **Spatial relationship** (212 episodes) — comprehending and executing instructions involving relative positions (e.g., left of, behind, next to).

## Action Space

The agent's action space is defined as:

- `forward` (0.25 m)
- `left` (30° rotation)
- `right` (30° rotation)
- `look-up` (30° tilt)
- `look-down` (30° tilt)
- `backward` (0.25 m)
- `stop`

## Capabilities

- Evaluate spatial perception and reasoning of [[navigation agents]] ⚠️ ⚠️
- Provide six task categories covering different spatial intelligence skills
- Serve as a benchmark for instruction-following navigation
- Probe spatial intelligence in [[embodied navigation]]

## Relationships

- **Depends on**: [[VLN framework]] ⚠️ ⚠️
- **Uses**: [[Habitat-Sim]], [[HM3D]]
- **Evaluates**: 22 navigation agents, including [[SNav]], [[StreamVLN]], and [[LLM evaluation route]] ⚠️
- **Includes**: 6 subtasks (environment state, space structure, precise movement, viewpoint shifting, vertical perception, spatial relationship)

> **Note on SNav**: Earlier sources described SNav as using NavSpace as an evaluation tool; newer data lists SNav among the agents evaluated by the benchmark. Both usages are compatible—SNav is both an evaluated agent and a methodology that reports results on NavSpace.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Pending review:**
- `NavSpace benchmark` --[[related_to]] ⚠️ ⚠️--> `SNav` _(wikilink)_
- `NavSpace benchmark` --[[related_to]] ⚠️ ⚠️--> `StreamVLN` _(wikilink)_
