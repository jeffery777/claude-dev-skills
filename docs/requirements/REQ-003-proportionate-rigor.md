---
id: REQ-003
title: Proportionate rigor; no over-engineering
status: active
sources:
  - type: chat
    locator: "Claude Code session 2026-10-20 (claude-dev-skills setup), user message 2 (answer to the graph-engineering question)"
    quote: "我發現Codex在開發時，有時會過度工程化，忽略了原始的專案需求，變成了通用需求"
  - type: chat
    locator: "Claude Code session 2026-10-20 (claude-dev-skills setup), user message 2 (answer to the graph-engineering question)"
    quote: "我不是說嚴謹不好，而是要適度地嚴謹。"
non_goals:
  - Weakening Core obligations to reduce ceremony
depends_on: []
refines: []
conflicts_with: []
superseded_by: []
superseded_reason: null
---

## Need

Rigor scales with risk, and every change traces back to the user's original requirement so the work does not drift into generic requirements.

## Acceptance

- Work is classified into light, standard and strict tiers with a recorded reason.
- Additions without a requirement are reported as SCOPE-CREEP findings.

## Notes

Related: [[REQ-007]], [[REQ-008]]
