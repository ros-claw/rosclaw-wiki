---
id: state_adaptive_mixture_of_experts_same
title: State-Adaptive Mixture of Experts (SAME)
type: algorithm
tags: []
confidence: 0.85
created_at: '2026-04-29T20:58:14'
last_reinforced: '2026-04-30'
supersedes: []
sources:
- papers/2412.05552.pdf
source_type: arxiv_paper
---

# State-Adaptive Mixture of Experts (SAME)

**State-Adaptive Mixture of Experts (SAME)** is a novel model that integrates high-level category-specific search and low-level language-guided navigation into a single agent, consolidating diverse language-guided visual navigation tasks into a generic framework. It employs a state-adaptive mixture of experts — a dynamic gating mechanism that selects expert modules based on the current navigation state and task type — allowing the agent to handle instructions of varying granularity and adapt to changing observations, dynamically combining shared knowledge and task-specific capabilities based on the current observation and instruction granularity.

---

## Key Innovation

The core innovation is the **state-adaptive gating mechanism**, which dynamically selects which expert modules to activate based on:

- The agent's current **navigation state** (e.g., position, velocity, scene context)
- The **type of task** being performed (e.g., category-specific search vs. language-guided navigation)

This enables the agent to smoothly transition between high-level goal searching (e.g., "find a kitchen") and low‑level instruction following (e.g., "turn left at the door"), all within a single model. The state-adaptive mechanism allows the agent to infer decisions from different-granularity language and dynamic visual observations, enabling a single policy to excel across multiple navigation benchmarks.

---

## Capabilities

- Enables an agent to infer decisions based on **different-granularity language instructions** and **dynamic observations**
- Consolidates diverse navigation tasks into a **unified framework** by sharing general knowledge and exploiting task-specific capabilities
- Simultaneously addresses **seven navigation tasks** (e.g., category‑specific search, language‑guided point navigation, etc.)
- Outperforms or achieves **highly comparable performance** to task‑specific agents on standard benchmarks

---

## Relationships

- **type**: [[Mixture of Experts]] model
- **adaptation**: state-adaptive routing based on observations and language
- **uses** → [[Mixture of Experts]], [[state-adaptive mechanism]] ⚠️, [[Language instructions]] ⚠️, [[Visual observations]] ⚠️
- **depends_on** → [[instruction-guided visual navigation]], [[dynamic observations]] ⚠️ ⚠️, shared general knowledge, task-specific expert modules

---

## Architecture Overview

SAME builds on a transformer‑based policy that processes:

1. **Language instructions** – parsed into task embeddings of varying granularity
2. **Visual observations** – egocentric RGB or depth images
3. **State features** – robot pose, scene semantics, and task context

These inputs are fed into a shared trunk, followed by a **state‑adaptive gating network** that computes a weighted combination of expert outputs. Each expert is a feed‑forward module specialized for certain subtask (e.g., exploration, object detection, low‑level control).

The resulting mixed output drives the agent's action policy (velocity commands or discrete actions) via a common head.

---

## References

- Source: `data/raw/papers/2412.05552.pdf`
- Related: [[Mixture of Experts]], [[instruction-guided visual navigation]], [[dynamic observations]] ⚠️ ⚠️, [[navigation tasks]] ⚠️

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `State-Adaptive Mixture of Experts (SAME)` --[[based_on]] ⚠️--> `instruction-guided visual navigation`