---
id: r2r_dataset
title: R2R dataset
type: concept
tags: []
confidence: 0.85
created_at: '2026-04-30T01:37:37'
last_reinforced: '2026-04-30'
supersedes: []
sources:
- papers/2302.06072.pdf
- papers/2210.03112.pdf
source_type: arxiv_paper
---

# R2R Dataset

The **R2R dataset** (Room-to-Room) is a fine-grained **Vision-and-Language Navigation (VLN)** benchmark. It provides paired instructions and visual trajectories in photorealistic environments, serving as the standard evaluation suite for measuring state-of-the-art performance in VLN tasks. The dataset is also referred to as the **RxR dataset** in some literature.

The R2R dataset evaluates models on their ability to follow natural language instructions to navigate through real-world indoor spaces. It is closely related to the broader field of [[Embodied AI]] and is widely used to benchmark [[Vision-Language Models]] ⚠️ in grounded, sequential decision-making.

## Naming Note

The source paper (arXiv:2210.03112) refers to this dataset as the **RxR dataset**. The naming appears to be an alternative abbreviation for the original Room-to-Room (R2R) dataset, sharing the same evaluation protocol and environments. If a separate RxR dataset exists, the conflict should be resolved; here, we treat them as synonymous for integration purposes.

## Capabilities

- Used to evaluate state-of-the-art in VLN research.
- Provides fine-grained turn-by-turn instructions with aligned panoramic views.
- Supports both single-path and multi-path evaluation protocols.
- Evaluates instruction-following agents in realistic indoor environments.
- Serves as a standard benchmark for state-of-the-art comparison across VLN models.

## Performance Benchmarks

The RxR dataset (as reported in arXiv:2210.03112) serves as a challenging benchmark. The presented approach achieves state-of-the-art performance with an **NDTW** (Normalized Dynamic Time Warping) of:
- **79.1** in seen environments
- **66.8** in unseen environments

These scores are representative of current leading methods on the standard R2R splits.

## Relationships

- The R2R dataset evaluates **[[Actional Atomic-Concept Learning (AACL)]]**, a method that decomposes navigation instructions into atomic action concepts for more robust policy learning. Implicitly, R2R *depends_on* photorealistic scene databases such as [[Matterport3D]] ⚠️.
- It implements the standard train/val/test splits commonly used in VLN competitions.
- Used in state-of-the-art comparisons across numerous VLN papers.

## Usage Notes

When citing the R2R dataset, refer to the original paper:  
Anderson et al., *Vision-and-Language Navigation: Interpreting visually-grounded navigation instructions in real environments*, CVPR 2018. The source for this page is the subsequent AACL paper (arXiv:2302.06072) and the paper arXiv:2210.03112, both of which use R2R for evaluation.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._  
**Confirmed links:**
- `R2R dataset` --[[related_to]] ⚠️ ⚠️--> `Embodied AI`  
**Pending review:**
- `R2R dataset` --[[related_to]] ⚠️ ⚠️--> `Actional Atomic-Concept Learning (AACL)` _(wikilink)_