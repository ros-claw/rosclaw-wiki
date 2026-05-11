---
id: one_map_to_find_them_all_real_time_open_vocabulary_mapping_for_zero_shot_multi_o
type: algorithm
tags:
- vln
- vision-language-navigation
- '2025'
- real-robot
confidence: 0.8
created_at: '2026-05-11'
sources:
- https://arxiv.org/pdf/2409.11764?
- https://github.com/KTH-RPL/OneMap
---

# One map to find them all: Real-time open-vocabulary mapping for zero-shot multi-object navigation

**Year**: 2025  
**Venue**: ICRA`<br>KTH Royal Institute of Technology  
**arXiv**: [2409.11764](https://arxiv.org/pdf/2409.11764?)  
**Code**: [https://github.com/KTH-RPL/OneMap](https://github.com/KTH-RPL/OneMap)  

## Overview

OneMap通过构建一个可复用的、实时的、开放词汇（Open-Vocabulary）语义地图；零样本物体导航；图像级的 CLIP 特征+ SED (Simple Encoder-Decoder) 架构，利用卡尔曼滤波将带有方差的特征融合到2D栅格地图上；至于导航与搜索策略：机器人优先前往语义相似度高且未被当前任务搜索过的区域；HM3D 数据集成功率为55.8%；可以在 Jetson Orin AGX 上（Boston Dynamics Spot+Realsense D455 + Livox Lidar）实时运行（2HZ）

## See Also

- [[vision_and_language_navigation|Vision-Language Navigation]]
- [[object_goal_navigation|Object-Goal Navigation]]

