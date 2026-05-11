---
id: navforesee_a_unified_vision_language_world_model_for_hierarchical_planning_and_d
type: algorithm
tags:
- vln
- vision-language-navigation
- '2025'
confidence: 0.65
created_at: '2026-05-11'
sources:
- https://arxiv.org/pdf/2512.01550
---

# NavForesee: A Unified Vision-Language World Model for Hierarchical Planning and Dual-Horizon Navigation Prediction

**Year**: 2025  
**Venue**: arXiv`<br>Amap  
**arXiv**: [2512.01550](https://arxiv.org/pdf/2512.01550)  

## Overview

首次将视觉语言模型（VLM）规划(将复杂指令分解为子指令)与世界模型预测（预测环境特征来指导导航）整合到统一框架下，用于导航任务；VLM规划训练（Gemini 2.5Pro构建层级语言规划/Hierarchical Language planning数据集）+世界模型训练（Dual-Horizon Predictive Foresight，通过decoder预测未来几步的环境特征，如DINOV2，SAM，帮助智能体增强局部感知、避障）。模型架构基于 Qwen2.5-VL-3B-Instruct 构建（同时实现规划和预测），包含文本编码器、图像编码器和位置编码器；在 R2R-CE 和 RxR-CE 数据集上SR>66%

## See Also

- [[vision_and_language_navigation|Vision-Language Navigation]]
- [[object_goal_navigation|Object-Goal Navigation]]

