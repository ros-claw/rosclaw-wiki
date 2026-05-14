---
id: navila
title: NaVILA
type: algorithm
tags: []
confidence: 0.85
created_at: '2026-04-29T20:56:57'
last_reinforced: '2026-04-30'
supersedes: []
sources:
- papers/2412.04453.pdf
source_type: arxiv_paper
---

# NaVILA

**Type**: Algorithm  
**Source**: [2412.04453](data/raw/papers/2412.04453.pdf) (arXiv)

## Overview

NaVILA is a **2-level framework** for Vision-and-Language Navigation on legged robots. It first generates mid-level actions with spatial information in natural language (e.g., "moving forward 75 cm"), then uses a visual locomotion RL policy to execute those actions as low-level joint commands. This separation of high-level reasoning from low-level control enables robust navigation in complex and cluttered scenes. The framework unifies a Vision-Language-Action model with locomotion skills ⚠️ ⚠️, avoiding the need to directly predict low-level actions from the VLA.

## Architecture

The framework consists of two levels:

1. **High-level reasoning** – A Vision-Language-Action model interprets human language instructions and produces **mid-level actions** expressed as natural language phrases that include spatial information (e.g., distances, directions). These mid-level actions are the bridge between abstract commands and concrete motor commands.
2. **Low-level execution** – A **visual locomotion RL policy ⚠️ ⚠️** takes the mid-level action as input and translates it into low-level joint angles or torques, enabling the legged robot to move precisely through the environment.

This two-level design is key to NaVILA's robustness: the high-level module can be trained on diverse language data, while the low-level policy can be fine-tuned for specific robot morphologies and terrain conditions.

## Capabilities

NaVILA can:

- **Translate human language instructions** directly to low-level leg joint actions, bypassing the need for manually engineered waypoints.
- **Generate mid-level actions with spatial information** in natural language form (e.g., "move forward 75 cm").
- **Navigate through challenging and cluttered scenes** with legged robots, including stairs, narrow passages, and uneven terrain.
- **Improve performance** on existing navigation benchmarks by effectively leveraging the two-level structure.
- **Work with the IsaacLab benchmark ⚠️ ⚠️ ⚠️**, which provides realistic simulated scenes and low-level control interfaces.
- **Run on real-world robots**, as demonstrated in the original paper with a Unitree G1 (or similar legged platform).

## Relationships

- **uses::** Vision-Language-Action model, locomotion skills ⚠️ ⚠️, RL policy ⚠️ ⚠️
- **depends_on::** vision-language model, locomotion RL policy ⚠️, legged robot platform ⚠️
- **targets::** legged robots
- **evaluated_on::** IsaacLab benchmark ⚠️ ⚠️ ⚠️, Unitree G1
- **implements::** two-level navigation framework ⚠️ (for legged robots)
- **part_of::** legged robot navigation ⚠️ family of algorithms

## Evaluation & Benchmarks

NaVILA was evaluated on the IsaacLab benchmark ⚠️ ⚠️ ⚠️ using both simulated and real-world environments. In simulation, the framework demonstrated strong generalization across different scenes and terrains. Real-world experiments on a legged robot (e.g., Unitree G1) confirmed that the two-level approach enables reliable navigation where end-to-end policies often fail.

## References

- Original paper: *NaVILA: Legged Robot Vision-Language Navigation via Imitation Learning* (arXiv:2412.04453)