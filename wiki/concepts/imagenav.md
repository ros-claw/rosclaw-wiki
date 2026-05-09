---
id: imagenav
title: ImageNav
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-29T23:57:42'
last_reinforced: '2026-04-29T23:57:42'
supersedes: []
sources:
- papers/2509.16445.pdf
source_type: arxiv_paper
---

# ImageNav

**ImageNav** (Image Goal Navigation) is a navigation task where an agent must move to a location that matches a given image goal. It is part of the training mixture used in [[FiLM-Nav]] fine-tuning, providing diverse visual experiences to improve generalization.

## Overview

In Image Navigation (ImageNav), the agent receives a goal image captured from the target location and must navigate through an environment to reach that location. The task emphasizes visual recognition and spatial reasoning, as the goal is defined solely by an image rather than coordinates or semantic labels.

## Capabilities

- **Training task for navigation**: ImageNav serves as a core training scenario for developing visual navigation policies.
- **Navigating to a specific image-based goal**: The agent learns to associate visual features with goal positions and plan paths accordingly.

## Evaluation Metrics

Standard metrics for ImageNav include:

- **Success Rate**: The fraction of episodes where the agent reaches the goal within a distance threshold.
- **SPL** (Success weighted by Path Length): Measures both success and efficiency of the navigation path.

## Relationship to FiLM-Nav

ImageNav is part of the [[FiLM-Nav]] training mixture. During fine-tuning, including ImageNav alongside other tasks (e.g., [[ObjectNav]]) helps the model learn robust visual grounding and navigation under varied goal representations. This diversity improves the agent's ability to handle different types of goal specifications in real-world deployment.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Pending review:**
- `ImageNav` --[[related_to]] ⚠️--> `FiLM-Nav` _(wikilink)_
