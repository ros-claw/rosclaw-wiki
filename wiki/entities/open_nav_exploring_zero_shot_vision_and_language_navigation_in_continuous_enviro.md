---
id: open_nav_exploring_zero_shot_vision_and_language_navigation_in_continuous_enviro
type: algorithm
tags:
- vln
- vision-language-navigation
- '2025'
- real-robot
confidence: 0.8
created_at: '2026-05-11'
sources:
- https://arxiv.org/pdf/2409.18794
- https://github.com/YanyuanQiao/Open-Nav
---

# Open-Nav: Exploring Zero-Shot Vision-and-Language Navigation in Continuous Environment with Open-Source LLMs

**Year**: 2025  
**Venue**: ICRA`<br>The University of Adelaide  
**arXiv**: [2409.18794](https://arxiv.org/pdf/2409.18794)  
**Code**: [https://github.com/YanyuanQiao/Open-Nav](https://github.com/YanyuanQiao/Open-Nav)  

## Overview

利用开源的LLM(本地部署非为call API)实现连续环境下的zero-shot VLN；Waypoint Prediction module负责预测潜在可导航点，场景感知模块包含了RAM（物体识别）和SpatialBot（VLM模型，输入RGB和深度信息，做空间感知，输出为文本描述）；LLM Navigator接收前两者的输入，将任务分解为：指令理解、进度估计、决策；真机实验为轮式机器人（RTX 3080 GPU）；测试了四个不同模型（Llama3.1-70B-instruct, Qwen2-72Binstruct, Gemma2-27B-instruct and Phi3-14B-instruct）成功率<20%

## See Also

- [[vision_and_language_navigation|Vision-Language Navigation]]
- [[object_goal_navigation|Object-Goal Navigation]]

