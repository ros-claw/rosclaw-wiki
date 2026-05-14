---
id: personal_space_adherence
title: Personal-Space Adherence
type: concept
tags: []
confidence: 0.85
created_at: '2026-04-29T21:23:59'
last_reinforced: '2026-04-30'
supersedes: []
sources:
- papers/2503.14229.pdf
source_type: arxiv_paper
---

## Definition

**Personal-Space Adherence** is a metric that quantifies the degree to which a navigating agent avoids intruding into the personal space of humans. It measures how well a robot respects the social distances and comfort zones of humans during navigation, and belongs to the family of Human-Aware Navigation constraints. It is a standard component of the HA-VLN 2.0 metrics ⚠️ ⚠️ suite, used within the HA-VLN 2.0 benchmark ⚠️ ⚠️ to evaluate socially-aware navigation policies.

## Parameters

| Parameter | Value |
|-----------|-------|
| **metric_type** | navigation constraint |
| **scale** | distance-based |

The metric operates on a distance-based scale, evaluating the minimum separation between the agent and any human over a trajectory or at discrete decision points.

## Capabilities

- Measures how well an agent respects human personal space.
- Provides a quantitative score that can be used to compare navigation policies.
- Integrates into reward functions or evaluation benchmarks for Socially-Aware Navigation ⚠️.
- Serves as a standard metric for evaluating socially-aware navigation behaviors.

## Relationships

- **part_of** → Human-Aware Navigation
- **part_of** → HA-VLN 2.0 metrics ⚠️ ⚠️
- **measured_in** → HA-VLN 2.0 benchmark ⚠️ ⚠️
- **implements** a Navigation Constraint ⚠️ for human-centric environments.
- **depends_on** → Human Personal Space ⚠️ models (e.g., proxemics zones).
- **uses** a Distance-based Metric ⚠️ to compute intrusion or comfort loss.

## Usage

Personal-Space Adherence is typically computed by:
1. Defining a personal-space zone around each human (e.g., 0.45–1.2 m for social distance).
2. Tracking the agent's minimum distance to any human during navigation.
3. Transforming the distance into a score (e.g., 1 if always outside the zone, 0 if inside).

It is often combined with other metrics such as path efficiency, goal success rate, and human comfort to form a holistic evaluation of robot behavior in crowded environments.

## Source

- ArXiv paper: [2503.14229](https://arxiv.org/abs/2503.14229) – *HA-VLN 2.0: A Benchmark for Human-Aware Visual Language Navigation* (2025).  
  This metric is defined as part of the HA-VLN 2.0 evaluation protocol.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Personal-Space Adherence` --related_to ⚠️--> `Human-Aware Navigation`