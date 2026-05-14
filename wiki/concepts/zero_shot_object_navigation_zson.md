---
id: zero_shot_object_navigation_zson
title: Zero-shot object navigation (ZSON)
type: concept
tags: []
confidence: 0.85
created_at: '2026-04-29T20:50:02'
last_reinforced: '2026-04-30'
supersedes: []
sources:
- papers/2511.06840.pdf
source_type: arxiv_paper
---

# Zero-shot Object Navigation (ZSON)

**Zero-shot Object Navigation (ZSON)** is a challenging problem in Embodied AI that tasks a robot with locating and navigating to a previously unseen object instance in an unfamiliar environment, without any task-specific fine-tuning or prior exposure to the target object class during training. ZSON demands strong Perceptual Understanding ⚠️ and Decision-Making ⚠️ capabilities to generalize across object categories and layouts — all without prebuilt maps or depth sensors.

## Description

ZSON is a challenging problem for household robots requiring strong perceptual understanding and decision-making. Agents must interpret natural language or visual queries about objects they have never encountered during training, then explore efficiently, recognize the target when seen, and plan a path to it—all without explicit navigation or object detection models specialized for that object class. Critically, ZSON agents operate without prebuilt maps or depth sensors, relying instead on vision-language reasoning and real-time perception to navigate novel environments.

## Capabilities

- **Zero-shot generalization ⚠️**: Navigate to previously unseen objects without task-specific training.
- **Cross-category transfer ⚠️**: Leverage semantic knowledge (e.g., from vision-language models) to recognize novel objects in context.
- **Exploration and search ⚠️**: Efficiently scan unknown environments to locate objects described only by category or appearance.
- **Generalization to unknown environments**: Adapt navigation strategies to unfamiliar layouts and lighting conditions without prior mapping.

## Relationships

- **part_of** Embodied AI – ZSON is a benchmark task within the broader field of embodied agents that interact with real or simulated environments.
- **part_of** Object Navigation ⚠️ – ZSON is a specific formulation of object‑goal navigation where the target object class has never been seen in training.
- **depends_on** Vision-Language Models ⚠️ ⚠️ – Modern ZSON systems often rely on pre-trained vision-language encoders to match queries to visual observations.
- **related_to** ObjectGoal Navigation ⚠️ – ZSON is an extreme variant of object‑goal navigation where the target object class has never been seen in training.

## Source

This page is based on the paper *RoboEXP: Action-Conditioned Embodied Exploration and Manipulation* (arXiv:2511.06840).

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Zero-shot object navigation (ZSON)` --related_to ⚠️--> `Embodied AI`