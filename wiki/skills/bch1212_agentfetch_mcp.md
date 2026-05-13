---
id: bch1212_agentfetch_mcp
type: concept
title: bch1212/agentfetch-mcp
tags:
- mcp-server
- browser-automation
- web-fetch
- token-budget
- open-source
confidence: 0.65
created_at: '2026-05-13'
last_reinforced: '2026-05-13'
sources:
- https://github.com/bch1212/agentfetch-mcp
section: Server Implementations > 📂 <a name="browser-automation"></a>Browser Automation
---

> [![bch1212/agentfetch-mcp MCP server](https://glama.ai/mcp/servers/bch1212/agentfetch-mcp/badges/score.svg)](https://glama.ai/mcp/servers/bch1212/agentfetch-mcp) 🐍 ☁️ 🏠 🍎 🪟 🐧 - Token-budgeted web fetch for AI agents. Auto-routes between Trafilatura, Jina Reader, FireCrawl, and pypdf based on URL pattern. `estimate_tokens` before `fetch_url`, 6h Redis cache, server-side `max_tokens` truncation. Open source MCP server (MIT) plus hosted REST API at [agentfetch.dev](https://www.agentfetch.dev) — 500 free fetches/mo, no card.

AgentFetch MCP is an open-source server that provides token-budgeted web fetching for AI agents. It automatically routes requests to different parsers such as Trafilatura, Jina Reader, FireCrawl, or pypdf based on the URL pattern. Key features include estimating token usage before fetching, a 6-hour Redis cache, and server-side max_tokens truncation. It also offers a hosted REST API at agentfetch.dev with 500 free fetches per month. This tool is designed to optimize web content retrieval for AI agents with cost and token constraints.

**Category:** Server Implementations > 📂 <a name="browser-automation"></a>Browser Automation
**Source:** [https://github.com/bch1212/agentfetch-mcp](https://github.com/bch1212/agentfetch-mcp)
