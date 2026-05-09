---
id: agile_locomotion_policy_deployment_on_anymal_d
title: Agile Locomotion Policy Deployment on ANYmal D
type: skill
tags: []
confidence: 0.8
created_at: '2026-04-30T04:11:47'
last_reinforced: '2026-04-30T04:11:47'
supersedes: []
sources:
- papers/2505.11164.pdf
source_type: arxiv_paper
---

# Agile Locomotion Policy Deployment on ANYmal D

## Definition

The **Agile Locomotion Policy Deployment on ANYmal D** is a skill that enables the [[ANYmal D]] quadruped robot to execute agile, dynamic locomotion behaviors in real-world complex environments. The policy is a trained unified controller that takes depth images as input and generalizes to unseen terrains without retraining.

## Parameters

| Parameter   | Value                                  |
|-------------|----------------------------------------|
| Robot       | [[ANYmal D]]                           |
| Controller  | Trained unified policy                 |
| Input       | Depth images                           |

## Capabilities

- Perform agile locomotion in real-world complex environments (e.g., uneven surfaces, obstacles, slopes).
- Generalize to unseen terrains without additional training data.

## Dependencies

This skill depends on the following:

- [[Multi-expert Distillation]] — used to distill multiple expert policies into a single unified policy.
- [[Reinforcement Learning Fine-tuning]] — applied during training to refine the distilled policy for robustness and agility.

## Implements

- [[Agile Locomotion]] — the skill directly implements a core capability of agile locomotion on the ANYmal D platform.

## Procedure

1. Prepare the [[ANYmal D]] robot with onboard depth camera.
2. Load the trained unified policy onto the robot's onboard computer (e.g., ROS 2 node or dedicated controller).
3. Provide depth images as input to the policy at runtime.
4. The policy outputs joint-level commands that drive agile locomotion behaviors.
5. Monitor robot state and environment feedback; the policy adapts to terrain changes in real time.
6. For best performance, ensure the robot’s actuators and sensors are calibrated and the depth camera is functioning properly.

## Related Pages

- [[ANYmal D]] (entity)
- [[Multi-expert Distillation]] (algorithm)
- [[Reinforcement Learning Fine-tuning]] (algorithm)
- [[Agile Locomotion]] (concept)

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Agile Locomotion Policy Deployment on ANYmal D` --[[operates_on]] ⚠️--> `ANYmal D`
- `Agile Locomotion Policy Deployment on ANYmal D` --[[uses]] ⚠️--> `Multi-expert Distillation`
