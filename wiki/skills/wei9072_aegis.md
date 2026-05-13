---
id: wei9072_aegis
type: concept
title: wei9072/aegis
tags:
- mcp-server
- admission-control
- security
- rust
- ai-safety
confidence: 0.65
created_at: '2026-05-13'
last_reinforced: '2026-05-13'
sources:
- https://github.com/wei9072/aegis
section: Server Implementations > 🔒 <a name="security"></a>Security
---

> [![wei9072/aegis MCP server](https://glama.ai/mcp/servers/wei9072/aegis/badges/score.svg)](https://glama.ai/mcp/servers/wei9072/aegis) 🦀 🏠 🍎 🪟 🐧 - AI-agent admission-control MCP server: validates file edits against Ring 0 syntax + Ring 0.5 structural-cost regression + workspace boundary (path / glob / shell-redirect / symlink). Negative-space framing — emits BLOCK / WARN / PASS verdicts, never coaches the agent.

Aegis is an admission-control MCP server for AI agents that validates file edits before execution. It enforces multiple security layers: Ring 0 syntax checks, Ring 0.5 structural cost regressions, and workspace boundary restrictions (path, glob, shell redirect, symlink). The server returns only BLOCK, WARN, or PASS verdicts without providing any guidance to the agent, maintaining a negative-space approach. Built in Rust, it runs across macOS, Windows, and Linux to prevent unsafe operations while allowing safe edits.

**Category:** Server Implementations > 🔒 <a name="security"></a>Security
**Source:** [https://github.com/wei9072/aegis](https://github.com/wei9072/aegis)
