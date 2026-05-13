---
id: ckanthony_chisel
type: concept
title: ckanthony/Chisel
tags:
- mcp-server
- file-system
- token-efficiency
- path-confinement
- rust
confidence: 0.65
created_at: '2026-05-13'
last_reinforced: '2026-05-13'
sources:
- https://github.com/ckanthony/Chisel
section: Server Implementations > 📂 <a name="file-systems"></a>File Systems
---

> [![chisel MCP server](https://glama.ai/mcp/servers/@ckanthony/chisel/badges/score.svg)](https://glama.ai/mcp/servers/@ckanthony/chisel) 🦀 🏠 🍎 🐧 ☁️ - Reduce context usage on file use. Send only unified diffs instead of full files (up to 20-100× fewer tokens), and read large files with targeted `grep`/`sed` instead of full reads (up to 500×). Kernel-enforced path confinement hard-locks the agent to a configured root: no accidental reads or writes outside scope. Standalone for your file access or embed in any MCP server (Rust, Node.js, Python via WASM).

Chisel is a high-efficiency MCP server that reduces token usage by sending unified diffs instead of full files, achieving up to 500× savings on large files through targeted grep/sed operations. It features kernel-enforced path confinement to hard-lock agents to a configured directory, preventing accidental out-of-scope reads or writes. Built in Rust, it can be used standalone for file access or embedded into MCP servers supporting Rust, Node.js, or Python via WASM.

**Category:** Server Implementations > 📂 <a name="file-systems"></a>File Systems
**Source:** [https://github.com/ckanthony/Chisel](https://github.com/ckanthony/Chisel)
