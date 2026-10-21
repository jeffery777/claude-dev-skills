---
id: REQ-013
title: Decision card for human decisions
status: active
sources:
  - type: chat
    locator: "Claude Code session 2026-10-20 (PR #2 Merge Review 5), user message at 07:18 UTC (pasted decisions D-009 to D-014), D-014 heading"
    quote: "D-014 需要人類決策的描述格式（寫進 dev-review、dev-gate、dev-deliver 的輸出規則，對應 Core wf-writing）："
  - type: chat
    locator: "Claude Code session 2026-10-20 (PR #2 Merge Review 5), user message at 07:18 UTC, D-014 item 1"
    quote: "1. 每個 Needs Human Decision 的 finding，以及每個交給使用者的決策，都使用固定的決策卡片，欄位如下：問題（一句）、為什麼需要你決定、選項（每個選項分別寫做什麼、結果、風險、成本）、建議與理由、不決定的後果（會擋住什麼、什麼可以繼續）、證據（檔案和行號、指令輸出；事實與推論分開）。"
  - type: chat
    locator: "Claude Code session 2026-10-20 (PR #2 Merge Review 5), user message at 07:18 UTC, D-014 item 2"
    quote: "2. 英文依 ASD-STE100 原則撰寫；繁體中文依 Core 的簡明寫作原則調適：一句只講一件事、寫明主詞、術語保持一致、技術詞第一次出現時用白話解釋、不用模糊詞、不套用英文字數規則。"
  - type: chat
    locator: "Claude Code session 2026-10-20 (PR #2 Merge Review 5), user message at 07:18 UTC, D-014 item 3"
    quote: "3. 報告註明「依 ASD-STE100 原則編寫，未完成完整符合性驗證」，不得宣稱符合 STE。"
  - type: chat
    locator: "Claude Code session 2026-10-20 (PR #2 Merge Review 5), user message at 07:18 UTC, D-014 item 4"
    quote: "4. 在 dev-review 的 references 放一份決策卡片範本與一個正例。"
  - type: chat
    locator: "Claude Code session 2026-10-20 (post-merge PR split), user message 1"
    quote: "先用 dev-plan 拆成 PR-A（D-015、R-REV-1、--evidence-file）、PR-B（D-013、D-014、D-016）、PR-C（D-009 到 D-012、context 成本那句話、CHANGELOG、core-feedback、清理項目），一次只做一個，從 PR-A 開始。"
non_goals:
  - A claim of ASD-STE100 conformance
  - English word-count rules for Traditional Chinese
depends_on: []
refines: [REQ-005]
conflicts_with: []
superseded_by: []
superseded_reason: null
---

## Need

Every decision handed to the user uses one fixed card, so the user can decide
from the card alone. English follows ASD-STE100 principles; Traditional
Chinese follows the plain-writing adaptation of Core. No text claims STE
conformance.

## Acceptance

- `skills/dev-review/references/` has a decision-card template with the six
  fields and one positive example.
- `dev-review`, `dev-gate` and `dev-deliver` require the card for each
  Needs Human Decision finding and each decision handed to the user.
- `dev-core` states the Traditional Chinese plain-writing rules and the
  conformance note.
- `docs/design-proposal.md` records D-014 in zh and EN with a Core-feedback
  note.

## Notes

Origin: PR #2 and PR-A decisions were raised in changing formats. The PR-A
decision card 1 (scan PR text before posting, `.dev/issue-4-commit-security/reviews/round-2.md`)
is the positive example. Related: [[REQ-005]], [[REQ-012]], [[REQ-014]].
