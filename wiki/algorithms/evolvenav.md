---
id: evolvenav
title: EvolveNav
type: algorithm
tags: []
confidence: 0.85
created_at: '2026-04-29T20:59:00'
last_reinforced: '2026-04-30'
supersedes: []
sources:
- papers/2506.01551.pdf
source_type: arxiv_paper
---

# EvolveNav

## Overview

**EvolveNav** is a novel self‑improving embodied reasoning paradigm for [[LLM]] ⚠️-based [[Vision-Language Navigation (VLN)]]. It improves decision accuracy and interpretability by combining formalized chain‑of‑thought supervision with self‑reflective learning, achieving consistent state‑of‑the‑art results across multiple VLN benchmarks. The algorithm addresses the limitations of straightforward input‑output mapping by introducing a two‑stage training process that first activates navigational reasoning and then refines it through iterative self‑reflection.

---

## Capabilities

- **Improved navigation decision accuracy and interpretability** for LLM‑based [[VLN]] ⚠️.
- **Self‑improving reasoning** through iterative self‑reflection on its own outputs.
- **Adaptable and generalizable** across diverse VLN tasks and environments.
- **Consistent superiority** over previous LLM‑based VLN approaches on the following benchmarks:
  - [[R2R (Room-to-Room)]]
  - [[REVERIE]]
  - [[CVDN]]
  - [[SOON]]

---

## Method

EvolveNav employs a **two‑stage training process** under the paradigm of *self‑improving embodied reasoning*:

1. **Formalized CoT Supervised Fine‑Tuning** – activates navigational reasoning and increases reasoning speed by training on structured [[Chain-of-Thought]] ⚠️ (CoT) labels.
2. **Self‑Reflective Post‑Training** – iteratively trains the model using its own reasoning outputs as self‑enriched CoT labels, enhancing supervision diversity. This stage includes a *self‑reflective auxiliary task* designed to contrast correct and wrong reasoning patterns, further refining the model’s decision‑making.

Reinforcement: The two‑stage pipeline, the names of each stage, and the “self‑improving embodied reasoning” paradigm are all confirmed by the source.

---

## Relationships

- `uses` → [[Large Language Models (LLMs)]]
- `uses` → [[Chain-of-Thought (CoT)]]
- `depends_on` → [[Vision-Language Navigation (VLN)]]
- `tested_on` → [[R2R (Room-to-Room)]], [[REVERIE]], [[CVDN]], [[SOON]]