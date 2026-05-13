---
id: ralph_wiggum_as_a_software_engineer
type: concept
title: Ralph Wiggum as a Software Engineer
tags:
- harness
- autonomous-coding
- prompt-engineering
- subagent
- loop
confidence: 0.65
created_at: '2026-05-13'
last_reinforced: '2026-05-13'
sources:
- https://ghuntley.com/ralph/
section: Runtimes, Harnesses & Reference Implementations
---

> Geoffrey Huntley's write-up of "Ralph," a minimalist `while :; do cat PROMPT.md | claude-code; done` harness pattern that uses single-task loops, deterministic prompt stacking, and bounded subagent parallelism to drive long-running autonomous coding.

Ralph is a minimalist harness pattern for running long-running autonomous coding tasks. It uses a simple while loop that repeatedly feeds a prompt to Claude Code. The pattern employs deterministic prompt stacking and bounded subagent parallelism to manage complexity. This approach is designed to enable sustained coding sessions without manual intervention. The concept is documented by Geoffrey Huntley as a reference implementation.

**Category:** Runtimes, Harnesses & Reference Implementations
**Source:** [https://ghuntley.com/ralph/](https://ghuntley.com/ralph/)
