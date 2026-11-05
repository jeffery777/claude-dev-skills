# Issue #101 U1 narrow confirmation NC1 (R-REV-4)

- Target: the unstaged fix diff of card I101-IR3-C1 (a) on top of the staged
  content (SHA-256 of `git --no-replace-objects diff --binary --no-textconv --no-ext-diff`
  = `a46ea892d978cba2e7db4c1b6ac70651134b3f14552d3f0446024f689d6b7ee9`;
  staged `58daf9ae65c1205c2aea3eac5aad6484662ad2ca73bdb20591299ce49ac46ce2`;
  plan `a605f268d8fc9e38ec504974ad8e65e481cb6050ffa516dc16912350365bd140`).
  The two diff hashes were equal before the dispatch and after the report.
- The main session made this fix itself after its floor check.
- Review: a deep review, narrow scope (role `review-deep`), `opus`/`xhigh`,
  read back `PASS`, `floor=review-scan` (result line in the PR gate record
  comment). It counts.
- Result: the card's actions are in the rule, with no new mechanism and no
  scope creep; IR3-D-01, IR3-D-02, IR3-D-03 and IR3-S-01 are resolved in the
  rule text. The reviewer's `validate.sh` run passed; it repeated the PR #100
  tree test with the same result.
- Written per ASD-STE100 principles; full conformance not verified.

## Findings (reviewer's severities)

All in-scope. Open until the user answers `cards-8.md`.

| ID | Severity | Finding (own words) |
| --- | --- | --- |
| NC1-01 | SHOULD-FIX | the rule is narrower than the card: `cards-7.md:49` says that on a cumulative target the report states the limit and this item does not count as passed, and the rule keeps only "the report says so"; the plan has no trace row for card I101-IR3-C1 (a). The reviewer warns: this is not a "did not run" case, which would stop every round on a cumulative target |
| NC1-02 | NIT | the fix changed only some copies: D-030 items 2 and 6 (zh and EN), DL-047, the REQ-029 Need and plan Acceptance still use the old words ("no command runs", "reports differences", "the diff that it reviews", "as card I101-IR2-C1 (a) states", design d6) |
| NC1-03 | NIT | `.dev/issue-96-pr3/plan.md:295` is off by one; the text is at line 296 (also in `cards-7.md` and `impl-u1-round-3.md`; the card is not edited) |

Residual risks named (kept, among others): the plan's check outputs predate
this fix and must be run again before the commit; the D-030 list of the user's
words, the CHANGELOG answer list and the DL-047 Source and Quote cells do not
name this answer yet; the tests pin the limit sentence but not "the fix diff".

## R-VER-2: the stop rule fired (sixth time, by the strict reading)

- Fact: round 3 reported a new `SHOULD-FIX` (IR3-D-01) and this confirmation
  reported a new `SHOULD-FIX` (NC1-01), both on the reading check of
  co-change rule 1. `skills/dev-core/SKILL.md:195` says "two consecutive
  review rounds" and does not leave out the narrow confirmation of R-REV-4.
- Inference: this counts as a round; the strict reading applies, because the
  rule does not say otherwise and the reviewer recommends it.
- Classification (inference): a card condition that the fix did not carry
  over, and copies that were not synchronized; not environment, permission
  or context. The Security side is not involved.
- No fix starts before the user's answer.

## Lesson candidates

- Trigger: the stop rule fired, and a spec lost a condition of its source;
  level L2. Observation (fact): the rule sentences came from the option's
  actions, and the result condition in the card's path list did not reach the
  rule; the plan has no trace row for this card. Lesson (inference): read a
  card's paths for conditions too, and add one trace row for each new card.
  Events: 1. Coverage: `dev-plan` step 2, REQ-027. Judgment: worth improving.
  Abstraction checklist: every item not present.
- Trigger: the same kind of finding (copies not synchronized); level L2.
  Observation (fact): the search list holds no string of the sentences that
  the fix changed. Lesson (inference): when a fix changes a rule sentence, add
  its words to the search list and run it before the review. Events: 1 in this
  round. Coverage: E1.1, R-EXH-2. Judgment: worth improving. Abstraction
  checklist: every item not present.
