# Issue #73 plan: model routing (C4, C5; C3 deferred to FU-034)

- Objective: GitHub Issue #73. Lower the model cost of routine work without
  losing protection. User decisions on 2026-10-27 on the cost proposal:
  「C3 選 a，C4/C5 同意」; the PR #70 lesson (decision 「I69-M1 a」) goes
  into the same Dispatch rule.
- Rigor `standard` (Issue #73, Process): one PR. The change edits rules that
  the pack publishes (public contract) and the R-DEL-2 floor of security
  work, so the review is deep and a Security Diff Scan runs (R-REV-7: agent
  tool and model policy of a security scan).
- Correction (Issue #75): by R-RIG-1 this was `strict` work (public contract).
- Base: `main` f7b2ea8, branch `73-model-routing`.

## Requirement trace

Rewritten after review round 2 (S2-004); C3 and REQ-011 left the plan in
"Changes after review round 1".

- REQ-009 (subagent model and effort; R-DEL-2, D-007, FU-018 records,
  DL-034, DL-038): C4 light routine review (with the reviewer's report on
  triggers 1 to 3, card I73-R2-C2 (a)), C5 Dispatch default and floor check
  (before each node under the floor and before each fix or write of such a
  node, card I73-R2-C1 (a)).
- REQ-011 is not changed (C3 deferred to FU-034).
- Source trace (dev-plan step 2): Issue #73 body (Goal, Change 2 to 4), the
  user's words quoted there and the card answers of review rounds 1 to 3.
  C4 and C5 use the examples of the Issue as the lists (see Decisions).

## Facts and checks before the change

- Main session setting (R-DEL-2): the transcript fields of this session
  record model `claude-opus-5-5` (alias `opus`) and effort `medium`. The
  work is public-contract and security-policy work, so the floor
  `opus`/`high` applies and the effort is below it. The implementation goes
  to `dev-implementer` at `opus`/`high` (C5 itself; the I69-M1 lesson). The
  plan and the brief are written by the main session.
- Core check (inference from the vendored text, not reviewed): Core
  `workflow.md#wf-delegation` (line 56, 60) asks the main agent to choose
  model and effort by need, risk, context and verification burden, and to
  delegate only bounded work that is independent, verifiable and improves
  quality or time. Core sets no model floor: the `opus`/`high` floor is the
  project tightening DL-005. So C3 loosens a project tightening (the user
  decides, deltas preface), not Core. C5 restates the Core delegation
  criterion and adds a check; C4 changes a table value above any Core
  requirement.
- `gitleaks` (and `trufflehog`, `detect-secrets`) is not installed on this
  machine (`which` prints nothing). Installing a tool needs the user's
  approval (R-REV-9 last bullet). So, until a scanner is installed, the C3
  path falls back to `opus`/`xhigh` and saves nothing.
- FU-005 comparison of the copies (sentence by sentence, main session).
  Superseded in part by "Changes after review round 1": the C3 parts below
  (the security reviewer and the scanner, the C3 text-scan exception in
  `task-brief.md`, the R-REV-9 text bullet, D-007 rule 2 and REQ-011) no
  longer apply; the copies changed are those that "What ships" of D-022
  lists.
  - `agents/dev-security-reviewer.md`: no model or effort text in the body;
    the front matter default `opus`/`xhigh` stays (REQ-009 non-goal: no
    change of agent defaults; a dispatch passes both values). "Use Bash only
    for read-only inspection, the scanners the brief names" is compatible
    with C3; in C3 the main agent runs the deterministic scanner, so the
    reviewer runs none. The description "the scan before every commit, push,
    PR post and Issue post" stays true. No change.
  - `agents/dev-reviewer.md`: "(routine or deep)" and the check list; no
    model text. No change.
  - `agents/dev-implementer.md`, `agents/dev-explorer.md`: no model, scan or
    dispatch text. No change.
  - `skills/dev-deliver/references/task-brief.md`: the line "Why this
    model/effort: <role and rigor tier from the dev-deliver table; R-DEL-2
    floor; escalation step and the quality failure it answers>" must also
    name the C3 text-scan exception and a C4 escalation trigger. Change.
  - Other copies to change: `skills/dev-core/SKILL.md` (R-DEL-2, R-REV-9
    text bullet), `skills/dev-review/SKILL.md` (mode table),
    `skills/dev-deliver/SKILL.md` (Dispatch step and table, Gate line),
    `skills/dev-core/deltas.md` (DL-005, DL-034, new DL-038),
    `docs/design-proposal.md` (section 4 table and paragraph, D-007 rule 2,
    new D-022, both languages), REQ-009, REQ-011, `docs/requirements/log.md`,
    `CHANGELOG.md`.
  - Not changed: `skills/dev-retro/SKILL.md` (its own reviewer dispatch at
    `opus`/`xhigh`); `skills/dev-continue/SKILL.md` line 58 and
    `skills/dev-review/references/decision-card.md` (refer to R-REV-9
    without a model); README (agent defaults only).

## Decisions (no card; reasons)

The Issue gives the lists as examples. None of the choices below weakens a
protection beyond what the user decided, so they are not trade-offs for the
user; each is recorded here.

1. C3, who runs the deterministic scan: the main agent, before the dispatch,
   on the same file the post will use. Reason: the result is then a fact the
   main agent reads directly (exit status), not a claim of a `sonnet`
   reviewer; the reviewer still reads the whole text. Like push step 4a,
   the deterministic check is the main agent's, and the independent scan is
   the reviewer's.
2. C3, fallback: when no scanner is installed, or it cannot run, fails, or
   gives a result other than a clean pass, the text scan runs at
   `opus`/`xhigh` (today's setting). Reason: the user chose the exception
   with the deterministic scan as its compensation; without it, the floor
   stays.
3. C3, scope: only a text scan that runs on its own (PR, MR or Issue title,
   body or comment, a review record). Text that is scanned with a push scan
   keeps the push scan settings. The commit, push and merge-readiness scans
   (the merge-readiness scan includes the merge or squash commit text) stay
   `opus`/`xhigh`.
4. C4 triggers (decided before the dispatch from the diff and the plan, and
   again after the review): the R-DEL-2 floor applies (security, trust
   boundary or another R-REV-7 case, data, persistent state, migration,
   public contract); packaging, installation, CI or dependencies; more than
   one module; a finding is disputed (rejected by the main agent or the
   author, or two reviews disagree); the reviewer reports a part of the
   target it could not check. A trigger after the review re-runs the review
   at `opus`/`high` on the same target; the first report and its findings
   stay. Not a trigger: a `MUST-FIX` alone (it goes to the fix loop; the
   Issue does not list it).
5. C5 delegate conditions: parallel read-only work, or a broad read whose
   conclusion is all the session needs; a context too large for the main
   session; every required review or scan (R-REV-1 already requires an
   independent subagent); a floor the main session does not meet; the user
   asks for delegation. Floor check: before the main session implements a
   node, it reads its own model and effort and compares them with the
   floor; below or `unknown` -> ask the user to switch or dispatch
   `dev-implementer` at `opus`/`high`, never implement first.

## Task graph

One write node `T1` (all rule copies and records; one review unit, because
the copies must agree and are reviewed together).

## DoD

- Every copy listed above states C3, C4 and C5 as in Decisions, with the
  same values and conditions; the two language versions of the design
  proposal mean the same.
- The C3 exception is written as a user-decided exception to the R-DEL-2
  floor with source, quote, authority, reason and scope (deltas preface);
  the commit, push and merge-readiness scans stay `opus`/`xhigh`.
- D-022 (both languages), REQ-009 and REQ-011 records, log rows, DL rows,
  CHANGELOG.
- `bash scripts/validate.sh` passes.
- Independent deep review (`dev-reviewer` `opus`/`xhigh`) and Security Diff
  Scan (`dev-security-reviewer` `opus`/`xhigh`) with no open MUST-FIX or
  SHOULD-FIX.

## Implementer

`dev-implementer`, requested `opus`/`high` (R-DEL-2 floor: public-contract
and security-policy work; main session `opus`/`medium` is below it).
Receipt T1: done; recorded (transcript fields): model `claude-opus-5-5`
(`opus`), effort `high`; effective `unknown`. Main agent read-back: the diff
of the four skill files matches the receipt; `bash scripts/validate.sh`
passed (`validate.sh: all checks passed`).

## Changes after review round 1 (user answers)

User answer (Claude Code session 2026-10-28, orchestrator relay):
「I73-R1-C1 選 c，I73-R1-C2 選 a。工具該裝還是得裝，你可以建議你認為適合的工具。」

- C3 is deferred (card I73-R1-C1 (c)): Decisions 1 to 3 above and the C3
  parts of the DoD no longer apply. The R-REV-9 text scan before posting
  stays `opus`/`xhigh` exactly as on `main`; REQ-011 is unchanged. C3 with
  findings S1-001 to S1-004 and R1-003 is tracked in FU-034.
- C4 (card I73-R1-C2 (a)): once a trigger applies to a node, every later
  review round of that node uses `opus`/`high`.
- C5: the floor check runs before this session runs any node under the
  floor (S1-006), not only before it implements.
- Fix round 1 part B: `dev-implementer` T1-F2, requested `opus`/`high`;
  recorded `opus`/`high`; effective `unknown`. Main agent read-back: receipt
  checked against `git diff --stat`; `bash scripts/validate.sh` passed; diff
  SHA-256 prefix `cbdf8aa3`.
- Review round 2: see `reviews/round-2.md` (R-VER-2 stop rule).

## Changes after review round 2 (user answers)

User answer (Claude Code session 2026-10-28, orchestrator relay):
「I73-R2-C1 選 a，接受 S2-001；I73-R2-C2 選 a」

Fix round 2 (`dev-implementer` T1-F3, requested `opus`/`high`), bounded to:

1. S2-001: the user accepted the main-session deviation; T1-F3 re-applied
   the REQ-009 row of Issue #73 in `docs/requirements/log.md` and recorded
   the acceptance in `reviews/round-2.md`.
2. S2-002: the floor check also runs before the main session fixes or
   writes any part of a node under the floor (R-DEL-2, `dev-deliver` steps
   2 and 5, `dev-review` step 6, DL-038, design section 4 and D-022,
   REQ-009, CHANGELOG).
3. S2-003: `dev-deliver` step 2 says why `verify`, `gate` and `human_gate`
   nodes are outside the floor check (mirrored in DL-038 and D-022).
4. S2-004 = R2-001: the graph is re-planned (titles, REQ-009 only, owns
   without the REQ-011 file and with `.dev/followups.md`, DoD for C4 and
   C5); the Requirement trace and FU-005 sections above no longer describe
   C3 as planned.
5. R2-002: FU-021 item (2) notes what C5 now covers; REQ-009 Notes say the
   check runs per node and per write.
6. S2-005 (card I73-R2-C2 (a)): the brief of a `light` routine review at
   `sonnet`/`medium` lists triggers 1 to 3 and the reviewer reports whether
   any holds; a reported trigger re-runs the review at `opus`/`high`, as for
   trigger 5, and the node keeps `opus`/`high` (`dev-review`,
   `task-brief.md`, DL-034, D-022, REQ-009, log row, CHANGELOG).

Pre-agreed rule (card I73-R2-C1 (a)): if the narrow re-review finds a new
blocker in the floor-check timing mechanism, that part moves to a follow-up
and the rest ships.

## Review round 3

See `reviews/round-3.md`. The floor-check timing findings (R3-001, S3-001,
S3-003) moved to FU-035 by the pre-agreed rule. S3-002 waits for card
I73-R3-C1. From this round on the main session's transcript records
`opus`/`high` (read back before each write), so it writes records and small
fixes itself.

## Changes after review round 3

User answer (Claude Code session 2026-10-28, orchestrator relay):
「I73-R3-C1 選 a」. A `light` routine-review report that does not say, for
each of triggers 1 to 3, whether it holds counts as trigger 5 (re-run at
`opus`/`high`): `dev-review` "Choose the mode", `task-brief.md`, a new field
in `review-report.md`, DL-034, D-022 (zh and en), REQ-009 (source and
acceptance), log row, CHANGELOG. Written by the main session after its
transcript read back `opus`/`high` (floor met).
