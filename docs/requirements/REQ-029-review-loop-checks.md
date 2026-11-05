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
    locator: "Claude Code session 2026-11-05 (Issue #101 session), user answer to the card of `.dev/issue-101/cards-8.md` (SHA-256 b0b75928…c8c3): card I101-NC1-C1 (a), after the fix and a narrow confirmation, when only NITs remain, the NIT exception of cards I101-C1 (a) and I101-R2-C2 (a) is used once early for U1, with all its conditions and its own narrow confirmation; condition (2) did not hold on the cumulative target of NC2, so the exception was not used and the U1 round was an ordinary stop (source: `.dev/issue-101/reviews/impl-u1-nc2.md:43-46`; card I101-NC2-C1 (a), the next source)"
    quote: "NC1-C1 選 a"
  - type: chat
    locator: "Claude Code session 2026-11-05 (Issue #101 session), user answer to the card of `.dev/issue-101/cards-9.md` (SHA-256 a20a6a3e…d37a): card I101-NC2-C1 (a), condition (2) of the exception does not hold on the cumulative target of NC2, so the exception is not used; an ordinary stop with one bounded fix of the NITs of NC2; a new finding of any severity in the next narrow confirmation stops the work"
    quote: "NC2-C1 選 a"
  - type: chat
    locator: "Claude Code session 2026-11-05 (orchestrator session, relayed to the Issue #101 session), user answer to the card of `.dev/issue-101/cards-10.md` (SHA-256 12d474ff…b538): card I101-NC3-C1 (a), finding NC3-01 is `Deferred`, U1 is committed, and T2 (unit U2) fixes it"
    quote: "NC3-C1 a"
  - type: chat
    locator: "Claude Code session 2026-11-05 (orchestrator session, relayed to the Issue #101 session), user answer to the card of `.dev/issue-101/cards-11.md` (SHA-256 aa88afc3…597a): card I101-U2S-C1 (a), R-AUTH-7 gets a class for private file content, with two cases that are not such content, and the same sentence is copied into `agents/dev-implementer.md` and `agents/dev-explorer.md`; card I101-U2R2-C1 (a) replaces this wording (next source)"
    quote: "U2S-C1 a"
  - type: chat
    locator: "Claude Code session 2026-11-05 (orchestrator session, relayed to the Issue #101 session), user answer to the cards of `.dev/issue-101/cards-12.md` (SHA-256 36fd37d5…d9da): card I101-U2R2-C1 (a), the class of R-AUTH-7 is drawn by where the content comes from and the exception sentence goes, which replaces the wording of card I101-U2S-C1 (a); card I101-U2R2-C2 (a), `agents/dev-reviewer.md` and `agents/dev-security-reviewer.md` get the class too, and this requirement gets an item for it; card I101-U2R3-C1 (a) replaces the wording of card I101-U2R2-C1 (a) (next source)"
    quote: "U2R2-C1 a，C2 a"
  - type: chat
    locator: "Claude Code session 2026-11-05 (orchestrator session, relayed to the Issue #101 session), user answer to the card of `.dev/issue-101/cards-13.md` (SHA-256 05ad099a…ab00): card I101-U2R3-C1 (a), R-AUTH-7 gets one narrow clause with no exclusion, the agent files get the same clause with the word write, and this replaces the wording of card I101-U2R2-C1 (a); other private files are not in the clause, and the R-REV-9 scan looks for them"
    quote: "U2R3-C1 a"
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
   #101 body, Proposed direction, Evidence rule). Unverified statements were
   copied forward as facts: a condition in one review summary went into a
   decision card, a fix brief and the records, and a later review disproved
   it by testing (source: GitHub Issue #101 body, Problem, item 2). The rule
   adds the mark "unverified", which R-VER-5 uses; it masks every source as
   R-REV-8 says and keeps out of a record what R-AUTH-7 forbids (source:
   `.dev/issue-101/plan.md`, E2.1). A true fact
   sentence without a source or a mark is residual risk that the main agent
   fixes before the commit, and a false one is at least a `NIT` (card
   I101-C4 (a)). Before this change, the words of R-AUTH-7 and R-REV-8 did
   not cover the content of private files other than identifiers, and the
   commit scan of R-REV-9 did (source: `skills/dev-core/SKILL.md:100`, `:138`
   and `:156` at commit `2c68faedf14a5f7692f3f296a9b7f88322d78ab6`; finding
   U2-S-02 of `.dev/issue-101/reviews/impl-u2-round-1.md`). So R-AUTH-7 got
   a class for that content (card I101-U2S-C1 (a), 「U2S-C1 a」, relayed by
   the orchestrator session, 2026-11-05). Card I101-U2R2-C1 (a) (「U2R2-C1 a，C2
   a」, relayed by the orchestrator session, 2026-11-05) replaced the wording of
   card I101-U2S-C1 (a), because the first wording drew its line by who wrote a
   text (finding U2R2-S-01 of `.dev/issue-101/reviews/impl-u2-round-2.md`). Card
   I101-U2R3-C1 (a) (「U2R3-C1 a」, relayed by the orchestrator session,
   2026-11-05) replaces the wording of card I101-U2R2-C1 (a), which drew findings
   U2R3-S-01, U2R3-S-02 and U2R3-D-01 of
   `.dev/issue-101/reviews/impl-u2-round-3.md`: R-AUTH-7 has one narrow clause
   with no exclusion, the content of native memory or of the user's private
   instruction files, in any form. Other private files are not in this clause,
   and the R-REV-9 scan looks for them (source: `.dev/issue-101/plan.md`, E2.3;
   `skills/dev-core/SKILL.md:156`). Subagents do not
   load `dev-core` (source:
   `docs/requirements/REQ-024-agent-write-and-delete.md:67`), so
   `agents/dev-implementer.md`, `agents/dev-explorer.md` and the receipt
   template of `task-brief.md` give the masking and that clause in words
   (finding U2-S-01). `agents/dev-reviewer.md` and
   `agents/dev-security-reviewer.md` already gave the masking in words (source:
   `agents/dev-reviewer.md:82-86`, `agents/dev-security-reviewer.md:61-65`) and
   not that clause, and their reports are committed (finding U2R2-S-04), so
   they get that clause in words too (card I101-U2R2-C2 (a)). Card I101-U2S-C1
   (a) said that the same sentence is copied into `agents/dev-implementer.md`
   and `agents/dev-explorer.md` (source: `.dev/issue-101/cards-11.md`); those
   files hold another sentence, the private-data sentence, and both reviewers
   of U2 round 2 found it inside the option because it is stricter (source:
   `.dev/issue-101/reviews/impl-u2-round-2.md`).

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
- `skills/dev-core/SKILL.md` has the rule R-EVD-3 after R-EVD-2, with its
  Core anchor `workflow.md#wf-evidence-lifecycle`, its row in
  `skills/dev-core/source-map.md` and the delta DL-047 (type `tighten`). The
  rule covers records, decision cards, briefs, receipts and fact sentences in
  rule and reference text; it gives the source forms and the marks
  "inference" and "unverified"; every source is masked as R-REV-8 says, and
  nothing that R-AUTH-7 forbids goes into a record; it changes no locator or quote rule of REQ-008 and no record
  of R-DEL-2; a fact taken from a review summary, a receipt, a card or the
  text of another session gives the original source that they name, after
  the writer read that source, or it is marked unverified; a relayed user
  answer is recorded as a relay, and the rule that applies decides which
  relayed answers count; a false fact sentence is a finding by R-REV-3 (at
  least a `NIT`); a true one without a source or a mark is residual risk,
  with the steps of card I101-C4 (a).
- R-DEL-1 adds "A brief gives each fact with its source (R-EVD-3).", and the
  DL-009 note says that DL-047 added this sentence to the index line.
- R-AUTH-7 of `skills/dev-core/SKILL.md`: the Never commit sentence adds one
  narrow clause with no exclusion: "or the content of native memory or of the
  user's private instruction files, in any form." (source:
  `.dev/issue-101/plan.md`, E2.3; card I101-U2R3-C1 (a), which replaces the
  wording of card I101-U2R2-C1 (a)). Limit: other private files are not in
  this clause, and the R-REV-9 scan looks for them; the words "private files"
  of R-REV-9 do not change (source: the same E2.3;
  `skills/dev-core/SKILL.md:156`). The delta DL-047 names R-AUTH-7.
