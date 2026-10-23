---
id: REQ-025
title: On-demand loading of the original Core text; project readings of two unclear Core sentences (FU-005)
status: active
sources:
  - type: chat
    locator: "Claude Code session 2026-10-22 (FU-010 session, Issue #18), user question during the pause after review round 2 (the compressed digest exists because the pack was first assumed to load all at once)"
    quote: "壓縮的原因是因為任務一開始的時候以為技能包是一次全部載入。但其實可以像codex一樣設計成漸進式的按需載入。若是這樣，是否乾脆把原始的條文寫進來？"
  - type: chat
    locator: "Claude Code session 2026-10-22 (FU-010 session, Issue #18), user answer to FU-010 decision cards 5 and 6 (card 5: narrow PR-A and design on-demand loading first)"
    quote: "卡片5改走縮小PR-A＋先做按需載入設計，6a"
  - type: chat
    locator: "Claude Code session 2026-10-22 (FU-010 session, Issue #18), user requirement on Core defects and project tightenings"
    quote: "原始的core並非沒缺陷，有些條文沒寫得很明確，之前的對話中似乎有發現，如果現有的設計中有補強了原始的core的部份，不要退化了，並且應該在上游的core中開Issue回饋給core"
  - type: chat
    locator: "Claude Code session 2026-10-22 (orchestrator session, relayed to the FU-005 design session), user answer to the FU-005 design cards 1, 2, 3, 5a, 5b, 6a, 6b, 7′ and 8 (all option a, the recommendations)"
    quote: "那先照你的建議。我想先完成移植和功能完善。後續再來針對這部份優化"
  - type: chat
    locator: "Claude Code session 2026-10-22 (orchestrator session, relayed to the FU-005 design session), user answer to FU-005 design card 9 (remove the two sentences added in draft v3 to the card 5a reading)"
    quote: "9b"
  - type: chat
    locator: "Claude Code session 2026-10-22 (orchestrator session, relayed to the FU-005 design session), user approval of the FU-005 design spec"
    quote: "核准 FU-005 規格"
  - type: chat
    locator: "Claude Code session 2026-10-22 (orchestrator session, relayed to the FU-005 session), user answer to decision card PR1-006 (REQ-GAP from review round 1 of Issue #22: where the approved design record is kept; option a, in `.dev/issue-22-fu005-records/`)"
    quote: "PR1-006 選 a"
  - type: chat
    locator: "Claude Code session 2026-10-22 (orchestrator session, relayed to the FU-005 session), user answer after the PR #23 Merge Review: continue with the fixes of MR23-001 and MR23-002; decision card MR23-003 (REQ-GAP: CF-007 in docs/core-feedback.md still says to wait for the measurements; option a, one status line); approval to post the review and gate records of PR #23 as PR comments"
    quote: "繼續，MR23-003 選 a，同意貼紀錄"
  - type: chat
    locator: "Claude Code session 2026-10-23 (orchestrator session, relayed to the FU-005 PR-2 session, Issue #28), user answer to the source conflict between this file (each PR gets its acceptance here before it starts) and the spec's PR-2 file list (option a: PR-2 adds its acceptance here, in the first commit)"
    quote: "同意你的建議，選a，驗收條件放第一個commit"
  - type: chat
    locator: "Claude Code session 2026-10-23 (orchestrator session, relayed to the FU-005 PR-4 session), user answer to decision cards PR4-C1 (option a: R-STG-4, R-AUTH-4 and R-VER-1 have a sentence literally stricter than Core, so they stay word for word and get DL rows) and PR4-C2 (option a: a sentence whose broader prohibition makes the agent do less is looser, not stricter)"
    quote: "同意你的建議，C1a C2a"
  - type: doc
    locator: ".dev/followups.md, FU-005 row (from FU-010 cards 5 and 7, Issue #18)"
    quote: "Moved forward (FU-010 card 5): design progressive on-demand loading."
