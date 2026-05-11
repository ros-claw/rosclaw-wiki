---
id: fsr_vln_fast_and_slow_reasoning_for_vision_language_navigation_with_hierarchical
type: algorithm
tags:
- vln
- vision-language-navigation
- '2025'
- real-robot
- unitree
confidence: 0.8
created_at: '2026-05-11'
sources:
- https://arxiv.org/pdf/2509.13733
- https://github.com/HorizonRobotics/HoloAgent
---

# FSR-VLN: Fast and Slow Reasoning for Vision-Language Navigation with Hierarchical Multi-modal Scene Graph

**Year**: 2025  
**Venue**: arXiv`<br>Horizon Robotics  
**arXiv**: [2509.13733](https://arxiv.org/pdf/2509.13733)  
**Code**: [https://github.com/HorizonRobotics/HoloAgent](https://github.com/HorizonRobotics/HoloAgent)  

## Overview

层次化多模态场景图(HMSG)：多模态地图表征（FAST-LIVO2等：几何+语义+显式拓扑关系）实现粗略的room-level定位到精细的目标视角与物体定位；接下来的快速到慢速导航推理（FSR）基于HMGS，应用VLM实现最终目标的选择；基于选择的目标实现路径规划以及全身控制来到达目标（这部分采用传统方案）；Unitree-G1验证157m导航

## See Also

- [[vision_and_language_navigation|Vision-Language Navigation]]
- [[object_goal_navigation|Object-Goal Navigation]]
- [[unitree_go2|Unitree Go2]]

