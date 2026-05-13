---
id: vaulted_fyi_vaulted_mcp_server
type: concept
title: vaulted-fyi/vaulted-mcp-server
tags:
- mcp-server
- security
- encryption
- secrets-management
- self-destructing-secrets
confidence: 0.65
created_at: '2026-05-13'
last_reinforced: '2026-05-13'
sources:
- https://github.com/vaulted-fyi/vaulted-mcp-server
section: Server Implementations > 🔒 <a name="security"></a>Security
---

> [![vaulted-fyi/vaulted-mcp-server MCP server](https://glama.ai/mcp/servers/vaulted-fyi/vaulted-mcp-server/badges/score.svg)](https://glama.ai/mcp/servers/vaulted-fyi/vaulted-mcp-server) 📇 🏠 🍎 🪟 🐧 - Share encrypted, self-destructing secrets from your AI agent. Zero-knowledge E2E encryption. Agent-blind input sources (env:, file:, dotenv:) keep secrets out of LLM context.

Vaulted MCP Server is a Model Context Protocol server that enables AI agents to share encrypted, self-destructing secrets. It uses zero-knowledge end-to-end encryption to ensure that even the server never sees the plaintext secrets. The server supports agent-blind input sources (environment variables, files, dotenv files) to keep secrets out of the LLM context. This design prevents sensitive data from being exposed to the language model during interactions.

**Category:** Server Implementations > 🔒 <a name="security"></a>Security
**Source:** [https://github.com/vaulted-fyi/vaulted-mcp-server](https://github.com/vaulted-fyi/vaulted-mcp-server)
