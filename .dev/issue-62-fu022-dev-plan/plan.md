# Issue #62 plan: FU-022 and review units

- Objective: REQ-027. Rigor `standard`: rule text of a public pack; the main
  risk is a wording that relaxes Core `workflow.md` (Plan row). No trust
  boundary is touched (R-REV-7 `not applicable`: text-only change of skill
  instructions and records; no executable, permission or dependency).
- Review units: one unit (one task node T1, deep review mode, one PR). The
  three needs are not high risk (T1 `medium`) and touch the same file set
  (user decision 2026-10-26 and cards FU022-C1 (a), FU022-C2 (a)).

## Source trace (`skills/dev-plan/SKILL.md` step 2, applied to this spec)

| User sentence (REQ-027 sources) | Condition | Place in the change |
| --- | --- | --- |
| 「任務拆太小，風險可控，但會多出許多審查成本」 | very small slices add review cost | step 6: "so that each small slice does not cost review rounds of its own" |
| 「可在可控的範圍內尊循規範儘量推進」 | follow the rules | step 6 keeps "smallest coherent slices"; each slice keeps its DoD, verification and requirement trace; the unit gets the strictest review mode |
| 同上 | within a controllable range | step 6: only slices that are not high risk and have a close review scope may share a unit |
| 「拆任務時要考慮成本和風險」 | weigh cost and risk | step 6: "choose the review units by risk and review cost" |
| 「風險高的任務可以拆細，一次一項」 | high-risk task: fine slices, one at a time | step 6: "In a `strict` objective, each slice is a review unit of its own"; a high-risk slice in any objective too; "Such units go one at a time, with the early reviews and scans that R-REV-6 requires" (card FU022-R2-C1 (a); finding FU22R2-004: the first text named slices only) |
| 「風險不高的，在可控的範圍內儘量推進」 | not high risk: move forward together | step 6: slices "that are not high risk (`low` or `medium`)" "may share one review unit" (in a `light` or `standard` objective); a unit is one graph node, so `dev-deliver` reviews it once |
| 「同時推二個以上的功能或修2個以上的bug，或是既加新功能也修bug」 | several features, several fixes, or both | step 6: "also when they mix features and fixes"; a unit is a group of slices (two or more) |
| 「是要開不同的Issue同時處理？或是同一個Issue 一起處理？這個我相信你有能力做出好的判斷」 | the agent decides the Issue mapping | Not kept in the pack. Reason: Core `authorization-and-stops.md` `auth-scope` makes Issue and branch rules a per-project overlay; step 6 says the mapping follows the project's own rules. The user's own instructions hold this judgment. Shown to the user in the PR description |
| 「如果你認為風險高時，可以向我詢問和確認」 | ask when the risk is high | step 6: a high-risk slice is always its own unit (no question needed); "When you judge that joining slices adds risk ... ask the user with a decision card" |
| (added, not from these words) | unknown risk is treated like high risk | step 6 bullet 1; R-RIG-2 (unknown never counts as low) |
| (added, not from these words) | every R-REV-7 case is its own unit | step 6 bullet 1. Reason: those slices need a Security Diff Scan (R-REV-7) and the early reviews of R-REV-6; joining them with other slices would mix that scope. Stricter than the words; shown to the user in the merge card |
| (added, not from these words) | a unit is delivered as one change; separate change requests mean separate units | step 6 definition and bullet 4. Reason: a shared review round covers one diff; the project's rules decide change requests (Core `auth-scope`) |
| (added, not from these words) | a unit is one graph node that lists each slice's DoD, verification and requirements; a slice re-assessed as high risk is re-planned alone | step 6 definition and bullet 1. Source: card FU022-R2-C1 (a) (user: 「FU022-R2-C1 選 a（確認審查再出 blocker 就改 b）」) |
| (added, not from these words) | record the units in the plan; Output lists them | step 6 "Record the units in the plan"; Output. Reason: the reviewer and a resumed session can see the units |
| 「FU022-R2-C1 選 a（確認審查再出 blocker 就改 b）」 | if the confirmation review finds a new blocker in the review-unit mechanism, defer the units (option b) | Process condition, not rule text: review round 3 found no such blocker (FU22R3-001 is a record NIT), so option (a) stays |
| 「FU022-C1 選 a」 (card option (a) text) | every spec or REQ from a user decision | step 2 bullet, first sentence |
| 同上 | a condition not kept: listed with its reason, shown to the user, never dropped silently | step 2 bullet |
| 同上 | the review checks the trace; a missing trace is a finding | step 2 bullet; Output "Source trace"; `skills/dev-review/SKILL.md` step 2, whenever step 2 requires a trace (findings FU22R1-003, FU22R2-002) |
| 同上 | no limit on a Core blocker fix (R-REV-4) or the `REQ-GAP` path (R-REV-3) | step 2 bullet, last sentence |
| 「D19-PR2-C1：…4b 並併入 FU-022…」 | `dev-retro` rule path obligation in `dev-plan` | step 2 bullet: "including a spec from a `dev-retro` card" |
| 「…C2 選 a」 (card option (a) text) | prefer card ID, rule ID or section name; a line number names its commit; old rows unchanged | `.dev/followups.md` header |
