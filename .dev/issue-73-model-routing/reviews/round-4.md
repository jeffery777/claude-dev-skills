# Issue #73 review round 4 (narrow re-review of the I73-R3-C1 (a) change)

Target: uncommitted candidate on `f7b2ea8` (tracked diff `--binary` SHA-256
prefix `ef3cf16f`; HEAD and `git status --porcelain` equal at start and end).

- Change: written by the main session after its transcript read back
  `opus`/`high` (floor met). Card I73-R3-C1 (a) named `dev-implementer` for
  the change; the main session made it itself because its setting met the
  floor (recorded deviation from the card's wording, reported to the user).
- Deep review R4: `dev-reviewer`, requested `opus`/`xhigh`; recorded
  `unknown` (not read back); the dispatch table of the Issue #73 merge card
  lists `opus`/`xhigh` (added later, Issue #75); effective `unknown`. PASS;
  five NITs and one SCOPE-CREEP. The decided sentence is in every copy with
  the same meaning.

## Findings and dispositions (all Fixed by the main session at `opus`/`high`)

| ID | Severity | Summary | Disposition |
| --- | --- | --- | --- |
| R4-001 | NIT | `docs/requirements/log.md:116` said "four new source entries" and lacked the I73-R3-C1 source | Fixed: "five", source added |
| R4-002 | NIT | D-022 "What ships" (zh and en) lacked the `review-report.md` field and FU-035 | Fixed in both languages |
| R4-003 | NIT | DL-034 had the new rule only in the Reason column | Fixed: added to the Difference column |
| R4-004 | NIT | `graph.json` T1 owns lacked `review-report.md`; title and DoD did not cover round 3; plan trace named rounds 1 and 2 | Fixed (re-planned; `graph.py validate` ok) |
| R4-005 | NIT | FU-035 said every write node owns its objective folder (32 of 60 do) | Fixed: "a write node that owns its objective folder (T1 of Issue #73 does; not every node does)" |
| R4-006 | SCOPE-CREEP | The report field asked for a reason per trigger, which no requirement asks | Fixed: removed "with the reason" |

Residual risk items also fixed: `dev-review` now asks the reviewer to answer
"for each of them" (as `task-brief.md` and the report field do); FU-035
covers docs sync inside and outside the owned paths; S3-002 in
`round-3.md` now records the answer and the fix.

Not re-reviewed after these record fixes: they change wording of records
and one phrase of `dev-review`; the Merge Review (complete base-to-head
review with a Security Diff Scan) covers them.
