---
id: navid
title: NaVid
type: algorithm
tags: []
confidence: 0.85
created_at: '2026-04-29T21:05:43'
last_reinforced: '2026-04-30'
supersedes: []
sources:
- papers/2402.15852.pdf
source_type: arxiv_paper
---

## NaVid

### Overview

**NaVid** is a video-based Large Vision Language Model ⚠️ (VLM) for Vision-and-language navigation (VLN) that directly outputs next-step actions from an on-the-fly video stream captured by a monocular RGB camera ⚠️ ⚠️. It eliminates the need for maps, odometers, or depth sensors, relying solely on visual temporal context — mimicking human navigation behavior. The architecture is a **Video-based Large Vision Language Model (VLM)** designed specifically for embodied navigation tasks.

### Capabilities

- State-of-the-art performance in both simulated and real-world Vision-and-language navigation
- Cross-dataset generalization
- Sim-to-real transfer without additional fine-tuning
- Action planning from video history
- Instruction following using spatio-temporal contexts encoded from historical observations
- Operates entirely without maps, odometers, or depth inputs

### Key Innovation

NaVid replicates human navigation by using **only visual temporal context**, thereby reducing the Sim2Real gap that typically arises from map or depth inputs. By avoiding odometry ⚠️ and depth estimation ⚠️, the model achieves robust zero-shot transfer from simulation to real environments. The reliance on a pure video stream allows NaVid to mimic human-like decision making without needing any explicit geometric or metric representation of the environment.

### Training

NaVid was trained on a large-scale dataset comprising:

- **510k navigation samples** from continuous environments, including action-planning trajectories and instruction-reasoning pairs.
- **763k large-scale web data** samples for general visual-language alignment.

This training leverages large-scale VLM training ⚠️ ⚠️ and continuous environment data collection ⚠️ ⚠️. The combination of domain-specific navigation data and broad web data enables both task-specific competence and robust generalization.

### Parameters

| Parameter | Value |
|-----------|-------|
| Architecture | Video-based Large Vision Language Model (VLM) |
| Input modality | On-the-fly video stream from monocular RGB camera ⚠️ ⚠️ |
| Output | Next-step action |
| Odometry required | No |
| Depth input required | No |
| Map input required | No |
| Training data size | 510k navigation samples + 763k web data samples |

### Relationships

- **Uses**: Video-based VLM ⚠️, monocular RGB camera ⚠️, Vision-and-Language Navigation, Embodied AI
- **Depends on**: large-scale VLM training ⚠️ ⚠️, continuous environment data collection ⚠️ ⚠️
- **Part of**: Vision-and-language navigation
- **Supersedes**: map-based navigation ⚠️, depth-based navigation ⚠️
- **Implements**: Sim-to-real transfer via video-only input, Video-based navigation ⚠️

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `NaVid` --based_on ⚠️--> `Vision-and-language navigation`