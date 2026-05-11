---
id: speaker_follower_models_for_vision_and_language_navigation
type: algorithm
tags:
- vln
- vision-language-navigation
- '2018'
confidence: 0.8
created_at: '2026-05-11'
sources:
- https://arxiv.org/pdf/1806.02724
- https://github.com/ronghanghu/speaker_follower
---

# Speaker-follower models for vision-and-language navigation

**Year**: 2018  
**Venue**: NIPS`<br> University of California  
**arXiv**: [1806.02724](https://arxiv.org/pdf/1806.02724)  
**Code**: [https://github.com/ronghanghu/speaker_follower](https://github.com/ronghanghu/speaker_follower)  

## Overview

将VLN任务视为轨迹搜索问题:指令解析模块(follower将指令映射到动作空间)+指令生成模块(speaker将动作序列映射回指令),两者均为seq2seq架构；speaker model可以通过真值导航路线与指令进行训练；在follower测试的时候，follower会生成给定的指令的潜在路线。而speaker对这些路线进行排名，选择能够更好的解析指令的一条（类似GAN网络的思路）

## See Also

- [[vision_and_language_navigation|Vision-Language Navigation]]
- [[object_goal_navigation|Object-Goal Navigation]]

