# Issue #77 plan: model and effort read-back test; `dev-implementer` defaults and pinned agent values

- Objective: GitHub Issue #77 (body updated 2026-10-29 after the design
  decisions). Step 1 is a read-only controlled test of what the host
  requests for sessions and subagents. Steps 2 to 4 record the result,
  change the `dev-implementer` defaults, pin the agent values in
  `check_pack`, and add a follow-up row.
- Rigor `strict`. Reason (R-RIG-1, re-assessed at Discover): the change
  touches the R-DEL-2 floor rule, which protects security work, a public
  agent file and the rule text that the pack publishes; the Issue's Process
  line also says `strict`. The design got an independent deep and security
  review before implementation (see Design reviews).
- Base: `main` 29f3e33, branch `77-effort-readback`.

## Requirement trace

- REQ-009 (subagent model and effort; R-DEL-2, DL-034, DL-040): the
  recorded-value sentence, the tested-host record, the host that cannot set
  values, the agent file, the pins, the explore row, the re-test procedure.
- REQ-011 (R-REV-9 scans): no text change; REQ-009 Notes say what the scans
  rest on.
- REQ-022 (each rule in one place): every new rule sentence is in
  `dev-core` once; `task-brief.md`, the `dev-deliver` table, section 4 and
  D-024 restate it with the same meaning.
- REQ-008 (requirements wiki): `docs/requirements/log.md` gets a new row
  only.

## Source trace

GitHub Issue #77, and the user answers (Claude Code session 2026-10-29,
orchestrator relay to the Issue #77 session):
「C1 a，C2 a，C3 a，C4 a，C5 a，C6 a，C7 a。」;
「R2-C1 a，同意 C2、C3、C4 移到新 Issue；R2-C2 移到新 Issue」;
「R3-C1 a，同意 E 移到新 Issue」.
The design cards, the raw test output and the review reports stay outside
the repository; the raw output holds private data (R-AUTH-7).

## Step 1: controlled test (facts)

Headless Claude Code 2.1.312 and the desktop app with its bundled Claude
Code 2.1.309, 2026-10-29. See D-024 for the result. Not tested: other
surfaces (cloud, SSH, interactive terminal), other models and levels for
dispatches, a same-turn read after a setting change.

## Design reviews (before implementation)

Each round: `dev-reviewer` (deep) and `dev-security-reviewer`, requested
`opus`/`xhigh`; the main agent read the model and effort fields of each
reviewer's transcript: `opus`/`xhigh` on every turn.

| Round | Target | Result | Outcome |
| --- | --- | --- | --- |
| 1 | Design card rev 1 (options A to F) | deep 3 MUST-FIX; security 2 MUST-FIX | rev 2; user cards I77-C1 to I77-C7 |
| 2 | rev 2 (read-back gate with a script) | deep 1 MUST-FIX; security BLOCKED, 3 MUST-FIX | R-VER-2 stop rule; card I77-R2-C1 (a): the gate moves to a new Issue |
| 3 | rev 3 (reduced scope with session read-back) | deep 2 MUST-FIX; security BLOCKED, 2 MUST-FIX | R-VER-2 stop rule; card I77-R3-C1 (a): only tightening and records |
| 4 | rev 4 (exact rule text, pin design) | no MUST-FIX; SHOULD-FIX and NIT findings | the findings are applied in the implementation |

Round 4 findings applied: the sentence for a host that cannot set values
names `dev-implementer` directly (S4-01, D4-03); the REQ-009 transcript
non-goal keeps "test" and names the repository (S4-02); inferred values are
not recorded values (S4-03); the re-test procedure names a version source
and the limits of the run (S4-04, D4-02); FU-038 names no folder or ID
(S4-05); the collision message has one line for each stem and keeps the
read-only wording (S4-06, D4-06); "pass the model and the effort" (S4-07);
FU-038 says that the dispatch input fields need the new Issue's rule or a
recorded decision (S4-08); section 4 gets the sentence for a host that
cannot set values (D4-01); the explore cell keeps its first two parts
(D4-04); the CHANGELOG Issue #73 entry gets a note (D4-05).

