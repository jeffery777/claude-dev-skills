# Issue #101 U2 implementation review round 1

- Target: the staged diff against HEAD `2c68faedf14a5f7692f3f296a9b7f88322d78ab6`
  (SHA-256 of `git --no-replace-objects diff --cached --binary --no-textconv --no-ext-diff`
  = `ffc91736be3bc5561526683afaa39e70f7991be324bfa9b78b690099cde89449`; plan
  `a88e329b222707b0f6bf34dab8f80e5e2849434394ac26df4ec710603ba8409a`). The
  hash and HEAD were equal before the dispatch and after both reports.
- T2 (`dev-implementer`, role `implement`, `opus`/`high`): read back `PASS`,
  `floor=work`.
- Reviews: a deep review (role `review-deep`) and a Security Diff Scan (role
  `review-security`), both `opus`/`xhigh`, both read back `PASS` with
  `floor=review-scan` (result lines in the PR gate record comment). Both count.
- Both reviewers re-ran the search list (292 rows) and co-change rule 1 with
  `--cached`: no difference. This target holds U2 alone, so the reading check
  of rule 1 passed. The deep review ran `scripts/validate.sh`: 378 tests OK,
  3 skipped.
- NC3-01 is resolved (deep review): DL-047, REQ-029 and D-030 keep the card's
  conditions and say that the exception was not used.
- R-EVD-3 equals plan E2.1 word for word (deep review). Accepted: the three
  wording choices of the implementer, and the reading that a report is the
  original source of "the report says X", which does not cover X itself.
- Written per ASD-STE100 principles; full conformance not verified.

## Findings (reviewers' severities)

All in-scope. Open until the user answers `cards-11.md`.

| ID | Severity | Finding (own words) |
| --- | --- | --- |
| U2-S-02 | SHOULD-FIX | neither R-AUTH-7 nor R-REV-8 covers the content of private files other than identifiers, so after the deletion of the private-source sentence only the R-REV-9 scan stops it; card I101-R3-C1 (a) did not name this loss. The sentence of `design-round-3.md` that says those rules cover it does not hold by their words |
| U2-S-01 | SHOULD-FIX | the copied source sentence names R-REV-8 and R-AUTH-7, but `dev-implementer` and `dev-explorer` do not hold their text, and the sentence after the receipt in `task-brief.md` is outside the templates |
| U2-D-01 | SHOULD-FIX | 251 `noted` rows give one reason, "the lines are the same as at HEAD", which does not say why the old text stays true; the K4 row of REQ-025 is really `historical` |
| U2-S-03 | NIT | "masked as ... R-AUTH-7 say" is not exact: R-AUTH-7 is a ban, not a masking rule |
| U2-D-02 | NIT | the CHANGELOG leaves out "after the writer read that source" |
| U2-D-03 | NIT | CHANGELOG and DL-047 say the test "pins the definition of R-EVD-3"; it pins that R-EVD-3 is defined once |

Residual risks named (kept, among others): the plan has no rule 1 output for
U2 yet and its U1 scan sentence gives no source; the read-back clause of
R-EVD-3 has no bound on which files; whether the relay of 「NC3-C1 a」 counts
rests on a practice, not a rule; a reviewer has no named place for a sentence
that it cannot judge true or false.

## R-VER-2

- Fact: this is the first review round of U2. The first trigger does not hold
  inside U2.
- The two reports differ on the second trigger: the security review counts
  U2-S-01 and U2-S-02 as the R-EVD-3 source mechanism of the design rounds; the
  deep review does not. Inference: the stricter reading applies, and U2-S-02
  needs the user in any case.

## Lesson candidates

- Trigger: the same kind of finding (private content: DR1-14, SR3-02, U2-S-02);
  level L2. Observation (fact): a deletion fix named two other rules as the
  protection, and their words do not list the deleted case. Lesson
  (inference): when a deletion points to another rule, try the deleted case on
  that rule's words, and tell the user what the deletion gives up. Events: 1.
  Coverage: R-REV-4, R-AUTH-6. Judgment: worth improving. Abstraction
  checklist: private instruction content turned into a category; every other
  item not present.
- Trigger: a rule does not reach subagents (SR2-08, U2-S-01); level L2. Lesson
  (inference): a copy for a subagent must work for a reader who has only the
  agent file and the brief. Events: 2. Coverage: REQ-024. Judgment: worth
  improving. Abstraction checklist: every item not present.
