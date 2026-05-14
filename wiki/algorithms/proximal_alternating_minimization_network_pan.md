---
id: proximal_alternating_minimization_network_pan
title: Proximal Alternating-minimization Network (PAN)
type: algorithm
tags: []
confidence: 0.8
created_at: '2026-04-29T21:30:00'
last_reinforced: '2026-04-29T21:30:00'
supersedes: []
sources:
- papers/2403.06828.pdf
source_type: arxiv_paper
---

# Proximal Alternating-minimization Network (PAN)

**Type:** Algorithm  
**Related to:** NeuPAN

**Overview**  
PAN is a plug-and-play proximal alternating-minimization network that acts as the core solver within the NeuPAN framework. It is designed to handle numerous point-level constraints simultaneously, enabling real‑time generation of collision‑free robot motion.

## Description

PAN solves constrained optimization problems by alternating minimization in a learned, proximal fashion. Its architecture embeds “neurons in the loop,” meaning the network’s internal computations directly incorporate the physical constraints that must be satisfied. This design produces outputs that are not only feasible but also physically interpretable.

## Parameters

| Attribute | Value |
|-----------|-------|
| Type | Plug-and-play network |
| Role | Solves point-level constraints in NeuPAN |
| Learning method | Backpropagation fine-tuning |
| Architectural feature | Neurons in the loop |

## Capabilities

- **Real‑time motion generation** – PAN efficiently processes the large number of constraints typical of robot motion planning, producing collision‑free trajectories at rates suitable for online control.
- **Physically interpretable outputs** – Because the network’s internal states correspond to physically meaningful quantities (e.g., distances, forces), its decisions can be inspected and understood.
- **Seamless integration of data and knowledge engines** – PAN bridges learning‑based components (data‑driven models) with explicit constraint solvers (knowledge‑driven optimization), making it a hybrid approach.

## Relationships

- `part_of:: NeuPAN` – PAN is a core solver module inside the NeuPAN algorithm.
- `used_by:: NeuPAN` – NeuPAN calls PAN to enforce point‑level constraints throughout its motion planning pipeline.
- `depends_on:: NeuPAN` – PAN operates only within the context of the larger NeuPAN framework.

**Relation annotations**  
- Implements: proximal alternating minimization for constrained motion.  
- Used by: NeuPAN.  
- Supports: collision‑free trajectory generation in real time.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Proximal Alternating-minimization Network (PAN)` --extends ⚠️--> `NeuPAN`
