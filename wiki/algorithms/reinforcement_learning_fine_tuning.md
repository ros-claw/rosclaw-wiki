---
id: reinforcement_learning_fine_tuning
title: Reinforcement Learning Fine-tuning
type: algorithm
tags: []
confidence: 0.8
created_at: '2026-04-30T04:08:54'
last_reinforced: '2026-04-30T04:08:54'
supersedes: []
sources:
- papers/2505.11164.pdf
source_type: arxiv_paper
---

## Reinforcement Learning Fine-tuning

**Reinforcement Learning Fine-tuning** is a post‑distillation stage in the Agile Locomotion pipeline. After a distilled policy is produced via Multi-expert Distillation, it is further refined through reinforcement learning on a broader set of terrains — including real‑world 3D scans — to improve its adaptability and robustness.

### Parameters
- **Input**: Real‑world 3D scans of diverse terrain geometries.
- **Use**: Fine‑tune the distilled policy on a broader terrain set than used during distillation.

### Capabilities
- Adapt to new, unseen terrains encountered in real‑world deployment.
- Improve overall robustness of the locomotion policy against varied ground conditions.

### Relationships
- **Part of** → Agile Locomotion (as a downstream stage)
- **Used after** → Multi-expert Distillation (the fine‑tuning step directly follows policy distillation)

### Fine‑tuning Stage
After distillation, the learned policy is not final. A second reinforcement learning phase is executed on an expanded terrain distribution that includes high‑fidelity 3D scans collected from real environments. This stage corrects biases or over‑specialization that may have arisen during distillation and ensures the controller generalizes to the messy, irregular surfaces typical of outdoor or unstructured settings.

*Source: `data/raw/papers/2505.11164.pdf`*

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Reinforcement Learning Fine-tuning` --extends ⚠️--> `Multi-expert Distillation`
