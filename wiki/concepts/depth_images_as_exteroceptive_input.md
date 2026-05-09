---
id: depth_images_as_exteroceptive_input
title: Depth Images as Exteroceptive Input
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-30T04:11:01'
last_reinforced: '2026-04-30T04:11:01'
supersedes: []
sources:
- papers/2505.11164.pdf
source_type: arxiv_paper
---

## Depth Images as Exteroceptive Input

Depth images are a form of exteroceptive sensing that provide per-pixel distance measurements from a [[Depth Camera]] ⚠️ ⚠️ to objects in the environment. In the context of legged locomotion, depth images enable the policy to perceive the geometry of the terrain ahead, allowing reactive and anticipatory adjustments during movement. They serve as the primary perception input for terrain navigation, especially in unstructured outdoor environments where foot placement and body posture must adapt continuously.

### Sensor Role

- **Sensor type**: [[Depth Camera]] ⚠️ ⚠️
- **Role**: Perception for terrain navigation

The depth camera captures a 2.5D representation of the surroundings, which is fed into the control policy as a visual observation. This allows the agent to build a spatial understanding of the ground surface, obstacles, and slopes without relying on explicit mapping or semantic labels.

### Capabilities

- **Robust navigation across unstructured terrains**: Depth images provide the necessary exteroceptive information for a policy to traverse rocks, grass, gravel, stairs, and other irregular surfaces. By reacting to local depth changes, the agent can maintain stability and avoid footholds that would cause slippage or tipping.

### Importance

Depth images provide exteroceptive information allowing the policy to perceive and react to terrain. Without this input, the agent would be blind to upcoming ground features and would rely solely on proprioceptive feedback, which is insufficient for agile locomotion over challenging substrates.

### Relationships

- **Used by**:
  - [[Agile Locomotion]] – Policies trained for high-speed, dynamic locomotion leverage depth perception to preemptively adjust gait and posture.
  - [[ANYmal D]] – This quadruped platform integrates depth imagery as a core input for its locomotion controller, enabling autonomous deployment in rough terrain.

### See Also

- [[Exteroception]] ⚠️ – Broader concept of sensing the external environment.
- [[Sim-to-Real Transfer]] – Depth images are often rendered in simulation and transferred to real sensors via domain randomization.
- [[Terrain Classification]] ⚠️ – While depth images provide geometry, they can be combined with semantic labels for more informed decisions.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Depth Images as Exteroceptive Input` --[[applies_to]] ⚠️--> `ANYmal D`
