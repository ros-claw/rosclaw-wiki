---
id: hierarchical_planner
title: Hierarchical Planner
type: algorithm
tags: []
confidence: 0.8
created_at: '2026-04-30T00:23:56'
last_reinforced: '2026-04-30T00:23:56'
supersedes: []
sources:
- papers/2508.08240.pdf
source_type: arxiv_paper
---

# Hierarchical Planner

## Description
The Hierarchical Planner is a high-level planning algorithm that leverages a Vision-Language Model to decompose complex language instructions into executable sub-tasks and guide precise actions. It overcomes the constrained egocentric perception challenges inherent to mobile platforms, enabling robust long-horizon task execution.

## Capabilities
- **Long-horizon instruction decomposition**: Breaks down multi-step natural language commands into a sequence of manageable sub-tasks.
- **Precise action execution**: Generates fine-grained action plans that can be directly executed by the robot's low-level controllers.
- **Addressing egocentric perception challenges**: Mitigates the limited field-of-view and partial observability common on mobile platforms by combining linguistic context with visual reasoning.

## Relationships
- **depends_on**: Vision-Language Model
- **part_of**: ODYSSEY

## Usage in ODYSSEY
Within the ODYSSEY system, the Hierarchical Planner acts as the cognitive orchestrator. It receives high-level instructions, queries the Vision-Language Model for environmental grounding and sub-task generation, and outputs structured plans that the robot's execution layer can follow. This architecture allows ODYSSEY to handle long-horizon mobile manipulation tasks that would otherwise be infeasible with flat, reactive planners.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Hierarchical Planner` --extends ⚠️--> `ODYSSEY`
