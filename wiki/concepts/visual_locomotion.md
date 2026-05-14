---
id: visual_locomotion
title: Visual Locomotion
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-30T05:02:56'
last_reinforced: '2026-04-30T05:02:56'
supersedes: []
sources:
- papers/2210.14791.pdf
source_type: arxiv_paper
---

## Definition

**Visual Locomotion** is a control paradigm in legged robotics where locomotion policies use visual input (e.g., camera images) to adapt foot placement and avoid obstacles in real time. Unlike blind locomotion, which relies solely on proprioception, visual locomotion enables the robot to perceive and react to terrain features ahead, stepping over or around obstacles while following velocity commands.

## Capabilities

- Control leg joints to step over or avoid small obstacles without damaging them.
- Follow high‑level velocity commands (forward, lateral, rotational) while maintaining stability.
- Adapt foot placement based on visual features of the terrain.

## Relationships

- **Implements**: Visual Locomotion Policy ⚠️ — the learned neural network that directly maps visual and proprioceptive observations to joint actions.
- **Used in**: ViNL — a system that combines visual navigation and visual locomotion to navigate cluttered environments.

## Source

Derived from the ViNL paper (2210.14791), which demonstrates a visual locomotion policy trained to step over obstacles while following velocity commands. The policy is trained in simulation and deployed on a real Unitree Go1 ⚠️ robot.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Pending review:**
- `Visual Locomotion` --related_to ⚠️--> `ViNL` _(wikilink)_
