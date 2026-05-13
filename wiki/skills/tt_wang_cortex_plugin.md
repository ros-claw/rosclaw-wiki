---
id: tt_wang_cortex_plugin
type: concept
title: TT-Wang/cortex-plugin
tags:
- mcp-server
- memory
- knowledge-management
- obsidian
- claude
confidence: 0.65
created_at: '2026-05-13'
last_reinforced: '2026-05-13'
sources:
- https://github.com/TT-Wang/cortex-plugin
section: Server Implementations > 🧠 <a name="knowledge--memory"></a>Knowledge & Memory
---

> [![cortex-plugin MCP server](https://glama.ai/mcp/servers/TT-Wang/cortex-plugin/badges/score.svg)](https://glama.ai/mcp/servers/TT-Wang/cortex-plugin) 🐍 🏠 🍎 🐧 - Persistent, self-evolving memory plugin for Claude Code. Background miner extracts durable lessons (decisions, conventions, bug fixes) from completed sessions via Claude Haiku, stores them as human-readable markdown in an Obsidian vault, and assembles query-tailored context briefings at session start. Local-first, no cloud, no API keys. Self-healing install via uv bootstrap shim, `/cortex-doctor` preflight, graceful FTS-only degraded mode when `claude` CLI missing. MIT.

This is a Model Context Protocol (MCP) server that provides persistent, self-evolving memory for Claude Code. It runs a background miner that extracts durable lessons—such as decisions, conventions, and bug fixes—from completed sessions using Claude Haiku. The extracted knowledge is stored as human-readable markdown files in an Obsidian vault. At the start of each session, it assembles query-tailored context briefings to improve Claude's performance. The system is local-first, requiring no cloud services or API keys, and includes self-healing installation and graceful degradation when the Claude CLI is missing.

**Category:** Server Implementations > 🧠 <a name="knowledge--memory"></a>Knowledge & Memory
**Source:** [https://github.com/TT-Wang/cortex-plugin](https://github.com/TT-Wang/cortex-plugin)
