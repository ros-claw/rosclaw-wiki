---
id: nav_r2_dual_relation_reasoning_for_generalizable_open_vocabulary_object_goal_nav
type: algorithm
tags:
- vln
- vision-language-navigation
- '2025'
confidence: 0.8
created_at: '2026-05-11'
sources:
- https://arxiv.org/pdf/2512.02400
- https://github.com/AMAP-EAI/Nav-R2
---

# Nav-R2: Dual-Relation Reasoning for Generalizable Open-Vocabulary Object-Goal Navigation

**Year**: 2025  
**Venue**: arXiv`<br>Tsinghua University  
**arXiv**: [2512.02400](https://arxiv.org/pdf/2512.02400)  
**Code**: [https://github.com/AMAP-EAI/Nav-R2](https://github.com/AMAP-EAI/Nav-R2)  

## Overview

面向开放词汇目标导航（Object-goal navigation），架构为LLM主干（Qwen2.5-VL-7B）+视觉编码器+记忆模块；构建了 Chain-of-Thought（CoT，包含了目标-环境建模与环境-动作规划）数据集（ Qwen2.5-VL-7B 生成标注），仅在模拟数据上进行微调，支持2HZ的实时推理；HM3D-OVON数据集的成功率为44~45%

## See Also

- [[vision_and_language_navigation|Vision-Language Navigation]]
- [[object_goal_navigation|Object-Goal Navigation]]

