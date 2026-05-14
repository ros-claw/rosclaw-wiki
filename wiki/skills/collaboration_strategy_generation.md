---
id: collaboration_strategy_generation
title: Collaboration Strategy Generation
type: skill
tags: []
confidence: 0.8
created_at: '2026-04-29T20:50:53'
last_reinforced: '2026-04-29T20:50:53'
supersedes: []
sources:
- papers/2505.13729.pdf
source_type: arxiv_paper
---

# Collaboration Strategy Generation

**Description**: The skill of automatically generating a collaboration strategy using LLMs, which determines how robots should coordinate based on their individual capabilities and the current state of the task.

**Method**: LLM ⚠️ ⚠️-based

**Output**: A strategy for a team of robots

**Capabilities**  
- Adapts based on Robot Skills ⚠️ ⚠️ and Robot Status ⚠️  
- Generated automatically without human intervention

**Part of** SayCoNav

## Overview

Collaboration Strategy Generation is an autonomous reasoning component that takes a high-level task description, the known skills of each robot in the team, and the current task status (e.g., which parts are completed or stalled), and produces a step-by-step coordination plan. The strategy may assign sub‑tasks, define temporal dependencies, or specify handover points between robots.

Because the generation is driven by a large language model, it can adapt to novel combinations of robots and tasks without requiring explicit pre‑programmed coordination logic. This makes the skill particularly suited for dynamic, heterogeneous multi‑robot systems.

## Dependencies

- Uses LLM ⚠️ ⚠️ for reasoning and plan generation  
- Depends on access to Robot Skills ⚠️ ⚠️ representation and Task State ⚠️ tracking

## Related Pages

- SayCoNav – the system containing this skill  
- Multi-Robot Coordination ⚠️ – broader context  
- Skill Representation ⚠️ – how robot capabilities are modeled for input

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Collaboration Strategy Generation` --uses ⚠️--> `SayCoNav`
