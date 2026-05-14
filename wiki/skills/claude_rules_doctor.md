---
id: claude_rules_doctor
type: entity
title: claude-rules-doctor
tags:
- claude-code
- config-management
- glob-patterns
- ci-tool
- validator
confidence: 0.65
created_at: '2026-05-14'
last_reinforced: '2026-05-14'
sources:
- https://github.com/nulone/claude-rules-doctor
section: Tooling > Config Managers
---

> CLI that detects dead `.claude/rules/` files by checking if `paths:` globs actually match files in your repo. Catches silent rule failures where renamed directories or typos in glob patterns cause rules to never apply. Features CI mode (exit 1 on dead rules), JSON output, and verbose mode showing matched files.

This CLI tool inspects `.claude/rules/` files to find rules that never apply because their `paths:` glob patterns do not match any files in the repository. It helps catch silent failures when directories are renamed or glob patterns contain typos. The tool can be run in CI mode to exit with an error if any dead rules exist, making it easy to integrate into automated workflows. It also supports JSON output and verbose mode for detailed debugging.

**Category:** Tooling > Config Managers
**Source:** [https://github.com/nulone/claude-rules-doctor](https://github.com/nulone/claude-rules-doctor)
