---
id: marky
title: Marky
type: algorithm
tags: []
confidence: 0.8
created_at: '2026-04-30T01:55:19'
last_reinforced: '2026-04-30T01:55:19'
supersedes: []
sources:
- papers/2210.03112.pdf
source_type: arxiv_paper
---

# Marky

**Marky** is a high-quality, multilingual navigation instruction generator designed for creating visually grounded instructions paired with trajectories. It produces synthetic instruction–trajectory pairs at scale, with a released dataset of **4.2 million** pairs across multiple languages. Marky is primarily used for data augmentation and training in Embodied AI navigation tasks, enabling agents to follow natural-language commands in unseen environments.

## Capabilities

- **Generate visually-grounded navigation instructions** for arbitrary trajectories in simulated or real environments. Each instruction is tied to the visual features along the path, ensuring spatial and semantic alignment.
- **Multilingual output** – supports multiple languages (e.g., English, Chinese, etc.) by leveraging pretrained multilingual language models.
- **High quality** – instructions are grammatically correct, spatially precise, and avoid hallucinations common in simpler sequence-to-sequence models.

## Parameters

| Parameter | Value |
|-----------|-------|
| multilingual | true |
| quality | high |

## Relationships

- **`used_for`** → synthetic instruction generation ⚠️ – Marky is the core engine for creating large-scale training datasets for instruction-following agents.
- **`depends_on`** → vision-language models ⚠️ – relies on cross-modal alignment to ground directions in visual input.
- **`implements`** → instruction-to-trajectory mapping ⚠️ – converts a sequence of waypoints into natural language with spatial verbs and landmarks.

## Usage

Marky is commonly employed in Sim-to-Real ⚠️ pipelines to augment real-world data with synthetic examples, improving generalization. Its multilingual capability makes it valuable for research in Cross-Lingual Embodied Agents ⚠️.

## Dataset

The Marky-generated dataset includes 4.2M instruction–trajectory pairs, covering diverse environments from indoor scenes to outdoor street views, and is available for research under standard academic licenses. The dataset language coverage can be expanded by swapping the underlying multilingual text decoder.

## References

- ArXiv paper: 2210.03112 – *Marky: A Multilingual High-Quality Instruction Generator for Visual Navigation*
- Related work: VLN-BERT, HOP ⚠️, Room-to-Room (R2R) Dataset

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Marky` --based_on ⚠️--> `Embodied AI`
- `Marky` --implements ⚠️--> `Room-to-Room (R2R) Dataset`
