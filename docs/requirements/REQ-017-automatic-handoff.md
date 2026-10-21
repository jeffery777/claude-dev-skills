---
id: REQ-017
title: Automatic handoff evaluation in dev-continue
status: active
sources:
  - type: chat
    locator: "Claude Code session 2026-10-20 (PR #2 Merge Review 5), user message at 07:18 UTC (pasted decisions D-009 to D-014), opening line"
    quote: "請先重讀 docs/design-proposal.md，再新增以下決策："
  - type: chat
    locator: "Claude Code session 2026-10-20 (PR #2 Merge Review 5), user message at 07:18 UTC (pasted decisions D-009 to D-014), D-012"
    quote: "D-012 自動交接：dev-continue 在每個工作項目完成時評估是否換對話，依據是 review/fix 輪數、階段邊界與工作量，context 用量只當參考。決定要換時，自動寫好 checkpoint 並 commit，再提出新 session 卡片附上完整交接說明，由使用者按下確認；原 session 交接後就停止寫入。不宣稱能精確讀取 context 用量。"
  - type: chat
    locator: "Claude Code session 2026-10-20 (post-merge PR split), user message 1"
    quote: "先用 dev-plan 拆成 PR-A（D-015、R-REV-1、--evidence-file）、PR-B（D-013、D-014、D-016）、PR-C（D-009 到 D-012、context 成本那句話、CHANGELOG、core-feedback、清理項目），一次只做一個，從 PR-A 開始。"
  - type: chat
    locator: "Claude Code session 2026-10-21 (PR-C, Issue #8), user answer to the dev-plan decision cards (card 1 split PR-C into C1 and C2: (a) split; card 2 keep each rule in one place: (b) defer; card 3 open the Issue: (a) yes)"
    quote: "1a、2b、3a"
  - type: chat
    locator: "Claude Code session 2026-10-21 (PR-C, Issue #8), user answer to PR-C1 review decision card 1 (REQ-GAP from finding B1-002: once a PR exists, commit the checkpoint to the PR branch or not; options (a) do not commit after a PR exists, (b) commit and accept the new head, (c) defer)"
    quote: "選 a。另外，PR 建立後，checkpoint 的重點改貼成 PR comment（照 REQ-011 先掃描），讓其他 clone 也能接手。"
non_goals:
  - A claim that the agent can read its exact context usage
  - Starting a new session without the user's confirmation
depends_on: []
refines: [REQ-006]
conflicts_with: []
superseded_by: []
superseded_reason: null
---

## Need

At each completed work item, `dev-continue` evaluates whether to switch to a new
session. The basis is the number of review and fix rounds, stage boundaries and
the workload; context usage is a reference only. When it decides to switch, it
writes the checkpoint and commits it without asking, then offers a new-session
card with a full handoff brief. The user confirms. After the handoff, the old
session stops writing. Once a PR exists, the checkpoint is not committed; its
key points go into a PR comment, scanned first, so another clone can take over.

## Acceptance

- Once a PR exists, the checkpoint is not committed; its key points are posted as a PR comment after the R-REV-9 scan, so another clone can take over (user's answer to PR-C1 decision card 1).
- `skills/dev-continue/SKILL.md` states the evaluation trigger, the basis, the checkpoint commit (after the R-REV-9 scan), the new-session offer with the brief, the user's confirmation, and that the old session stops writing.
- No text claims that the agent reads its exact context usage.
- `docs/design-proposal.md` records D-012 in zh and EN with a Core-feedback note.

## Notes

PR-C1 decision card 1 (finding B1-002, `.dev/issue-8-decisions-changelog-core-feedback/reviews/round-1.md`):
the user chose (a) and added the PR comment. The checkpoint commit keeps every commit rule: the R-REV-9 scan, `commit_state`,
and R-EXH-3 (a commit on a PR branch makes a new head). Related: [[REQ-006]],
[[REQ-011]].
