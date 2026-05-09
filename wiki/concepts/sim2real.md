---
id: sim2real
title: Sim2Real
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-30T01:28:37'
last_reinforced: '2026-04-30T01:28:37'
supersedes: []
sources:
- papers/2402.15852.pdf
source_type: arxiv_paper
---

# Sim2Real

**Sim2Real** (Simulation to Reality) refers to the process of transferring machine learning policies, control strategies, or entire robot behaviors from a simulated environment to a real-world physical system. It is a fundamental challenge in embodied AI and robotics because simulations introduce idealized physics, perfect sensors, and noiseless actuators that rarely match the complexity of the real world.

## Key Concept

The core difficulty of Sim2Real is bridging the *reality gap*—the discrepancy between simulated and real-world dynamics, perception, and embodiment. Successful Sim2Real transfer often requires techniques such as domain randomization, domain adaptation, or policy distillation to make the learned behavior robust enough to generalize to a physical robot.

## Challenges

### Gap Sources

Traditional Sim2Real approaches rely on map or depth inputs, which can introduce significant transfer gaps due to differences in sensor fidelity, lighting, or scene geometry. The video-only approach of [[NaVid]] eliminates these gaps entirely, enabling a more direct and robust transfer from simulation to reality.

## Approaches

One notable advancement in Sim2Real is the work of NaVid, a vision-language navigation policy that demonstrates **superior Sim2Real transfer** without requiring depth or map information. NaVid is a key mitigator of the Sim2Real gap (*is mitigated by [[NaVid]]*), showing that careful design of input modalities and training procedures can dramatically reduce the obstacles to real-world deployment.

## Relationships

- **Depends on**: [[Domain Randomization]] ⚠️, [[Domain Adaptation]] ⚠️
- **Is mitigated by**: [[NaVid]]
- **Related concepts**: [[Embodied AI]], [[Sim-to-Real Gap]] ⚠️, [[Reality Gap]] ⚠️

---

*For further reading, see the paper: "NaVid: Video-based Language Navigation for Real-World Robots" (arXiv 2402.15852).*

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Sim2Real` --[[related_to]] ⚠️ ⚠️--> `Embodied AI`
**Pending review:**
- `Sim2Real` --[[related_to]] ⚠️ ⚠️--> `NaVid` _(wikilink)_
