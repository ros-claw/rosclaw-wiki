---
id: wheeled_legged_robot
title: Wheeled-Legged Robot
type: entity
tags: []
confidence: 0.8
created_at: '2026-04-29T21:40:10'
last_reinforced: '2026-04-29T21:40:10'
supersedes: []
sources:
- papers/2405.01792.pdf
source_type: arxiv_paper
---

# Wheeled-Legged Robot

## Overview

Wheeled-legged robots combine wheeled and legged mobility for enhanced efficiency and adaptability in urban environments. This paper presents a fully integrated system using hierarchical reinforcement learning to achieve robust autonomous navigation over kilometer-scale missions. The robot adaptively switches between walking and driving, allowing it to traverse rough terrains and smooth urban surfaces with seamless transitions.

## Parameters

- **Locomotion modes**: walking and driving
- **Terrain types**: rough terrains, urban environments

## Capabilities

- Adaptive locomotion across varied terrains
- Smooth transitions between walking and driving
- Autonomous kilometer-scale navigation in cities

## Relationships

- **Uses**:
  - Model-Free Reinforcement Learning
  - Privileged Learning
  - Hierarchical Reinforcement Learning
- **Depends on**:
  - Adaptive Locomotion Control
  - Mobility-Aware Local Navigation Planning
  - Large-Scale Path Planning

## References

- Source paper: *Adaptive Locomotion and Navigation for Wheeled-Legged Robots* (arXiv:2405.01792)

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Wheeled-Legged Robot` --uses ⚠️ ⚠️ ⚠️--> `Model-Free Reinforcement Learning`
- `Wheeled-Legged Robot` --uses ⚠️ ⚠️ ⚠️--> `Privileged Learning`
- `Wheeled-Legged Robot` --uses ⚠️ ⚠️ ⚠️--> `Hierarchical Reinforcement Learning`
**Pending review:**
- `Wheeled-Legged Robot` --related_to ⚠️ ⚠️ ⚠️--> `Adaptive Locomotion Control` _(wikilink)_
- `Wheeled-Legged Robot` --related_to ⚠️ ⚠️ ⚠️--> `Mobility-Aware Local Navigation Planning` _(wikilink)_
- `Wheeled-Legged Robot` --related_to ⚠️ ⚠️ ⚠️--> `Large-Scale Path Planning` _(wikilink)_
