---
id: REQ-014
title: Review findings and their relation to requirements
status: active
sources:
  - type: chat
    locator: "Claude Code session 2026-10-20 (PR #2 Merge Review 5), user message queued at 07:58 UTC (D-016 for memory), heading"
    quote: "D-016 Review 範圍與需求的關係（寫進 dev-review 的 brief 規則與 finding 格式）："
  - type: chat
    locator: "Claude Code session 2026-10-20 (PR #2 Merge Review 5), user message queued at 07:58 UTC, D-016 item 1"
    quote: "1. Review 找問題的範圍不限於需求，但每個 finding 都必須標明 requirement_relation，值為 in-scope、gap、no-requirement 或 unrelated 之一。"
  - type: chat
    locator: "Claude Code session 2026-10-20 (PR #2 Merge Review 5), user message queued at 07:58 UTC, D-016 item 2"
    quote: "2. 新增 finding 類別 REQ-GAP：需求沒有涵蓋、但看起來應該涵蓋的問題。REQ-GAP 不在當次直接修正，而是依 D-014 的格式做成決策卡片，交給使用者選擇：新增需求、延後處理或不採納。"
  - type: chat
    locator: "Claude Code session 2026-10-20 (PR #2 Merge Review 5), user message queued at 07:58 UTC, D-016 item 3"
    quote: "3. 只有使用者能新增需求。使用者同意後，由 dev-plan 把它 ingest 成新的 REQ，sources 記下 finding ID 與使用者的決定；agent 不能自己把 REQ-GAP 寫成需求。"
  - type: chat
    locator: "Claude Code session 2026-10-20 (PR #2 Merge Review 5), user message queued at 07:58 UTC, D-016 item 4"
    quote: "4. no-requirement 歸為 SCOPE-CREEP；unrelated 列為 residual risk 或 follow-up，不阻擋當次交付。"
  - type: chat
    locator: "Claude Code session 2026-10-20 (PR #2 Merge Review 5), user message queued at 07:58 UTC, D-016 item 5"
    quote: "5. 例外：Core 規定的阻擋項（安全、資料遺失、授權、完整性）不論 requirement_relation 為何都照樣阻擋；需求沒寫到不構成豁免。"
  - type: chat
    locator: "Claude Code session 2026-10-20 (post-merge PR split), user message 1"
    quote: "先用 dev-plan 拆成 PR-A（D-015、R-REV-1、--evidence-file）、PR-B（D-013、D-014、D-016）、PR-C（D-009 到 D-012、context 成本那句話、CHANGELOG、core-feedback、清理項目），一次只做一個，從 PR-A 開始。"
non_goals:
  - An agent adding a requirement on its own
depends_on: [REQ-013]
refines: [REQ-003, REQ-008]
conflicts_with: []
superseded_by: []
superseded_reason: null
---

## Need

A review may find any problem, but every finding states how it relates to the
requirements. A gap in the requirements goes to the user as a decision card
and is not fixed in the same round. Only the user adds a requirement. Core
blockers block whatever the relation.

## Acceptance

- The `dev-review` report format and brief rules give every finding a
  `requirement_relation` of `in-scope`, `gap`, `no-requirement` or
  `unrelated`, and add the `REQ-GAP` category.
- A `REQ-GAP` becomes a decision card (add requirement, defer, reject); it is
  not fixed in the same round.
- `dev-plan` ingests a requirement from a `REQ-GAP` only after the user's
  decision, and its sources record the finding ID and that decision.
- `no-requirement` is `SCOPE-CREEP`; `unrelated` is residual risk or a
  follow-up and does not block; Core blockers (security, data loss,
  authorization, integrity) block for every relation.
- `docs/design-proposal.md` records D-016 in zh and EN with a Core-feedback
  note.

## Notes

The user wrote this text in a message queued in the same session and asked to
add it to memory. Evidence: the PR-A requirement_relation table in
`.dev/issue-4-commit-security/reviews/round-2.md`. Related: [[REQ-003]],
[[REQ-008]], [[REQ-012]], [[REQ-013]].
