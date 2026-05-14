---
id: reverie_remote_embodied_visual_referring_expression_in_real_indoor_environments
title: REVERIE (Remote Embodied Visual Referring Expression in Real Indoor Environments)
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-30T02:13:09'
last_reinforced: '2026-04-30T02:13:09'
supersedes: []
sources:
- papers/2103.12944.pdf
source_type: arxiv_paper
---

# REVERIE

REVERIE (Remote Embodied Visual Referring Expression in Real Indoor Environments) is a benchmark and task definition for **remote embodied visual grounding**. It requires an agent to interpret a concise, high-level natural language instruction and navigate a real indoor environment to localize a remote target object. Unlike typical referring expression tasks where the object is in the agent’s immediate field of view, REVERIE demands that the agent first move through the environment to find the object specified by the instruction.

## Parameters

| Parameter | Description |
|-----------|-------------|
| **Task type** | Remote embodied visual grounding |
| **Input** | High-level natural language instruction (e.g., “Go to the kitchen and tell me the color of the mug on the counter”) |
| **Goal** | Localize the remote target object in a real indoor environment |

## Capabilities

- The agent must navigate through the environment, understand spatial language, and identify objects specified by concise instructions. This requires integration of visual perception, language understanding, and path planning.

## Relationships

- **Depends on**: Embodied Visual Grounding — REVERIE extends the grounding problem to remote, unexplored spaces, where the object is not initially visible and must be actively searched for.

## See also

- Embodied AI
- Visual Language Models ⚠️
- Sim-to-Real Transfer

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `REVERIE (Remote Embodied Visual Referring Expression in Real Indoor Environments)` --related_to ⚠️--> `Embodied AI`
