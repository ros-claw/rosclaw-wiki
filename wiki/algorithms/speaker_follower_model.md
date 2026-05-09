---
id: speaker_follower_model
title: Speaker-Follower Model
type: algorithm
tags: []
confidence: 0.85
created_at: '2026-04-29T21:18:58'
last_reinforced: '2026-04-30'
supersedes: []
sources:
- papers/1806.02724.pdf
source_type: arxiv_paper
---

---

## Overview

The **Speaker-Follower Model** is an architecture for [[Vision-and-Language Navigation]] (VLN) that incorporates an explicit **speaker** component alongside the standard **follower** (or navigator). It was introduced by Fried et al. (2018, arxiv:1806.02724) to address two core limitations of earlier VLN models: the scarcity of human‑annotated instruction–trajectory pairs, and the lack of pragmatic reasoning about which actions best satisfy a given instruction. The speaker generates synthetic instructions from observed trajectories (data augmentation) and later acts as a pragmatic listener that scores candidate action sequences, enabling the follower to disambiguate instructions.  Both steps are supported by a [[Panoramic Action Space]] that reflects the granularity of human‑generated instructions.

## Components

- **Speaker model** – generates instructions from trajectories.
- **Follower model** – predicts actions from instructions.
- **Pragmatic reasoning** – uses the speaker model to score action sequences against the original instruction.
- **Data augmentation** – synthesizes additional training data from unlabeled trajectories.

## Capabilities

- **Vision-and-language navigation** – The model addresses the full VLN task, interpreting natural‑language instructions to navigate real environments.
- **Instruction following with high‑level decisions** – The follower makes discrete navigation decisions based on perceptual context and linguistic input.
- **Data augmentation for training** – The speaker generates synthetic instruction–trajectory pairs, vastly expanding the training dataset without additional human annotation.
- **Pragmatic reasoning for action selection** – During inference, the speaker evaluates candidate paths to pick the one most consistent with the instruction, improving success rate and path fidelity.
- **Pragmatic reasoning over action sequences** – Uses a Bayesian‑inspired pragmatic listener to re‑rank candidate trajectories.
- **Panoramic action space** – The model operates over a panoramic view of the environment (e.g., 36 evenly spaced camera headings at multiple elevations), matching the granularity typically found in human‑generated navigation instructions.

## How It Works

The Speaker‑Follower Model comprises two jointly trained modules:

1. **Follower** – A neural policy that takes an instruction and visual observations (from a panoramic viewpoint) and produces a distribution over next actions. Standard sequence‑to‑sequence with attention.
2. **Speaker** – A separate sequence‑to‑sequence model that, given a trajectory (a sequence of panoramic images), generates a natural‑language instruction describing that trajectory.

During training, the speaker produces synthetic instruction–trajectory pairs for data augmentation. During inference, the follower outputs a set of candidate trajectories; the speaker then scores each candidate by computing the likelihood of the original instruction given that trajectory, and the best‑scoring path is selected.

## Parameters

No explicit hyperparameters (e.g., learning rate, LSTM hidden size) are defined in the source. The model uses standard hyperparameters for LSTM‑based seq2seq models and a beam search for instruction synthesis. Key architectural components (Speaker, Follower, pragmatic reasoning, data augmentation) are described above.

## Benchmark Performance

The approach more than doubles the success rate over the best existing approach on a standard benchmark (Fried et al., 2018).

## Relationships

- **Uses**:
  - [[Speaker Model]] ⚠️
  - [[Follower Model]] ⚠️
  - [[Panoramic Action Space]]
  - [[Pragmatic Reasoning]]
- **Depends on**:
  - [[Vision-and-Language Navigation]]
  - [[Pragmatic Reasoning]] (specifically the Rational Speech Acts framework)
  - [[Panoramic Action Space]]
  - [[Data Augmentation for VLN]] ⚠️ ⚠️
  - **perceptual context** – visual observations from the environment.
  - **human‑generated instructions** – both for initial training and as the target for pragmatic scoring.
- **Implements**:
  - [[Data Augmentation for VLN]] ⚠️ ⚠️
  - [[Pragmatic Listener]] ⚠️

## Applications

This model served as a foundation for many later VLN systems (e.g., [[Reinforced Cross‑Modal Matching (RCM)]] ⚠️, [[EnvDrop]]) and demonstrated that explicit speaker–follower interaction can substantially improve both success rate and path fidelity in navigation tasks.

## References

- Fried, D., Hu, R., Cirik, V., Rohrbach, A., Andreas, J., Morency, L.P., Berg‑Kirkpatrick, T., Saenko, K., Klein, D., & Darrell, T. (2018). *Speaker‑Follower Models for Vision‑and‑Language Navigation*. arxiv:1806.02724.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Speaker-Follower Model` --[[based_on]] ⚠️--> `Vision-and-Language Navigation`