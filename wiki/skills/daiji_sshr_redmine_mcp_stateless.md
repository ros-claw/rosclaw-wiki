---
id: daiji_sshr_redmine_mcp_stateless
type: concept
title: daiji-sshr/redmine-mcp-stateless
tags:
- redmine
- mcp-server
- stateless
- issue-tracking
- project-management
confidence: 0.65
created_at: '2026-05-13'
last_reinforced: '2026-05-13'
sources:
- https://github.com/daiji-sshr/redmine-mcp-stateless
section: Server Implementations > 📋 <a name="product-management"></a>Product Management
---

> [![daiji-sshr/redmine-mcp-stateless MCP server](https://glama.ai/mcp/servers/daiji-sshr/redmine-mcp-stateless/badges/score.svg)](https://glama.ai/mcp/servers/daiji-sshr/redmine-mcp-stateless) 🐍 🏠 🐧 - Stateless Redmine MCP server. Credentials are passed per-request via HTTP headers and never stored on the server. Supports listing/creating/updating issues, full-text search across subjects, descriptions and comments, and editing journals (Redmine 5.0+). Deployable on RHEL (systemd) or Docker.

This is a stateless MCP server for Redmine, meaning user credentials are passed per-request via HTTP headers and not stored on the server. It supports listing, creating, and updating issues, as well as full-text search across subjects, descriptions, and comments. Additionally, it can edit journal entries (Redmine 5.0+). The server can be deployed on RHEL using systemd or via Docker.

**Category:** Server Implementations > 📋 <a name="product-management"></a>Product Management
**Source:** [https://github.com/daiji-sshr/redmine-mcp-stateless](https://github.com/daiji-sshr/redmine-mcp-stateless)
