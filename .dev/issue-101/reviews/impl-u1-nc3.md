# Issue #101 U1 narrow confirmation NC3 (R-REV-4)

- Target: the unstaged diff, which holds the NIT fix after NC2 alone (SHA-256
  of `git --no-replace-objects diff --binary --no-textconv --no-ext-diff` =
  `41bd4996db83ca8e783e5780611fa6b6c84ef3be4ad4f0d889a87b9c02131dbb`; staged
  `7224fcc263e7410f8a2921bc63de94c288a896423e654f56da8523d57208d25e`). Both
  hashes were equal before the dispatch and after the report.
- Review: a deep review, narrow scope (role `review-deep`), `opus`/`xhigh`,
  read back `PASS`, `floor=review-scan` (result line in the PR gate record
  comment). It counts.
- Result: 0 MUST-FIX, 0 SHOULD-FIX, 1 NIT. NC2-01 and NC2-03 are resolved;
  NC2-02 stays as it is, with its reason (it is the record of its round).
  The diff changes nothing beyond those NITs and the recording of the card
  answer. Co-change rule 1: no requirement file in the fix, pass.
- Written per ASD-STE100 principles; full conformance not verified.

## Finding (reviewer's severity)

| ID | Severity | Finding (own words) |
| --- | --- | --- |
| NC3-01 | NIT | DL-047 ends with "the NIT exception is used once early for U1", without the card's conditions, and the plan says that the exception was not used; `REQ-029` (source locator) and D-030 hold the same summary of card I101-NC1-C1 (a) |

The reviewer accepts that 「NC2-C1 選 a」 stands in the plan only, because
plan C-2 triggers only for answers recorded in REQ-012 or REQ-029, but not
the plan's reason "a process decision": `dev-plan` rule 2 has no such
exemption, and this card did make a sentence elsewhere untrue.

## R-VER-2

- Fact: card I101-NC2-C1 (a) says that a new finding of any severity stops the
  work (`cards-9.md`). NC3-01 is new, so the work stops.
- Fact: the first trigger does not hold (NC2 and NC3 report no new `MUST-FIX`
  or `SHOULD-FIX`). Inference: the second trigger holds (copies not
  synchronized).
