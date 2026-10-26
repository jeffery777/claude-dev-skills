---
id: REQ-027
title: dev-plan - source trace of rule sentences (FU-022) and review units by risk and review cost
status: active
sources:
  - type: chat
    locator: "Claude Code session 2026-10-26 (orchestrator session, relayed to the D-019 session, PR-2), user answer to card D19-PR2-C1, part 4b: no dev-plan change in D-019; the dev-plan obligation of the rule path goes to FU-022 (also recorded in REQ-026 sources)"
    quote: "D19-PR2-C1：1a、2a、3a、4b 並併入 FU-022、5a"
  - type: chat
    locator: "Claude Code session 2026-10-26 (orchestrator session), user message on cost when slicing tasks (relayed to the FU-022 session)"
    quote: "你也可以有一些成本概念，任務拆太小，風險可控，但會多出許多審查成本。所以在推進任務時，可在可控的範圍內尊循規範儘量推進。"
  - type: chat
    locator: "Claude Code session 2026-10-26 (orchestrator session), user correction of the message above (relayed to the FU-022 session)"
    quote: "我要修正一下，拆任務時要考慮成本和風險，風險高的任務可以拆細，一次一項。風險不高的，在可控的範圍內儘量推進。所以其實也可以同時推二個以上的功能或修2個以上的bug，或是既加新功能也修bug。但這情況，是要開不同的Issue同時處理？或是同一個Issue 一起處理？這個我相信你有能力做出好的判斷，如果你認為風險高時，可以向我詢問和確認"
  - type: chat
    locator: "Claude Code session 2026-10-26 (orchestrator session, relayed to the FU-022 session, Issue #62), user answer to plan cards FU022-C1 (option a: the source trace applies to every spec or REQ from a user decision; settles FU-022 part 2, review card V5) and FU022-C2 (option a: the `.dev/followups.md` header prefers card IDs, rule IDs or section names, and names the commit with a line number, in this PR)"
    quote: "FU022-C1 選 a，C2 選 a"
  - type: chat
    locator: "Claude Code session 2026-10-26 (orchestrator session), task brief to the FU-022 session, scope line: the orchestrator relays the user's decision to deliver FU-022 and the slicing item in one PR in `skills/dev-plan/SKILL.md` (orchestrator text, not the user's own words; the user answered cards FU022-C1 and FU022-C2, whose card note named the step 6 change)"
    quote: "Scope, two items in one PR (user decision: bundle low-risk work to save review rounds):"
  - type: chat
    locator: "Claude Code session 2026-10-26 (orchestrator session, relayed to the FU-022 session, Issue #62), user answer to card FU022-R2-C1 after the R-VER-2 stop rule (review rounds 1 and 2): option (a), one review unit is one write node of the task graph; in a strict objective each slice is its own unit; the added `dev-deliver` sentence is removed; if the confirmation review finds a new blocker in the review-unit mechanism, option (b): defer the review units to a follow-up. Choosing (a) confirms need 2 as a pack rule"
    quote: "FU022-R2-C1 選 a（確認審查再出 blocker 就改 b）"
non_goals:
  - No change of the vendored Core or of the `dev-core` rule text; the slices stay the smallest coherent slices (Core `workflow.md`, Plan row).
  - No Issue-first or branch rule in the pack; Issue and branch rules are a per-project overlay (Core `authorization-and-stops.md`, `auth-scope`).
  - No change of the graph schema or of `graph.py`.
  - Earlier `.dev/followups.md` rows are not rewritten for the location rule.
depends_on: [REQ-026]
refines: []
conflicts_with: []
superseded_by: []
superseded_reason: null
---

## Need

1. **Source trace (FU-022).** The rule path of `dev-retro` gives
   `dev-plan` an obligation: for a spec from a `dev-retro` card, name for
   each rule sentence the user sentence that it comes from, and check that
   every condition of those words has a place. Until now only the card text
   carried it (card D19-PR2-C1 (4b), a management measure); `dev-plan`
   itself did not state it. By card FU022-C1 (a), the same trace applies to
   every spec or REQ from a user decision; a condition that the spec does
   not keep is listed with its reason and shown to the user, never dropped
   silently.
