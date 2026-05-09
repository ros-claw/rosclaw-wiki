---
id: cross_modal_planner
title: Cross-modal planner
type: algorithm
tags: []
confidence: 0.8
created_at: '2026-04-30T01:20:01'
last_reinforced: '2026-04-30T01:20:01'
supersedes: []
sources:
- papers/2304.03047.pdf
source_type: arxiv_paper
---

# Cross-modal Planner

## Overview

The Cross-modal Planner is a transformer-based algorithm that generates high-level navigation plans from [[Topological map]] ⚠️ ⚠️ and [[language instructions]] ⚠️. It is a core component of the [[ETPNav]] system, enabling embodied agents to navigate complex environments by grounding linguistic commands in topological representations of space.

## Architecture

The planner uses a [[Transformer]] ⚠️ architecture to process multi‑modal inputs—topological maps and natural language instructions—and outputs a sequence of subgoals or waypoints that form a navigation plan. The cross-modal attention mechanism aligns spatial and linguistic features to produce coherent, executable routes.

## Capabilities

- Generate navigation plans based on topological maps and language instructions.
- Produce high‑level plans that can be executed by a lower‑level motion controller.
- Support dynamic replanning when instructions or map topology change.

## Relationships

- **part_of**: [[ETPNav]]
- **uses**: [[Topological map]] ⚠️ ⚠️, [[Instructions]] ⚠️

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Cross-modal planner` --[[extends]] ⚠️--> `ETPNav`
