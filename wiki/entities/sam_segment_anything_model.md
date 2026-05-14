---
id: sam_segment_anything_model
title: SAM (Segment Anything Model)
type: entity
tags: []
confidence: 0.85
created_at: '2026-04-29T20:59:49'
last_reinforced: '2026-04-30'
supersedes: []
sources:
- papers/2407.05890.pdf
source_type: arxiv_paper
---

# SAM (Segment Anything Model)

**SAM** (Segment Anything Model) is a large-scale vision foundation model developed by Meta AI for interactive and automatic segmentation of any object in images. In the context of embodied intelligence and robotic navigation, SAM has been repurposed to segment visible ground regions, enabling visual affordance detection for path planning.

## Overview

SAM is trained on the SA-1B dataset, which contains over 1 billion masks across 11 million images. It supports three input modalities: point prompts, box prompts, and fully automatic mask generation. Its zero-shot generalization makes it highly adaptable to domain-specific tasks without fine-tuning.

## Capabilities

- **Segmentation of visible ground for navigational affordances** – SAM is used to extract drivable terrain or walkable surfaces from egocentric camera views, providing an explicit "ground mask" that serves as a spatial constraint for Visual Affordances Prompting ⚠️ ⚠️ ⚠️.
- **Ground segmentation for affordances extraction** – This capability is further leveraged by other planners that require precise terrain delineation.

## Usage

SAM is employed as a pre-processing step in the Visual Affordances Prompting ⚠️ ⚠️ ⚠️ pipeline. The raw image is passed to SAM with a foreground/background prompting strategy, and the resulting ground segmentation mask is combined with affordance features to guide robot locomotion. Additionally, SAM is used as a component in the AO-Planner system, where its ground segmentation output provides the spatial affordance cues needed for obstacle-aware path planning.

## Relationships

- **Used by**
  - Visual Affordances Prompting ⚠️ ⚠️ ⚠️ – SAM provides the ground segmentation masks that are critical for deriving navigational affordances.
  - AO-Planner – SAM's ground segmentation is integrated into the planner to supply terrain affordances for safe navigation.
- **Depends on** No external dependencies (runs as a standalone model).

## References

- Kirillov, A., et al. (2023). *Segment Anything*. arXiv:2304.02643.
- Usage in embodied navigation documented in [Visual Affordances Prompting](https://arxiv.org/abs/2407.05890) (2024).