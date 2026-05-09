---
id: adaptive_locomotion_control
title: Adaptive Locomotion Control
type: skill
tags: []
confidence: 0.8
created_at: '2026-04-29T21:43:44'
last_reinforced: '2026-04-29T21:43:44'
supersedes: []
sources:
- papers/2405.01792.pdf
source_type: arxiv_paper
---

# Adaptive Locomotion Control

**Type:** [[Skill]] ⚠️  
**Source:** `papers/2405.01792.pdf`  
**Confidence:** 0.8 (peer-reviewed)

**Adaptive Locomotion Control** is an [[RL-based locomotion controller]] ⚠️ that enables a wheeled-legged robot to robustly traverse rough terrains, switch smoothly between walking and driving modes, and operate at high speeds. It is a key component of [[Hierarchical Reinforcement Learning]] systems.

## Parameters

| Parameter | Value |
|-----------|-------|
| Controller type | RL-based locomotion controller |
| Modes | Walking, driving |

## Capabilities

- Robust locomotion over rough terrains
- Smooth transitions between walking and driving modes
- Operates at high speeds

## Relationships

- **part_of** → [[Hierarchical Reinforcement Learning]]
- **depends_on** → [[Model-Free Reinforcement Learning]]
- **depends_on** → [[Privileged Learning]]

## Implementation

Trained using model-free RL with privileged learning; outputs motor commands for wheeled-legged robot joints. The policy learns to dynamically select walking or driving gait based on terrain and velocity commands, enabling seamless mode switching without explicit state machines.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Adaptive Locomotion Control` --[[uses]] ⚠️ ⚠️ ⚠️--> `Hierarchical Reinforcement Learning`
- `Adaptive Locomotion Control` --[[uses]] ⚠️ ⚠️ ⚠️--> `Model-Free Reinforcement Learning`
- `Adaptive Locomotion Control` --[[uses]] ⚠️ ⚠️ ⚠️--> `Privileged Learning`
