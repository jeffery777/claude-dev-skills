# Issue #101 U2 implementation review round 3 (scoped to the fix round, d8)

- Target: the unstaged diff, which holds the fix round alone (SHA-256 of
  `git --no-replace-objects diff --binary --no-textconv --no-ext-diff` =
  `2106616f942cdca0f7c3476a0eeb349361b33a98099018afa9abf0c2a11a4db5`; staged
  `256b349b0f7736225486c7f7afc20f1a2dcb6d87469a66792c1d97fe723fad39`; plan
  `7fcea85e44494af006a4f5953d981c30c40d6dc2e6b7172e474bcb6e987c325e`). The
  two diff hashes were equal before the dispatch and after both reports.
- T2-fix2 (`dev-implementer`, role `implement`, `opus`/`high`): read back
  `PASS`, `floor=work`.
- Reviews: a deep review (role `review-deep`) and a Security Diff Scan (role
  `review-security`), both `opus`/`xhigh`, both read back `PASS` with
  `floor=review-scan` (result lines in the PR gate record comment). Both count.
- Round 2: the deep review finds all seven groups resolved. The security
  review finds U2R2-S-01 partly resolved and S-02 to S-05 resolved.
- `scripts/validate.sh` (deep review): 383 tests OK, 3 skipped. Search list: 29
  strings, 344 rows, no difference.
- The implementer's handling of the R-REV-9 phrase "chosen to publish" is right
  (deep review); the `dev-retro` citation is no false statement (deep review).
- Written per ASD-STE100 principles; full conformance not verified.

## Findings (reviewers' severities)

All open until the user answers `cards-13.md`.

| ID | Severity | Finding (own words) |
| --- | --- | --- |
| U2R3-S-01 | MUST-FIX | "Files of this pack are not private files" has no bound: in this pack's own repository it can only exclude untracked or ignored files, the very thing the class protects (`cards-1.md` is such a file); it also touches the words "private files" of R-REV-9, which is a loosening, so DL-047 `tighten` does not hold for it |
| U2R3-S-02 | MUST-FIX | "what the user says in a message is no file" fails for pasted text, and it clashes with drawing the line by source: a pasted part of a private instruction file is both "in the class" and "outside it" |
| U2R3-D-01 | SHOULD-FIX | the floor-check model and effort are copied from a transcript file, so the walk "not file content" does not hold; with the exception sentence gone, R-AUTH-7 and R-DEL-2 clash by their words (`cards-12.md:51`; U2R3-S-03 is the same point, NIT) |
| U2R3-D-02 | NIT | the K28 reason of the REQ-015 row does not fit that hit |
| U2R3-D-03 | NIT | the plan headings still say d7 |

## R-VER-2: the stop rule fired

- Fact: rounds 2 and 3 of U2 both report new blockers on the private-content
  class of R-AUTH-7. Inference: both triggers hold.
- Classification (inference): spec precision of text that the main agent
  drafted; not environment, permission or context.
- Re-evaluation (inference): three rounds drew a line of what does not count,
  and each exclusion (author, pack, message, field) had a hole, because the
  class was general and needed exclusions. A short class with no exclusions
  needs none: `cards-13.md`.

## Lesson candidates

- Trigger: the stop rule fired, and the same kind of finding came back a third
  time; level L2. Observation (fact): an exclusion written for one situation
  excluded the protected content in another repository state. Lesson
  (inference): prefer a narrow list to a wide class with exclusions, and walk
  each exclusion where the protected content lives. Events: 3. Coverage: R-REV-4,
  R-AUTH-6. Judgment: necessary fix. Abstraction checklist: private instruction
  content turned into a category; every other item not present.
