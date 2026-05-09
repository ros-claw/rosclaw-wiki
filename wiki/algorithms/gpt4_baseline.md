---
id: gpt4_baseline
title: gpt4_baseline
type: algorithm
tags: []
confidence: 0.8
created_at: '2026-04-29T21:08:45'
last_reinforced: '2026-04-29T21:08:45'
supersedes: []
sources:
- papers/2403.07376.pdf
source_type: arxiv_paper
---

# GPT-4 Baseline (Algorithm)

**GPT-4 Baseline** is an offline LLM-based approach used for [[Vision-and-Language Navigation]] (VLN). It leverages the general reasoning capabilities of [[GPT-4]] to process visual and linguistic instructions, but its direct application to VLN is hindered by a substantial domain gap between the training corpus of the LLM and the specific requirements of embodied navigation tasks.

## Usage

The GPT-4 Baseline serves as a **comparative benchmark** for evaluating newer, more specialized VLN algorithms. It is applied in an offline setting, meaning it does not interact with the environment in real time but rather processes pre-recorded observations to generate navigation decisions.

- Uses: [[GPT-4]] for reasoning, [[VLN]] ⚠️ ⚠️ task formulation
- Depends on: Large-scale language model pretraining, offline dataset (e.g., [[R2R Dataset]])

## Limitations

- **Domain gap**: The LLM’s training data primarily consists of general internet text, lacking the embodied spatial and temporal context required for accurate navigation.
- **Limited accuracy**: Due to the domain mismatch, the baseline produces suboptimal route predictions compared to dedicated VLN models.

## Capabilities

- Provides navigational reasoning by combining visual features with language instructions.
- Serves as a zero-shot baseline that requires no task-specific fine-tuning.
- However, performance is constrained by the absence of embodied experience in the LLM’s knowledge.

## Relationships

| Entity | Relationship | Description |
|--------|-------------|-------------|
| [[NavCoT]] | Outperformed by | NavCoT achieves significantly better results on VLN benchmarks |
| [[R2R Dataset]] | Evaluated on | The baseline is tested on the Room-to-Room navigation task |
| [[VLN]] ⚠️ ⚠️ | Implements | This algorithm addresses the VLN problem using an LLM reasoning backbone |

## Baseline Comparison

A recent evaluation of the GPT-4 Baseline on the [[R2R Dataset]] showed that while it can produce coherent navigation plans, its performance lags behind specialized methods. Specifically, [[NavCoT]] — a chain-of-thought prompting approach tailored for VLN — outperforms the GPT-4 Baseline by approximately **7% relative improvement** in success rate. This gap underscores the importance of bridging the domain gap through techniques like task-specific prompting or fine-tuning on navigation data.

> **Source**: arxiv paper 2403.07376 — *NavCoT: Boosting LLM-Based Vision-and-Language Navigation via Chain-of-Thought Reasoning*

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `gpt4_baseline` --[[based_on]] ⚠️--> `Vision-and-Language Navigation`
- `gpt4_baseline` --[[extends]] ⚠️--> `NavCoT`
