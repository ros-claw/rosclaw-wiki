---
id: ovon
title: OVON
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-29T23:57:14'
last_reinforced: '2026-04-29T23:57:14'
supersedes: []
sources:
- papers/2509.16445.pdf
source_type: arxiv_paper
---

# Open-Vocabulary Object Navigation (OVON)

**OVON** (Open-Vocabulary Object Navigation) is a concept in embodied AI that extends the traditional [[ObjectNav]] task by requiring agents to navigate to objects belonging to **unseen categories** — categories not present in the training data. This tests the agent's ability to generalize beyond a fixed vocabulary of object classes.

## Description

Open-Vocabulary Object Navigation (OVON) is a training task and evaluation paradigm that challenges agents to locate and reach objects whose category names were never encountered during training. Traditional ObjectNav benchmarks (e.g., [[HM3D-ObjectNav]] ⚠️) assume a closed set of target categories; OVON removes this assumption, forcing agents to rely on semantic understanding, visual grounding, and zero-shot generalization.

OVON data is included as one of the core components of the [[FiLM-Nav]] training mixture. By incorporating OVON examples, FiLM-Nav improves its ability to handle novel object categories at inference time, leading to better generalization performance on benchmarks like [[HM3D-OVON]].

## Parameters

| Parameter | Value |
|-----------|-------|
| Full form | **Open-Vocabulary Object Navigation** |
| Benchmark | [[HM3D-OVON]] |
| Primary metrics | [[SPL]] (Success weighted by Path Length), [[Success Rate]] ⚠️ |

## Capabilities

- **Training task for navigation**: Used as a supervised learning objective to teach agents how to locate objects in 3D environments.
- **Generalization to unseen object categories**: Evaluates and improves the model's ability to handle objects not seen during training, critical for real-world deployment where category lists are unbounded.

## Relationships

- **`part_of`** [[FiLM-Nav]] training mixture — OVON data is one of several tasks in the FiLM-Nav multi-task learning setup.
- **`used_in`** [[HM3D-OVON]] benchmark — The HM3D-OVON benchmark is the primary evaluation suite for OVON capabilities.

> **Note**: OVON should not be confused with [[Grounded Open-Vocabulary Object Navigation]] ⚠️, which integrates grounding mechanisms for object detection. OVON is a purely navigation-oriented task formulation.

## Benchmark Details

The HM3D-OVON benchmark uses scenes from the [[HM3D dataset]] and defines target categories that are disjoint between training and evaluation splits. Metrics are computed over multiple episodes per scene, measuring both efficiency (SPL) and task completion (success rate). For more details on the metrics, see [[Navigation Metrics]] ⚠️.

## Related Concepts

- [[Zero-shot Navigation]]
- [[Open-Vocabulary Detection]] ⚠️
- [[Semantic Navigation]] ⚠️
- [[FiLM Conditioned Vision-Language Model]] ⚠️
- [[Embodied AI Generalization]] ⚠️

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `OVON` --[[related_to]] ⚠️ ⚠️--> `HM3D-OVON`
**Pending review:**
- `OVON` --[[related_to]] ⚠️ ⚠️--> `FiLM-Nav` _(wikilink)_
