---
id: trevin_creator_autoresearch_mlx
type: concept
title: trevin-creator/autoresearch-mlx
tags:
- mlx
- apple-silicon
- machine-learning
- port
- efficient
confidence: 0.65
created_at: '2026-05-13'
last_reinforced: '2026-05-13'
sources:
- https://github.com/trevin-creator/autoresearch-mlx
section: 💻 Platform ports and hardware forks
---

> ![GitHub stars](https://img.shields.io/github/stars/trevin-creator/autoresearch-mlx?style=social) - MLX-native Apple Silicon port that keeps the upstream fixed-budget `val_bpb` loop while removing the PyTorch/CUDA dependency entirely.

This project is an MLX-native port of the upstream AutoResearch codebase, optimized exclusively for Apple Silicon hardware. It removes all PyTorch and CUDA dependencies while preserving the original fixed-budget validation bits-per-byte (val_bpb) training loop. Researchers can now run efficient machine learning experiments on Macs without any GPU configuration or CUDA toolchain, leveraging Apple's Metal Performance Shaders through MLX.

**Category:** 💻 Platform ports and hardware forks
**Source:** [https://github.com/trevin-creator/autoresearch-mlx](https://github.com/trevin-creator/autoresearch-mlx)
