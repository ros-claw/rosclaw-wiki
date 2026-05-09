---
id: target_driven_structured_transformer_planner_td_stp
title: Target-Driven Structured Transformer Planner (TD-STP)
type: algorithm
tags: []
confidence: 0.8
created_at: '2026-04-30T02:05:55'
last_reinforced: '2026-04-30T02:05:55'
supersedes: []
sources:
- papers/2207.11201.pdf
source_type: arxiv_paper
---

## Target-Driven Structured Transformer Planner (TD-STP)

**TD-STP** is a structured transformer planner for [[Vision-Language Navigation]] that explicitly estimates long-term navigation targets in unexplored environments and incorporates room layout for global planning. It achieves state-of-the-art results on both the [[R2R benchmark]] and [[REVERIE benchmark]].

### Summary
TD-STP is a structured transformer planner that explicitly estimates long-term navigation targets and incorporates room layout for global planning, achieving state-of-the-art results on R2R and REVERIE.

### Capabilities
- Explicit estimation of long-term navigation target in unexplored environments
- Global planning incorporating explored room layout via structured attention
- Long-horizon goal-guided and room layout-aware navigation

### Components
- **Imaginary Scene Tokenization**: Used for target estimation.
- **Structured Transformer Planner**: Used for incorporating room layout.

### Benchmarks and Performance
- On [[R2R benchmark]]: +2% success rate improvement over prior state-of-the-art.
- On [[REVERIE benchmark]]: +5% success rate improvement over prior state-of-the-art.

### Related Entities
- **Uses**: [[Imaginary Scene Tokenization]] ⚠️, [[Structured Transformer Planner]] ⚠️
- **Depends on**: [[Vision-Language Navigation]], [[Transformer architecture]] ⚠️
- **Evaluated on**: [[R2R benchmark]], [[REVERIE benchmark]]

### Code Availability
The implementation is available at: [https://github.com/YushengZhao/TD-STP](https://github.com/YushengZhao/TD-STP)