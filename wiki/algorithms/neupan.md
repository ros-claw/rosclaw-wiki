---
id: neupan
title: NeuPAN
type: algorithm
tags: []
confidence: 0.8
created_at: '2026-04-29T21:29:10'
last_reinforced: '2026-04-29T21:29:10'
supersedes: []
sources:
- papers/2403.06828.pdf
source_type: arxiv_paper
---

## Overview

**NeuPAN** is a robot motion planner that directly maps raw point cloud data to motions using an end-to-end model-based learning approach. It integrates a plug-and-play [[Proximal Alternating-minimization Network (PAN)]] to solve point-level constraints for collision-free navigation. The system operates in real-time in cluttered unknown environments and works with arbitrarily shaped objects.

## Key Innovation

NeuPAN avoids error propagation from perception to control by using a latent distance feature space, and provides interpretability through a mathematical model with neurons in the loop. This design enables environment-invariant operation across diverse settings such as sandbox, office, corridor, and parking lot.

## Parameters

- **Type**: End-to-end model-based learning
- **Input**: Raw point cloud data
- **Output**: Collision-free motion
- **Key component**: [[Proximal Alternating-minimization Network (PAN)]]
- **Learning paradigm**: Plug-and-play with backpropagation fine-tuning

## Capabilities

- Real-time navigation in cluttered unknown environments
- Direct mapping from point cloud to latent distance feature space
- Interpretable motion generation
- Environment-invariant operation across sandbox, office, corridor, parking lot
- Works with arbitrarily shaped objects
- Transforms impassable paths into passable ones

## Relationships

- **Uses**: [[Proximal Alternating-minimization Network (PAN)]], [[point cloud sensors]] ⚠️
- **Depends on**: [[end-to-end model-based learning]], [[tightly coupled perception-to-control framework]] ⚠️
- **Implements**: [[real-time collision avoidance for nonholonomic robots]] ⚠️

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `NeuPAN` --[[extends]] ⚠️--> `Proximal Alternating-minimization Network (PAN)`
- `NeuPAN` --[[based_on]] ⚠️--> `end-to-end model-based learning`
