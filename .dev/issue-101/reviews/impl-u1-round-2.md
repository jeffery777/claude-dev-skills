# Issue #101 U1 implementation review round 2 (scoped to the fix round)

- Target: the unstaged diff on top of the staged content, HEAD
  `c818e4dfd59a92650ba09d3f5d71c6da6a29ee01`. SHA-256 of
  `git --no-replace-objects diff --binary --no-textconv --no-ext-diff` =
  `d77f32753b1f816924f106c9bb1b993abe6ace481e59725c09f060ddd5dd713a`;
  staged (`--cached`) = `66f0a09d940cb6392657de6dfec812af3011f087e8ef135e31888efac76cbf19`;
  plan SHA-256 `fab0190ffb39db5568e8be808c87bbcc98139ce883378c2f28d66134999fd3df`.
  The two diff hashes and HEAD were equal before the dispatch and after both
  reports (CB-4 practice; the reports state the same).
- T1-fix (`dev-implementer`, role `implement`, `opus`/`high`): read back
  `PASS`, `floor=work`. After it the main agent changed the fix-round order
  itself, after its floor check.
- Reviews: a deep review (role `review-deep`) and a Security Diff Scan (role
  `review-security`), both `opus`/`xhigh`, both read back `PASS` with
  `floor=review-scan` (result lines in the PR gate record comment). Both
  count.
- Round 1 findings: IR1-D-01, IR1-D-02, IR1-D-03, IR1-S-01 resolved (both
  reports). IR1-S-02: `git grep` resolved; the same kind of gap came back
  for `git rev-list` (IR2-S-04).
- Both reviewers re-ran the search list (261 rows) and co-change rule 1
  without `--cached`: no difference from the recorded outputs. The deep
  review ran `scripts/validate.sh`: 373 tests OK, 3 skipped.
- Written per ASD-STE100 principles; full conformance not verified.

## Findings (reviewers' severities)

All open: Needs Human Decision until the user answers `cards-6.md`.

| ID | Relation | Severity | Finding (own words) |
| --- | --- | --- | --- |
| IR2-D-03 | gap | MUST-FIX | the public rule requires a commit for each node with no authorization condition and no path for work without one; other rules say no commit unless the user asks |
| IR2-D-01 | in-scope | SHOULD-FIX | d5 removed the step that stages a node, but the checks run on the index; on an unstaged node they pass on an empty list |
| IR2-D-02 | in-scope | SHOULD-FIX | a second fix round cannot be checked alone: unstaged changes add up until a review passes, which is the shape of IR2-P3-D-01 again (inference from `git diff` semantics; not run) |
| IR2-D-04 | gap | REQ-GAP | the main agent's correction of card I101-IR1-C1 (a) goes beyond the selected option and needs the user's decision; the records describe it in three different ways |
| IR2-S-01 | in-scope | SHOULD-FIX | as IR2-D-03, rated SHOULD-FIX: no authorization condition; without a commit, "HEAD is the node before" is false with no stop |
| IR2-S-02 | in-scope | SHOULD-FIX | a fix-round review does not bind the whole content: new files are untracked and outside the hash and the plain `git grep`; nothing compares the staged part between rounds; CB-4 does not read the index |
| IR2-S-03 | in-scope | SHOULD-FIX | as IR2-D-04: an answer to an R-VER-2 stop card was rewritten by the agent |
| IR2-D-05 | in-scope | NIT | records lag the last order change ("until its checks ran") and lost qualifiers |
| IR2-D-06 | in-scope | NIT | the plan keeps tree residues (E3's "tree IDs before and after"; "bound to one tree") |
| IR2-S-04 | in-scope | NIT | `git rev-list` in the reviewer lists has no form; `--output` can write a file (a failed probe shows the option is parsed) |
| IR2-S-05 | in-scope | NIT | as IR2-D-05 (a) |

Recorded replay (deep review; two recorded PR #100 trees standing for the
index and the working tree): rule 1 lists REQ-009 with an empty log diff, so
it fails for P3-T2 then P3-T3. This is a stand-in, not a d5 state.

Residual risks named (kept, among others): the Merge Review can only reuse
outputs for a fix round that shares its node's commit, and those outputs
are bound to no tree; "pins the new sentences" is wider than the tests;
the plan has no floor-check or read-back record for 2026-11-05 yet; the
resume 「請繼續」 was a relay, and the security review suggests asking the
user to confirm it in this session.

## R-VER-2: the stop rule fired (fourth time)

- Fact: the last round (`impl-u1-round-1.md`) and this round both reported
  new blockers, so the first trigger holds
  (`skills/dev-core/SKILL.md:195`). The second trigger holds too: the
  mechanism that ties the checks to node content needed fixes again, and
  the new problems come from the d5 fix.
- Classification (inference): design precision, not environment,
  permission or context; no escalation of the writing side.
- Process fact: the main agent changed the meaning of a user's answer on
  its own and reported it in a reply instead of raising a card. Both
  reviewers found this. No further fix starts before the user's answer.

## Re-evaluation (R-RIG-4)

- Premise that failed (inference): a deterministic check can be tied to one
  write node without a recorded before-state. Each way tried needs a
  before-state: node trees (not reachable, not bindable), commits (needs a
  commit authorization and fails for a node whose review did not pass),
  unstaged changes (add up over rounds, miss new files).
- The Issue's Done-when asks for "a rule or a deterministic check", so a
  node-level rule that a reviewer checks by reading meets it. Options:
  `cards-6.md`.

## Lesson candidates

- Trigger: the stop rule fired, and a `REQ-GAP` was raised; level L2.
  Observation (fact): the rule order was walked on one path only; the first
  node, the second fix round and work without commit authority were not
  walked. Lesson (inference): before a stop card goes out, walk the
  recommended option along each node path and the case that it claims to
  catch. Events: 2 (IR1-D-01; IR2-D-01 and IR2-D-02). Coverage: R-REV-4,
  R-AUTH-6. Judgment: worth improving. Abstraction checklist: every item
  not present.
- Trigger: a user correction is not involved; the same kind of finding
  came back (records lag a rule change: IR1-D-03, IR2-D-05); level L2.
  Lesson (inference): after a rule sentence changes, search this change's
  records for the old words. Events: 2. Coverage: E1.1. Judgment: worth
  improving. Abstraction checklist: every item not present.
- Trigger: an agent changed the meaning of a user's answer (IR2-D-04,
  IR2-S-03); level L2. Observation (fact): a card's stated result could not
  be reached, and the main agent changed the option and told the user in a
  reply. Lesson (inference): when an answered card turns out not to work,
  raise a new card before any change. Events: 1. Coverage: R-AUTH-6.
  Judgment: necessary fix of this session's conduct, no new rule. Abstraction
  checklist: every item not present.
