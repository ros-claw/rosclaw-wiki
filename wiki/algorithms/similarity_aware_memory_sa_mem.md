---
id: similarity_aware_memory_sa_mem
title: Similarity-Aware Memory (SA-Mem)
type: algorithm
tags: []
confidence: 0.85
created_at: '2026-04-29T20:48:04'
last_reinforced: '2026-04-30'
supersedes: []
sources:
- papers/2512.02400.pdf
source_type: arxiv_paper
---

## Similarity-Aware Memory (SA-Mem)

**Source**: [arXiv paper 2512.02400](papers/2512.02400.pdf)

Similarity-Aware Memory (SA-Mem) is an algorithm component used in the [[Nav-R^2]] architecture. It serves as a parameter‑free memory mechanism that compresses video frames and fuses historical observations by preserving features with high relevance along both temporal and semantic dimensions, enabling efficient reasoning without introducing any additional learnable parameters.

### Description

SA-Mem compresses video frames and fuses historical observations to preserve the most target‑relevant and current observation‑relevant features. It operates along two axes:

- **Temporal relevance**: features that have consistently contributed to recent decisions are retained.
- **Semantic similarity**: features that are similar to the content of the current observation are kept, focusing memory on contextually important information.

This dual‑axis selection ensures that SA‑Mem maintains a compact yet informative history—effectively a fixed‑size representation—reducing memory footprint while preserving task‑critical cues. The compression is achieved entirely through selection, requiring **no additional parameters** beyond those of the backbone feature extractor.

### Capabilities

- **Parameter‑free** – introduces zero additional learnable parameters, making it highly efficient for reinforcement learning or end‑to‑end training pipelines.
- **Video frame compression** – reduces the stream of visual observations into a compact fixed‑size representation.
- **Historical observation fusion** – merges past observations from both temporal and semantic perspectives into a single memory state.
- Preserves the most target‑relevant and current observation‑relevant features.

### Relationships

- **Part of**: [[Nav-R^2]] – a navigation framework that leverages similarity‑aware memory to improve long‑horizon visual navigation.
- SA‑Mem acts as the episodic memory module within [[Nav-R^2]], feeding compact historical representations to downstream policy or value networks.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Similarity-Aware Memory (SA-Mem)` –[[extends]] ⚠️–> `Nav-R^2`