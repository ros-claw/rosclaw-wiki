---
id: explicit_global_memory
title: Explicit Global Memory
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-30T04:39:12'
last_reinforced: '2026-04-30T04:39:12'
supersedes: []
sources:
- papers/2412.04380.pdf
source_type: arxiv_paper
---

# Explicit Global Memory

**Explicit Global Memory** is a conceptual module in embodied AI that maintains a persistent, updatable representation of the entire scene in the form of **3D Gaussians**. As the agent explores its environment, the memory is incrementally refined to reflect new observations, enabling continuous global awareness without requiring the full re-initialization of the scene.

## Core Properties

| Property | Value |
|----------|-------|
| **Storage format** | [[3D Gaussians]] ⚠️ |
| **Update mechanism** | Local refinement |
| **Primary user** | [[EmbodiedOcc]] |

## Capabilities

- Maintains a global scene representation that persists across agent motion and over time.
- Supports incremental updating — new sensor data is integrated via local refinement of the Gaussian parameters, avoiding costly global re-computation.

## Relationship with EmbodiedOcc

Explicit Global Memory is actively used by [[EmbodiedOcc]], an occupancy prediction framework for embodied agents. The memory provides the underlying scene structure that EmbodiedOcc queries to generate occupancy predictions grounded in the agent’s accumulated knowledge.

## Source

This concept is derived from the paper *EmbodiedOcc: Embodied 3D Occupancy Prediction via Vision-Language Models* (arXiv:2412.04380).

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Pending review:**
- `Explicit Global Memory` --[[related_to]] ⚠️--> `EmbodiedOcc` _(wikilink)_
