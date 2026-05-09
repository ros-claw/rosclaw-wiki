---
id: ddn
title: DDN
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-30T01:24:06'
last_reinforced: '2026-04-30T01:24:06'
supersedes: []
sources:
- papers/2406.04882.pdf
source_type: arxiv_paper
---

# DDN (Demand-Driven Navigation)

**Type:** Navigation benchmark  
**Source:** [arxiv:2406.04882](https://arxiv.org/abs/2406.04882)

## Description

DDN (Demand-Driven Navigation) is a navigation benchmark designed to evaluate goal-oriented navigation based on user demand. The robot must interpret a natural language demand (e.g., "Find a cup on the table") and navigate to the correct object. The [[InstructNav]] system achieves an 86.34% improvement over previous state-of-the-art (SOTA) methods on this benchmark.

## Capabilities

- Evaluates goal-oriented navigation grounded in user demand.
- Requires reasoning over natural language instructions to locate and approach the target object.

## Relationships

- **Used by:** [[InstructNav]] uses DDN as an evaluation benchmark.
- **Related to:** DDN is conceptually related to [[R2R-CE]] (Room-to-Room with Commonsense Extensions) and [[Habitat ObjNav]] (Object Navigation in Habitat), but differs in its emphasis on dynamic, demand-driven goals rather than static target lists.

## References

- Original paper: *InstructNav: Zero-shot System for Generic Instruction Navigation in Unexplored Environment* (arxiv:2406.04882) – introduces DDN as a benchmark for evaluating instruction-following navigation.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `DDN` --[[applies_to]] ⚠️--> `R2R-CE`
