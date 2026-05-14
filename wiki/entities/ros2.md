---
id: ros2
title: ROS2
type: entity
tags: []
confidence: 0.8
created_at: '2026-04-30T01:07:27'
last_reinforced: '2026-04-30T01:07:27'
supersedes: []
sources:
- papers/2410.06239.pdf
source_type: arxiv_paper
---

# ROS2

**ROS2** (Robot Operating System 2) is a middleware framework designed for robotics software development. It enables real-time communication between onboard components, providing a modular, distributed architecture for building complex robotic systems. ROS2 is the successor to ROS1 and is built on top of DDS ⚠️ (Data Distribution Service) for deterministic, low‑latency messaging.

## Capabilities

- **Real‑time communication** between sensing, control, and actuation subsystems.
- **Integration** of localization ⚠️, mapping ⚠️, and planning ⚠️ modules into a cohesive pipeline.
- Support for multiple programming languages (C++, Python) and cross‑platform deployment.

## Relationships

- **Unitree Go2** uses ROS2 as its primary middleware for bridging the onboard Jetson Orin ⚠️ to low‑level motor controllers and high‑level planning stacks.
- ROS2 depends on ROS2 Humble ⚠️ (or later) for the specific distribution used in the Unitree stack.
- Common complementary tools include Nav2 ⚠️ for navigation and Cartographer ⚠️ for SLAM.

## Notes

The version of ROS2 referenced in the source (arxiv:2410.06239) is not explicitly specified but is assumed to be **ROS2 Humble** or a later LTS release, consistent with current Unitree software support.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `ROS2` --depends_on ⚠️--> `Unitree Go2`
