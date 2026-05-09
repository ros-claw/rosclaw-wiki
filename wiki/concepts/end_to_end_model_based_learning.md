---
id: end_to_end_model_based_learning
title: End-to-end model-based learning
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-29T21:30:32'
last_reinforced: '2026-04-29T21:30:32'
supersedes: []
sources:
- papers/2403.06828.pdf
source_type: arxiv_paper
---

# End-to-end Model-based Learning

## Definition
End-to-end model-based learning refers to methods that learn a mathematical model from data and use that model for decision-making, with the ability to fine-tune parameters via backpropagation. In [[NeuPAN]], it allows interpretable motion generation while maintaining data-driven adaptability.

## Domain
This concept is primarily applied in **robot navigation**, where it bridges perception and control through a differentiable model.

## Characteristics
- Combines **data-driven** and **knowledge-driven** approaches.
- Provides **interpretability** — the learned model can be inspected and reasoned about.
- Enables **fine-tuning** of model parameters via backpropagation, allowing the system to adapt to new environments or tasks without full retraining.

## Capabilities
- **Directly maps perception to control** — eliminates hand-crafted intermediate representations.
- **Avoids error propagation** common in cascaded pipelines, because perception, planning, and control are unified in a single differentiable computation graph.

## Relationship to Other Concepts
- **Used by**: [[NeuPAN]] implements end-to-end model-based learning for real-time navigation.
- **Related to**: 
  - [[model-based learning]] ⚠️ ⚠️ — shares the core idea of using an explicit model, but end-to-end model-based learning also integrates the model into a differentiable, data‑trained pipeline.
  - [[end-to-end learning]] — inherits the principle of learning a mapping from raw inputs to outputs, but adds a structured model component for interpretability and safety.

## Advantages over Pure Alternatives
Compared to pure **model-based** approaches, end-to-end model‑based learning does not require hand‑designed dynamics or cost functions; it learns them from data. Compared to pure **end-to-end** black‑box methods, it retains a **structured, interpretable model** that can be probed and debugged.

## Source
Based on arxiv paper 2403.06828 (NeuPAN).

---

**See also:** [[NeuPAN]], [[model-based learning]] ⚠️ ⚠️, [[end-to-end learning]]

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Pending review:**
- `End-to-end model-based learning` --[[related_to]] ⚠️--> `NeuPAN` _(wikilink)_
