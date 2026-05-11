---
id: orionnav_online_planning_for_robot_autonomy_with_context_aware_llm_and_open_voca
type: algorithm
tags:
- vln
- vision-language-navigation
- '2024'
- real-robot
confidence: 0.65
created_at: '2026-05-11'
sources:
- https://arxiv.org/pdf/2410.06239
---

# Orionnav: Online planning for robot autonomy with context-aware llm and open-vocabulary semantic scene graphs

**Year**: 2024  
**Venue**: arXiv`<br>New York University  
**arXiv**: [2410.06239](https://arxiv.org/pdf/2410.06239)  

## Overview

在线自主导航框架（四足机器人、Jetson AGX Orin和Jetson Orin Nano、传感器：RGBD、LiDAR、IMU、腿部里程计）：LiDAR-SLAM（2D栅格地图为主）+开放词汇表3D语义映射方法（基于RGBD的语义物体地图，FC-CLIP）+基于LLM（GPT-4-Turbo,云端API调用）的规划器+ROS2导航stack+[mexplore ROS2](https://github.com/robo-friends/m-explore-ros2)探索；96次真机实验中成功完成了85次，成功率为88.5%

## See Also

- [[vision_and_language_navigation|Vision-Language Navigation]]
- [[object_goal_navigation|Object-Goal Navigation]]

