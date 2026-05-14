---
id: probes_prompt_based_environmental_self_exploration
title: ProbES (Prompt-based Environmental Self-Exploration)
type: algorithm
tags: []
confidence: 0.8
created_at: '2026-04-30T02:03:43'
last_reinforced: '2026-04-30T02:03:43'
supersedes: []
sources:
- papers/2203.04006.pdf
source_type: arxiv_paper
---

## ProbES (Prompt-based Environmental Self-Exploration)

ProbES is a method for vision-language navigation that uses CLIP to automatically generate trajectory-instruction pairs via self-exploration, avoiding the need for human-labeled navigation data. It employs prompt-based learning to adapt language embeddings efficiently, enabling fast adaptation to diverse Visual-Language Navigation ⚠️ ⚠️ tasks.

### Parameters

- **Prompt type**: learnable language embeddings
- **Self-exploration sampling**: trajectory sampling
- **Instruction generation**: via CLIP

### Capabilities

- Self-explore environments by sampling trajectories
- Automatically generate structured instructions via CLIP
- Build in-domain datasets without human labeling
- Fast cross-domain adaptation via prompt-based learning
- Improve generalization on unseen scenes

### Relationships

- **Uses**: CLIP
- **Depends on**: CLIP, prompt-based learning
- **Applied to**: Visual-Language Navigation ⚠️ ⚠️, REVERIE

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `ProbES (Prompt-based Environmental Self-Exploration)` --extends ⚠️--> `CLIP`
