---
id: harness_evolver
type: concept
title: Harness Evolver
tags:
- claude-code-plugin
- llm-agent-harness
- multi-agent-evolution
- langsmith-evaluation
- git-worktree-isolation
confidence: 0.65
created_at: '2026-05-13'
last_reinforced: '2026-05-13'
sources:
- https://github.com/raphaelchristi/harness-evolver
section: Runtimes, Harnesses & Reference Implementations
---

> Claude Code plugin that autonomously evolves LLM agent harnesses using multi-agent proposers, LangSmith-backed evaluation, and git worktree isolation. Based on Meta-Harness (Lee et al., 2026).

The Harness Evolver is a plugin for Claude Code that automatically improves LLM agent harnesses. It uses multiple AI proposers to generate new harness designs and evaluates them with LangSmith monitoring. The plugin isolates each experiment using git worktrees to prevent conflicts. It is based on the Meta-Harness research from 2026. This tool allows autonomous iterative refinement of agent orchestration systems.

**Category:** Runtimes, Harnesses & Reference Implementations
**Source:** [https://github.com/raphaelchristi/harness-evolver](https://github.com/raphaelchristi/harness-evolver)
