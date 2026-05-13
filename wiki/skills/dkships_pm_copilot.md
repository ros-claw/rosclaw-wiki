---
id: dkships_pm_copilot
type: concept
title: dkships/pm-copilot
tags:
- product-management
- mcp-server
- prioritization
- support-tickets
- feature-requests
confidence: 0.65
created_at: '2026-05-13'
last_reinforced: '2026-05-13'
sources:
- https://github.com/dkships/pm-copilot
section: Server Implementations > 📋 <a name="product-management"></a>Product Management
---

> 📇 ☁️ - Triangulates HelpScout support tickets and ProductLift feature requests to generate prioritized product plans. Scores themes by convergence (same signal in both sources = 2x boost), scrubs PII, and accepts business metrics from other MCP servers via `kpi_context` for composable prioritization.

This tool integrates support tickets from HelpScout with feature requests from ProductLift to create prioritized product plans. It identifies themes and boosts scores when the same signal appears in both sources, effectively doubling the priority. It also scrubs personally identifiable information (PII) and can accept business metrics from other MCP servers via a `kpi_context` parameter, enabling composable prioritization. The result is a data-driven product plan that balances qualitative feedback with quantitative business data.

**Category:** Server Implementations > 📋 <a name="product-management"></a>Product Management
**Source:** [https://github.com/dkships/pm-copilot](https://github.com/dkships/pm-copilot)
