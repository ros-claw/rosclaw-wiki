---
id: visual_prompt_vp_technique
title: Visual Prompt (VP) technique
type: algorithm
tags: []
confidence: 0.8
created_at: '2026-04-29T20:48:41'
last_reinforced: '2026-04-29T20:48:41'
supersedes: []
sources:
- papers/2512.02631.pdf
source_type: arxiv_paper
---

# Visual Prompt (VP) Technique

The **Visual Prompt (VP) technique** is a **dual-view visual prompt** algorithm designed to reduce **perception hallucinations** and improve **spatial understanding** in robotic navigation agents. It operates in a **zero-shot** manner, requiring no additional training or fine-tuning, and is a core component of the [[SeeNav-Agent]] system.

## Description

The Visual Prompt technique introduces a dual-view input representation that provides the agent with complementary spatial perspectives. By structuring the visual input as a prompt containing two distinct views, the agent gains a more robust understanding of its current spatial state, mitigating common failures caused by hallucinated or ambiguous perceptual cues. This technique is applied entirely at inference time, making it lightweight and broadly applicable.

## Parameters

| Parameter | Value |
|-----------|-------|
| Type | Dual-view visual prompt |
| Purpose | Reduce perception hallucinations, improve spatial understanding |

## Capabilities

- Achieves **zero-shot improvement** in navigation success rate across diverse environments.
- Enhances the agent's ability to reason about spatial layouts without additional training data.
- Integrates seamlessly into existing vision-language-action (VLA) models used by [[SeeNav-Agent]].

## Relationships

```mermaid
flowchart LR
    VP[Visual Prompt Technique]
    VP -->|part_of| SeeNav[SeeNav-Agent]
    VP -->|depends_on| VLA[Vision-Language-Action Model]
    VP -->|implements| DualView[Dual-View Input Processing]
```

- **Part of**: [[SeeNav-Agent]] — the VP technique is a key algorithmic component of this navigation system.
- **Depends on**: [[Vision-Language-Action Model]] — the technique is applied on top of a VLA backbone to condition its spatial reasoning.
- **Implements**: Dual-view input processing — the core mechanism of combining two visual perspectives into a single prompt.

## See Also

- [[Perception Hallucination]] ⚠️ — the problem the VP technique addresses.
- [[Spatial Understanding]] ⚠️ — the capability improved by the VP technique.
- [[Zero-Shot Navigation]] — the paradigm within which VP operates.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Visual Prompt (VP) technique` --[[extends]] ⚠️--> `SeeNav-Agent`
