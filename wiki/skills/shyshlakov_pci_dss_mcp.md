---
id: shyshlakov_pci_dss_mcp
type: concept
title: shyshlakov/pci-dss-mcp
tags:
- pci-dss
- static-analysis
- security
- go
- mcp-server
confidence: 0.65
created_at: '2026-05-13'
last_reinforced: '2026-05-13'
sources:
- https://github.com/shyshlakov/pci-dss-mcp
section: Server Implementations > 🔒 <a name="security"></a>Security
---

> [![shyshlakov/pci-dss-mcp MCP server](https://glama.ai/mcp/servers/shyshlakov/pci-dss-mcp/badges/score.svg)](https://glama.ai/mcp/servers/shyshlakov/pci-dss-mcp) 🏎️ 🏠 🍎 🪟 🐧 - PCI DSS v4.0.1 static-analysis MCP server for Go payment codebases. 12 scanners detect PAN/CVV exposure, weak crypto, missing audit logs, vulnerable deps, TLS misconfig, auth weaknesses, plus CycloneDX 1.6 SBOM generation - each finding mapped to the exact PCI requirement. AI-assisted triage via triage_findings. Keyless-signed multi-arch Docker image on ghcr.io.

This project provides a Model Context Protocol (MCP) server that performs static analysis of Go codebases for compliance with PCI DSS v4.0.1. It includes 12 scanners that detect issues like credit card number exposure, weak cryptography, missing audit logs, vulnerable dependencies, TLS misconfigurations, and authentication weaknesses. Each finding maps to specific PCI requirement and the server can generate CycloneDX 1.6 SBOMs. It also features AI-assisted triage of findings and is distributed as a keyless-signed multi-architecture Docker image.

**Category:** Server Implementations > 🔒 <a name="security"></a>Security
**Source:** [https://github.com/shyshlakov/pci-dss-mcp](https://github.com/shyshlakov/pci-dss-mcp)
