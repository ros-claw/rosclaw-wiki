---
id: abot_n0_technical_report_on_the_vla_foundation_model_for_versatile_embodied_navi
type: algorithm
tags:
- vln
- vision-language-navigation
- '2026'
- real-robot
confidence: 0.8
created_at: '2026-05-11'
sources:
- https://arxiv.org/pdf/2602.11598
- https://github.com/amap-cvlab/ABot-Navigation
---

# ABot-N0: Technical Report on the VLA Foundation Model for Versatile Embodied Navigation

**Year**: 2026  
**Venue**: arXiv`<br>AMAP, Alibaba Group  
**arXiv**: [2602.11598](https://arxiv.org/pdf/2602.11598)  
**Code**: [https://github.com/amap-cvlab/ABot-Navigation](https://github.com/amap-cvlab/ABot-Navigation)  

## Overview

统一模型实现点目标、物体目标、指令跟随、兴趣点导航、行人跟随；LLM（Qwen3-4B）负责语义推理，flow matching驱动action expert生成轨迹，7802 个 3D 场景（总面积高达10.7平方公里）、1690 万条轨迹与 500 万条推理样本的大规模数据引擎；部署于NVIDIA Jetson Orin NX，2HZ

## See Also

- [[vision_and_language_navigation|Vision-Language Navigation]]
- [[object_goal_navigation|Object-Goal Navigation]]

