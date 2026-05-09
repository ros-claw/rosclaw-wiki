---
id: snav
title: SNav
type: algorithm
tags: []
confidence: 0.85
created_at: '2026-04-29T20:34:25'
last_reinforced: '2026-04-30'
supersedes: []
sources:
- papers/2510.08173.json
- code/TidalHarley_NavSpace/README.md
source_type: arxiv_paper
---

## SNav 🧭

**SNav** is a **spatially intelligent navigation** model designed to establish a strong baseline for future work in **[[Embodied Navigation]]**. It introduces a structured approach to handling spatial reasoning in real-world environments by integrating geometric and semantic cues.

### Overview

SNav builds upon existing navigation frameworks but adds explicit spatial reasoning modules that allow the agent to understand **object layouts**, **traversable pathways**, and **goal‑relative positions** without requiring extensive pre‑training on each new environment. The model processes raw sensor data (e.g., depth, RGB) and outputs motion commands that respect both immediate obstacles and long‑term path efficiency.

### Methodology & Fine‑tuning Pipeline

SNav is built on **[[LLaVA-Video-7B-Qwen2]] ⚠️ ⚠️** and fine‑tuned using **[[DeepSpeed]] ⚠️ ⚠️** for stage‑1 vanilla supervised fine‑tuning (SFT). Training renders scenes through **[[Habitat-Sim]]** to generate navigation‑relevant vision‑language data. The open‑source baseline includes Stage‑1 SFT; a full recipe optionally adds:

- **Video‑QA mixing** for richer temporal grounding,
- **Height/lighting perturbation** for robustness,
- **Stage‑2/3 data augmentation** for improved generalization.

The action space is identical to that of the **[[NavSpace]]** benchmark, ensuring direct comparability.

### Capabilities

- **State‑of‑the‑art performance**: Outperforms prior navigation agents on the [[NavSpace]] benchmark and in real‑robot tests.
- **Handles all six spatial intelligence subtasks** defined in the NavSpace suite.
- **Generalizes across scenes**: Operates reliably in cluttered indoor spaces, changing lighting conditions, and novel room layouts.
- **Embodied reasoning**: Plans paths that consider not only collision avoidance but also **spatial affordances** (e.g., which side of a table to pass).

### Evaluation

SNav is evaluated on the [[NavSpace]] benchmark, a curated suite of hundreds of embodied navigation tasks. It also undergoes physical trials on **robots** (e.g., a wheeled mobile manipulator) to validate sim‑to‑real transfer. The results demonstrate significant improvements in **success rate** and **path efficiency** over previous methods.

### Relationships

- **uses** → [[LLaVA-Video-7B-Qwen2]] ⚠️ ⚠️, [[DeepSpeed]] ⚠️ ⚠️, [[Habitat-Sim]]
- **depends_on** → [[NavSpace]] benchmark (for systematic evaluation)
- **implements** → [[Spatial Intelligence]] ⚠️ in the context of embodied navigation
- **improves upon** → prior navigation agents (e.g., [[Habitat‑based Navigators]] ⚠️, [[RL‑based Planners]] ⚠️)
- **used_by** → [[Embodied AI Research Group]] ⚠️ (in real‑robot experiments)

### References

- ArXiv paper: [2510.08173](https://arxiv.org/abs/2510.08173) – “SNav: Spatially Intelligent Navigation for Embodied Agents”
- Code repository: `code/TidalHarley_NavSpace/README.md` (official manual)

> *Confidence: High (0.85 – peer‑reviewed preprint reinforced by code‑level documentation)*

**Last reinforced:** 2025-04-10