---
id: mm_nav
title: MM-Nav
type: algorithm
tags: []
confidence: 0.85
created_at: '2026-04-29T20:51:29'
last_reinforced: '2026-04-30'
supersedes: []
sources:
- papers/2510.03142.pdf
source_type: arxiv_paper
---

## MM-Nav

**MM-Nav** is a multi-view vision-language-action (VLA) model for robust visual navigation. It leverages pretrained Large Language Models (LLMs) and pretrained Visual Foundation Models ⚠️ to process multi-view 360° observations and produce navigation actions. The model is trained via a teacher-student paradigm using RL Experts ⚠️ ⚠️ ⚠️ and dynamically balanced online data collection.

### Overview

MM-Nav aims to bridge the gap between high-level semantic understanding and low-level motor control in embodied navigation. By taking as input multi-view 360° images (e.g., from a panoramic camera or multiple cameras), it produces actions such as reaching, squeezing, and avoiding obstacles. The model's training methodology is designed to continuously improve generalization across diverse environments and tasks. The architecture is a **multi-view VLA model** that processes 360-degree observations, using pretrained LLMs and visual foundation models as the backbone for feature extraction and action prediction.

### Capabilities

The model demonstrates four primary capabilities:

- **Reaching** – navigating to target objects or locations.
- **Squeezing** – moving through narrow passages or gaps.
- **Avoiding** – obstacle and collision avoidance in dynamic scenes.
- **Generalization** – zero-shot or few-shot transfer to unseen environments and object types.

### Training

MM-Nav is trained using an iterative teacher-student framework:

- **Base model**: A student network initialized from pretrained LLMs and visual foundation models. These base models provide strong priors for language understanding and visual feature extraction.
- **Teacher experts**: Three RL Experts ⚠️ ⚠️ ⚠️ are trained in custom simulation environments with access to **privileged depth information** (ground-truth depth). These experts provide high-quality demonstration data for the student.
- **Data collection**: Training data is collected online from the RL experts (teacher policies). A **dynamically balanced training ratio** is applied: the proportion of data from each capability (reaching, squeezing, avoiding) is adjusted based on the student's per-capability performance. For example, if the student's reaching accuracy drops, more reaching examples are added to the next training batch.
- **Training procedure**: The student is trained on this online mixture, then evaluated; the teacher may be refined, and the process repeats. This ensures continuous improvement and adaptation.

The dependence on **privileged depth information** is a key aspect of MM-Nav: the RL teachers rely on it to acquire robust behaviors, while the student learns to imitate them using only visual observations, enabling deployment without depth sensors.

### Architecture

MM-Nav adopts a **multi-view VLA architecture** that processes 360° observations. The input consists of multiple camera views (e.g., from a panoramic camera or an array of sensors), which are simultaneously fed into the pretrained vision backbone. The visual features are combined with language embeddings from the LLM and passed through a lightweight action head to produce motor commands (e.g., linear and angular velocities). This design allows the model to reason about the entire surroundings rather than a single forward-facing view, improving spatial awareness and robustness in cluttered environments.

### Relationships

- **Depends on**: Pretrained Large Language Models ⚠️, Pretrained Visual Foundation Models ⚠️, RL Experts ⚠️ ⚠️ ⚠️, and **privileged depth information** (during teacher training).
- **Uses**: reinforcement learning experts, online data collection, dynamic balancing.
- **Implements**: A teacher-student imitation learning pipeline for visual navigation.
- **Related to**: VLA Models ⚠️, Embodied Navigation, Sim-to-Real Transfer (if applicable to the paper's test environments).

### References

- Source paper: arXiv 2510.03142

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `MM-Nav` --implements ⚠️--> `Large Language Models (LLMs)`