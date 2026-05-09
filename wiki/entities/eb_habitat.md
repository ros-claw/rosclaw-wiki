---
id: eb_habitat
title: EB-Habitat
type: entity
tags: []
confidence: 0.6
created_at: '2026-04-29T21:54:42'
last_reinforced: '2026-04-29T21:54:42'
supersedes: []
sources:
- articles/article.md
source_type: blog_post
---

**EB-Habitat** is a component of the [[EmbodiedBench]] benchmark suite that focuses on high-level task decomposition and planning within the [[Habitat environment]] ⚠️ ⚠️ ⚠️. It provides an action interface for abstract, semantically rich commands rather than low-level motor control.

## Overview

EB-Habitat evaluates an agent’s ability to reason about sequential tasks — such as navigating to a room, picking up an object, or rearranging furniture — by issuing high-level instructions in the [[Habitat environment]] ⚠️ ⚠️ ⚠️. It is designed to test planning, common sense, and task sequencing capabilities without requiring the agent to handle raw sensorimotor details.

## Capabilities

- **High-level planning** – decomposing broad goals into ordered subtasks and executing them via Habitat’s simulator.

## Relationships

| Relation | Entity | Description |
|----------|--------|-------------|
| `part_of` | [[EmbodiedBench]] | EB-Habitat is one of the evaluation suites within the broader EmbodiedBench framework. |
| `uses` | [[Habitat environment]] ⚠️ ⚠️ ⚠️ | Relies on the Habitat simulation platform for 3D scene rendering, physics, and interactive object manipulation. |

## Action Level

- **Action level**: `high-level` — the agent outputs abstract action tokens (e.g., `"go to kitchen table"`) rather than joint torques or pixel-level velocities. This aligns with the emphasis on cognitive reasoning over motor control.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `EB-Habitat` --[[depends_on]] ⚠️--> `EmbodiedBench`
