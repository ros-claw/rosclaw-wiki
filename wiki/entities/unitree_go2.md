---
id: unitree_go2
title: Unitree Go2
type: entity
tags: []
confidence: 0.95
created_at: '2026-04-29T21:00:19'
last_reinforced: '2026-04-30'
supersedes: []
sources:
- papers/2410.06239.pdf
- papers/2507.06747.pdf
source_type: arxiv_paper
---

# Unitree Go2

The **Unitree Go2** is a legged quadruped robot manufactured by **Unitree**, designed for agile locomotion and integrated with onboard sensing and real-time control capabilities. In the context of the Real-Time Autonomous Navigation System ⚠️ ⚠️, it serves as the physical carrier for an open-architecture navigation stack, with all components communicating over ROS2. When augmented with the LOVON framework, the Go2 also achieves long-range object navigation in dynamic environments, and provides a plug-and‑play platform for open‑vocabulary object navigation. The platform supports zero-shot navigation, enabling operation in previously unseen environments without task‑specific training.

## Platform Overview

The Unitree Go2 legged quadruped robot is used as the physical platform for the open-architecture navigation system. Manufactured by Unitree, it integrates multiple onboard components that communicate via ROS2, enabling robust and low‑latency control for autonomous navigation tasks. The Go2 serves as a test platform for the LOVON framework, which can be deployed in a plug‑and‑play manner without requiring platform‑specific modifications.

## Capabilities

- **Quadruped Locomotion** – The Go2 can perform walking, trotting, and dynamic gaits over varied terrain.
- **Onboard Sensing** – It carries proprioceptive (joint encoders, IMU) and exteroceptive sensors (e.g., depth cameras, LiDAR) to perceive its environment.
- **Real‑Time Control** – The robot’s control loops run at frequencies sufficient for reactive navigation and obstacle avoidance, made possible by ROS2’s real‑time capabilities.
- **Real‑World Autonomous Navigation** – The Go2 is capable of long‑term autonomous navigation in unknown dynamic environments, including indoor spaces and cluttered settings.
- **Zero‑Shot Navigation** – The robot can navigate previously unseen environments without task‑specific fine‑tuning, relying on general‑purpose perception and planning modules.
- **Long‑Range Object Navigation** – When integrated with the LOVON framework, the Go2 can perform long-range object navigation in dynamic environments, leveraging learned visual representations and reactive planning.
- **Open‑Vocabulary Object Navigation** – As a test platform for the LOVON framework, the Go2 enables plug‑and‑play open‑vocabulary object navigation, allowing navigation to any object described in natural language without prior training.

## Performance

The Real-Time Autonomous Navigation System ⚠️ ⚠️ deployed on the Unitree Go2 achieved over **88% task success** in real‑world indoor environments, demonstrating robust zero-shot generalization and reliable obstacle avoidance under time‑critical conditions. In LOVON experiments, the Go2 also demonstrated successful long‑range object navigation in unseen dynamic environments.

## Relationships

- **uses** ROS2 – The Unitree Go2 depends on ROS2 for inter‑component messaging, node management, and timing‑critical control.
- **uses** LLM‑based Planner ⚠️ – The navigation system incorporates a large‑language‑model‑based planner for high‑level decision‑making and object‑goal reasoning.
- **uses** LOVON – The Go2 can be integrated with the LOVON framework to enable long-range object navigation in dynamic settings; the framework is plug‑and‑play compatible.
- **used_in** LOVON experiments ⚠️ – The Go2 served as the primary robotic platform for evaluating the LOVON framework in real‑world trials.

## Onboard Sensors

While the exact sensor suite may vary by configuration, the Unitree Go2 supports a range of exteroceptive sensors (e.g., Intel RealSense depth cameras, Livox LiDAR) that feed into the navigation pipeline. All sensor data is published over ROS2 topics.

## Source

This page is based on the arxiv papers **2410.06239** (Real-Time Autonomous Navigation System) and **2507.06747** (LOVON framework for long-range object navigation), both deployed on the Unitree Go2.