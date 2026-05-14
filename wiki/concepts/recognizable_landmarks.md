---
id: recognizable_landmarks
title: Recognizable Landmarks
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-30T02:03:00'
last_reinforced: '2026-04-30T02:03:00'
supersedes: []
sources:
- papers/2302.09230.pdf
source_type: arxiv_paper
---

## Recognizable Landmarks

**Recognizable Landmarks** are specific environmental features or objects that an autonomous navigation agent can reliably identify using its own perceptual capabilities (e.g., vision, depth sensing). This concept is central to Instruction Understanding in VLN ⚠️ ⚠️ ⚠️ because it defines the subset of landmarks that the agent can actually ground in its observations, as opposed to those an instructor might describe but the agent cannot see.

### Definition

Landmarks that the navigation agent can visually recognize based on its own visual abilities, as opposed to landmarks described by an instructor with different vision capabilities. The recognizability of a landmark depends on the agent's sensor suite, learned representations, and the salience of the landmark in the environment.

### Role in Visual Language Navigation (VLN)

In Vision-Language Navigation, an agent must follow natural language instructions that often refer to landmarks (e.g., “turn left at the red mailbox”). If the instruction mentions a landmark that the agent **cannot** recognize (e.g., a small sign with text), the instruction becomes ambiguous or impossible to follow. Therefore, **Recognizable Landmarks** form the bridge between natural language directives and the agent’s spatial understanding. They are a prerequisite for successful grounding in Instruction Understanding in VLN ⚠️ ⚠️ ⚠️.

### Relationship to Unrecognizable Landmarks

- **part_of**: Recognizable Landmarks are a subset of all landmarks mentioned in instructions; they are the filter through which Instruction Understanding in VLN ⚠️ ⚠️ ⚠️ becomes executable.
- **contradicts**: Unrecognizable Landmarks ⚠️ — landmarks that the agent cannot perceive or identify, often due to differences in sensory capabilities between the human instructor and the robotic agent. A landmark that is unrecognizable contradicts the notion of being recognizable; the two categories are mutually exclusive for a given agent.

### Example

A VLN agent equipped with a camera may recognize a large red double‑decker bus as a landmark, but fail to recognize a small brass plaque with text. The bus is a **recognizable landmark**; the plaque is an **unrecognizable landmark** for this agent. Instruction designers should prefer recognizable landmarks to improve navigation success.

### See Also

- Landmark ⚠️ (generic concept)
- Groundedness ⚠️
- Sim-to-Real Transfer (where recognizability may degrade)