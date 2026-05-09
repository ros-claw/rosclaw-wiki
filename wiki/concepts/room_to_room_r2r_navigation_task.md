---
id: room_to_room_r2r_navigation_task
title: Room-to-Room (R2R) Navigation Task
type: concept
tags: []
confidence: 0.95
created_at: '2026-04-30T04:43:12'
last_reinforced: '2026-04-30T04:43:12'
supersedes: []
sources:
- code/peteanderson80_Matterport3DSimulator/README.md
source_type: official_manual
---

## Room-to-Room (R2R) Navigation Task

The **Room-to-Room (R2R) Navigation Task** is a benchmark in [[Vision-and-Language Navigation]] (VLN) that tests an autonomous agent's ability to navigate to a goal location in a previously unseen building while following a natural language instruction. It provides a standardized environment, dataset, and evaluation metrics for research in embodied AI and instruction following.

### Description

In the R2R task, an agent is placed at a start viewpoint within a 3D environment (the [[Matterport3D Dataset]]) and must navigate to a specified goal location using only RGB-D observations from the [[Matterport3D Simulator]] and a natural language instruction. The instruction describes the route in human terms (e.g., "walk past the sofa, turn left at the fireplace, and stop in front of the window"). The agent must understand the instruction, perceive its surroundings, and execute a sequence of actions (move forward, turn left/right, etc.) to reach the goal. The environment is previously unseen by the agent during training, requiring generalization to novel layouts.

### Parameters

| Parameter | Value |
|-----------|-------|
| **Task type** | Vision-and-language navigation |
| **Goal** | Navigate to a goal location in a previously unseen building following a natural language instruction |
| **Evaluation** | Via [[EvalAI]] ⚠️ ⚠️ test server and public leaderboard |

### Capabilities

- Tests autonomous agent ability to understand and follow natural language instructions in real, complex environments.
- Provides a large-scale training dataset (human-annotated instructions for routes in the Matterport3D houses) and standardized evaluation metrics (e.g., success rate, path length, navigation error).
- Enables fair comparison across different VLN models through the EvalAI leaderboard.

### Relationships

- **Implemented by**: [[Matterport3D Simulator]] – the R2R task is the primary benchmark delivered with this simulator.
- **Depends on**: [[Matterport3D Dataset]] – the task uses Matterport3D scans for environment geometry and appearance, along with human-written navigation instructions.
- **Used in**: [[Vision-and-Language Navigation]] research; many models (e.g., [[Seq2Seq VLN]] ⚠️, [[Speaker-Follower]], [[VLN-BERT]]) are evaluated on R2R.

### Evaluation

Agent performance is measured via the EvalAI platform. Metrics include:
- **Success Rate** (SR): whether the agent stops within a threshold distance of the goal.
- **Oracle Success Rate** (OSR): success if the goal is ever visible during the trajectory.
- **Path Length** (PL): total distance traveled by the agent.
- **Success weighted by Path Length** (SPL): combines success with efficiency.

The leaderboard tracks submissions and provides per-split results (train/val/test unseen).

### See Also

- [[Matterport3D Dataset]]
- [[Matterport3D Simulator]]
- [[Vision-and-Language Navigation]]
- [[EvalAI]] ⚠️ ⚠️

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Room-to-Room (R2R) Navigation Task` --[[related_to]] ⚠️--> `Vision-and-Language Navigation`
- `Room-to-Room (R2R) Navigation Task` --[[applies_to]] ⚠️--> `Matterport3D Simulator`
