---
id: waypoint_predictor
title: waypoint predictor
type: algorithm
tags: []
confidence: 0.85
created_at: '2026-04-29T21:02:50'
last_reinforced: '2026-04-30'
supersedes: []
sources:
- papers/2408.10388.pdf
- papers/2203.02764.pdf
source_type: arxiv_paper
---

# Waypoints Predictor

A **waypoints predictor** is an algorithm component that generates a set of candidate waypoints during navigation, allowing agents designed with high-level actions to be transferred to and trained in continuous environments. It is a key sub-module in [[Vision and Language Navigation in the Continuous Environment (VLN-CE)]] ⚠️, where it selects intermediate sub-goals to guide the agent toward the final navigation target.

## Description

The predictor generates candidate waypoints from a robot observation and the environment connectivity graph. It simplifies navigation in continuous space into a sequence of view-selection decisions, enabling agents originally developed for discrete environments (e.g., using graph-based navigation) to operate in continuous settings. The predictor is typically trained using refined connectivity graphs derived from [[Matterport3D]] ⚠️ ⚠️ datasets.

## Parameters

- **Input**: robot observation, environment connectivity graph
- **Output**: set of candidate waypoints

## Capabilities

- Generates candidate waypoints during navigation, enabling discrete decision-making in continuous environments.
- Simplifies navigation actions into view selection, reducing the complexity of the action space.
- Enables transfer from discrete to continuous environments for agents trained with high-level actions.
- Can be augmented during training (e.g., through data augmentation techniques) to diversify views and paths, improving generalization.

## Dependencies

- **Depends on**: [[Connectivity Graph]] (e.g., from [[Matterport3D]] ⚠️ ⚠️)

## Used By

- [[Cross-Modal Matching Agent]]
- [[Recurrent VLN-BERT]]

## Limitations

Existing waypoint predictors often neglect object semantics and passibility attributes. These attributes are informative for action feasibility—for example, knowledge that a chair is an obstacle (semantics) or that a terrain is traversable (passibility). Ignoring such features can lead to unrealistic or infeasible waypoint predictions.

## Relationship Summary

- **Used in**: [[VLN-CE]]
- **Has issue**: Neglects object semantics and passibility attributes (see Limitations)
- **Depends on**: [[Connectivity Graph]]

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `waypoint predictor` --[[based_on]] ⚠️--> `VLN-CE`

**Newly identified links:**
- `waypoint predictor` --[[used_by]] ⚠️ ⚠️--> [[Cross-Modal Matching Agent]]
- `waypoint predictor` --[[used_by]] ⚠️ ⚠️--> [[Recurrent VLN-BERT]]
- `waypoint predictor` --[[depends_on]] ⚠️--> [[Connectivity Graph]]