---
id: taniwhaai_arai
type: concept
title: taniwhaai/arai
tags:
- policy-enforcement
- mcp-server
- claude-code
- coding-agents
- audit-logging
confidence: 0.65
created_at: '2026-05-13'
last_reinforced: '2026-05-13'
sources:
- https://github.com/taniwhaai/arai
section: Server Implementations > 🔒 <a name="security"></a>Security
---

> [![taniwhaai/arai MCP server](https://glama.ai/mcp/servers/taniwhaai/arai/badges/score.svg)](https://glama.ai/mcp/servers/taniwhaai/arai) 🦀 🏠 🍎 🪟 🐧 - Policy enforcement for AI coding agents derived from existing instruction files (CLAUDE.md, .cursorrules, .windsurfrules, .github/copilot-instructions.md) — no separate YAML to maintain. Rules with prohibitive predicates (`never`, `forbids`, `must_not`) emit `permissionDecision: deny` to block tool calls in Claude Code; advisory rules inject context. PostToolUse is correlated with PreToolUse to produce per-rule obeyed/ignored compliance verdicts in a local JSONL audit log. MCP tools — `arai_add_guard` (register rules mid-session), `arai_list_guards`, `arai_recent_decisions` — work in any MCP client (Claude Desktop, Cursor, Windsurf, Cline). No network on the hook hot path; opt-out anonymous telemetry.

Arai is a policy enforcement server for AI coding agents that reads existing instruction files (such as CLAUDE.md, .cursorrules, .windsurfrules, and Copilot instructions) to derive rules. It uses predicates like 'never' and 'must_not' to block tool calls or inject advisory context, and logs compliance verdicts to a local JSONL file for audit. Arai provides MCP tools (add_guard, list_guards, recent_decisions) that work across multiple clients like Claude Desktop, Cursor, Windsurf, and Cline, with no network dependency on the critical path.

**Category:** Server Implementations > 🔒 <a name="security"></a>Security
**Source:** [https://github.com/taniwhaai/arai](https://github.com/taniwhaai/arai)
