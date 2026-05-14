---
id: online_visual_language_mapper
title: Online visual-language mapper
type: algorithm
tags: []
confidence: 0.85
created_at: '2026-04-29T21:08:27'
last_reinforced: '2026-04-30'
supersedes: []
sources:
- papers/2310.10822.pdf
source_type: arxiv_paper
---

# Online Visual-Language Mapper

## Overview

An **online visual-language mapper** is an algorithmic framework that continuously constructs a real-time spatial-semantic map by fusing visual observations from a robot’s sensors with language-aligned semantic interpretations. It enables a robot to maintain both spatial and semantic understanding of previously unseen environments, updating the map incrementally as the robot moves.

## Description

The mapper continuously constructs a map that fuses visual features and language embeddings, enabling the robot to localize and plan based on semantic concepts. It operates online and in real-time, processing incoming sensor streams without requiring offline pre‑computation.

## Parameters

- **Type**: Spatial-semantic map (online, real-time)
- **Input**: RGB-D images, odometry
- **Output**: Real-time visual-language map (Real-time visual-language map)
- **Builds**: Real-time visual-language map

## Capabilities

- Maintain spatial and semantic understanding of unseen environments.
- Update the map online as the robot moves.
- Builds spatial and semantic map of unseen environment.
- Maintains visual-language feature associations.

## Relationships

- **Part of** → Vision and Language Navigation in the Real World via Online Visual Language Mapping ⚠️
- **Uses** → Foundation models for language-aligned feature extraction.
- **Depends on** → Visual input from robot sensors ⚠️ (e.g., RGB cameras, depth sensors, specifically RGB-D camera ⚠️).
- **Used by** → Language indexing-based localizer for downstream navigation queries.

## Online Mapping

The mapper continuously constructs a visual-language map that fuses visual observations with semantic information, providing a persistent representation for navigation. This process runs in real-time, allowing the robot to adapt its understanding of the environment without offline pre‑computation.

*Source: arxiv paper `papers/2310.10822.pdf`*