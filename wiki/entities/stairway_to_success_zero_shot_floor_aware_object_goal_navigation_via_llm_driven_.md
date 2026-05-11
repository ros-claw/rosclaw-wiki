---
id: stairway_to_success_zero_shot_floor_aware_object_goal_navigation_via_llm_driven_
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
- https://arxiv.org/pdf/2505.23019
- https://github.com/Zeying-Gong/ascent
---

# Stairway to Success: Zero-Shot Floor-Aware Object-Goal Navigation via LLM-Driven Coarse-to-Fine Exploration

**Year**: 2026  
**Venue**: RAL`<br>HKUST-GZ  
**arXiv**: [2505.23019](https://arxiv.org/pdf/2505.23019)  
**Code**: [https://github.com/Zeying-Gong/ascent](https://github.com/Zeying-Gong/ascent)  

## Overview

跨楼层物体目标导航；多楼层抽象（每层楼维护独立的鸟瞰图表示）、粗到精分层推理：VLM对前沿点进行语义相似度排序，必要时才调用LLM进行深度推理（基于楼层先验概率决定是否切换楼层、基于区域先验概率选择最相关的探索目标）；在HM3D上SR为65.4%，MP3D为44.5%；Unitree Go2 上真机验证，核心算法在笔记本RTX2060，LLM在RTX3090服务器

## See Also

- [[vision_and_language_navigation|Vision-Language Navigation]]
- [[object_goal_navigation|Object-Goal Navigation]]
- [[unitree_go2|Unitree Go2]]

