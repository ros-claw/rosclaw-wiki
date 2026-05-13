---
id: context_mode
type: concept
title: context-mode
tags:
- context-compression
- sandboxing
- subprocesses
- developer-productivity
- llm-plugin
confidence: 0.65
created_at: '2026-05-13'
last_reinforced: '2026-05-13'
sources:
- https://github.com/mksglu/claude-context-mode
section: Plugins > Developer Productivity
---

> Process large outputs in sandboxed subprocesses, keeping only summaries in the context window. 98% context savings across 21 benchmarked scenarios.

Context-mode is a developer plugin that processes large outputs in sandboxed subprocesses, extracting only summaries to conserve context window space. It achieves 98% context savings across 21 benchmarked scenarios, dramatically reducing token usage for large outputs. By isolating execution in subprocesses, it ensures safety while maintaining key information from large results. This tool is particularly useful for AI-assisted coding where limited context windows need to handle large outputs efficiently.

**Category:** Plugins > Developer Productivity
**Source:** [https://github.com/mksglu/claude-context-mode](https://github.com/mksglu/claude-context-mode)
