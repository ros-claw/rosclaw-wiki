---
id: pathagent
title: PathAgent
type: algorithm
tags: []
confidence: 0.85
created_at: '2026-04-29T20:59:38'
last_reinforced: '2026-04-30'
supersedes: []
sources:
- papers/2407.05890.pdf
source_type: arxiv_paper
---

# PathAgent

**PathAgent** is an algorithmic component of the [[AO-Planner]] framework. It functions as a **high-level planner**, integrating path planning with visual context. The agent marks planned paths directly into image input and reasons the most probable trajectory by comprehending the full environmental information.

## Capabilities

- Marks planned paths into image input (e.g., overlaying trajectory candidates on camera or sensor imagery).
- Reasons the most probable path by evaluating and interpreting all available environmental information (obstacles, terrain, semantic cues, etc.).
- Provides **reasoning over planned paths**, selecting the most suitable path based on environmental context.

## Implementation Notes

- PathAgent likely consumes multi-modal inputs (vision, lidar, or metric maps) and outputs a ranked or scored set of trajectories.
- It combines symbolic reasoning (path feasibility) with perceptual grounding (image-space annotation), enabling explainable planning outputs.
- Its operation depends on **Visual Affordances Prompting**, leveraging visual affordances to ground its spatial reasoning.

## Dependencies

- **Depends on** → [[Visual Affordances Prompting]] ⚠️ ⚠️: PathAgent relies on visual affordance cues to evaluate trajectory candidates in the image space.

## Relationships

- **Part of** → [[AO-Planner]]: PathAgent functions as the planning perception layer within the AO-Planner architecture.
- **Depends on** → [[Visual Affordances Prompting]] ⚠️ ⚠️: For environmental understanding and path feasibility assessment.

## Source

- Derived from: *arxiv: 2407.05890* – details of PathAgent’s role in the AO-Planner pipeline.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `PathAgent` --[[extends]] ⚠️--> `AO-Planner`
- `PathAgent` --[[depends_on]] ⚠️--> `Visual Affordances Prompting`