---
id: vlnverse_a_benchmark_for_vision_language_navigation_with_versatile_embodied_real
type: entity
tags:
- vln
- vision-language-navigation
- '2025'
- dataset
confidence: 0.8
created_at: '2026-05-11'
sources:
- https://arxiv.org/pdf/2512.19021
- https://github.com/william13077/IAmGoodNavigator
---

# VLNVerse: A Benchmark for Vision-Language Navigation with Versatile, Embodied, Realistic Simulation and Evaluation

**Year**: 2025  
**Venue**: arXiv`<br>Adelaide University  
**arXiv**: [2512.19021](https://arxiv.org/pdf/2512.19021)  
**Code**: [https://github.com/william13077/IAmGoodNavigator](https://github.com/william13077/IAmGoodNavigator)  

## Overview

基于 NVIDIA Isaac Sim 构建，包含 263 个高保真物理场景，并且统一了细粒度 (Fine-grained，一步一指令)、粗粒度 (Coarse-grained，目标导向)、视觉参考 (Visual-Reference，看图找物)、长程 (Long-Horizon，多阶段连续导航) 及对话式 (Dialogue-based，通过交互解决歧义) 五大导航任务；不仅仅是视觉上的高保真，每个场景中的物体均可移动，交互。物体的物理属性，比如质量，摩擦系数，反光系数也都有提供。除此之外，还提供了详细的拓扑和语义标注，以及occupancy map。

## See Also

- [[vision_and_language_navigation|Vision-Language Navigation]]
- [[object_goal_navigation|Object-Goal Navigation]]

