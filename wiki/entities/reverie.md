---
id: reverie
title: REVERIE
type: entity
tags: []
confidence: 0.9
created_at: '2026-04-30T01:07:05'
last_reinforced: '2026-04-30'
supersedes: []
sources:
- papers/2506.01551.pdf
- papers/2203.04006.pdf
- papers/2211.16649.pdf
source_type: arxiv_paper
---

# REVERIE

**REVERIE** (Remote and Embodied Referring Expression Interactions) is a **benchmark for coarse-grained instruction following** in the **vision-language navigation (VLN)** domain. It evaluates embodied agents on object-oriented navigation by testing their ability to follow natural language instructions and identify target objects in photo-realistic environments.

## Overview

REVERIE is a benchmark for coarse-grained instruction following in VLN. It provides thousands of annotated instructions paired with target objects, drawn from panoramic image datasets of real-world scenes. The benchmark assesses both navigation accuracy and object grounding at a higher semantic level than fine-grained step-by-step tasks.

## Key Features

- Large-scale collection of referring expression instructions (remote and embodied).
- Environments derived from real-world scenes (e.g., Matterport3D).
- Coarse-grained granularity: instructions describe the target object and its remote context, requiring agents to infer the route without step‑by‑step directions.
- Standardized evaluation metrics for object grounding and path completion.

## Capabilities

- Serves as a standardized **evaluation for VLN agents**.
- Requires **object grounding** and **navigation** in a unified framework.
- Demands sequential reasoning over visual observations and language instructions.
- Evaluates both path completion and object detection accuracy.

## Addressing Models

Several models have been designed to improve performance on REVERIE:

- **[[ProbES]]** improves generalization on REVERIE without requiring human-labeled data, leveraging probabilistic exploration strategies.
- **[[EvolveNav]]** uses dynamic policy evolution and has been evaluated on the REVERIE benchmark.
- **[[CLIP-Nav]]** leverages CLIP-based visual representations and has been used on the REVERIE benchmark for coarse-grained object‑grounded navigation.

## Relationships

- **is_subtask_of**: [[Visual Language Navigation (VLN)]] ⚠️
- **addressed_by**: [[ProbES]], [[EvolveNav]]
- **used_by**: [[CLIP-Nav]]
- **used_in**: Evaluation of [[EvolveNav]]

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `REVERIE` --[[uses]] ⚠️--> `EvolveNav`
- `REVERIE` --[[is_subtask_of]] ⚠️--> `Visual Language Navigation (VLN)`
- `REVERIE` --[[used_by]] ⚠️--> `CLIP-Nav`