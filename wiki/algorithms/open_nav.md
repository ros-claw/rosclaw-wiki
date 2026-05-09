---
id: open_nav
title: Open-Nav
type: algorithm
tags: []
confidence: 0.85
created_at: '2026-04-29T20:51:01'
last_reinforced: '2026-04-30'
supersedes: []
sources:
- papers/2409.18794.pdf
source_type: arxiv_paper
---

---

# Open-Nav

**Type**: Algorithm  
**Confidence**: 0.85 *(reinforced by peer-reviewed arxiv paper 2409.18794)*

**Open-Nav** is a novel method for zero-shot [[Vision-and-Language Navigation]] (VLN) that employs open-source [[Large Language Models]] (LLMs) with [[spatial-temporal chain-of-thought]] ⚠️ reasoning to navigate continuous 3D environments from [[natural language instructions]] ⚠️. It breaks down navigation tasks into instruction comprehension, progress estimation, and decision-making using spatial-temporal CoT reasoning.

## Methodology

Open-Nav employs a spatial-temporal chain-of-thought (CoT) reasoning approach that decomposes the VLN task into instruction comprehension, progress estimation, and decision-making. It enhances [[scene perception]] ⚠️ with fine-grained object and spatial knowledge to improve LLM reasoning. This decomposition allows the model to iteratively process visual observations and linguistic cues without requiring task-specific training.

## Capabilities

- Zero-shot vision-and-language navigation in continuous environments using open-source LLMs
- Spatial-temporal chain-of-thought reasoning for task decomposition
- Instruction comprehension, progress estimation, and decision-making
- Enhanced scene perception with fine-grained object and spatial knowledge

## Parameters

| Parameter | Value |
|-----------|-------|
| Paradigm | Zero-shot VLN |
| LLM type | Open-source large language models |
| Reasoning method | Spatial-temporal chain-of-thought (CoT) |

## Relationships

- **uses**: [[Large Language Models (LLMs)]], [[Spatial-temporal chain-of-thought reasoning]]
- **depends_on**: [[open-source LLMs]] ⚠️, [[scene perception models]] ⚠️, [[LLM reasoning]] ⚠️
- **contradicts**: [[closed-source LLM approaches]] ⚠️ (e.g., GPT-4) used for VLN, as Open-Nav avoids token costs and data breach risks while achieving competitive performance

## Comparison

Open-Nav achieves competitive performance compared to closed-source LLM methods (such as [[GPT-4]]-based VLN agents) while avoiding token costs and data breach risks. It demonstrates that open-source LLMs, when combined with structured reasoning, can match or approach the performance of proprietary models in embodied navigation tasks.

## References

- Source: arxiv paper 2409.18794 – "Open-Nav: Zero-shot Vision-and-Language Navigation using Open-source LLMs with Spatial-temporal Chain-of-Thought Reasoning" (available in `papers/2409.18794.pdf`)

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._  
**Confirmed links:**
- `Open-Nav` --[[implements]] ⚠️--> `Large Language Models (LLMs)`