---
id: embodied_interaction
title: Embodied Interaction
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-30T03:20:06'
last_reinforced: '2026-04-30T03:20:06'
supersedes: []
sources:
- papers/2407.06886.pdf
source_type: arxiv_paper
---

# Embodied Interaction

**Embodied Interaction** is a core concept within Embodied AI that focuses on the study and design of how intelligent agents interact with physical environments, humans, and other agents through their bodies. It emphasizes the role of the physical form—including sensors, actuators, and morphology—in shaping perception, cognition, and behavior.

## Definition

Embodied interaction goes beyond purely symbolic or text-based communication. It encompasses physical actions such as reaching, grasping, walking, manipulating objects, gesturing, and maintaining social proxemics. The agent’s body mediates all exchanges with the world, making embodiment a necessary condition for meaningful interaction.

## Role in Embodied AI

- `part_of:: Embodied AI` — Embodied Interaction is one of the foundational pillars of the broader field of Embodied AI, which studies how intelligence arises from the coupling of perception, action, and learning within physical embodiments.

- **Research Target**: Embodied Interaction is identified as **one of four main research targets** within Embodied AI. The other three targets typically include Embodied Perception, Embodied Learning, and Embodied Reasoning, though the exact taxonomy may vary across sources.

## Scope

The study of embodied interaction covers:
- **Human-robot interaction** (HRI) at the physical level, including haptic feedback and collaborative manipulation.
- **Multi-agent interaction**, where robots coordinate through shared physical space.
- **Environment interaction**, such as manipulating objects, navigating cluttered spaces, or using tools.
- **Social embodiment**, where robots infer and produce non-verbal cues (posture, gaze, touch) to facilitate communication.

Embodied Interaction is tightly coupled with ROS ⚠️ (and its successors like ROS 2 ⚠️), since real-time sensorimotor loops require robust middleware for perception, planning, and actuation.

## Relationship to Other Concepts

- `depends_on:: Sensorimotor Control ⚠️` — Effective interaction requires precise, closed-loop control based on sensory feedback.
- `implements:: Tool Use ⚠️` — Many embodied agents are designed to interact with objects that extend their reach or capability.
- `uses:: Force/Torque Sensing ⚠️` — Physical interaction often requires measuring contact forces to prevent damage and provide compliant behavior.

## Sources

- arxiv paper `2407.06886.pdf` (Embodied Interaction as a major research target)
- Standard taxonomy in Embodied AI literature

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Embodied Interaction` --related_to ⚠️--> `Embodied AI`
