---
id: social_intelligence
title: Social Intelligence
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-30T03:48:13'
last_reinforced: '2026-04-30T03:48:13'
supersedes: []
sources:
- papers/2508.15354.pdf
source_type: arxiv_paper
---

# Social Intelligence

**Social Intelligence** is a Concept ⚠️ that enables an Embodied Agent to navigate and interact within human environments by understanding and responding to social cues, norms, and dynamics. It bridges the gap between purely geometric navigation and socially aware behavior, allowing robots to move efficiently while respecting human comfort, intent, and social conventions.

## Definition

Social Intelligence in the context of Embodied Navigation refers to the set of perceptual, reasoning, and planning capabilities that allow a robot to infer the social state of others (e.g., attention, intent, personal space) and adapt its actions accordingly. Unlike classical navigation that treats humans as moving obstacles, social intelligence models humans as social entities with which the robot must coordinate.

## Capabilities

- **Socially-aware navigation**: Plans paths that avoid violating personal space, respect queues, and yield right-of-way.
- **Intent prediction**: Anticipates human motion and goals using gaze, body orientation, and past trajectory.
- **Nonverbal communication**: Uses motion cues (e.g., speed, orientation, path curvature) to signal intent to humans.
- **Policy learning from human demonstrations**: Can be acquired through Imitation Learning or Reinforcement Learning from human-human or human-robot interaction data.

## Relationships

- **Part of**: Embodied Navigation — Social intelligence is a component that augments traditional navigation with social reasoning.
- **Depends on**: Human Pose Estimation ⚠️, Gaze Detection ⚠️, Social Norms Modeling ⚠️
- **Implements**: Social Navigation ⚠️ — a subfield of navigation focused on human-aware path planning.
- **Related to**: Proxemics ⚠️, Theory of Mind ⚠️, Interactive Navigation

## Sources

This page is based on content from `data/raw/papers/2508.15354.pdf`.