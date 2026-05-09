---
id: data_augmentation_via_speaker_model
title: Data Augmentation via Speaker Model
type: algorithm
tags: []
confidence: 0.8
created_at: '2026-04-30T02:46:58'
last_reinforced: '2026-04-30T02:46:58'
supersedes: []
sources:
- papers/1806.02724.pdf
source_type: arxiv_paper
---

## Data Augmentation via Speaker Model

**Data Augmentation via Speaker Model** is a technique used in [[Vision-and-Language Navigation]] to synthetically expand the training dataset by generating new natural-language instructions for existing visual trajectories. It is a core component of the **Speaker-Follower Model**.

### Overview

In vision-and-language navigation, obtaining large-scale human-annotated instruction–trajectory pairs is expensive and time-consuming. The Speaker Model addresses this by learning to produce realistic instructions from a given path in a visual environment. These synthetic pairs are then used to augment the original training set, effectively multiplying the available data without additional human effort.

### Parameters

| Parameter | Description |
|-----------|-------------|
| **Source** | A pre-trained speaker model, itself trained on existing human instruction–trajectory pairs |
| **Output** | New synthetic instruction–trajectory pairs that follow the same distribution as real annotations |

### Capabilities

- **Increases training data quantity** — enables training on a much larger pool of examples.
- **Reduces overfitting** — the expanded dataset improves generalization to unseen environments.
- **Enables learning from unannotated trajectories** — any path for which a visual representation exists can be paired with a synthetic instruction, even if no human annotation was collected.

### Relationships

- **Depends on**: [[Speaker-Follower Model]] (the speaker component must first be trained on real data)
- **Part of**: [[Speaker-Follower Model]] (this augmentation strategy is integral to the original architecture)

### Usage in Training

The augmented dataset—composed of real human annotations plus synthetic instructions from the speaker model—is used to train the follower (or navigator) agent. This approach was first introduced in the paper *"Vision-and-Language Navigation: Interpreting Visually-Grounded Navigation Instructions in Real Environments"* (Anderson et al., 2018) and has become a standard baseline for many subsequent VLN methods.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Data Augmentation via Speaker Model` --[[based_on]] ⚠️--> `Vision-and-Language Navigation`
- `Data Augmentation via Speaker Model` --[[extends]] ⚠️--> `Speaker-Follower Model`
