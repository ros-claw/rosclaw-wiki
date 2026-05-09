---
id: imitation_learning_objective
title: Imitation Learning Objective
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-30T02:23:10'
last_reinforced: '2026-04-30T02:23:10'
supersedes: []
sources:
- papers/2203.02764.pdf
source_type: arxiv_paper
---

## Imitation Learning Objective

The **Imitation Learning Objective** is a [[learning objective]] ⚠️ used to train [[VLN agents]] ⚠️ ⚠️ (Vision-and-Language Navigation agents) for [[navigation]] ⚠️ tasks. It is a **simple imitation learning** approach that directly supervises the agent's actions based on expert demonstrations.

### Details

- **Type**: Simple imitation learning (supervised behavior cloning).
- **Capabilities**: Trains agents for navigation by mimicking expert trajectories.
- **Application**: Used in the paper *"VLN-BERT: A BERT-Style Model for Vision-and-Language Navigation"* (arXiv 2203.02764) to train agents that outperform prior methods on benchmark datasets.

### Usage in VLN

The objective is applied during [[behavior cloning]] ⚠️ of [[VLN agents]] ⚠️ ⚠️, where the agent is trained to predict the next action (e.g., moving forward, turning left/right) given the current observation and language instruction. The loss is typically [[cross-entropy loss]] ⚠️ between the predicted action distribution and the expert's action.

### Relation to Other Concepts

- Depends on: [[expert demonstration]] ⚠️ data from [[R2R-CE]] and [[RxR-CE]] datasets.
- Implements: [[supervised learning]] ⚠️ for [[Vision-and-Language Navigation]].
- Supersedes: earlier methods that used [[reinforcement learning]] objectives (though some VLN models combine IL with RL).

### Performance

Agents trained with this objective achieved state-of-the-art performance on:
- [[R2R-CE]] (Room-to-Room Continuous Environment)
- [[RxR-CE]] (Room-by-Room Continuous Environment)

The simple imitation learning approach proved effective despite its simplicity, suggesting that high-quality expert data and a well-designed model architecture (e.g., [[VLN-BERT]]) are key to navigation success.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Imitation Learning Objective` --[[applies_to]] ⚠️ ⚠️--> `R2R-CE`
- `Imitation Learning Objective` --[[applies_to]] ⚠️ ⚠️--> `RxR-CE`
- `Imitation Learning Objective` --[[related_to]] ⚠️--> `Vision-and-Language Navigation`
