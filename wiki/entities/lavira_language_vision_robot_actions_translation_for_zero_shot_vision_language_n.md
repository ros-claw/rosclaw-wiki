---
id: lavira_language_vision_robot_actions_translation_for_zero_shot_vision_language_n
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
- https://arxiv.org/pdf/2510.19655
---

# LaViRA: Language-Vision-Robot Actions Translation for Zero-Shot Vision Language Navigation in Continuous Environments

**Year**: 2025  
**Venue**: arXiv`<br>Nanjing University  
**arXiv**: [2510.19655](https://arxiv.org/pdf/2510.19655)  

## Overview

分层导航框架：大模型决策（Gemini-2.5-Pro/GPT-4o，接收自然语言指令、历史轨迹和当前全景观察。充当“大脑”，输出宏观的方向性指令及进度的语言评估）+小模型定位/感知（Qwen2.5-VL-32B，识别与指令最相关的物体/区域，并输出其边界框）+规划控制（将视觉动作输出的 2D 目标投影到 3D 世界坐标系中，生成局部地图上的导航点，并通过路径规划驱动机器人移动）；VLN-CE上成功率>35%；真机测试：Unitree Go1 四足机器人和Agilex Cobot Magic 轮式机器人

## See Also

- [[vision_and_language_navigation|Vision-Language Navigation]]
- [[object_goal_navigation|Object-Goal Navigation]]
- [[unitree_go2|Unitree Go2]]

