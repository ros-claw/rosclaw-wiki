---
id: sysnav_multi_level_systematic_cooperation_enables_real_world_cross_embodiment_ob
type: algorithm
tags:
- vln
- vision-language-navigation
- '2026'
- real-robot
- unitree
confidence: 0.8
created_at: '2026-05-11'
sources:
- https://arxiv.org/pdf/2603.06914
- https://github.com/zwandering/SysNav
- https://cmu-vln.github.io/
---

# SysNav: Multi-Level Systematic Cooperation Enables Real-World, Cross-Embodiment Object Navigation

**Year**: 2026  
**Venue**: arXiv`<br>CMU  
**arXiv**: [2603.06914](https://arxiv.org/pdf/2603.06914)  
**Code**: [https://github.com/zwandering/SysNav](https://github.com/zwandering/SysNav)  
**Website**: [https://cmu-vln.github.io/](https://cmu-vln.github.io/)  

## Overview

[website](https://cmu-vln.github.io/) 
 将整改导航系统解耦为高级语义推理、中级几何规划和低级运动控制；高级语义推理：利用视觉语言模型（Gemini 2.5）实时构建环境的语义拓扑图（YoLov8与SAM2），并通过常识推理决定探索方向；中级几何规划：具体的空间建图与安全路径规划工作，确保机器人在未知的物理环境中能够避开障碍物；低级运动控制：专注于底盘的运动学执行，将规划好的安全轨迹转化为极其精确的底层电机控制指令。论文用 Unitree Go2 and G1做了真机实验

## See Also

- [[vision_and_language_navigation|Vision-Language Navigation]]
- [[object_goal_navigation|Object-Goal Navigation]]
- [[unitree_go2|Unitree Go2]]

