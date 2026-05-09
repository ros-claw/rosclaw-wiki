---
id: neural_net_parkour_policy
title: Neural Net Parkour Policy
type: algorithm
tags: []
confidence: 0.8
created_at: '2026-04-29T21:43:21'
last_reinforced: '2026-04-29T21:43:21'
supersedes: []
sources:
- papers/2309.14341.pdf
source_type: arxiv_paper
---

# Neural Net Parkour Policy

## Overview

A **Neural Net Parkour Policy** is a single neural net policy trained entirely in simulation using large-scale reinforcement learning, operating directly from camera images to produce precise control outputs despite imprecise actuation and low-quality depth sensing. It demonstrates end-to-end learning of dynamic parkour maneuvers for legged robots.

### Parameters

| Parameter | Value |
|-----------|-------|
| Training method | Large-scale reinforcement learning |
| Input | Single front-facing depth camera image |
| Output | End-to-end precise control behavior |
| Architecture | Single neural net policy |
| Simulation used | Yes |

## Training Details

Trained in simulation with RL, likely using a variant of PPO or similar. The policy learns to overcome sensing and actuation noise end-to-end, relying on the high diversity of simulated environments and randomized physical parameters. The simulation runs at scale to expose the policy to a wide range of obstacle configurations and failure modes.

## Results

The policy demonstrates dynamic parkour maneuvers including:
- High jump on obstacles up to **2x the robot's height**
- Long jump across gaps up to **2x the robot's length**
- Handstand (static inversion)
- Running across tilted ramps
- **Generalization to novel obstacle courses** with different physical properties (e.g., friction, geometry, compliance)

These results indicate that pure simulation‑based training with domain randomization can produce robust, transferable locomotion skills for quadrupedal robots.

## Capabilities

- [[High Jump]] ⚠️ over tall obstacles
- [[Long Jump]] ⚠️ across wide gaps
- [[Handstand]] ⚠️
- [[Ramp Traversal]] ⚠️
- [[Novel Obstacle Generalization]] ⚠️

## Relationships

- **Uses:** [[Sim-to-Real Transfer]], [[Large-Scale RL]] ⚠️, [[Domain Randomization]] ⚠️
- **Depends on:** [[Single Depth Camera]] ⚠️ (noisy, low‑resolution perception), [[Imprecise Actuation]] ⚠️ (noisy servos, imperfect torque control)
- **Implements:** [[End-to-End Control]] ⚠️, [[Visuomotor Policy]] ⚠️

## Source

This algorithm is described in the paper *Neural Net Parkour Policy* (arXiv:2309.14341).