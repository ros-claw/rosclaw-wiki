---
id: long_horizon_mobile_manipulation
title: Long-Horizon Mobile Manipulation
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-30T00:28:09'
last_reinforced: '2026-04-30T00:28:09'
supersedes: []
sources:
- papers/2508.08240.pdf
source_type: arxiv_paper
---

# Long-Horizon Mobile Manipulation

**Long-Horizon Mobile Manipulation** is a grand challenge in embodied AI that involves language-guided tasks requiring coordination between a mobile base and a manipulator over extended temporal and spatial horizons. It represents a frontier where robots must integrate perception, planning, and control to complete complex, dynamic tasks in open-world environments, often with minimal explicit supervision.

The ODYSSEY benchmark introduced the first structured evaluation for this scenario, providing a standardized suite of tasks that test the interplay of mobility and dexterity under natural language instructions.

## Challenges

The primary obstacles in long-horizon mobile manipulation include:

- **Constrained perception and limited actuation ranges** of mobile platforms, which restrict the robot's ability to sense and reach objects from a stationary posture.
- **Generalization to diverse object configurations** in open-world settings, where the same linguistic command may refer to arbitrarily arranged instances across different environments.
- **Dual requirement** of high maneuverability (e.g., navigating cluttered spaces) and precise end-effector control (e.g., grasping a small bottle), demanding tight coordination between the base and the arm.

These challenges are amplified by the long-horizon nature of the tasks, where errors in early steps compound and inference must be maintained over dozens of action primitives without resets.

## Capabilities

Despite the difficulty, mastering long-horizon mobile manipulation enables **complex, dynamic tasks in open-world environments** — such as fetching a medicine bottle from one room and pouring a drink in another — that are impossible for either a fixed manipulator or a mobile platform alone. It unlocks applications in household service, warehouse logistics, search-and-rescue, and eldercare.

## Related Concepts

- **[[Mobile Manipulation]] ⚠️** — The broad field combining mobility and manipulation; long-horizon tasks are a subset with extended temporal reasoning.
- **[[Whole-body Control]] ⚠️** — A key technical component that coordinates the mobile base and manipulator torques to achieve both stability and precision.
- **[[Language-Conditioned Tasks]] ⚠️** — The ability to interpret natural language commands and map them to action sequences over long horizons.

Additionally, the ODYSSEY benchmark builds on prior work in **[[Embodied AI]]** and **[[Sim-to-Real]] ⚠️** transfer, and its tasks are designed to be solved by **[[VLA Models]] ⚠️** (vision‑language‑action models) that handle both perception and motion planning.

## References

- ODYSSEY: A Benchmark for Long-Horizon Mobile Manipulation. (arXiv:2508.08240)

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Long-Horizon Mobile Manipulation` --[[related_to]] ⚠️--> `Embodied AI`
