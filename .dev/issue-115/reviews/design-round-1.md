# Design review round 1, Issue #115

- Target: `.dev/issue-115/plan.md`, SHA-256 `1243420d9f4a0d976b76c39a6e450862f497bdf2bb647f3ebfa9e2e77885102e`, and `.dev/issue-115/graph.json`, SHA-256 `c40a04560ddb19e48d96ac9d1481bb70ef7d1e73795dc8de18569ed13d592e8c`; both uncommitted, at HEAD = base `e37a990391241a04c01df1a1aec333bcf9934364`.
- Reviewer check (R-REV-1): `reviewer_acceptance.py check` printed `PASS` (exit 0), in the same command as the CB-4 commands before the reviews.
- Tree check (CB-4): HEAD, the status hash and the diff hash were the same before and after both reviews (exit 0 each time), and both target hashes were the same after the reviews.
- Deep: `dev-reviewer`, role `review-deep`, requested opus/xhigh; recorded: `unknown` (not read back); effective: `unknown`.
- Security: `dev-security-reviewer`, role `review-security`, requested opus/xhigh; recorded: `unknown` (not read back); effective: `unknown`.
- Dispositions: the user's answer 「繼續」 to the proposed dispositions (relayed by the orchestrator session, 2026-11-14).
- Writing: written per ASD-STE100 principles; full conformance not verified.

## Findings and dispositions

The IDs are the reviewers' IDs (DR-D deep, DR-S security).

| ID | Severity | Finding | Class | Disposition |
| --- | --- | --- | --- | --- |
| DR-S-01, DR-D-02 | SHOULD-FIX (security), NIT (deep) | The draft note "Can be empty" on the `verify` row has no limit; it invites `verify: []` on a write node, which no check finds, and it conflicts with `dev-plan` step 6 (each slice has verification commands) | necessary fix | `Fixed` in the design: the note is deleted; the row keeps no note |
| DR-D-01 | NIT | False fact in the plan: `T4` and `T5` of `rate-limit.json` do not have all five lists empty (their `depends_on` is not empty) | necessary fix | `Fixed` in the plan (Facts) |
| DR-D-03 | NIT | "A missing key … is a `SCHEMA` error" names no command; `graph.py ready` stops with a traceback when `status` is missing (`graph.py:809`) | necessary fix | `Fixed` in the design: the claim names `graph.py validate` |

Also adopted from the deep review residual risks (wording only, no new
mechanism): no "strings" sentence (4); "write `[]`; never leave the key out"
(3); test precision (7); the Issue records how option (a) reads "without
the optional content" (8); the `depends_on` reason against option (b) (9);
`python3 -I -B` in verification commands (12). Fixes get their re-review in
the implementation review.

## Residual risk and not handled

- `graph.py ready` stops with a traceback when a node has no `status` or no
  `id` (deep review residual risk 1; existed before): follow-up FU-068, no
  code change in this work.
- No test covers the write-node DoD rule (`graph.py:162-163`), and the valid
  fixture has a docs writer with `verify: []` (`rate-limit.json:76`); both
  existed before and are outside the Issue.
- The text still does not state the `id` pattern, a non-empty `title`, the
  `objective` fields or the `node` string of each `depends_on` entry; out of
  scope (plan, Out).
- Not handled (deliberate tampering): a graph, event log or `graph.py` copy
  that someone changes on purpose.
- The reviews used the Core criteria files of the plugin cache; both
  reviewers report them equal to the vendored copies in the worktree.

## Lesson candidates

- Observation (fact, deep review): with `python3 -I`, Python ignores
  `PYTHONDONTWRITEBYTECODE`, so a brief test command without `-B` writes
  bytecode caches (git-ignored). One event; already covered by "or the
  runner's equivalent" in `agents/dev-reviewer.md`. Judgment: worth
  improving; smallest fix: briefs add `-B`. Level: L2. Abstraction
  checklist: each item not present.
