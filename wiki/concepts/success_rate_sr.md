---
id: success_rate_sr
title: Success Rate (SR)
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-30T00:32:56'
last_reinforced: '2026-04-30T00:32:56'
supersedes: []
sources:
- papers/2511.06182.pdf
source_type: arxiv_paper
---

## Success Rate (SR)

**Success Rate (SR)** is a metric used to evaluate navigation agents in embodied AI. It measures the percentage of navigation episodes in which the agent successfully reaches the target goal location. A higher SR indicates a more reliable navigation policy.

### Definition

Percentage of navigation episodes that reach the goal. OpenVLN improves SR by up to 4.34%.

### Usage in Evaluation

SR is commonly used as the primary **evaluation metric** in vision-language navigation (VLN) tasks. It is computed as:

```
SR = (Number of successful episodes) / (Total episodes) × 100%
```

An episode is considered successful when the agent stops within a predefined distance (e.g., 3 m) from the goal after executing a valid sequence of actions.

### Relationship to Other Concepts

- **OpenVLN** → SR is the key performance indicator improved by this framework.  
- **depends_on**: Reliable goal detection and path planning from Robot Navigation ⚠️ stacks.  
- **contrasts with**: Metrics like **Path Length** (efficiency) or **Execution Time** (speed); SR focuses purely on goal‑reaching outcome.

### Typical Improvements

In recent literature (e.g., OpenVLN), SR gains are reported in percentage points. The 4.34% improvement cited indicates a relative or absolute increase over baseline methods, depending on the experimental setup.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Pending review:**
- `Success Rate (SR)` --related_to ⚠️--> `OpenVLN` _(wikilink)_
