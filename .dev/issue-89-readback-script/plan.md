# Issue #89 plan: read-back script for the recorded model and effort of a subagent transcript (Issue #79 slice B)

- Objective: GitHub Issue #89 (body and its 2026-10-30 update), slice B of
  the tracking Issue #79: a stdlib script in the pack that reads one
  subagent transcript and prints closed tokens only, with its threat model
  and synthetic tests. No skill rule tells an agent to run it (card I79-C1
  (a)); the wiring is slice C.
- Rigor `strict`. Reason (R-RIG-1, re-assessed at Discover as R-RIG-2
  says): a new executable in a public pack that reads security-relevant,
  user-writable input.
- Base: `main` 852b4de, branch `issue-89-readback-script` (created from
  Issue #89 on GitHub).

## Source trace (dev-plan step 2)

Sources: the Issue #89 body and update; the Issue #79 body (Change 1 and 4,
spec input "Binding and location", "Comparison", "Failure classes",
"Script threat model and fixtures", and the tracking section); FU-021; and
these user answers (Claude Code session 2026-10-30, the user's words in the
orchestrator session, relayed by the orchestrator):

- 「I79-C1 a+d，I79-C2 a」: slice B is the script without gate wiring.
- 「I79B-C1 a，I79B-C2 a」: subagent mode only (session mode, its UUID
  source and its turn range move to slice D); the re-test use of the
  script, the Sonnet and Haiku IDs and an exact-match mode go to FU-049.
- 「I79B-R2-C1 a」: rev 3 simplifies the directory walk and applies the
  round 2 precision fixes; there is no design review round 3; the
  implementation review checks rev 3.
- The FU-035 evidence note for PR #86 finding MR85B-01: the user agreed,
  relayed by the orchestrator without a quote. It is an exception to the
  Out of scope list of Issue #79 (FU-035).

From the design reviews, not from the user's words: the walk with
directory file descriptors and no symlink following (D1-01, S1-01, D2-01,
S2-01 to S2-03), the `sessionId` binding (D1-03), the open and read limits
(D1-02, S1-02, S2-04), the parsing limits (S1-03), the CLI behavior (S1-04,
S2-05), the opus-only allowlist (S1-07), the non-normative reference (D1-05,
S1-08), the static test (D1-07, S2-06, D2-04) and the dependency table
(D1-06, D2-02).

## Design reviews

| Round | Target | Result | Outcome |
| --- | --- | --- | --- |
| 1 | Design rev 1 | deep: 2 MUST-FIX, 5 SHOULD-FIX, 2 NIT; security: BLOCKED, 1 MUST-FIX, 7 SHOULD-FIX, 1 REQ-GAP, 3 NIT | cards I79B-C1 (a) and I79B-C2 (a); rev 2 |
| 2 | Design rev 2 | deep: no MUST-FIX, 5 SHOULD-FIX, 1 NIT; security: PASS, 7 SHOULD-FIX, 4 NIT | R-VER-2: the same mechanism (the confinement of the directory walk) needed fixes in rounds 1 and 2; stop card I79B-R2-C1 (a); rev 3 without a round 3 |

All reviewers: requested `opus`/`xhigh`; recorded `claude-opus-5-5`/`xhigh`
from the transcript fields; effective `unknown`.

## Implementation review

Round 1 (T1 as implemented): deep, no MUST-FIX or SHOULD-FIX, REQ-GAP
I89-R1-01 (the static test has gaps), NIT I89-R1-02 and I89-R1-03, and no
new problem in the confinement mechanism by its reading; Security Diff
Scan, PASS, SHOULD-FIX I89-S1-01 (no test guards the open flags, a test-level
confinement problem by its reading), NIT I89-S1-02 and I89-S1-03. The
reviewers disagreed on the confinement question; the main agent counted it
as a new confinement problem and stopped (the user's rule with card
I79B-R2-C1 (a); R-VER-2 for the static check, changed in design rounds 1
and 2). Card I89-C1 (b) (the user's words in the orchestrator session,
relayed: 「I89-C1 b」):

