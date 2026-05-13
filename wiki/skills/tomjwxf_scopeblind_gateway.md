---
id: tomjwxf_scopeblind_gateway
type: concept
title: tomjwxf/scopeblind-gateway
tags:
- security
- mcp-server
- policy-enforcement
- approval-workflow
- audit-logging
confidence: 0.65
created_at: '2026-05-13'
last_reinforced: '2026-05-13'
sources:
- https://github.com/tomjwxf/scopeblind-gateway
section: Server Implementations > 🔒 <a name="security"></a>Security
---

> [![tomjwxf/scopeblind-gateway MCP server](https://glama.ai/mcp/servers/tomjwxf/scopeblind-gateway/badges/score.svg)](https://glama.ai/mcp/servers/tomjwxf/scopeblind-gateway) 📇 🏠 — Security gateway that wraps any MCP server with per-tool policies, approval gates, and optional Ed25519-signed receipts. Shadow mode logs every tool call; enforce mode blocks, rate-limits, or requires approval.

Scopeblind Gateway is a security wrapper for MCP servers that adds access control on a per-tool basis. It supports approval gates where certain tools require explicit authorization, and logs all tool calls in shadow mode. In enforce mode, the gateway can block, rate-limit, or require approval for tool invocations. It also optionally produces Ed25519-signed receipts for auditability. This helps secure MCP server deployments by adding policy enforcement layers.

**Category:** Server Implementations > 🔒 <a name="security"></a>Security
**Source:** [https://github.com/tomjwxf/scopeblind-gateway](https://github.com/tomjwxf/scopeblind-gateway)
