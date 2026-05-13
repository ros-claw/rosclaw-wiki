---
id: zboralski_ida_headless_mcp
type: concept
title: zboralski/ida-headless-mcp
tags:
- ida-pro
- headless-analysis
- binary-analysis
- reverse-engineering
- mcp-server
confidence: 0.65
created_at: '2026-05-13'
last_reinforced: '2026-05-13'
sources:
- https://github.com/zboralski/ida-headless-mcp
section: Server Implementations > 🔒 <a name="security"></a>Security
---

> 🏎️ 🐍 🏠 🍎 🪟 🐧 - Headless IDA Pro binary analysis via MCP. Multi-session concurrency with Go orchestration and Python workers. Supports Il2CppDumper and Blutter metadata import for Unity and Flutter reverse engineering.

This project implements a server that connects IDA Pro, a powerful binary analysis tool, to the Model Context Protocol, enabling AI agents to perform headless binary analysis. It supports multiple concurrent sessions orchestrated by Go and executed by Python workers. The system can import metadata from Il2CppDumper and Blutter, allowing analysis of Unity and Flutter applications. It is intended for security research and reverse engineering tasks.

**Category:** Server Implementations > 🔒 <a name="security"></a>Security
**Source:** [https://github.com/zboralski/ida-headless-mcp](https://github.com/zboralski/ida-headless-mcp)
