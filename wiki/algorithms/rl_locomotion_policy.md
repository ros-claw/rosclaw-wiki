---
id: rl_locomotion_policy
title: RL Locomotion Policy
type: algorithm
tags: []
confidence: 0.8
created_at: '2026-04-30T03:23:45'
last_reinforced: '2026-04-30T03:23:45'
supersedes: []
sources:
- papers/2512.09537.pdf
source_type: arxiv_paper
---

## RL Locomotion Policy

The **RL Locomotion Policy** is a lightweight, reinforcement learning-based algorithm designed for **locomotion control** of legged robots. It takes sensor inputs and outputs leg motor commands directly, enabling agile and adaptive walking, running, or other gaits. The policy is part of the [[REASAN]] framework, where it serves as the low-level control component that translates high-level plans into physical actions.

### Capabilities
- **Generates leg motor commands** for stable and efficient locomotion.
- **Lightweight neural network** architecture, allowing real-time inference on embedded hardware with minimal computational overhead.

### Relationships
- **Part of**: [[REASAN]] — the RL Locomotion Policy is one of the core modules in the REASAN system.
- **Uses**: [[Reinforcement Learning]] for policy optimization, typically trained in simulation before deployment.
- **Dependencies**: Relies on a [[Robot Model]] ⚠️ (e.g., kinematic and dynamic parameters) and a well-designed [[Reward Function]] ⚠️ to learn stable gaits.

### Architecture
The policy is typically implemented as a compact multilayer perceptron (MLP) or recurrent neural network (RNN) that processes proprioceptive and exteroceptive inputs to produce joint-level torque or position commands. Its lightweight nature makes it suitable for onboard deployment without significant latency.

### Usage
The policy is executed at high frequency (e.g., 50–100 Hz) and can be combined with a [[State Estimator]] ⚠️ and a [[Footstep Planner]] ⚠️ for full autonomous locomotion.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `RL Locomotion Policy` --[[extends]] ⚠️--> `REASAN`
