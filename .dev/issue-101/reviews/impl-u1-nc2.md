# Issue #101 U1 narrow confirmation NC2 (R-REV-4)

- Target: the unstaged diff on top of the staged content (SHA-256 of
  `git --no-replace-objects diff --binary --no-textconv --no-ext-diff` =
  `ae632337a848aa3f70cae3f1c5fb5709b9033360ad215bdce0ef88a81eab53f0`; staged
  `58daf9ae65c1205c2aea3eac5aad6484662ad2ca73bdb20591299ce49ac46ce2`; plan
  `7d493d0b0f85db16ace8a7abc1cf9fa193789e5fc79bf784483ce3a4f5dfa661`). The
  two diff hashes were equal before the dispatch and after the report.
- The main session made the fix itself after its floor check.
- Review: a deep review, narrow scope (role `review-deep`), `opus`/`xhigh`,
  read back `PASS`, `floor=review-scan` (result line in the PR gate record
  comment). It counts.
- Result: 0 MUST-FIX, 0 SHOULD-FIX, 3 NIT. NC1-01 and NC1-02 resolved,
  NC1-03 partly (NC2-02). The rule matches `cards-7.md`, with no new
  mechanism. `scripts/validate.sh` passed: 375 tests OK, 3 skipped.
- Co-change rule 1, by the new rule: the target holds two fix rounds, so it
  is cumulative; the reviewer could not tell whether each `log.md` row came
  in the same change as its round, and this item does not count as passed.
  Two new `+|` rows name REQ-029, with no `-|` row.
- Written per ASD-STE100 principles; full conformance not verified.

## Findings (reviewer's severities)

All in-scope. Open until the user answers `cards-9.md`.

| ID | Severity | Finding (own words) | Text that it names |
| --- | --- | --- | --- |
| NC2-01 | NIT | the Files row of the plan stops at `cards-7.md`, and Decisions says `cards-8.md` | the file list of that row |
| NC2-02 | NIT | `reviews/impl-u1-round-3.md` still says `plan.md:295`; NC1-03 named it | the number `295`, or keep as is, with the reason that it is that round's record |
| NC2-03 | NIT | the `Source:` and `Quote:` lists of the DL-047 Reason cell name four cards and four answers, and the same row uses card I101-IR3-C1 (a) | those two lists |

Residual risks named (kept, among others): "no check that did not run" is
not in the `dev-review` step 2 text, and subagents do not read `dev-plan`;
"shows the change" and "the diff that it reviews" are two wordings of one
sentence; the plan's check outputs predate two fixes, and K18 to K23 are not
run yet; plan C-2 and the DL-048 sources need card I101-NC1-C1 (a) in U3.

## R-VER-2

- Fact: the first trigger does not hold (no new `MUST-FIX` or `SHOULD-FIX`).
- Inference: the second trigger holds (NC2-01 and NC2-03 are the same
  mechanism as NC1-02: copies not synchronized).
- Exception of card I101-NC1-C1 (a): condition (2) of `cards-2.md:22` says "no
  part that a reviewer could not check". The reviewer could not check one
  part on this cumulative target, and no card says how that limit relates to
  condition (2). By its words, condition (2) does not hold. The main agent
  does not decide this: `cards-9.md`.
