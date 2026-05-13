---
id: davidlandais_ovh_api_mcp
type: concept
title: davidlandais/ovh-api-mcp
tags:
- ovh-api
- mcp-server
- cloud-platform
- rust
- sandboxed-javascript
confidence: 0.65
created_at: '2026-05-13'
last_reinforced: '2026-05-13'
sources:
- https://github.com/davidlandais/ovh-api-mcp
section: Server Implementations > ☁️ <a name="cloud-platforms"></a>Cloud Platforms
---

> [![ovh-api-mcp MCP server](https://glama.ai/mcp/servers/davidlandais/ovh-api-mcp/badges/score.svg)](https://glama.ai/mcp/servers/davidlandais/ovh-api-mcp) 🦀 ☁️ - Code Mode MCP server for the entire OVH API. Two tools (search + execute) give LLMs access to all OVH endpoints via sandboxed JavaScript, using ~1,000 tokens instead of thousands of tool definitions.

This MCP server provides LLMs with access to the entire OVH API using only two tools: search and execute. It uses sandboxed JavaScript to dynamically call any OVH endpoint, reducing token usage to around 1,000 tokens instead of thousands of individual tool definitions. The server is implemented in Rust and enables AI agents to manage OVH cloud services such as domains and hosting. It is listed under Cloud Platforms in the MCP server ecosystem.

**Category:** Server Implementations > ☁️ <a name="cloud-platforms"></a>Cloud Platforms
**Source:** [https://github.com/davidlandais/ovh-api-mcp](https://github.com/davidlandais/ovh-api-mcp)
