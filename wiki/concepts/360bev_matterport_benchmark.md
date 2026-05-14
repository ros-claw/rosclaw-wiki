---
id: 360bev_matterport_benchmark
title: 360BEV-Matterport benchmark
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-29T21:52:09'
last_reinforced: '2026-04-29T21:52:09'
supersedes: []
sources:
- papers/2503.09010.pdf
source_type: arxiv_paper
---

# 360BEV-Matterport Benchmark

The **360BEV-Matterport benchmark** is a standardized evaluation framework for assessing 360° Bird’s-Eye View (BEV) perception from panoramic imagery and LiDAR data. It provides a controlled environment derived from the Matterport3D dataset to measure how well perception systems reconstruct 3D occupancy, object detection, or semantic segmentation from omnidirectional sensors.

## Overview

Benchmarks like 360BEV-Matterport are critical for embodied AI research because they enable reproducible comparisons between methods that process 360° inputs. The benchmark defines specific evaluation protocols, metrics, and data splits, making it a reference point for HumanoidPano and other work targeting spherical perception.

## Usage

-   **Used by**: HumanoidPano – The HumanoidPano framework relies on this benchmark to validate its panoramic 360° perception and BEV prediction pipeline. ((uses)) 360BEV-Matterport benchmark

## Capabilities

-   Provides a standardized testbed for 360° BEV perception from panoramic and LiDAR data.
-   Facilitates fair comparison across algorithms processing omnidirectional visual and geometric inputs.
-   Grounded in the Matterport3D real-world indoor dataset, ensuring ecological validity for mobile robotic tasks.

## See Also

-   Matterport3D ⚠️ – The underlying dataset (concept)
-   360° BEV Perception ⚠️ – The broader research area (concept)
-   HumanoidPano – Entity using this benchmark
-   Embodied AI – Related concept

## Sources

-   arxiv paper 2503.09010: "HumanoidPano: Humanoid Perception System for 360° BEV Perception" – Introduces the benchmark and evaluates on it.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `360BEV-Matterport benchmark` --related_to ⚠️ ⚠️--> `Embodied AI`
**Pending review:**
- `360BEV-Matterport benchmark` --related_to ⚠️ ⚠️--> `HumanoidPano` _(wikilink)_
