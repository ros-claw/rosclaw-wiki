---
id: navforesee
title: NavForesee
type: algorithm
tags: []
confidence: 0.85
created_at: '2026-04-29T20:48:19'
last_reinforced: '2026-04-30'
supersedes: []
sources:
- papers/2512.01550.pdf
source_type: arxiv_paper
---

# NavForesee

**NavForesee** is a novel Vision-Language Model (VLM) that unifies high-level language planning with predictive world model imagination for embodied navigation. It takes a full natural language instruction and historical observations, decomposes the navigation task into sub‑goals, tracks progress, and simultaneously predicts short‑term environmental dynamics and long‑term navigation milestones. The architecture creates an internal feedback loop where planning guides prediction, and prediction informs action selection.

## Parameters

| Parameter | Value |
|-----------|-------|
| Model type | Vision-Language Model (VLM) |
| Input modalities | vision, language |
| Inputs | full instruction, historical observations |
| Outputs | sub‑goals, short‑term predictions, long‑term predictions |
| Framework | Unified high‑level language planning and predictive world model |
| Training data | Natural language instructions and historical observations (R2R‑CE, RxR‑CE) |
| Evaluation benchmarks | R2R-CE, RxR-CE |

## Capabilities

- Long‑horizon navigation guided by complex natural language instructions
- Simultaneous high‑level planning and predictive world model imagination
- Task decomposition into sub‑goals
- Progress tracking
- Short‑term environmental dynamics prediction
- Long‑term navigation milestone prediction
- Internal feedback loop of perception–planning/prediction–action

## Methodology

The model takes the full instruction and history, decomposes the task into sub‑goals, tracks progress, and predicts both immediate environmental dynamics and long‑term navigation milestones. The imagined future then informs action selection, forming a closed loop.

## Relationships

- **uses**: Vision-Language Model (VLM), World Model, R2R-CE, RxR-CE
- **depends_on**: natural language instructions, historical observations

## Summary

NavForesee unifies high‑level language planning and generative world model prediction within a single VLM, enabling embodied agents to reason about unseen environments over long horizons. It achieves competitive performance on the R2R-CE and RxR-CE benchmarks.