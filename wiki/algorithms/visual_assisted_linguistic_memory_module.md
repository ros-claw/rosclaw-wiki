---
id: visual_assisted_linguistic_memory_module
title: Visual-Assisted Linguistic Memory Module
type: algorithm
tags: []
confidence: 0.8
created_at: '2026-04-29T23:58:38'
last_reinforced: '2026-04-29T23:58:38'
supersedes: []
sources:
- papers/2601.08665.pdf
source_type: arxiv_paper
---

# Visual-Assisted Linguistic Memory Module

A **Visual-Assisted Linguistic Memory Module** is a persistent cross-modal semantic memory algorithm designed for embodied navigation agents. It integrates visual and linguistic modalities to construct long-term memory of past observations, enabling agents to prevent repetitive exploration and infer movement trends in dynamic environments. This module is a core component of the [[VLingNav]] system.

## Architecture

The module maintains a cross-modal memory bank that associates visual observations with linguistic descriptions to enable long-horizon recall. It stores embeddings representing observed scenes and their natural language labels, allowing the agent to query spatial information at any time during a task. The memory is persistent across episodes, providing a continuous record of the environment.

## Function

The module allows the agent to query past spatial information in order to avoid revisiting locations and predict changes in dynamic scenes. By linking visual features to linguistic descriptions, the agent can efficiently recall whether a location has been visited, what objects were present, and how the scene may have changed over time. This reduces redundant exploration and improves navigation efficiency in partially observable environments.

## Capabilities

- Constructs persistent memory of past observations.
- Prevents repetitive exploration by encoding location visitation history.
- Infers movement trends for dynamic environments, enabling prediction of scene changes.

## Relationships

- **Part of** → [[VLingNav]]
- **Depends on** → [[Persistent Memory]] ⚠️, [[Cross-modal Mapping]] ⚠️

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Visual-Assisted Linguistic Memory Module` --[[extends]] ⚠️--> `VLingNav`
