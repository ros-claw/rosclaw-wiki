---
id: jetson_orin_agx
title: Jetson Orin AGX
type: entity
tags: []
confidence: 0.85
created_at: '2026-04-29T20:48:03'
last_reinforced: '2026-04-29'
supersedes: []
sources:
- papers/2409.11764.pdf
source_type: arxiv_paper
---

### Jetson Orin AGX

**Overview**

The Jetson Orin AGX is an embedded computing platform manufactured by [[NVIDIA]] ⚠️, designed for high-performance, real-time inference in robotics and autonomous systems. In the [[OneMap]] paper, the Jetson Orin AGX is used as the onboard computer to run open-vocabulary feature extraction and semantic mapping at real-time rates, demonstrating its capability to handle complex vision models without cloud dependency.

**Capabilities**

- Real-time inference for vision and mapping
- Real-time inference for open-vocabulary feature extraction
- Runs the [[OneMap]] method at real-time rates, enabling efficient open-vocabulary mapping and object navigation on a mobile robot
- Supports open-vocabulary vision models

**Relevance to Embodied AI**

The Jetson Orin AGX enables deployment of computationally intensive semantic mapping pipelines on mobile robots, eliminating the need for cloud connectivity. This makes it a key enabler for autonomous navigation systems that rely on large vision-language models for environment understanding.

**Relationships**

- **Used by**: [[OneMap]] (as the onboard computing platform)
- **Depends on**: None (no external dependencies listed in the source; the platform itself provides the necessary compute resources)

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Jetson Orin AGX` --[[uses]] ⚠️--> `OneMap`