- `skills/dev-review/references/decision-card.md`: the Facts bullet says that
  a quote of a review summary, a receipt or another card is not the source of
  a fact (the card gives the source that it names, or marks the statement
  unverified), and the template has an `Unverified:` line under Evidence.
- `skills/dev-deliver/references/task-brief.md` has the field "Facts given:
  each with its source (R-EVD-3)", and its receipt text asks the same for
  every fact sentence that the subagent writes. The source forms and the
  masking sentence of R-EVD-3, and after them the private-data sentence of
  `.dev/issue-101/plan.md`, E2.3 (the masking of R-REV-8 and the clause of
  R-AUTH-7 in words), are word for word in the receipt template of
  `task-brief.md`, in `agents/dev-implementer.md` and in
  `agents/dev-explorer.md`, because subagents do not load `dev-core` (source:
  `docs/requirements/REQ-024-agent-write-and-delete.md:67`).
- `agents/dev-reviewer.md` and `agents/dev-security-reviewer.md`: after the
  masking bullet, which stays as it is, one bullet holds the last
  sentence of the private-data sentence word for word (card I101-U2R2-C2 (a),
  「U2R2-C1 a，C2 a」, relayed by the orchestrator session, 2026-11-05; finding
  U2R2-D-03 of `.dev/issue-101/reviews/impl-u2-round-2.md`; card I101-U2R3-C1
  (a), 「U2R3-C1 a」, relayed by the orchestrator session, 2026-11-05).
