---
id: instruction_trajectory_compatibility_model
title: Instruction-trajectory compatibility model
type: algorithm
tags: []
confidence: 0.8
created_at: '2026-04-30T02:23:33'
last_reinforced: '2026-04-30T02:23:33'
supersedes: []
sources:
- papers/2101.10504.pdf
source_type: arxiv_paper
---

## Instruction-trajectory compatibility model

The **instruction-trajectory compatibility model** is a scoring mechanism used in Vision-and-Language Navigation (VLN) evaluation to assess how well a natural language instruction matches a given navigation trajectory. Unlike traditional metrics that compare against a reference instruction, this model evaluates individual instructions in isolation, making it more aligned with human wayfinding performance.

### Capabilities

- **Evaluates individual instructions without reference instructions** – the model does not require a ground-truth instruction to compute compatibility; it directly scores the alignment of an instruction with a candidate trajectory.
- **Shows highest correlation with human wayfinding outcomes** – among existing VLN metrics, this model achieves the strongest agreement with how humans judge the quality of an instruction-trajectory pair, suggesting it captures nuanced aspects of language‐grounded navigation that other metrics miss.

### Dependencies

- `depends_on::Vision-and-Language Navigation (VLN) evaluation` – the model is designed as a component of the VLN evaluation framework and relies on standard VLN input formats (instruction text and sequence of viewpoints/actions).

### Source

- The model is introduced and validated in the paper "Vision-and-Language Navigation: Interpreting visually-grounded navigation instructions in real environments" (arXiv:2101.10504).