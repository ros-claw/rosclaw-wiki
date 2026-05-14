---
id: haps_20_dataset
title: HAPS 2.0 dataset
type: entity
tags: []
confidence: 0.85
created_at: '2026-04-29T21:22:16'
last_reinforced: '2026-04-30'
supersedes: []
sources:
- papers/2503.14229.pdf
source_type: arxiv_paper
---

## HAPS 2.0

**HAPS 2.0** is an enhanced dataset for human-aware navigation, providing socially grounded instructions in both discrete and continuous environments with dynamic multi-human interactions. It is part of the larger **HA-VLN 2.0** framework, which targets language-guided navigation with human interaction awareness.

### Overview

- **Type:** Dataset  
- **Task:** Human-aware navigation  
- **Environment types:** outdoor, indoor  
- **Size:** 16,844 socially grounded instructions  
- **Key features:**  
  - Multi-human interactions – agents co-exist and influence navigation paths  
  - Language-motion alignment – fine-grained correspondence between natural language instructions and robot motion in social contexts  
  - Outdoor context support – extends human-aware navigation beyond controlled indoor settings to realistic outdoor scenes  

### Description

HAPS 2.0 is an enhanced dataset for human-aware navigation, providing socially grounded instructions in both discrete and continuous environments with dynamic multi-human interactions. It models multiple human agents whose behaviors influence the robot’s path, enabling training and evaluation of socially-aware navigation agents under realistic social constraints.

### Capabilities

HAPS 2.0 enables:

- **Models multi-human interactions** – captures the complexity of navigating around groups of people with diverse behaviors.  
- **Outdoor context support** – extends human-aware navigation beyond controlled indoor settings to realistic outdoor scenes.  
- **Finer language-motion alignment** – provides tightly coupled instruction-motion pairs that reflect social constraints (e.g., passing on the right, pausing for crossing pedestrians).  
- **Supports training and evaluation** – of socially-aware navigation agents and baselines.  
- **Diverse human interaction scenarios** – covers a wide variety of pedestrian behaviors and group dynamics.  

### Relationships

- **Part of:** HA-VLN 2.0 – HAPS 2.0 is the socially-grounded dataset component within the larger HA-VLN 2.0 ecosystem.  
- **Used by:** Navigation Agents ⚠️ and baselines for benchmarking social navigation.  
- **Depends on:** Human-aware Navigation principles, Language-Motion Alignment ⚠️ techniques, and simulation backends (e.g., Habitat Sim).  
- **Supports:** Social Navigation ⚠️ benchmarks and evaluation of VLA Models ⚠️ for real-world interaction.  

### Source

- Derived from *arxiv paper 2503.14229.pdf* (available in `data/raw/papers/`).

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `HAPS 2.0 dataset` --depends_on ⚠️--> `HA-VLN 2.0`