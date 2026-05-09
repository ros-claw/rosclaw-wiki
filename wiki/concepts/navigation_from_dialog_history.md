---
id: navigation_from_dialog_history
title: Navigation from Dialog History
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-29T21:23:41'
last_reinforced: '2026-04-29T21:23:41'
supersedes: []
sources:
- papers/1907.04957.pdf
source_type: arxiv_paper
---

# Navigation from Dialog History

**Navigation from Dialog History** is a concept in embodied AI where an agent is tasked with inferring goal-oriented navigation actions solely from a natural language dialog history between two humans cooperating to find a target object, and then executing those actions in an **unexplored photorealistic home environment**. This task sits at the intersection of visual navigation, dialog understanding, and cooperative reasoning.

## Task

Given a target object and a dialog history between humans cooperating to find that object, the agent must infer navigation actions towards the goal in unexplored environments. The agent cannot rely on prior exploration of the environment and must ground its decisions in the spatial references and instructions embedded in the dialog.

## Parameters

- **Input**: target object + dialog history
- **Output**: sequence of navigation actions (e.g., turn, move forward, stop)
- **Environment**: unexplored photorealistic homes (from the *Matterport3D* dataset)
- **Evaluation**: success rate, path length, and task completion metrics

## Capabilities

- Inference of goal-oriented navigation from dialog context
- Generalization to unseen environments without prior map or exploration
- Reasoning over spatial language and human cooperative strategies in dialogs

## Dependencies

- Depends on the [[CVDN dataset]] ⚠️ ⚠️ (Cooperative Vision-and-Dialog Navigation), which provides pairs of dialogs, target objects, and human trajectories in homes.
- Implements a core component of [[Cooperative Vision-and-Dialog Navigation]] ⚠️ ⚠️, where a human helper and a robotic navigator collaborate via dialog.

## Relationships

- **part_of**: [[Cooperative Vision-and-Dialog Navigation]] ⚠️ ⚠️
- **depends_on**: [[CVDN dataset]] ⚠️ ⚠️
- **implements**: goal-oriented navigation from natural language instructions
- **contrasts_with**: navigation from explicit metric path descriptions (e.g., "walk 5 meters forward") – this approach requires inference from ambiguous conversational cues.

## References

- *"CVDN: Cooperative Vision-and-Dialog Navigation"* – arxiv:1907.04957 (original paper introducing the task)