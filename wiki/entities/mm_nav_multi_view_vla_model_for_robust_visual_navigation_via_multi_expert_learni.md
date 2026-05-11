---
id: mm_nav_multi_view_vla_model_for_robust_visual_navigation_via_multi_expert_learni
type: algorithm
tags:
- vln
- vision-language-navigation
- '2025'
- real-robot
- unitree
confidence: 0.65
created_at: '2026-05-11'
sources:
- https://arxiv.org/pdf/2510.03142v1
---

# MM-Nav: Multi-View VLA Model for Robust Visual Navigation via Multi-Expert Learning

**Year**: 2025  
**Venue**: arXiv`<br>Peking University  
**arXiv**: [2510.03142](https://arxiv.org/pdf/2510.03142v1)  

## Overview

训练3个RL专家（到达/Reaching、挤压/Squeezing、躲避/Avoiding）并进行初始VLA（SigLIP+Qwen2-7B）微调，然后部署到仿真环境，再进行在线的教师-学生训练，部署到Unitree GO2（模型运行在RTX5090），4个鱼眼相机，VKA输出的速度由底层控制器执行（平均响应为7HZ），到达的成功率>80%，混合三种情况成功率>47%

## See Also

- [[vision_and_language_navigation|Vision-Language Navigation]]
- [[object_goal_navigation|Object-Goal Navigation]]
- [[unitree_go2|Unitree Go2]]

