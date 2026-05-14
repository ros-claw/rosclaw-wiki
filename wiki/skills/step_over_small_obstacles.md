---
id: step_over_small_obstacles
title: Step over small obstacles
type: skill
tags: []
confidence: 0.8
created_at: '2026-04-30T05:03:22'
last_reinforced: '2026-04-30T05:03:22'
supersedes: []
sources:
- papers/2210.14791.pdf
source_type: arxiv_paper
---

# Step Over Small Obstacles

## Definition

**Step over small obstacles** is a locomotion skill that enables a robot to lift its feet over small objects on the ground, such as shoes, toys, or cables, without contacting or disrupting them. The skill is analogous to how humans and pets step over items on the floor, allowing continuous traversal in cluttered environments.

This skill is a component of the ViNL framework and requires a Visual Locomotion Policy ⚠️ ⚠️ to operate.

## Parameters

- **Obstacle types**: shoes, toys, cables
- **Size**: small (low height/length relative to the robot’s foot clearance)

## Capabilities

- Avoid contacting or disrupting obstacles while walking over them

## Relationships

- **Part of**: ViNL
- **Requires**: Visual Locomotion Policy ⚠️ ⚠️

## Source

- arxiv paper: `papers/2210.14791.pdf`

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Step over small obstacles` --uses ⚠️--> `ViNL`
