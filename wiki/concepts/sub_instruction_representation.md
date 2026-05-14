---
id: sub_instruction_representation
title: Sub-Instruction Representation
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-30T02:03:52'
last_reinforced: '2026-04-30T02:03:52'
supersedes: []
sources:
- papers/2302.09230.pdf
source_type: arxiv_paper
---

## Sub-Instruction Representation

A **Sub-Instruction Representation** is an easy-to-follow decomposition of a high-level navigation instruction into smaller, actionable steps. The representation is dynamically tailored to the agent’s visual capabilities and its current environment, ensuring that each sub‑instruction references only landmarks the agent can recognize or distinguish.

### Description

Rather than presenting an agent with a single lengthy instruction such as *“Walk past the blue sofa, turn left at the white door, then enter the second room on your right”*, a sub‑instruction representation breaks this into discrete steps (e.g., *“Step 1: Locate the blue sofa.”*, *“Step 2: Move toward it.”*, *“Step 3: Turn left at the white door.”*, …). Each step is expressed in terms of Recognizable Landmarks that are visually salient and distinct from their surroundings. The granularity of the sub‑instructions adapts to the agent’s perceptual abilities: if the agent has difficulty distinguishing two similar doors, the representation may incorporate additional contextual cues or merge those steps.

This representation is essential for systems that must map natural language instructions to a sequence of grounded actions in a real or simulated environment. It reduces the cognitive load on the agent’s language understanding module and aligns the instruction with the agent’s moment‑to‑moment observations.

### Relationships

- **Used by**: VLN-Trans – the sub‑instruction representation is a core input format for the VLN-Trans transformer architecture, enabling it to predict waypoint‑level actions.
- **Depends on**:  
  - Recognizable Landmarks – each sub‑instruction must refer to landmarks that the agent’s visual system can reliably detect.  
  - Distinctive Landmarks – to avoid ambiguity, sub‑instructions should reference landmarks that are not easily confused with other objects in the scene.

### Related Concepts

- Visual Language Navigation ⚠️ (VLN) – the broader task that motivates the need for sub‑instruction representations.
- Instruction Decomposition ⚠️ – the process of generating sub‑instructions from a full instruction.
- Grounded Language Understanding ⚠️ – ensuring that each sub‑instruction has a clear perceptual correlate in the environment.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Pending review:**
- `Sub-Instruction Representation` --related_to ⚠️--> `VLN-Trans` _(wikilink)_
