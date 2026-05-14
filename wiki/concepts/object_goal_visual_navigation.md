---
id: object_goal_visual_navigation
title: Object goal visual navigation
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-30T04:31:25'
last_reinforced: '2026-04-30T04:31:25'
supersedes: []
sources:
- papers/2206.07423.pdf
source_type: arxiv_paper
---

# Object Goal Visual Navigation

Object goal visual navigation is a task within embodied AI and visual navigation where a robot must locate and navigate to a specified target object based solely on visual observations. The target object is typically drawn from a predefined set of object classes, making this a class-conditional navigation problem.

## Description

In object goal visual navigation, a robot is placed in an unseen environment and receives a visual goal (e.g., an image or class label of the object). The robot must explore its surroundings and move toward the target object, relying on visual perception to detect and identify the object. This task evaluates a system's ability to integrate visual recognition, spatial reasoning, and goal-driven exploration.

## Capabilities

- Guide a robot to find a target object based on visual observation — the core capability required to perform the task.

## Relationships

- **subtype_of**: visual navigation — shares the fundamental requirement of moving toward a visually specified target.
- **subtype_of**: embodied AI — the task is an instance of an embodied agent interacting with a physical (or simulated) environment to achieve a goal.

## Related Concepts

- Semantic navigation ⚠️ expands the goal from a single object to a class of objects or a state.
- Visual SLAM ⚠️ often underpins the mapping and localization needed for navigation.
- Object detection and semantic segmentation ⚠️ are perceptual components commonly used to identify the target object.

## Source

- Papers/2206.07423.pdf — introduces the task and provides benchmarks.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Object goal visual navigation` --related_to ⚠️--> `embodied AI`
