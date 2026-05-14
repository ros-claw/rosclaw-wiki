---
id: uni_navid
title: Uni-NaVid
type: algorithm
tags: []
confidence: 0.85
created_at: '2026-04-29T20:56:01'
last_reinforced: '2026-04-30'
supersedes: []
sources:
- papers/2412.06224.pdf
source_type: arxiv_paper
---

# Uni-NaVid

## Overview
Uni‑NaVid is the first **video‑based Vision‑Language‑Action (VLA) model** designed to unify diverse embodied navigation tasks. It harmonizes input/output data configurations across commonly used navigation sub‑tasks, enabling a single model to handle instruction following, object searching, question answering, and people tracking across a wide range of real‑world scenarios. By combining video input ⚠️ ⚠️ with action output ⚠️ ⚠️, it learns a unified vision-language-action modeling ⚠️ ⚠️ paradigm for navigation.

## Capabilities
- Handles multiple navigation tasks: **instruction following**, **object searching**, **question answering**, and **people tracking**.
- Unifies these four sub‑tasks within a single architecture, achieving state‑of‑the‑art performance on established navigation benchmarks.
- Executes mixed, long‑horizon tasks in **unseen real‑world environments** without task‑specific fine‑tuning.
- Demonstrates strong generalizability in real‑world experiments.

## Training Data
Uni‑NaVid was trained on a dataset of **3.6 million navigation data samples** collected from the four essential sub‑tasks. This large‑scale data collection fosters **synergy** across tasks, allowing the model to generalize to novel combinations of behaviors. Training relied on multi-task training ⚠️ ⚠️ and careful data curation to harmonize input and output specifications across different navigation tasks.

## Performance
Extensive benchmarks and real‑world experiments confirm that Uni‑NaVid achieves state‑of‑the‑art performance on comprehensive navigation benchmarks and exhibits strong generalizability in unseen environments.

## Parameters
- **Type**: Video‑based Vision‑Language‑Action (VLA) model
- **Input modality**: video
- **Output modality**: action
- **Training data size**: 3.6 million samples
- **Sub‑tasks**: 4 (instruction following, object searching, question answering, people tracking)

## Relationships
- **uses** video input ⚠️ ⚠️, action output ⚠️ ⚠️, vision-language-action modeling ⚠️ ⚠️
- **depends_on** large-scale navigation data collection ⚠️, multi-task training ⚠️ ⚠️, training data ⚠️ from four navigation sub‑tasks
- **implements** VLA model ⚠️ paradigm for embodied navigation
- **part_of** Embodied Navigation task family

## Further Reading
- Related algorithms: RT‑2 ⚠️, Octo ⚠️, PaLM‑E ⚠️
- Related concepts: Sim‑to‑Real Transfer ⚠️, Long‑Horizon Task Planning ⚠️, Multi‑Task Learning ⚠️