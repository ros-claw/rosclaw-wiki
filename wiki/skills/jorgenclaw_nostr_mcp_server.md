---
id: jorgenclaw_nostr_mcp_server
type: concept
title: jorgenclaw/nostr-mcp-server
tags:
- nostr
- lightning-network
- mcp-server
- ai-agents
- micropayments
confidence: 0.65
created_at: '2026-05-13'
last_reinforced: '2026-05-13'
sources:
- https://github.com/jorgenclaw/nostr-mcp-server
section: Server Implementations > 🌐 <a name="social-media"></a>Social Media
---

> [![jorgenclaw/nostr-mcp-server MCP server](https://glama.ai/mcp/servers/jorgenclaw/nostr-mcp-server/badges/score.svg)](https://glama.ai/mcp/servers/jorgenclaw/nostr-mcp-server) 📇 ☁️ - Lightning-paid Nostr signing MCP server. AI agents pay sats per call to sign and publish Nostr events — no API keys, just Lightning. Live at https://mcp.jorgenclaw.ai/sse. Tools: nostr_sign_event (2 sats), nostr_publish_event (3 sats).

This project implements a Model Context Protocol (MCP) server that integrates with the Nostr protocol, allowing AI agents to sign and publish Nostr events by paying small amounts of sats over the Lightning Network. It eliminates the need for API keys by using Lightinng micropayments per call, with costs of 2 sats for signing and 3 sats for publishing. The server is live at mcp.jorgenclaw.ai/sse and is designed for use with AI agents that need to interact with Nostr in a pay-per-use, trustless manner.

**Category:** Server Implementations > 🌐 <a name="social-media"></a>Social Media
**Source:** [https://github.com/jorgenclaw/nostr-mcp-server](https://github.com/jorgenclaw/nostr-mcp-server)
