# Issue #101 U3b implementation review round 1 (d10)

- Target: the staged diff against HEAD `da87694bba7ebd9b3c74b9b1e474cc5ea79371d1`
  (SHA-256 of `git --no-replace-objects diff --cached --binary --no-textconv --no-ext-diff`
  = `616ec8836704ea38163b86fd1d0dd15c9d0f6f52c36d4bea90ec86ffb11ae5e2`; plan
  `112fb9bed3075a50addd3a74a7f001b1015005bc190f57b3fa90dddb63a58164`; no
  unstaged change). Hash and HEAD equal before the dispatch and after both
  reports (CB-4 practice).
- T4 (`dev-implementer`, role `implement`, `opus`/`high`): read back `PASS`,
  `floor=work`.
- Reviews: a deep review (role `review-deep`) and a Security Diff Scan (role
  `review-security`), both `opus`/`xhigh`, both read back `PASS` with
  `floor=review-scan` (result lines in the PR gate record comment). Both
  count.
- Result: deep review: 0 MUST-FIX, 1 SHOULD-FIX, 1 NIT. Security Diff Scan:
  status FINDINGS, 0 MUST-FIX, 1 SHOULD-FIX, 1 NIT. The two `SHOULD-FIX` have one
  subject. Private data: no hit (scan item 1). No staged file changes a rule, a
  script, an agent file or a test (scan item 3).
- Deep review items: R-VER-2 equal to the bound base, no record says that a
  change of it ships; U2R4-D-01, U2R4-D-02, U2R4-D-03, the Files row and the
  content of U3R1-D-04 resolved; the records of the card agree, zh and EN
  included; no false `noted` reason; plan E3 unchanged; Issue #101 Done when
  against Acceptance resolved. Item 3 (a disposition for each finding) not
  resolved.
- Search list K1 to K31: the deep review re-ran it: 357 rows, no difference;
  rule 1 passed on this target, which shows U3b alone.
- Deep review: 383 tests OK, 3 skipped; `check_pack.py` and
  `check_core_coverage.py` passed.
- Written per ASD-STE100 principles; full conformance not verified.

## Findings (reviewers' severities)

All open until the user answers `cards-15.md`.

| ID | Severity | Finding (own words) |
| --- | --- | --- |
| U3B-D-01 | SHOULD-FIX | U3R1-D-03 has no R-REV-3 disposition; U3R1-D-04 `Fixed` has no re-review; PS4-01 and PS4-02 have a class and no disposition; PS3-01 to PS3-03 `Fixed` have no fields. `dev-gate` step 4 lists a missing or incomplete disposition as a blocker |
| U3B-S-01 | SHOULD-FIX | same subject as U3B-D-01; also, PS4 rests only on the main agent's decision, and "a path sentence" does not say that it is no private path |
| U3B-S-02 | NIT | D-030 puts the copy of the diff (the main agent's action) under what the user decided, and "superseded for this PR" has no mark "inference" |
| U3B-D-02 | NIT | Issue #102 says that the fixes of `cards-14.md` option (a) were not made; items 7 (D-04) and 9 of that list were made here. The fixes of the exception text (items 1 to 6) were not |

Residual risks named (kept, among others): whether a `Deferred` MUST-FIX
(U3R1-S-01) is an unresolved one for `dev-gate` (the deep review reads no: the
text is withdrawn, and Core allows the four dispositions); three sentences
of the plan have no source or mark; the U3b commit rests on card I101-C3 (a),
whose U3 card I101-U3R1-C1 (b) replaced (inference); the `git restore` form of
the plan gives no path; R-REV-9 line 156 and R-REV-3 line 124 read differently
for a NIT of a scan (the scan reads: a NIT with a full disposition is no open
finding).

## R-VER-2: the stop rule fired

- Fact: U3 round 1 and this round both reported new `SHOULD-FIX` findings, so
  the first trigger holds by its words (`skills/dev-core/SKILL.md:195`), although
  the two rounds have different targets.
- Classification (inference): a quality failure of the records (the plan used
  words outside the four dispositions for a withdrawn target); not environment,
  permission or context. No escalation of the writing side.
- No fix starts before the user's answer.

## Lesson candidates

- Trigger: the stop rule fired; level L2. Observation (fact): the search list
  and the co-change rules gave no difference in 357 rows, and the list of
  dispositions is free text outside any check; for a withdrawn target the writer
  used words outside the four dispositions. Lesson (inference): a brief that
  moves findings names each ID and asks for one of the four dispositions.
  Events: 1. Coverage: R-REV-3, `dev-gate` step 4. Judgment: worth improving.
  Abstraction checklist: every item not present.
- Trigger: another gap; level L2. Observation (fact): R-REV-9 says that a finding
  blocks until it is fixed and scanned again, and R-REV-3 says that a NIT does
  not block once it has a disposition; no sentence says which one holds for a
  NIT of a scan. Lesson (inference): a NIT of a scan needs one reading. Events:
  1. Coverage: R-REV-3, R-REV-4, R-REV-9. Judgment: needs human decision.
  Abstraction checklist: every item not present.
