---
id: czagents_cnb
type: concept
title: '@czagents/cnb'
tags:
- finance
- fx-rates
- czech-national-bank
- czk
- mcp-server
confidence: 0.65
created_at: '2026-05-13'
last_reinforced: '2026-05-13'
sources:
- https://github.com/martinhavel/cz-agents-mcp
section: Server Implementations > 💰 <a name="finance--fintech"></a>Finance & Fintech
---

> [![martinhavel/cz-agents-mcp MCP server](https://glama.ai/mcp/servers/martinhavel/cz-agents-mcp/badges/score.svg)](https://glama.ai/mcp/servers/martinhavel/cz-agents-mcp) 📇 ☁️ 🏠 🍎 🪟 🐧 - Czech National Bank (ČNB) daily FX rates: fetch official CZK exchange rates, convert between currencies, fetch historical rates. Cached 10 min to ease upstream load. npm `@czagents/cnb` or HTTP at cnb.cz-agents.dev/mcp.

This server provides access to official daily foreign exchange rates from the Czech National Bank (ČNB). It supports fetching current and historical CZK exchange rates for multiple currencies, and can convert between currencies using the official rates. Data is cached for 10 minutes to reduce load on upstream sources. It can be used as an npm package or via HTTP at cnb.cz-agents.dev/mcp.

**Category:** Server Implementations > 💰 <a name="finance--fintech"></a>Finance & Fintech
**Source:** [https://github.com/martinhavel/cz-agents-mcp](https://github.com/martinhavel/cz-agents-mcp)
