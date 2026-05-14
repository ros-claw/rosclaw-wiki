---
id: dynamic_chain_of_navigation
title: Dynamic Chain-of-Navigation
type: algorithm
tags: []
confidence: 0.8
created_at: '2026-04-30T01:22:07'
last_reinforced: '2026-04-30T01:22:07'
supersedes: []
sources:
- papers/2406.04882.pdf
source_type: arxiv_paper
---

# Dynamic Chain-of-Navigation (DCoN)

**Dynamic Chain-of-Navigation (DCoN)** is a planning algorithm that unifies the process for different types of navigation instructions. It converts linguistic instructions into a chain of navigation steps, enabling zero-shot planning across instruction types. DCoN is a core component of the InstructNav framework.

## Purpose

The primary purpose of DCoN is to bridge the gap between diverse natural language instructions and actionable navigation plans. By decomposing varied instruction formats into a common chain of subtasks, InstructNav can handle instructions that mix spatial, temporal, and object‑referential elements without requiring task‑specific training.

## Capabilities

- **Linguistic to step conversion**: Transforms natural language instructions into an ordered sequence of navigation subtasks.
- **Zero‑shot planning**: Generalizes to instruction types not seen during training, adapting the chain structure dynamically.
- **Unified representation**: Encodes all instruction types into the same schema, simplifying downstream execution by InstructNav’s planning module.

## Relationships

- **`part_of`** InstructNav — DCoN is the planning backbone that generates the chain of steps consumed by the rest of the system.
- **`depends_on`** Vision-Language Models ⚠️ — DCoN likely leverages pre‑trained VLMs to parse instructions and ground them in visual observations.
- **`implements`** Task Decomposition ⚠️ — This algorithm embodies the concept of breaking complex navigation commands into sub‑goals.

## References

- Based on the paper “InstructNav: Zero-Shot System for Generic Instruction Navigation in Unexplored Environments” (arXiv:2406.04882).