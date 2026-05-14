---
id: claude_pace
type: concept
title: claude-pace
tags:
- bash
- jq
- statusline
- rate-limiting
- claude-code
confidence: 0.65
created_at: '2026-05-14'
last_reinforced: '2026-05-14'
sources:
- https://github.com/Astro-Han/claude-pace
section: Status Lines > General
---

> A lightweight Bash + jq statusline for Claude Code that displays rate limit pace delta (burn rate vs. time remaining), 5h/7d usage percentage, context window usage, git branch and diff stats. Compares current consumption rate against time remaining in each rate limit window to indicate whether quota is being used faster or slower than the window allows. Single file with no external dependencies beyond jq.

claude-pace is a lightweight Bash and jq statusline tool designed for Claude Code. It displays real-time rate limit pace by comparing current consumption against time remaining in each window. The tool also shows usage percentages over 5-hour and 7-day windows, context window usage, and git branch/diff stats. It is a single file with no external dependencies beyond jq, making it easy to integrate into Claude Code workflows.

**Category:** Status Lines > General
**Source:** [https://github.com/Astro-Han/claude-pace](https://github.com/Astro-Han/claude-pace)
