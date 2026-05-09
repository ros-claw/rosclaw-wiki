---
id: aerial_vision_and_dialog_navigation_avdn
title: Aerial Vision-and-Dialog Navigation (AVDN)
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-29T21:09:07'
last_reinforced: '2026-04-29T21:09:07'
supersedes: []
sources:
- papers/2205.12219.pdf
source_type: arxiv_paper
---

# Aerial Vision-and-Dialog Navigation (AVDN)

**AVDN** defines a task where a drone is navigated through natural language conversation between a **commander** and a **follower**. The commander issues instructions or answers queries, while the follower (the drone agent) interprets the language in the context of its visual observations to move towards a goal. This paradigm reduces dependency on physical controllers and supports interactive clarification via dialog, enabling more intuitive human–drone interaction.

## Key Facts

| Attribute | Value |
|-----------|-------|
| **Task** | Navigating a drone via natural language conversation between a commander and a follower |
| **Dataset size** | Over 3000 recorded navigation trajectories |
| **Data collection** | Human-human dialogs with asynchronous communication |
| **Simulator** | Continuous photorealistic drone simulator |

## Relationships

- **Depends on:** [[Aerial Navigation]] ⚠️, [[Vision-and-Language Navigation]], [[Dialog Systems]] ⚠️
- **Supersedes:** Standard drone control with joystick/remote

## How It Works

In AVDN, a human commander and a human follower (role-playing the drone) engage in a dialogue to complete a navigation task. The follower has access to first-person visual observations from a continuous photorealistic simulator and can ask clarifying questions (e.g., “Do you mean the red building?”). The commander responds with more specific directions. This asynchronous communication loop allows the system to handle ambiguity and incomplete instructions, mirroring real-world collaborative navigation.

## Significance

AVDN bridges the gap between low-level drone control and high-level human communication. By leveraging dialog, it enables non-expert users to guide drones without training on joystick operation. The dataset of over 3000 trajectories provides a rich resource for training and evaluating models that combine language understanding, visual reasoning, and motion planning. This paradigm is a step toward embodied agents that can follow complex, interactive instructions in dynamic environments.

## References

- Paper: *Aerial Vision-and-Dialog Navigation* (arXiv:2205.12219)
- Data and simulator details available from the associated project page.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Aerial Vision-and-Dialog Navigation (AVDN)` --[[related_to]] ⚠️--> `Vision-and-Language Navigation`
