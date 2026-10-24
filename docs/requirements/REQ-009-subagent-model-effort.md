---
id: REQ-009
title: Choose subagent model and effort per task
status: active
sources:
  - type: chat
    locator: "Claude Code session 2026-10-20 (claude-dev-skills setup), user message 3 (go-ahead to implement)"
    quote: "我在另一個對話補了 D-001（Core vendor+pin 並加 dev-core 精簡版）與 D-007（subagent 依任務選 model/effort）"
  - type: doc
    locator: "docs/design-proposal.md, section 7, D-007 (2026-10-20)"
    quote: "每個角色在 `agents/*.md` 設定預設的 `model` 與 `effort`；派工時由主代理依第 4 節的對照表逐次覆寫。"
  - type: doc
    locator: "docs/design-proposal.md, section 7, D-007 rule 3 (2026-10-20); R-DEL-2 did not carry it and no record said why (FU-018)"
    quote: "一輪修正沒有解決問題，或證據互相矛盾時，主代理重新評估模型與深度。"
  - type: doc
    locator: ".dev/followups.md, row FU-018 (user decisions 2026-10-24, relayed by the orchestrator session to the FU-015 PR-2 session)"
    quote: "Subagent model and effort: choose before dispatch, escalate after failure."
  - type: chat
    locator: "Claude Code session 2026-10-24 (orchestrator session, relayed to the FU-018 session), user answer to the FU-018 evaluation cards: card 1 (scope of the rule) and card 2 (Fable evaluation)"
    quote: "卡 1 選 b（effort 寫成 skill 的明確指示，涵蓋主 session 實作），卡 2 選 c"
non_goals:
  - A routing engine or a full model x effort matrix
  - "`fable` in the escalation order before an evaluation (D-007 rule 4; FU-018 card 2 (c): evaluation deferred)"
  - Changes to the agent file defaults (FU-018)
  - A script or test that reads transcripts; the effective setting stays `unknown` (FU-018)
depends_on: []
refines: [REQ-001]
conflicts_with: []
superseded_by: []
superseded_reason: null
---

## Need

Agents carry default model and effort; the main agent overrides them per task, with a floor for high-risk work.

## Acceptance

- Each agent file sets model and effort aliases.
- dev-deliver and dev-review state the per-task choice.

FU-018 (Issue #50; D-007 rule 3; cards 1 (b) and 2 (c)):

- R-DEL-2: the main agent chooses the model and effort before each dispatch and passes both (a dispatch that names only the model keeps the agent file's effort); the brief states why.
- The `dev-deliver` table gives an explicit model and effort for each role; the implementer row depends on the rigor tier (`light`: `sonnet`/`medium`; `standard`: `opus`/`high`, `sonnet`/`medium` only for a mechanical, clearly bounded slice; `strict`: `opus`/`high`). The `dev-review` mode table gives single values; `max` is an escalation step only. The `opus`/`high` floor is unchanged.
- When the main session implements, it records the model and effort that its own transcript records, or `unknown` with the reason. The user sets main-session effort in the app; when it is below the tier's implementer level, the plan says so.
- After one review and fix round that did not solve the problem, the main agent classifies the failure (R-VER-2) and escalates only for a quality failure, one step per such round: effort first (`low` -> `medium` -> `high`), then the model (`haiku` -> `sonnet` -> `opus`), then effort at `opus` (`xhigh`, then `max`). `fable` is not in the order.
- An escalated setting is never lowered for the rest of the node, and no setting goes below the floor. Escalation never resets the count of review rounds and never clears findings.
- The receipt and the review report record the requested setting, the setting that the transcript records (only the model and effort values are copied), or `unknown` with the reason, and `effective: unknown`.
- Design section 4 and the D-007 limits sentence agree with R-DEL-2. DL-034 records the tightening.

## Notes

Related: [[REQ-001]]
