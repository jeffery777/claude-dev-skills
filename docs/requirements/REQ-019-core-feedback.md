---
id: REQ-019
title: Feed Core-level changes back to engineering-workflow-core
status: active
sources:
  - type: chat
    locator: "Claude Code session 2026-10-20 (PR #2 merge), user message at 08:25 UTC"
    quote: "對了，你其實有發現參考的codex-dev-skills的問題對吧？而且列在你的memory裡，這些問題如果是上游engineering-workflow-core的問題，要紀錄下來，由於engineering-workflow-core是codex-dev-skills、grok-build-dev-skills以及claude-dev-skills的核心流程，所以你在claude-dev-skills的修改必須要能回饋到engineering-workflow-core，這樣另外二個專案才能跟著改"
  - type: chat
    locator: "Claude Code session 2026-10-20 (post-merge PR split), user message 1"
    quote: "先用 dev-plan 拆成 PR-A（D-015、R-REV-1、--evidence-file）、PR-B（D-013、D-014、D-016）、PR-C（D-009 到 D-012、context 成本那句話、CHANGELOG、core-feedback、清理項目），一次只做一個，從 PR-A 開始。"
  - type: chat
    locator: "Claude Code session 2026-10-21 (PR-C, Issue #8), user answer to the dev-plan decision cards (card 1 split PR-C into C1 and C2: (a) split; card 2 keep each rule in one place: (b) defer; card 3 open the Issue: (a) yes)"
    quote: "1a、2b、3a"
non_goals:
  - Changes to engineering-workflow-core, codex-dev-skills or grok-build-dev-skills
  - Opening Issues in those repositories without the user's approval
depends_on: []
refines: [REQ-007]
conflicts_with: []
superseded_by: []
superseded_reason: null
---

## Need

engineering-workflow-core is the shared core of codex-dev-skills,
grok-build-dev-skills and claude-dev-skills. A change made here that is a
Core-level issue is recorded so that it can be fed back to Core, and the other
two projects can then adopt it.

## Acceptance

- Every decision D-009 to D-016 in `docs/design-proposal.md` (zh and EN) has a "Core feedback: yes/no" note with a reason.
- `docs/core-feedback.md` lists each Core-level item with the problem, the evidence, the proposed Core change, additive or modifying, and the impact on codex-dev-skills and grok-build-dev-skills.
- The Evidence column of `skills/dev-core/deltas.md` cites the recorded evidence for each delta that has some.

## Notes

D-001 defines the feedback process (additive companion text preferred; a
modifying change needs candidate pins and evals in the other two projects).
PR-C decision card 2 (keep each rule in one place) was deferred by the user and
is recorded as a follow-up and a feedback item. Related: [[REQ-007]],
[[REQ-016]].
