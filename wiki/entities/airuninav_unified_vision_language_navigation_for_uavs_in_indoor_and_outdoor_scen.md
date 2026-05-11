---
id: airuninav_unified_vision_language_navigation_for_uavs_in_indoor_and_outdoor_scen
type: algorithm
tags:
- vln
- vision-language-navigation
- '2026'
- real-robot
confidence: 0.65
created_at: '2026-05-11'
sources:
- https://www.techrxiv.org/doi/full/10.36227/techrxiv.176834454.46554529
---

# AirUniNav: Unified Vision-Language Navigation for UAVs in Indoor and Outdoor Scenes

**Year**: 2026  
**Venue**: arXiv`<br>Beihang University  

## Overview

无人机具身导航；模型架构分为：文本处理模块（将指令文本分解为离散的Token）、视频编码（将视觉观测分为历史和当前）、connector、LLM（Qwen 2 7B）；动作集同样是离散化，室内（停止、前进、左转、右转）+室外（室内的+上升、下降、左移、右移）；仿真环境下VLN-CE R2R的SR为47.2%，RxR为43.7%，室外的为6.8`13.9%;真机实验中，A100部署框架，通过API接收任务指令，室内导航步长为0.5米，室外导航步长为2米，旋转动作调整15°

## See Also

- [[vision_and_language_navigation|Vision-Language Navigation]]
- [[object_goal_navigation|Object-Goal Navigation]]