- `skills/dev-review/references/review-report.md` says that a true fact
  sentence without a source or a mark goes to residual risk and that a false
  one is a finding.
- `skills/dev-plan/references/requirements-wiki.md` says "In a REQ file, the
  quotes are the originals and live only in `sources`", because co-change
  rule 2 also puts quotes into other records (finding DR2-14 of
  `.dev/issue-101/reviews/design-round-2.md`).
- `tests/test_review_loop_rules.py` pins that R-EVD-3 is defined once in
  `skills/dev-core/SKILL.md`, the Never commit sentence of R-AUTH-7, the word-for-word
  sentences in `task-brief.md`, `agents/dev-implementer.md` and
  `agents/dev-explorer.md`, the last sentence of the private-data
  sentence in `agents/dev-reviewer.md` and `agents/dev-security-reviewer.md`,
  that the receipt template of `task-brief.md` holds them, that the replaced
  wording of R-AUTH-7 is gone from `skills/dev-core/SKILL.md` and `agents/*.md`,
  and the `Unverified:` line of `decision-card.md`.
- Recorded example (Issue #101 body, Done when): in PR #100, the condition
  "a relative `GIT_DIR` only when no `GIT_WORK_TREE` is set" came from a
  parenthesis of a security summary, through the facts of a decision card and
  a brief, and a later review disproved it by testing (finding IR2-P3-S-01;
  source: `.dev/issue-96-pr3/plan.md:316-321`, the record of a read-only test
  of the security review; unverified: U2 did not re-run that test).

## Notes

- Decisions: cards I101-C1 to I101-C5 (`cards-2.md`), I101-R2-C1 and
  I101-R2-C2 (`cards-3.md`), I101-R3-C1 (`cards-4.md`), I101-IR1-C1 and
  I101-IR1-C2 (`cards-5.md`), I101-IR2-C1 and I101-IR2-C2 (`cards-6.md`) and
  I101-IR3-C1 (`cards-7.md`), I101-NC1-C1 (`cards-8.md`), I101-NC2-C1
  (`cards-9.md`), I101-NC3-C1 (`cards-10.md`), I101-U2S-C1 (`cards-11.md`),
  I101-U2R2-C1 and I101-U2R2-C2 (`cards-12.md`) and I101-U2R3-C1
  (`cards-13.md`), all option (a); the SHA-256 of each card file is in
  `.dev/issue-101/plan.md`, Decisions. Card I101-IR2-C1 (a) replaces card
  I101-IR1-C1 (a). Card I101-U2R2-C1 (a) replaced the wording of card
  I101-U2S-C1 (a), and card I101-U2R3-C1 (a) replaces the wording of card
  I101-U2R2-C1 (a). The answer to `cards-4.md` was relayed, and the user
  confirmed it in the Issue #101 session (card I101-IR1-C2 (a)). The answers
  to `cards-10.md`, `cards-11.md`, `cards-12.md` and `cards-13.md` were relayed by the
  orchestrator session, 2026-11-05.
- The R-VER-2 exception for NIT repeats (Issue #101 defect 3) goes into
  [[REQ-012-review-convergence]] in U3, not into this requirement.
- Plan: `.dev/issue-101/plan.md`, design d9, slices S1 and S2 (units U1 and
  U2).
