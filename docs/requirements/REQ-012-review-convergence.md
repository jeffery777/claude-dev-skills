---
id: REQ-012
title: Review convergence
status: active
sources:
  - type: chat
    locator: "Claude Code session 2026-10-20 (PR #2 Merge Review 5), user message at 07:18 UTC (pasted decisions D-009 to D-014), D-013 heading"
    quote: "D-013 Review 收斂規則（寫進 dev-review、dev-gate 與 dev-core 的 delta）："
  - type: chat
    locator: "Claude Code session 2026-10-20 (PR #2 Merge Review 5), user message at 07:18 UTC, D-013 item 1"
    quote: "1. 嚴重度門檻：MUST-FIX 只限 Core 的阻擋項；SHOULD-FIX 必須有可重現的失敗，並影響需求、DoD 或文件寫明的行為；NIT 只限 delta 造成的回歸或不實的文件內容；其餘列為 residual risk，不列為 finding。"
  - type: chat
    locator: "Claude Code session 2026-10-20 (PR #2 Merge Review 5), user message at 07:18 UTC, D-013 item 2"
    quote: "2. 修補前先分類：每個 finding 依 Core wf-assumptions-and-options 判讀為必要修正、值得改善、維持現狀或需要人類決策。管理措施（流程、文件、人工檢查）是有效的修補方式，但必須寫明責任人、可驗證的前提與失效時的處理。"
  - type: chat
    locator: "Claude Code session 2026-10-20 (PR #2 Merge Review 5), user message at 07:18 UTC, D-013 item 3"
    quote: "3. 新增機制前，必須說明它的獨特作用，以及對應哪一條需求；說不出來就列為 SCOPE-CREEP。"
  - type: chat
    locator: "Claude Code session 2026-10-20 (PR #2 Merge Review 5), user message at 07:18 UTC, D-013 item 4"
    quote: "4. 修正後、push 前，先做窄範圍的獨立確認；完整 Merge Review 可以重用未受影響部分的證據，但要寫明理由與覆蓋範圍。"
  - type: chat
    locator: "Claude Code session 2026-10-20 (PR #2 Merge Review 5), user message at 07:18 UTC, D-013 item 5"
    quote: "5. 連續兩輪 review 仍出現新的阻擋項時，停下來重新評估規格、驗收標準與做法，不直接進入下一輪修正。"
  - type: chat
    locator: "Claude Code session 2026-10-20 (PR #2 Merge Review 5), user message at 07:18 UTC, D-013 item 6"
    quote: "6. 審查紀錄的保存方式不能產生新的 head（例如寫成 PR comment），避免出現結構性的循環。"
  - type: chat
    locator: "Claude Code session 2026-10-20 (PR #2 Merge Review 5), user message at 09:19 UTC (on the PR-A round-2 findings)"
    quote: "其實主要是希望發現問題要修，但要想一下正確的修補方式、是否是在符合需求的範圍內的修補？或是原本需求沒考量到的缺陷必須先改需求文件再進行修補。而不是看到問題就順手修，最終過度設計。"
  - type: chat
    locator: "Claude Code session 2026-10-21 (PR-B, Issue #6), user answer to decision card 1 (REQ-GAP G-001 from finding B1-004: add the stop-rule trigger 'the same mechanism needed fixes and produced new problems in two consecutive rounds'), selected option"
    quote: "(a) Add it (Recommended)"
  - type: chat
    locator: "Claude Code session 2026-10-20 (post-merge PR split), user message 1"
    quote: "先用 dev-plan 拆成 PR-A（D-015、R-REV-1、--evidence-file）、PR-B（D-013、D-014、D-016）、PR-C（D-009 到 D-012、context 成本那句話、CHANGELOG、core-feedback、清理項目），一次只做一個，從 PR-A 開始。"
  - type: issue
    locator: "GitHub Issue #68 body, Goal (user decisions of 2026-10-27 on cards E1 and E2 and item 4 of the cost proposal; E2: evidence bound to the tree)"
    quote: "E1 選 A，E2 同意"
non_goals:
  - D-009 to D-012, the context-cost sentence, CHANGELOG, core-feedback and cleanups (PR-C)
  - Changes to engineering-workflow-core, codex-dev-skills or grok-build-dev-skills
depends_on: []
refines: [REQ-003]
conflicts_with: []
superseded_by: []
superseded_reason: null
---

## Need

Review rounds converge. Severity follows fixed thresholds. Each finding is
classified before anyone fixes it, and a fix stays inside the requirements. A
new mechanism names its unique role and its requirement. Fixes get a narrow
independent confirmation before a push. Two rounds in a row with new blockers,
or the same mechanism needing fixes and producing new problems in two rounds
in a row, stop the fix loop for a re-evaluation. Review records never create a new head.

## Acceptance

- `dev-core` defines the severity thresholds, classification before fixing,
  the narrow confirmation before a push, evidence reuse in the Merge Review
  for provably unaffected parts with reason and coverage, the stop rule, and record storage without a new
  head; `deltas.md` records each difference from Core.
- Issue #68 (E2): `dev-core` R-EXH-3 binds reusable content evidence to the
  tree and the diff. When a new head differs from a reviewed head only in
  identities or messages (the same base, the same number of commits, and
  equal trees, one by one, for the commits in
  `git rev-list --reverse <base>..<head>`), the content evidence of the
  reviewed head may be reused when the other R-CAP-3 conditions still
  match and the review records the tree comparison as the reason and the
  coverage (review round 4, R4-002); `git range-diff` is only a view. Other
  partial reuse follows the existing R-CAP-3 sentence (review round 1,
  R1-004). The new review still binds the exact
  base, head and merge-base and gives its own verdict; this is reuse inside
  a complete review, never a skipped review. `dev-gate` never reuses a
  previous head's verdict. D-021 records the decision.
- `dev-review` and `dev-gate` apply these rules.
- `docs/design-proposal.md` records D-013 in zh and EN with a Core-feedback
  note.

## Notes

Origin: PR #2 Merge Reviews 1 to 5 did not converge (Merge Reviews 6 and 7
had no findings). Evidence: the PR-A
re-evaluation in `.dev/issue-4-commit-security/reviews/round-2.md` applied
these rules before they were in the pack. The second stop-rule trigger was
added by the user's answer to decision card 1 of PR-B (finding B1-004,
`.dev/issue-6-review-convergence/reviews/round-1.md`). Item 3 is already covered by
`dev-core` R-RIG-3. Related: [[REQ-003]], [[REQ-013]], [[REQ-014]].
