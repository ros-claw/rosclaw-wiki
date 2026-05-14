---
id: language_guided_visual_navigation
title: Language-Guided Visual Navigation
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-30T00:48:13'
last_reinforced: '2026-04-30T00:48:13'
supersedes: []
sources:
- papers/2412.05552.pdf
source_type: arxiv_paper
---

# Language-Guided Visual Navigation

**Language-guided visual navigation** is a core task in embodied AI, where an agent moves through a physical or simulated environment by following natural language instructions. The instructions vary in granularity, from high-level goals (e.g., "find the kitchen") to detailed step-by-step directions (e.g., "turn left at the sofa, then go straight until you see a red door"). This capability bridges vision ⚠️ and language understanding ⚠️ with continuous control ⚠️ in real-world spaces.

## Task Structure

- **Task family**: instruction-following navigation
- **Subtasks**:
  - *High-level category-specific search*: The agent must locate a target object or location given a broad command (e.g., "bring me a cup").
  - *Low-level language-guided navigation*: The agent follows precise, sequential instructions (e.g., "go forward, stop at the table").

## Capabilities

- Interpret natural language instructions
- Understand visual surroundings (scene semantics, object recognition, spatial layout)
- Infer action decisions (discrete or continuous commands, e.g., "move 0.5 m forward", "turn 90° left")

## Relationship: Implementation

`Language-Guided Visual Navigation` **is implemented by** State-Adaptive Mixture of Experts (SAME). SAME adaptively selects expert modules based on the current state and instruction, enabling the agent to share general navigation knowledge while exploiting task-specific cues.

## Challenges

- Sharing general knowledge across task variants (e.g., high-level search vs. low-level navigation) while retaining the ability to exploit task-specific cues.
- Dynamically adapting to varying instruction precision and visual context — a command like "go to the kitchen" requires different reasoning than "take the second left after the painting".
- Robustness to ambiguous or incomplete language, noisy perception, and dynamic environments.

## See Also

- Embodied AI
- Visual Language Action (VLA) Models ⚠️
- Sim-to-Real Transfer
- ROS2 Navigation Stack ⚠️

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Language-Guided Visual Navigation` --related_to ⚠️ ⚠️ ⚠️--> `embodied AI`
- `Language-Guided Visual Navigation` --related_to ⚠️ ⚠️ ⚠️--> `Embodied AI`
**Pending review:**
- `Language-Guided Visual Navigation` --related_to ⚠️ ⚠️ ⚠️--> `State-Adaptive Mixture of Experts (SAME)` _(wikilink)_
