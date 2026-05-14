---
id: advisor
title: Advisor
type: entity
tags: []
confidence: 0.8
created_at: '2026-04-30T03:52:55'
last_reinforced: '2026-04-30T03:52:55'
supersedes: []
sources:
- papers/2503.22942.pdf
source_type: arxiv_paper
---

The **Advisor** is an LLM-based Module ⚠️ ⚠️ that serves as the decision-making core within the Adaptive Replanning framework. It continuously monitors system state and task progress to determine whether a replanning action is warranted, providing a **flexible replanning trigger** rather than relying on fixed thresholds or timeouts.

### Capabilities
- **Flexible replanning trigger**: Evaluates contextual cues (e.g., unexpected sensor readings, partial failures, or changes in the environment) and issues a replanning request when necessary. This adaptability reduces unnecessary replanning overhead while maintaining robustness.

### Relationships
- **`part_of`**: Adaptive Replanning – the Advisor is a core component that decides when the planner should regenerate a new plan.
- **`depends_on`**: LLM-based Module ⚠️ ⚠️ – the Advisor leverages large language model reasoning for contextual decision-making.
- **`uses`**: ROS2 Action Servers ⚠️ – typically interfaces with action servers to signal replanning events to the execution layer.

### Usage Notes
In a typical ROS2 pipeline, the Advisor subscribes to high-level status topics (e.g., `~plan_progress`, `~environment_changes`) and publishes a `~replan_request` trigger when its LLM evaluation flags a divergence from expected behavior. This design enables human-like flexible replanning while remaining compatible with standard ROS2 nodes.

### Source
- ArXiv paper 2503.22942 (Adaptive Replanning for Long-Horizon Tasks)