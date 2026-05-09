---
id: reward_shaping
title: Reward Shaping
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-30T03:36:55'
last_reinforced: '2026-04-30T03:36:55'
supersedes: []
sources:
- papers/2512.09537.pdf
source_type: arxiv_paper
---

**Reward Shaping** is a technique in reinforcement learning (RL) that modifies the reward signal to provide **targeted guidance** for an RL agent, helping it learn desired behaviors more efficiently. By supplementing the sparse or delayed environment reward with shaped rewards, the agent can converge to optimal policies faster, reducing exploration time and improving sample efficiency.

Reward shaping is often implemented through potential-based functions, which guarantee that the optimal policy remains unchanged (policy invariance). It is a key component in many modern RL systems, including [[REASAN]] (Reinforcement Learning with Adaptive State-Action Normalization), where it serves to direct the agent’s learning toward high‑reward regions and accelerate convergence in complex tasks.

Related concepts: [[Reinforcement Learning]], [[Potential-Based Reward Shaping]] ⚠️, [[REASAN]], [[Exploration vs Exploitation]] ⚠️.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Pending review:**
- `Reward Shaping` --[[related_to]] ⚠️--> `REASAN` _(wikilink)_
