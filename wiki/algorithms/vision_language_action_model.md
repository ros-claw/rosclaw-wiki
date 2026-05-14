---
id: vision_language_action_model
title: Vision-Language-Action Model
type: algorithm
tags: []
confidence: 0.8
created_at: '2026-04-30T04:04:17'
last_reinforced: '2026-04-30T04:04:17'
supersedes: []
sources:
- papers/2405.14093.pdf
source_type: arxiv_paper
---

# Vision-Language-Action Model

## Overview

A **Vision-Language-Action Model** (VLA) is a category of multimodal model that extends Vision-Language Models ⚠️ ⚠️ (VLMs) to generate motor commands or action sequences for Embodied AI systems. These models take both visual observations and natural language instructions as input and output low-level or high-level actions, enabling language-conditioned robotic tasks.

## Description

VLAs are organized along three distinct lines of research:

1. **Individual components** – models that process perception, language understanding, and action generation as separate modules.
2. **Low-level action prediction policies** – end-to-end models that directly output joint angles, end-effector poses, or torques from visuo-linguistic inputs.
3. **High-level task planners** – models that generate symbolic task plans or skill sequences, which are then executed by lower-level controllers.

This taxonomy covers a broad spectrum of approaches, from modular pipelines to fully integrated architectures.

## Capabilities

- **Language-conditioned robotic tasks**: VLAs can follow natural language commands to perform manipulation, navigation, and mobile manipulation tasks.
- **Generating actions from vision and language inputs**: They map high-level human instructions and real-time camera feeds directly to executable actions, bridging the gap between human communication and robot control.

## Relationships

- **Uses**: Large Language Models (LLMs) for language understanding and reasoning, Vision-Language Models ⚠️ ⚠️ (VLMs) for joint visual-linguistic representation learning.
- **Depends on**: Embodied AI as the overarching research area that provides the physical grounding and task definitions needed to train and evaluate action generation.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Vision-Language-Action Model` --based_on ⚠️--> `Embodied AI`
