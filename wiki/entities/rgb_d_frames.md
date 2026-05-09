---
id: rgb_d_frames
title: RGB-D frames
type: entity
tags: []
confidence: 0.8
created_at: '2026-04-30T00:46:30'
last_reinforced: '2026-04-30T00:46:30'
supersedes: []
sources:
- papers/2507.04047.pdf
source_type: arxiv_paper
---

# RGB-D Frames

**RGB-D frames** are a type of sensor data that simultaneously capture color (RGB) and depth (D) information from a scene. Each frame contains two aligned modalities: a standard 2D RGB image and a per-pixel depth map, enabling rich perception of 3D geometry and appearance.

## Modalities
- **RGB**: Color image with three channels (red, green, blue), typically captured by an optical camera.
- **Depth**: A single-channel distance map where each pixel encodes the distance from the camera to the corresponding surface point in the scene.

## Capabilities
The use of RGB-D frames enables:
- **Online query-based representation learning** – A system can learn representations on the fly by querying specific regions or objects within the stream of frames.
- **Direct spatial memory construction without explicit 3D reconstruction** – Instead of building a full dense mesh or point cloud, the system can organize spatial knowledge directly from the frames, often via learned embeddings or spatial indexing.

## Relationships
- Used by **[[MTU3D]]** *(uses)* — MTU3D leverages RGB-D frames to perform online query-based representation learning and spatial memory construction.

> **See also:** [[Spatial Memory]] ⚠️, [[Representation Learning]] ⚠️, [[3D Reconstruction]] ⚠️