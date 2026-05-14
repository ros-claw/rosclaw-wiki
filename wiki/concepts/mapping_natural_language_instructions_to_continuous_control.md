---
id: mapping_natural_language_instructions_to_continuous_control
title: Mapping Natural Language Instructions to Continuous Control
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-30T02:46:24'
last_reinforced: '2026-04-30T02:46:24'
supersedes: []
sources:
- papers/1910.09664.pdf
source_type: arxiv_paper
---

# Mapping Natural Language Instructions to Continuous Control

A framework for translating natural language navigation commands, combined with first-person visual observations from a quadcopter, into continuous low-level control commands. The core challenge lies in grounding abstract language to physical actions and enabling exploration in both simulation and real-world environments.

## Parameters

| Parameter | Description |
|-----------|-------------|
| **Input** | Natural language instructions + first-person observations (e.g., camera feed) |
| **Output** | Continuous control commands for a quadcopter (e.g., thrust, yaw, pitch, roll) |
| **Challenge** | Requires grounding language to physical actions and exploration across domains |

## Capabilities

- Enables a quadcopter to follow natural language navigation commands (e.g., "fly forward and turn left at the red door")
- Integrates language understanding directly with low-level control, bypassing high-level waypoint planning
- Supports sim-to-real transfer through the Joint Simulation and Real-World Learning Framework

## Relationships

- **Part of** Joint Simulation and Real-World Learning Framework – this mapping is a key component that bridges language understanding with continuous control in both simulated and real environments.
- **Enabled by** SuReAL – the SuReAL algorithm provides the reinforcement learning structure that supports joint training across simulation and reality, making the language-to-control mapping feasible.

## Source

Derived from paper: 1910.09664 ⚠️ *"Mapping Natural Language Instructions to Continuous Control"* (arxiv source: `papers/1910.09664.pdf`).

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Mapping Natural Language Instructions to Continuous Control` --related_to ⚠️ ⚠️--> `Joint Simulation and Real-World Learning Framework`
**Pending review:**
- `Mapping Natural Language Instructions to Continuous Control` --related_to ⚠️ ⚠️--> `SuReAL` _(wikilink)_
