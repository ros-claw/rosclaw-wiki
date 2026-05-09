---
id: mllm
title: MLLM
type: algorithm
tags: []
confidence: 0.8
created_at: '2026-04-30T00:36:10'
last_reinforced: '2026-04-30T00:36:10'
supersedes: []
sources:
- papers/2509.22548.pdf
source_type: arxiv_paper
---

**MLLM (Multimodal Large Language Model)**

A **Multimodal Large Language Model (MLLM)** is a neural architecture that extends traditional large language models (LLMs) to process and reason over multiple modalities — most commonly vision and language. In the context of embodied AI and vision-language navigation (VLN), MLLMs serve as the semantic backbone, enabling agents to understand visual scenes, interpret natural language instructions, and generate grounded action plans.

**Role**

MLLMs provide powerful semantic understanding of both visual and textual data, allowing navigation agents to map high‑level instructions (e.g., “go to the red sofa”) to relevant objects and spatial relationships in the environment.

**Capabilities**

- Semantic understanding of visual and textual data  
- Cross‑modal alignment and reasoning  
- Instruction‑driven action prediction (when fine‑tuned for downstream tasks)

**Relationships**

- **Used by** [[JanusVLN]] – JanusVLN builds on top of an MLLM backbone to achieve instruction following in 3D scenes.  
- **Used by** many recent [[VLN methods]] ⚠️ – MLLMs have become a standard component in state‑of‑the‑art VLN pipelines.  
- **Enhanced by** [[spatial-geometric encoder]] ⚠️ ⚠️ – In JanusVLN, the MLLM’s spatial reasoning is augmented with 3D prior knowledge from a dedicated encoder.

**Role in JanusVLN**

JanusVLN extends a pre‑trained MLLM to incorporate 3D prior knowledge from a [[spatial-geometric encoder]] ⚠️ ⚠️. This encoder provides geometric and depth cues (e.g., object distances, room layouts) that the MLLM alone cannot easily infer from 2D images. The integration substantially improves the agent’s ability to reason about spatial arrangements and navigate to goal locations described in natural language.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `MLLM` --[[extends]] ⚠️--> `JanusVLN`
