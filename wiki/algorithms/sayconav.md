---
id: sayconav
title: SayCoNav
type: algorithm
tags: []
confidence: 0.8
created_at: '2026-04-29T20:49:33'
last_reinforced: '2026-04-29T20:49:33'
supersedes: []
sources:
- papers/2505.13729.pdf
source_type: arxiv_paper
---

## SayCoNav

SayCoNav is an **LLM-based decentralized multi-robot navigation algorithm** designed for cooperative exploration and object search in large-scale unknown environments. It leverages [[Large Language Models (LLMs)]] to automatically generate adaptive collaboration strategies for teams of heterogeneous robots. Each robot executes its own instance of the algorithm, producing plans and actions in a fully decentralized manner while sharing critical information with teammates to continuously update step-by-step plans.

### Overview

SayCoNav enables a team of autonomous robots to coordinate without a central controller. At each planning cycle, every robot uses an LLM to reason about its current observations, shared information from other robots, and the overall task goal (e.g., locating multiple objects). The LLM produces a customized strategy that determines which robot should explore which region, how to dynamically reassign targets, and when to backtrack or regroup. By relying on natural language as the communication medium, SayCoNav can handle heterogeneous robot capabilities and changing mission priorities.

### Key Capabilities

- Generates **adaptive collaboration strategies** among heterogeneous robots without pre-programmed protocols.
- Produces plans and actions in a **decentralized** way – each robot runs its own LLM-based reasoning.
- Shares information between robots to **update step-by-step plans** in real time.
- Improves **search efficiency** by up to **44.28%** compared to state-of-the-art baselines.
- Dynamically adapts to **changing conditions** (e.g., robot failures, newly discovered obstacles, shifting target locations).

### Evaluation

SayCoNav was evaluated on the [[Multi-Object Navigation (MultiON)]] task, which requires a team of robots to locate and approach multiple objects in a previously unseen environment. Tests were conducted with varied team compositions (homogeneous and heterogeneous) and under different environmental complexities. The algorithm consistently outperformed baseline methods, achieving up to 44.28% improvement in search efficiency (measured as the number of steps or time required to find all objects).

### Dependencies & Relationships

- **Uses**: [[Large Language Models (LLMs)]] for reasoning and plan generation; [[decentralized planning]] ⚠️ framework.
- **Depends on**: The [[Multi-Object Navigation (MultiON)]] benchmark for training and evaluation.

### Related Pages

- [[Large Language Models (LLMs)]]
- [[Decentralized Multi-Robot Navigation]]
- [[Multi-Object Navigation (MultiON)]]
- [[Heterogeneous Robot Teams]] ⚠️
- [[Sim-to-Real Transfer]] (potential extension)

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `SayCoNav` --[[implements]] ⚠️--> `Large Language Models (LLMs)`
- `SayCoNav` --[[based_on]] ⚠️ ⚠️--> `Multi-Object Navigation (MultiON)`
- `SayCoNav` --[[based_on]] ⚠️ ⚠️--> `Decentralized Multi-Robot Navigation`
