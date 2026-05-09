---
id: world_models_wms
title: World Models (WMs)
type: algorithm
tags: []
confidence: 0.8
created_at: '2026-04-30T03:09:16'
last_reinforced: '2026-04-30T03:09:16'
supersedes: []
sources:
- papers/2407.06886.pdf
source_type: arxiv_paper
---

# World Models (WMs)

**World Models** are a class of neural-architecture designed to learn an internal representation of an environment, enabling an agent to simulate outcomes of possible actions before executing them. They are a fundamental building block for **[[Embodied Agents]] ⚠️**, providing a compact latent space for **[[Perception]] ⚠️ ⚠️**, **[[Interaction]] ⚠️ ⚠️**, and **[[Reasoning]] ⚠️ ⚠️**.

## Overview

A World Model encapsulates the dynamics, rewards, and affordances of the world into a differentiable model. By predicting future states and rewards from current observations and actions, the agent can plan, explore, and learn without direct interaction. This approach is central to model‑based reinforcement learning, mental simulation, and **[[Sim-to-Real Transfer]]**.

## Capabilities

- **Perception** – Compresses high‑dimensional sensory input (e.g., vision, proprioception) into a latent representation, enabling efficient state estimation.
- **Interaction** – Provides gradient signals for action selection, allowing closed‑loop behaviour in both simulation and physical robots.
- **Reasoning** – Supports long‑horizon planning through **[[Temporal Abstraction]] ⚠️** and counterfactual reasoning (e.g., “what would happen if I moved left?”).

## Role in Embodied Intelligence

As noted in the original source (arXiv 2407.06886), World Models represent a *promising architecture for embodied agents*. They unify **[[Perception]] ⚠️ ⚠️**, **[[Interaction]] ⚠️ ⚠️**, and **[[Reasoning]] ⚠️ ⚠️** under a single predictive framework, enabling agents to learn efficiently from limited real‑world experience. Their applications span **[[Manipulation]] ⚠️**, **[[Locomotion]] ⚠️**, and **[[Visual Navigation]]**.

## References

- *World Models for Embodied Agents* (arXiv:2407.06886, 2024).