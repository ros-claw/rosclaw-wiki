---
id: prompt_based_learning
title: Prompt-based Learning
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-30T02:06:22'
last_reinforced: '2026-04-30T02:06:22'
supersedes: []
sources:
- papers/2203.04006.pdf
source_type: arxiv_paper
---

# Prompt-based Learning

**Prompt-based learning** is a paradigm in natural language processing and machine learning in which a model is adapted to a downstream task by providing **language embedding prompts** — input templates or prefixes — rather than full fine-tuning of parameters. This approach leverages prior knowledge stored in pretrained models and enables fast adaptation with minimal data and computation.

## Capabilities

- **Fast adaptation**: By using prompts as a flexible interface, the model can be directed to new tasks without retraining all parameters, leveraging its existing knowledge efficiently.
- **Improved learning efficiency**: Compared to conventional fine-tuning, prompt-based methods often achieve comparable or better performance with far fewer training examples and updates.

## Use in ProbES

[[ProbES]] introduces prompt-based learning to achieve fast adaptation for language embeddings, substantially improving learning efficiency in the context of probabilistic embedding spaces.

## Related Concepts

- [[Transfer Learning]] ⚠️
- [[Few-shot Learning]] ⚠️
- [[Language Model Fine-tuning]] ⚠️ (conventional approach, contradicted by prompt-based methods)
- [[ProbES]] (uses prompt-based learning)

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Pending review:**
- `Prompt-based Learning` --[[related_to]] ⚠️--> `ProbES` _(wikilink)_
