---
id: janusvln_decoupling_semantics_and_spatiality_with_dual_implicit_memory_for_visio
type: algorithm
tags:
- vln
- vision-language-navigation
- '2026'
confidence: 0.8
created_at: '2026-05-11'
sources:
- https://arxiv.org/pdf/2509.22548
- https://github.com/MIV-XJTU/JanusVLN
---

# JanusVLN: Decoupling Semantics and Spatiality with Dual Implicit Memory for Vision-Language Navigation

**Year**: 2026  
**Venue**: ICLR`<br> Amap Alibaba Group  
**arXiv**: [2509.22548](https://arxiv.org/pdf/2509.22548)  
**Code**: [https://github.com/MIV-XJTU/JanusVLN](https://github.com/MIV-XJTU/JanusVLN)  

## Overview

模拟大脑左右半球的分工，并行处理“是什么”和“在哪里”的问题：2D视觉语义编码器 (语义“左脑”，Qwen2.5-VL) +3D空间几何编码器 (空间“右脑”，VGGT)；通过一个3D视觉基础模型来扩展MLLM,实现从空间几何编码器中获取3D先验知识,进而增强模型的空间理解能力;双隐式记忆(空间几何与视觉语义记忆)的历史键值对则是通过3D空间几何编码器和MLLM的语义视觉编码器来分别提取;通过滑动窗口进行动态及增量式更新

## See Also

- [[vision_and_language_navigation|Vision-Language Navigation]]
- [[object_goal_navigation|Object-Goal Navigation]]

