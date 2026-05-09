---
id: mobilevla_cot_dataset
title: MobileVLA-CoT Dataset
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-30T00:11:12'
last_reinforced: '2026-04-30T00:11:12'
supersedes: []
sources:
- papers/2511.17889.pdf
source_type: arxiv_paper
---

## MobileVLA-CoT Dataset

MobileVLA-CoT is a **large-scale** dataset containing **multi-granularity chain-of-thought reasoning** paired with embodied robot trajectories. Its primary purpose is **supervised reasoning alignment** — teaching vision-language-action (VLA) models to align high-level reasoning steps with low-level continuous control.

### Description

The dataset provides step-by-step chain-of-thought (CoT) annotations for real-world trajectory data, enabling models to learn the reasoning behind each action. MobileVLA-CoT is used in the first training stage of [[MobileVLA-R1]] to teach the model to bridge the gap between semantic planning and motor execution. By exposing the model to diverse reasoning patterns, the dataset helps imbue VLA models with interpretable, generalizable decision-making capabilities. This approach falls under the umbrella of **Chain-of-Thought Alignment**.

### Parameters

- **Scale**: Large-scale
- **Content**: Multi-granularity chain-of-thought annotations for embodied trajectories
- **Purpose**: Supervised reasoning alignment for VLA models

### Capabilities

- Provides **reasoning supervision** for aligning high-level language reasoning with low-level control in VLA architectures.

### Relationships

- **Used by** [[MobileVLA-R1]]
- **Depends on** (implicitly) raw embodied trajectory data and CoT annotation pipelines
- **Implements** the concept of [[Chain-of-Thought Alignment]] in the embodied domain
- **Part of** the training pipeline for supervised VLA alignment

### Source

Derived from the methodology presented in arXiv paper [2511.17889](https://arxiv.org/abs/2511.17889).

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Pending review:**
- `MobileVLA-CoT Dataset` --[[related_to]] ⚠️--> `MobileVLA-R1` _(wikilink)_
