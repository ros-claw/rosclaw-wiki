---
id: large_scale_path_planning
title: Large-Scale Path Planning
type: skill
tags: []
confidence: 0.8
created_at: '2026-04-29T21:46:25'
last_reinforced: '2026-04-29T21:46:25'
supersedes: []
sources:
- papers/2405.01792.pdf
source_type: arxiv_paper
---

## Large-Scale Path Planning

**Type**: Skill  
**Scale**: City-wide (kilometer-scale)  
**Method**: Global planning using topological maps or similar representations  

**Large-Scale Path Planning** is a high-level navigation skill that enables a robot to generate feasible routes through expansive, complex environments such as entire urban districts. It operates over a topological abstraction of the environment—compressing detailed geometric data into a graph of nodes and edges—so that the planning problem remains computationally tractable even at city scale.

### Capabilities

- **Plan kilometer-scale routes** through urban areas, including roads, sidewalks, plazas, and mixed‑use zones.
- **Avoid large static obstacles** (e.g., construction sites, permanent barriers) and respect **predefined no‑go zones** (e.g., restricted buildings, park areas).

### Relationships

- **Part of** Autonomous Navigation for Wheeled-Legged Robots — this skill is one of the key modules in the overall navigation stack for robots such as the Unitree G1 or similar platforms.
- **Supplies** Mobility-Aware Local Navigation Planning — the coarse route produced by large‑scale planning serves as the reference path for local planners, which then refine the trajectory while accounting for dynamic obstacles and terrain constraints.

### Integration

Provides a high-level route that the local planner follows, ensuring that the robot can complete long‑duration missions autonomously. The topological map is updated periodically to reflect changes in the environment (e.g., road closures), and the planner re‑routes as needed without requiring full recomputation.

**Source:** papers/2405.01792.pdf ⚠️  
**Reinforces:** *Confidence: 0.8* (peer‑reviewed paper)

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Large-Scale Path Planning` --[[operates_on]] ⚠️--> `Unitree G1`
**Pending review:**
- `Large-Scale Path Planning` --related_to ⚠️ ⚠️--> `Autonomous Navigation for Wheeled-Legged Robots` _(wikilink)_
- `Large-Scale Path Planning` --related_to ⚠️ ⚠️--> `Mobility-Aware Local Navigation Planning` _(wikilink)_
