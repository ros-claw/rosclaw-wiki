---
id: sureal
title: SuReAL
type: algorithm
tags: []
confidence: 0.8
created_at: '2026-04-29T21:18:22'
last_reinforced: '2026-04-29T21:18:22'
supersedes: []
sources:
- papers/1910.09664.pdf
source_type: arxiv_paper
---

# SuReAL (Supervised Reinforcement Asynchronous Learning)

## Overview

Supervised Reinforcement Asynchronous Learning (SuReAL) is a learning framework that combines supervised learning for predicting positions to visit and reinforcement learning for continuous control. It is designed for mapping natural language instructions and first-person observations to continuous control in [[Quadcopter]] ⚠️ flight, using both [[Simulated Environment|simulated]] and [[Real Environment|real environments]] without requiring autonomous flight in the physical environment during training.

## Capabilities

- Estimates the need for environment exploration during execution.
- Predicts the likelihood of visiting environment positions during execution.
- Controls the agent to both explore and visit high‑likelihood positions.

## Relationships

- **Uses**: [[Supervised Learning]] ⚠️ and [[Reinforcement Learning]].
- **Depends on**: [[Simulated Environment]] ⚠️ ⚠️ and [[Real Environment]] ⚠️ ⚠️.

## Parameters

No specific parameters are defined in the source paper.

## Source

- *SuReAL: Supervised Reinforcement Asynchronous Learning for Mapping Natural Language Instructions to Continuous Control* (arXiv:1910.09664).