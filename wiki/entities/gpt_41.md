---
id: gpt_41
title: GPT-4.1
type: entity
tags: []
confidence: 0.8
created_at: '2026-04-30T00:01:36'
last_reinforced: '2026-04-30T00:01:36'
supersedes: []
sources:
- papers/2512.02631.pdf
source_type: arxiv_paper
---

### GPT-4.1

**GPT-4.1** is a Large Vision-Language Model (LVLM) developed by OpenAI. In the context of embodied intelligence, it serves as a backbone for zero-shot visual navigation when paired with a dual-view **Visual Prompt (VP)** module, achieving state-of-the-art performance on the EmbodiedBench Navigation benchmark.

#### Capabilities

- Performs **zero-shot visual navigation** when combined with a dual-view Visual Prompt — no fine-tuning or task-specific training required.
- Outperforms the previous best LVLM by approximately 20 percentage points on the **EmbodiedBench** navigation task.

#### Usage in SeeNav-Agent

GPT-4.1 acts as the core reasoning backbone of SeeNav-Agent. The system augments the model with a **zero-shot Visual Prompt** module that transforms raw camera observations into structured prompts, enabling the model to produce goal-directed navigation actions without explicit imitation learning or reinforcement.

#### Performance

When evaluated on the EmbodiedBench Navigation benchmark, **GPT-4.1 with zero-shot VP** achieved a **86.7% navigation success rate**, surpassing all prior LVLM-based approaches. This result demonstrates that large vision-language models, when properly prompted, can serve as effective controllers for embodied navigation tasks.

#### Relationships

- **used_in** → SeeNav-Agent
- **enhanced_by** → Visual Prompt (VP)
- **implements** → zero-shot visual navigation
- **depends_on** → EmbodiedBench for evaluation

#### Parameters

| Field | Value |
|-------|-------|
| Type | Large Vision-Language Model (LVLM) |
| Usage in SeeNav-Agent | Backbone with zero-shot Visual Prompt |
| Navigation success rate (with VP) | 86.7% on EmbodiedBench Navigation |

---

*Source: 2512.02631.pdf ⚠️ (SeeNav-Agent paper)*

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `GPT-4.1` --depends_on ⚠️--> `EmbodiedBench`
- `GPT-4.1` --uses ⚠️--> `SeeNav-Agent`
