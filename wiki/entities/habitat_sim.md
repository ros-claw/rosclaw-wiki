---
id: habitat_sim
title: Habitat-Sim
type: entity
tags: []
confidence: 0.95
created_at: '2026-04-30T04:46:21'
last_reinforced: '2026-04-30T04:46:21'
supersedes: []
sources:
- code/TidalHarley_NavSpace/README.md
source_type: official_manual
---

## Overview

**Habitat-Sim** is a high-performance 3D simulator for embodied AI research, developed by Meta AI (FAIR). It provides photorealistic rendering of large-scale indoor environments and serves as the core simulation backend for trajectory generation, annotation, and evaluation in [[NavSpace]] and [[SNav]].

## Capabilities

- Renders complex 3D indoor scenes with dynamic lighting and object interactions.
- Supports standard asset datasets, including [[HM3D]] and [[MP3D]].
- Exposes a Python API for programmatic control of agents, sensors, and scene configurations.

## Relationships

- **used_by**: [[NavSpace]], [[SNav]], [[Annotation Pipeline]] ⚠️ (for trajectory annotation and agent evaluation)
- **depends_on**: [[HM3D]], [[MP3D]] (for scene assets)

## Role in NavSpace

Habitat-Sim is the core simulation backend for both trajectory annotation and agent evaluation in [[NavSpace]]. It provides the rendering engine that generates visual observations for human annotators and automated validation pipelines, ensuring consistent environments across all stages of the NavSpace workflow.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Habitat-Sim` --[[uses]] ⚠️--> `SNav`