| ID | Severity | Disposition |
| --- | --- | --- |
| I89-S1-01 | SHOULD-FIX | Fixed: the flag constants are pinned and an AST check requires one of them in every `open_at` call; in-process tests cover the untested errno branches; the real symlink swap stays untested (residual risk in the reference) |
| I89-R1-01, I89-S1-02 | REQ-GAP, NIT | Deferred to FU-050 by card I89-C1 (b); the reference says that the static test is a regression aid only |
| I89-R1-02 | NIT | Fixed: the reference and the test docstring say what process data is read |
| I89-R1-03 | NIT | Fixed: the flags are computed inside `main`, and a closed or broken stdout gives no traceback |
| I89-S1-03 | NIT | Fixed: the CHANGELOG wording and the added limits in the reference; the allowlist policy is a pointer to REQ-009 |

Round 2 (narrow, the fix round): deep, no MUST-FIX or SHOULD-FIX, NIT
I89-R2-01 (the REQ-009 test item missed two in-process cases and the flag
pins) and I89-R2-02 (this plan said "every open"), both Fixed; Security
Diff Scan, PASS, NIT I89-S2-01 (the pins and the AST check do not cover a
direct `os.open` or flags masked inside `open_at`: added to FU-050 with the
other gaps that round 2 listed), I89-S2-02 (= I89-R2-01, Fixed) and
I89-S2-03 (a partial line on a full disk: a result needs a full line and
its exit code; Rejected, no change). Both reviewers: no new blocker and no
new problem in the confinement mechanism; requested `opus`/`xhigh`,
recorded `claude-opus-5-5`/`xhigh`.

The main agent also replaced a U+FEFF character in the script by the
escape `\ufeff` before the review.

Round 1 card I79B-C1 said that a directory whose name does not match the
pattern but holds the target file stops the script. Rev 3 does not descend
into such a directory at all: the script never looks inside it, so it
cannot be led by it, and the result is the same fail-closed direction
(S2-01, D2-01).

## Dependencies on other slices

| Item | Goes to |
| --- | --- |
| When and by whom the script runs; no fallback to ad hoc reads; IDs only from the harness line or a task notification; the CB-6 call path; the source of `--projects-dir`; headless; read only after the subagent finished | slice C |
| Reason tokens to R-VER-2 classes and actions; the bootstrap rule (run the copy of the bound base); what to do when a value cannot be read back; the transcript rewrite residual risk (card I77-R2-C2); confinement to the subagents of the dispatching session | slice C |
| A cross-check of the agent ID with `.meta.json` (candidate) | slice C decides |
| A `light` routine review at `sonnet`/`medium` (`dev-review`) stops with `MODEL_NOT_ALLOWED` until FU-049 adds the Sonnet ID | slice C depends on FU-049 |
| Session mode, the session UUID source, the turn range, the host's session tool | slice D |
| Sonnet and Haiku IDs, an exact-match mode, the re-test use of the script | FU-049 |

## Copies left unchanged (R-EXH-2)

REQ-009 Notes (the two Limit paragraphs), `docs/design-proposal.md` section
4 and the D-024 residual risk 1 stay as they are: no rule uses the script
yet, so what they say about read-back is still true.

## Dispatches and floor check

The main session read its own transcript before it wrote this plan and
again before it wrote the round 1 records: `claude-opus-5-5`/`high`; requested value `unknown` (set by the session
that started it).

| Node or step | Agent | Requested | Recorded | Effective |
| --- | --- | --- | --- | --- |
| Issue #89 and #79 text scan | `dev-security-reviewer` | `opus`/`xhigh` | `claude-opus-5-5`/`xhigh` | `unknown` |
| Design review rounds 1 and 2 | `dev-reviewer`, `dev-security-reviewer` | `opus`/`xhigh` | `claude-opus-5-5`/`xhigh` | `unknown` |
| T1 and its fix round | `dev-implementer` | `opus`/`high` | `claude-opus-5-5`/`high` | `unknown` |
| Implementation review rounds 1 and 2 | `dev-reviewer`, `dev-security-reviewer` | `opus`/`xhigh` | `claude-opus-5-5`/`xhigh` | `unknown` |

## Residual risks

The reference lists them; the main ones: recorded is not effective; a
transcript can be rewritten or deleted, and the lowest-value rule only
stops appended lines; an agent ID can be swapped; the script cannot prove
that the file belongs to the dispatching session or that `--projects-dir`
is the real one; a PR can change the script that would judge it; the size
limits are not measured; mode bits are not checked; the binding and the
line format were observed on one machine and one project; the static test
only guards against regressions; CI does not run Python 3.9.

## Non-goals

Gate wiring and any rule that names the script (slice C); session mode
(slice D); environment variables and host version sources (FU-045);
R-DEL-2 text; agent files and `check_pack` pins.
