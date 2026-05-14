---
id: driving_videos
title: driving videos
type: entity
tags: []
confidence: 0.8
created_at: '2026-04-30T01:11:47'
last_reinforced: '2026-04-30T01:11:47'
supersedes: []
sources:
- papers/2402.03561.pdf
source_type: arxiv_paper
---

# Driving Videos

Driving videos are a resource of real-world footage collected from vehicles traveling through multiple cities in the U.S. Their diversity—covering varied outdoor environments such as urban streets, highways, suburbs, and rural roads—makes them a valuable source of scenes for outdoor Vision-and-Language Navigation (VLN) ⚠️ tasks.

## Description

Driving videos from U.S. cities provide a rich source of diverse outdoor scenes. VLN-Video automatically generates navigation instructions and action labels from these videos to create additional training data.

## Capabilities

- Augment training data for outdoor VLN
- Enable automatic generation of navigation instructions and action labels

## Relationships

- **used_by**: VLN-Video — The dataset is used to produce synthetic navigation trajectories and instructions.
- **depends_on**: Implicitly depends on video capture hardware and diverse geographic coverage.
- **provides**: Real-world visual diversity that helps Embodied AI agents generalize across environments.

## Sources

- ArXiv paper 2402.03561 (VLN-Video)

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `driving videos` --uses ⚠️--> `VLN-Video`
- `driving videos` --related_to ⚠️--> `Embodied AI`
