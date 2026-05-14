---
id: soon
title: SOON
type: entity
tags: []
confidence: 0.8
created_at: '2026-04-30T01:08:16'
last_reinforced: '2026-04-30T01:08:16'
supersedes: []
sources:
- papers/2506.01551.pdf
source_type: arxiv_paper
---

# SOON

**SOON** is a VLN ⚠️ ⚠️ benchmark used for evaluating vision-and-language navigation models. It was introduced as part of the EvolveNav framework to test the ability of agents to follow natural language instructions in continuous environments with evolving conditions.

## Overview

SOON focuses on measuring navigation performance under distributional shifts and environment changes, making it a challenging benchmark for assessing robustness and generalization in VLN models. It is specifically designed to complement the training and evaluation protocols of EvolveNav.

## Relationships

- **tests** → VLN models ⚠️  
  SOON evaluates the capabilities of VLN agents in dynamic settings.
- **evaluated_by** → EvolveNav  
  The benchmark is used as the primary evaluation suite within the EvolveNav framework.

## Usage

SOON serves as the standard testbed for validating the effectiveness of navigation algorithms that must adapt to changing environments, such as those proposed in EvolveNav. Its scenarios encompass varying lighting, object placements, and layout modifications.

## See also

- EvolveNav (depends on SOON for evaluation)
- VLN ⚠️ ⚠️

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `SOON` --uses ⚠️--> `EvolveNav`
