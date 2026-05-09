---
id: cross_embodiment
title: Cross-embodiment
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-30T00:39:10'
last_reinforced: '2026-04-30T00:39:10'
supersedes: []
sources:
- papers/2509.12129.pdf
source_type: arxiv_paper
---

# Cross-embodiment

## Definition

**Cross-embodiment** refers to the ability of a single model or control policy to operate across multiple distinct robot platforms without task‑specific adaptation. Rather than being tied to a particular morphology (e.g., a specific arm length, number of legs, or sensor suite), a cross‑embodiment system can transfer skills and behaviors between different robots by learning shared representations that abstract away physical differences.

## Capabilities

- Enables a single model to control multiple robot types without task‑specific adaptation.

## Relationships

- **Is property of** → [[NavFoM]]: The Navigation Foundation Model (NavFoM) architecture is designed around cross‑embodiment generalization, allowing it to control wheeled, legged, and aerial platforms from a unified policy.
- **Contrasts with** → [[single‑embodiment architectures]] ⚠️: Traditional approaches train separate policies for each robot morphology, requiring significant redesign and retraining when hardware changes.

## Importance

Cross‑embodiment generalization is key to scalable deployment in real‑world robotics. Without it, every new robot platform demands a complete retraining pipeline, limiting rapid experimentation and real‑world adaptation. By unifying control across embodiments, robots can share learned experiences, accelerate development, and operate in environments where hardware may be swapped or upgraded frequently.

## Sources

- Data: `papers/2509.12129.pdf` (arXiv)

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Pending review:**
- `Cross-embodiment` --[[related_to]] ⚠️--> `NavFoM` _(wikilink)_
