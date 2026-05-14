---
id: target_bench
title: Target-Bench
type: entity
tags: []
confidence: 0.85
created_at: '2026-04-29T21:43:26'
last_reinforced: '2026-04-30'
supersedes: []
sources:
- papers/2511.17792.pdf
source_type: arxiv_paper
---

## Target-Bench

Target-Bench is the first benchmark specifically designed to evaluate Video World Models on semantic reasoning, spatial estimation, and planning capabilities. It provides 450 robot-collected scenarios spanning 47 semantic categories, with SLAM-based trajectories serving as motion tendency references. The benchmark is accompanied by a Metric Scale Recovery Mechanism to enable accurate spatial evaluation.

### Description

Target-Bench offers the first comprehensive evaluation framework for video world models across three core capabilities: semantic reasoning (recognizing scene content and object affordances), spatial estimation (inferring metric distances and layout from video), and planning (generating goal-directed motion sequences). The dataset comprises 450 robot-collected scenarios across 47 semantic categories, each grounded by SLAM-based motion references. Evaluation relies on five complementary metrics that measure target‑approaching effectiveness and directional consistency. In initial tests, the best off‑the‑shelf model achieved an overall score of 0.341, highlighting significant room for improvement.

### Overview

The benchmark systematically assesses how well video world models can understand and act within real-world environments. Data is collected from a real robot platform, ensuring naturalistic motion and scene diversity. Each scenario includes a trajectory grounded by SLAM, enabling direct comparison between predicted motion patterns and ground‑truth robot behavior.

### Capabilities

Target-Bench evaluates the following dimensions of video world models:

- **Semantic Reasoning** – ability to recognize scene content and object affordances relevant to goal‑oriented behavior.
- **Spatial Estimation** – accurate inference of metric distances and spatial layout from video observations.
- **Planning** – generation of feasible, goal‑directed motion sequences that approach a target.

### Metrics

Five complementary metrics focus on two key performance aspects:

1. **Target-approaching capability** – how effectively the model's predicted trajectory reduces distance to the goal.
2. **Directional consistency** – how well the predicted heading matches the reference motion.

### Parameters

| Parameter | Value |
|-----------|-------|
| Number of scenarios | 450 |
| Semantic categories | 47 |
| Metrics | 5 |

### Relationships

- **uses**: Video World Models, SLAM, Metric Scale Recovery Mechanism
- **depends_on**: robot-collected scenarios, SLAM-based trajectories

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Target-Bench` --uses ⚠️ ⚠️ ⚠️--> `Video World Models`
- `Target-Bench` --uses ⚠️ ⚠️ ⚠️--> `SLAM`
- `Target-Bench` --uses ⚠️ ⚠️ ⚠️--> `Metric Scale Recovery Mechanism`
- `Target-Bench` --depends_on ⚠️--> `SLAM`-based trajectories