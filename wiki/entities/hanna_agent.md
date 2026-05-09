---
id: hanna_agent
title: HANNA Agent
type: entity
tags: []
confidence: 0.8
created_at: '2026-04-29T21:24:51'
last_reinforced: '2026-04-29T21:24:51'
supersedes: []
sources:
- papers/1909.01871.pdf
source_type: arxiv_paper
---

## HANNA Agent

**HANNA** (Hierarchical Attention-based Navigation and Assistance agent) is a memory-augmented neural agent designed for interactive embodied tasks. It operates in tandem with its counterpart [[ANNA Agent]] ⚠️ ⚠️ ⚠️ ⚠️ to complete goal-driven navigation and object retrieval while proactively requesting human assistance when uncertain.

---

### Overview

HANNA is built on a hierarchical decision-making framework that allows it to decompose complex tasks into manageable sub-goals. It is trained using a novel algorithm that encourages curiosity and retrospective learning, enabling it to avoid repeating past failures and to self-assess its own progress potential.

---

### Architecture

The agent employs a **memory-augmented neural network** that models multiple levels of decision-making hierarchically. This structure allows HANNA to:

- Maintain a long-term memory of past episodes, obstacles, and successful strategies.
- Reason over goals at different granularities (e.g., room-level navigation vs. object-level interaction).
- Integrate visual and linguistic inputs from both its own sensors and assistance provided by [[ANNA Agent]] ⚠️ ⚠️ ⚠️ ⚠️.

---

### Capabilities

- **Help-seeking**: When the agent encounters uncertainty (e.g., ambiguous object location or occluded view), it can explicitly request help from [[ANNA Agent]] ⚠️ ⚠️ ⚠️ ⚠️.
- **Multimodal interpretation**: Understands natural language commands and visual cues (e.g., pointing gestures or highlighted areas).
- **Navigation and object search**: Uses hierarchical reasoning to explore environments efficiently.
- **Error correction**: Learns to identify and avoid actions that previously led to failures.
- **Metacognitive prediction**: Estimates its own likelihood of making progress on the current task, allowing it to decide when to persist versus request assistance.

---

### Learning Algorithm: Retrospective Curiosity-Encouraging Imitation Learning

HANNA is trained using **Retrospective Curiosity-Encouraging Imitation Learning**, a hybrid algorithm that combines:

- **Imitation learning** from expert demonstrations.
- **Curiosity-driven exploration** to incentivize novel and informative experiences.
- **Retrospective analysis** of past trajectories to reinforce successful patterns and penalize repeated mistakes.

This algorithm helps the agent develop robust policies that generalize to unseen environments and request help appropriately.

---

### Relationships

- `uses`: [[ANNA Agent]] ⚠️ ⚠️ ⚠️ ⚠️ (cooperative assistant)
- `trained_with`: [[Retrospective Curiosity-Encouraging Imitation Learning]]

---

### Sources

- `papers/1909.01871.pdf`

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `HANNA Agent` --[[uses]] ⚠️--> `Retrospective Curiosity-Encouraging Imitation Learning`
