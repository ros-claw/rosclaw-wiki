---
id: quadruped_robot
title: Quadruped Robot
type: entity
tags: []
confidence: 1.0
created_at: '2026-04-30T00:03:31'
last_reinforced: '2026-04-30'
supersedes: []
sources:
- papers/2505.23019.pdf
- papers/2511.17889.pdf
- papers/2502.19024.pdf
- papers/2602.18424.pdf
- papers/2210.14791.pdf
source_type: arxiv_paper
---

# Quadruped Robot

A Quadruped Robot is a legged robotic platform with four limbs capable of dynamic locomotion and navigation over rough terrain. In the ASCENT project, it serves as the physical deployment platform for validating embodied AI and control algorithms; in the MobileVLA-R1 framework, it grounds natural‑language instructions into continuous control via a Vision‑Language‑Action (VLA) model; and in the ViNL system, it acts as a generic platform for learning visual navigation and locomotion policies from egocentric camera input. Due to its low‑height construction, the quadruped provides a ground‑level field of view that is particularly well‑suited for close‑range perception tasks such as visual language navigation (VLN). Its legged mobility also enables traversal of stairs and other structured obstacles, offering more versatile movement than wheeled robots.

## Parameters

- **Locomotion type**: legged  
- **Number of legs**: 4  
- **Field of view**: low‑height (ground‑level)  
- **Vision sensor**: egocentric camera (commonly an onboard RGB camera)  
- **Can traverse stairs**: yes  

## Capabilities

- **Real‑world deployment platform**: The quadruped robot is employed in practical, outdoor, and unstructured environments to validate embodied AI and control algorithms. It provides a mobile base for sensor suites, computing payloads, and manipulation appendages.  
- **Ground locomotion**: Stable locomotion over varied terrain (e.g., grass, gravel, slopes).  
- **Autonomous navigation and obstacle avoidance**: Navigates through unknown environments while avoiding obstacles.  
- **Stair traversal**: Capable of ascending and descending stairs, enabling operation in multi‑level environments.  
- **Versatile mobility**: Legged locomotion provides superior terrain adaptability compared to wheeled robots, allowing navigation over obstacles, stairs, and uneven ground.  
- **Natural language grounding**: Translates natural‑language instructions into continuous motor commands, enabling intuitive human‑robot interaction.  
- **Real‑world visual language navigation (VLN) with GVNav**: The robot can perform VLN tasks using the GVNav framework, leveraging its low‑height viewpoint for ground‑level scene understanding.  
- **Indoor navigation and small‑obstacle stepping**: In the ViNL system, the robot walks and navigates indoors while stepping over small obstacles, guided by a learned navigation and locomotion policy.

## Relationships

- **used_in**: This robot platform is integrated into the ASCENT deployment ⚠️ system, the MobileVLA‑R1 ⚠️ ⚠️ ⚠️ ⚠️ framework, the GVNav navigation pipeline, the Capability‑Conditioned Navigation (CapNav) ⚠️ ⚠️ ⚠️ ⚠️ ⚠️ framework, and the ViNL visual navigation and locomotion system.  

- **platform_for**:
  - Visual Navigation Policy – learned policy that steers the robot through known and unknown environments.
  - Visual Locomotion Policy ⚠️ ⚠️ – learned policy that controls gait and foot placement to follow navigation commands while avoiding small obstacles.

- **example_in**: Capability‑Conditioned Navigation (CapNav) ⚠️ ⚠️ ⚠️ ⚠️ ⚠️ — the quadruped serves as an exemplar for capabilities such as stair traversal and versatile terrain adaptation.

- **depends_on**: The robot’s operation depends on ROS 2 ⚠️ middleware, sensor drivers, and low‑level locomotion controllers (e.g., quadruped gait controller ⚠️). It may also rely on onboard compute hardware such as a NVIDIA Jetson ⚠️ or similar edge device. In the ViNL system, an egocentric camera ⚠️ provides visual input for learning policies.

