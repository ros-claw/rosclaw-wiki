---
id: interbotix_locobot_wx250
title: Interbotix LoCoBot WX250
type: entity
tags: []
confidence: 0.85
created_at: '2026-04-29T21:07:05'
last_reinforced: '2026-04-30'
supersedes: []
sources:
- papers/2310.10822.pdf
source_type: arxiv_paper
---

# Interbotix LoCoBot WX250

The **Interbotix LoCoBot WX250** is a mobile robot platform manufactured by Interbotix ⚠️. Designed for indoor navigation and manipulation, it serves as the primary test platform for the real-world vision-language navigation (VLN) experiments described in the paper 2310.10822.pdf ⚠️. The robot is capable of following natural language instructions and operating in previously unseen laboratory environments. It features a 3-DOF robotic arm as a payload, but the paper focuses on navigation rather than manipulation.

## Capabilities

- Mobile robot navigation in complex indoor spaces
- Execution of natural language instructions queried via an LLM-based interface
- Operation in unseen lab environments without prior mapping
- Low-level control command execution for coordinated movement

## Hardware Platform

The LoCoBot WX250 is a differential-drive mobile base equipped with a 3-DOF WX250 series robotic arm and on-board sensors for visual perception. It provides a flexible platform that integrates high-level decision-making with low-level motor control. The robot supports ROS-based software stacks, enabling modular development of perception and planning pipelines.

## Research Context

The platform is used in the paper *Vision and Language Navigation in the Real World via Online Visual Language Mapping ⚠️* for experiments in real-world VLN. While the robot includes a manipulation arm, the study concentrates on navigation capabilities.

## System Components

The LoCoBot WX250 integrates with the following software components as part of the VLN pipeline:

- LLMs-based instruction parser — translates natural language commands into structured navigation goals
- Online visual-language mapper — builds and updates a semantic map from visual observations
- Language indexing-based localizer — localizes the robot within the map using language-grounded features
- DD-PPO-based local controller — executes smooth, collision-free motion using a deep reinforcement learning policy (DD-PPO)

These components communicate with the robot’s onboard ROS nodes and run either on-board or on a companion computer.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Interbotix LoCoBot WX250` --uses ⚠️ ⚠️--> `LLMs-based instruction parser`
- `Interbotix LoCoBot WX250` --uses ⚠️ ⚠️--> `Online visual-language mapper`