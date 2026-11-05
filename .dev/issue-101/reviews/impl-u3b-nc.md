# Issue #101 U3b narrow confirmation (R-REV-4)

- Target: the unstaged fix diff of card I101-U3B-C1 (a) on top of the staged
  content (SHA-256 of `git --no-replace-objects diff --binary --no-textconv --no-ext-diff`
  = `8695c4fa830e1257eb7f06b0376bbe8b6f5ee2aefa818a113b929f3a06cb412a`; staged
  `616ec8836704ea38163b86fd1d0dd15c9d0f6f52c36d4bea90ec86ffb11ae5e2`; plan
  `44b53ee08ad964ab53dc4be16d5100b58e2ae67fdd9f36144ac9c25764155151`), and the
  two new records `cards-15.md` and `reviews/impl-u3b-round-1.md`. The hashes
  were equal at the start and the end of the review (source: its report).
- The main session made this fix itself after its floor check.
- Review: a deep review, narrow scope (role `review-deep`), `opus`/`xhigh`,
  read back `PASS`, `floor=review-scan` (result line in the PR gate record
  comment). It counts.
- Result: 0 MUST-FIX, 0 SHOULD-FIX, 4 NIT. U3B-D-01, U3B-S-01 and U3B-S-02 are
  resolved, and U3B-D-02 has a full disposition. Every ID of the DoD has exactly
  one R-REV-3 disposition. D-030 zh and EN agree. The fix changes no more than
  the card lists. K1 to K31: 357 rows, no difference on the working tree and on
  the index; rules 1 and 2 passed by reading.
- Severity of U3B-NC-01: the reviewer's reading (inference): `skills/dev-plan/SKILL.md:182-187`
  makes a place that the change made false `SHOULD-FIX` for the listed kinds of
  completeness finding, and the "What ships" list is not one of them. If the user
  reads that sentence as covering this place, it is a `SHOULD-FIX`, and the work
  stops for the user.
- Written per ASD-STE100 principles; full conformance not verified.

## Findings (reviewer's severities)

The ceiling of card I101-U3B-C1 (a) applies: only NITs, so dispositions and no
fix round. The dispositions are in the plan, section "Deferred findings".

| ID | Severity | Finding (own words) |
| --- | --- | --- |
| U3B-NC-01 | NIT | the "What ships (U3b)" list of D-030 (zh and EN) does not name `cards-15.md` and `reviews/impl-u3b-round-1.md` |
| U3B-NC-02 | NIT | the plan row of `cards-15.md` copies from the row of `cards-13.md` the clause "against `main` this still tightens R-AUTH-7", which has nothing to do with this card; the basis of the relay does not rest on that clause |
| U3B-NC-03 | NIT | the check output says "on the working tree" and also gives a result of the `--cached` form |
| U3B-NC-04 | NIT | the fix removed the class of PS4-01 and PS4-02 |

Residual risks named (kept, among others): the result of this confirmation must
be written where the `Fixed` items point; three sentences rest on the PS3 and PS4
reports, which are not in the repository; "U3B-D review item 5" has no such
number in the record of that round.

## Lesson candidates

- Trigger: the same kind of finding in two or more rounds; level L2. Observation
  (fact): the fix added two record files and updated only the Files row, and a
  copied row kept a clause of the row before it. Lesson (inference): when a record
  file is added, find each place that lists its kind; when a row is copied, read
  each clause again for the new subject. Events: 1. Coverage: `dev-plan` step 6
  and its Limit, R-EVD-3. Judgment: worth improving. Abstraction checklist: every
  item not present.
- Trigger: another gap; level L2. Observation (fact): the fix stayed unstaged so
  that the confirmation shows it alone, and the `--cached` commands see it only
  after staging; the record described both states in one paragraph. Lesson
  (inference): write the output of a command after the run that it describes.
  Events: 1. Coverage: `dev-plan` step 6. Judgment: worth improving. Abstraction
  checklist: every item not present.
