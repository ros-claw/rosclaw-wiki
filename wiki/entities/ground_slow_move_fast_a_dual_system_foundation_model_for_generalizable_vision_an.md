---
id: ground_slow_move_fast_a_dual_system_foundation_model_for_generalizable_vision_an
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
- https://arxiv.org/pdf/2512.08186
- https://github.com/InternRobotics/InternNav
---

# Ground Slow, Move Fast: A Dual-System Foundation Model for Generalizable Vision-and-Language Navigation

**Year**: 2025  
**Venue**: arXiv`<br>Shanghai AI Laboratory  
**arXiv**: [2512.08186](https://arxiv.org/pdf/2512.08186)  
**Code**: [https://github.com/InternRobotics/InternNav](https://github.com/InternRobotics/InternNav)  

## Overview

（DualVLN）VLN 领域首个双系统基础模型；System2：基于Qwen-VL-2.5(7B)的全局规划器，以约 2 Hz 的频率运行，负责理解指令、观察环境，并预测像素级目标点（此外，System2还可以自主调整视角）；System1：轻量级Diffusion Transformer，30HZ运行，接收System2的像素目标及隐含的语义特征，结合当前高频RGB图像，生成平滑、连续、避障的轨迹；真机实验：轮式（Turtlebot4）、四足（Unitree Go2）、人形（Unitree G1），均仅搭载RealSense D455 单目 RGB 相机(成功率：R2R 64.3%，RxR 61.4%；）

## See Also

- [[vision_and_language_navigation|Vision-Language Navigation]]
- [[object_goal_navigation|Object-Goal Navigation]]
- [[unitree_go2|Unitree Go2]]

