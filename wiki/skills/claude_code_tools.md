---
id: claude_code_tools
type: entity
title: claude-code-tools
tags:
- session-continuity
- claude-code
- codex-cli
- rust
- tmux
confidence: 0.65
created_at: '2026-05-14'
last_reinforced: '2026-05-14'
sources:
- https://github.com/pchalasani/claude-code-tools
section: Tooling > General
---

> Well-crafted toolset for session continuity, featuring skills/commands to avoid compaction and recover context across sessions with cross-agent handoff between Claude Code and Codex CLI. Includes a fast Rust/Tantivy-powered full-text session search (TUI for humans, skill/CLI for agents), tmux-cli skill + command for interacting with scripts and CLI agents, and safety hooks to block dangerous commands.

claude-code-tools is a collection of utilities designed to enhance session continuity for AI coding agents like Claude Code and Codex CLI. It provides skills and commands to prevent context compaction and recover context across sessions. The toolset includes a fast full-text session search powered by Rust and Tantivy, with a TUI interface for humans and CLI/skill interface for agents. It also features a tmux-cli skill and command for interacting with scripts and CLI agents, along with safety hooks to block dangerous commands.

**Category:** Tooling > General
**Source:** [https://github.com/pchalasani/claude-code-tools](https://github.com/pchalasani/claude-code-tools)
