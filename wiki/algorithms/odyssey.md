---
id: odyssey
title: ODYSSEY
type: algorithm
tags: []
confidence: 0.85
created_at: '2026-04-29T20:53:49'
last_reinforced: '2026-04-30'
supersedes: []
sources:
- papers/2508.08240.pdf
source_type: arxiv_paper
---

---

# ODYSSEY: Unified Mobile Manipulation for Agile Quadruped Robots

**ODYSSEY** is a unified mobile manipulation framework designed for agile quadruped robots equipped with manipulators. It seamlessly integrates high-level task planning with low-level whole-body control, addressing language-guided long-horizon tasks in open-world environments. The framework demonstrates robust coordination across challenging terrains and successful sim-to-real transfer, establishing the first benchmark for long-horizon mobile manipulation.

## Architecture

ODYSSEY adopts a hierarchical design composed of two core components:

- **[[Hierarchical Planner]]**: A vision-language model (VLM) driven planner that decomposes long-horizon natural language instructions into actionable subgoals. It reasons over visual observations and robot state to generate feasible sequences of high-level commands.
- **[[Whole-body Policy]]**: A novel control policy that coordinates the quadruped’s locomotion and the manipulator’s arm movements into a single, fluid action space. This policy is trained in simulation and directly zero-shot transferred to the real robot.

The planner depends on a [[Vision-Language Model]] to interpret environmental context and task semantics. Together, these components implement **[[Language-guided long-horizon mobile manipulation]] ⚠️ ⚠️**.

## Capabilities

- **Unified mobile manipulation**: Combines locomotion and manipulation in a single coordinated framework.
- **Long-horizon task decomposition**: Breaks down complex instructions (e.g., “open the door, pick up the box, and place it on the shelf”) into sequential subtasks.
- **High-level task planning and low-level control integration**: Seamlessly bridges semantic reasoning with precise motor commands.
- **Precise action execution**: Achieves millimeter-level accuracy in manipulation while maintaining dynamic stability during locomotion.
- **Terrain robustness**: Operates reliably on uneven surfaces, stairs, slopes, and cluttered environments.
- **Generalization across diverse object configurations**: Handles varying object shapes, sizes, and positions without additional training.
- **Sim-to-real transfer**: All policies are trained entirely in simulation and deployed on real hardware without additional fine-tuning.
- **Benchmark suite**: Introduces the first standardized benchmark for evaluating long-horizon mobile manipulation on quadrupedal robots, including tasks like door opening, object retrieval, and item rearrangement.

## Relationships

- **Uses**: [[Hierarchical Planner]], [[Whole-body Policy]]
- **Depends on**: [[Vision-Language Model]]
- **Implements**: [[Language-guided long-horizon mobile manipulation]] ⚠️ ⚠️
- **Deployed on**: [[Quadruped Robot with Manipulator]]

## Sim-to-Real Transfer

ODYSSEY demonstrates that the learned whole-body policy generalizes from simulation to reality without modification. Experiments on a real quadruped robot with a 6-DOF arm show consistent performance across diverse tasks, including tasks not seen during training. The hierarchical planner, powered by a pre-trained VLM, provides semantic understanding that bridges the sim-to-real gap in task planning.

## Benchmark and Evaluation

The framework includes a benchmark of 10 long-horizon manipulation tasks, each requiring multiple steps and environmental interaction. Evaluation metrics include task success rate, execution time, and number of plan revisions. ODYSSEY outperforms baseline methods that use separate locomotion and manipulation controllers, achieving a **92.5% average success rate** in the benchmark tasks. The framework also demonstrates strong generalization across diverse object configurations and environmental layouts.

## Source

This page is derived from the paper: *ODYSSEY: A Unified Mobile Manipulation Framework for Agile Quadruped Robots* (arXiv:2508.08240, 2025).