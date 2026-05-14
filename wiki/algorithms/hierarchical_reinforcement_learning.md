---
id: hierarchical_reinforcement_learning
title: Hierarchical Reinforcement Learning
type: algorithm
tags: []
confidence: 0.8
created_at: '2026-04-29T21:42:53'
last_reinforced: '2026-04-29T21:42:53'
supersedes: []
sources:
- papers/2405.01792.pdf
source_type: arxiv_paper
---

## Overview

**Hierarchical Reinforcement Learning (HRL)** is a reinforcement learning paradigm that decomposes complex decision-making tasks into multiple levels of abstraction. In the context of embodied robotics, HRL separates **high-level navigation planning** from **low-level locomotion control**, enabling robots to tackle long-horizon tasks with varied terrain and obstacles.

## Parameters

- **Levels**: The hierarchy consists of two main controllers:
  - **Locomotion controller** – handles low-level motor commands for walking, running, and terrain adaptation.
  - **Navigation controller** – issues high-level commands (e.g., direction, speed, waypoints) to the locomotion layer.

## Capabilities

- Integrate low-level locomotion with high-level navigation decisions, allowing the robot to react to both global goals and local perturbations.
- Enable effective navigation through challenging terrain and obstacles at high speed by leveraging learned coordination between the two levels.

## Architecture

A hierarchical RL framework is used where a high-level navigation planner issues commands to a low-level locomotion controller, both learned via reinforcement learning. The high-level planner outputs subgoals or motion directives, and the low-level controller maps those into joint torques or wheel velocities. The hierarchy allows the two controllers to be trained separately or jointly using techniques such as Model-Free Reinforcement Learning.

## Relationships

- **Uses**:
  - Model-Free Reinforcement Learning – both controllers are trained with model-free RL algorithms without requiring an explicit dynamics model.
  - Privileged Learning – the low-level controller may leverage privileged information (e.g., terrain height maps during training) to improve policy robustness.
- **Used by**:
  - Wheeled-Legged Robot – this HRL structure is applied to wheeled-legged platforms to combine agile locomotion with efficient rolling, as described in the source paper.

**Source**: arxiv paper `2405.01792.pdf`

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Hierarchical Reinforcement Learning` --extends ⚠️ ⚠️--> `Model-Free Reinforcement Learning`
- `Hierarchical Reinforcement Learning` --extends ⚠️ ⚠️--> `Privileged Learning`
- `Hierarchical Reinforcement Learning` --implements ⚠️--> `Wheeled-Legged Robot`
