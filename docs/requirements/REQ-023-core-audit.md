---
id: REQ-023
title: dev-core is never weaker than Core - full audit and R-WRT-1 (FU-010)
status: active
sources:
  - type: chat
    locator: "Claude Code session 2026-10-22 (FU-006 session, Issue #16), user answer to decision card 6 (method after the R-VER-2 stop rule in review round 2)"
    quote: "6a，FU-006 合併後 FU-010 列為下一項並做完整盤點"
  - type: chat
    locator: "Claude Code session 2026-10-22 (FU-006 session, PR #17), user answer to decision card 8 (scope of acceptance item 1 after Merge Review finding MR17-001)"
    quote: "8a。reviewer 找到的那幾處（platform-profile.md、dev-review、dev-plan 等）請明確列入 FU-010。"
  - type: chat
    locator: "Claude Code session 2026-10-22 (FU-010 session, Issue #18), user answer to the FU-010 decision cards (card 1 split into three sequential PRs; card 2 placement of the per-rule notes; card 3 reviewer temporary files)"
    quote: "1a 2a 3d"
  - type: chat
    locator: "Claude Code session 2026-10-22 (FU-010 session, Issue #18), user answer to decision card 4 (review finding R1-004: `git fetch --prune` before a push and the destructive-action list of R-AUTH-3)"
    quote: "同意你的建議，選a。"
  - type: chat
    locator: "Claude Code session 2026-10-22 (FU-010 session, Issue #18), user remark before deciding decision card 5 (R-VER-2 stop rule after review round 2)"
    quote: "壓縮的原因是因為任務一開始的時候以為技能包是一次全部載入。但其實可以像codex一樣設計成漸進式的按需載入。若是這樣，是否乾脆把原始的條文寫進來？"
  - type: chat
    locator: "Claude Code session 2026-10-22 (FU-010 session, Issue #18), user answer to decision cards 5 (approach after the stop rule) and 6 (implementer deletions)"
    quote: "卡片5改走縮小PR-A＋先做按需載入設計，6a"
  - type: chat
    locator: "Claude Code session 2026-10-22 (FU-010 session, Issue #18), user requirement relayed by the orchestrator session during the pause after review round 3"
    quote: "原始的core並非沒缺陷，有些條文沒寫得很明確，之前的對話中似乎有發現，如果現有的設計中有補強了原始的core的部份，不要退化了，並且應該在上游的core中開Issue回饋給core"
  - type: chat
    locator: "Claude Code session 2026-10-22 (FU-010 session, Issue #18), user answer to decision card 7 (R-VER-2 stop rule after review round 3)"
    quote: "繼續，7a"
  - type: doc
    locator: ".dev/followups.md, FU-010 row (FR1-R10, Issue #16 review round 1; MR17-001, PR #17)"
    quote: "Compare R-WRT-1 with Core wf-writing items 1 to 6 sentence by sentence; tighten R-WRT-1 and record the correction in `deltas.md`"
non_goals:
  - Adding Core obligations or conditions that the digest leaves out or states more loosely (cards 5 and 7a: input for the on-demand loading design, FU-005)
  - Opening Issues on engineering-workflow-core (the orchestrator session drafts them with the user from CF-009)
  - Rule IDs on restated rule text outside the Issue #16 inventory (FU-011; scope re-decided after the design)
  - A per-rule note on why each rule exists (FU-012; scope re-decided after the design)
  - The reviewer test-cache measure and the implementer deletion rule (FU-013, cards 3d and 6a)
  - Changing the agent files or the references given to subagents (card 1a of Issue #16)
  - Splitting dev-core (FU-005)
  - Changes to engineering-workflow-core, codex-dev-skills or grok-build-dev-skills, or an upstream Issue
depends_on: [REQ-007]
refines: [REQ-022]
conflicts_with: []
superseded_by: []
superseded_reason: null
---

## Need

`dev-core` may rephrase, compress or tighten Core, never relax it (REQ-007).
FU-010 found R-WRT-1 weaker than Core `wf-writing`. The user asked for a full
audit of `dev-core` against Core after FU-006 (card 6a) and moved the restated
text that PR #17 left without IDs into FU-010 (card 8a). The user split the
work into three sequential PRs (card 1a); this REQ is PR-A. Review rounds 1
and 2 both found new blockers, because the compressed digest kept leaving out
Core words (R-VER-2 stop rule). The user then narrowed PR-A (card 5): fix only
the sentences that are looser than Core and R-WRT-1, state in `dev-core` that
a left-out Core obligation still applies, and design on-demand loading of the
original Core text next (FU-005). Review round 3 found more looser sentences
(the stop rule again); the user chose card 7a: the header hands every shorter or
looser rule to its Core section, and keeps every stricter project rule.

## Acceptance

- An audit table rates every `dev-core` rule (R-*, CB-1 to CB-5) against its
  Core source as equal, tighter, weaker or dev-core-only, with evidence
  (`.dev/issue-18-core-audit/audit.md`).
- R-WRT-1 covers Core `wf-writing` items 1 to 6 and the spot-check; a
  sentence-by-sentence table shows each item.
- The `dev-core` header states that where a rule is shorter or looser than
  its cited Core section, that Core section governs, and that a stricter rule
  (for example DL tightenings, CB-1 to CB-5, user decisions) still applies
  (card 7a). The
  audit lists every gap as input for FU-005, and the change is recorded in
  `deltas.md` (DL-017).
- No project tightening regresses: no DL row except the new DL-017, no CB
  binding, no other skill and no agent file changes.
- `git fetch --prune` before a push is recorded in R-REV-9 as a project
  policy (card 4).
- The FU-006 row in `.dev/followups.md` states the card 8a limit (MR17B-001).
- Core-level observations are recorded as Core-feedback candidates in
  `docs/core-feedback.md` (CF-009), each with the Core file and line, in both
  languages, with the status "not proposed".
- `.dev/followups.md` records the design step (FU-005), FU-011 and FU-012 as
  re-decided after the design, and FU-013 with cards 3d and 6a.

## Notes

Related: [[REQ-007-core-authority]], [[REQ-022-single-source-rules]],
[[REQ-019-core-feedback]].
