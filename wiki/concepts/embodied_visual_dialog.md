---
id: embodied_visual_dialog
title: Embodied Visual Dialog
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-30T02:59:16'
last_reinforced: '2026-04-30T02:59:16'
supersedes: []
sources:
- papers/2011.08277.pdf
source_type: arxiv_paper
---

# Embodied Visual Dialog

**Embodied Visual Dialog** is a task within embodied AI that focuses on modeling the **Observer** agent. The Observer must navigate an environment while answering natural language questions posed by a **Locator** — a human or simulated partner who cannot directly perceive the observer’s surroundings.

## Definition

In Embodied Visual Dialog, the goal is to enable a robot (or embodied agent) to maintain a conversational interaction with a remote human who is trying to locate an object or understand the environment. The Observer must simultaneously:

- Move through a 3D space using visual perception.
- Understand and respond to free-form queries about what it sees.
- Track the dialogue history to resolve ambiguous references.

This task goes beyond standard visual dialog (which is often static) by requiring **embodied, temporally extended reasoning** — the answers depend on where the agent has been and what it has observed over time.

## Task

The core of the task is **modeling the Observer** — the agent that must:

1. Perceive its environment via an onboard camera.
2. Plan and execute navigation actions.
3. Produce natural language answers to questions from the Locator.

The task is formally defined as part of the **Where Are You? Dataset** (WAY dataset), which provides:

- 3D indoor scenes.
- Human-written dialog trajectories.
- Ground truth annotations for object locations and agent positions.

## Capabilities

An Embodied Visual Dialog system must be able to:

- **Generate responses to questions while navigating** — the agent does not pause the dialog while moving; it answers immediately based on current visual input and memory.
- Maintain a consistent world model across time.
- Resolve spatial language such as “to your left”, “behind that chair”, or “the blue vase you saw earlier”.

## Relationships

- **Part of** tasks defined in the Where Are You? Dataset.  
- **Depends on** the Where Are You? Dataset for training and evaluation.  
- **Uses** concepts from Visual Dialog ⚠️, Embodied Navigation, and Sim-to-Real Transfer.  
- **Related to** Visual Question Answering ⚠️ (VQA) but extended to an interactive, sequential setting with physical action.

## Background

The work is introduced in the paper *“Where Are You? Localization from Embodied Dialog”* (arXiv:2011.08277). It highlights the challenge of **active perception through conversation** — where the robot’s movements and a human’s questions are coupled.

For further reading, see also: Embodied AI, Way Dataset ⚠️, Observer-Locator Framework ⚠️.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Embodied Visual Dialog` --related_to ⚠️--> `Embodied AI`
