---
id: visual_navigation
title: Visual Navigation
type: concept
tags: []
confidence: 0.85
created_at: '2026-04-30T04:22:20'
last_reinforced: '2026-04-30'
supersedes: []
sources:
- papers/2510.08713.pdf
- papers/2210.14791.pdf
source_type: arxiv_paper
---

# Visual Navigation

**Visual Navigation** is the task of guiding an embodied agent to a goal location using visual input. It is a core capability within Embodied AI that requires the agent to perceive its surroundings, predict future states, and select appropriate actions in order to reach a goal or explore autonomously. In implementations like ViNL, the navigation policy outputs velocity commands.

## Definition

Visual Navigation is defined as the task of guiding a robot to a goal location using visual input. The agent must interpret egocentric camera images to determine its position relative to a target and plan a path. In the context of ViNL, the navigation policy directly outputs velocity commands, bridging perception and action.

## Capabilities

- Enables embodied agents to navigate through environments based solely on visual input, without requiring pre-mapped layouts or external localization aids.
- Requires tight alignment between perception (interpreting visual data), prediction (simulating possible outcomes), and action selection (choosing the next movement).
- Capable of navigating to **distant goals** using only egocentric vision in **unseen environments**, demonstrating generalization beyond training conditions.

## Challenges

State-action misalignment and weak adaptability in novel or dynamic scenarios are key challenges addressed by unified models like UniWM. Agents often fail when visual inputs deviate from training distributions or when the mapping between observed states and required actions is inconsistent.

## Relationships

**Visual Navigation** depends on Embodied AI and uses the following computational components:

- World Models – to simulate the environment and plan future trajectories.
- Foresight ⚠️ – to anticipate the consequences of candidate actions.
- Memory ⚠️ – to retain representations of previously visited locations and to guide exploration.

**Implemented by:**
- Visual Navigation Policy – a policy that maps visual observations directly to control commands (e.g., velocity outputs in ViNL).

**Used in:**
- ViNL – a framework that combines visual navigation with language instructions for goal-directed behavior.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Visual Navigation` --related_to ⚠️--> `Embodied AI`