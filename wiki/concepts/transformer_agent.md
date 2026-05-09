---
id: transformer_agent
title: Transformer Agent
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-30T02:01:27'
last_reinforced: '2026-04-30T02:01:27'
supersedes: []
sources:
- papers/2210.03112.pdf
source_type: arxiv_paper
---

## Transformer Agent

The **Transformer Agent** is a neural network-based agent that uses a [[Transformer Architecture]] ⚠️ ⚠️ to process navigation instructions and generate action trajectories. It is trained via [[Imitation Learning]] on synthetic instruction-trajectory pairs, achieving state-of-the-art performance on the [[RxR]] (Room-to-Room) benchmark.

### Architecture

The agent employs a simple transformer model that encodes natural language instructions and previous visual observations into a joint representation, then decodes step-by-step actions. The model does not rely on complex modular components or external knowledge bases—its power comes from scaling the transformer depth and attention mechanisms.

### Capabilities

- Processes synthetic instruction-trajectory pairs generated from existing datasets.
- Achieves state-of-the-art results on the RxR benchmark, demonstrating strong generalization to unseen environments and instruction styles.
- Operates end-to-end, mapping raw instructions and visual input directly to navigational actions.

### Training

- **Trained with**: [[Imitation Learning]]
- Uses behavioral cloning to mimic expert demonstrations derived from synthetic data.
- Training data consists of pairs of natural language instructions and corresponding ground-truth trajectories, generated automatically from simulator-based exploration.

*Key relationships*: [[Transformer Agent]] **uses** → [[Transformer Architecture]] ⚠️ ⚠️, **trained_with** → [[Imitation Learning]], **evaluated_on** → [[RxR]].

*Source*: arxiv paper [2210.03112](https://arxiv.org/abs/2210.03112)