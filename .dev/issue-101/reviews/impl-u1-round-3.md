# Issue #101 U1 implementation review round 3 (d6)

- Target: the staged diff against HEAD `c818e4dfd59a92650ba09d3f5d71c6da6a29ee01`
  (SHA-256 of `git --no-replace-objects diff --cached --binary --no-textconv --no-ext-diff`
  = `58daf9ae65c1205c2aea3eac5aad6484662ad2ca73bdb20591299ce49ac46ce2`; plan
  `47cd1ef03f50894911083b5ce9030ad4999c8324819b8fbeaf3f37cfc874ccfa`; no
  unstaged change). Hash and HEAD equal before the dispatch and after both
  reports (CB-4 practice).
- T1-fix2 (`dev-implementer`, role `implement`, `opus`/`high`): read back
  `PASS`, `floor=work`.
- Reviews: a deep review (role `review-deep`) and a Security Diff Scan (role
  `review-security`), both `opus`/`xhigh`, both read back `PASS` with
  `floor=review-scan` (result lines in the PR gate record comment). Both
  count.
- Round 2 findings: all resolved in both reports, except IR2-D-02, partly
  resolved (deep review): the command level no longer needs a check per
  round, but the reading level has the same accumulation (IR3-D-01).
- Both reviewers re-ran the search list (261 rows) and co-change rule 1 with
  `--cached`: no difference from the recorded outputs. The deep review ran
  the three Merge Review forms on PR #100's commit and `scripts/validate.sh`
  (374 tests OK, 3 skipped).
- Written per ASD-STE100 principles; full conformance not verified.

## Findings (reviewers' severities)

All in-scope. Open until the user answers `cards-7.md`.

| ID | Severity | Finding (own words) |
| --- | --- | --- |
| IR3-D-01 | SHOULD-FIX | the reading check works only on a diff that shows the fix alone; the card said "the fix diff", the rule says "the diff that it reviews", and a fix staged together with its node shows nothing to read. Tested on PR #100's trees: fix-only `b96c4298…` → `539a2f05…` lists REQ-009 and no `log.md`; cumulative `c78d53c7…` → `539a2f05…` shows a `+\|` row naming REQ-009, so it looks fine. PR #100's reader saw it because that round was scoped to the fix diff (`.dev/issue-96-pr3/plan.md:295`) |
| IR3-D-02 | NIT | "reports differences" assumes that the main agent ran first; the order differs between steps 5 and 7, and with no commit authorization but a staged target `dev-plan` says no command runs while `dev-review` says the reviewer runs them |
| IR3-D-03 | NIT | six records call "in one commit" the card's limit; the card does not say it (the narrowing is right, the attribution is not) |
| IR3-S-01 | NIT | the trace row of R2-C1 shortens the card to "only the main agent runs" and drops the reviewer re-run clause (`cards-3.md:29`) |

Residual risks named (kept, among others): `plan.md` "the user authorized the
commits of this objective" gives no source and is wider than card I101-C3
(a) (commits of each unit after its review); a misspelled requirements
folder passes with an empty list; `dev-implement` and `dev-gate` do not name
the checks; the floor-check and read-back records of 2026-11-05 are missing
in the plan; `cards-6.md` says the Merge Review forms were tested, and
`impl-u1-round-2.md` has no such record (this round's deep review is the
first recorded run).

## R-VER-2: the stop rule fired (fifth time)

- Fact: round 2 and this round both reported new blockers (IR3-D-01 is a new
  `SHOULD-FIX`), so the first trigger holds
  (`skills/dev-core/SKILL.md:195`). The second trigger holds too: the
  mechanism that ties a check to one node or fix round has a new problem.
- Fact: the Security Diff Scan reports no blocker and says that the d6
  deletion brought no new security problem.
- Classification (inference): a claim that was too wide (card I101-IR2-C1 (a)
  said reading catches the P3-T3 case), not environment, permission or
  context; no escalation of the writing side.
- No fix starts before the user's answer.

## Lesson candidates

- Trigger: the stop rule fired; level L2. Observation (fact): when a command
  check became a reading check, the card's condition "the fix diff" became
  wider in the rule. Lesson (inference): a reading check needs the same
  before-state as a command; name what the reader must get. Events: 1.
  Coverage: R-REV-4, R-REV-6. Judgment: worth improving. Abstraction
  checklist: every item not present.
- Trigger: the same kind of finding (a record says more than its source:
  IR1-D-03, IR3-D-03, IR3-S-01); level L2. Lesson (inference): say who
  narrowed a source, and keep each clause that names an actor. Events: 3.
  Coverage: R-EVD-3 (U2), `dev-plan` step 2. Judgment: keep as is until U2 is
  in force. Abstraction checklist: every item not present.
