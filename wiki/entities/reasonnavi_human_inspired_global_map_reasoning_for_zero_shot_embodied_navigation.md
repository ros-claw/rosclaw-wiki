---
id: reasonnavi_human_inspired_global_map_reasoning_for_zero_shot_embodied_navigation
type: algorithm
tags:
- vln
- vision-language-navigation
- '2026'
confidence: 0.65
created_at: '2026-05-11'
sources:
- https://arxiv.org/pdf/2602.15864
---

# ReasonNavi: Human-Inspired Global Map Reasoning for Zero-Shot Embodied Navigation

**Year**: 2026  
**Venue**: arXiv`<br>HKUST  
**arXiv**: [2602.15864](https://arxiv.org/pdf/2602.15864)  

## Overview

“全局语义推理”+“局部精准执行”:先通过MLLM分析全局俯视图，锁定目标大致位置(选出目标房间——>房间再锁定具体的位置)，再用确定性规划器精准抵达（基于RGB-D观测+A*全局规划+VFH局部避障），到达目标后，采用预训练目标检测器和 MobileSAM 分割模型确认目标存在，再微调位置完成导航；用两个不同 MLLM（如 Seed-1.6-Thinking、Gemini-2.5-Pro）分别生成候选目标，再由第三个 MLLM 作为判别器；

## See Also

- [[vision_and_language_navigation|Vision-Language Navigation]]
- [[object_goal_navigation|Object-Goal Navigation]]

