---
id: capnav_benchmarking_vision_language_models_on_capability_conditioned_indoor_navi
type: entity
tags:
- vln
- vision-language-navigation
- '2026'
- dataset
confidence: 0.8
created_at: '2026-05-11'
sources:
- https://arxiv.org/pdf/2602.18424
- https://github.com/makeabilitylab/CapNav
---

# CapNav: Benchmarking Vision Language Models on Capability-conditioned Indoor Navigation

**Year**: 2026  
**Venue**: arXiv`<br>University of Washington  
**arXiv**: [2602.18424](https://arxiv.org/pdf/2602.18424)  
**Code**: [https://github.com/makeabilitylab/CapNav](https://github.com/makeabilitylab/CapNav)  

## Overview

CapNav基准;从导航可行性、路径有效性、路线可通行性、不可行推理质量四个维度评估模型性能；从HM3D和Matterport3D选取45个3D场景，由Gemini 2.5 Pro生成导航任务并人工验证，为5类主体完成边级可通行性标注，对13款主流VLM进行验证，闭源模型表现远优于开源模型：Gemini 2.5 Pro/Flash、GPT-5-Pro超越人类平均水平（0.61），但未达人类最佳水平（0.75）

## See Also

- [[vision_and_language_navigation|Vision-Language Navigation]]
- [[object_goal_navigation|Object-Goal Navigation]]

