---
id: memory_augmented_planning
title: Memory-Augmented Planning
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-30T04:30:11'
last_reinforced: '2026-04-30T04:30:11'
supersedes: []
sources:
- papers/2510.08713.pdf
source_type: arxiv_paper
---

# Memory-Augmented Planning

## Definition

Memory-Augmented Planning incorporates hierarchical memory mechanisms to retain and utilize both recent (short-term) and historical (long-term) information for improved navigation decisions. It fuses perceptual cues from the immediate environment with trajectory context accumulated over past episodes, enabling stable and coherent reasoning over extended planning horizons.

## Capabilities

- **Short-term & long-term fusion:** Combines momentary sensor readings with previously learned trajectories to maintain consistency.
- **Extended horizon reasoning:** Supports planning beyond typical local windows by drawing on stored contextual knowledge.
- **Robustness to ambiguous cues:** When perceptual input is noisy or incomplete, the memory component provides priors from analogous past situations.

## Relationships

- **Depends on** [[Hierarchical Memory Mechanism]] ⚠️ ⚠️ for the encoding, storage, and retrieval of spatiotemporal experience.
- **Used by** [[UniWM]] as a core module within its unified world model architecture for navigation.

## Related Concepts

- [[Hierarchical Memory Mechanism]] ⚠️ ⚠️ – the underlying memory framework that stores short-term episodes and long-term trajectory knowledge.
- [[UniWM]] – a world model that leverages memory-augmented planning to achieve stable long‑horizon reasoning.
- [[Embodied AI]] – the broader field under which memory‑augmented planning is applied.
- [[Sim-to-real]] ⚠️ – memory systems often require transfer from simulation to real-world deployment.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Memory-Augmented Planning` --[[related_to]] ⚠️ ⚠️--> `Embodied AI`
**Pending review:**
- `Memory-Augmented Planning` --[[related_to]] ⚠️ ⚠️--> `UniWM` _(wikilink)_
