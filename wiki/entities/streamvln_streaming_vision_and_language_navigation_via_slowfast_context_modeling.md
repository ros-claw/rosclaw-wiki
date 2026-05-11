---
id: streamvln_streaming_vision_and_language_navigation_via_slowfast_context_modeling
type: algorithm
tags:
- vln
- vision-language-navigation
- '2025'
confidence: 0.8
created_at: '2026-05-11'
sources:
- https://arxiv.org/pdf/2507.05240
- https://github.com/InternRobotics/StreamVLN
---

# Streamvln: Streaming vision-and-language navigation via slowfast context modeling

**Year**: 2025  
**Venue**: arXiv`<br>Shanghai AI Laboratory  
**arXiv**: [2507.05240](https://arxiv.org/pdf/2507.05240)  
**Code**: [https://github.com/InternRobotics/StreamVLN](https://github.com/InternRobotics/StreamVLN)  

## Overview

将Video-LLM（LLaVA-Video模型，采用的是Qwen2-7B）扩展为交错的视觉-语言-动作模型，进而实现多轮对话下与视频的连续交互;为了应对长期上下文管理和计算效率的挑战，StreamVLN采用混合的慢速-快速上下文建模策略:快速流式对话部分通过活动对话的滑动窗口促进响应式动作生成;缓慢更新的内存部分使用3D感知Token来修剪策略以及压缩历史视觉状态。这部分使得StreamVLN可以通过键值对的缓存重用，实现连贯的多回合对话

## See Also

- [[vision_and_language_navigation|Vision-Language Navigation]]
- [[object_goal_navigation|Object-Goal Navigation]]

