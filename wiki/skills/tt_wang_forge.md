---
id: tt_wang_forge
type: entity
title: TT-Wang/forge
tags:
- mcp-server
- coding-agents
- structured-planning
- parallel-execution
- validation
confidence: 0.65
created_at: '2026-05-13'
last_reinforced: '2026-05-13'
sources:
- https://github.com/TT-Wang/forge
section: Server Implementations > 🤖 <a name="coding-agents"></a>Coding Agents
---

> [![forge MCP server](https://glama.ai/mcp/servers/TT-Wang/forge/badges/score.svg)](https://glama.ai/mcp/servers/TT-Wang/forge) 📇 🏠 🍎 🪟 🐧 - Structured planning, parallel execution in git worktrees, and deep validation for Claude Code. Turns a one-line objective into a validated DAG of modules executed by worker agents, each self-checked and cross-module-reviewed before merge-back. 7 MCP tools: `validate`, `validate_plan`, `memory_recall`, `memory_save`, `iteration_state` (per-run scoped, with stagnation/velocity/oscillation detection), `forge_logs`, `session_state`. Stdio-only. Zero telemetry.

Forge is an MCP server that enhances Claude Code by turning simple objectives into structured, executable plans. It uses a directed acyclic graph (DAG) of modules, executed by worker agents in parallel using git worktrees. Each module is self-checked and cross-reviewed before being merged, ensuring deep validation. The server provides seven MCP tools for validation, planning, memory, iteration state detection (including stagnation and oscillation), log retrieval, and session management. It runs via stdio with no telemetry.

**Category:** Server Implementations > 🤖 <a name="coding-agents"></a>Coding Agents
**Source:** [https://github.com/TT-Wang/forge](https://github.com/TT-Wang/forge)
