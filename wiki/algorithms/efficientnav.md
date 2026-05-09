---
id: efficientnav
title: EfficientNav
type: algorithm
tags: []
confidence: 1.0
created_at: '2026-04-29T21:52:53'
last_reinforced: '2026-04-30'
supersedes: []
sources:
- code/PKU-SEC-Lab_EfficientNav/README.md
source_type: official_manual
---

## EfficientNav

**EfficientNav** is a novel framework for on-device Object Goal Navigation (ObjNav) that addresses the challenges of limited model capacity in smaller LLM planners and high planning latency caused by long navigation map prompts. It achieves efficient navigation map caching and retrieval through memory-optimization techniques, enabling real-time navigation without reliance on large cloud-based planners.

### Capabilities

- Enables efficient on-device **Object Goal Navigation** using smaller LLMs.
- Reduces **KV-cache recomputation** and memory usage on local devices.
- Improves navigation success rates on the [[HM3D Dataset]].
- Outperforms [[GPT-4-based planners]] ⚠️ in success rate.
- Prunes redundant navigation map information using semantics-aware memory retrieval.
- Reuses KV cache across planning steps to lower latency and peak memory consumption.
- Recovers memory interactions lost during discretization via attention-based clustering.

### Key Features

EfficientNav incorporates three core mechanisms to reduce computational and memory overhead:

- **[[Semantics-Aware Memory Retrieval]] ⚠️** – prunes redundant information from navigation maps, keeping only semantically relevant data.
- **[[Discrete Memory Caching]] ⚠️** – saves and reuses KV-cache across steps, lowering latency and peak memory.
- **[[Attention-Based Memory Clustering]] ⚠️** – recovers memory interactions that are lost during discretization, preserving planning quality.

### Architecture & Components

EfficientNav depends on a **[[LLaVA-34b]] ⚠️** as its planner model, with a **[[CLIP]]** visual encoder and **[[GroundingDINO]] ⚠️** object detector. The system uses **KV-cache caching** to avoid repeated full inference and is integrated with the [[Habitat]] simulation platform (including both habitat-sim and habitat-lab). Related memory modules, [[Navigation Map Caching]] ⚠️ and [[Navigation Map Retrieval]] ⚠️, support the semantic retrieval pipeline.

### Evaluation & Performance

Tested on the [[HM3D Dataset]], EfficientNav significantly reduces KV-cache recomputation and memory usage while improving navigation success rates, outperforming prior methods including those powered by GPT-4. The combination of discrete memory caching and semantic pruning allows it to run effectively on resource-constrained hardware while maintaining competitive navigation performance.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `EfficientNav` --[[extends]] ⚠️--> `CLIP`