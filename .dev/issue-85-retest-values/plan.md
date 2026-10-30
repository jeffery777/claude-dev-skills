# Issue #85 plan: re-test with dispatch values that differ from the agent file, re-test trigger and owner, floor-check pointer (Issue #79 slice A)

- Objective: GitHub Issue #85, Change 1 to 4, slice A of the tracking
  Issue #79. The basis is the user answer to the Issue #79 slicing cards,
  relayed by the orchestrator: 「I79-C1 a+d，I79-C2 a」 (four slices A to D,
  one sub-Issue each, A first; item 7 of #79 moves to a follow-up; slice A
  changes the re-test procedure text only).
- Rigor `strict`. Reason (R-RIG-1, re-assessed at the Discover of Issue
  #79 as R-RIG-2 says): the change edits pack rule text (`dev-deliver`) and
  REQ-009 of a public repository. It adds no behavior that an agent runs.
- Base: `main` 41f7256, branch `issue-85-retest-values` (created from
  Issue #85 on GitHub).

## Requirement trace

- REQ-009 (subagent model and effort): T1, the re-test procedure (MR77D-01),
  the trigger and the owner (S4-04, D4-02), the floor-check pointer
  (I77-RS1-04), the sources and the scope record.
- REQ-022 (each rule in one place): the `dev-deliver` sentence restates the
  R-DEL-2 exception for a host that cannot set the values with the same
  meaning; R-DEL-2 does not change.
- REQ-008 (requirements wiki): `docs/requirements/log.md` gets one new row.

## Source trace (dev-plan step 2)

Sources: the GitHub Issue #85 body (Goal, Change 1 to 4); the first
comment of Issue #79 (findings MR77D-01, PR #80 merge card M1 (a), and
I77-RS1-04); the Issue #79 body (Round 4 spec input S4-04 and D4-02;
Change 7 and its caveats; S3-03 and S3-05); and the user answer
「I79-C1 a+d，I79-C2 a」 (Claude Code session 2026-10-30, orchestrator
relay).

- From the user answer: four slices A to D, one sub-Issue each, A first;
  Issue #79 tracks them; item 7 of #79 moves to a follow-up (FU-045);
  slice A changes the re-test procedure text only and does not run it.
  The reason for moving item 7 is the card's reason, not the user's words.
- From MR77D-01 (M1 (a)): dispatches whose values differ from the agent
  file (`dev-explorer` with `opus`/`high`, `dev-reviewer` with
  `opus`/`xhigh`), headless and desktop, and a parent session effort that
  differs from the agent files.
- From design review round 1, not from the user's words: the parent model
  differs too (`sonnet`, D1-01 and S1-01); the maintainer starts or sets the
  parent session and a run is void when the parent transcript does not
  record the planned values (D1-02, S1-04); a step passes only on the
  expected value, for the Issue #77 steps too (D1-07); the trigger for each
  surface and the `unknown` case (D1-05, S1-03); the wording of the version
  sources (D1-06); FU-045 caveats (D1-04, S1-05), where "copy only the
  effort token" of Issue #79 Change 7 becomes "exactly one of the level
  names".
- From implementation review rounds 1 and 2, not from the user's words:
  the maintainer starts the headless parent run (I85-S1-03); the FU-045
  caveats are split by source and keep one exclusion for every evaluation
  (I85-S1-01, I85-R2-02); FU-046 also asks when a void run stops.
- From the user answer 「I85-C1 a，I85-C2 a」 (Claude Code session
  2026-10-30, orchestrator relay): the REQ-GAP of a failed re-test step is
  deferred to FU-046; FU-047 and FU-048 track two residual risks of the PR
  #86 Merge Review.
- From S4-04 and D4-02: the trigger and the owner of the re-test.
- From I77-RS1-04: the `dev-deliver` pointer, worded as R-DEL-2 (D1-03,
  S1-02).

## Dispatches and floor check

The main session read its own setting before it wrote this plan and again
before the round 1 and round 2 fixes: its transcript records
`claude-opus-5-5`/`high` on the turns of this slice, and `get_session`
gives the same; requested value `unknown` (set by the session that started
it). Observations of the Issue #79 Discover stay outside the repository
(card I79-C2 (a)). The fixes ran at `opus`/`high`.

The main session wrote the record lines of the second commit (cards
I85-C1 and I85-C2; FU-047, FU-048, the log row, the CHANGELOG and this
plan) itself. Its floor check for that write rested on the read of its
transcript at the end of the turn before; it did not read the transcript
again right before the write (Merge Review finding MR85B-01). A read after
the write shows `claude-opus-5-5`/`high` on every turn of that write: the
values met the floor, but the timing of the check did not meet decision
I69-M1 (check before the write, never after), and a later read never
replaces that check. The main session read its transcript again before
it wrote this paragraph: `claude-opus-5-5`/`high`.

