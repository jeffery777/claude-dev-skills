# Round 2: narrow re-review (Issue #32, SR21B-001)

- Revision: base `33ba87cbb67b5217565ba87e6e764e0cbb424479` plus uncommitted changes; `git diff HEAD --binary` SHA-256 `097e10ccf3acb65d557472f2fc57ee6e7a11a2b77edfcd097f2b90512846d014`. HEAD, diff hash and status were the same at the end of the review.
- Scope: the fixes of R1-001 and R1-002 and the round-1 record and graph changes. The reviewer rebuilt the round-1 diff in memory and got its SHA-256 (`9242e5c3…`), so the only tracked changes since round 1 are `.dev/followups.md:13` and the end of the new REQ-024 acceptance line. `agents/dev-security-reviewer.md` did not change since round 1.
- Requirements: REQ-024; user decision card R1-002 (a).
- Reviewer: `dev-skills:dev-reviewer` (opus, high requested; effective settings unknown).
- Commands: `git diff HEAD --check` (exit 0), `--word-diff`, `git hash-object --stdin` rebuild, `PYTHONDONTWRITEBYTECODE=1 bash scripts/validate.sh` (exit 0, 131 tests OK), `graph.py validate` (ok). No scanner run; this is not a full R-REV-7 scan. Core criteria files were not given in the brief.

## Findings

None (0 MUST-FIX, 0 SHOULD-FIX, 0 NIT, 0 REQ-GAP, 0 SCOPE-CREEP). R1-001 and R1-002 are confirmed Fixed.

## Residual risk

- REQ-024 line 64, read alone outside its bullet, still has a literal tension with the new line; no reproducible failure.
- The FU-005 row says "is fixed by Issue #32" before the merge; the sentence is false if this change does not merge (user card R1-002 (a)).
- The T1 `dod` text does not name the FU-005 row update (title and `owns` do).
- RR-1 to RR-3 of round 1 stay.

Written per ASD-STE100 principles; full conformance not verified.
