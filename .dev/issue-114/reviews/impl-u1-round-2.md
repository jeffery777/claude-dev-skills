# Issue #114 implementation review of U1, round 2 (narrow confirmation)

Written per ASD-STE100 principles; full conformance not verified.

## Binding

- Target: the U1 paths after the round 1 fixes, uncommitted, HEAD = base
  `7e71ad5061b345d6f8c921adca65bf494876855c`; tree diff hash before and
  after the review (CB-4): `5592907a30901cc89ca6856c087fc493b75f08d303cedb2a96228231257d375d`
  (it also holds the U2 paths, not a target). REQ-030 SHA-256
  `97d7b6b637964f2840a47b606de7a6704ce780444ec1c02fef2b0acdf908d14f`.
- Reviewer: `dev-skills:dev-reviewer`, role `review-deep` (narrow
  confirmation, R-REV-4), `opus`/`xhigh` passed; recorded `unknown`, case
  `not read back`; effective `unknown`. Dispatched in parallel with the two
  U2 reviews (read-only, separate targets).
- `reviewer_acceptance.py check` printed `PASS` (exit 0) in the same Bash
  command as the CB-4 values before the dispatch; after all three reviews
  the values were the same (exit 0).
- Reported commands: read-only `git diff`, `git status`, `grep`; unit tests
  -> 424 tests, OK (3 skipped), status unchanged. No write reported.
- Co-change rule 1 for the fix round: `log.md` has one new row each for
  REQ-026 and REQ-030 that name "Issue #114 fix round 1"; only appended
  lines. On the cumulative diff, only the row text tells the rounds apart.

## Result

All 12 findings of round 1 confirmed (IR1-D-01 to IR1-D-08, IR1-S-01 to
IR1-S-04). New finding:

| ID | Relation | Severity | Summary | Class | Disposition |
| --- | --- | --- | --- | --- | --- |
| IR2-01 | in-scope | NIT | The plan still expects an `UNUSED_REQUIREMENT` warning for REQ-009, which the IR1-D-04 fix removed | necessary fix | Fixed in the plan (record wording only; no new review round, as for record NITs) |

Residual notes of the reviewer, handled in the plan record without a new
round: plan D3 still said "change order" (now "grouped by kind"); the
"Before the create" fetch came after the Notes step (now before it).
Other residual notes are kept as residual risk: the shorter README,
REQ-030 Need and CHANGELOG entry texts do not repeat the pinned-install
exception (true for the documented install path without a ref;
inference); "an install pinned to a tag or branch does not get it" is not
true for a pin to `main` (safe direction); the FU-069 reopen step is
derived from card C2.

The reviewer did not read the Issue #3 comment or the official docs in
this round; round 1 did (deep review, `curl` and `gh`).
