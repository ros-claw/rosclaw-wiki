---
id: slam_free_visual_navigation_with_hierarchical_vision_language_perception_and_coa
type: algorithm
tags:
- vln
- vision-language-navigation
- '2025'
confidence: 0.65
created_at: '2026-05-11'
sources:
- https://arxiv.org/pdf/2509.20739
---

# SLAM-Free Visual Navigation with Hierarchical Vision-Language Perception and Coarse-to-Fine Semantic Topological Planning

**Year**: 2025  
**Venue**: arXiv`<br> HKUST-GZ  
**arXiv**: [2509.20739](https://arxiv.org/pdf/2509.20739)  

## Overview

不依赖于SLAM的导航框架。通过VLM来实现场景（Qwen）以及物体级别（Grounding DINO）的语义推理,进而构建轻量的拓扑地图（topological representations）。基于LLM（GPT-4）的实现子目标的选择，而基于视觉的局部规划（Viplanner）实现障碍物躲避。 最后再通过强化学习来实现腿式机器人的运动控制。

## See Also

- [[vision_and_language_navigation|Vision-Language Navigation]]
- [[object_goal_navigation|Object-Goal Navigation]]

