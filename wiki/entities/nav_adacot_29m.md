---
id: nav_adacot_29m
title: Nav-AdaCoT-2.9M
type: entity
tags: []
confidence: 0.8
created_at: '2026-04-29T23:58:54'
last_reinforced: '2026-04-29T23:58:54'
supersedes: []
sources:
- papers/2601.08665.pdf
source_type: arxiv_paper
---

## Nav-AdaCoT-2.9M

**Nav-AdaCoT-2.9M** is a large-scale embodied navigation dataset featuring 2.9 million samples annotated with an **adaptive chain-of-thought (CoT)** reasoning paradigm. It is the largest available dataset of its kind, designed to train vision-language navigation agents that can dynamically adjust both *when* to reason and *what* to reason about during navigation.

### Parameters

| Parameter | Value |
|-----------|-------|
| Size | 2.9 million samples |
| Type | Embodied navigation dataset with reasoning annotations |
| Annotation | Adaptive chain-of-thought (CoT) — each episode includes expert CoT traces that teach the agent to decide the timing and content of intermediate reasoning steps |
| Purpose | Induce reasoning paradigms that adjust both *when to think* and *what to think* |

### Capabilities

- **Largest embodied navigation dataset** with reasoning annotations, providing a rich resource for training complex navigation policies.
- Enables training of **VLingNav** agents with adaptive CoT reasoning, improving both interpretability and performance in long-horizon navigation tasks.
- Supports research into reasoning-grounded action selection and sim-to-real transfer in embodied AI.

### Relationships

- **Used by**: VLingNav — the dataset is explicitly constructed to train VLingNav models, which leverage visual-language inputs and adaptive reasoning to navigate.

### Dataset Composition

The dataset contains navigation episodes collected from simulated environments. Each episode is paired with expert CoT reasoning traces that demonstrate adaptive thinking: the agent learns to produce a reasoning step only when necessary (e.g., at decision points) and to focus that reasoning on relevant spatial or semantic cues. This structure contrasts with static, full‑sequence CoT annotations, enabling more efficient and robust decision‑making.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Nav-AdaCoT-2.9M` --uses ⚠️--> `VLingNav`
