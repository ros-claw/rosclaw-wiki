---
id: s60yucca_mnemos
type: concept
title: s60yucca/mnemos
tags:
- persistent-memory
- ai-coding-agent
- go
- sqlite
- context-management
confidence: 0.65
created_at: '2026-05-13'
last_reinforced: '2026-05-13'
sources:
- https://github.com/s60yucca/mnemos
section: Server Implementations > 🧠 <a name="knowledge--memory"></a>Knowledge & Memory
---

> [![s60yucca/mnemos MCP server](https://glama.ai/mcp/servers/s60yucca/mnemos/badges/score.svg)](https://glama.ai/mcp/servers/s60yucca/mnemos) 🏎️ 🏠 🍎 🪟 🐧 - Persistent memory engine for AI coding agents. Stores architecture decisions, bug root causes, and project conventions across sessions. Single Go binary with embedded SQLite, FTS5 search, context assembly within token budgets, and autopilot setup for Claude Code, Kiro, and Cursor.

Mnemos is a persistent memory engine designed for AI coding agents that need to remember project context across sessions. It stores architecture decisions, bug root causes, and project conventions in a lightweight embedded SQLite database with full-text search (FTS5). The tool assembles relevant context within token budgets to help agents stay coherent without exceeding limits. It ships as a single Go binary with autopilot setup for popular coding tools like Claude Code, Kiro, and Cursor.

**Category:** Server Implementations > 🧠 <a name="knowledge--memory"></a>Knowledge & Memory
**Source:** [https://github.com/s60yucca/mnemos](https://github.com/s60yucca/mnemos)