Round 1 to 3 findings that moved to the read-back gate Issue (#79) are its spec
input.

## Review-and-Fix

Round 1 (diff identity `44438da5…`): deep `dev-reviewer` and security
`dev-security-reviewer` (Security Diff Scan), requested `opus`/`xhigh`,
recorded `opus`/`xhigh` from the transcript fields.

| ID | Severity | Disposition |
| --- | --- | --- |
| I77-R1-01 | MUST-FIX | Fixed: R-DEL-2 has the two rev 4 A2 clauses again ("not a check that an agent runs"; the maintainers run the test again when Claude Code changes) |
| I77-R1-02, I77-RS1-03 | SHOULD-FIX, NIT | Fix attempted in round 1; the case was wrong and was replaced in round 2 (I77-R2-01) |
| I77-R1-03 | NIT | Fixed: the FU-021 note says that the re-test is a REQ-009 procedure and that the deterministic version check moved |
| I77-R1-04 | NIT | Fixed: `task-brief.md` names the tested-host record too |
| I77-R1-05 | NIT | Fixed: FU-038 gives its reason deferred |
| I77-R1-06 | REQ-GAP | Decision card for the user (the re-test procedure has no headless dispatch) |
| I77-RS1-01, I77-RS1-02 | NIT | Fixed: the collision message names R-DEL-2 for a pinned agent; the size comment names pinned agents |
| I77-RS1-04 | NIT | Deferred to Issue #79 (the `dev-deliver` floor-check text does not point to the exception for a host that cannot set values; no change from main) |

Also: the read-back gate Issue is #79; the DL-040 Evidence says "is
requested"; D-023 residual risk 3 says "before Issue #77".

Round 2 (narrow, diff identity `686f9cd7…`): deep and security, requested
`opus`/`xhigh`, recorded `opus`/`xhigh`. Security passed with one NIT; deep
found one SHOULD-FIX.

| ID | Severity | Disposition |
| --- | --- | --- |
| I77-R2-01, I77-RS2-01 | SHOULD-FIX, NIT | Fixed: the round-1 test case did not open the quote, so it tested the duplicate key again; a new case opens the quote in the description and closes it after the pinned lines, and asserts the value-grammar error. The round-1 row for I77-R1-02 said "Fixed" too early |
| I77-R1-06 | REQ-GAP | User answer 「I77-R1-06 選 a」: the re-test procedure in REQ-009 adds a headless dispatch step; every run uses an empty temporary directory, no bypass flags and prompts without side effects |

Also: DL-040 names the maintainer re-test; DL-034 says "showed that the host
requests" instead of "confirmed"; the CHANGELOG and DL-040 name #79; the
FU-021 note names the card for each moved item.

Round 3 (narrow, diff identity `8beddfff…`): deep and security, requested
`opus`/`xhigh`, recorded `opus`/`xhigh`; no MUST-FIX or SHOULD-FIX. NITs
fixed: the re-test procedure forbids a bypass flag or mode, reads only the
transcripts of the test runs and reads no environment, process or
credential data for any value (I77-RS3-01, I77-RS3-02); the REQ-009 Issue
#77 group and D-024 (both languages) list the answer to card I77-R1-06
(I77-R3-01). The commit scan covers these text fixes.

## Floor checks and dispatches (R-DEL-2)

- This session started at `opus`/`medium` (transcript fields and host
  metadata). It did the read-only test and wrote no repository file. The
  orchestrator set it to `high`; from the next turn, the transcript fields
  read `opus`/`high`. The floor check before the first repository write
  read `opus`/`high`, so this session wrote the change itself.
- Reviews and scans: `dev-reviewer` and `dev-security-reviewer` at
  `opus`/`xhigh`, recorded `opus`/`xhigh` from the transcript fields.
- Diagnostic dispatches of step 1 (read-only, no writes) are part of the
  test result in D-024.

## Lesson candidates

- When a scope is split, list which kept items depend on fixes in the moved
  part (round 3: the session read-back lost the source priority that round
  2 had added with the read-back gate). Suggested level: this pack; one
  event.
