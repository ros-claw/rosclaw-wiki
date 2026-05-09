---
id: eb_alfred
title: EB-ALFRED
type: entity
tags: []
confidence: 0.6
created_at: '2026-04-29T21:54:27'
last_reinforced: '2026-04-29T21:54:27'
supersedes: []
sources:
- articles/article.md
source_type: blog_post
---

# EB-ALFRED

**EB-ALFRED** is a high-level planning component within the [[EmbodiedBench]] suite. It is designed for high-level task decomposition and planning, operating at an abstract action level (e.g., "put a book on the desk") rather than low-level motor commands.

## Overview

EB-ALFRED leverages the [[ALFRED environment]] ⚠️ ⚠️ to generate executable plans from natural language instructions. It focuses on breaking down complex, long-horizon tasks into sequences of subgoals, enabling downstream agents to execute them in a simulated or real-world setting.

## Capabilities

- **High-level planning**: Translates natural language goals into ordered action steps (e.g., "pick up the book", "move to desk", "place on desk").

## Relationships

- **part_of**: [[EmbodiedBench]] — EB-ALFRED is one of the benchmark tasks within the EmbodiedBench framework.
- **uses**: [[ALFRED environment]] ⚠️ ⚠️ — The planning component relies on the ALFRED simulation environment to define valid actions, object interactions, and scene configurations.

## Usage Notes

While EB-ALFRED provides the planning layer, it does not include low-level control or perception modules; these are expected to be supplied by the agent being evaluated in EmbodiedBench. The high-level action space simplifies evaluation of language understanding and task reasoning.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `EB-ALFRED` --[[depends_on]] ⚠️--> `EmbodiedBench`
