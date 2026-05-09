---
id: capability_conditioned_navigation_capnav
title: Capability-Conditioned Navigation (CapNav)
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-30T02:49:36'
last_reinforced: '2026-04-30T02:49:36'
supersedes: []
sources:
- papers/2602.18424.pdf
source_type: arxiv_paper
---

# Capability-Conditioned Navigation (CapNav)

## Overview

**CapNav** is a benchmark for evaluating [[Vision-Language Models]] ⚠️ ⚠️ ⚠️ on indoor navigation tasks conditioned on the agent’s physical and operational capabilities. It systematically tests how well a VLM can adapt its reasoning and behavior when the agent’s mobility, dimensions, and environmental interaction abilities vary.

CapNav defines **five representative agent types** (human and robot) with distinct constraints, enabling fine-grained assessment of capability-aware navigation. The benchmark spans **45 scenes**, **473 navigation tasks**, and **2,365 QA pairs**, making it a comprehensive resource for embodied-AI evaluation.

## Description

A benchmark for evaluating Vision-Language Models on indoor navigation tasks conditioned on the agent's physical and operational capabilities. Defines five representative human and robot agents with specific dimensions, mobility, and environmental interaction abilities.

## Dependencies

CapNav **depends on**:

- [[Vision-Language Models]] ⚠️ ⚠️ ⚠️ — the core model being evaluated
- [[Vision-Language Navigation]] — the underlying task framework

## Capabilities

CapNav is designed to:

- **Evaluate VLM navigation under mobility constraints** — tests whether the model can account for an agent’s size, speed, and access limitations (e.g., can it fit through a narrow passage? Can it open cabinets?)
- **Include spatial reasoning** — requires understanding of room layouts, object placements, and path feasibility with given agent capabilities
- **Test capability-aware navigation** — measures the model’s ability to modify its plan or query when the agent lacks certain abilities (e.g., cannot jump, cannot rotate in place)

## Parameters

| Parameter | Value |
|-----------|-------|
| Scenes    | 45    |
| Tasks     | 473   |
| QA pairs  | 2,365 |
| Agent types | 5   |

## Relationships

- **depends_on**: [[Vision-Language Models]] ⚠️ ⚠️ ⚠️, [[Vision-Language Navigation]]
- **related**: [[Embodied AI]], [[Indoor Navigation]] ⚠️, [[Sim-to-Real Transfer]]

## Usage

CapNav serves as a diagnostic tool for researchers developing VLMs for embodiment, highlighting weaknesses in capability inference and persistent spatial reasoning. It is typically used in conjunction with standard VLN benchmarks to separate general navigation ability from capability-conditioned adaptation.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Capability-Conditioned Navigation (CapNav)` --[[related_to]] ⚠️--> `Embodied AI`
