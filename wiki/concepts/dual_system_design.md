---
id: dual_system_design
title: Dual-System Design
type: concept
tags: []
confidence: 0.85
created_at: '2026-04-29T20:52:16'
last_reinforced: '2026-04-30'
supersedes: []
sources:
- papers/2512.08186.pdf
source_type: arxiv_paper
---

## Dual-System Design

**Dual-System Design** is a foundation model architecture that separates high-level reasoning (System 2) from low-level control (System 1), improving robustness and real-time adaptability by decoupling training for generalization and interpretability. Inspired by cognitive dual-process theories from psychology, this design pattern enables robust real-time control and adaptive local decision-making.

### Key Capabilities

- **Robust real-time control**: The separation allows the low-level (System 1) to execute fast, reactive actions without waiting for high-level deliberation, enabling real-time performance.
- **Adaptive local decision-making**: System 2 provides strategic oversight, adapting System 1's behavior based on context or goals.
- **Decoupled training**: Each system can be optimized separately — System 2 for reasoning and planning, System 1 for sensorimotor execution — improving overall generalization and interpretability.

### Applications

Dual-System Design is applied to DualVLN, a vision-language navigation system that uses this architecture to combine reasoning with local action selection.

### Related Concepts

- Contrasts with end-to-end pipelines ⚠️, which typically couple reasoning and action in a single monolithic model, often at the cost of interpretability and modularity.
- Draws inspiration from System 1 / System 2 ⚠️ cognitive theory (often referenced in AI literature).
- Shares principles with hierarchical reinforcement learning (HRL) and mixture of experts (MoE) architectures.
- Directly related to vision-language navigation, as DualVLN exemplifies the dual-system paradigm in that domain.

### Sources

- Arxiv paper `papers/2512.08186.pdf` (2025).