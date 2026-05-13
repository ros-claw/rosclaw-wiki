---
id: thezenmonster_agentscore_mcp_server
type: concept
title: Thezenmonster/agentscore-mcp-server
tags:
- security
- mcp-server
- npm-monitoring
- github-action
- policy-gate
confidence: 0.65
created_at: '2026-05-13'
last_reinforced: '2026-05-13'
sources:
- https://github.com/Thezenmonster/agentscore-mcp-server
section: Server Implementations > 🔒 <a name="security"></a>Security
---

> [![agentscore-mcp-server MCP server](https://glama.ai/mcp/servers/Thezenmonster/agentscore-mcp-server/badges/score.svg)](https://glama.ai/mcp/servers/Thezenmonster/agentscore-mcp-server) 📇 ☁️ 🍎 🪟 🐧 - MCP security trust layer. Continuously monitors 800+ MCP packages on npm for install scripts, command injection, hardcoded secrets, capability drift, and publisher posture. Ships a GitHub Action policy gate for PR-level allow/warn/block decisions with OIDC auto-provisioning. 5 MCP tools, no API key required.

The agentscore-mcp-server provides a security trust layer for MCP tools by continuously monitoring over 800 npm packages for threats like command injection, hardcoded secrets, and capability drift. It includes a GitHub Action that functions as a policy gate, evaluating pull requests with allow, warn, or block decisions using OIDC auto-provisioning. The server exposes five MCP tools and requires no external API key, making it a no-frills security addition to MCP workflows.

**Category:** Server Implementations > 🔒 <a name="security"></a>Security
**Source:** [https://github.com/Thezenmonster/agentscore-mcp-server](https://github.com/Thezenmonster/agentscore-mcp-server)