non_goals:
  - Optimizing the context cost now, for example reading Core by anchor section instead of whole files (design card 2 (b)); a later step decided on the FU-004 before and after measurements
  - Rewriting, translating or changing the vendored Core or the upstream Core; posting on engineering-workflow-core
  - Giving Core files to the implementer or the explorer, or letting any subagent follow Core text as instructions (design card 8)
  - A new rationale file for the rules (design card 6b; FU-010 card 2a no longer applies)
  - The `--prune` rule (FU-014)
  - Changes to codex-dev-skills or grok-build-dev-skills
depends_on: [REQ-007, REQ-016, REQ-022, REQ-023]
refines: [REQ-007]
conflicts_with: []
superseded_by: []
superseded_reason: null
---

## Need

`dev-core` is a compressed English digest of the vendored Core. The FU-010
audit (Issue #18, REQ-023) showed that the digest does not converge in
review: each of three rounds found Core conditions that it left out. The
user chose progressive on-demand loading: skills read the original Core text
at the stage that needs it. `dev-core` keeps the header, a stage map, every
rule that is stricter than Core or Claude-specific (word for word), and an
index line for each other rule. R-AUTH-5 and R-VER-3 become index lines that
keep their project readings. No project tightening regresses.

Two Core sentences can be read two ways (`authorization-and-stops.md:35`,
`workflow.md:76`; CF-009 items 4 and 5). The project writes its reading of
each, never looser than Core.

The user accepted that the context grows (estimated 1.5 to 1.85 times the
bytes per skill; tokens not measured) and that reading whole files is only
coarse on-demand loading. Correctness and finishing the port come first;
context optimization follows the FU-004 measurements.

The work is four sequential PRs (design decision D-020). Each PR starts
after the previous one merges (PR-2 also waits for the FU-004 baseline
run); the user decides each merge.

## Acceptance

- PR-1 (records):
  - `skills/dev-core/SKILL.md` R-AUTH-5 and R-VER-3 each carry the project
    reading that the user approved (design cards 5a, 5b, 9b), and no other
    rule text changes; CB-1 to CB-5 each name their origin (design card 6b).
  - `skills/dev-core/deltas.md` has a row for each project reading and for
    each existing tightening that had no row (design checklist table C);
    the existing rows do not change.
  - `docs/design-proposal.md` records D-020 in zh and EN; D-001 is marked as
    superseded by it (in effect from PR-2).
  - `docs/core-feedback.md` (zh and EN) records the upstream Issues
    engineering-workflow-core#21 to #27 for CF-001 to CF-006 and CF-009,
    and the two readings as input for engineering-workflow-core#27 items 4
    and 5; CF-007 gets one status line that points to D-020 (decision card
    MR23-003).
  - `.dev/followups.md`: FU-004 runs the with-the-pack arm before PR-2 and
    after PR-4 (design card 7′a); FU-005, FU-011 (design card 6a) and
    FU-012 (design card 6b) are updated; SR21B-001 (PR #21) is recorded as
    an input for PR-3.
  - The approved design spec and its no-regression checklist are in
    `.dev/issue-22-fu005-records/` (`fu005-spec.md`, `fu005-checklist.md`),
    word for word; masking of private paths or identifiers is the only
    change, and the folder's `README.md` records it (decision card PR1-006).
- PR-2 (Core reading; design 1.1 (A), 1.2 and 7.2):
  - `skills/dev-core/SKILL.md` has the two new header sentences of the
    design and a stage map with the reviewer role table; no rule text
    changes.
  - `skills/dev-core/deltas.md` has a row for the new header sentences; the
    existing rows do not change.
  - The first line of each of the 7 other skills says to read the Core files
    that the stage map lists for that skill.
  - `CHANGELOG.md` has an entry.
  - `bash scripts/validate.sh` passes; `git diff` of the skill files shows
    only added lines plus the 7 first lines; a reviewer confirms that the new
    header sentences loosen no project tightening.
- PR-3 (reviewer Core criteria; design 2.2 and 7.2):
  - `skills/dev-deliver/references/task-brief.md` has the "Core review
    criteria" line of the design.
  - `agents/dev-reviewer.md` and `agents/dev-security-reviewer.md` each have
    the paragraph of the design.
  - The restated rule text (the copies) does not change.
  - SR21B-001 (PR #21) is handled per its decision card.
  - `CHANGELOG.md` has an entry.
  - An early `dev-security-reviewer` design review and an R-REV-7 Security
    Diff Scan; the agent files are compared sentence by sentence with
    `dev-core`; `git diff` shows only added content.
- PR-4 (index lines; design 1.1 (A), (D), 1.3 and 7.2; decision cards
  PR4-C1 (a) and PR4-C2 (a)):
  - `skills/dev-core/SKILL.md`: 13 rules of checklist table D become index
    lines (rule ID, title, `[core: …]`): R-STG-1, R-STG-3, R-STG-5,
    R-RIG-4, R-AUTH-2, R-AUTH-3, R-AUTH-5, R-REV-5, R-EXH-1, R-CAP-2,
    R-CAP-3, R-DEL-1 and R-VER-3. R-AUTH-5 and R-VER-3 keep their project
    readings word for word. R-STG-4, R-AUTH-4 and R-VER-1 stay word for word
    (card PR4-C1 (a)). The other rule text, CB-1 to CB-5 and the stage map do
    not change. The first header sentence says that the file is the index of
    the vendored Core and the project's tightenings.
  - `skills/dev-core/deltas.md`: the DL-001 Difference records the new
    structure; DL-007 and DL-009 each get one note; new rows DL-031 to
    DL-033 for R-STG-4, R-AUTH-4 and R-VER-1 ("Recorded, text unchanged");
    no other row changes.
  - `skills/dev-core/source-map.md`: the Notes that this change makes false
    are updated; the table keeps its four columns.
  - `README.md` (zh and EN, the same meaning), `skills/dev-plan/SKILL.md`
    line 6 and `CHANGELOG.md` describe the new structure.
  - `docs/design-proposal.md` D-020 item 2 (zh and EN) says 33 items and
    13 rules, and keeps the rules whose text carries a DL-row tightening
    (MR23B-001).
  - `.dev/followups.md`: the FU-005, FU-011 (MR23B-001; the copy-gap input
    of Issue #33 item 2) and FU-012 (trigger) rows are updated.
  - `.dev/issue-22-fu005-records/README.md` records where PR-4 differs from
    the approved spec and checklist (cards PR4-C1, PR4-C2) and their known
    stale cross-references; the spec and the checklist do not change.
  - `bash scripts/validate.sh` passes. A reviewer confirms sentence by
    sentence that the deleted text has no sentence stricter than Core in the
    protective direction (card PR4-C2 (a)), that checklist tables A, B, C and
    E keep their places, and checks each table F row whose reader is a
    reviewer subagent and records the result (Issue #33 item 1). `grep`
    finds no stale wording.
- PR-2 to PR-4 each get their acceptance in this file before they start.
- No project tightening is loosened in any PR (the FU-005 no-regression
  checklist: every DL row, CB-1 to CB-5, D-013 to D-018, REQ-011 to REQ-025).

## Notes

- Design card 3 (a), as the user confirmed it: every skill always reads
  `authorization-and-stops.md`; this removes the failure path "the text was
  not at hand". It is one defense layer, not a guarantee.
- Design card 6b changes FU-010 card 2a (a new `rationale.md`): the reasons
  stay in the Reason and Evidence columns of `deltas.md` and in the CB origin
  lines. The user accepted it with the words of the fourth source.
- Design card 7′ (a) replaces the wait in REQ-022 `non_goals` ("waits for
  FU-004") and the FU-004 trigger "Before FU-005 is decided": the design is
  decided now, and FU-004 measures before PR-2 and after PR-4. REQ-022 keeps
  its text.
- REQ-024 is FU-013; this design uses REQ-025.
- "FU-005 checklist item C-n" and "table D" in `deltas.md`, `.dev/followups.md`
  and this file refer to `.dev/issue-22-fu005-records/fu005-checklist.md`.

Related: [[REQ-007]], [[REQ-016]], [[REQ-022]], [[REQ-023]], [[REQ-024]]
