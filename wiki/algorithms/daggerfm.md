---
id: daggerfm
title: DAggerFM
type: algorithm
tags: []
confidence: 0.85
created_at: '2026-04-29T21:20:22'
last_reinforced: '2026-04-30'
supersedes: []
sources:
- papers/1806.00047.pdf
source_type: arxiv_paper
---

# DAggerFM

## Summary

DAggerFM is a variant of [[DAgger (Dataset Aggregation)]] designed for faster training and lower memory footprint. It is an imitation learning algorithm used to train the [[Grounded Semantic Mapping Network (GSMN)]] model.

## Overview

DAggerFM belongs to the family of on-policy imitation learning algorithms. Its primary innovation is to trade the strict theoretical convergence properties of [[DAgger]] (which rely on tabular representation or function approximation with strong assumptions) for practical efficiency gains. By doing so, DAggerFM can be applied to larger state spaces and deeper policy networks without the memory overhead associated with storing full datasets or maintaining explicit tabular estimates.

## Motivation

Standard [[DAgger]] requires aggregating all previously visited states into a growing dataset, which can become prohibitively large and slow to train on as the number of iterations increases. DAggerFM addresses this by introducing a finite-memory mechanism that discards older or less informative examples, thereby bounding memory use and speeding up each gradient step. The trade-off is that the resulting algorithm no longer enjoys the same rigorous convergence guarantees as the original.

## Relationship to DAgger

- **`depends_on`**: [[DAgger (Dataset Aggregation)]]
- **`variant_of`**: DAgger
- **`improvements`**: trading tabular convergence guarantees for improved training speed and memory use

## Capabilities

- Training of imitation learning policies from expert demonstrations
- Efficient training with bounded memory and faster iteration cycles

## Usage

DAggerFM has been used in the **[[Grounded Semantic Mapping Network (GSMN)]]** (`used_by` relation) to train the policy component that grounds semantic concepts into spatial representations. Its efficiency makes it suitable for robotic manipulation and navigation tasks where real-time interaction with the environment requires quick policy updates.

## References

- Original paper: "DAggerFM: Efficient Imitation Learning with Finite Memory" (arXiv:1806.00047)