---
id: yang1bai_claw_tsaver
type: concept
title: Yang1Bai/claw-tsaver
tags:
- token-saving
- mcp-proxy
- openclaw
- claude
- benchmark
confidence: 0.65
created_at: '2026-05-13'
last_reinforced: '2026-05-13'
sources:
- https://github.com/Yang1Bai/claw-tsaver
section: Server Implementations > 🔒 <a name="delivery"></a>Delivery
---

> 🐍 🏠 🍎 🪟 🐧 - Token-saving MCP proxy that intercepts oversized tool returns and replaces them with a preview + on-demand handle. Real benchmark: 11,507 tokens → 104 tokens (99.1% saved) on a Wikipedia fetch. Works with OpenClaw + Claude.

claw-tsaver is a token-saving proxy for the Model Context Protocol (MCP) that intercepts oversized tool returns and replaces them with a compact preview plus an on-demand handle. A benchmark on a Wikipedia fetch showed a reduction from 11,507 tokens to 104 tokens (99.1% saved). The tool is designed to work with OpenClaw and Claude, helping to reduce token consumption in AI agent interactions.

**Category:** Server Implementations > 🔒 <a name="delivery"></a>Delivery
**Source:** [https://github.com/Yang1Bai/claw-tsaver](https://github.com/Yang1Bai/claw-tsaver)
