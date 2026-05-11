---
id: efficientnav_towards_on_device_object_goal_navigation_with_navigation_map_cachin
type: algorithm
tags:
- vln
- vision-language-navigation
- '2026'
- real-robot
confidence: 0.8
created_at: '2026-05-11'
sources:
- https://arxiv.org/pdf/2510.18546v2
- https://github.com/PKU-SEC-Lab/EfficientNav
---

# EfficientNav: Towards On-Device Object-Goal Navigation with Navigation Map Caching and Retrieval

**Year**: 2026  
**Venue**: arXiv`<br>Peking University  
**arXiv**: [2510.18546](https://arxiv.org/pdf/2510.18546v2)  
**Code**: [https://github.com/PKU-SEC-Lab/EfficientNav](https://github.com/PKU-SEC-Lab/EfficientNav)  

## Overview

目标物体导航，针对KV缓存限制：提出离散记忆缓存机制，将地图信息聚类为不同组并独立计算每组的KV缓存，实现KV缓存的复用；RGB-D +Grounding DINO实现语义理解，用图结构管理语义与空间信息（地图构建），将地图与导航目标指令输入LLM（1B参数量的CLIP对目标与语义信息进行相似度计算，LLM采用LLaVA-7b/AGX Orin。由LLM规划子目标（若目标已在地图中则直接导航，否则继续探索）

## See Also

- [[vision_and_language_navigation|Vision-Language Navigation]]
- [[object_goal_navigation|Object-Goal Navigation]]

