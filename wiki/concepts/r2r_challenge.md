---
id: r2r_challenge
title: R2R Challenge
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-30T02:47:25'
last_reinforced: '2026-04-30T02:47:25'
supersedes: []
sources:
- papers/2007.08037.pdf
source_type: arxiv_paper
---

# R2R Challenge

## Overview

The **R2R (Room-to-Room) challenge** is a standard benchmark for Vision-Language Navigation. It evaluates an agent's ability to follow natural language instructions to navigate through real-world indoor environments. The benchmark includes multiple evaluation settings to test different aspects of navigation:

- **Single run**: The agent navigates without any prior knowledge of the environment.
- **Pre-exploration**: The agent is allowed to explore the environment before receiving the instruction.
- **Beam search**: The agent considers multiple trajectory candidates and selects the best one.

## Capabilities

- **Benchmark for vision-language navigation** – R2R provides a standardized testbed for comparing VLN models.

## Usage

The R2R Challenge is used by Vision-Language Navigation to evaluate model performance. It serves as a primary benchmark in the field, corresponding to a key evaluation standard for embodied AI agents operating in indoor environments.

## Related Concepts

- Vision-Language Navigation depends_on R2R Challenge
- VLN BERT implements R2R Challenge for training and evaluation