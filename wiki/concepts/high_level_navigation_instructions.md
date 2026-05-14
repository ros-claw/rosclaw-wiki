---
id: high_level_navigation_instructions
title: High-level Navigation Instructions
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-30T02:50:25'
last_reinforced: '2026-04-30T02:50:25'
supersedes: []
sources:
- papers/1806.00047.pdf
source_type: arxiv_paper
---

# High-Level Navigation Instructions

## Overview

**High-Level Navigation Instructions** are natural language commands that specify a goal or sequence of actions at an abstract level, requiring an intelligent agent (robot, quadcopter, etc.) to map them to continuous low-level control. They serve as a bridge between human intent and robotic execution, enabling non-expert users to guide autonomous systems without specifying every joint angle or wheel velocity.

These instructions contrast with low-level commands (e.g., "move forward 0.5 meters") by focusing on what to achieve rather than how to achieve it. The agent must leverage perception, semantic understanding, and motion planning to ground the language into executable trajectories.

## Capabilities

- **Guide robot or quadcopter** to perform tasks specified in natural language, such as "go to the kitchen" or "follow the red hallway."
- **Provide high-level directives** without specifying low‑level actions, requiring the system to decompose the instruction into a sequence of primitive motions or behaviors.

## Relationships

- **Used in**: Grounded Semantic Mapping Network (GSMN) — this architecture explicitly consumes high-level navigation instructions to produce spatially grounded action sequences for visual navigation.

## Related Concepts

- Natural Language Instruction Following ⚠️
- Embodied AI
- Sim-to-Real Transfer (often used to train models that map language commands to control)
- Visual Navigation

## References

- *Grounded Semantic Mapping Network* (arxiv 1806.00047) — introduces the concept in the context of linguistic guidance for robot navigation.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `High-level Navigation Instructions` --related_to ⚠️ ⚠️--> `Embodied AI`
**Pending review:**
- `High-level Navigation Instructions` --related_to ⚠️ ⚠️--> `Grounded Semantic Mapping Network (GSMN)` _(wikilink)_
