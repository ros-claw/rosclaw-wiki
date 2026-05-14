---
id: logoplanner
title: LoGoPlanner
type: algorithm
tags: []
confidence: 0.85
created_at: '2026-04-29T21:29:07'
last_reinforced: '2026-04-30'
supersedes: []
sources:
- papers/2512.19629.pdf
source_type: arxiv_paper
---

# LoGoPlanner

## Overview

LoGoPlanner is a fully end-to-end navigation framework that integrates localization, mapping, and planning into a single learned policy. It fine‑tunes a visual‑geometry backbone to output metric‑scale predictions, reconstructs surrounding scene geometry from historical observations, and uses implicit geometry to condition the policy, reducing cumulative error. The framework unifies implicit state estimation with dense scene geometry reconstruction to achieve robust, embodiment‑agnostic navigation without a separate localization module.

## Method

The approach fine‑tunes a long‑horizon visual‑geometry backbone to predict absolute metric scale, reconstructs surrounding scene geometry from historical observations, and conditions the policy on implicit geometry bootstrapped by auxiliary tasks. The framework uses Long-horizon Visual-geometry Backbone to encode temporal visual sequences, Implicit Geometry Bootstrapping ⚠️ ⚠️ to infer latent spatial structure, and Auxiliary Task Conditioning ⚠️ ⚠️ to ground the policy in metric scale and scene geometry.

Key auxiliary tasks include:
- **Metric scale grounding** – learns to recover real‑world distances from monocular input
- **Scene geometry reconstruction** – builds a dense, fine‑grained environmental map from past frames
- **Implicit geometry bootstrapping** – closes the loop between geometry prediction and policy conditioning

## Parameters

| Parameter | Description |
|-----------|-------------|
| Type | Localization‑grounded end‑to‑end navigation framework |
| Architecture | Long‑horizon visual‑geometry backbone with auxiliary task conditioning |
| Key innovation | Metric‑aware visual geometry with implicit state estimation |
| Auxiliary tasks | Metric scale grounding, scene geometry reconstruction, implicit geometry bootstrapping |

## Capabilities

- Fully end‑to‑end trajectory planning from raw visual observations — no separate localization module required
- Implicit state estimation for accurate localization without explicit pose tracking
- Dense geometry memory for obstacle avoidance via scene geometry reconstruction
- Reduced cumulative error and cascading failures compared to modular pipelines
- Over 27.3% improvement over oracle‑localization baselines
- Strong generalization across embodiments (different robot platforms) and environments

## Results

In both simulation and real‑world settings, LoGoPlanner achieves more than **27.3% improvement** over oracle‑localization baselines in planning consistency and obstacle avoidance, while demonstrating strong generalization across embodiments and environments. The framework substantially reduces drift and failure cascades that plague traditional modular pipelines.

## Relationships

- **Uses:** Long-horizon Visual-geometry Backbone, Implicit Geometry Bootstrapping ⚠️ ⚠️, Auxiliary Task Conditioning ⚠️ ⚠️, auxiliary tasks for metric scale grounding
- **Part of:** Navigation Pipeline for Mobile Robots ⚠️
- **Depends on:** metric‑aware visual geometry, implicit state estimation, surrounding scene geometry reconstruction
- **Evaluated in:** simulation, real‑world environments
- **Contradicts:** traditional modular pipelines (perception → localization → planning) that suffer from cascading errors; end‑to‑end methods that rely on separate localization modules or explicit pose estimation

## Sources

- arXiv paper `2512.19629.pdf` – "LoGoPlanner: Localization-Grounded End-to-End Navigation with Long-Horizon Visual-Geometry"

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `LoGoPlanner` --extends ⚠️--> `Long-horizon Visual-geometry Backbone`