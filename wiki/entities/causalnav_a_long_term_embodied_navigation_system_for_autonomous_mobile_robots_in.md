---
id: causalnav_a_long_term_embodied_navigation_system_for_autonomous_mobile_robots_in
type: algorithm
tags:
- vln
- vision-language-navigation
- '2026'
- real-robot
confidence: 0.65
created_at: '2026-05-11'
sources:
- https://arxiv.org/pdf/2601.01872
---

# CAUSALNAV: A Long-term Embodied Navigation System for Autonomous Mobile Robots in Dynamic Outdoor Scenarios

**Year**: 2026  
**Venue**: RAL`<br>Tsinghua University  
**arXiv**: [2601.01872](https://arxiv.org/pdf/2601.01872)  

## Overview

首个基于场景图的语义导航；感知部分为开发词汇感知模型（ YOLOWorld检测2D bounding box以及进行分割，ByteTrack进行多目标跟踪，通过LiDAR对目标进行定位）+LiDAR定位（FAST-LIO2）；利用LLM（边端，作者验证了四种）构建粗粒度建筑物地图和细粒度目标，形成可检索的知识库（Embodied Graph，这部分参考自[OpenGraph](https://arxiv.org/pdf/2403.09412)）；规划模块结合离线地图（sense graph）与实时感知数据（基于LiDAR的动态避障）；仿真下，系统运行在 Intel i9-14900K CPU 和 RTX 3090 GPU 上，关键模块实时运行，包括开放词汇对象跟踪（30Hz）、时空走廊过滤（20Hz）、局部动态建图与规划（10Hz）以及 Embodied Graph 更新（1Hz）；实测时系统运行为 Intel Core i9-13900H CPU 和 NVIDIA GeForce RTX 4070 GPU 的轮式移动机器人

## See Also

- [[vision_and_language_navigation|Vision-Language Navigation]]
- [[object_goal_navigation|Object-Goal Navigation]]

