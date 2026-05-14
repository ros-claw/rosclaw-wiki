---
id: privileged_information_guidance
title: Privileged Information Guidance
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-29T21:33:08'
last_reinforced: '2026-04-29T21:33:08'
supersedes: []
sources:
- papers/2505.08712.pdf
source_type: arxiv_paper
---

# Privileged Information Guidance

**Privileged Information Guidance** is a training technique that leverages privileged information – data available only in simulation (or other high-information environments) – to provide supervision during policy learning. This guidance takes the form of **critic values for contrastive trajectory samples**, enabling the policy to internalize spatial understanding and safety distinctions without needing access to that privileged information at test time.

## Overview

In embodied-agent training, the environment often holds ground-truth states, future outcomes, or risk metrics that are inaccessible during real-world deployment. Privileged Information Guidance exploits this gap by conditioning the learning process on that privileged data, then training the policy to predict the resulting critic values. This creates a robust understanding of which trajectories are safe, which are dangerous, and how the spatial layout constrains behavior.

## Mechanism

The policy learns to predict critic values for **contrastive trajectory samples** – pairs or sets of trajectories that differ in success, safety, or other desired properties. During training, a critic (trained with privileged information from simulation) assigns scalar values to these trajectories. The policy is then supervised to replicate those values, effectively distilling the privileged knowledge into a deployable inference network.

This approach is closely related to methods like **auxiliary task learning** and **privileged learning** (e.g., learning-by-cheating).

## Capabilities

- **Fosters accurate spatial understanding** – The policy learns to interpret spatial relationships from the contrastive signals, even though it never directly observes the privileged layout information.
- **Enables distinction between safe and dangerous behaviors** – By training on contrastive examples with known risk outcomes (available in simulation), the policy learns to avoid dangerous configurations without needing explicit safety labels at runtime.

## Relationships

- **Used by** Navigation Diffusion Policy ⚠️ (NavDP) – Privileged Information Guidance provides the critic supervision that allows NavDP to generate navigation trajectories that are both spatially coherent and risk-aware.
- **Depends on** – Simulation ⚠️ environment capable of providing task-relevant privileged information (e.g., collision outcomes, goal distances, task completion metrics).

> *See also:* Contrastive Learning ⚠️, Critic Networks ⚠️, Sim-to-Real Transfer