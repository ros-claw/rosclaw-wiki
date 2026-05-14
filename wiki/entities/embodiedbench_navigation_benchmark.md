---
id: embodiedbench_navigation_benchmark
title: EmbodiedBench Navigation benchmark
type: entity
tags: []
confidence: 0.8
created_at: '2026-04-30T00:03:42'
last_reinforced: '2026-04-30T00:03:42'
supersedes: []
sources:
- papers/2512.02631.pdf
source_type: arxiv_paper
---

# EmbodiedBench Navigation Benchmark

**EmbodiedBench Navigation** is a benchmark designed for evaluating embodied navigation tasks, specifically measuring the success rate of Vision-and-Language Navigation (VLN) agents. It provides a standardized framework to assess how well an agent can follow natural language instructions to reach target locations in simulated 3D environments.

## Overview

The benchmark tests the ability of VLN agents to navigate through realistic scenes while grounding language instructions in visual observations. It is used as the primary evaluation suite in the SeeNav-Agent paper.

## Capabilities

- Measures **navigation success rate** of VLN agents.
- Provides a reproducible environment for comparing different navigation policies.

## Evaluation

All reported navigation success rates in the SeeNav-Agent paper are on the EmbodiedBench Navigation benchmark. This includes results for baseline models such as GPT-4.1 and Qwen2.5-VL-3B.

## Related Entities

- Used by: SeeNav-Agent, GPT-4.1, Qwen2.5-VL-3B
- Source: paper `papers/2512.02631.pdf`

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `EmbodiedBench Navigation benchmark` --uses ⚠️--> `SeeNav-Agent`
