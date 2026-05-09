---
id: active_visual_information_gathering_avig
title: Active Visual Information Gathering (AVIG)
type: algorithm
tags: []
confidence: 0.85
created_at: '2026-04-29T21:17:34'
last_reinforced: '2026-04-30'
supersedes: []
sources:
- papers/2007.08037.pdf
source_type: arxiv_paper
---

## Active Visual Information Gathering (AVIG)

**Active Visual Information Gathering (AVIG)** is an end-to-end learning framework for exploration policy in [[Vision-Language Navigation (VLN)]]. It addresses the challenge of ambiguous instructions and insufficient observation by enabling the agent to actively explore its surroundings to gather additional information before making navigation decisions. The policy determines three aspects: **when and where** to explore, **what** information to gather, and **how** to update the navigation plan post-exploration. The goal is to mitigate uncertainty and achieve robust navigation through confident decision-making.

### Capabilities
- Mitigate uncertainty arising from ambiguous instructions.
- Mitigate insufficient observation by actively exploring the environment.
- Perform active exploration to gather missing visual information.
- **Improve navigation robustness** through learned exploration.
- **Achieve significant performance gains** on the [[R2R Challenge]] benchmark.
- Make confident navigation decisions after information gathering.

### Methodology

AVIG uses an end-to-end framework that learns an exploration policy. When the agent encounters an ambiguous instruction or incomplete visual input, it decides:
1. **When** to initiate exploration (i.e., stop moving and gather more views).
2. **Where** to explore (e.g., which directions or viewpoints to sample).
3. **What** information to gather (e.g., specific objects, landmarks, or layout details).
4. **How** to adjust the navigation path post-exploration based on newly acquired evidence.

The policy is trained end-to-end, jointly optimizing exploration and navigation, without requiring separate hand-coded exploration heuristics.

### Parameters

- **Exploration policy**: Learned end-to-end to decide when/where to explore, what to gather, and how to adjust navigation decisions.

### Experimental Results

AVIG was evaluated on the [[R2R Challenge]] across three settings:
- **Single run** navigation.
- **Pre-exploration** (where the agent gathers information before starting the main path).
- **Beam search** (multiple candidate trajectories).

In all settings, AVIG outperformed strong baselines, demonstrating the effectiveness of learned exploration for resolving ambiguity and improving success rates.

### Relationships
- ⚙️ **uses**: [[Vision-Language Navigation (VLN)]], photo-realistic environments, [[R2R Challenge]]
- 🧩 **depends_on**: [[Exploration Policy]], [[Vision-Language Navigation (VLN)]] (foundational), ambiguous instructions, insufficient observation