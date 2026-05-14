---
id: dd_ppo_distributed_proximal_policy_optimization
title: DD-PPO (Distributed Proximal Policy Optimization)
type: algorithm
tags: []
confidence: 0.8
created_at: '2026-04-29T21:07:42'
last_reinforced: '2026-04-29T21:07:42'
supersedes: []
sources:
- papers/2310.10822.pdf
source_type: arxiv_paper
---

# DD-PPO (Distributed Proximal Policy Optimization)

**DD-PPO** is a distributed variant of Proximal Policy Optimization (PPO) ⚠️ ⚠️ designed for training reinforcement learning (RL) policies across multiple parallel environments. In embodied robotics, it serves as a **local controller** that predicts low-level motor commands for robot movement based on high-level waypoint inputs.

## Key Characteristics

- **Type**: Reinforcement learning algorithm (on-policy, actor-critic)
- **Usage**: Local controller for mobile manipulation platforms
- **Key property**: Distributes PPO training across multiple workers to accelerate convergence and improve sample efficiency.

## Capabilities

- Predicts low-level actions (e.g., joint velocities, wheel speeds) for robot movement.
- Takes waypoint information (e.g., target position in the robot's frame) and outputs concrete motor commands.
- Trained end-to-end in simulation or on real hardware using distributed rollouts.

## Relationships

- **depends_on**: Proximal Policy Optimization (PPO) ⚠️ ⚠️ – DD-PPO extends PPO by distributing the policy optimization across multiple parallel agents or environments.
- **used_by**: Interbotix LoCoBot WX250 – The LoCoBot deploys a DD-PPO-based local controller as its action prediction module.

### Local Controller

The DD-PPO-based local controller serves as the final action prediction module in the robot's control stack. It receives waypoint information (e.g., a target pose from a global planner) and generates concrete motor commands that drive the robot toward that goal. The model is typically trained in a simulation environment (e.g., Isaac Sim ⚠️ or Gazebo ⚠️) with domain randomization to bridge the sim-to-real gap.

*For a detailed training procedure and network architecture, see the original paper (source: `papers/2310.10822.pdf`).*

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `DD-PPO (Distributed Proximal Policy Optimization)` --implements ⚠️--> `Interbotix LoCoBot WX250`
