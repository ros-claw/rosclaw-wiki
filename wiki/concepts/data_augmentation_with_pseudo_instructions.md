---
id: data_augmentation_with_pseudo_instructions
title: Data augmentation with pseudo instructions
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-30T02:02:07'
last_reinforced: '2026-04-30T02:02:07'
supersedes: []
sources:
- papers/2305.11918.pdf
source_type: arxiv_paper
---

# Data augmentation with pseudo instructions

## Definition

**Data augmentation with pseudo instructions** is a technique used in Vision-and-Language Navigation (VLN) training to improve model generalization. It generates additional training data by having an independent speaker model produce synthetic natural language instructions for unlabeled navigation trajectories. This expands the training set beyond human‑annotated data, helping the agent learn to follow instructions in novel environments.

## Capabilities

- Generates additional training data using an independent speaker model.

## Relationships

- **used_in**: Vision-and-Language Navigation training — the pseudo instructions augment the standard VLN dataset.
- **improved_by**: PASTS (Progress-Aware Spatio-Temporal Transformer Speaker) — a more advanced speaker model that yields higher‑quality pseudo instructions.

## Description

By decoupling instruction generation from the navigation task, this method allows leveraging large amounts of unlabeled trajectory data. The speaker model, often a transformer or recurrent network, takes a path through an environment and outputs a plausible instruction in natural language. The resulting paired data (path + pseudo instruction) is then used to train the navigation agent, improving its robustness to instruction variability and environment diversity.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Data augmentation with pseudo instructions` --related_to ⚠️--> `Vision-and-Language Navigation`
