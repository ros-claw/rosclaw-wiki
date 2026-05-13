---
id: tooluse_labs_perfetto_mcp_rs
type: entity
title: tooluse-labs/perfetto-mcp-rs
tags:
- perfetto
- mcp-server
- trace-analysis
- rust
- performance-tooling
confidence: 0.65
created_at: '2026-05-13'
last_reinforced: '2026-05-13'
sources:
- https://github.com/tooluse-labs/perfetto-mcp-rs
section: Server Implementations > 💻 <a name="developer-tools"></a>Developer Tools
---

> [![tooluse-labs/perfetto-mcp-rs MCP server](https://glama.ai/mcp/servers/tooluse-labs/perfetto-mcp-rs/badges/score.svg)](https://glama.ai/mcp/servers/tooluse-labs/perfetto-mcp-rs) 🦀 🏠 🍎 🪟 🐧 - MCP server for [Perfetto](https://perfetto.dev) trace analysis. Runs PerfettoSQL queries on `.perfetto-trace` / `.pftrace` files via auto-downloaded `trace_processor_shell`, with dedicated Chrome tools for page loads, scroll jank, main-thread hotspots, and stdlib module discovery. Cross-client tested on Claude Code and Codex. Available via `cargo install`, Homebrew tap, and curl install script.

This project implements an MCP (Model Context Protocol) server for analyzing Perfetto traces, a system profiling and tracing tool. It enables running PerfettoSQL queries on `.perfetto-trace` or `.pftrace` files using an auto-downloaded `trace_processor_shell` binary. The server includes dedicated tools for analyzing Chrome page loads, scroll jank, main-thread hotspots, and discovering standard library modules. It supports installation via Cargo, Homebrew, and a curl script, and has been tested across clients like Claude Code and Codex. This integration allows AI assistants to directly query performance trace data for debugging and optimization.

**Category:** Server Implementations > 💻 <a name="developer-tools"></a>Developer Tools
**Source:** [https://github.com/tooluse-labs/perfetto-mcp-rs](https://github.com/tooluse-labs/perfetto-mcp-rs)
