---
id: REQ-010
title: Phase 1 scope
status: active
sources:
  - type: chat
    locator: "Claude Code session 2026-10-20 (claude-dev-skills setup), user message 2 (answer to the Phase 1 question (selected option))"
    quote: "8 技能 + 4 agents + G0 (Recommended)"
  - type: chat
    locator: "Claude Code session 2026-10-20 (claude-dev-skills setup), user message 3 (go-ahead to implement)"
    quote: "選 1，定案並開始實作。"
non_goals:
  - G1-G3, hooks and a CI workflow in Phase 1
depends_on: [REQ-001, REQ-002]
refines: []
conflicts_with: []
superseded_by: []
superseded_reason: null
---

## Need

Phase 1 delivers the eight skills, four agents, the G0 task graph with fixtures, the Core vendor and its checks, and plugin packaging (D-008).

## Acceptance

- scripts/validate.sh runs every Phase 1 check and passes.

## Notes

Related: [[REQ-002]], [[REQ-008]]
