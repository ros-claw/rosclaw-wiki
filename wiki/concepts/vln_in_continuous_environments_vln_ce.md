---
id: vln_in_continuous_environments_vln_ce
title: VLN in Continuous Environments (VLN-CE)
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-30T01:22:11'
last_reinforced: '2026-04-30T01:22:11'
supersedes: []
sources:
- papers/2304.03047.pdf
source_type: arxiv_paper
---

# VLN in Continuous Environments (VLN-CE)

**VLN-CE** (Vision-Language Navigation in Continuous Environments) is a specialized formulation of [[Vision-Language Navigation (VLN)]] in which agents navigate in continuous, non-discrete spaces rather than the discretized graph nodes or waypoints typical of earlier VLN benchmarks. This setting better reflects real-world deployment, where the agent must move freely and react to obstacles, dynamics, and fine-grained spatial details.

## Description

VLN-CE is a more practical setting where the agent navigates in continuous environments rather than discretized graphs. By removing the assumption of pre-defined navigable waypoints, VLN-CE requires the agent to generate continuous trajectories, handle local collision avoidance, and leverage low-level motor commands—closely aligning the task with embodied AI and robotics.

## Capabilities

- **Navigation in continuous, non-discrete environments** – Agents operate in photorealistic 3D scans (e.g., [[Habitat]], [[Matterport3D]] ⚠️ ⚠️) without a precomputed navigation graph, using raw RGB-D observations and language instructions to decide where and how to move.

## Relationships

- **subtype_of**: [[Vision-Language Navigation (VLN)]] – VLN-CE inherits the core task of following natural language instructions to reach a goal, but adopts a more realistic continuous action space and sensorimotor loop.

## Background and Motivation

Traditional VLN benchmarks discretize environments into nodes (e.g., pre-defined viewpoints) and restrict the agent to teleporting between them. VLN-CE (first systematically studied in the paper *VLN-CE: Vision-Language Navigation in Continuous Environments*, arXiv:2304.03047) addresses this gap by proposing a simulator framework and evaluation protocol where the agent executes continuous steps (e.g., forward/backward movement, rotation). This setting exposes challenges such as noisy odometry, partial observability, and the need for real-time local planning.

## Usage in Research

VLN-CE has become a standard testbed for evaluating models that combine language understanding with continuous control. Approaches often rely on **cross-modal encoders**, **policy networks**, and **sim-to-real transfer** techniques. The task is commonly benchmarked on the [[VLN-CE dataset]] ⚠️ (derived from [[Matterport3D]] ⚠️ ⚠️) using metrics such as success rate (SR), oracle success rate (OSR), and navigation error (NE).

## Source

- arXiv:2304.03047 – *VLN-CE: Vision-Language Navigation in Continuous Environments* (the primary paper introducing the setting and baseline models).