---
id: extreme_parkour_with_legged_robots
title: Extreme Parkour with Legged Robots
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-29T21:44:30'
last_reinforced: '2026-04-29T21:44:30'
supersedes: []
sources:
- papers/2309.14341.pdf
source_type: arxiv_paper
---

## Overview

**Extreme Parkour with Legged Robots** is a research area within [[Parkour Robotics]] ⚠️ ⚠️ that focuses on enabling small, low-cost legged robots to traverse highly dynamic obstacles with precise eye-muscle coordination and movement. It demonstrates that a learning-based approach can overcome the limitations of imprecise actuation and noisy perception, achieving agile locomotion in unstructured environments.

## Definition

Parkour for legged robots involves traversing obstacles in a **highly dynamic** fashion, requiring **precise eye-muscle coordination and movement**. This contrasts with traditional quasi-static or conservative locomotion methods.

## Challenges

Classically, parkour for legged robots required engineering perception, actuation, and control to very low tolerances—a brittle and expensive process. The work presented in this source paper (arXiv:2309.14341) shows that a learning-based approach can overcome imprecise hardware, such as small low-cost robots with low-quality sensors, by training policies in simulation and transferring them to the real world via [[Sim-to-Real Transfer]].

## Key Parameters

- **Difficulty**: Highly dynamic, requiring rapid, coordinated actions.
- **Perception**: Relies on a single front-facing depth camera that is low-frequency, jittery, and prone to artifacts.
- **Robot type**: Small, low-cost legged robot with imprecise actuation.
- **Required coordination**: Precise eye-muscle coordination and movement (i.e., tight coupling between vision and motor control).

## Techniques Used

This approach **uses**:

- [[Neural Net Parkour Policy]]: A learned policy that maps noisy depth images directly to motor commands, enabling agile obstacle negotiation.
- [[Sim-to-Real Transfer]]: Training the policy entirely in simulation and deploying it on real hardware without fine-tuning, despite the simulator–reality gap.

## Relation to Broader Field

Extreme Parkour with Legged Robots is a subfield **part of** [[Parkour Robotics]] ⚠️ ⚠️, which studies agile, athletic locomotion for legged robots. It complements other work on stair climbing, gap jumping, and obstacle courses.

## References

The core findings are documented in the paper *Extreme Parkour with Legged Robots* (arXiv:2309.14341), available in the source repository.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Pending review:**
- `Extreme Parkour with Legged Robots` --[[related_to]] ⚠️--> `Neural Net Parkour Policy` _(wikilink)_
