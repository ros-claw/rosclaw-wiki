---
id: semantic_similarity_network_ssnet
title: Semantic Similarity Network (SSNet)
type: algorithm
tags: []
confidence: 0.85
created_at: '2026-04-29T21:43:17'
last_reinforced: '2026-04-30'
supersedes: []
sources:
- papers/2206.07423.pdf
source_type: arxiv_paper
---

## Semantic Similarity Network (SSNet)

### Overview

The **Semantic Similarity Network (SSNet)** is a framework for [[zero-shot object goal visual navigation]]. It uses detection results and the [[cosine similarity]] ⚠️ ⚠️ between semantic word embeddings as input to guide a robot toward target objects. Because the input has weak correlation with specific class labels, the policy can generalize to novel classes never seen during training. By decoupling policy from explicit category names and relying instead on continuous semantic similarity, SSNet overcomes a key limitation of traditional object navigation agents that fail when confronted with unseen targets. SSNet was evaluated on the [[AI2-THOR]] simulation platform and demonstrated superior performance over baseline models in zero-shot settings.

### Capabilities

- **Zero-shot object goal navigation** – SSNet can navigate to target objects without requiring any training samples for novel classes.
- **Generalization to novel target classes** – The policy transfers to unseen object categories by leveraging semantic embeddings.
- **State-of-the-art performance** – Outperforms baseline models on zero-shot object navigation tasks in [[AI2-THOR]].

### Parameters

| Parameter | Description |
|-----------|-------------|
| **Input** | Detection results from the environment and cosine similarity between semantic word embeddings of the target name and detected object labels. |
| **Output** | A policy for [[object goal visual navigation]] (e.g., movement commands). |
| **Training** | Zero-shot; no training samples for novel classes required. The network is trained on a set of known classes and learns to transfer via semantic similarity. |

### Relationships

- **Uses** detection results, [[cosine similarity]] ⚠️ ⚠️, and [[semantic word embeddings]] ⚠️ (e.g., GloVe, Word2Vec).
- **Tested on** [[AI2-THOR platform]] ⚠️.
- **Depends on** the paradigm of [[object goal visual navigation]].
- **Implements** [[zero-shot object goal visual navigation]].

### References

- *Semantic Similarity Network for Zero-Shot Object Goal Navigation* (arXiv:2206.07423).