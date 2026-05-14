---
id: nasa_jpl_nebula2_wildos
type: entity
tags: [code-repository, ros, ros2, vln, object-search, outdoor-navigation, jpl, nasa]
confidence: 0.92
created_at: 2026-05-11
sources:
  - https://github.com/nasa-jpl/nebula2-wildos
  - https://arxiv.org/abs/2602.19308
  - https://leggedrobotics.github.io/wildos/
---

# Nebula2-WildOS (NASA JPL)

Official implementation of **WildOS: Open-Vocabulary Object Search in the Wild** from NASA JPL and ETH Zurich. A unified system for long-range, open-vocabulary object search by mobile robots in unstructured outdoor environments.

## Overview

WildOS enables autonomous navigation to distant, semantically specified targets across complex off-road and urban terrains without requiring prior maps. By combining a sparse topological memory with vision foundation models and probabilistic localization, it bridges semantic reasoning and geometric safety over 100+ meter distances.

## Key Modules

| Module | Description |
|--------|-------------|
| ExploRFM | Foundation-model-based vision module scoring frontier nodes |
| triangulation3d | Particle-filter-based coarse localization of target queries |
| graphnav_planner | Sparse navigation graph planner for exploration |
| [[visual_navigation]] | Visual navigation components |
| nvidia_radio | NVIDIA radio communication interface |

## Architecture

```
RGB/Depth Images → ExploRFM → Traversability + Frontier + Object Similarity
                                    ↓
Particle Filter Localization ← Target Query (open-vocabulary)
                                    ↓
Sparse Navigation Graph → Hierarchical Planner → Navigation Commands
```

## Capabilities

- **Open-vocabulary object search**: Query any object class without training
- **Long-range navigation**: Operates over 100+ meter distances
- **Geometric safety**: Ensures safe traversal while exploring semantically
- **Real-time onboard**: Runs on embedded platforms (Jetson Orin AGX)

## Relationship to VLN

WildOS extends [[vision_and_language_navigation|Vision-Language Navigation (VLN)]] from indoor structured environments to unstructured outdoor terrains. Unlike indoor VLN systems that rely on pre-built maps and discrete action spaces, WildOS builds its own sparse topological map online and reasons about traversability and object presence in real-time.

## Datasets

- WildOS Dataset available on HuggingFace
- Field experiments across diverse off-road and urban terrains

## See Also

- [[wildos|WildOS Algorithm]] — Detailed algorithm description
- [[wildos_open_vocabulary_object_search_in_the_wild|WildOS Paper]] — Paper entity page
- [[vision_and_language_navigation|Vision-Language Navigation]]
- [[object_goal_navigation|Object-Goal Navigation]]
- Outdoor Navigation
