---
id: vla_an_an_efficient_and_onboard_vision_language_action_framework_for_aerial_navi
type: algorithm
tags:
- vln
- vision-language-navigation
- '2026'
- real-robot
confidence: 0.65
created_at: '2026-05-11'
sources:
- https://arxiv.org/pdf/2512.15258
---

# VLA-AN: An Efficient and Onboard Vision-Language-Action Framework for Aerial Navigation in Complex Environments

**Year**: 2026  
**Venue**: arXiv`<br>Zhejiang University  
**arXiv**: [2512.15258](https://arxiv.org/pdf/2512.15258)  

## Overview

1. 基于3D-GS的高保真数据构建(100K+ 轨迹和 1M+ 多模态样本的混合数据集);2.渐进式三阶段训练策略(海量VQA数据训练学会看图说话/空间推理---导航训练学习输出3D航点和偏航角---强化学习保证长序列任务的决策一致性和鲁棒性)；3. 非生成式动作模块（为了保证安全不直接输出电机控制信号，而是输出局部3D航点）+轻量级的action module（结合深度信息保证安全）+轻量化模型（Flash-Attention、算子融合、KV-Cache 预加载以及 CUDA Graph 调度）。7B模型（ViT+LLM），在Jetson Orin NX（ 100+TOPS）上可实现2～3Hz的控制频率（7B模型：0.11s/token， 2B模型：0.032s/token），单任务成功率高达98%且有实机飞行测试

## See Also

- [[vision_and_language_navigation|Vision-Language Navigation]]
- [[object_goal_navigation|Object-Goal Navigation]]

