---
id: retrospective_curiosity_encouraging_imitation_learning
title: Retrospective Curiosity-Encouraging Imitation Learning
type: algorithm
tags: []
confidence: 0.85
created_at: '2026-04-29T21:25:21'
last_reinforced: '2026-04-30'
supersedes: []
sources:
- papers/1909.01871.pdf
source_type: arxiv_paper
---

# Retrospective Curiosity-Encouraging Imitation Learning

## Overview

**Retrospective Curiosity-Encouraging Imitation Learning** is an [[algorithm]] ⚠️ that combines [[Imitation Learning]] with [[Curiosity-driven learning]] ⚠️ ⚠️ and a retrospective review mechanism. It teaches agents to avoid repeating past mistakes while simultaneously predicting future progress, thereby encouraging curiosity‑driven exploration and improving the effectiveness of help‑seeking behavior. The approach was introduced in the 2019 paper *Retrospective Curiosity-Encouraging Imitation Learning* (arXiv:1909.01871) and is used by a [[Memory-augmented neural agent]] such as the [[HANNA Agent]].

## Description

A novel imitation learning algorithm that incorporates retrospective curiosity. The agent learns from human demonstrations while being encouraged to avoid past failures and to anticipate its future progress, leading to more effective help requests. By reviewing earlier episodes, the agent identifies errors and develops strategies to prevent their recurrence, while curiosity drives exploration toward novel and informative states.

## Parameters

- **Type**: Imitation learning with curiosity and retrospective aspects  
- **Underlying technique**: Imitation learning with curiosity  
- **Architecture**: [[Memory-augmented neural agent]]  
- **Training data**: Expert demonstrations and agent’s own interaction history

## Capabilities

- Teaches the agent to avoid repeating past mistakes  
- Enables the agent to predict its own chances of making future progress  
- Improves the effectiveness of help‑seeking behavior  
- Encourages curiosity‑driven exploration  
- Outperforms baselines on both seen and unseen environments

## Architecture

The algorithm is built on a [[Memory-augmented neural network]] ⚠️ that stores episodic memories of past successes and failures. During training, the agent reviews these memories and uses a curiosity signal (based on prediction error) to guide exploration. The combination of retrospective review and intrinsic motivation allows the agent to request human assistance when it anticipates low future progress.

## Relationships

- **Used by**: [[Memory-augmented neural agent]] (e.g., [[HANNA Agent]])  
- **Depends on**: [[Imitation Learning]], [[Curiosity-driven learning]] ⚠️ ⚠️ (curiosity-based exploration)  
- **Implements**: [[HANNA Agent]]

## Related Algorithms

- [[Behavioral Cloning]] ⚠️  
- [[Generative Adversarial Imitation Learning (GAIL)]] ⚠️  
- [[DQN with Intrinsic Motivation]] ⚠️  
- [[Intrinsic Curiosity Module (ICM)]] ⚠️  

## References

- Paper: *Retrospective Curiosity-Encouraging Imitation Learning*, arXiv:1909.01871 (source: `papers/1909.01871.pdf`)