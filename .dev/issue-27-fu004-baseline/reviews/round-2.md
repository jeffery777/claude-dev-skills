# Review round 2 (narrow confirmation), Issue #27

Written per ASD-STE100 principles; full conformance not verified.

- Target: working tree against HEAD `90b9f33`, `git diff HEAD --binary` sha256 `ae36fbee…41200dd2`.
  Reviewer: `dev-skills:dev-reviewer` (opus, xhigh, deep, strict), fresh context. HEAD, status and diff
  hash were the same before and after the review.
- Scope: the fixes of R1-001 to R1-004 and S-1, the new REQ-016 source and the log line.
- Commands (reviewer): `git diff HEAD` and `--stat`, `git ls-files --stage`, `git log`, read-only
  `python3 -I` reads of the four session records (output masked: counts and comparisons only),
  `bash scripts/validate.sh` exit 0, `graph.py validate` ok.
- Result: R1-001, R1-002 and R1-003 fixed. The four quoted first sentences equal the first user messages,
  character by character (T4 with the local path masked); the first `git log -1 --format=%h` outputs are
  `863db22`, `863db22`, `789af96` and `599c0e8`. R1-004 fixed in section 8, but see R2-001. No MUST-FIX;
  two SHOULD-FIX.

## Dispositions

| ID | Relation | Severity | Finding | Class | Disposition |
| --- | --- | --- | --- | --- | --- |
| R2-001 | in-scope | SHOULD-FIX | Section 1 said that the run after PR-4 replays the tasks from the same start commits with the same first sentences; this contradicted section 8 and the user's card R1-004 answer (how to rerun is decided later) | necessary fix | Fixed by removing wording: section 1 says only that the record keeps the start commits and first sentences and that how to run after PR-4 is decided later; "(for the replay)" and "replay input" removed |
| R2-002 | in-scope | SHOULD-FIX | The Reads method did not state the counting unit, so T4 `dev-core` 2 could not be reproduced; the claim that T4 also read `review-report.md` rested on a `grep` counting as a read | necessary fix | Fixed by removing wording: the example is removed; the method says that this record does not state the counting unit and that counts from another unit cannot be compared |

## Residual risk

- `events.jsonl` seq 3 hash (as in round 1).
- The T4 session read `dev-core` from its worktree by a relative path, not the plugin copy; this can
  affect a comparison of `dev-core` reads between repositories.
- The R1-004 paragraph in section 8 has three sentences; the extra two give the verified facts and the
  source of the decision.
