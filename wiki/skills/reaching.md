---
id: reaching
title: Reaching
type: skill
tags: []
confidence: 0.8
created_at: '2026-04-30T00:19:42'
last_reinforced: '2026-04-30T00:19:42'
supersedes: []
sources:
- papers/2510.03142.pdf
source_type: arxiv_paper
---

# Reaching

**Reaching** is a navigational skill that enables an agent (robot) to move toward and physically contact or grasp a target object or location. Within the MM-Nav framework, reaching is a fundamental capability — a building block for more complex manipulation and navigation tasks.

## Capabilities

- Navigational ability to reach a target, whether an object, coordinate, or spatial region.

## Learning & Training

Reaching is learned from a reinforcement learning (RL ⚠️) expert trained specifically in a reaching environment. The expert policy is distilled or transferred to the agent’s policy network, providing robust initial performance.

## Relationships

- **Part of**: MM-Nav capabilities — reaching acts as a primitive skill within the multimodal navigation system.
- **Learned from**: RL expert ⚠️ trained in reaching environment.

## See Also

- Manipulation ⚠️ — reaching often precedes grasping and object manipulation.
- Goal-Conditioned Policy ⚠️ — a class of policies that output actions conditioned on a target pose or location.
- Sim-to-Real Transfer — reaching policies trained in simulation are commonly transferred to real robots.

## Sources

- `papers/2510.03142.pdf` — arxiv paper that describes reaching as an MM-Nav skill learned from an RL expert.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Reaching` --uses ⚠️--> `MM-Nav`
