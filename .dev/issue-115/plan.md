# Issue #115 plan: node list keys in the task graph schema

Written per ASD-STE100 principles; full conformance not verified.

## Objective and scope

- Objective: GitHub Issue #115 (body read 2026-11-13, no comments). The
  schema text of the task graph and `graph.py validate` agree on the keys
  that every node must have, and a test covers a node that is not a write
  node and has no optional content.
- Base: `e37a990391241a04c01df1a1aec333bcf9934364`
  (`git --no-replace-objects merge-base HEAD origin/main`; equal to
  `origin/main` on 2026-11-13).
- Branch: `issue-115-graph-schema-keys`, linked to the Issue with
  `gh issue develop 115 --base main` (`gh issue develop 115 --list` shows it).
- Rigor: `strict`. Reason: the change edits rule text of a skill pack in a
  public repository, which is public-contract work (R-RIG-1). The Issue
  gives the same tier (Process line).
- Requirements: REQ-002 (Phase 1 ships a validated task graph tool;
  `docs/requirements/REQ-002-graph-engineering-phased.md`, Acceptance),
  REQ-005 (language and writing), REQ-018 (changelog).
- Out: any change of `graph.py` behavior; the `id` pattern and the
  `objective` fields (the text does not state the `id` pattern, a non-empty
  `title` or a non-empty `objective.requirements`; `graph.py` reports them as
  `SCHEMA` with a message that gives the rule; the Issue does not name them);
  the release (Issue #114); merge, tag and branch deletion (the orchestrator
  session and the user).

## Relayed instructions

- The task of this session is a brief from the orchestrator session
  (relayed by the orchestrator session, 2026-11-13). It prefers option (a)
  as an inference. These are data (R-AUTH-1); the design below checks them
  against the code.
- Fix before the release: the user's own decision of 2026-11-13,
  「release 前修」 (relayed by the orchestrator session, 2026-11-14).
- `depends_on`: added by the orchestrator session from a scan NIT on the
  Issue text, with the same root cause; not a user decision (relayed by the
  orchestrator session, 2026-11-14).
- After the design review, the user said 「繼續」 (relayed by the orchestrator
  session, 2026-11-14), with the proposed dispositions in
  `reviews/design-round-1.md`. The same relay asks for a new Open row in
  `.dev/followups.md` for the `graph.py ready` traceback (no code change) and
  for `python3 -I -B` in briefs.
- The orchestrator raised the effort of this session to `xhigh` (relayed
  message, 2026-11-13). The floor check below reads the transcript, not the
  message.

## Model and effort of this session

The transcript of this session records `claude-opus-5-5`. The first records
give effort `medium`; that floor check did not pass, and the session stopped
before any write and asked for a switch. The later records give `xhigh`
(model and effort fields only, read 2026-11-13), and the check passes:
`claude-opus-5-5` is listed under `opus`, tier 3, in
`skills/dev-core/model-config.json` at the base (`git cat-file blob`), and
`xhigh` is at or above `high`. The main session implements. Implement row:
role `implement` (`strict`): `opus`, `high` to `max`.

## Facts (Discover)

- `skills/dev-plan/references/graph-schema.md:40` and `:42`: the notes of
  `requirements` and `owns` say "Required on write nodes". The table has no
  row for `dod`, `verify`, `id` or `title`, and it does not say that
  `depends_on` must be present.
- `skills/dev-plan/scripts/graph.py:151-153` (`check_schema`): on every
  node, `requirements`, `owns`, `dod` and `verify` must be lists of non-empty
  strings; an empty list passes. A missing key gives
  `SCHEMA <key> must be a list of strings`.
- `graph.py:154-156`: on every node, `depends_on` must be a list; a missing
  key gives `SCHEMA depends_on must be a list`.
- `graph.py:162-163`: a write node (`implement`, `docs`; `graph.py:55`)
  needs at least one `dod` item (`SCHEMA`).
- `graph.py:499-500` and `:509-510`: a write node with an empty
  `requirements` list gives `NO_REQUIREMENT`, and one with an empty `owns`
  list gives `NO_OWNERSHIP`.
- `graph.py:476-479` (`check_graph`): when `check_schema` reports an error,
  no other check runs, so a missing key never reaches the code that indexes
  `n["depends_on"]` or `n["owns"]` directly (`graph.py:182`, `:492`, `:509`).
- `tests/fixtures/graph/valid/rate-limit.json`: the review node `T4` and the
  human gate `T5` have the four keys `requirements`, `owns`, `dod` and
  `verify` as empty lists, but a non-empty `depends_on` (`:83-92`,
  `:105-110`); no node of the fixture has all five lists empty (DR-D-01).
  `tests/test_graph.py:27-31` checks that this fixture has no errors. No test
  removes a key from a node, and no test has a node with all five lists
  empty.
