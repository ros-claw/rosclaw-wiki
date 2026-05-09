---
id: matterport3d_simulator
title: Matterport3D Simulator
type: entity
tags: []
confidence: 1.0
created_at: '2026-04-29T21:52:51'
last_reinforced: '2026-04-30'
supersedes: []
sources:
- code/peteanderson80_Matterport3DSimulator/README.md
source_type: official_manual
---

# Matterport3D Simulator

The **Matterport3D Simulator** is a high-performance, photorealistic 3D environment simulator designed for embodied AI research. Built atop the [[Matterport3D Dataset]], it provides an interactive, traversal-based simulation of 90 real-world indoor environments with densely sampled 360° RGB-D panoramas. The simulator is used for training and evaluating navigation agents in deep reinforcement learning, vision-and-language navigation, and robotics research.

## Overview

A simulator for AI agents to interact with real 3D indoor environments using RGB-D images. It outputs real (not synthetic) RGB and depth images, offering high-fidelity visual input for learning. Fully Dockerized, it supports batching multiple agents in parallel for efficient training.

## Parameters

| Parameter | Value |
|-----------|-------|
| Default resolution | 640×480 pixels (customizable) |
| Rendering speed | ~1000 fps with RGB-D off-screen rendering on Titan X GPU |
| Average viewpoint spacing | 2.25 m |
| Number of environments | 90 |
| Image type | RGB-D (color + depth) |
| Batch support | Yes |
| Depth output | Yes |
| Available actions | `pan camera`, `elevate camera`, `move between viewpoints` |

## Capabilities

- Outputs **real (not synthetic)** RGB and depth images, offering high-fidelity visual input for learning.
- Customizable image resolution and camera intrinsic parameters.
- Supports **off-screen rendering** via GPU (EGL), CPU (OSMesa), or OpenGL with an X server.
- Provides a dual **C++** and **Python** API for flexible integration.
- Includes comprehensive unit tests for the rendering pipeline and agent motions.
- Fully **Dockerized**, with support for batching multiple agents in parallel.

## Dataset

The simulator is based on the [[Matterport3D Dataset]], which consists of 90 indoor environments including homes, offices, churches, and hotels. Each environment contains densely sampled 360° RGB-D images, with between 8 and 349 viewpoints per environment.

## Room-to-Room (R2R) Navigation Task

The simulator ships with the **Room-to-Room (R2R)** benchmark, a standard task in embodied AI where an agent must follow a natural language navigation instruction to reach a goal in a previously unseen building. Results are tracked on the [[EvalAI]] ⚠️ leaderboard.

## Installation

Recommended installation is via Docker; requires an [[Nvidia GPU]] ⚠️ ⚠️ ⚠️ and [[nvidia-docker]] ⚠️ 2.0. Build the simulator with CMake, choosing the rendering option (EGL recommended for speed). Dependencies include [[CUDA]] ⚠️ ⚠️, [[OpenGL]] ⚠️ ⚠️ ⚠️/[[EGL]] ⚠️ ⚠️/[[OSMesa]] ⚠️ ⚠️, [[OpenCV]] ⚠️ ⚠️, and a [[C++11 compiler]] ⚠️ ⚠️.

## Dataset Preprocessing

Preprocess the Matterport3D Dataset for use with the simulator:
- Downscale skybox images using `scripts/downsize_skybox.py`.
- Optionally generate depth skyboxes via `scripts/depth_to_skybox.py`.

## Interactive Demo

After building the simulator, you can run an interactive demo:
- **Python**: `python3 src/driver/driver.py`
- **C++**: `build/mattersim_main`

## Relationships

- **Uses**: [[Matterport3D Dataset]], [[Docker]] ⚠️ ⚠️, [[Nvidia GPU]] ⚠️ ⚠️ ⚠️, [[CMake]] ⚠️, [[OpenCV]] ⚠️ ⚠️, [[OpenGL]] ⚠️ ⚠️ ⚠️
- **Depends on**: [[Nvidia GPU]] ⚠️ ⚠️ ⚠️ with driver ≥ 396.37, [[CUDA]] ⚠️ ⚠️, [[OpenGL]] ⚠️ ⚠️ ⚠️/[[EGL]] ⚠️ ⚠️/[[OSMesa]] ⚠️ ⚠️, [[Docker]] ⚠️ ⚠️, [[nvidia-docker2.0]] ⚠️, [[C++11 compiler]] ⚠️ ⚠️