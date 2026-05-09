---
id: hierarchical_cross_modal_hcm_agent
title: Hierarchical Cross-Modal (HCM) Agent
type: algorithm
tags: []
confidence: 0.8
created_at: '2026-04-30T02:24:17'
last_reinforced: '2026-04-30T02:24:17'
supersedes: []
sources:
- papers/2104.10674.pdf
source_type: arxiv_paper
---

# Hierarchical Cross-Modal (HCM) Agent

The **Hierarchical Cross-Modal (HCM) Agent** is an algorithm for [[Vision-and-Language Navigation (VLN)]] ⚠️ ⚠️ that decomposes the navigation task into specialized high- and low-level policies. It uses layered decision making and modularized training to handle continuous 3D environments with obstacles and longer trajectories.

## Overview

The HCM agent employs a **hierarchical high- and low-level policy architecture**. High-level policies reason over subgoals using visual and linguistic inputs, while low-level policies execute continuous motor commands to reach those subgoals. Training is **modularized**, decoupling **reasoning and imitation** to improve sample efficiency and generalization. The agent operates in a **continuous action space**, enabling smooth motion in complex 3D scenes.

## Capabilities

- Outperforms existing baselines in Robo-VLN key metrics.

## Parameters

| Parameter       | Value                                      |
|-----------------|--------------------------------------------|
| Architecture    | Hierarchical high- and low-level policies  |
| Training        | Modularized training, decoupled reasoning and imitation |
| Action space    | Continuous                                 |

## Relationships

- **uses**: [[Visual sensory inputs]] ⚠️, [[Natural language instructions]] ⚠️, [[Continuous action spaces]] ⚠️
- **depends_on**: [[Vision-and-Language Navigation (VLN)]] ⚠️ ⚠️
- **part_of**: None

## Sources

- *Hierarchical Cross-Modal Agent for Continuous Vision-and-Language Navigation* (arXiv:2104.10674)