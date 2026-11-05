---
id: REQ-029
title: Review loop - deterministic completeness checks and sources of new facts (Issue #101)
status: active
sources:
  - type: issue
    locator: "GitHub Issue #101 body, Proposed direction, bullet Deterministic completeness checks, first sub-item (search list)"
    quote: "a search list (for example `git grep -F` strings) in the plan, where every hit is changed, noted or marked historical, and checked one to one"
  - type: issue
    locator: "GitHub Issue #101 body, Proposed direction, bullet Deterministic completeness checks, second sub-item (co-change rules)"
    quote: "co-change rules: a change to a requirement adds a log row, and a user decision quote goes into the CHANGELOG quote list."
  - type: issue
    locator: "GitHub Issue #101 body, Proposed direction, bullet Evidence rule"
    quote: "every new fact sentence in records, cards and briefs gives its test or source, or says it is an inference. Briefs pass facts with their source, not as bare text."
  - type: issue
    locator: "GitHub Issue #101 body, Done when, first item"
    quote: "The three defects above have a rule or a deterministic check, each with a test or a recorded example."
  - type: chat
    locator: "Claude Code session 2026-11-04 (Issue #101 session), user answer to the cards of `.dev/issue-101/cards-2.md` (SHA-256 dffb8a8b…1388): cards I101-C1 to I101-C5, each option (a); C2 (a): rule-text commands, no script; C3 (a): three review units in one PR, one after the other"
    quote: "C1 a，C2 a，C3 a，C4 a，C5 a"
  - type: chat
    locator: "Claude Code session 2026-11-04 (Issue #101 session), user answer to the cards of `.dev/issue-101/cards-3.md` (SHA-256 fa0cf1d8…7502): cards I101-R2-C1 and I101-R2-C2, each option (a); R2-C1 (a): the completeness checks keep only two command forms whose values are checked tree IDs, fixed paths and checked strings, and quotes are checked by reading"
    quote: "R2-C1 a，R2-C2 a"
  - type: chat
    locator: "Claude Code session 2026-11-04 (orchestrator session, relayed to the Issue #101 session), user answer to the card of `.dev/issue-101/cards-4.md` (SHA-256 4ef1edde…c265): card I101-R3-C1, option (a): fix the design review round 3 findings by deletion, then U1; confirmed by the user's own message in the Issue #101 session: 「R3-C1 a 確認」 (card I101-IR1-C2 (a), the next source)"
    quote: "同意你建議a"
  - type: chat
    locator: "Claude Code session 2026-11-04 (Issue #101 session), user answer to the cards of `.dev/issue-101/cards-5.md` (SHA-256 cc16819d…2966): cards I101-IR1-C1 and I101-IR1-C2, each option (a); IR1-C1 (a): every write node, fix rounds included, is committed after its review passes, and the checks bind to the index and to commit IDs (replaced by card I101-IR2-C1 (a), the next source); IR1-C2 (a): the user confirms card I101-R3-C1 (a) in that session"
    quote: "IR1-C1 a，IR1-C2 a，R3-C1 a 確認"
  - type: chat
    locator: "Claude Code session 2026-11-05 (Issue #101 session), user answer to the cards of `.dev/issue-101/cards-6.md` (SHA-256 2341b626…92d6): cards I101-IR2-C1 and I101-IR2-C2, each option (a); IR2-C1 (a): at node level a rule that a reviewer checks by reading, and commands only before a commit and in the Merge Review; IR2-C2 (a): the user confirms the resume in that session"
    quote: "都選 a"
  - type: chat
    locator: "Claude Code session 2026-11-05 (Issue #101 session), user answer to the card of `.dev/issue-101/cards-7.md` (SHA-256 10bb1355…1a5b): card I101-IR3-C1 (a), the limit of the reading check goes into the rule and no mechanism is added"
    quote: "IR3-C1 選 a"
  - type: chat
    locator: "Claude Code session 2026-11-05 (Issue #101 session), user answer to the card of `.dev/issue-101/cards-8.md` (SHA-256 b0b75928…c8c3): card I101-NC1-C1 (a), after the fix and a narrow confirmation, the NIT exception is used once early for U1, with its narrow confirmation kept"
    quote: "NC1-C1 選 a"
non_goals:
  - The review roles, floors and efforts do not change, and adversarial review stays as it is (Issue #101 body, Scope, Out).
  - No new script and no configuration (card I101-C2 (a); Issue #101 body, Where the setting lives, first choice).
  - Issue #79 slices C3 and D, and open follow-ups.
depends_on: []
refines: [REQ-012, REQ-013, REQ-027]
conflicts_with: []
superseded_by: []
superseded_reason: null
---

## Need

Issue #96 PR-3 (PR #100) showed defects in the review loop (source: GitHub
Issue #101 body, Problem). This requirement covers two of them.

1. **Completeness checks (defect 1).** Records that must change together
   were missed; for example, REQ-009 changed and `docs/requirements/log.md`
   got no row (source: GitHub Issue #101 body, Problem, item 1). A plan of
   a `standard` or `strict` slice lists fixed search strings, and each file
   with hits gets a row with a disposition, checked one to one by a
   command on the index before a commit. Co-change rules: each write node
   and each fix round that changes a requirement file adds its own
   `log.md` row, which the reviewer checks by reading
   the node's diff or the fix diff; a recorded user decision is quoted in every record that lists
   the decisions of the change, checked by reading. The commands are rule
   text, with no script (card I101-C2 (a)); only the commands of the
   search list and co-change rule 1 remain (card I101-R2-C1 (a)). They run
   before a commit and in the Merge Review, and their values are checked
   search strings, a checked folder and, in the Merge Review, checked
   commit IDs; no rule requires a commit for each node (card I101-IR2-C1
   (a)). Limit (card I101-IR3-C1 (a); the main agent narrowed the wording to one
   commit): a second change of one requirement file in one commit without
   its own row is found only by reading, and only on a target that shows
   that change alone; on a cumulative diff the report says so, and this item
   does not count as passed. Design
   d6 replaces design d5: the per-node commit and the unstaged order are
   gone, card I101-IR1-C1 (a) is replaced by card I101-IR2-C1 (a), and the
   main agent's correction of that card was never a decision (source:
   `.dev/issue-101/plan.md`, Decisions).
2. **Sources of new facts (defect 2).** Every new fact sentence in
   records, cards and briefs gives its test or source, or says that it is
   an inference; briefs pass facts with their source (source: GitHub Issue
   #101 body, Proposed direction, Evidence rule).

## Acceptance

- `skills/dev-plan/SKILL.md` step 6 ends with a completeness-checks bullet
  group, with no step renumbering: the value rule; when the commands run
  (before a commit, after the content of that commit is staged and before
  the R-REV-9 commit scan; the rule requires no commit, and when the user
  authorized none, the main agent runs no command, and the co-change rules and their
  reading check still apply); the search list
  with its `git grep --cached` form, its exit codes, its row format (path,
  count, disposition, reason; no line numbers and no hit text; no rows for
  the objective's own record folder) and its limit; the co-change rules,
  rule 1 (each write node and each fix round adds its own row, and the
  reviewer checks this by reading) with its two `git diff --cached` forms,
  its check of the `+|` and `-|` lines of `log.md` and its limit, rule 2 by
  reading; the results: a
  check that did not run stops the dependent work (R-AUTH-5), and a wrong
  or missing row, quote or log line is at least a `NIT`, a `SHOULD-FIX`
  when it leaves a place that the change made false without a disposition
  (R-REV-3).
- `skills/dev-deliver/SKILL.md` step 7: for a commit at `standard` and
  `strict`, the main agent runs the search list and co-change rule 1 as
  `dev-plan` step 6 says, and records the outputs (counts and exit codes)
  in the plan.
- `skills/dev-review/SKILL.md` step 2: the brief of an implementation
  review and of a fix round review gives the search list and the co-change
  rules with their commands in the forms of `dev-plan` step 6, and only the
  values come from the plan (not an R-REV-9 scan); the reviewer checks each
  value by the value rule; when its target is staged, it runs the commands on the index and
  compares them with the outputs in the plan, if the plan has any; it
  always checks co-change rule 1 by reading the diff that it reviews (for
  a fix round, the fix diff), and on a cumulative diff its report says that it cannot tell the rounds apart and that this
  item does not count as passed; the Merge Review lists the
  commits with `git rev-list`, runs co-change rule 1 on each commit with
  `'<commit ID>^1' '<commit ID>'` in place of `--cached`, reads a merge
  commit by hand and says so, and runs the search list on the head.
- `skills/dev-review/references/review-report.md` has a "Completeness
  checks" header line; `skills/dev-deliver/references/task-brief.md` has a
  "Completeness checks" field.
- The value rule is word for word in `skills/dev-plan/SKILL.md`, the
  "Completeness checks" field of `task-brief.md`, `agents/dev-reviewer.md`,
  `agents/dev-security-reviewer.md` and `agents/dev-implementer.md`,
  because subagents do not load `dev-core` (source:
  `docs/requirements/REQ-024-agent-write-and-delete.md:67`) and, by
  inference from the `tools:` lines of the agent files, which have no Skill
  tool, not `dev-plan` either; the Bash lists of both reviewer agent files
  add `git rev-parse --show-prefix` and the `git rev-list`, `git grep` and
  `git diff` forms of the brief.
- `tests/test_review_loop_rules.py` pins the word-for-word copies of the
  value rule, the command forms and the limit of co-change rule 1 of the
  `dev-plan` bullet group, the Merge Review forms of `dev-review` step 2
  and the Bash list wording of both reviewer agent files, and it checks
  that the replaced d5 text is gone.
- Recorded example (Issue #101 body, Done when): PR #100 P3-T3 changed
  REQ-009 without a `log.md` row of its own, and a reviewer found it by
  reading (finding IR2-P3-D-01; source: `.dev/issue-96-pr3/plan.md:303-305`);
  on the whole PR range the command form passes (source:
  `.dev/issue-101/reviews/design-round-2.md`, "Recorded test", a read-only
  test of the deep review with the tree form, which the main agent did not
  re-run). So this case stays a reading check, and only on a target that
  shows the fix alone: PR #100's round 2 was scoped to the fix diff (source:
  `.dev/issue-96-pr3/plan.md:296`), and on a cumulative diff reading cannot
  tell the rounds apart (source: `.dev/issue-101/reviews/impl-u1-round-3.md`,
  a read-only test of the deep review, which the main agent did not re-run;
  card I101-IR3-C1 (a)). The check outputs of `.dev/issue-101/plan.md`.
- E2 (R-EVD-3) is added by U2.

## Notes

- Decisions: cards I101-C1 to I101-C5 (`cards-2.md`), I101-R2-C1 and
  I101-R2-C2 (`cards-3.md`), I101-R3-C1 (`cards-4.md`), I101-IR1-C1 and
  I101-IR1-C2 (`cards-5.md`), I101-IR2-C1 and I101-IR2-C2 (`cards-6.md`) and
  I101-IR3-C1 (`cards-7.md`) and I101-NC1-C1 (`cards-8.md`), all option (a); the SHA-256 of each card file is in
  `.dev/issue-101/plan.md`, Decisions. Card I101-IR2-C1 (a) replaces card
  I101-IR1-C1 (a). The answer to `cards-4.md` was relayed, and the user
  confirmed it in the Issue #101 session (card I101-IR1-C2 (a)).
- The R-VER-2 exception for NIT repeats (Issue #101 defect 3) goes into
  [[REQ-012-review-convergence]] in U3, not into this requirement.
- Plan: `.dev/issue-101/plan.md`, design d7, slice S1 (unit U1).
