---
id: navigate_to_goal_in_unfamiliar_indoor_environments
title: Navigate to goal in unfamiliar indoor environments
type: skill
tags: []
confidence: 0.8
created_at: '2026-04-30T05:03:09'
last_reinforced: '2026-04-30T05:03:09'
supersedes: []
sources:
- papers/2210.14791.pdf
source_type: arxiv_paper
---

# Navigate to Goal in Unfamiliar Indoor Environments

**Navigate to Goal** is a high-level skill that enables a mobile robot to reach distant goal coordinates in unfamiliar indoor environments using only egocentric vision. It is a core capability of the ViNL system.

## Overview

This skill allows a robot to safely navigate from its current position to a specified coordinate goal within previously unseen apartments. It does not rely on pre‑built maps or external localization; instead, it uses an end‑to‑end learned policy that processes first‑person visual input.

## Parameters

| Parameter | Value |
|-----------|-------|
| Goal format | `coordinate` (e.g., (x, y) in the environment frame) |
| Environment type | Unseen apartments |

## Capabilities

- **Reach distant goal coordinates** using only egocentric vision
- **Avoid obstacles** during navigation

## Description

The skill is performed by ViNL through the combination of two sub‑policies:

1. A **Visual Navigation Policy** → handles wayfinding (global direction toward the goal).
2. A **visual locomotion policy** → handles local obstacle avoidance and low‑level motion control.

This decomposition allows the system to navigate over long horizons while reacting to obstacles in real time, without requiring explicit mapping or planning.

## Relationships

- **Part of**: ViNL
- **Requires**: Visual Navigation Policy (for wayfinding)
- **Depends on**: visual locomotion policy (for obstacle avoidance)

## See Also

- ViNL — the overall framework that implements this skill
- Visual Navigation Policy — the higher‑level policy that provides directional commands
- Obstacle Avoidance ⚠️ — the local reactive behavior used during navigation

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Navigate to goal in unfamiliar indoor environments` --uses ⚠️--> `ViNL`
