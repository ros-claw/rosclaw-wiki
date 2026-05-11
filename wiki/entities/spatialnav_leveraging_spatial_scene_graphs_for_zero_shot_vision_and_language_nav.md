---
id: spatialnav_leveraging_spatial_scene_graphs_for_zero_shot_vision_and_language_nav
type: algorithm
tags:
- vln
- vision-language-navigation
- '2026'
confidence: 0.65
created_at: '2026-05-11'
sources:
- https://arxiv.org/pdf/2601.06806
---

# SpatialNav: Leveraging Spatial Scene Graphs for Zero-Shot Vision-and-Language Navigation

**Year**: 2026  
**Venue**: arXiv`<br>Adelaide University  
**arXiv**: [2601.06806](https://arxiv.org/pdf/2601.06806)  

## Overview

全局地图可以让VLN更好的理解空间，进而具备长程推理能力，采用全局空间建模（SLAM3D点云+人工分割，环境的层级结构、语义标签与空间关系显式编码），基于当前agent的位置，提取7米半径范围的空间（Z轴确定楼层、XY确定房间）；将360全景图拆成8张图，将画面拼成3*3网格（中间为指南针，明确机器人朝向）；且走之前先查询全局空间地图确认下一步的位置周围有什么物体；仿真环境，R2R（59.3%）、REVERIE（50.4%）和R2R-CE（68.0%）、RxR-CE（39.0）

## See Also

- [[vision_and_language_navigation|Vision-Language Navigation]]
- [[object_goal_navigation|Object-Goal Navigation]]

