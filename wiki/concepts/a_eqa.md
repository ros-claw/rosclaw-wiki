---
id: a_eqa
title: A-EQA
type: concept
tags: []
confidence: 0.85
created_at: '2026-04-29T21:00:04'
last_reinforced: '2026-04-30'
supersedes: []
sources:
- papers/2507.04047.pdf
source_type: arxiv_paper
---

# A-EQA

**A-EQA** is a benchmark for embodied question answering ⚠️ ⚠️ (EQA). It stands for *Actionable Embodied Question Answering* and evaluates an agent’s ability to navigate a 3D environment while answering questions that demand both spatial reasoning and action planning. As a benchmark, it provides a standardized testbed for embodied AI systems.

## Key Facts

- A-EQA is a **benchmark** in the **embodied question answering** domain.
- Its primary capability is to evaluate embodied question answering performance.
- The MTU3D algorithm achieved a **2% improvement in success rate** over the previous state-of-the-art on the A-EQA benchmark, demonstrating that A-EQA remains a challenging and discriminative testbed.

## Related Concepts

- **Embodied navigation**: The underlying task that enables agents to physically move through an environment to gather information.
- **Embodied question answering ⚠️**: The broader domain that A-EQA belongs to, combining navigation with question comprehension and answering.
- **Success rate ⚠️**: The primary metric used in A-EQA evaluations.
- **State-of-the-art (SOTA) ⚠️**: Refers to the best performing methods prior to MTU3D’s result.
- **MTU3D**: The model that surpassed previous SOTA on this benchmark.

## Relationship Annotations

- *A-EQA* is a *benchmark* used by *MTU3D*
- *A-EQA depends_on* embodied navigation and embodied question answering ⚠️ ⚠️ benchmarks
- *A-EQA uses* success rate ⚠️ as evaluation metric
- *MTU3D achieves* improvement on *A-EQA*