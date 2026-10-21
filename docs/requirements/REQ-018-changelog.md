---
id: REQ-018
title: CHANGELOG with the upstream Core version
status: active
sources:
  - type: chat
    locator: "Claude Code session 2026-10-20 (PR #2 merge), user message at 08:14 UTC"
    quote: "另外，changelog是否要寫？並且要紀錄依據的上游engineering-workflow-core版本，這樣才好追蹤。而且如果這次不發行版本，後續處理版本發行時，也可以直接從changelog取出所需的訊息。"
  - type: chat
    locator: "Claude Code session 2026-10-20 (post-merge PR split), user message 1"
    quote: "先用 dev-plan 拆成 PR-A（D-015、R-REV-1、--evidence-file）、PR-B（D-013、D-014、D-016）、PR-C（D-009 到 D-012、context 成本那句話、CHANGELOG、core-feedback、清理項目），一次只做一個，從 PR-A 開始。"
  - type: chat
    locator: "Claude Code session 2026-10-21 (PR-C, Issue #8), user answer to the dev-plan decision cards (card 1 split PR-C into C1 and C2: (a) split; card 2 keep each rule in one place: (b) defer; card 3 open the Issue: (a) yes)"
    quote: "1a、2b、3a"
non_goals:
  - A release or a tag before FU-001 (GitHub Issue #3)
depends_on: []
refines: [REQ-007]
conflicts_with: []
superseded_by: []
superseded_reason: null
---

## Need

The repository keeps a changelog. It records the upstream engineering-workflow-core
version that the pack follows, so the version can be traced, and it holds what a
later release needs.

## Acceptance

- `CHANGELOG.md` follows Keep a Changelog and has an `[Unreleased]` section that covers Phase 1 (PR #2), PR #5, PR #7 and this change.
- It records the upstream Core pin: v0.1.1, tag object `7ce698fa853106c8ef44c4240c9334762da5ffb0`, commit `7b66978a76597d09be1b55ad199a969b4ee59c0f`, matching `vendor/engineering-workflow-core.lock.json`.

## Notes

No release yet: the first tagged release waits for FU-001 (its promotion
trigger in `.dev/followups.md`). Related: [[REQ-007]].