2. **Review units by risk and review cost.** Slices that are too small keep
   the risk under control but add review cost. High-risk work is split and
   done one item at a time. Work that is not high risk moves forward as far
   as it stays under control, also two or more features or fixes, or features and fixes
   together. The agent decides how the work maps to issues, and asks the
   user when it judges the risk high.
3. **Location references in follow-up rows (card FU022-C2 (a)).** A
   `file:line` reference drifts when lines are added above it. New rows
   prefer a card ID, a rule ID or a section name, and a line number names
   its commit.

## Acceptance

- `skills/dev-plan/SKILL.md` step 2 states the source trace for every spec
  or REQ from a user decision, a `dev-retro` card included; a condition
  that the spec does not keep is listed with its reason and shown to the
  user; the plan contains the trace; the review of the spec checks it, and
  a missing trace or a condition dropped without a reason is a finding;
  the trace does not limit a fix of a Core blocker (R-REV-4) or the
  `REQ-GAP` path (R-REV-3).
- `skills/dev-plan/SKILL.md` step 6 keeps "the smallest coherent slices"
  and adds review units: a review unit is one write node of the task graph
  (one task without a graph), which lists the DoD, verification and
  requirements of each of its slices; in a `strict` objective each slice is
  a unit of its own, and a high-risk slice (every R-REV-7 case and unknown
  risk included) always is, one at a time, with the early reviews and
  scans of R-REV-6; a slice re-assessed as high risk is re-planned as a
  unit of its own; in a `light` or `standard` objective, slices that are
  not high risk (`low` or `medium`) with a close review scope may share a
  unit, also when they mix features and fixes; the unit gets the highest
  risk and the strictest review mode of its slices; when joining adds risk or is unclear, a decision card goes to the
  user before slices are joined; the mapping to issues, branches and
  change requests follows the project's own rules, and separate change
  requests mean separate units.
- `skills/dev-deliver/SKILL.md` and the graph schema do not change: a unit
  is one node, so the loop reviews it once (card FU022-R2-C1 (a); findings
  FU22R1-002, FU22R2-001).
- `skills/dev-review/SKILL.md` step 2 tells the reviewer to check the
  source trace whenever `dev-plan` step 2 requires one (card FU022-C1 (a):
  the review checks the trace; findings FU22R1-003, FU22R2-002).
- The Output lists the source trace and the review units.
- No Core obligation is relaxed: an independent deep review checks the new
  text against Core `workflow.md` (Plan row, `wf-assumptions-and-options`),
  `review-and-security.md` (`review-risk-timing`) and
  `authorization-and-stops.md` (`auth-scope`).
- `.dev/followups.md` FU-022 status records the result, and its header
  states the location rule of need 3.

## Notes

- FU-022 part 2 (the trace for every spec from a user decision) was plan
  card FU022-C1; the user chose (a). Card FU022-C2 (a) added need 3.
- Review round 1 (deep): FU22R1-001 restored 「風險不高」 as "not high
  risk" (the first text said low risk only); FU22R1-002 and FU22R1-003
  carried the units and the trace check into `dev-deliver` and
  `dev-review`, which the first text left out; the merge card names these
  two additions for the user.
- Review round 2 (narrow): FU22R2-001 (the `dev-deliver` sentence
  deadlocked with the graph states) and FU22R2-004 (the rule judged risk
  per slice, while the user's words name high-risk tasks) fired the R-VER-2
  stop rule; card FU022-R2-C1 (a) replaced the mechanism with one unit per
  node and no joining in a `strict` objective. The card removed the
  `dev-deliver` sentence of round 1; the merge card names only the
  `dev-review` step 2 addition (finding FU22R3-001).
- "Review unit" is the word for the user's question of separate or shared
  issues: the pack decides the unit by risk and review cost; the project's
  own rules decide how a unit maps to issues and branches.
