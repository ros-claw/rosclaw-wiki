---
id: seqwalker_sequential_horizon_vision_and_language_navigation_with_hierarchical_pl
type: algorithm
tags:
- vln
- vision-language-navigation
- '2026'
confidence: 0.8
created_at: '2026-05-11'
sources:
- https://arxiv.org/pdf/2601.04699v1
- https://github.com/SeqWalker/SeqWalker-code
---

# SeqWalker: Sequential-Horizon Vision-and-Language Navigation with Hierarchical Planning

**Year**: 2026  
**Venue**: arXiv`<br>North University of China  
**arXiv**: [2601.04699](https://arxiv.org/pdf/2601.04699v1)  
**Code**: [https://github.com/SeqWalker/SeqWalker-code](https://github.com/SeqWalker/SeqWalker-code)  

## Overview

提出序列视野视觉语言导航（SH-VLN）任务，要求智能体遵循长序列语言指令完成多任务连续导航；SeqWalker模型：高层感知规划（指令分割模块（ISM）：CLIP+Qwen-0.5b，对长指令进行局部分割、分步理解）、导航场景映射（并显式存储场景语义地图和栅格地图）、底层运动规划（通过探索-验证（EaV）策略，生成具体导航动作并修正轨迹误差）；扩展 IVLN 的 IR2R-CE 数据集，构建 SH IR2R-CE 数据集：序列轨迹拼接+LLaVA-OneVision 充实长指令

## See Also

- [[vision_and_language_navigation|Vision-Language Navigation]]
- [[object_goal_navigation|Object-Goal Navigation]]

