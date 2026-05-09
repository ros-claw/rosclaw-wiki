---
id: room_to_room_r2r_benchmark
title: Room-to-Room (R2R) benchmark
type: entity
tags: []
confidence: 0.8
created_at: '2026-04-30T02:48:45'
last_reinforced: '2026-04-30T02:48:45'
supersedes: []
sources:
- papers/1909.02244.pdf
source_type: arxiv_paper
---

## Room-to-Room (R2R) benchmark

The **Room-to-Room (R2R) benchmark** is a standard dataset and evaluation framework for the [[Vision-and-Language Navigation (VLN)]] ⚠️ ⚠️ ⚠️ ⚠️ task. It consists of natural language navigation instructions paired with corresponding paths through real, visually rich indoor environments (e.g., multiple floors of buildings). The benchmark is designed to measure how well an agent can follow human‑written instructions to navigate from a starting location to a goal in previously unseen environments.

### Metrics

The primary evaluation metric for the R2R benchmark is **Success Rate weighted by Path Length (SPL)**, which balances the agent's ability to reach the goal (success) with the efficiency of the chosen path relative to the optimal path. Other common metrics include **Success Rate (SR)** and **Navigation Error (NE)**.

### Capabilities

- **Evaluate VLN agent performance** in realistic, complex indoor spaces.
- Provide a controlled, reproducible testbed for comparing different [[Vision-and-Language Navigation (VLN)]] ⚠️ ⚠️ ⚠️ ⚠️ models and training paradigms.
- Support both **single‑path** and **multi‑path** instruction‑following scenarios.

### Relationships

- **part_of**: [[Vision-and-Language Navigation (VLN)]] ⚠️ ⚠️ ⚠️ ⚠️ – the R2R benchmark is a foundational component of the VLN research area.
- **uses**: [[Success Rate weighted by Path Length (SPL)]] ⚠️ as its official metric.
- **depends_on**: Real‑world visual data (RGB and depth) from the [[Matterport3D]] ⚠️ ⚠️ dataset, which provides the panoramic image views used in the R2R environments.

### See Also

- [[Matterport3D]] ⚠️ ⚠️ – the source of the visual environments.
- [[Vision-and-Language Navigation (VLN)]] ⚠️ ⚠️ ⚠️ ⚠️ – the broader research field.
- [[SPL (Success Rate weighted by Path Length)]] ⚠️ – the main evaluation metric.
- [[Room‑to‑Room (R2R) dataset]] ⚠️ – the specific set of instruction‑path pairs.