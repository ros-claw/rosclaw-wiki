---
id: end_to_end_learning
title: End-to-End Learning
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-30T02:48:29'
last_reinforced: '2026-04-30T02:48:29'
supersedes: []
sources:
- papers/2007.08037.pdf
source_type: arxiv_paper
---

## Overview

**End-to-End Learning** is a machine learning paradigm where the entire system—from raw sensor inputs to final control outputs—is trained jointly using a single optimization objective (e.g., reward signal). Unlike modular pipelines that decompose perception, planning, and control into separately trained components, end-to-end approaches allow the network to discover internal representations that directly optimize the desired behavior.

This approach has been applied in robotics for tasks such as visuomotor control, manipulation, and navigation. In the context of embodied intelligence, end-to-end learning can unify exploration and navigation policies, enabling the agent to learn how to collect information and move toward goals without explicit engineered submodules.

## Capabilities

- Jointly optimizes exploration and navigation policies without modular separation. Instead of handcrafting separate routines for mapping, path planning, and exploration, a single neural network learns both behaviors from reward signals, often leading to more efficient and adaptive behavior in unknown environments.

## Relationships

- **Used by**: Active Visual Information Gathering (AVIG) — End-to-end learning provides a framework for AVIG systems to simultaneously learn where to look and how to move, maximizing information gain over time.

## Related Concepts

- Reinforcement Learning (typically provides the reward signal for end-to-end training)
- Sim-to-Real Transfer (end-to-end policies often require careful domain randomization to transfer from simulation to the real world)
- Imitation Learning (an alternative to end-to-end reinforcement learning)

## Sources

- Paper: *Learning to Actively Gather Information* (arXiv:2007.08037)

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Pending review:**
- `End-to-End Learning` --related_to ⚠️--> `Active Visual Information Gathering (AVIG)` _(wikilink)_
