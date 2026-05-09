---
id: instructnav
title: InstructNav
type: algorithm
tags: []
confidence: 0.8
created_at: '2026-04-30T01:21:48'
last_reinforced: '2026-04-30T01:21:48'
supersedes: []
sources:
- papers/2406.04882.pdf
source_type: arxiv_paper
---

# InstructNav

**InstructNav** is a zero-shot system for generic instruction navigation in unexplored environments. It unifies planning via [[Dynamic Chain-of-Navigation]] and converts plans to robot trajectories via [[Multi-sourced Value Maps]].

## Overview

InstructNav tackles diverse instruction-following navigation tasks without any navigation training. It operates in previously unseen environments and does not require pre-built maps, making it the first zero-shot system capable of performing on the [[R2R-CE]] benchmark.

## Parameters

- **Zero-shot**: `true`  
- **Requires training**: `false`  
- **Requires pre-built maps**: `false`

## Capabilities

- Handles diverse instruction navigation tasks without navigation training
- Operates in unexplored environments without pre-built maps
- First zero-shot system for the [[R2R-CE]] task

## Related Components

InstructNav `uses`:
- [[Dynamic Chain-of-Navigation]] – plan synthesis from natural language instructions
- [[Multi-sourced Value Maps]] – converts high-level plans into robot trajectories

## Evaluation

InstructNav has been `tested_on`:
- [[R2R-CE]] (Room-to-Room with Continuous Environment)
- [[Habitat ObjNav]] (Object Navigation in Habitat)
- [[DDN]] (Diverse Domain Navigation)

## References

- arXiv paper 2406.04882 – *InstructNav: Zero-Shot System for Generic Instruction Navigation in Unexplored Environments* (source: `data/raw/papers/2406.04882.pdf`)

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `InstructNav` --[[implements]] ⚠️--> `R2R-CE`
