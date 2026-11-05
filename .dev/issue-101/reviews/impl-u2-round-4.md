# Issue #101 U2 implementation review round 4 (scoped to the fix round, d9)

- Target: the unstaged diff, which holds the fix round alone (SHA-256 of
  `git --no-replace-objects diff --binary --no-textconv --no-ext-diff` =
  `90c4d0eed985b854f3a4315a4e2aa0aca5a274ebead77ea2bb40c13fcad86e93`; staged
  `76ed0e64ac28d52d884fcd30d79da0bf6de6b6247a8365d22bf012c3991dee84`; plan
  `244f14fc9a85daef435862c3face5cb101f4d79c4d66469fb48d06f508f78943`). The diff
  hash was equal before the dispatch and after both reports.
- T2-fix3 (`dev-implementer`, role `implement`, `opus`/`high`): read back
  `PASS`, `floor=work`.
- Reviews: a deep review (role `review-deep`) and a Security Diff Scan (role
  `review-security`), both `opus`/`xhigh`, both read back `PASS` with
  `floor=review-scan` (result lines in the PR gate record comment). Both count.
- Result: Security Diff Scan: no finding, status PASSED for the fix round. Deep
  review: 0 MUST-FIX, 0 SHOULD-FIX, 3 NIT, all in record text. The ceiling of
  card I101-U2R3-C1 (a) does not apply: no finding on the R-AUTH-7 sentence.
- Round 3: U2R3-S-01, S-02, S-03, D-01, D-02 and D-03 are resolved (both reports).
  Both walked the paths of `cards-13.md` and found that the rule text gives
  those results; DL-047 `tighten` holds against `main`.
- `scripts/validate.sh` (deep review): 383 tests OK, 3 skipped.
- Written per ASD-STE100 principles; full conformance not verified.

## Findings

| ID | Severity | Finding (own words) | Disposition |
| --- | --- | --- | --- |
| U2R4-D-01 | NIT | D-030 (zh and EN) says that items 5 to 11 are of 2026-11-05, and item 12 is too | `Deferred` to T3 (plan, Deferred findings) |
| U2R4-D-02 | NIT | the plan's revision chain goes from d9 to d7, and `impl-u2-round-3.md` names d8 | `Deferred` to T3 |
| U2R4-D-03 | NIT | the Files table says "the R-AUTH-7 sentences"; it is one sentence now | `Deferred` to T3 |

Residual risks named (kept, among others): "in any form" can be read as
qualifying the whole list, with the same result on every path walked; "private
instruction files" rests on judgment (`cards-13.md`); other private files have
only the R-REV-9 scan (the limit that the card states); the source of "the
practice of Issue #96" is not in the plan (the security review found relay
records in `.dev/issue-96-*/plan.md` and `.dev/issue-95-*/plan.md`).

## R-VER-2

- Fact: no new `MUST-FIX` or `SHOULD-FIX`, so the first trigger does not hold.
- Inference: the second trigger depends on the mechanism: "the R-AUTH-7 text"
  has no new problem; "records after a rule change" had NITs in rounds 3 and 4.
  The rule stops the next fix round; no fix round starts here: the three NITs
  have a full `Deferred` disposition (R-REV-3), and T3 changes the same records,
  as card I101-NC3-C1 (a) did for NC3-01.