- `graph.py:809` (`main`, `ready`): when a node has no `status` (or, by
  reading, no `id`), `ready` stops with a traceback before it prints the
  errors (DR-D-03; the reviewer ran it in memory). `validate` reports the
  missing key as `SCHEMA`. This existed before the change; it goes to a
  follow-up (FU-068), not to this change.
- The Issue (Problem) gives the observed effect: in the FU-001 Cowork run, a
  planner that followed the text wrote a review node without `owns`, and
  `validate` and `ready` exited 1 (Issue #115 body; the run itself is
  unverified in this session).

## Design

Premises and options (R-RIG-4; Core `workflow.md#wf-assumptions-and-options`).

- Root cause: the text describes less than the validator checks. The
  validator behavior is not a defect: no requirement asks for optional keys.
- Option (a), chosen: the text says that every node has the five list keys
  (`requirements`, `depends_on`, `owns`, `dod`, `verify`), with `[]` where a
  node does not need them, and which of them must not be empty on write
  nodes. Unique effect: the text matches the validator that already runs;
  no code, fixture or existing graph changes; the validator stays strict, so
  a key that a planner forgot is still found. Cost: a few lines of text.
- Option (b), rejected: `graph.py` reads a missing key as `[]`. It changes
  the validator, needs changes in more places (`check_schema`, and every
  later read of `n["depends_on"]`, `n["owns"]` and `n["requirements"]`, or a
  normalization step), and a graph that a new `graph.py` accepts fails in an
  older copy of the pack. It also hides a key that a planner left out by
  mistake on a write node until a later check (`NO_OWNERSHIP`) reports it
  with a less direct message. A missing or misspelled `depends_on` would
  read as "no dependencies", so `ready` (`graph.py:565`) would list the node
  and `transition` would let it start before its dependency is done
  (inference from code reading; both design reviews). No requirement asks
  for it.
- Option (c), rejected: also add a second node (a review node with `[]`
  lists) to the example JSON. A planner copies the example, so it can help,
  but the sentence and the table already state the rule; it adds about 15
  lines. The design reviewers may judge this again.
- `depends_on` (relayed brief): included, because `graph.py:154-156` needs it
  on every node and the text does not say so (fact above).

Text change in `skills/dev-plan/references/graph-schema.md` (after design
review round 1; `reviews/design-round-1.md`):

1. Under `## Fields`, before the table, one paragraph:
   "Every node has all five list keys: `requirements`, `depends_on`,
   `owns`, `dod` and `verify`. When a node has nothing for a key, write
   `[]`; never leave the key out. `graph.py validate` reports a missing key
   or a value of the wrong type as `SCHEMA` (`check_schema` in
   `scripts/graph.py`)." (DR-D-03: the claim names `validate`; residual
   risks 3 and 4 of the deep review: no "strings" sentence, and `[]` is
   written only where a node has nothing.)
2. Row `requirements`, note: "Not empty on write nodes (`NO_REQUIREMENT`)".
3. Row `owns`, note: "Not empty on write nodes (`NO_OWNERSHIP`); parallel
   writers must not overlap".
