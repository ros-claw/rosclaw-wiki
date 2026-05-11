---
id: film_nav_efficient_and_generalizable_navigation_via_vlm_fine_tuning
type: algorithm
tags:
- vln
- vision-language-navigation
- '2026'
confidence: 0.65
created_at: '2026-05-11'
sources:
- https://arxiv.org/pdf/2509.16445v1
---

# FiLM-Nav: Efficient and Generalizable Navigation via VLM Fine-tuning

**Year**: 2026  
**Venue**: arXiv`<br>Georgia Institute of Technology  
**arXiv**: [2509.16445](https://arxiv.org/pdf/2509.16445v1)  

## Overview

微调VLM（SigLIP ViT+Mamba LLM/2.8B）作为导航policy；将轨迹历史、语言目标和边界图像格式化为输入序列，VLM 预测最优边界标记；将选择的边界坐标传递给预训练的 PointNav 策略，计算下一步的离散动作；使用 OWLViT v2 检测目标物体，并使用 MobileSAM 分割物体点云；在 HM3D ObjectNav(目标导航)中的SR为61.7%

## See Also

- [[vision_and_language_navigation|Vision-Language Navigation]]
- [[object_goal_navigation|Object-Goal Navigation]]

