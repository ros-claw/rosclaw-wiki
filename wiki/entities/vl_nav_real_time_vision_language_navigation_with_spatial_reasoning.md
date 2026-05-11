---
id: vl_nav_real_time_vision_language_navigation_with_spatial_reasoning
type: algorithm
tags:
- vln
- vision-language-navigation
- '2025'
- real-robot
confidence: 0.65
created_at: '2026-05-11'
sources:
- https://arxiv.org/pdf/2502.00931
---

# VL-Nav: Real-time Vision-Language Navigation with Spatial Reasoning

**Year**: 2025  
**Venue**: arXiv`<br> University at Buffalo  
**arXiv**: [2502.00931](https://arxiv.org/pdf/2502.00931)  

## Overview

集成了空间推理（将视觉语言特征转换为空间分数分布），分数（CVL scores）与每个目标点相结合，再通过curiosity-driven weighting实现选择目标点进行探索（保证所选的目标点不仅是人类指令还是让机器人探索未知区域）,选择目标点后采用传统的planner进行避障导航（Modular learning approaches）；移动小车（Orin NX）上实现30HZ频率（成功率86.3%）

## See Also

- [[vision_and_language_navigation|Vision-Language Navigation]]
- [[object_goal_navigation|Object-Goal Navigation]]

