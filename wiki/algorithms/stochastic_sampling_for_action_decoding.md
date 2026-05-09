---
id: stochastic_sampling_for_action_decoding
title: Stochastic Sampling for Action Decoding
type: algorithm
tags: []
confidence: 0.8
created_at: '2026-04-30T02:47:52'
last_reinforced: '2026-04-30T02:47:52'
supersedes: []
sources:
- papers/1909.02244.pdf
source_type: arxiv_paper
---

# Stochastic Sampling for Action Decoding

## Overview

Stochastic Sampling for Action Decoding is a training technique that applies random sampling during the action decoding step, aligning the action distribution seen during training with that encountered at test time. By forcing the agent to sample from its own action distribution rather than always using the expert's actions, the method bridges the distribution shift between training and inference, leading to more robust performance in sequential decision-making tasks.

## Method

During training, the action decoder does not deterministically select the expert action but instead stochastically draws from the model's predicted action distribution. This exposes the agent to its own sampled actions throughout the sequence, enabling it to experience and learn from the consequences of its actual choices. The approach is particularly effective in long-horizon tasks where small errors can compound, as the agent learns to recover from mistakes it might make at test time.

## Capabilities

- **Reduces gap between expert actions and sampled actions**: By sampling during training, the model learns to produce action distributions that are more representative of its own behavior, narrowing the mismatch that often occurs when training with ground-truth expert actions only.
- **Enables the agent to learn to correct its own mistakes during long action sequences**: Because the agent observes the outcome of its sampled actions, it can develop corrective behaviors internally, improving robustness over extended episodes.

## Parameters

- **Sampling strategy**: Stochastic sampling is applied during training to match the test-time distribution. The exact sampling mechanism (e.g., top-κ, temperature scaling) is implementation-dependent, but the core idea is to replace greedy or expert actions with samples from the model's own output distribution.

## Dependencies and Relationships

- **Depends on**: `[[Monte Carlo sampling]] ⚠️` – the stochastic sampling process relies on Monte Carlo methods to draw actions from a probability distribution.
- **Used by**: `[[Vision-and-Language Navigation (VLN)]] ⚠️` – this technique has been successfully applied in VLN tasks to improve generalization and error recovery, as demonstrated in the source paper (arXiv:1909.02244).