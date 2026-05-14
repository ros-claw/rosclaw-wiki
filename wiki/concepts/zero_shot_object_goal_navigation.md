---
id: zero_shot_object_goal_navigation
title: Zero-Shot Object-Goal Navigation
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-30T00:01:29'
last_reinforced: '2026-04-30T00:01:29'
supersedes: []
sources:
- papers/2505.23019.pdf
source_type: arxiv_paper
---

## Zero-Shot Object-Goal Navigation

**Zero-Shot Object-Goal Navigation** is a paradigm in embodied AI that enables a robot to locate and navigate to a specific object instance within completely unseen environments without requiring any task-specific retraining or fine-tuning. This capability is achieved through the combination of large-scale pretrained vision-language models, semantic scene understanding, and generalizable navigation policies.

### Key Characteristics

- **No Retraining Required**: The robot can be deployed directly in novel environments (e.g., unknown homes or offices) and still succeed at object search tasks.
- **Semantic Generalization**: The system leverages high-level object descriptions (e.g., "find a chair") rather than relying on a fixed set of known objects.
- **Integration with Modular Pipelines**: Typically implemented as a component within a larger navigation system that includes mapping, exploration, and goal identification modules.

### Capabilities

- Enable robots to find objects in novel environments without retraining.

### Evaluation Benchmarks

Zero-Shot Object-Goal Navigation is commonly evaluated on:

- **HM3D** (Habitat-Matterport 3D): A large-scale photorealistic 3D dataset of indoor environments.
- **MP3D** (Matterport3D): Another standard benchmark for embodied navigation tasks.

These benchmarks test the ability to generalize across floorplans and object categories without prior exposure to the test environments.

### Relationships

- **Used in**: The **ASCENT** system, which integrates zero-shot object-goal navigation as a core skill for multi-floor, open-vocabulary search.
- **Related to**: 
  - **Object-Goal Navigation** – the broader task of navigating to a specific object target.
  - **Multi-floor Navigation** – extensions of the zero-shot principle to environments with multiple levels, where the robot must also handle vertical transitions.

### See Also

- ASCENT
- Object-Goal Navigation
- Multi-floor Navigation
- HM3D
- MP3D

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Pending review:**
- `Zero-Shot Object-Goal Navigation` --related_to ⚠️--> `ASCENT` _(wikilink)_
