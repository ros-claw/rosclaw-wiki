---
id: r2r
title: R2R
type: entity
tags: []
confidence: 0.8
created_at: '2026-04-30T01:06:22'
last_reinforced: '2026-04-30T01:06:22'
supersedes: []
sources:
- papers/2506.01551.pdf
source_type: arxiv_paper
---

# R2R (Room-to-Room) Benchmark

The **R2R** (Room-to-Room) benchmark is a standard evaluation task in Vision-and-Language Navigation ([[VLN]] ⚠️). It tests the ability of embodied agents to follow natural language instructions and navigate through photorealistic indoor environments (primarily from the [[Matterport3D]] ⚠️ dataset). In the R2R task, an agent is given a natural language instruction and must traverse a path through a sequence of connected viewpoints to reach a target location.

## Role in EvolveNav

R2R is used as the primary evaluation benchmark for the [[EvolveNav]] framework. The benchmark **tests** various [[VLN models]] ⚠️ ⚠️ on instruction-following and path completion. EvolveNav itself is evaluated on R2R to assess improvements in navigation policies through evolutionary optimization.

## Relationships

- **tests** → [[VLN models]] ⚠️ ⚠️: The R2R benchmark measures model performance on metric such as success rate, path length, and navigation error.
- **evaluated_by** → [[EvolveNav]]: EvolveNav uses R2R as its core test environment to validate its evolutionary training methods.

## Parameters

| Parameter | Value |
|-----------|-------|
| Type | VLN benchmark |
| Used in | [[EvolveNav]] evaluation |

## Notes

- R2R was proposed by Anderson et al. (2018) and remains a foundational benchmark in embodied AI.
- Instructions are collected via Amazon Mechanical Turk and aligned to ground-truth trajectories in Matterport3D scans.
- The benchmark includes training, validation, and test splits (with and without known environments).

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `R2R` --[[uses]] ⚠️--> `EvolveNav`
