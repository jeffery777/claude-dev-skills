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
  - type: chat
    locator: "Claude Code session 2026-10-24 (orchestrator session, relayed to the FU-018 session), user answer to the FU-018 round-1 review cards C1 to C6 (findings R1-002 and S1-005: the evidence-conflict trigger; R1-004: spec or mechanism failures; R1-005: whose setting escalates; R1-006 and S1-003: main-session effort under the floor; R1-007 and S1-004: R-REV-9 scan effort; R1-009: tracking of the deferred Fable evaluation)"
    quote: "C1a C2a C3a C4b C5b C6a"
  - type: chat
    locator: "Claude Code session 2026-10-25 (orchestrator session, relayed to the FU-018 session), user answer to the FU-018 round-2 review card C7 (findings R2-001 and S2-001: the floor check for the main session covered the effort only, not the model)"
    quote: "C7 選 a"
  - type: chat
    locator: "Claude Code session 2026-10-25 (orchestrator session, relayed to the FU-018 session), user answer to the FU-018 round-3 review card C8 (findings S3-001 and S3-002: deferred to FU-021)"
    quote: "C8 選 a，model ID 寫法一併記進 FU-021"
  - type: chat
    locator: "Claude Code session 2026-10-25 (orchestrator session, relayed to the FU-018 session), user answer to the PR #51 merge-review card C9 (finding MF-001: the cross-module trigger of the implementer row, restored from the FU-018 source; finding SF-001: how to find and read the transcript fields, deferred to FU-021)"
    quote: "C9-1 選 a，C9-2 選 a"
  - type: chat
    locator: "Claude Code session 2026-10-27 (orchestrator relay), user answer to the cost proposal cards C3 to C5 (C3: the R-REV-9 text scan at sonnet/high with a deterministic secret scan, a written exception to the R-DEL-2 floor; C4: light routine review at sonnet/medium with escalation triggers; C5: Dispatch defaults to the main session with a floor check); the user was told that C3 touches the floor (Issue #73); C3 was deferred later, see the I73-R1-C1 entry"
    quote: "C3 選 a，C4/C5 同意"
  - type: chat
    locator: "Claude Code session (orchestrator relay), user decision I69-M1 on the PR #70 deviation (the main session implemented a permission-boundary change before it checked its own model and effort against the R-DEL-2 floor; Issue #73)"
    quote: "I69-M1 a"
  - type: chat
    locator: "Claude Code session 2026-10-28 (orchestrator relay), user answer to the Issue #73 review round 1 cards I73-R1-C1 (option c: defer C3 to a follow-up, text scans stay opus/xhigh; findings S1-001 to S1-004, R1-003) and I73-R1-C2 (option a: once a C4 trigger applies to a node, every later review round of that node uses opus/high; finding R1-002)"
    quote: "I73-R1-C1 選 c，I73-R1-C2 選 a。工具該裝還是得裝，你可以建議你認為適合的工具。"
  - type: chat
    locator: "Claude Code session 2026-10-28 (orchestrator relay), user answer to cards I73-R2-C1 and I73-R2-C2 (I73-R2-C1 option a: one bounded fix round after the R-VER-2 stop rule, the floor check also before the main session fixes or writes any part of a node under the floor (finding S2-002), and acceptance of the main-session deviation S2-001; I73-R2-C2 option a: the brief of a light routine review at sonnet/medium lists triggers 1 to 3 and the reviewer reports whether any holds (finding S2-005))"
    quote: "I73-R2-C1 選 a，接受 S2-001；I73-R2-C2 選 a"
  - type: chat
    locator: "Claude Code session 2026-10-28 (orchestrator relay), user answer to the Issue #73 review round 3 card I73-R3-C1 (option a: a light routine-review report that does not say, for each of triggers 1 to 3, whether it holds counts as trigger 5 and the review re-runs at opus/high; finding S3-002)"
    quote: "I73-R3-C1 選 a"
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

