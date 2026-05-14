---
id: r2r_ce_dataset
title: R2R-CE dataset
type: entity
tags: []
confidence: 0.95
created_at: '2026-04-29T21:04:58'
last_reinforced: '2026-04-30'
supersedes: []
sources:
- papers/2304.03047.pdf
source_type: arxiv_paper
---

# RxR-CE dataset

**RxR-CE** (Rendezvous in Continuous Environments), also referred to as **R2R-CE** in some earlier publications, is a benchmark dataset for **vision-language navigation in continuous environments (VLN-CE)**. It adapts existing navigational instructions and trajectories from the RxR dataset ⚠️ ⚠️ ⚠️ ⚠️ ⚠️ to a continuous action space, requiring agents to operate in realistic 3D simulators with free movement.

## Description

- **Type**: Dataset  
- **Domain**: VLN-CE  
- **Task**: Vision-language navigation in continuous environments  
- **Format**: The dataset is derived from photorealistic indoor scenes (via the Matterport3D simulator) paired with natural-language instructions originally sourced from the RxR dataset ⚠️ ⚠️ ⚠️ ⚠️ ⚠️. Unlike its discrete predecessor, RxR-CE uses a continuous action space, enabling more realistic agent motion.

The exact relationship between RxR-CE and R2R-CE has been a source of confusion in the literature. Some papers treat them as the same benchmark, while others draw a distinction based on their originating dataset (RxR vs. R2R). The original ETPNav paper (arXiv:2304.03047) refers to it as simply the "VLN-CE benchmark" and does not clearly differentiate; later analyses have clarified that the correct expanded name is *Rendezvous* in Continuous Environments, indicating a link to the RxR dataset rather than R2R.

## Relationships

- **derived_from** → RxR dataset ⚠️ ⚠️ ⚠️ ⚠️ ⚠️ — the RxR dataset provides the language instructions and human-annotated paths.
- **used_by** → ETPNav — the ETPNav agent achieved substantial improvements on this benchmark.

## Usage

RxR-CE is the primary evaluation benchmark for the ETPNav agent. In the ETPNav paper (arXiv:2304.03047), the agent obtained a >10% improvement over prior state-of-the-art methods. A later analysis claims a >20% improvement; the discrepancy is documented in the conflict section below. The dataset continues to be a key driver of continuous VLN research.

## Related Pages

- ETPNav — agent that uses RxR-CE for evaluation  
- R2R dataset — predecessor discrete navigation dataset (distinct from RxR)  
- RxR dataset ⚠️ ⚠️ ⚠️ ⚠️ ⚠️ — base dataset for RxR-CE  
- R2R-CE — a potential alias or sibling dataset  
- vision-language navigation — general task domain  

---

## 待核实冲突

1. **Base dataset identity (partially resolved)**  
   The current page now reflects that RxR-CE is derived from RxR dataset ⚠️ ⚠️ ⚠️ ⚠️ ⚠️, consistent with the source from arXiv:2304.03047. However, some external references continue to call it R2R-CE or treat it interchangeably. *Resolution needed*: Confirm whether the two names refer to the same dataset or distinct benchmarks in the original RxR and R2R documentation.

2. **Improvement magnitude**  
   - ETPNav paper reports: >10% improvement over prior SOTA.  
   - A later analysis claims: >20% improvement over prior SOTA.  
   - *Resolution needed*: Check the exact evaluation metrics (e.g., SR vs. SPL) and whether the improvement is relative to the same baseline. Both values may be correct for different metrics or subsets.