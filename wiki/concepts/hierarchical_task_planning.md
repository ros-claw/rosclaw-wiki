---
id: hierarchical_task_planning
title: Hierarchical Task Planning
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-30T03:57:56'
last_reinforced: '2026-04-30T03:57:56'
supersedes: []
sources:
- papers/2507.06747.pdf
source_type: arxiv_paper
---

# Hierarchical Task Planning

**Hierarchical Task Planning** is a concept in embodied AI where a high-level reasoning module — typically a [[Large Language Model]] (LLM) — decomposes long-horizon tasks into a sequence of manageable sub-tasks, each of which is executed by a lower-level controller. This approach bridges symbolic planning and continuous control, enabling robots to perform complex, multi-step operations in dynamic environments.

## Description

A framework where high-level planning (via LLMs) is combined with lower-level control actions for sequential task execution. The LLM generates a structured plan (e.g., "find the kitchen", "approach the cabinet", "grasp the cup") while a low-level policy handles motion and manipulation. This separation of concerns improves both generality and robustness.

## Capabilities

- Decomposing long-horizon navigation tasks into sub-tasks using LLMs.
- Leveraging natural language instructions to guide sequential decision-making.
- Integrating symbolic reasoning with reactive control for open-vocabulary tasks.

## Relationships

- **Part of** [[Open-Vocabulary Object Navigation]] ⚠️ ⚠️ — hierarchical planning is a core component that enables agents to navigate and interact with objects specified by free-form language.
- **Used by** [[LOVON]] — the LOVON system implements this planning hierarchy to perform language-guided navigation in unknown environments.
- **Depends on** [[LLM]] ⚠️ ⚠️ — the high-level planner relies on an LLM for task decomposition and world knowledge.
- **Implements** the **means-ends analysis** pattern common to classical AI planning, but adapted for continuous robotics.

## Example Workflow

1. Receive an open-vocabulary instruction: “Bring me the red mug from the kitchen.”
2. LLM decomposes this into: [navigate to kitchen, locate red mug, approach, grasp, return].
3. Each sub-task is executed by a specialized controller (e.g., [[ROS2]] navigation stack for movement, grasp network for manipulation).
4. Feedback loops refine the plan if sub-tasks fail.

## Related Pages

- [[LOVON]]
- [[Open-Vocabulary Object Navigation]] ⚠️ ⚠️
- [[LLM]] ⚠️ ⚠️
- [[Task Planning in Robotics]] ⚠️
- [[ROS2 Navigation Stack]] ⚠️