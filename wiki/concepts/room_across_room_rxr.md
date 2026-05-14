---
id: room_across_room_rxr
title: Room-Across-Room (RxR)
type: concept
tags: []
confidence: 0.9
created_at: '2026-04-29T21:22:31'
last_reinforced: '2026-04-30'
supersedes: []
sources:
- papers/2010.07954.pdf
- papers/2110.14143.pdf
source_type: arxiv_paper
---

# Room-Across-Room (RxR)

## Overview

**Room-Across-Room (RxR)** is a large-scale, multilingual benchmark for Vision-and-Language Navigation (VLN ⚠️) introduced by **Alexander Ku et al.** in the paper *Room-Across-Room: Multilingual Vision-and-Language Navigation with Dense Spatiotemporal Grounding* (arxiv:2010.07954). It extends the earlier Room-to-Room (R2R) dataset with instructions in English, Hindi, and Telugu, a significantly larger number of paths, and word‑level temporal alignment to agent poses. RxR serves as both a dataset and an evaluation benchmark, focusing on indoor environments. It supersedes R2R by providing multilingual coverage, reduced path biases, and dense spatiotemporal grounding, making it a more challenging VLN benchmark that demands richer visual‑language understanding and cross‑lingual capability.

## Key Parameters

| Parameter | Details |
|-----------|---------|
| **Type** | Navigation benchmark / dataset |
| **Domain** | Indoor environments – simulated photo‑realistic scenes |
| **Languages** | English, Hindi, Telugu |
| **Scale** | Larger than any previous VLN dataset (more paths and multilingual instructions) |
| **Time‑aligned words** | Yes – each word in an instruction is temporally aligned to the corresponding virtual pose trace |
| **Spatiotemporal grounding** | Dense – instructions are grounded in both space and time, with synchronized pose traces from instruction creators and validators |
| **Environment** | Matterport3D ⚠️ ⚠️ ⚠️ (simulated photo‑realistic environments) |
| **Key Metric** | Success Rate (SR) |

## Features

- **Multilingual instructions** in English, Hindi, and Telugu, enabling cross‑lingual VLN research.
- **Larger scale** – more paths and instruction–path pairs than any prior VLN dataset.
- **Reduced path biases** – careful instruction collection reduces shortcut learning that plagued R2R.
- **Dense spatiotemporal grounding** – word‑level alignment with virtual pose traces from instruction creators and validators, providing finer‑grained anchor points between language and visual observations.
- **More references to visible entities** (objects, landmarks) compared to prior datasets, encouraging richer visual‑language understanding.

## Capabilities

- Supports vision‑and‑language navigation research.
- Enables multilingual VLN – agents must understand and follow instructions in three languages.
- Provides dense spatiotemporal grounding for language instructions, allowing models to learn precise alignments between words and visual‑temporal cues.
- Addresses biases in path selection, reducing shortcut learning and promoting robust generalisation.

## Relationships

- **Depends on:** the Room-to-Room (R2R) dataset (baseline design and environment) and the Matterport3D ⚠️ ⚠️ ⚠️ simulator (underlying visual space and pose traces).
- **Supersedes:** Room-to-Room (R2R) in terms of scale, multilingual coverage, grounding density, and path bias reduction.
- **Uses:** Virtual pose traces ⚠️ of instruction creators and validators, Multilingual language instructions ⚠️, and Matterport3D ⚠️ ⚠️ ⚠️ environments. 
- **Used by:** Scene‑ and Object‑Aware Transformer (SOAT) ⚠️ – achieves a 3.7% absolute improvement in Success Rate on this benchmark.

## Significance

RxR expands the frontier for research on embodied language agents in simulated environments. It has become a standard benchmark for evaluating navigation agents that must follow instructions in multiple languages and ground language to dynamic visual streams. Its dense annotations support research in instruction understanding, cross‑lingual transfer, and embodied AI. The introduction of SR as a primary metric facilitates direct comparisons across models such as SOAT and other VLN approaches.