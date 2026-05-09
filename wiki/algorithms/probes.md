---
id: probes
title: ProbES
type: algorithm
tags: []
confidence: 0.8
created_at: '2026-04-29T21:13:55'
last_reinforced: '2026-04-29T21:13:55'
supersedes: []
sources:
- papers/2203.04006.pdf
source_type: arxiv_paper
---

# ProbES

**ProbES** (Prompt-Based Self-Exploration) is an algorithm for fast cross-domain adaptation in visual navigation. It leverages a [[Large-Scale Cross-Modal Pretrained Model]] ⚠️ ⚠️ (specifically [[CLIP]]) and [[Prompt-Based Learning]] to automate the generation of instruction-trajectory pairs without human labeling, enabling a navigation model to adapt to new scenes with minimal fine-tuning.

## Capabilities

- **Self-explore environments** by sampling trajectories in an unfamiliar scene.
- **Automatically generate structured instructions** by querying [[CLIP]] for semantic descriptions of sampled trajectories.
- **Fast cross-domain adaptation** via prompt-based fine-tuning of the navigation model.
- **Improved generalization** to unseen scenes compared to traditional fine-tuning or zero-shot methods.

## Method Overview

ProbES combines two key ideas: **self-exploration** of the environment and **prompt-based learning**. The algorithm first samples diverse trajectories in a new environment (e.g., a simulated home or office). For each trajectory, it uses [[CLIP]] to produce a natural language instruction that describes the visual features along the path, creating a synthetic instruction-trajectory pair. These pairs are then used to fine-tune a navigation model by optimizing prompt embeddings, not the full model weights. This prompt-based approach allows the model to quickly adapt to the new domain while retaining its pretrained knowledge.

## Parameters

| Parameter | Value |
|-----------|-------|
| Type | Prompt-based self-exploration |
| Pretrained Model | [[CLIP]] |
| Learning Paradigm | [[Prompt-Based Fine-Tuning]] ⚠️ ⚠️ |

## Dependencies & Relationships

- **Uses**: [[CLIP]]
- **Depends on**:
  - [[Large-Scale Cross-Modal Pretrained Model]] ⚠️ ⚠️
  - [[Prompt-Based Learning]]
- **Related concepts**: [[Self-Exploration]], [[Visual Navigation]], [[Domain Adaptation]] ⚠️

## See Also

- [[Prompt-Based Fine-Tuning]] ⚠️ ⚠️
- [[Cross-Modal Learning]] ⚠️
- [[Navigation Model]] ⚠️

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `ProbES` --[[extends]] ⚠️--> `CLIP`
