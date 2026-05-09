---
id: urbannav
title: UrbanNav
type: algorithm
tags: []
confidence: 0.9
created_at: '2026-04-29T20:42:17'
last_reinforced: '2026-04-29'
supersedes: []
sources:
- papers/2512.09607.pdf
- papers/2512.09607.json
source_type: arxiv_paper
---

# UrbanNav

## Overview

UrbanNav is a scalable framework that trains embodied agents to navigate complex urban environments using natural language instructions. It leverages web-scale city walking videos and an annotation pipeline to create over 1,500 hours of navigation data and 3 million instruction–trajectory–landmark triplets.

## Capabilities

- Follow free-form language instructions in diverse urban settings
- Superior spatial reasoning compared to prior methods
- Robustness to noisy or ambiguous instructions
- Generalization to unseen urban environments
- **Contrast with prior work**: Existing methods are typically limited to simulated or off-street environments; UrbanNav is trained on real-world urban walking data, allowing better generalization to the complexity of city streets.

## Key Parameters

| Parameter | Value |
|-----------|-------|
| Training data (hours) | 1,500+ |
| Instruction–trajectory–landmark triplets | 3,000,000 |
| Data source | Web-scale city walking videos |
| Annotation pipeline | Scalable alignment of trajectories with language instructions grounded in real-world landmarks |

## Dependencies & Relationships

- **Uses**: [[Language Instructions]] ⚠️, [[Web-Scale City Walking Videos]] ⚠️, [[Annotation Pipeline]] ⚠️
- **Depends on**: Web-scale city walking videos and the scalable annotation pipeline
- **Implements**: [[Language-Guided Navigation Policy]] ⚠️ ⚠️ ⚠️
- **Contradicts**: Existing navigation methods that restrict training to [[Simulated Environments]] ⚠️ or off-street datasets

## Methodology

UrbanNav first collects a large corpus of city walking videos from the web. A scalable annotation pipeline extracts trajectory and landmark information from each video and pairs them with synthetic natural-language instructions grounded in real-world landmarks. The resulting 3 million instruction–trajectory–landmark triplets (spanning over 1,500 hours) are used to train a [[Language-Guided Navigation Policy]] ⚠️ ⚠️ ⚠️ via imitation or reinforcement learning. The framework learns robust navigation policies that understand directional phrases, landmark references, and environmental context, remaining effective even when instructions contain noise or incomplete references.

## Results

UrbanNav outperforms existing methods in three key areas:

- **Spatial reasoning**: The agent accurately interprets spatial language and landmark references.
- **Noise robustness**: Performance degrades gracefully under ambiguous or partial instructions.
- **Generalization**: The policy transfers to unseen urban layouts and instruction styles without retraining.

## See Also

- [[Embodied AI]]
- [[Visual Navigation]]
- [[Sim-to-Real Transfer]] (for generalization aspects)
- [[Spatial Reasoning]] ⚠️
- [[Language-Guided Navigation]]
- [[Language-Guided Navigation Policy]] ⚠️ ⚠️ ⚠️
- [[Trajectory Alignment with Language Instructions]] ⚠️

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `UrbanNav` --[[based_on]] ⚠️ ⚠️--> `Embodied AI`
- `UrbanNav` --[[based_on]] ⚠️ ⚠️--> `Language-Guided Navigation`
- `UrbanNav` --[[implements]] ⚠️--> `Language-Guided Navigation Policy`