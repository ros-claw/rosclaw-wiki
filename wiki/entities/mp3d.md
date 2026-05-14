---
id: mp3d
title: MP3D
type: entity
tags: []
confidence: 0.8
created_at: '2026-04-30T00:02:53'
last_reinforced: '2026-04-30T00:02:53'
supersedes: []
sources:
- papers/2505.23019.pdf
source_type: arxiv_paper
---

# MP3D

**MP3D** is a multi-floor, object-goal navigation benchmark used for evaluating embodied AI agents. It provides a set of photorealistic, large-scale indoor environments from the Matterport3D dataset, adapted for the task of navigating to specified target objects across different floors and rooms.

MP3D is designed to test an agent's ability to understand spatial layouts, generalize across floor plans, and perform long-horizon navigation with occlusion and partial observability. It is commonly used as an evaluation standard for visual navigation policies.

## Key Properties

- **Type**: Object-goal navigation benchmark
- **Environment**: Multi-floor, indoor scenes
- **Task**: Navigate to a target object category (e.g., "chair", "bed") using only egocentric observations

## Usage

MP3D has been employed in the evaluation of ASCENT, a navigation framework that learns adaptive skill composition. In that work, MP3D serves as a challenging testbed to measure generalization across unseen buildings and floor transitions.

## Related Concepts

- Object Goal Navigation — the general task that MP3D evaluates
- Embodied AI — the broader research domain
- Matterport3D ⚠️ — the underlying dataset of 3D scans
- Sim-to-Real Transfer — relevant for evaluating whether policies trained on MP3D generalize to real robots

## See Also

- ASCENT — uses MP3D for evaluation (`used_in` → ASCENT)
- Habitat Simulator — often used to run MP3D episodes
- PointNav vs ObjectNav ⚠️ — comparison of navigation benchmarks

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `MP3D` --uses ⚠️--> `ASCENT`
- `MP3D` --related_to ⚠️--> `Embodied AI`
