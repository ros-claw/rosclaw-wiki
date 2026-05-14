---
id: time_decayed_reward_tdr
title: Time-Decayed Reward (TDR)
type: algorithm
tags: []
confidence: 0.8
created_at: '2026-04-30T00:17:57'
last_reinforced: '2026-04-30T00:17:57'
supersedes: []
sources:
- papers/2506.17221.pdf
source_type: arxiv_paper
---

# Time-Decayed Reward (TDR)

**Time-Decayed Reward (TDR)** is a mechanism in reinforcement fine-tuning ⚠️ ⚠️ ⚠️ ⚠️ that strategically weights multi-step future actions by applying a temporal decay to the reward signal. By attenuating the influence of rewards that are temporally distant from the current state, TDR focuses learning on immediate and near-future consequences, improving sample efficiency and policy stability in long-horizon tasks.

## Overview

TDR operates as a drop-in modification to the reward calculation in reinforcement learning based fine-tuning pipelines. Instead of treating all future rewards equally (as in standard discounted returns), it applies a **decay factor** that reduces the contribution of rewards proportional to their time-step distance from the decision point. This encourages the agent to prioritize actions that yield faster returns, naturally aligning with embodied AI tasks where delayed rewards are often less reliable.

## Mechanism

Let a trajectory consist of states \(s_1, s_2, \dots, s_T\) and actions \(a_1, a_2, \dots, a_{T-1}\) with observed rewards \(r_2, \dots, r_T\) (reward after each action). The standard discounted return at timestep \(t\) is:

\[
G_t = \sum_{k=0}^{T-t-1} \gamma^k r_{t+k+1}
\]

TDR modifies this by applying a **time‑aware weight** \(w(\Delta t)\) that decays with the gap \(\Delta t\) between the action and the reward:

\[
G_t^{\text{TDR}} = \sum_{k=0}^{T-t-1} w(k) \, \gamma^k r_{t+k+1}
\]

where \(w(k)\) is a monotonically decreasing function (e.g., exponential, linear, or step). Common choices include:

- **Exponential decay**: \(w(k) = e^{-\lambda k}\)
- **Linear decay**: \(w(k) = \max(1 - \alpha k, 0)\)
- **Step decay**: \(w(k) = 1\) for \(k < K\), else \(0\)

The decay shape and strength are hyperparameters that control how aggressively future rewards are suppressed.

## Capabilities

- **Enhances reinforcement fine-tuning ⚠️ ⚠️ ⚠️ ⚠️** by decaying reward over time, leading to faster convergence and reduced variance in gradient estimates.
- Improves policy robustness in environments where reward signals become noisy or sparse over long horizons.
- Naturally integrates with existing RLHF ⚠️ and VLA model ⚠️ fine-tuning pipelines.

## Usage in VLN-R1

TDR is employed in the reinforcement fine-tuning ⚠️ ⚠️ ⚠️ ⚠️ (RFT) stage of the VLN-R1 system for Vision-Language Navigation. In VLN-R1, an agent must follow natural‑language instructions through visual environments — a task where rewards (e.g., goal reached, subgoal success) often arrive many steps after the critical decision. TDR helps the agent attribute credit to actions that lead to near‑term progress, complementing the cross-modal attention ⚠️ backbone.

The specific decay curve used in VLN‑R1 is an exponential decay with \(\lambda = 0.1\), chosen based on ablation studies that balanced long‑term planning against myopic convergence.

## Relationships

- **depends_on**: reinforcement learning, discounted return ⚠️
- **implements**: credit assignment ⚠️ with temporal awareness
- **used_in**: reinforcement fine-tuning ⚠️ ⚠️ ⚠️ ⚠️ of VLN-R1
- **related_to**: Generalized Advantage Estimation (GAE) ⚠️ (both shape temporal weighting; TDR is simpler and decoupled from baseline estimation)

## References

- Source paper: arxiv 2506.17221 – *VLN-R1: Vision-Language Navigation via Reinforcement Fine-Tuning* (TDR introduced in Section 3.3).
- See also Unitree G1 for a hardware platform that may benefit from TDR in future manipulation fine-tuning.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Time-Decayed Reward (TDR)` --based_on ⚠️--> `embodied AI`
- `Time-Decayed Reward (TDR)` --extends ⚠️--> `VLN-R1`
- `Time-Decayed Reward (TDR)` --implements ⚠️--> `Unitree G1`
