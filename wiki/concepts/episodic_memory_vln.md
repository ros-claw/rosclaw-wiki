---
id: episodic_memory_vln
title: Episodic Memory (VLN)
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-30T01:28:19'
last_reinforced: '2026-04-30T01:28:19'
supersedes: []
sources:
- papers/2403.14158.pdf
source_type: arxiv_paper
---

**Episodic Memory (VLN)** is a form of memory used in [[Vision-Language Navigation]] that stores previously visited states and observations from a robot's or agent's past experiences. It enables the agent to remember what it has seen and where it has been, which is essential for making informed decisions during navigation—especially in partially observed or dynamic environments.

## Capabilities
- Stores previously visited states and observations.
- Used to predict the next step in navigation, leveraging historical context to improve path planning and decision-making.

## Relationships
- **[[Vision-Language Navigation]]**: Episodic Memory is a core component of VLN systems, enabling agents to recall prior perceptions and actions.
- **[[Volumetric Environment Representation]]**: Episodic memory is built from online-collected VERs, forming a structured history of the environment.
- **[[Volume State Estimation]]**: Episodic Memory depends on volume state estimation to index and retrieve spatial states effectively.

## Role
Episodic memory built from online collected VERs allows the agent to remember past observations and make informed navigation decisions. By maintaining a history of visited states, the agent can avoid revisiting explored areas, infer unobserved regions, and apply reasoning over time—similar to how biological episodic memory supports spatial cognition.