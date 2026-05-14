---
id: memory_augmented_hierarchical_decision_making
title: Memory-Augmented Hierarchical Decision-Making
type: algorithm
tags: []
confidence: 0.8
created_at: '2026-04-29T21:26:18'
last_reinforced: '2026-04-29T21:26:18'
supersedes: []
sources:
- papers/1909.01871.pdf
source_type: arxiv_paper
---

## Memory-Augmented Hierarchical Decision-Making

**Memory-Augmented Hierarchical Decision-Making** is a neural network architecture that integrates external memory with a multi‑level hierarchical structure to improve decision‑making in complex, long‑horizon tasks. The agent’s decisions are structured across multiple levels of abstraction, each informed by past experiences stored in a dedicated memory module.

---

### Description

The agent’s decision‑making is structured hierarchically with a memory component that stores past experiences to inform current actions. This allows the system to reason over temporal dependencies, retain useful knowledge, and reuse strategies across episodes. The hierarchy models different granularities of action selection, from high‑level goals to low‑level motor commands.

---

### Architecture

- **Type**: Memory‑augmented neural network with hierarchical levels  
- **Levels**: Multiple decision‑making levels (exact number not specified in the original source)  
- **Memory module**: Stores and retrieves past trajectories, outcomes, or state‑action pairs to guide current choices  
- **Hierarchy**: Combines abstract (task‑oriented) and concrete (execution‑oriented) reasoning  

---

### Capabilities

- Integrates memory to improve decision‑making over time  
- Models multiple levels of abstraction in decisions  
- Supports long‑term credit assignment  
- Enables knowledge transfer across similar tasks  

---

### Relationships

- **HANNA Agent** — This algorithm is part of the HANNA Agent system. It provides the decision‑making backbone for the HANNA agent.  
- **Retrospective Curiosity-Encouraging Imitation Learning** (RCIL) — The algorithm is trained using RCIL, a method that combines imitation learning with intrinsic curiosity rewards.  

---

### Usage Context

Memory‑augmented hierarchical decision‑making is particularly suitable for environments that require long‑term reasoning, partial observability, or hierarchical task decomposition, such as embodied AI, robotics, and simulation‑based training.

---

### References

- Source paper: [1909.01871] *HANNA: Hierarchical Attention Neural Network with Memory for Long‑Horizon Decision Making* (arXiv)

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Memory-Augmented Hierarchical Decision-Making` --implements ⚠️--> `HANNA Agent`
- `Memory-Augmented Hierarchical Decision-Making` --extends ⚠️--> `Retrospective Curiosity-Encouraging Imitation Learning`
