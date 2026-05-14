---
id: r2r_benchmark
title: R2R benchmark
type: entity
tags: []
confidence: 0.85
created_at: '2026-04-30T00:12:22'
last_reinforced: '2026-04-30'
supersedes: []
sources:
- papers/2409.18800.pdf
- papers/2207.11201.pdf
source_type: arxiv_paper
---

## R2R Benchmark

The **R2R benchmark** is a standard public benchmark for evaluating **vision-and-language navigation (VLN ⚠️ ⚠️)** agents. Based on the Matterport3D ⚠️ dataset, it provides room-to-room navigation tasks where agents must follow natural language instructions to traverse indoor environments. The benchmark offers standardized tasks and metrics to measure an agent’s ability to follow instructions while navigating through photorealistic scenes.

### Parameters

- **Type**: Vision-Language Navigation benchmark
- **Task**: Room-to-Room navigation (R2R) in Matterport3D

### Capabilities

- Used to evaluate VLN ⚠️ ⚠️ agents on instruction following and path planning under realistic visual conditions.
- Measures both navigation success and linguistic alignment between the instruction and the agent’s trajectory.
- Evaluates agents on following natural language instructions to navigate through indoor environments across diverse room layouts.

### Relationships

- **Evaluates** → MiniVLN, teacher model ⚠️, Target-Driven Structured Transformer Planner (TD-STP): These agents are commonly benchmarked on R2R to assess their visual grounding, language comprehension, and structured planning capabilities.
- **Used by** → TD-STP ⚠️: The Target-Driven Structured Transformer Planner is evaluated on the R2R benchmark to demonstrate its instruction-following performance in continuous environments.

### Source

- Based on the paper *“Continuous Vision-and-Language Navigation: A Bird’s-Eye View”* (arXiv:2409.18800).
- Additional references: The R2R benchmark as originally introduced with the Matterport3D dataset.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `R2R benchmark` --uses ⚠️--> `MiniVLN`