- **implements**: The robot implements the hardware abstraction layer required by the ASCENT stack, providing odometry, state estimation, and actuator interfaces. For MobileVLA‑R1 ⚠️ ⚠️ ⚠️ ⚠️, it implements the physical embodiment that closes the Vision‑Language‑Action loop. For GVNav, it provides the mobile base and low‑height viewpoint for environment perception. For Capability‑Conditioned Navigation (CapNav) ⚠️ ⚠️ ⚠️ ⚠️ ⚠️, it demonstrates how legged capabilities (e.g., stair climbing) can be conditioned upon during navigation planning. For ViNL, it implements the physical platform for training and deploying visual navigation and locomotion policies.

- **uses**:  
  - MobileVLA‑R1 ⚠️ ⚠️ ⚠️ ⚠️ — the robot acts as the physical platform for the VLA control pipeline.  
  - Vision‑Language‑Action ⚠️ ⚠️ — the robot’s sensorimotor system enables the translation of visual and linguistic inputs into actions.  
  - GVNav — the robot executes real‑world VLN trajectories using GVNav’s navigation policies.  
  - Capability‑Conditioned Navigation (CapNav) ⚠️ ⚠️ ⚠️ ⚠️ ⚠️ — the robot provides the legged mobility substrate for studying capability‑aware navigation.  
  - ViNL — the robot serves as the generic platform for learning visual navigation and locomotion policies from egocentric camera observations.

- **used_by**: ViNL

- **related_to**:  
  - **low‑height viewpoint** — the robot’s ground‑level perspective is a defining characteristic that influences perception algorithms and navigation strategies, particularly for VLN tasks with close‑range semantic cues.  
  - **stair‑traversal capability** — the ability to traverse stairs distinguishes legged quadrupeds from wheeled platforms and enables multi‑floor operation.  
  - **egocentric camera** — an onboard camera providing first‑person visual input used by ViNL and other learning‑based frameworks.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Confirmed links:**
- `Quadruped Robot` --uses ⚠️ ⚠️ ⚠️--> `ASCENT`
- `Quadruped Robot` --depends_on ⚠️--> `Unitree G1`
- `Quadruped Robot` --uses ⚠️ ⚠️ ⚠️--> `MobileVLA-R1`
- `Quadruped Robot` --uses ⚠️ ⚠️ ⚠️--> `Vision-Language-Action`
- `Quadruped Robot` --used_by ⚠️--> `ViNL`

## Related Pages

- ASCENT — the overall system into which this robot is integrated.  
- Quadruped Locomotion ⚠️ — algorithmic principles governing gait and balance.  
- Sim‑to‑Real Transfer ⚠️ — methods used to transfer policies trained in simulation to this hardware.  
- Unitree G1 — an example commercial quadruped often used in research (if applicable; otherwise remove).  
- MobileVLA‑R1 ⚠️ ⚠️ ⚠️ ⚠️ — a VLA framework that uses this robot as the deployment platform.  
- Vision‑Language‑Action ⚠️ ⚠️ — the model family that grounds language into continuous control.  
- GVNav — a navigation framework for real‑world visual language navigation.  
- Capability‑Conditioned Navigation (CapNav) ⚠️ ⚠️ ⚠️ ⚠️ ⚠️ — a framework that uses capability awareness (e.g., stair traversal) for navigation.  
- Low‑Height Viewpoint ⚠️ — the perceptual perspective inherent to quadruped platforms.  
- ViNL — a system for learning visual navigation and locomotion policies with egocentric vision.  
- Egocentric Camera ⚠️ — the typical vision sensor onboard the robot.  
- Visual Navigation Policy — a learned policy that drives the robot through environments.  
- Visual Locomotion Policy ⚠️ ⚠️ — a learned policy that controls gait and obstacle crossing.

> **Sources**: Arxiv paper 2505.23019 (ASCENT deployment), arxiv paper 2511.17889 (MobileVLA‑R1), arxiv paper 2502.19024 (GVNav), arxiv paper 2602.18424 (CapNav), and arxiv paper 2210.14791 (ViNL). See `data/raw/papers/2505.23019.pdf`, `data/raw/papers/2511.17889.pdf`, `data/raw/papers/2502.19024.pdf`, `data/raw/papers/2602.18424.pdf`, and `data/raw/papers/2210.14791.pdf`.