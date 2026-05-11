---
id: vlingnav_embodied_navigation_with_adaptive_reasoning_and_visual_assisted_linguis
type: algorithm
tags:
- vln
- vision-language-navigation
- '2026'
- real-robot
- unitree
confidence: 0.65
created_at: '2026-05-11'
sources:
- https://arxiv.org/pdf/2601.08665
---

# VLingNav: Embodied Navigation with Adaptive Reasoning and Visual-Assisted Linguistic Memory

**Year**: 2026  
**Venue**: arXiv`<br>ByteDance Seed  
**arXiv**: [2601.08665](https://arxiv.org/pdf/2601.08665)  

## Overview

通过AdaCoT自适应生成语言化思维链（实现显式推理）+VLingMem实现基于关键视觉特征的记忆存储（for长程任务，语言），基于语言驱动的认知再通过VLA（LLaMA-7B+ViT-L，+online RL）实现具身导航；此外，构建了Nav-AdaCoT-2.9M具身导航数据集（带有推理过程，采用基于Qwen 2.5 VL-72B）；128个A100 GPU训练，目标导航SR为58~83%，真机部署为Unitree Go2+RTX 4090 GPU，通信延迟约100ms，推理速度约2.5 FPS

## See Also

- [[vision_and_language_navigation|Vision-Language Navigation]]
- [[object_goal_navigation|Object-Goal Navigation]]
- [[unitree_go2|Unitree Go2]]

