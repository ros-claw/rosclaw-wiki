---
id: relative_change_in_success_rcs
title: Relative Change in Success (RCS)
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-30T02:21:02'
last_reinforced: '2026-04-30T02:21:02'
supersedes: []
sources:
- papers/2211.16649.pdf
source_type: arxiv_paper
---

# Relative Change in Success (RCS)

**Relative Change in Success (RCS)** is a metric used to evaluate generalization across environments within the field of [[Vision-and-Language Navigation]] (VLN). It quantifies the relative improvement or degradation in success rate when a model is transferred from a source environment (e.g., training distribution) to a target environment (e.g., unseen scenes), thereby measuring transfer capability and robustness.

## Definition

RCS is defined as the percentage change in the success rate between two experimental conditions — typically the success rate in a seen environment versus that in an unseen environment, or between pretrained and fine-tuned models. A higher (positive) RCS indicates better generalization, while a negative RCS signals overfitting or poor transfer.

## Relationship

This metric is part of the broader set of [[Evaluation Metrics for VLN]] ⚠️. Unlike absolute success rate (SR) or navigation error (NE), RCS focuses on *relative* change, making it more informative for cross‑setting comparisons. It is typically reported alongside standard metrics such as:

- **Success Rate (SR)**
- **Oracle Success Rate (OSR)**
- **Navigation Error (NE)**
- **Success weighted by Path Length (SPL)**

RCS can be computed as:

\[
RCS = \frac{SR_{target} - SR_{source}}{SR_{source}} \times 100\%
\]

## Usage

In practice, RCS is a diagnostic tool:

- A **large negative RCS** from seen to unseen environments suggests the model has memorized training environments rather than learning generalizable representations.
- A **small or zero RCS** indicates robust generalization.
- A **positive RCS** may arise when a model benefits from domain adaptation or transfer learning (e.g., using external knowledge or pretraining on large datasets).

This metric is particularly relevant in works that evaluate sim‑to‑real transfer or cross‑scene generalization in VLN, such as the paper “Core Challenges in Embodied Vision‑Language Planning” (arxiv [2211.16649](https://arxiv.org/abs/2211.16649)).

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Relative Change in Success (RCS)` --[[related_to]] ⚠️--> `Vision-and-Language Navigation`
