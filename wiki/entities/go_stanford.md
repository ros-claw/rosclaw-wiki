---
id: go_stanford
title: Go Stanford
type: entity
tags: []
confidence: 0.85
created_at: '2026-04-29T21:31:03'
last_reinforced: '2026-04-30'
supersedes: []
sources:
- papers/2510.08713.pdf
source_type: arxiv_paper
---

# Go Stanford

**Go Stanford** is a benchmark for visual navigation, originally designed to evaluate navigation agents on real-world indoor scenes. It is included as a component of [[Navigation benchmarks]] ⚠️ ⚠️ and was one of four benchmarks used in the evaluation of [[UniWM]].

## Overview

The benchmark consists of a set of visual navigation tasks where an agent must navigate to a specified goal location using only egocentric visual observations. It provides standardized environments and evaluation protocols to measure navigation performance across different algorithms and models. Key metrics include **success rate** and **trajectory error**, emphasizing both goal achievement and path efficiency.

## Relationship

- Part of [[Navigation benchmarks]] ⚠️ ⚠️
- Used to evaluate [[UniWM]] — alongside three other benchmarks, Go Stanford tests the model's generalization capability in zero-shot visual navigation.

## Usage in Research

In the paper evaluating [[UniWM]], Go Stanford served as one of four key benchmarks to assess the model's generalization in unseen environments. The benchmark's design highlights zero-shot transfer and long-horizon planning under partial observability, with performance quantified by success rate and trajectory error.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Go Stanford` --[[uses]] ⚠️--> `UniWM`