FU-018 (Issue #50; D-007 rule 3; cards 1 (b) and 2 (c); review cards C1a, C2a, C3a, C4b, C5b, C6a; round-2 card C7a; round-3 card C8a; merge-review cards C9-1a and C9-2a):

- R-DEL-2: the main agent chooses the model and effort before each dispatch and passes both (a dispatch that names only the model keeps the agent file's effort); the brief states why.
- The `dev-deliver` table gives an explicit model and effort for each role; the implementer row depends on the rigor tier (`light`: `sonnet`/`medium`, `opus`/`high` for a cross-module or unclear slice; `standard`: `opus`/`high`, `sonnet`/`medium` only for a mechanical, clearly bounded slice in one module (card C9-1a); `strict`: `opus`/`high`). The `dev-review` mode table gives single values: the security review uses `xhigh` (`max` only when the user asks; card C3a) and the R-REV-9 commit and push scans use `xhigh` (card C5b). The `opus`/`high` floor is unchanged.
- When the main session implements, it records the model and effort that its own transcript records, or `unknown` with the reason. The user sets main-session model and effort in the app. For work under the floor, when that model is not `opus`, that effort is below `high`, or either is `unknown`, the main agent asks the user to switch to `opus`/`high` before it implements, or dispatches the implementation to `dev-implementer` at `opus`/`high` (cards C4b and C7a); for other work below the tier's implementer level, the plan says so.
- After one review and fix round that did not solve the problem, the main agent classifies the failure (R-VER-2) and escalates only for a quality failure and only the side that fixes (the implementer or the main session; reviewers keep the table values; card C3a), one step per such round: effort first (`low` -> `medium` -> `high`), then the model (`haiku` -> `sonnet` -> `opus`), then effort at `opus` (`xhigh`, then `max`). `fable` is not in the order. A failure that the spec, the acceptance criteria or the design caused is not a quality failure: it goes to the R-VER-2 stop rule and does not escalate (card C2a).
- When the evidence conflicts, the main agent also re-assesses the model and effort; the re-assessment alone does not escalate (D-007 rule 3; card C1a).
- An escalated setting is never lowered for the rest of the node, and no setting goes below the floor. Escalation never resets the count of review rounds and never clears findings.
- The receipt and the review report record the requested setting, the setting that the transcript records (the main agent fills it in from the model and effort fields only; a subagent does not read transcripts), or `unknown` with the reason, and `effective: unknown`.
- Design section 4 and the D-007 limits sentence agree with R-DEL-2. DL-034 records the tightening. The FU-018 row points to a new open row FU-020 for the deferred Fable evaluation (card C6a).

Issue #73 (D-022; user answers 「C3 選 a，C4/C5 同意」, 「I69-M1 a」, for review round 1 「I73-R1-C1 選 c，I73-R1-C2 選 a」 for review round 2 「I73-R2-C1 選 a，接受 S2-001；I73-R2-C2 選 a」 and for review round 3 「I73-R3-C1 選 a」):

- C3 is deferred (card I73-R1-C1 (c)): the R-DEL-2 floor has no exception, and the R-REV-9 text scan before posting keeps `opus`/`xhigh` as before. Follow-up FU-034 tracks C3.
- C4: at the `light` tier, routine review may use `dev-reviewer` at `sonnet`/`medium`. `dev-review` lists the escalation triggers once (the R-DEL-2 floor applies; packaging, installation, CI or dependencies; more than one module; a disputed finding; a part of the target that the reviewer could not check), decided before the dispatch from the diff and the plan and checked again after the review; a trigger then escalates to `opus`/`high`, and a trigger found after the review re-runs the review on the same target while the first report and its findings stay. The brief of a `light` routine review at `sonnet`/`medium` lists triggers 1 to 3 and asks the reviewer to report whether any of them holds; when the reviewer reports one, the review re-runs at `opus`/`high`, as for trigger 5, and the node keeps `opus`/`high` (card I73-R2-C2 (a); `task-brief.md` has the line); a report that does not say, for each of triggers 1 to 3, whether it holds counts as trigger 5 (card I73-R3-C1 (a); `review-report.md` has the field). Once a trigger applies to a node, every later review round of that node uses `opus`/`high`, never `sonnet`/`medium` again (card I73-R1-C2 (a)). `standard` and `strict` routine review stay `opus`/`high`. R-DEL-2 says that reviewers keep the table values with these triggers.
- C5: the `dev-deliver` Dispatch step runs a node in this session by default and delegates to one subagent when a listed condition applies (parallel read-only work or a broad read whose conclusion is all the session needs; a context too large; every required review or scan; the session does not meet the floor of the node and the user does not switch it; the user asks). Before this session runs any node under the floor (explore, implement or docs), and again before the main session fixes or writes any part of such a node itself (a fix round, a re-applied change, a record line in an owned file; card I73-R2-C1 (a), finding S2-002), it checks its own model and effort against the floor and the row of the node, dispatches the node or the fix at `opus`/`high` when the user does not switch, and never implements first (I69-M1); R-DEL-2 says that the check runs at the Dispatch step and before each such fix or write, `dev-deliver` step 5 and `dev-review` step 6 point to it, and `dev-deliver` says why `verify`, `gate` and `human_gate` nodes are outside it. DL-038 records the tightening. The `task-brief.md` "Why this model/effort" line names a `light` escalation trigger where it applies.
- Design section 4 and D-022 (both languages) agree with these rules. The agent file defaults do not change.

## Notes

Limit (review card C8 (a), Issue #50): the floor check of a main session runs before each node under the floor that it runs and before each fix or write of such a node (Issue #73); entry points that do not pass through `dev-deliver` steps 2 and 5 (resume through `dev-continue`, docs sync) and the status of record writes in owned paths are open (FU-035); no rule checks the `recorded` value after a floor dispatch, the rule names the alias `opus` while the transcript records a full model ID, and no rule says how to find the session's own transcript or read only its model and effort fields (card C9-2a). FU-021 tracks these gaps.

Related: [[REQ-001]]
