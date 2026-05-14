---
id: ha_vln_20
title: HA-VLN 2.0
type: entity
tags: []
confidence: 0.85
created_at: '2026-04-29T21:21:45'
last_reinforced: '2026-04-30'
supersedes: []
sources:
- papers/2503.14229.pdf
source_type: arxiv_paper
---

# HA-VLN 2.0

## Overview

**HA-VLN 2.0** is an open benchmark introducing explicit social-awareness constraints to Vision-and-Language Navigation (VLN). It covers both discrete and continuous environments with dynamic multi-human interactions, and extends prior VLN benchmarks by integrating dynamic human agents and social constraints into navigation tasks. The benchmark supports outdoor contexts, provides 16,844 socially grounded instructions, and includes a standardized framework for evaluating goal accuracy alongside personal-space adherence.

## Parameters

| Parameter | Value |
|-----------|-------|
| Version | 2.0 |
| Task | Socially-aware Vision-and-Language Navigation |
| Environments | Discrete, Continuous |
| Human interactions | Dynamic multi-human |
| Outdoor contexts | Yes |
| Instructions count | 16,844 |

## Capabilities

- **Standardized task and metrics** capturing goal accuracy and personal-space adherence.
- **Benchmark** on a large corpus of socially grounded instructions (16,844).
- **Real-world robot experiments** validating sim-to-real transfer.
- **Open leaderboard** for transparent comparison of methods.
- **Unified benchmark** for human-aware navigation, covering both discrete and continuous environments with dynamic multi‑human interactions.

## Components

HA-VLN 2.0 includes the following components:
- HAPS 2.0 dataset — the dataset of socially grounded instructions.
- Simulators (discrete & continuous).
- Baseline models.
- Evaluation protocols and metrics.
- An open leaderboard for benchmarking.

## Task Definition

Agents must navigate to a goal location following natural language instructions while avoiding collision with dynamic human agents and respecting personal space ⚠️. The task integrates traditional VLN objectives with social navigation constraints, requiring agents to understand both spatial goals and human–robot interaction norms. The benchmark includes outdoor scenarios and supports dynamic multi‑human interactions in both simulated and real‑world settings.

## Metrics

Performance is evaluated along two axes:

- **Goal accuracy**: Standard VLN metrics such as success rate and path-length-weighted success (SPL/B, SR).
- **Personal-space adherence**: Collision rate with dynamic humans and proximity intrusion frequency (how often the agent violates a defined personal-space buffer).

## Related Entities

- **Uses**:
  - HAPS 2.0 dataset
  - Simulators (discrete & continuous)
  - Real-world robot platform
- **Depends on**:
  - Vision-and-Language Navigation (VLN)
- **Contributes to**:
  - Human-aware Navigation
  - Socially Compliant Robot Navigation ⚠️

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `HA-VLN 2.0` --related_to ⚠️--> `Vision-and-Language Navigation`

<!-- Further details: see HA-VLN 2.0 Paper (2503.14229) ⚠️ for the original publication. -->