---
id: ground_slow_move_fast
title: Ground Slow, Move Fast
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-29T20:52:26'
last_reinforced: '2026-04-29T20:52:26'
supersedes: []
sources:
- papers/2512.08186.pdf
source_type: arxiv_paper
---

# Ground Slow, Move Fast

**Ground Slow, Move Fast** is a guiding principle behind [[DualVLN]] (Dual-system Vision-Language Navigation). It describes a co-design philosophy where two complementary subsystems operate at different temporal scales:

- **System 2 (Slow Grounding):** Deliberate, context-rich reasoning that builds a stable understanding of the environment, task, and goals. It “grounds” the agent slowly by processing high-level semantic information, validating plans, and resolving ambiguities.
- **System 1 (Fast Motion):** Reactive, low-latency execution that transforms the high-level plan into smooth, continuous trajectories. It “moves fast” by leveraging efficient motor policies, enabling real-time closed-loop control without waiting for full deliberation.

## Description

The guiding principle behind [[DualVLN]]: System 2 "grounds slowly" by reasoning deeply about goals, while System 1 "moves fast" by executing smooth trajectories in real time.

## Relationship to DualVLN

`Ground Slow, Move Fast` is a core principle that defines the architecture of [[DualVLN]]:

- **Is principle of** → [[DualVLN]]
- **Implements** a dual-system separation in embodied navigation, analogous to Kahneman’s System 1 / System 2 dichotomy.

## Applicability

This concept extends beyond VLN to any embodied AI system where high-level reasoning must coexist with real-time physical control. It serves as a design pattern for balancing computational cost, latency, and robustness in autonomous robots.

## Sources

- Based on arxiv paper `papers/2512.08186.pdf` (DualVLN).

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Pending review:**
- `Ground Slow, Move Fast` --[[related_to]] ⚠️--> `DualVLN` _(wikilink)_
