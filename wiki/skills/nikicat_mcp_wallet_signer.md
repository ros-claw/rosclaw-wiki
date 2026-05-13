---
id: nikicat_mcp_wallet_signer
type: concept
title: nikicat/mcp-wallet-signer
tags:
- finance
- evm-wallet
- non-custodial
- browser-wallet
- eip-6963
confidence: 0.65
created_at: '2026-05-13'
last_reinforced: '2026-05-13'
sources:
- https://github.com/nikicat/mcp-wallet-signer
section: Server Implementations > 💰 <a name="finance--fintech"></a>Finance & Fintech
---

> 📇 🏠 - Non-custodial EVM wallet MCP — routes transactions to browser wallets (MetaMask, etc.) for signing. Private keys never leave the browser; every action requires explicit user approval via EIP-6963.

This MCP server provides a non-custodial EVM wallet signer that routes transaction signing requests to browser-based wallets like MetaMask via EIP-6963. Private keys never leave the user's browser, and every action requires explicit user approval. It enables secure financial interactions within AI agent workflows by leveraging existing browser wallet infrastructure. The server is categorized under Finance & Fintech within MCP server implementations. It ensures user control over transactions while allowing AI agents to propose signable actions.

**Category:** Server Implementations > 💰 <a name="finance--fintech"></a>Finance & Fintech
**Source:** [https://github.com/nikicat/mcp-wallet-signer](https://github.com/nikicat/mcp-wallet-signer)
