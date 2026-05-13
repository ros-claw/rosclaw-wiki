---
id: co_browser_attestable_mcp_server
type: concept
title: co-browser/attestable-mcp-server
tags:
- trusted-execution-environment
- remote-attestation
- mcp-server
- gramine
- ra-tls
confidence: 0.65
created_at: '2026-05-13'
last_reinforced: '2026-05-13'
sources:
- https://github.com/co-browser/attestable-mcp-server
section: Server Implementations > 🔒 <a name="security"></a>Security
---

> 🐍 🏠 ☁️ 🐧 - An MCP server running inside a trusted execution environment (TEE) via Gramine, showcasing remote attestation using [RA-TLS](https://gramine.readthedocs.io/en/stable/attestation.html). This allows an MCP client to verify the server before conencting.

This project provides an MCP server that runs inside a Trusted Execution Environment (TEE) using Gramine. It demonstrates remote attestation via RA-TLS, enabling an MCP client to cryptographically verify the server's integrity before connecting. This enhances security for MCP-based AI agent interactions by ensuring the server is running in a trusted environment. The project serves as a reference for implementing attestation in MCP server deployments.

**Category:** Server Implementations > 🔒 <a name="security"></a>Security
**Source:** [https://github.com/co-browser/attestable-mcp-server](https://github.com/co-browser/attestable-mcp-server)
