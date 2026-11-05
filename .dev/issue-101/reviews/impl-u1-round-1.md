# Issue #101 U1 implementation review round 1

- Target: the staged diff against HEAD `c818e4dfd59a92650ba09d3f5d71c6da6a29ee01`
  (SHA-256 of `git --no-replace-objects diff --cached --binary --no-textconv --no-ext-diff`
  = `66f0a09d940cb6392657de6dfec812af3011f087e8ef135e31888efac76cbf19`; full
  staged tree `cabb8fb6beac702566c301d4dbed8a7abc80d1f9`; T1 node tree
  `92da6436d0ef2f702a3b9e9ba504c9927deb2baf`). The hash, HEAD and the
  unstaged diff (empty) were equal before the dispatch and after both
  reports (CB-4). `cards-1.md` stays untracked.
- T1 (`dev-implementer`, role `implement`, `opus`/`high`): read back `PASS`,
  `floor=work`. After T1 the main agent changed one sentence of
  `skills/dev-plan/SKILL.md` and the plan (the base-tree command now ends in
  `^{tree}`), after its own floor check.
- Reviews: a deep review (role `review-deep`) and a Security Diff Scan (role
  `review-security`), both `opus`/`xhigh`, both read back `PASS` with
  `floor=review-scan` (result lines in the PR gate record comment). Both
  count. They also stand in for design review round 4 (card I101-R3-C1 (a)).
- Both reviewers re-ran the search list K1 to K17 and co-change rule 1 on
  the T1 trees: equal to the recorded outputs (no difference). Both re-ran
  the unit tests: 371 OK, 3 skipped.
- Written per ASD-STE100 principles; full conformance not verified.

## Findings (reviewers' severities)

All in-scope. Disposition: Needs Human Decision until the user answers
`cards-5.md`.

| ID | Severity | Finding (own words) |
| --- | --- | --- |
| IR1-D-01 | SHOULD-FIX | the binding check `diff --cached --quiet '<tree ID>'` is meant for the node tree that the brief gives, but the node tree can never equal the index, because the records that hold the node outputs are staged after it; tested: exit 1 on the T1 node tree, exit 0 on the full staged tree, which no rule defines |
| IR1-D-02 | SHOULD-FIX | the owned-path check reads `git status --porcelain`, which compares the index with HEAD, so it lists the paths of earlier nodes and of the records; for any second node of a unit it cannot pass, and the rule gives no stop when it fails |
| IR1-S-01 | SHOULD-FIX | the binding check lacks `--no-ext-diff --no-textconv --ignore-submodules=none`, so a trusted external diff helper or `submodule.<name>.ignore=all` can make it pass on a different index (not reproduced; this repository has no gitlink, no `.gitmodules`, no diff config) |
| IR1-D-03 | NIT | D-030 (zh and EN) says the records were missed in five rounds, but the Issue says "incomplete or not exact"; DL-047 quotes it right |
| IR1-S-02 | NIT | the reviewer Bash lists add `git grep` without the brief's form; `-O<pager>` and `--textconv` can run programs |

Residual risks named (kept, among others): the value rule's patterns have
no anchor ("the whole value matches"); a staged path outside the owned
paths has no stated stop; the Merge Review per-commit run has no command
form for commit IDs and merge commits; the tests do not pin every new
sentence, so "pins the new sentences" in the plan is wider than the tests;
the plan headings still say d3; `REQ-024:67` supports "do not load
`dev-core`" only; the plan's sentence "by card I101-C5 (a) a relay counts"
for card I101-R3-C1 is not what C5 (a) says (its option covers C1; its
recommendation sentence names C2 to C4), and "no loosening" is a judgment
without a mark.

## R-VER-2: the stop rule fired (third time)

- Fact: design review round 3 reported new MUST-FIX findings
  (`design-round-3.md`), and this round reports new SHOULD-FIX findings, so
  the first trigger holds (`skills/dev-core/SKILL.md:195`). The second
  trigger holds too: the E1 tree binding needed fixes in design rounds 1 to
  3 (SR1-06, SR2-03, DR2-07, DR3-04, DR3-05) and again here, and the new
  problems come from the d4 fix (node trees, the `git status` reading).
- Card I101-R3-C1 (a) says that a new blocker of the same mechanism in this
  review stops again (`cards-4.md`).
- Classification (inference): design precision of E1's tree mechanism, not
  environment, permission or context; no escalation of the writing side.
- No fix round starts before the user's answer.

## Lesson candidates

- Trigger: the stop rule fired; level L2. Observation (fact): the binding
  command of `dev-review` step 2 was not tried on the plan's own recorded
  node tree before the review; tried now, it exits 1 (IR1-D-01). Lesson
  (inference): before a review, run each new command form of a rule once on
  the change's own records, in the order the rule gives. Events: 1.
  Coverage: R-REV-4. Judgment: worth improving. Abstraction checklist:
  every item not present.
- Trigger: the same kind of finding again (a record says more than its
  source: DR2-02, DR3-09, IR1-D-03); level L2. Observation (fact): D-030
  dropped the qualifier "or not exact" of its source. Lesson (inference):
  write the qualifiers of the source with the fact. Events: 1. Coverage:
  R-EVD-3 (U2). Judgment: keep as is until U2 is in force. Abstraction
  checklist: every item not present.
