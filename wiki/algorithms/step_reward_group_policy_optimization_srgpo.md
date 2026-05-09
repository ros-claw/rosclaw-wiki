---
id: step_reward_group_policy_optimization_srgpo
title: Step Reward Group Policy Optimization (SRGPO)
type: algorithm
tags: []
confidence: 0.8
created_at: '2026-04-29T20:48:52'
last_reinforced: '2026-04-30'
supersedes: []
sources:
- papers/2512.02631.pdf
source_type: arxiv_paper
---

## Step Reward Group Policy Optimization (SRGPO)

**Type:** Algorithm – also described as a *Step-level Reinforcement Fine-Tuning (RFT) algorithm* (see conflict note below).  
**Related to:** [[Reinforcement Learning]], [[Vision-Language Navigation (VLN)]], [[Post-training]] ⚠️, [[Process Reward Model]] ⚠️, [[GRPO]], [[GiGPO]] ⚠️ ⚠️ ⚠️ ⚠️, [[Reinforcement Fine-Tuning (RFT)]]

**Description:**  
Step Reward Group Policy Optimization (SRGPO) is a novel step-level Reinforcement Fine-Tuning (RFT) method specifically designed for post-training Vision-Language Navigation (VLN) agents. SRGPO introduces **verifiable process rewards** and performs efficient **step-level advantage estimation** by randomly grouping different navigation steps within a trajectory. This approach provides dense, fine-grained reward signals during training, leading to improved planning capability, training stability, convergence efficiency, and generalization compared to existing methods.

---

### Mechanism

SRGPO defines verifiable process rewards for navigation tasks and performs step-level advantage estimation by randomly grouping different navigation steps. This yields dense reward signals for reinforcement learning, addressing the sparse reward problem inherent in long-horizon VLN tasks.

---

### Capabilities

- Provides dense reward signals for RL training by breaking down trajectory-level rewards into step-level process rewards.
- Enhances planning capability of [[VLN]] ⚠️ agents (particularly those based on [[LVLM]] ⚠️s) by offering more granular feedback per navigation step.
- Improves **training stability**, **convergence efficiency**, and **generalization** compared to [[GRPO]] and [[GiGPO]] ⚠️ ⚠️ ⚠️ ⚠️.
- Outperforms baseline methods in post-training settings for Vision-Language Navigation.

---

### Parameters & Key Features

| Feature | Description |
|---------|-------------|
| **Algorithm type** | Step-level Reinforcement Fine-Tuning (RFT) |
| **Reward type** | Verifiable process rewards |
| **Advantage estimation** | Step-level, with random grouping of navigation steps |
| **Key innovations** | Verifiable process rewards, random step grouping, step-level advantage estimation |
| **Comparison baselines** | [[GRPO]] and [[GiGPO]] ⚠️ ⚠️ ⚠️ ⚠️ (SRGPO demonstrates superior performance over both) |

---

### Relationships

- **Extends:** [[Reinforcement Fine-Tuning (RFT)]] – SRGPO is a step-level generalization of RFT.
- **Used by:** [[SeeNav-Agent]] leverages SRGPO for post-training.
- **Compared with:** [[GRPO]] (Group Relative Policy Optimization) and [[GiGPO]] ⚠️ ⚠️ ⚠️ ⚠️ (Generalized Group Policy Optimization) – SRGPO shows better training stability, convergence, and generalization.
- **Family:** A member of the process reward / step-level RL family for VLN.

> **Conflict note:** The original page listed SRGPO’s type simply as “Algorithm,” while the source paper describes it as a “Step-level Reinforcement Fine-Tuning (RFT) algorithm.” Both perspectives are preserved here. The more specific descriptor is used in the new content.

---

### Notes

- SRGPO’s step-level reward structure addresses the sparse reward problem common in long-horizon VLN tasks.
- The random grouping mechanism in advantage estimation reduces variance while maintaining bias control, contributing to stable and efficient training.
- Advantages over GRPO and GiGPO include improved training stability, better convergence efficiency, and enhanced generalization capability.

---

*See source: `papers/2512.02631.pdf`*