| Node or step | Agent | Requested | Recorded | Effective |
| --- | --- | --- | --- | --- |
| Discover survey | `dev-explorer` | `opus`/`high` | `claude-opus-5-5`/`high` | `unknown` |
| Design review round 1 | `dev-reviewer`, `dev-security-reviewer` | `opus`/`xhigh` | `claude-opus-5-5`/`xhigh` | `unknown` |
| Issue #85 text scan | `dev-security-reviewer` | `opus`/`xhigh` | `claude-opus-5-5`/`xhigh` | `unknown` |
| T1 | `dev-implementer` | `opus`/`high` | `claude-opus-5-5`/`high` | `unknown` |
| Implementation review round 1 | `dev-reviewer`, `dev-security-reviewer` | `opus`/`xhigh` | `claude-opus-5-5`/`xhigh` | `unknown` |
| Implementation review round 2 and commit scan | `dev-reviewer`, `dev-security-reviewer` | `opus`/`xhigh` | `claude-opus-5-5`/`xhigh` | `unknown` |

Recorded values come from the model and effort fields of each transcript.

## Implementation review

Round 1: deep, no MUST-FIX, 2 SHOULD-FIX, 2 NIT; security (Security Diff
Scan), PASS, 1 SHOULD-FIX, 2 NIT.

| ID | Severity | Disposition |
| --- | --- | --- |
| I85-R1-01 | SHOULD-FIX | Fixed: this Source trace section |
| I85-R1-02 | SHOULD-FIX | Card I85-C1 (a) (user answer, relayed: 「I85-C1 a，I85-C2 a」): REQ-GAP I79A-D1-08 is Deferred to FU-046 |
| I85-R1-03 | NIT | Fixed: the CHANGELOG entry and the log row name the runs that dispatch an agent |
| I85-R1-04 | NIT | Fixed in round 2 (I85-R2-01): line wrapping in the CHANGELOG, `dev-deliver` and this plan |
| I85-S1-01 | SHOULD-FIX | Fixed: FU-045 splits the `CLAUDE_EFFORT` read, the version check (S3-03) and host metadata (S3-05) |
| I85-S1-02 | NIT | Fixed: the slice C spec input names the `dev-deliver` sentence |
| I85-S1-03 | NIT | Fixed: the maintainer starts the headless parent run |

Round 2 (narrow, the round 1 fixes): deep, no MUST-FIX or SHOULD-FIX, 3
NIT, no new blocker (R-VER-2); the commit scan and the check of the round
1 security fixes, PASS, 2 NIT.

| ID | Severity | Disposition |
| --- | --- | --- |
| I85-R2-01, I85-S2-02 | NIT | Fixed: line wrapping |
| I85-R2-02, I85-S2-01 | NIT | Fixed: FU-045 keeps one exclusion (environment, process arguments, credential or account files, binary contents) for every evaluation |
| I85-R2-03 | NIT | Fixed: the log row, the CHANGELOG and FU-046 say "proposed deferral pending card I85-C1"; FU-046 names the implementation review source; the source trace keeps the implementation review findings apart |

## Design reviews

| Round | Target | Result | Outcome |
| --- | --- | --- | --- |
| 1 | Design rev 1 | deep: no MUST-FIX, 5 SHOULD-FIX, 2 NIT, 1 REQ-GAP; security: PASS, 5 SHOULD-FIX, 2 NIT | rev 2 applies every in-scope finding; the REQ-GAP I79A-D1-08 is not applied: card I85-C1 (a) deferred it to FU-046 |

Both reviewers: requested `opus`/`xhigh`; recorded
`claude-opus-5-5`/`xhigh` from the transcript fields; effective `unknown`.
Round 1 raised no blocker, and every finding except the REQ-GAP
I79A-D1-08 was inside the requirements, so the implementation review checks
rev 2 (as Issue #77 did with its rev 4 findings); there is no round 2 of
the design review.

## Spec input for slice C (Issue #79)

- Security round 1 residual risk: R-DEL-2 does not say that a host whose
  ability to set a value is unknown counts as a host that cannot set it.
  Slice C takes it into the rule for surfaces that cannot be read back.
- The `dev-deliver` floor-check sentence restates the R-DEL-2 exception for
  a host that cannot set the values; it changes with R-DEL-2 (I85-S1-02).

## Spec input for slice B (Issue #79)

- The re-test compares level names and the aliases `sonnet` and `opus`
  with the full model IDs that transcripts record; slice B's exact model ID
  allowlist (FU-021 (3)) should cover this comparison too (implementation
  review round 1 residual risk).

## Non-goals

R-DEL-2 and its tested-host record (no re-test, card I79-C2 (a)); agent
files and `check_pack` pins; a new D-0xx entry; slices B, C and D;
FU-021 item (2), FU-035, FU-038, FU-044.
