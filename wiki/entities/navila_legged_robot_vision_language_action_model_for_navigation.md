---
id: navila_legged_robot_vision_language_action_model_for_navigation
type: algorithm
tags:
- vln
- vision-language-navigation
- '2025'
confidence: 0.8
created_at: '2026-05-11'
sources:
- https://arxiv.org/pdf/2412.04453
- https://github.com/AnjieCheng/NaVILA
---

# NaVILA: Legged Robot Vision-Language-Action Model for Navigation

**Year**: 2025  
**Venue**: RSS`<br>UC San Diego  
**arXiv**: [2412.04453](https://arxiv.org/pdf/2412.04453)  
**Code**: [https://github.com/AnjieCheng/NaVILA](https://github.com/AnjieCheng/NaVILA)  

## Overview

采用双系统架构：VLM(视觉语言模型)+locomotion policy (RL实现的基于视觉的运动控制)。VLM将语言指令和图像作为输入，输出mid-level action/动作语言指令，再由locomotion policy翻译为机器人low-level action/运控电机指令；

## See Also

- [[vision_and_language_navigation|Vision-Language Navigation]]
- [[object_goal_navigation|Object-Goal Navigation]]

