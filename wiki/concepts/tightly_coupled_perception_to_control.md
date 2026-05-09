---
id: tightly_coupled_perception_to_control
title: Tightly coupled perception-to-control
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-29T21:32:17'
last_reinforced: '2026-04-29T21:32:17'
supersedes: []
sources:
- papers/2403.06828.pdf
source_type: arxiv_paper
---

# Tightly Coupled Perception-to-Control

**Type:** Architectural design  
**Benefit:** Reduces error propagation  

## Description

A framework where perception and control are integrated into a single learned process rather than separate modules. In this paradigm, raw sensory data (e.g., point clouds) is directly transformed into control commands, bypassing intermediate representations such as object detection maps or trajectory plans. This tight coupling aims to minimize information loss and latency that accumulate in classical modular pipelines.

The approach is exemplified by [[NeuPAN]], which takes raw point cloud as input and generates motions without relying on explicit intermediate representations like semantic maps or path plans.

## Capabilities

- Directly transforms perception into control commands  
- Improves accuracy and robustness compared to decoupled pipelines  

## Relationships

- **Contrasts with:** [[Modular Perception-Planning-Control Pipeline]] ⚠️ – the traditional architecture where perception, planning, and control operate as distinct, sequentially chained modules  
- **Used by:** [[NeuPAN]] – implements a tightly coupled perception-to-control framework powered by neural networks  

## Benefits

By fusing perception and control into a single end-to-end process, the system avoids error propagation across module boundaries. This is especially critical in dynamic or high-speed scenarios where delays from intermediate processing can degrade performance. The architecture also reduces the need for hand-engineered state representations, allowing the system to learn task-relevant features directly from sensor data.

## Related Concepts

- [[End-to-End Learning]]  
- [[Imitation Learning]]  
- [[Sensorimotor Control]] ⚠️

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Pending review:**
- `Tightly coupled perception-to-control` --[[related_to]] ⚠️--> `NeuPAN` _(wikilink)_
