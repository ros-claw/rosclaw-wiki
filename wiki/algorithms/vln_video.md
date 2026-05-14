---
id: vln_video
title: VLN-Video
type: algorithm
tags: []
confidence: 0.85
created_at: '2026-04-29T21:00:45'
last_reinforced: '2026-04-30'
supersedes: []
sources:
- papers/2402.03561.pdf
source_type: arxiv_paper
---

## Overview

**VLN-Video** is a deep learning algorithm for Vision-and-Language Navigation (VLN) ⚠️ that leverages large-scale, diverse outdoor driving videos — augmented with automatically generated instructions and actions — to improve navigation performance. It addresses the data scarcity problem in outdoor VLN by synthesizing high-quality training examples from raw video footage.

The algorithm combines classical template infilling with deep learning methods: it generates natural language instructions from video frames using a template-based approach, and extracts ground-truth navigation actions via an image rotation similarity predictor. The resulting augmented dataset is used to pretrain a Cross-Modal Transformer ⚠️ ⚠️ with three proxy tasks: Masked Language Modeling ⚠️ ⚠️, Instruction and Trajectory Matching ⚠️ ⚠️, and Next Action Prediction ⚠️ ⚠️. This pretrain-then-finetune paradigm achieves state-of-the-art results on the Touchdown dataset, with a +2.1% improvement in task completion rate.

## Methodology

### Input & Output
- **Input**: Raw driving videos (e.g., from U.S. city street footage)
- **Output**: Navigation actions (e.g., turn left, go straight, stop)

### Instruction Generation: Template Infilling
1. Parse each video frame sequence into a trajectory of turns and straight segments.
2. Fill a language template (e.g., "Go straight until the traffic light, then turn left.") with landmarks and actions detected from the visual context.
3. This provides **automatically generated instructions** paired with each video trajectory.

### Action Extraction: Image Rotation Similarity Predictor
1. For each video frame pair, compute rotation similarity between consecutive frames.
2. Classify the action (turn angle, stop, straight) based on the dominant rotation direction.
3. Produces **automated action labels** for each video timestep.

### Proxy Tasks for Pretraining
The model is pretrained on the augmented driving video dataset using three complementary proxy tasks, then fine-tuned on the Touchdown dataset:

| Task | Description |
|------|-------------|
| **Masked Language Modeling (MLM)** | Mask a token in the instruction and predict it from visual context. This teaches the model to learn language representations grounded in visual observations. |
| **Instruction and Trajectory Matching (ITM)** | Predict whether an instruction–trajectory pair is aligned. This forces the model to align instructions with the visual sequence. |
| **Next Action Prediction (NAP)** | Given visual history and instruction, predict the next navigation action. This instills temporally-aware decision-making. |

Together, these proxy tasks enable the model to learn rich cross-modal representations without requiring human-annotated data for every video.

## Key Results

- **Dataset**: Trained and evaluated on the Touchdown dataset (outdoor navigation).
- **Performance**: Achieves a **+2.1% improvement in task completion rate** over the previous state-of-the-art on Touchdown.
- **Core insight**: Augmenting with driving videos from diverse U.S. cities significantly expands the training distribution, improving generalization to unseen environments.

## Relationships

- **Uses ⚠️**: driving videos, Touchdown dataset, Masked Language Modeling ⚠️ ⚠️, Instruction and Trajectory Matching ⚠️ ⚠️, Next Action Prediction ⚠️ ⚠️, Cross-Modal Transformer ⚠️ ⚠️, image rotation similarity predictor, template infilling
- **Depends on ⚠️**: classical approaches ⚠️ (template infilling), deep learning techniques ⚠️ (cross-modal fusion and action prediction)
- **Technique ⚠️**: Combines classical template infilling ⚠️ with deep learning action prediction ⚠️
- **Addresses ⚠️**: data scarcity in outdoor VLN ⚠️, generalization gap in VLN ⚠️

## References

- *VLN-Video: Improving Outdoor Vision-and-Language Navigation Using Large-Scale Driving Videos* (arXiv:2402.03561)

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `VLN-Video` --implements ⚠️--> `Touchdown dataset`