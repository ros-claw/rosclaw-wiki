---
id: create_worktrees
type: concept
title: /create-worktrees
tags:
- git
- worktree
- branch-management
- pull-requests
- developer-tools
confidence: 0.65
created_at: '2026-05-14'
last_reinforced: '2026-05-14'
sources:
- https://github.com/evmts/tevm-monorepo/blob/main/.claude/commands/create-worktrees.md
section: Slash-Commands > Version Control & Git
---

> Creates git worktrees for all open PRs or specific branches, handling branches with slashes, cleaning up stale worktrees, and supporting custom branch creation for development.

This slash-command tool automates the creation of git worktrees for open pull requests or specific branches. It handles branch names containing slashes and cleans up stale worktrees automatically. Users can also create custom branches for development, enabling parallel work on multiple features without switching directories. The command integrates with GitHub/GitLab PRs to simplify workflow management.

**Category:** Slash-Commands > Version Control & Git
**Source:** [https://github.com/evmts/tevm-monorepo/blob/main/.claude/commands/create-worktrees.md](https://github.com/evmts/tevm-monorepo/blob/main/.claude/commands/create-worktrees.md)
