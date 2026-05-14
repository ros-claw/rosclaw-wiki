---
id: image_goal_navigation
title: Image-goal Navigation
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-30T03:53:22'
last_reinforced: '2026-04-30T03:53:22'
supersedes: []
sources:
- papers/2508.00823.pdf
source_type: arxiv_paper
---

# Image-goal Navigation

**Image-goal navigation** (also known as *image-based navigation* or *view-instructed navigation*) is a core problem in Embodied AI where the agent must navigate to a location that matches a **goal image** rather than a coordinate or semantic label. The agent observes its environment, builds/updates a representation, and moves until the current observation sufficiently matches the goal image.

## Description

Image-goal navigation is a fundamental problem in embodied AI where an agent must navigate to a location depicted in a goal image. The challenge lies in localizing the goal within the agent's 3D representation. Unlike classical Visual navigation systems that rely on metric maps or goal coordinates, this paradigm uses a single snapshot (the goal image) as the only specification of the destination. The agent must infer the relative spatial relationship between its current position and the goal location from visual cues alone.

## Parameters

- **Definition:** Visual navigation where the goal is specified by an image.

## Capabilities

- **Goal specification via image** – The user (or task) provides a single photograph or rendered view of the target location.
- **Requires localization of goal in 3D environment** – The agent must recognise where the goal image was taken or what scene it depicts, and then estimate its own pose relative to that location.

## Relationships

- `part_of` → Visual navigation (image-goal navigation is a sub-problem of the broader visual navigation family)
- `part_of` → Embodied AI (it is a typical task for embodied agents operating in real or simulated spaces)
- `depends_on` → Localization ⚠️ (the goal must be localised in the agent's 3D representation)
- `depends_on` → 3D representation ⚠️ (the agent’s internal model must support spatial reasoning about the goal)
- `related_to` → Active Perception (agent may need to move to disambiguate the goal location)
- `related_to` → Sim-to-Real ⚠️ (many training pipelines rely on simulated environments with image-based goals)

## See also

- Visual Navigation (parent concept)
- Embodied AI (wider field)
- Goal-conditioned reinforcement learning ⚠️ (common algorithmic approach for this task)
- Semantic Navigation ⚠️ (alternative goal specification via object labels)

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Image-goal Navigation` --related_to ⚠️--> `Embodied AI`
