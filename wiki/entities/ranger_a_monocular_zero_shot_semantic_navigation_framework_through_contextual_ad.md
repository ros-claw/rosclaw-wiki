---
id: ranger_a_monocular_zero_shot_semantic_navigation_framework_through_contextual_ad
type: algorithm
tags:
- vln
- vision-language-navigation
- '2025'
confidence: 0.65
created_at: '2026-05-11'
sources:
- https://arxiv.org/pdf/2512.24212
---

# RANGER: A Monocular Zero-Shot Semantic Navigation Framework through Contextual Adaptation

**Year**: 2025  
**Venue**: arXiv`<br>Beihang University  
**arXiv**: [2512.24212](https://arxiv.org/pdf/2512.24212)  

## Overview

对于RGB输入先通过MASt3R-SLAM估算pose和dense 3D map，然后调用语以模块（CLIP+Grounding DINO）生成语义点云，导航则是采用基于2D栅格（由3D投影而来）的路径规划，进而实现zero-shot目标导航

## See Also

- [[vision_and_language_navigation|Vision-Language Navigation]]
- [[object_goal_navigation|Object-Goal Navigation]]

