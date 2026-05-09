---
id: memory_guided_decision_making
title: Memory-guided Decision-Making
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-30T00:09:04'
last_reinforced: '2026-04-30T00:09:04'
supersedes: []
sources:
- papers/2511.06840.pdf
source_type: arxiv_paper
---

# Memory-guided Decision-Making

**Memory-guided Decision-Making** is a paradigm in which an agent leverages stored historical context alongside current observations to inform action selection. Unlike reactive policies that map only the immediate sensory input to actions, memory-guided approaches maintain a bounded internal state — often implemented as a queue, buffer, or recurrent network — enabling the agent to reason over past events, detect temporal patterns, and make more consistent long‑term decisions.

In embodied navigation, this concept is critical for tasks where partial observability or ambiguous sensor readings require the agent to "remember" where it has been, what it has seen, and which strategies succeeded or failed previously.

## Capabilities

- **Decision-making with historical context** – The agent consults a memory of past states and actions before choosing the next action, reducing greedy or repetitive errors.

## Enhancements

- Enhanced by **[[Dynamic Bounded Memory Queue]]** – A fixed‑size, sliding‑window memory structure that retains the most recent observations and actions. Its bounded nature keeps computational cost predictable while still providing sufficient context for short‑term planning.

## Mechanism

Memory-guided Decision-Making combines the current observation with memory to make informed navigation choices. The agent fuses a representation of the current sensor reading (e.g., depth image, RGB, or occupancy grid) with a compressed or stored version of recent history via a lightweight attention or recurrent layer. The resulting joint representation is passed to a policy network that outputs the next action (e.g., a waypoint or velocity command). The memory is updated at each step, and the oldest entry is discarded when the queue reaches its capacity.

## Relationships

- **Used by** **[[PanoNav]]** – The panoramic navigation system integrates a memory‑guided decision module to leverage historical viewpoints when traversing complex indoor environments.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Pending review:**
- `Memory-guided Decision-Making` --[[related_to]] ⚠️--> `PanoNav` _(wikilink)_
