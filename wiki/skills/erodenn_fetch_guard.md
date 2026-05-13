---
id: erodenn_fetch_guard
type: concept
title: Erodenn/fetch-guard
tags:
- url-fetcher
- html-to-markdown
- prompt-injection-defense
- security
- mcp-server
confidence: 0.65
created_at: '2026-05-13'
last_reinforced: '2026-05-13'
sources:
- https://github.com/Erodenn/fetch-guard
section: Server Implementations > 🔒 <a name="security"></a>Security
---

> [![fetch-guard MCP server](https://glama.ai/mcp/servers/@Erodenn/fetch-guard/badges/score.svg)](https://glama.ai/mcp/servers/@Erodenn/fetch-guard) 🐍 🏠 🍎 🪟 🐧 - URL fetcher and HTML-to-markdown converter with three-layer prompt injection defense: pre-extraction sanitization of hidden/off-screen elements and non-printing Unicode, 15-pattern risk scanning (HIGH/MEDIUM/OK), and per-request session-salt content boundary wrapping.

Fetch-guard is a server implementation that fetches URLs and converts HTML to Markdown. It includes a three-layer defense against prompt injection attacks: first, it sanitizes hidden/off-screen elements and non-printing Unicode characters before extraction; second, it scans the content for 15 risk patterns classified as HIGH, MEDIUM, or OK; third, it wraps the final content with per-request session-salt boundaries. This tool is designed to safely retrieve web content for use in AI agent conversations.

**Category:** Server Implementations > 🔒 <a name="security"></a>Security
**Source:** [https://github.com/Erodenn/fetch-guard](https://github.com/Erodenn/fetch-guard)
