---
id: end_to_end_trajectory_learning
title: End-to-end trajectory learning
type: algorithm
tags: []
confidence: 0.85
created_at: '2026-04-29T20:58:11'
last_reinforced: '2026-04-30'
supersedes: []
sources:
- papers/2507.04047.pdf
source_type: arxiv_paper
---

# End-to-End Trajectory Learning

**End-to-end trajectory learning** is an algorithmic paradigm where a policy directly maps raw sensor observations (e.g., vision, language commands) to continuous or discrete trajectory commands, bypassing explicit intermediate representations such as waypoints, costmaps, or motion primitives. This approach is particularly relevant in embodied AI, where an agent must act in real-world environments based on high-level instructions.

## Capabilities

- Learns navigation policies directly from RGB-D input, processing egocentric video frames alongside natural language commands.
- Combines [[Vision-Language-Exploration pre-training]] over **more than a million diverse trajectories** drawn from simulated and real-world RGB-D sequences, enabling the model to generalize across scenes, objects, and instruction formats without hand‑crafted features or heuristic planners.

## Relationships

- **Part of**: [[MTU3D (Move to Understand 3D)]] – this algorithm serves as the core trajectory generation component within the MTU3D system.
- **Depends on**: [[Vision-Language-Exploration pre-training]] – the pre‑trained embeddings provide the visual‑language grounding necessary for trajectory decoding.

## Key Characteristics

- Learns a single neural network that ingests egocentric video and a natural language command, then outputs velocity or joint‑space commands.
- The pre‑training phase leverages large‑scale, heterogeneous trajectory data (over a million samples from both simulation and real‑robot rollouts with RGB-D observations).
- Fine‑tuning can be performed on task‑specific datasets to adapt the motion style or constraints.

## Connections to Other Knowledge

- Closely related to [[behavior cloning]] ⚠️ and [[imitation learning]], but end‑to‑end trajectory learning typically avoids intermediate state‑action decompositions.
- Often used in conjunction with [[large vision-language models]] ⚠️ to interpret complex, long‑horizon instructions.
- Contrasts with modular approaches that separate perception, planning, and control (e.g., [[classical robotics pipeline]] ⚠️).

## References

- Source paper: *arxiv 2507.04047* (End‑to‑end trajectory learning with Vision‑Language‑Exploration pre‑training).