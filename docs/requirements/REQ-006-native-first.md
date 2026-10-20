---
id: REQ-006
title: Use native Claude capabilities first
status: active
sources:
  - type: chat
    locator: "Claude Code session 2026-10-20 (claude-dev-skills setup), user message 2 (answer to the language question)"
    quote: "如果你原生已經會的技能，甚至你原生已經會的技能比這技能包中設計的還好，那你可以視狀況調整，不用再在claude-dev-skills再多做設計（只要在文件中說明即可）。"
non_goals:
  - Re-implementing native review, planning, worktree or orchestration features
depends_on: []
refines: []
conflicts_with: []
superseded_by: []
superseded_reason: null
---

## Need

Where Claude Code already does something as well or better, use it and document the mapping instead of designing a duplicate.

## Acceptance

- The design document lists the native capabilities used and what the pack adds.

## Notes

Related: [[REQ-001]]
