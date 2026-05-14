---
id: pinhole_camera_projection_model
title: Pinhole Camera Projection Model
type: concept
tags: []
confidence: 0.8
created_at: '2026-04-30T02:54:01'
last_reinforced: '2026-04-30T02:54:01'
supersedes: []
sources:
- papers/1806.00047.pdf
source_type: arxiv_paper
---

# Pinhole Camera Projection Model

The **Pinhole Camera Projection Model** is a foundational geometric model in computer vision that maps 3D world points to 2D image coordinates. It assumes a single viewpoint and rectilinear projection, meaning straight lines in the world remain straight in the image. This model is widely used for visual sensor modeling, camera calibration, and 3D reconstruction.

## Description

A camera model that assumes a single viewpoint and rectilinear projection, used within Grounded Semantic Mapping Network (GSMN) to compute local-to-world transformations.

## Capabilities

- Maps 3D world points to 2D image coordinates
- Provides geometric transformation for visual sensor modeling

## Relationships

- **used_by**: Grounded Semantic Mapping Network (GSMN) – employs the pinhole model to project visual observations into a consistent world coordinate frame for semantic mapping.

## Key Properties

- **Single viewpoint**: All rays pass through a single optical center.
- **Rectilinear projection**: Straight lines in 3D project to straight lines in 2D.
- **Mathematical formulation**: Typically expressed as \( \mathbf{x} = K [R|\mathbf{t}] \mathbf{X} \), where \( K \) is the intrinsic matrix, \( [R|\mathbf{t}] \) is the extrinsic matrix, and \( \mathbf{X} \) is a 3D point in homogeneous coordinates.

## Source

This page is derived from the paper *1806.00047*, which describes the Grounded Semantic Mapping Network (GSMN) and its use of the pinhole camera model for projection.

### 自动链接关系
_These relationships were discovered automatically by the heuristic entity linker._
**Pending review:**
- `Pinhole Camera Projection Model` --related_to ⚠️--> `Grounded Semantic Mapping Network (GSMN)` _(wikilink)_
