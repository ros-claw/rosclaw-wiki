---
id: panonav_mapless_zero_shot_object_navigation_with_panoramic_scene_parsing_and_dyn
type: algorithm
tags:
- vln
- vision-language-navigation
- '2025'
confidence: 0.65
created_at: '2026-05-11'
sources:
- https://arxiv.org/pdf/2511.06840v1
---

# PanoNav: Mapless Zero-Shot Object Navigation with Panoramic Scene Parsing and Dynamic Memory

**Year**: 2025  
**Venue**: arXiv`<br>HKUST-GZ  
**arXiv**: [2511.06840](https://arxiv.org/pdf/2511.06840v1)  

## Overview

Zero-shot目标导航，无需 prebuilt maps；全景（6个方向）RGB输入MLLM（Qwen2.5-VL），此外，结合当前的局部和全局信息以及历史记忆信息（存储在动态有界的记忆队列）利用LLM（DeepSeek-V3）做导航决策（决策结果包括导航方向和是否找到目标的标志），在HM3D数据集上SR约为43.5%

## See Also

- [[vision_and_language_navigation|Vision-Language Navigation]]
- [[object_goal_navigation|Object-Goal Navigation]]

