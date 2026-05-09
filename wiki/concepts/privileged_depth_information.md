---
id: privileged_depth_information
title: Privileged Depth Information
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-30T00:19:12'
last_reinforced: '2026-04-30T00:19:12'
supersedes: []
sources:
- papers/2510.03142.pdf
source_type: arxiv_paper
---

## Privileged Depth Information

**Privileged Depth Information** refers to the **simulation-only depth data** that is available to a reinforcement learning (RL) teacher during training in simulation, but is not available to the student policy at deployment time. It is a form of **privileged information** that provides a richer, noiseless view of the environment, enabling the teacher to learn robust behaviors that can later be distilled into a policy that relies only on **onboard sensors** (e.g., cameras, IMUs).

### Role

Privileged depth information is used to **train RL teachers** in simulation ([[Sim-to-Real]] ⚠️ ⚠️). The teacher uses this data to learn optimal control policies under ideal sensing conditions. These policies are then distilled into a student policy via techniques like **teacher-student training** or **behavior cloning**. This approach mitigates the **sim-to-real gap** by allowing the student to learn from the teacher’s performance without requiring direct access to the privileged data.

### Relationships

- **Used by** → [[Reinforcement Learning]] experts during policy training.
- **Depends on** → [[Simulation environments]] ⚠️ capable of rendering depth maps.
- **Related to** → [[Sim-to-Real]] ⚠️ ⚠️, [[Teacher-Student Training]] ⚠️, [[Domain Randomization]] ⚠️.

### Notes

- The term appears in the context of **legged locomotion** policies that use depth cameras for real-world navigation.
- Privileged depth information is often paired with **privileged states** (e.g., ground truth joint positions, friction coefficients) to further boost teacher performance.