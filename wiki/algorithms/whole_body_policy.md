---
id: whole_body_policy
title: Whole-body Policy
type: algorithm
tags: []
confidence: 0.8
created_at: '2026-04-30T00:24:27'
last_reinforced: '2026-04-30T00:24:27'
supersedes: []
sources:
- papers/2508.08240.pdf
source_type: arxiv_paper
---

# Whole-body Policy

A **Whole-body Policy** is a low-level, learned control policy designed for legged manipulators that achieves robust whole-body coordination across challenging terrains. It is a core component of the ODYSSEY system, balancing platform agility with precise end-effector control in unstructured environments.

## Description

The Whole-body Policy serves as the low-level control layer within the ODYSSEY architecture. It processes high-level commands from a Hierarchical Planner and generates joint torques that simultaneously maintain the robot's dynamic stability while allowing precise manipulation. The policy is trained via reinforcement learning to handle complex interactions between the legs (for locomotion) and the arm (for manipulation), ensuring that arm movements do not destabilize the base and that terrain irregularities do not degrade end-effector accuracy.

## Capabilities

- **Robust coordination across challenging terrains**: The policy maintains stable locomotion on uneven, slippery, or cluttered surfaces while actively controlling the arm.
- **Maneuverability with precise end-effector control**: It enables the robot to perform tasks such as grasping, pushing, or placing objects without sacrificing speed or agility.

## Relationships

- **Hierarchical Planner**: The Whole-body Policy depends on the Hierarchical Planner for task-level commands (e.g., desired foot placements, end-effector targets). (*depends_on*)
- **ODYSSEY**: The policy is a fundamental subsystem of the ODYSSEY framework, which combines high-level planning with learned low-level control for mobile manipulation. (*part_of*)
- **Reinforcement Learning**: The policy is trained using RL, often with sim-to-real transfer techniques. (*implements*)
- **Legged Manipulator ⚠️ ⚠️**: The policy is specifically designed for robots with both legs and an actuated arm, such as the Unitree G1 or ANYmal. (*applies_to*)

## Source

This page is based on insights from the arxiv paper *ODYSSEY: A Hierarchical Framework for Whole-Body Control of Legged Manipulators* (2508.08240). See the raw source: `papers/2508.08240.pdf`.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Whole-body Policy` --extends ⚠️--> `ODYSSEY`
- `Whole-body Policy` --implements ⚠️ ⚠️--> `Unitree G1`
- `Whole-body Policy` --implements ⚠️ ⚠️--> `ANYmal`
