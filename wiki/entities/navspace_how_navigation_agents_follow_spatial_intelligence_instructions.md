---
id: navspace_how_navigation_agents_follow_spatial_intelligence_instructions
type: algorithm
tags:
- vln
- vision-language-navigation
- '2026'
- real-robot
confidence: 0.8
created_at: '2026-05-11'
sources:
- https://arxiv.org/pdf/2510.08173
- https://github.com/TidalHarley/NavSpace
---

# NavSpace: How Navigation Agents Follow Spatial Intelligence Instructions

**Year**: 2026  
**Venue**: ICRA`<br>Peking University  
**arXiv**: [2510.08173](https://arxiv.org/pdf/2510.08173)  
**Code**: [https://github.com/TidalHarley/NavSpace](https://github.com/TidalHarley/NavSpace)  

## Overview

第一个基于空间智能的评估基准（包含 1228 个高质量的轨迹-指令对，给定 NavSpace 中的语言指令，给定导航智能体当前的第一视角观测，导航智能体需要在时间步内预测下一个导航动作；导航智能体一次可以预测的动作包括前进0.25米，左转30度，右转30度，停）,基于Habitat 3.0 模拟器和 HM3D 场景构建了数据收集平台；标注的过程采用人工+GPT-5；并提出SNav Model：使用 SigLIP 当作视频编码器，每8帧接收观测的 RGB 图作为一组，经过编码器提取视觉编码特征，再经过两层 MLP 投影到语言模型的输入空间中。指令同样经过 tokenizer，与提取的视觉特征一起通过 Qwen2 的解码器，输出一连串的动作（前进、左转、右转、停止等）。整个模型采用 Llava-Video-7b 作为主干网络；实验方面：使用 AgiBot Lingxi D1 四足机器人，机器人接收到导航指令后，将 RGB 观测传输到远程服务器上的导航模型（搭载 NVIDIA A100 GPU），模型预测动作并通过 D1 的运动 API 执行。（SR约为32%）

## See Also

- [[vision_and_language_navigation|Vision-Language Navigation]]
- [[object_goal_navigation|Object-Goal Navigation]]
- [[ai_habitat|AI Habitat]]

