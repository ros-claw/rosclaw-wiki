---
id: zkproofport_proofport_ai
type: concept
title: zkproofport/proofport-ai
tags:
- zero-knowledge-proof
- mcp-server
- identity
- tee
- blockchain
confidence: 0.65
created_at: '2026-05-13'
last_reinforced: '2026-05-13'
sources:
- https://github.com/zkproofport/proofport-ai
section: Server Implementations > 🔒 <a name="security"></a>Security
---

> [![proofport-ai MCP server](https://glama.ai/mcp/servers/zkproofport/proofport-ai/badges/score.svg)](https://glama.ai/mcp/servers/zkproofport/proofport-ai) 📇 ☁️ - Zero-knowledge proof generation MCP server for AI agents. Lets agents prove identity claims (Coinbase KYC, Country, Google OIDC, Google Workspace, Microsoft 365) without revealing personal information. Server-side proving in AWS Nitro Enclave TEE, paid via x402 USDC on Base. Built on Noir circuits (Aztec) and ERC-8004 agent identity. Reference application [OpenStoa](https://github.com/zkproofport/openstoa) won 1st place at The Synthesis Hackathon ("Agents That Keep Secrets" track).

This project is a Model Context Protocol (MCP) server that enables AI agents to generate zero-knowledge proofs for identity claims, such as KYC verification or email domain ownership, without revealing the underlying personal data. The proof generation runs inside an AWS Nitro Enclave trusted execution environment (TEE) for security, and usage is paid for via x402 micropayments in USDC on the Base blockchain. It uses Noir circuits from Aztec for the zero-knowledge proofs and implements the ERC-8004 standard for agent identity. The reference application, OpenStoa, won first place at The Synthesis Hackathon in the 'Agents That Keep Secrets' track, demonstrating the practical value of privacy-preserving agent identity.

**Category:** Server Implementations > 🔒 <a name="security"></a>Security
**Source:** [https://github.com/zkproofport/proofport-ai](https://github.com/zkproofport/proofport-ai)
