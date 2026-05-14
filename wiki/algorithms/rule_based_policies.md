---
id: rule_based_policies
title: Rule-based policies
type: algorithm
tags: []
confidence: 0.8
created_at: '2026-04-30T00:32:12'
last_reinforced: '2026-04-30T00:32:12'
supersedes: []
sources:
- papers/2511.06182.pdf
source_type: arxiv_paper
---

**Rule-based policies** are heuristic or manually defined strategies used within the OpenVLN framework to guide the fine-tuning of a Vision-Language Model (VLM) under limited training data conditions.

### Purpose
The primary purpose of rule-based policies is to enable **data-efficient fine-tuning** of a VLM when fully supervised data is scarce. They act as a proxy supervisory signal, leveraging domain knowledge to shape the behavior of the model without requiring large labeled datasets.

### Capabilities
- **Data-efficient fine-tuning**: By embedding prior knowledge, rule-based policies reduce the need for thousands of annotated examples, making VLM adaptation feasible in low-resource settings.
- **Structured guidance**: They provide explicit action preferences or constraints that the VLM learns to follow, enforcing consistency with known task dynamics.

### Relationships
- **`part_of`**: OpenVLN (an embodied vision-and-language navigation framework).
- **`uses`**: Reinforcement Learning – the rule-based policy serves as a reward shaping mechanism or as a teacher policy within an RL loop to update the VLM.

### Role
In the OpenVLN framework, rule-based policies are employed within the reinforcement learning paradigm. They define a baseline behavior that the VLM should approximate, allowing the agent to bootstrap its policy from simple heuristics and then improve via interaction with the environment. This approach bypasses the need for extensive human demonstrations, enabling **data-efficient fine-tuning** of the VLM even when only a small number of training trajectories are available.

> **Source**: arxiv paper `2511.06182.pdf`

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Rule-based policies` --extends ⚠️--> `OpenVLN`
