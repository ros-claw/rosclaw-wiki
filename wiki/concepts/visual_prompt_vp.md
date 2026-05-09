---
id: visual_prompt_vp
title: Visual Prompt (VP)
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-30T00:03:08'
last_reinforced: '2026-04-30T00:03:08'
supersedes: []
sources:
- papers/2512.02631.pdf
source_type: arxiv_paper
---

## Visual Prompt (VP)

Visual Prompt is a **dual-view visual prompting technique** designed for large vision-language models (LVLMs) in visual language navigation (VLN). It operates as a **zero-shot module** — no fine-tuning of the base LVLM is required — and aims to **reduce perceptual hallucinations** while improving the agent’s understanding of its current spatial state.

The technique inserts additional structured visual cues into the LVLM’s input space, effectively grounding the model’s attention on task-relevant visual features. This allows the agent to make more reliable navigation decisions without retraining the underlying vision-language backbone.

### Key Parameters
- **Type**: Dual-view visual prompting technique  
- **Usage**: Zero-shot module for [[LVLM]] ⚠️-based navigation  
- **Purpose**: Reduce perception hallucinations and improve spatial state understanding  

### Capabilities
- Enhances the agent’s understanding of current spatial states  
- Enables zero-shot navigation improvement — no fine-tuning of the vision-language model is required  

### Relationships
- **Used in**: [[SeeNav-Agent]] (as a core component) and [[GPT-4.1]] (in its zero-shot VP variant)  
- **Complemented by**: [[Step Reward Group Policy Optimization (SRGPO)]] — a reinforcement learning method that further improves navigation behavior  

### Background
Visual Prompt was introduced in the paper *"SeeNav-Agent: See Before You Navigate for Zero-Shot VLN with Embodied Error"* (arxiv 2512.02631). It forms part of the effort to bridge sim-to-real gaps by providing robust visual grounding without requiring task-specific training data.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Pending review:**
- `Visual Prompt (VP)` --[[related_to]] ⚠️ ⚠️--> `SeeNav-Agent` _(wikilink)_
- `Visual Prompt (VP)` --[[related_to]] ⚠️ ⚠️--> `Step Reward Group Policy Optimization (SRGPO)` _(wikilink)_
