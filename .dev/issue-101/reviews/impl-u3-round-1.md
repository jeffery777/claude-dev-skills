# Issue #101 U3 implementation review round 1 (d9)

- Target: the staged diff against HEAD `da87694bba7ebd9b3c74b9b1e474cc5ea79371d1`
  (SHA-256 of `git --no-replace-objects diff --cached --binary --no-textconv --no-ext-diff`
  = `7ddb4d93b7e9a20570d63e3ddd7a6c928e9738cc1f9a81211d16736b1b4319e9`; plan
  `d9116b2d95fec6c98f00e2158b6383c64a2dea1777957164d840d2784fdba82f`; no
  unstaged change). Hash and HEAD equal before the dispatch and after both
  reports (CB-4 practice).
- T3 (`dev-implementer`, role `implement`, `opus`/`high`): read back `PASS`,
  `floor=work`.
- Reviews: a deep review (role `review-deep`) and a Security Diff Scan (role
  `review-security`), both `opus`/`xhigh`, both read back `PASS` with
  `floor=review-scan` (result lines in the PR gate record comment). Both
  count.
- Result: deep review: 0 MUST-FIX, 2 SHOULD-FIX, 3 NIT, 1 SCOPE-CREEP. Security
  Diff Scan: status FINDINGS, 1 MUST-FIX, 2 SHOULD-FIX, 2 NIT. Private data: no
  hit (scan item 3). R-REV-9, the Merge Review and the read-back gate stay in
  force on the path of the exception (scan item 2). DL-048 `tighten` holds
  against Core (both reports; deep review item 4).
- Deferred NITs U2R4-D-01, U2R4-D-02, U2R4-D-03 and the Files row of the cards
  are resolved (deep review item 6).
- Search list K1 to K33: the deep review re-ran it on the index: 385 rows, no
  difference in counts or exit codes; rule 1 passed on this target, which shows
  U3 alone.
- `scripts/validate.sh` (deep review): passed; 388 tests OK, 3 skipped.
- Written per ASD-STE100 principles; full conformance not verified.

## Findings (reviewers' severities)

All open until the user answers `cards-14.md`.

| ID | Severity | Finding (own words) |
| --- | --- | --- |
| U3R1-S-01 | MUST-FIX | condition (3) says that the main agent classified the failure; the card says that the failure is a quality failure (`cards-2.md:23`). The record has no field for the classification, so a confirmation cannot check it. The rule is wider than the card; `CHANGELOG.md` says the card's form, and the plan trace says "kept" |
| U3R1-S-02 | SHOULD-FIX | condition (2) can be checked only from the main agent's summary: "the reports" is not defined, and the saved records are in the writer's own words |
| U3R1-S-03 | SHOULD-FIX | only the narrow confirmation gets the record; later rounds and the Merge Review do not, so "under any name" and "once per PR" stay with the side that uses the exception |
| U3R1-D-01 | SHOULD-FIX | before the PR exists the second place does not exist, but "cannot read both places" makes the check fail, and the cards allow a use before the PR (`cards-3.md:67`) |
| U3R1-D-02 | SHOULD-FIX | with a NIT in a requirement file, co-change rule 1 asks for a `log.md` row, and the exception allows only the text that the NIT names: the two cannot both hold; the deep review classes it as a human decision |
| U3R1-S-04 | NIT | the card's 「最新一輪」 became "the round" |
| U3R1-S-05 | NIT | same subject as U3R1-D-01; also, once the PR exists R-EXH-3 keeps records off the PR branch, so the plan section at the PR head stays "None", and reviewers have no `gh` in their list |
| U3R1-D-03 | NIT | the `noted` reason of five K16 rows is false; a K29 reason fits one of two hits |
| U3R1-D-04 | NIT | three new records say that C5 (a) covers C1 and R2-C2; the card covers C1 (`cards-2.md`), and R2-C2 has its own sentence (`cards-3.md:61`). The root is `plan.md:51` |
| U3R1-D-05 | NIT | REQ-012 and the CHANGELOG say that the tests pin the sentences that carry the conditions; removing six of those sentences fails no test (in-memory mutation) |
| U3R1-D-06 | SCOPE-CREEP | "(for a design review, the next review round)" and "(in a headless run, in the final output)" have no source and no trace row |

Residual risks named (kept, among others): a use that nobody recorded is not
seen by condition (4); closing a PR and opening another is not stopped by the
words of condition (4); a recorded residual security risk that is not marked
open is left out of condition (2) (`dev-gate` step 4 still stops it); the D-030
sentence on `dev-gate` cites only the card and not `skills/dev-gate/SKILL.md:77`
and `review-and-security.md:21`; DL-048 does not list I101-R3-C1 (a), which set
the first sentence and the two record places (`cards-4.md:17-18`); the tree IDs
of the record are not covered by the value rule; `plan.md:34` and `plan.md:51`
differ on C5 (a).

Open question of the Security Diff Scan: may the exception apply to the
remaining rounds of this PR? The sentence "in no rule until U3" of the plan
loses its condition with the U3 commit.

## R-VER-2: the stop rule fired

- Fact: U2 round 4 had no new blocker, so the first trigger does not hold.
- Fact: card I101-R3-C1 (a) says that the implementation review reads the same
  text and that a new blocker on the same mechanism stops the work by R-VER-2
  (`cards-4.md`). The mechanism of E3 needed fixes in design round 3, and this
  review is the next one of that text; it reports new blockers on it.
- Inference: D-03 and D-04 are also of the mechanism "records after a rule
  change" of U2 rounds 3 and 4.
- Fact: the exception cannot apply: this round has `MUST-FIX` and `SHOULD-FIX`
  findings, and the exception is not in the bound base.
- Classification (inference): a spec that lost conditions of its source
  (U3R1-S-01, U3R1-S-04) and paths that were not walked (U3R1-D-01,
  U3R1-D-02); not environment, permission or context. No escalation of the
  writing side.
- No fix starts before the user's answer.

## Lesson candidates

- Trigger: a spec lost a condition of its source; level L2. Observation
  (fact): a condition on a fact became a condition on an action, and "latest"
  was lost, while the trace rows said "kept". Lesson (inference): a trace row
  that says "kept" compares the subject and the qualifiers of the condition,
  not only its topic. Events: 1. Coverage: `dev-plan` step 2, R-VER-5.
  Judgment: worth improving. Abstraction checklist: every item not present.
- Trigger: the same kind of finding in two or more rounds; level L2.
  Observation (fact): the input of an independent check is a summary that the
  checked side wrote (SR2-06, U3R1-S-02, U3R1-S-03). Lesson (inference): when a
  rule uses an independent check to bound the main agent, first make sure that
  the reviewer gets the original. Events: 1. Coverage: R-EVD-2, R-EVD-3,
  R-REV-2. Judgment: necessary fix. Abstraction checklist: every item not
  present.
- Trigger: the same kind of finding in two or more rounds; level L2.
  Observation (fact): no review walked the limit of the fix diff against the
  rules that force other changes, or the time when a record place does not
  exist yet. Lesson (inference): a sentence that limits a diff is walked against
  each co-change rule. Events: 2. Coverage: R-RIG-4, `dev-plan` step 6.
  Judgment: worth improving. Abstraction checklist: every item not present.
- Trigger: the same kind of record problem; level L1. Observation (fact): one
  reason was given to all the rows of one string, and it was true for one row.
  Lesson (inference): when a disposition changes, read the hit of that row
  again. Events: 1. Coverage: `dev-plan` step 6. Judgment: necessary fix.
  Abstraction checklist: every item not present.
