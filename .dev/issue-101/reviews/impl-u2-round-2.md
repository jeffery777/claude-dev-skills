# Issue #101 U2 implementation review round 2 (scoped to the fix round)

- Target: the unstaged diff, which holds the fix round alone (SHA-256 of
  `git --no-replace-objects diff --binary --no-textconv --no-ext-diff` =
  `c0ab85ec8bba041ae0758612857982e4e356ed616a16ddf080d1bdca0270844a`; staged
  `ffc91736be3bc5561526683afaa39e70f7991be324bfa9b78b690099cde89449`; plan
  `9c817622180f61108dbafb939a658778a3496098a401650f7e9559bac57e9f96`). The
  two diff hashes were equal before the dispatch and after both reports.
- T2-fix (`dev-implementer`, role `implement`, `opus`/`high`): read back
  `PASS`, `floor=work`.
- Reviews: a deep review (role `review-deep`) and a Security Diff Scan (role
  `review-security`), both `opus`/`xhigh`, both read back `PASS` with
  `floor=review-scan` (result lines in the PR gate record comment). Both count.
- Round 1 findings: U2-S-01, U2-S-03, U2-D-02, U2-D-03 resolved; U2-S-02 and
  U2-D-01 partly. `scripts/validate.sh` (deep review): 381 tests OK, 3 skipped.
- The difference from card I101-U2S-C1 (a) ("the same sentence" against the
  private-data sentence): both reviewers say that it stays inside the option,
  because it is stricter; both reject the plan's reason for it.
- Written per ASD-STE100 principles; full conformance not verified.

## Findings (reviewers' severities; highest of the two)

All open until the user answers `cards-12.md`.

| ID | Severity | Finding (own words) |
| --- | --- | --- |
| U2R2-S-01 = U2R2-D-02 | MUST-FIX | the exception sentence of R-AUTH-7 draws its line by who wrote a text, not by where it comes from; a user's private instruction file is the user's own words, so a verbatim quote of it passes as a source, while a paraphrase does not. Only the R-REV-9 scan stops it |
| U2R2-S-03 = U2R2-D-01 | SHOULD-FIX | the class has no public-file line: by its words it covers tracked `CLAUDE.md` and `AGENTS.md`, agent files, and pack files outside a target repository, which R-AUTH-6 tells agents to quote |
| U2R2-S-02 | SHOULD-FIX | "chosen to publish" gives no form for the choice; an agent can read "read this file" as a choice to publish |
| U2R2-S-04 = U2R2-D-03 | SHOULD-FIX, REQ-GAP | the two reviewer agent files do not have the new class, and their reports are committed |
| U2R2-S-05 = U2R2-D-04 | NIT | the plan's reason ("records that subagents do not write") is not true; REQ-029 and D-030 give the private-data sentence as the card's answer |
| U2R2-D-05 | NIT | three K4 `noted` rows state what R-DEL-1 holds and should be `historical` |
| U2R2-D-06 | NIT | the Files table does not show R-AUTH-7 and the new tests |

## R-VER-2: the stop rule fired

- Fact: U2 round 1 and this round both report new `SHOULD-FIX` findings, and
  this round a `MUST-FIX`. The second trigger holds by both reports (inference):
  the fix of the private-content text brought new problems. The E3 exception
  is in no rule and would not cover these.
- Classification (inference): spec precision of a rule that the main agent
  drafted; not environment, permission or context.
- Re-evaluation: both main findings come from the same choice: the class names
  kinds of file, and the exception names an author. A class drawn by where the
  content comes from needs no exception (`cards-12.md`).

## Lesson candidates

- Trigger: the stop rule fired, and a `REQ-GAP` was raised; level L2.
  Observation (fact): an exception for the user's answers used authorship as
  its test, and the protected files have the same author; the card's walk did
  not try the protected content itself. Lesson (inference): test an exception
  on the content it protects, and draw the line by channel, not by author.
  Events: 1. Coverage: R-REV-4, R-AUTH-6. Judgment: necessary fix. Abstraction
  checklist: private instruction content turned into a category; every other
  item not present.
- Trigger: the same kind of finding (a rule does not reach a role: SR2-08,
  U2-S-01, U2R2-S-04); level L2. Lesson (inference): list every role whose text
  goes into records, not only the roles with write tools. Events: 3. Coverage:
  REQ-024. Judgment: worth improving. Abstraction checklist: every item not
  present.
