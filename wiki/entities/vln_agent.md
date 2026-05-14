---
id: vln_agent
title: VLN Agent
type: entity
tags: []
confidence: 0.8
created_at: '2026-04-30T01:24:54'
last_reinforced: '2026-04-30T01:24:54'
supersedes: []
sources:
- papers/2403.14158.pdf
source_type: arxiv_paper
---

# VLN Agent

The **VLN Agent** is an embodied AI system designed for Vision-Language Navigation tasks. It integrates visual perception and natural language understanding to navigate through 3D environments, following natural language instructions while building an episodic memory of visited locations. The agent relies on a **Volumetric Environment Representation** to achieve comprehensive 3D scene understanding, enabling robust exploration and goal-oriented movement.

## Role

The VLN Agent uses Volumetric Environment Representation to achieve comprehensive 3D scene understanding for navigation.

## Parameters

| Parameter | Value |
|-----------|-------|
| observation_type | Visual and language |
| navigation_mode | 3D exploration |

## Capabilities

- Navigates through 3D environments
- Understands natural language instructions
- Builds episodic memory of visited locations

## Relationships

| Type | Related Entity |
|------|----------------|
| uses | Volumetric Environment Representation |
| uses | Multi-Task Learning ⚠️ ⚠️ ⚠️ |
| uses | 2D-3D Sampling |
| uses | Volume State Estimation |
| part_of | Vision-Language Navigation |

## Architecture Overview

The VLN Agent processes visual and language inputs jointly, employing Multi-Task Learning ⚠️ ⚠️ ⚠️ to simultaneously learn navigation actions and scene understanding. It samples points in both 2D image space and 3D world space via 2D-3D Sampling, and maintains a **Volume State Estimation** module to track the agent’s position and environment occupancy over time. This architecture enables the agent to form episodic memories that support long-horizon planning and instruction following.

## See Also

- Vision-Language Navigation
- Volumetric Environment Representation
- Multi-Task Learning ⚠️ ⚠️ ⚠️