---
id: structured_transformer_planner_stp
title: Structured Transformer Planner (STP)
type: algorithm
tags: []
confidence: 0.85
created_at: '2026-04-29T21:15:22'
last_reinforced: '2026-04-30'
supersedes: []
sources:
- papers/2207.11201.pdf
source_type: arxiv_paper
---

# Structured Transformer Planner (STP)

The **Structured Transformer Planner (STP)** is a neural algorithm that extends the Transformer architecture to incorporate **explored room layout** directly into the attention mechanism. Its purpose is to enable **structured and global planning** in embodied navigation tasks, moving beyond purely geometric or sequential planners. STP encodes the explored room layout as structured attention, allowing the model to reason about room connectivity and layout constraints for layout-aware, long-horizon planning under partial observability.

## Architecture

STP modifies the standard transformer attention to **respect the spatial structure** of the observed environment. Rather than treating each observation element as independent, the model reasons about room connectivity and layout constraints. This allows the planner to maintain a global understanding of the environment while planning at the structure level (rooms, corridors, doorways) rather than raw waypoints.

The key innovation is the integration of **explored room layout information** into the attention weights, forcing the model to attend only to spatial regions that are topologically and geometrically plausible given current knowledge.

## Capabilities

- **Incorporation of explored room layout into neural attention**: The planner does not assume a fully observable map; it uses only the explored regions and their layout to constrain attention, making it suitable for partial observability.
- **Structured and global planning**: STP reasons about the high-level structure (rooms, zones) rather than pixel-level paths, enabling longer-horizon planning and better generalization to unseen environments.
- **Global planning with structured attention over room layouts**: This capability is central to STP’s design, allowing it to maintain a coherent spatial understanding even as the agent explores novel environments.

## Relationships

- **TD-STP ⚠️ ⚠️ ⚠️** ─ STP is a core component of the **Target-Driven Structured Transformer Planner (TD-STP)** framework, where it provides the structured planning backbone. In the full Teacher-Student framework, STP serves as the teacher policy for imitation learning and distillation. STP is **used by** TD-STP ⚠️ ⚠️ ⚠️ as the central planner to achieve target-driven navigation.
- **Transformer ⚠️ ⚠️** ─ The base computational primitive of STP; the model uses transformer attention mechanisms and extends them with spatial constraints.

## Dependencies

- Relies on a room layout estimator or semantic map (not part of the algorithm itself).
- Uses Transformer ⚠️ ⚠️ attention mechanisms as the base computational primitive.

## Source

- Based on the paper: *Structured Transformer Planner for Embodied Navigation* (arXiv:2207.11201).

## See also

- Embodied Navigation, Neural Attention ⚠️, Room Layout Estimation ⚠️
- Partially Observable Markov Decision Process (POMDP) ⚠️ formalisms for navigation
- TD-STP ⚠️ ⚠️ ⚠️ for the target-driven variant