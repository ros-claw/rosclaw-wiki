---
id: target_bench_can_world_models_achieve_mapless_path_planning_with_semantic_target
type: algorithm
tags:
- vln
- vision-language-navigation
- '2025'
- real-robot
confidence: 0.8
created_at: '2026-05-11'
sources:
- https://arxiv.org/pdf/2511.17792
- https://github.com/TUM-AVS/target-bench
---

# Target-Bench: Can World Models Achieve Mapless Path Planning with Semantic Targets?

**Year**: 2025  
**Venue**: arXiv`<br>TUM  
**arXiv**: [2511.17792](https://arxiv.org/pdf/2511.17792)  
**Code**: [https://github.com/TUM-AVS/target-bench](https://github.com/TUM-AVS/target-bench)  

## Overview

数据集Target-Bench: 450 个视频（112,500 帧），覆盖 45 种语义目标类别，涉及多种室内外环境。数据集包含SLAM轨迹、人类标注的显式和隐式目标，数据集平台为四足机器人（AGX Orin+Livox+双目）; 首次提出世界模型在无图路径规划中的评价框架（路径评估模块）；世界解码器(world decoder)：时空重建恢复轨迹（VGGT/SpaTracker/ViPE）+尺度恢复（ViPE为视觉惯性SLAM不需要，其他两者需要真值对齐）;评估的世界模型包括了Sora、Veo、Wan三个系列及其变体

## See Also

- [[vision_and_language_navigation|Vision-Language Navigation]]
- [[object_goal_navigation|Object-Goal Navigation]]

