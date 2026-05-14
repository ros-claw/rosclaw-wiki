---
id: scene_grounding_sub_task
title: Scene Grounding sub-task
type: algorithm
tags: []
confidence: 0.8
created_at: '2026-04-29T21:16:43'
last_reinforced: '2026-04-29T21:16:43'
supersedes: []
sources:
- papers/2103.12944.pdf
source_type: arxiv_paper
---

# Scene Grounding Sub-task

**Type:** Algorithm (Cross-modal alignment pretraining)  
**Source:** [arxiv paper 2103.12944](papers/2103.12944.pdf)

## Overview

The **Scene Grounding sub-task** is a critical component of the Two-stage Training Pipeline for REVERIE. It belongs to the first stage of training, where the agent learns to align scene-level visual features with natural language instructions. The core objective is to teach the agent **when and where to stop** during navigation — i.e., to ground a language description to a specific location within an environment.

This sub-task is a form of cross-modal alignment pretraining, designed to bridge the gap between raw visual observations and linguistic goals. By solving this task, the agent builds the ability to recognize that certain visual configurations correspond to a linguistically described "goal location," which is essential for success in the full REVERIE task.

## Parameters

- **Type:** Cross-modal alignment pretraining
- **Objective:** Learn where to stop during navigation

## Capabilities

- Determines the correct stopping location for an agent in a navigation episode, based on visual input and language instruction.

## How It Works

During the first stage of the two-stage pipeline (before fine-tuning on the full REVERIE task), the agent is presented with pairs of a visual environment ⚠️ ⚠️ and a language instruction ⚠️ ⚠️. It must learn to identify the specific scene or viewpoint in which the instruction is "fulfilled." This is akin to phrase grounding, but extended to 3D environments and temporal sequences of observations.

The scene grounding sub-task uses:

- A visual encoder to process RGB-D or panoramic images
- A language encoder to parse the instruction
- A cross-modal attention mechanism to align scene features with linguistic cues
- A binary or categorical output indicating whether the current viewpoint is the goal

Training is typically supervised using either human-annotated goal positions or automatically generated positive/negative examples from the REVERIE dataset.

## Relationship to Other Components

- **Part of:** Two-stage Training Pipeline for REVERIE
- **Uses:** visual environment ⚠️ ⚠️, language instruction ⚠️ ⚠️
- **Related to:** Goal Prediction ⚠️ (the second stage focuses on predicting the exact target object/position)
- **Depends on:** Cross-modal Alignment Pretraining ⚠️ techniques (e.g., ViLBERT, VL-BERT, or similar)
- **Contributes to:** Embodied Navigation agents that follow natural language commands

## Why It Matters

Without effective scene grounding, an agent might stop early at an irrelevant location or fail to recognize when it has reached the correct place. This sub-task is thus foundational for the REVERIE task and for any embodied AI system that must interpret "stop here" from language.

## References

- Source paper: *R2R and REVERIE* (arxiv 2103.12944) — Section on two-stage training pipeline
- Two-stage Training Pipeline for REVERIE

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Scene Grounding sub-task` --extends ⚠️--> `Two-stage Training Pipeline for REVERIE`
