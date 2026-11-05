# Issue #101 design review round 3 (scoped, on d3)

- Target: `.dev/issue-101/plan.md` d3 (SHA-256
  `e64abb32a3452cc735587bf4a0a8630f52b657413dc45fe2e03bed7a3a55c5c9`), with
  `cards-2.md` (`dffb8a8b…1388`) and `cards-3.md`
  (`fa0cf1d863f4607e31da384302bc4e02cd734c3531e3527a098125775d967502`) as
  the decided cards; untracked, base HEAD
  `c818e4dfd59a92650ba09d3f5d71c6da6a29ee01`, no tracked change. Source:
  `shasum -a 256`, `git rev-parse HEAD`, `git status --porcelain=v1
  --untracked-files=all`, before the dispatch and after both reports; all
  equal (CB-4).
- Reviews: a deep review (role `review-deep`) and a security review (role
  `review-security`), both dispatched with `opus`/`xhigh`, both read back
  with the stdin form at the bound base and `--floor review-scan`: both
  `PASS`, `floor=review-scan` (result lines in the PR gate record comment).
  Both count (R-DEL-2).
- Written per ASD-STE100 principles; full conformance not verified.

## Findings (reviewers' severities)

All in-scope. Disposition: Needs Human Decision until the user answers
`cards-4.md`; the last column says what the recommended option does.

| ID | Severity | Finding (own words) | Under card I101-R3-C1 (a) |
| --- | --- | --- | --- |
| DR3-01 | MUST-FIX | the private-source sentence of R-EVD-3 forbids session quotes and transcript values that REQ-008, R-DEL-2 and the `deltas.md` loosening record require | sentence removed; R-EVD-3 says it changes no locator, quote or R-DEL-2 record rule |
| DR3-02 | SHOULD-FIX | "a NIT that has a disposition is not a new blocker" ties the test to a disposition that does not exist yet when the stop rule is judged | "a NIT that a review reports is not a new blocker of this rule; it still gets a disposition (R-REV-3)" |
| DR3-03 | SHOULD-FIX | no trace row for card R2-C1 (a); E1.0 puts owned paths and the base ID into commands, outside the card's three value kinds | E1.0 puts no plan value into a command (below) |
| DR3-04 | SHOULD-FIX | node trees are unreachable objects: not pushed, may be pruned; a Merge Review in another clone stops | node trees are local evidence; the Merge Review runs rule 1 per commit of base..head and reuses the recorded node outputs with reason and coverage (R-EXH-3) |
| DR3-05 | NIT | two definitions of the tree before a node | one definition: the tree that the main agent records |
| DR3-06 | NIT | the plan asks T nodes to record outputs that only the main agent makes | the main agent records them |
| DR3-07 | NIT | the trace says "every hit" kept, but E1.1 excludes the objective's own record folder | the trace names the exclusion and its reason |
| DR3-08 | NIT | `R-VER-5` listed as a fix in `cards-3.md` but not in the search list | added |
| DR3-09 | NIT | the defect 3 example still stops under d3 by its words (the line-number edits); it holds only as a counterfactual with d3 row format | acceptance written as a counterfactual; the round-3 report contents marked unverified |
| SR3-01 | MUST-FIX | as DR3-03 (owned paths with globs into `git add`; base ID; no `--no-replace-objects` on `rev-parse`) | as DR3-03 |
| SR3-02 | MUST-FIX | d3 commits `cards-1.md`, which paraphrases a private instruction file, into a public repository | `cards-1.md` is never committed; its SHA-256 stays in the plan and in `design-round-1.md` |
| SR3-03 | SHOULD-FIX | the private-source sentence is too narrow (as DR3-01) and too wide ("marked unverified" lets private content into public records) | as DR3-01; private content of other kinds stays out by R-AUTH-7 and R-REV-8, which the rule cites |
| SR3-04 | SHOULD-FIX | the plan's round-3 stop sentence was narrower than R-VER-2 | the plan cites R-VER-2 only |
| SR3-05 | SHOULD-FIX | the narrow confirmation has no input to check condition (4), once per PR | each use is recorded in one fixed place: a "R-VER-2 exception uses" section of the plan, and after the PR exists the PR gate record comment; the brief gives both; a reviewer that cannot read them reports the check as failed |
| SR3-06 | NIT | as DR3-09 | as DR3-09 |

Residual risks named (kept): a requirements folder that is spelled wrong
passes rule 1 with an empty list (a `cat-file -t '<after>:<folder>/log.md'`
precondition is proposed); E1.4 binding commands lack
`--no-ext-diff --no-textconv`; stderr of a failed check can hold private
paths (record the exit code only); the R-VER-5 trigger "the stop rule
fired" when the exception applies; "which the user accepted" in the DL-048
reason is an inference and needs the mark.

## R-VER-2: the stop rule fired again

- Fact: rounds 2 and 3 both reported new MUST-FIX and SHOULD-FIX findings
  (`design-round-2.md`, this record), so the first trigger holds
  (`skills/dev-core/SKILL.md:195`). The second trigger holds too: E1
  values in commands (SR1-01 → SR2-01 → SR3-01), the R-EVD-3 source form
  (SR1-02 → DR2-03 → DR3-01) and E3 precision (DR1-02 → DR2-01 → DR3-02,
  SR3-05) each needed fixes in three rounds.
- Classification (inference): spec and design precision of new rule text,
  not environment, permission or context; no escalation of the writing
  side.
- Re-evaluation (R-RIG-4; inference): each round fixes the previous
  findings and the fix text itself adds a new edge (E1.0 commands, a new
  "never" sentence, a new definition). The rule text is the deliverable,
  so a design review and the implementation review read the same text.

## Lesson candidates

- Trigger: the stop rule fired (rounds 2 and 3); level L2. Observation
  (fact): a new "never" sentence was not applied to the plan's own existing
  records, which it then forbade (DR3-01). Lesson (inference): try each new
  prohibition on one existing record of each kind it covers before review.
  Events: 1. Coverage: R-REV-4. Judgment: worth improving. Smallest fix: a
  management measure in the fix brief (owner: the main agent; when it
  fails, the design review reports it). Abstraction checklist: every item
  not present.
- Trigger: the same kind of finding in three rounds (values in commands);
  level L2. Observation (fact): each fix that added a command brought a
  value kind that the value rule did not list (SR3-01). Lesson (inference):
  a fix that adds a command lists each placeholder with its source and
  check. Events: 1. Coverage: R-REV-9 step 7. Judgment: worth improving.
  Smallest fix: a placeholder table in the plan. Abstraction checklist:
  every item not present; vulnerability details turned into a category.
- Trigger: the same kind of finding again (private content, DR1-14 →
  SR3-02); level L2. Observation (fact): "commit as they are" was extended
  to a superseded card that an earlier finding had marked private. Lesson
  (inference): before a record is committed as it is, check it against the
  earlier privacy findings; a superseded record without an answer keeps
  only its hash. Events: 1. Coverage: R-AUTH-7, R-REV-9. Judgment: worth
  improving. Abstraction checklist: private instruction content turned into
  a category; every other item not present.
