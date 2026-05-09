---
id: visual_locomotion_rl_policy
title: Visual Locomotion RL Policy
type: algorithm
tags: []
confidence: 0.85
created_at: '2026-04-30T00:44:13'
last_reinforced: '2026-04-30'
supersedes: []
sources:
- papers/2412.04453.pdf
- papers/2210.14791.pdf
source_type: arxiv_paper
---

## Visual Locomotion RL Policy

**Visual Locomotion RL Policy** is a reinforcement learning ([[RL]] ⚠️) algorithm designed for legged robots. It takes sensory data and high‑level commands as input and produces low‑level joint actions as output, enabling the robot to execute locomotion on complex terrain while adapting to visual information. Multiple variants of this policy exist, differing in their input modalities and the broader system they are part of.

### Input

The policy accepts one of two forms of input depending on the system:

- **Mid‑level language action** ([[NaVILA framework]] ⚠️ ⚠️) – a high‑level command expressed in natural language (e.g., "step over the rock") that has been parsed into a structured locomotion instruction.
- **Egocentric camera images and velocity commands** ([[ViNL framework]] ⚠️) – visual input from onboard cameras paired with velocity commands produced by a [[Visual Navigation Policy]].

Both inputs are fused with internal state representations to generate the appropriate motor commands.

### Output

- **Low‑level joint actions** – a sequence of joint position/velocity/torque commands that drive the robot's actuators. In the [[ViNL]] variant, the output specifically targets joint positions/torques for obstacle avoidance.

### Capabilities

- Execute locomotion on **complex terrain** (uneven ground, stairs, obstacles).
- Adapt to **visual information** (e.g., depth maps, camera images) in real‑time, allowing the policy to react to changing environmental conditions.
- **Avoid stepping on small obstacles** while following provided velocity commands.
- **Traverse cluttered environments** without disrupting obstacles.

### Relationships

- **Part of**:
  - [[NaVILA framework]] ⚠️ ⚠️ – the policy receives high‑level navigation commands from NaVILA’s language planner and closes the loop with visual feedback.
  - [[ViNL]] – the policy executes obstacle‑avoiding locomotion under the guidance of a visual navigation policy.

- **Depends on**:
  - [[visual odometry]] ⚠️ and [[terrain perception]] ⚠️ for context‑aware control.
  - [[Visual Navigation Policy]] for higher‑level direction in the [[ViNL]] variant.
  - [[visual input]] ⚠️ (camera images, depth data) for online adaptation.

- **Implements**: a [[model‑free RL approach]] ⚠️ trained in simulation with domain randomization to transfer to the real world.

### Function

In the [[ViNL]] variant, the policy controls the robot’s joints to step over obstacles. It is trained in a **different simulator** than the navigation policy, which allows both policies to be optimized independently for their respective tasks. The NaVILA variant is trained jointly with the language planner.

### How It Works

The policy is trained using [[proximal policy optimization (PPO)]] ⚠️ in a simulated environment where the robot must follow either language‑grounded locomotion goals ([[NaVILA]]) or velocity commands from a visual navigation policy ([[ViNL]]). During training, the policy learns to fuse its input – whether it is a mid‑level language embedding, camera images, or velocity commands – with a visual encoder’s output, producing joint commands that respect both the intended behavior and the physical constraints of the world. The resulting controller generalizes to unseen terrains without explicit terrain classification.

> **Note**: The input format and training context differ between the NaVILA and ViNL implementations. At present there is no single unified definition; both variants share the core idea of visual‑guided locomotion learning.