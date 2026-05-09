---
id: onemap
title: OneMap
type: algorithm
tags: []
confidence: 0.85
created_at: '2026-04-29T20:48:15'
last_reinforced: '2026-04-29'
supersedes: []
sources:
- papers/2409.11764.pdf
source_type: arxiv_paper
---

# OneMap

**OneMap** is an open‑vocabulary mapping algorithm for zero‑shot multi‑object navigation. It builds a reusable, probabilistic‑semantic feature map that enables a robot to search for arbitrary objects without prior training, and supports efficient multi‑object exploration by leveraging previously gathered map information.

## Parameters

- **Type**: Open‑vocabulary feature mapping
- **Map update**: Probabilistic‑semantic
- **Uncertainty handling**: Semantic uncertainty for informed exploration
- **Runtime**: Real‑time (validated on [[Jetson Orin AGX]])
- **Queries**: Zero‑shot multi‑object navigation

## Capabilities

- Zero‑shot object search (no prior training required)
- Builds a reusable open‑vocabulary feature map
- Mitigates common semantic extraction errors via probabilistic map updates
- Leverages semantic uncertainty for informed multi‑object exploration
- Multi‑object navigation that reuses prior exploration data
- Real‑time operation on embedded hardware
- Outperforms state‑of‑the‑art on single and multi‑object navigation tasks

## Method

OneMap employs a probabilistic‑semantic map update that actively mitigates errors in semantic feature extraction. Uncertainty is used to guide exploration: the robot decides where to look next based on which areas are most uncertain and likely to contain target objects. The map is built using [[Open‑Vocabulary Vision Models]] ⚠️ ⚠️ ⚠️ for semantic feature extraction, and features are fused probabilistically to produce a reusable open‑vocabulary representation.

## Benchmark

The paper introduces a new benchmark for zero‑shot multi‑object navigation that allows repeated queries, enabling the robot to leverage information from previous searches. This setup better reflects real‑world scenarios where a robot must find multiple objects after one exploration pass.

## Evaluation

OneMap was validated on object‑navigation tasks both in simulation and on a real robot. It runs in real‑time on a [[Jetson Orin AGX]] and uses [[Open‑Vocabulary Vision Models]] ⚠️ ⚠️ ⚠️ for semantic feature extraction. The algorithm achieves state‑of‑the‑art results on both single‑object and multi‑object navigation tasks.

## Relationships

- **Uses**: [[Jetson Orin AGX]], [[Open‑Vocabulary Vision Models]] ⚠️ ⚠️ ⚠️
- **Depends on**: [[Semantic Feature Extraction]] ⚠️, [[Probabilistic Map Fusion]] ⚠️

---

*Source: arxiv paper [2409.11764] — "OneMap: Open-Vocabulary Mapping for Zero-Shot Multi-Object Navigation"*