---
id: panonav
title: PanoNav
type: algorithm
tags: []
confidence: 0.85
created_at: '2026-04-29T20:49:47'
last_reinforced: '2026-04-30'
supersedes: []
sources:
- papers/2511.06840.pdf
source_type: arxiv_paper
---

# PanoNav

**PanoNav** is a fully **RGB-only**, mapless **Zero-Shot Object Navigation (ZSON)** framework that integrates a [[Panoramic Scene Parsing module]] ⚠️ ⚠️ and a [[Memory-guided Decision-Making]] mechanism enhanced by a [[Dynamic Bounded Memory Queue]] to avoid local deadlocks. It leverages the semantic understanding of [[Multimodal Large Language Models (MLLMs)]] ⚠️ ⚠️ to operate without explicit maps or depth sensors.

## Overview

PanoNav addresses the challenge of mobile robot object navigation in unseen environments without prior maps. The system relies solely on RGB camera input, processing panoramic images to parse the surrounding scene. A dynamic memory queue stores recent observations and decision contexts, allowing the robot to recover from repetitive or deadlocked states. The framework integrates multiple modules: panoramic perception, memory management, and MLLM-based decision reasoning.

## Parameters

| Parameter | Value |
|-----------|-------|
| Input type | RGB-only |
| Navigation type | Mapless |
| Memory system | Dynamic Bounded Memory Queue |

## Capabilities

- **Zero-shot object navigation** in unseen environments – requires no prior map, no depth sensor, and no task-specific fine-tuning.
- **Mapless operation** using only a single RGB camera – the robot explores and locates target objects without constructing a metric map.
- **Panoramic scene parsing** – constructs a structured representation of the environment from a single 360° camera image.
- **Memory-guided decision-making** with a Dynamic Bounded Memory Queue – prevents local deadlocks by maintaining a bounded history of actions and observations.
- **Outperforms baselines** on Success Rate (SR) and Success weighted by Path Length (SPL) metrics across multiple evaluation scenarios.

## Relationships

- **uses**:
  - [[Multimodal Large Language Models (MLLMs)]] ⚠️ ⚠️
  - [[Panoramic Scene Parsing module]] ⚠️ ⚠️
  - [[Memory-guided Decision-Making]]
  - [[Dynamic Bounded Memory Queue]]
- **depends_on**:
  - [[RGB-only perception]] ⚠️
  - [[RGB camera]] ⚠️

## References

- Source: *PanoNav: Mapless Zero-Shot Object Navigation with Panoramic Scene Understanding* (arXiv:2511.06840)