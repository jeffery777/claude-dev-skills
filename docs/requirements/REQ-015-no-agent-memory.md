---
id: REQ-015
title: No agent memory; project state lives in the repository
status: active
sources:
  - type: chat
    locator: "Claude Code session 2026-10-20 (PR #2 Merge Review 5), user message at 07:18 UTC (pasted decisions D-009 to D-014), opening line"
    quote: "請先重讀 docs/design-proposal.md，再新增以下決策："
  - type: chat
    locator: "Claude Code session 2026-10-20 (PR #2 Merge Review 5), user message at 07:18 UTC (pasted decisions D-009 to D-014), D-010"
    quote: "D-010 不做 agent memory：不建立任何 memory backend 或記憶契約。專案狀態以 repo 為準（REQ wiki、graph.json、events.jsonl、Git、review 紀錄）。原生記憶只當參考資料，與 repo 衝突時以 repo 為準，也不得作為需求來源、授權或完成證據。"
  - type: chat
    locator: "Claude Code session 2026-10-20 (post-merge PR split), user message 1"
    quote: "先用 dev-plan 拆成 PR-A（D-015、R-REV-1、--evidence-file）、PR-B（D-013、D-014、D-016）、PR-C（D-009 到 D-012、context 成本那句話、CHANGELOG、core-feedback、清理項目），一次只做一個，從 PR-A 開始。"
  - type: chat
    locator: "Claude Code session 2026-10-21 (PR-C, Issue #8), user answer to the dev-plan decision cards (card 1 split PR-C into C1 and C2: (a) split; card 2 keep each rule in one place: (b) defer; card 3 open the Issue: (a) yes)"
    quote: "1a、2b、3a"
non_goals:
  - A memory backend, a memory contract or a memory migration
depends_on: []
refines: [REQ-007]
conflicts_with: []
superseded_by: []
superseded_reason: null
---

## Need

The pack builds no memory backend and no memory contract. Project state lives in the
repository: the REQ wiki, `graph.json`, `events.jsonl`, Git and the review records.
Native memory is reference material only. When it conflicts with the repository,
the repository wins. Memory is never a requirement source, authority or
completion evidence.

## Acceptance

- `docs/design-proposal.md` records D-010 in zh and EN with a Core-feedback note.
- The design document's list of things not built (section 6) agrees with D-010.

## Notes

`dev-core` R-AUTH-1 and R-AUTH-7 already treat memory as advisory data that never
overrides the instruction order, so no skill rule changes. Related: [[REQ-007]].
