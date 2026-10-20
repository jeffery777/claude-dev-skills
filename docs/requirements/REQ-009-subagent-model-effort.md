---
id: REQ-009
title: Choose subagent model and effort per task
status: active
sources:
  - type: chat
    locator: "Claude Code session 2026-10-20 (claude-dev-skills setup), user message 3 (go-ahead to implement)"
    quote: "我在另一個對話補了 D-001（Core vendor+pin 並加 dev-core 精簡版）與 D-007（subagent 依任務選 model/effort）"
  - type: doc
    locator: "docs/design-proposal.md, section 7, D-007 (2026-10-20)"
    quote: "每個角色在 `agents/*.md` 設定預設的 `model` 與 `effort`；派工時由主代理依第 4 節的對照表逐次覆寫。"
non_goals:
  - A routing engine or a full model x effort matrix
depends_on: []
refines: [REQ-001]
conflicts_with: []
superseded_by: []
superseded_reason: null
---

## Need

Agents carry default model and effort; the main agent overrides them per task, with a floor for high-risk work.

## Acceptance

- Each agent file sets model and effort aliases.
- dev-deliver and dev-review state the per-task choice.

## Notes

Related: [[REQ-001]]