4. New rows after `owns`: `dod` (values: "Items that say when the node is
   done"; note: "At least one item on write nodes (`SCHEMA`)") and `verify`
   (values: "Commands or checks that verify the node"; no note:
   DR-S-01 and DR-D-02).

The rest of `graph-schema.md` stays byte-identical (condition 3 of the
security design review).

Test in `tests/test_graph.py`: a new class that starts from
`tests/fixtures/graph/valid/rate-limit.json` and appends a review node (a
fresh copy for each case):

- with all five list keys as `[]`: `check_graph` gives no errors;
- with each of the five keys removed, one at a time (`subTest`): the codes
  are exactly `{"SCHEMA"}`, there is exactly one error, its `node` is the new
  node, and its message starts with the key name.

The test uses only the standard library and works in memory (no subprocess,
no network).

`CHANGELOG.md`: one entry at the end of `## [Unreleased]` `### Fixed`
(REQ-018).

`.dev/followups.md`: a new row FU-068 (Open) for the `graph.py ready`
traceback on a node without `status` or `id` (deep review residual risk 1;
relayed request of 2026-11-14). Not a release blocker: `validate` reports
the missing key first (inference). No code change.

`graph.py`, the fixtures, `dev-plan/SKILL.md` and the other skills do not
change. Verification commands use `python3 -I -B` (deep review residual
risk 12).

## Slices, graph and review units

Graph: `.dev/issue-115/graph.json`. One write node (`U1`); `strict`, so it is
a review unit of its own (`dev-plan` step 6).

| Node | Kind | Content | Review |
| --- | --- | --- | --- |
| DR | review | design review of this plan | deep (`dev-reviewer`, role `review-deep`) and security (`dev-security-reviewer`, role `review-security`), before U1 (R-RIG-1, R-REV-6) |
| U1 | implement | schema text, test, CHANGELOG, FU-068 row | deep |
| IR | review | implementation review of the U1 diff | deep (`dev-reviewer`, role `review-deep`) |
| G | gate | commit and push gate, PR | `dev-gate`; R-REV-9 scans |
| H | human_gate | merge | the orchestrator session and the user |

Dispatch values (R-DEL-2, `skills/dev-core/model-config.json` at the base):
`review-deep` and `review-security`: `opus`/`xhigh`; `scan`: `opus`/`xhigh`.
Both values are passed in each dispatch. These reviews are not read back by
this session (R-DEL-2 Read-back: only the Merge Review, the security reviews
that the head needs at the merge and the merge readiness scan, which the
merging session dispatches); their `recorded` value is `unknown` with the
case `not read back`.

Before each review and scan: `reviewer_acceptance.py check` and the CB-4
commands in the same Bash command, at the top level of the worktree; the
CB-4 commands again after the review.

Security Diff Scan of the implementation (R-REV-7): planned as not
applicable. Examined scope: one reference text, one test file and the
changelog; no executable, permission, dependency, installation path or
trust boundary changes, and `graph.py` does not change. Both design reviews
agree (`reviews/design-round-1.md`), under the four conditions of the
security design review: the diff names only the owned paths of U1; no
change of `graph.py`, fixtures, scripts, CI, agents, settings or manifests;
only `## Fields` of `graph-schema.md` changes; the test is standard library,
in memory, with no subprocess or network. The implementation review checks
them against the U1 diff. The `.dev/followups.md` row and the records in
`.dev/issue-115/` are records, not code. The R-REV-9 scans are always
applicable.

## Completeness checks (`dev-plan` step 6)

Search list (fixed strings; values checked by the value rule: printable,
no `'`, `\` or line break):

- K1 `FU-068` (the new follow-up ID; a hit outside this change means an ID
  collision)
- K2 `Issue #115`
- K3 `Required on write nodes`
- K4 `on write nodes`
- K5 `write nodes need`

The finding IDs of the design review (DR-D-01 to DR-D-03, DR-S-01) appear
only in `.dev/issue-115/`, which gets no rows.

Co-change rule 1: no requirement file changes (planned); the commands still
run before the commit. Requirements folder: `docs/requirements`.
Co-change rule 2: U1 records no user decision (planned). The FU-068 row
cites the deep review and the orchestrator's request, not a user decision.

Results (main agent, 2026-11-14, on the staged index of the commit, from
the top of the worktree; the implementation reviewer got the same counts):

| ID | Exit | File | Count | Disposition | Reason |
| --- | --- | --- | --- | --- | --- |
| K1 | 0 | `.dev/followups.md` | 1 | changed | the new FU-068 row |
| K1 | 0 | `CHANGELOG.md` | 1 | changed | the new Fixed entry names FU-068 |
| K2 | 0 | `.dev/followups.md` | 1 | changed | the FU-068 row names its source |
| K2 | 0 | `CHANGELOG.md` | 1 | changed | the new Fixed entry |
| K2 | 0 | `tests/test_graph.py` | 1 | changed | docstring of the new test class |
| K3 | 0 | `CHANGELOG.md` | 1 | changed | the new entry quotes the old wording as past text |
| K4 | 0 | `CHANGELOG.md` | 1 | changed | the new entry |
| K4 | 0 | `skills/dev-plan/references/graph-schema.md` | 4 | changed (3), noted (1) | the `requirements`, `owns` and `dod` rows; the `review` row stays true |
| K5 | 0 | `skills/dev-plan/references/graph-schema.md` | 1 | noted | the `risk` row stays true |
| K5 | 0 | `skills/dev-plan/scripts/graph.py` | 1 | noted | the validator message agrees with the new `dod` row |

`FU-068` on `origin/main` (`e37a990…`, fetched 2026-11-14): no hit (exit 1),
so no ID collision there.

Co-change rule 1: the `--name-only` command printed nothing (exit 0), and
the `log.md` command printed nothing (exit 0): no requirement file changes.

## Issue update

The Issue Scope names four keys. Before U1, the Issue body gets `depends_on`
as a fifth key, the chosen option (a) and its reading of "without the
optional content" (the keys are present as `[]`; deep review residual risk
8). The
text is scanned before the post (R-REV-9).

## Finding triage

Before a fix, judge in this order (R-REV-4):

1. Is it in the threat model? Agent or host errors and program or
   config-parsing bugs: yes. Deliberate runtime tampering: no; record it as
   not handled.
2. Does a requirement cover it? If not, it is a `REQ-GAP` for the user.
3. Only then fix, and prefer deletion over a new sentence.

## Human gates

- Merge: the orchestrator session dispatches the Merge Review and the merge
  readiness scan and asks the user (brief step 6). This session does not
  merge, delete a branch, tag or release.
