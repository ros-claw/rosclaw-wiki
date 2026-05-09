---
id: janusvln
title: JanusVLN
type: algorithm
tags: []
confidence: 0.85
created_at: '2026-04-29T20:54:27'
last_reinforced: '2026-04-30'
supersedes: []
sources:
- papers/2509.22548.pdf
source_type: arxiv_paper
---

# JanusVLN

## Overview

**JanusVLN** is a novel [[Vision-Language Navigation]] (VLN) framework that decouples semantics and spatiality using **dual implicit neural memory**. It extends [[Multimodal Large Language Models]] ⚠️ ⚠️ ⚠️ (MLLMs) with 3D prior knowledge from a [[spatial-geometric encoder]] ⚠️ ⚠️ ⚠️ ⚠️ to enhance spatial reasoning from [[RGB video input]] ⚠️ ⚠️ ⚠️ alone. Historical key-value caches from both the spatial-geometric encoder and the [[visual-semantic encoder]] ⚠️ ⚠️ ⚠️ ⚠️ form the dual implicit memory, enabling efficient incremental updates by retaining only initial tokens and those within a [[sliding window]] ⚠️ ⚠️ ⚠️. The framework achieves state-of-the-art navigation performance by treating semantic understanding and geometric reasoning as separate, complementary memory streams.

## Method

JanusVLN constructs a **dual implicit neural memory** by retaining [[key-value cache]] ⚠️ ⚠️ ⚠️s from both the [[spatial-geometric encoder]] ⚠️ ⚠️ ⚠️ ⚠️ and a [[visual-semantic encoder]] ⚠️ ⚠️ ⚠️ ⚠️. Only initial tokens and those within a [[sliding window]] ⚠️ ⚠️ ⚠️ are kept, reducing redundancy and enabling efficient incremental updates. This design allows the model to maintain a compressed representation of the observed environment without explicit map-building, while preserving both semantic context (e.g., object labels, instructions) and spatial structure (e.g., 3D positions, depths).

### Key Components

| Component | Role |
|-----------|------|
| [[spatial-geometric encoder]] ⚠️ ⚠️ ⚠️ ⚠️ | Extracts 3D priors (depth, occupancy, geometry) from RGB video |
| [[visual-semantic encoder]] ⚠️ ⚠️ ⚠️ ⚠️ | Encodes object semantics, language grounding, and instruction alignment |
| dual implicit neural memory | Maintains separate key-value caches for geometry and semantics |
| sliding window | Limits token retention to reduce redundancy and computation |

## Parameters

- **Input**: [[RGB video stream]] ⚠️ + natural language instructions  
- **Memory type**: Dual implicit neural memory (spatial-geometric + visual-semantic)  
- **Token retention**: Initial tokens + sliding window  

## Capabilities

- State-of-the-art [[Vision-Language Navigation]]  
- Outperforms over 20 recent methods across multiple benchmarks  
- **Success rate improvement**:
  - +10.5% to +35.5% over methods that rely on multiple input data types (e.g., depth, semantic maps)
  - +3.6% to +10.8% over methods using only RGB video with more training data  
- **Efficient incremental updates** by retaining only key-value caches of initial and sliding window tokens  

## Results

JanusVLN sets a new state-of-the-art on standard VLN benchmarks. The improvement is most pronounced when compared to methods that fuse multiple sensor modalities (RGB + depth + segmentation), indicating that the dual memory strategy effectively mimics the benefits of extra sensors using only RGB input. Even when compared to other RGB-only methods, the gain from its efficient memory design is substantial.

## Relationships

- **depends_on**: [[Multimodal Large Language Models]] ⚠️ ⚠️ ⚠️, [[Vision-Language Navigation]], [[RGB video input]] ⚠️ ⚠️ ⚠️, [[dual implicit neural memory]], [[spatial-geometric encoder]] ⚠️ ⚠️ ⚠️ ⚠️, [[visual-semantic encoder]] ⚠️ ⚠️ ⚠️ ⚠️  
- **uses**: [[MLLM]], [[key-value cache]] ⚠️ ⚠️ ⚠️, [[sliding window]] ⚠️ ⚠️ ⚠️  
- **implements**: Efficient memory-augmented [[Vision-Language Navigation]]  
- **improves upon**: Existing VLN methods by decoupling spatial and semantic reasoning  

---

*See also: [[Vision-Language Navigation]], [[Multimodal Large Language Models]] ⚠️ ⚠️ ⚠️, [[RGB video input]] ⚠️ ⚠️ ⚠️, [[key-value cache]] ⚠️ ⚠️ ⚠️*