# Issue #106 design review, round 1

Written per ASD-STE100 principles; full conformance not verified.

Target: `.dev/issue-106/plan.md`, `cards-1.md`, `graph.json` (uncommitted) at
base `23ed6dd352dba41e76d878655239c22465092f49`.

## Dispatches

| Review | Agent | Requested | Recorded |
| --- | --- | --- | --- |
| DR-sec (security design review) | `dev-security-reviewer` | opus/xhigh | `unknown`, case `not read back` (R-DEL-2: only the three merge-time dispatches are read back) |
| DR-deep (deep design review) | `dev-reviewer` | opus/xhigh | `unknown`, case `not read back` |

CB-4: the review target is untracked (`?? .dev/issue-106/`), so the CB-4 hash
does not see edits inside it (CB-4 list). The reviewer reported `git rev-parse
HEAD` = base and the same `git status --short` at start and end (receipt
DR-sec, Verification). The main agent did not edit the target files while the
reviews ran.

## DR-sec findings and triage (R-REV-4: threat model, requirement, fix)

| ID | Severity | Triage | Disposition plan |
| --- | --- | --- | --- |
| DR-S-01 | MUST-FIX | in the threat model (an agent applies D-032 to a resource that it does not cover); Core `review-required-read-only` :21, :31 | Fix: D-032 covers only the content under review in the repository of the change (worktree, index, refs, objects) and the scan input files; when a task, brief or project policy names another protected resource or requires technical isolation, D-032 does not apply. Card C1 gets this fact; an owner-repo option is added |
| DR-S-02 | SHOULD-FIX | agent error (reads the new CB-5 sentence as covering isolation tasks); Core :11, :35 | Fix: keep the CB-5 sentence, add after it; D-032 lists what it does not exempt (Core :35) |
| DR-S-03 | SHOULD-FIX | agent or config error (a `docs/` file of another project, or a branch under review, decides the qualification); CB-6, CB-7 | Fix: the check command and the literal go into pack rule text under `skills/dev-core/`; it prints only PASS or STOP; D-032 in `docs/` is the record, not the check |
| DR-S-04 | SHOULD-FIX | requirement: Core :29 (what the detection misses) | Fix: card C1 and D-032 list items (1) to (5). Extra detection is a new mechanism: not added (no requirement) |
| DR-S-05 | SHOULD-FIX | agent error (edits D-032 to make the test pass) | Fix: delete the claim; a rule says a change of the tools, the pins or the D-032 tool strings needs a new acceptance in the user's words; the agent never edits D-032 to pass a test. The test stays as a co-change check |
| DR-S-06 | NIT | R-EVD-3 (fact without a source) | Fix: write channel = Bash and any tool the host gives beyond the agent file (runtime enforcement not tested, DL-004); delete the unsourced reason clause |
| DR-S-07 | NIT | conflict with Core :33 (discard vs keep evidence) | Fix by replacement, not addition; "each review and scan" |
| DR-S-08 | SHOULD-FIX | Core :93; pack: own-commit signatures go to the user | Fix in PR-3 design: read `commit.gpgsign`, `gpg.format`, and the `-S` flag; a signature that Git will make is a finding for the user; `user.signingkey` recorded by class only |
| DR-S-09 | SHOULD-FIX | Core :91, :97 | Fix in PR-3 design: the expected `owner/repo` comes only from the user's instruction or the task; text check before use; fixed URL forms; PASS or STOP |
| DR-S-10 | SHOULD-FIX | Issue #106 scope 3 | Fix in PR-3 design: `--repo`, `--body-file` or `--notes-file` with the scanned file, literal `--title`, no fill, editor, web or template options, `--head` for `gh pr create` |
| DR-S-11 | SHOULD-FIX | Core :99 (unknown is not clean) | Fix in PR-3 design: a text scan that cannot read a whole attachment or asset is `NOT_RUN` and stops for the user; the tag name and target of a Release are scanned; no `--generate-notes` |
| DR-S-12 | SHOULD-FIX | Issue #106 scope 8 | Fix in PR-3 design: one clause naming each scan and R-REV-1 too; both REQ-011 notes reworded (session binding and R-REV-1 for each scan, read-back for the merge readiness scan only) |
| DR-S-13 | NIT | "Done when" item 3 | Fix in PR-3 design: rows become "substitute or accepted residual risk" with the source card; hostnames and addresses; awk pattern `-----BEGIN ` |

Residual risk listed by DR-sec, not a finding: the older phrases in R-REV-1
("an agent with write tools never counts"), CB-4 ("read-only agent") and
`skills/dev-review/SKILL.md:108-118` fail closed under the new R-REV-1 clause;
candidates for the same change.

Orchestrator note (its own view, not a user decision; message to this
session, 2026-11-09): DR-S-03 should be one rule sentence if that is enough,
with no new script; DR-S-08 to DR-S-13 take only what Core
`review-publication-data` asks for. Single `gh` flags and fixed URL forms
that no recorded agent error reaches become "keep as is" or an option on a
user card. Re-triage of these rows: after DR-deep, before the plan changes.

Re-triage of DR-S-08 to DR-S-13 by that note: each row keeps only what Core
`review-publication-data` names (destination, actual payload, attached data,
signer information, unknown is not clean). Kept as is: `--head` for
`gh pr create`, fixed URL forms beyond https, a listing of `gh` fill, editor,
web and template options (no recorded agent error reaches them). DR-S-03:
one rule sentence with the command, no script.

## DR-deep findings and triage

The reviewer saw one plan edit during its review (the branch-plan paragraph,
277 → 284 lines; receipt DR-deep, Verification); its line numbers are at the
284-line version. The edit did not touch the reviewed design.

| ID | Severity | Triage | Disposition plan |
| --- | --- | --- | --- |
| DR-D-01 | MUST-FIX | authorization (Core `review-and-security.md:47`, `:51`) | Fix in PR-2 by rewriting R-REV-3 and R-REV-4: a blocker is fixed only inside the authorized scope; outside it, a decision card |
| DR-D-02 | MUST-FIX | agent error (a branch that changes reviewer tools qualifies its own reviews); Core :29, :31 | Fix: D-032 lists protected resources; R-REV-1: a change that edits the agent files, the pins or D-032 does not use D-032; only a new quoted user decision changes D-032; Not covered adds CB-6 Limit and host permission settings |
| DR-D-03 | MUST-FIX | possible relaxation of Core (card C1 (a) any repo) | Fix: card C1 cites Core :31, recommends this repository only, adds the owner-repo option and "not accept", drops the version option and its false REQ-009 claim |
| DR-D-04 | MUST-FIX | R-REV-7 (vendor and lock, authorization text) | Fix: a security review for PR-2 |
| DR-D-05 | SHOULD-FIX | Core :91 (actual destination) | Fix: PR-3 row; `--repo`, as `dev-retro` already does |
| DR-D-06 | SHOULD-FIX | Core :29, :31 | Fix: bound rules narrowed to the qualification rules; R-REV-9 listed as "applies to" |
| DR-D-07 | SHOULD-FIX | program error (failed `git diff` = clean hash); Core :99 | Fix: CB-4 uses the `dev-retro` read-back commands; a failed command is `NOT_RUN` and the review does not count |
| DR-D-08 | SHOULD-FIX | = DR-S-02 | Fix as DR-S-02 |
| DR-D-09 | SHOULD-FIX | REQ-022 (agent copies) | Fix: P3 owns `agents/dev-security-reviewer.md` and `skills/dev-implement/SKILL.md` |
| DR-D-10 | SHOULD-FIX | window between the bump and PR-3 | Asked the orchestrator: order PR-1 → PR-3 → PR-2 |
| DR-D-11 | SHOULD-FIX | "Done when" item 1 (equals v0.5.0) | Fix: a read-only `git ls-remote` check in the lock |
| DR-D-12 | SHOULD-FIX | Core `workflow.md:36` | Fix: `dev-implement` row of the stage map and the task brief |
| DR-D-13 | SHOULD-FIX | honest record of an inference | Fix: DL-049 note and the final report |
| DR-D-14 | NIT | = DR-S-06 | Fix as DR-S-06 |
| DR-D-15 | NIT | = DR-S-07 | Fix as DR-S-07 |
| DR-D-16 | NIT | card facts | Fix: card C2 rewritten |
| DR-D-17 | NIT | delta reasons | Fix: DL-003 and DL-011 reasons |

DR-deep residual items: 1 (R-DEL-2 "or mixed") fixed in the plan; 2 wording
fixed; 3 the non-contract files get one sentence; 4 R-WRT-2 names the two
Core points; 5 = DR-S-08; 6, 7 = DR-S-03; 8 the test reads the English part;
9 = DR-S-09; 10 risk `high` in both; 11 REQ-018 acceptance names the current
pin; 12 `Rejected` (deliberate tampering only); 13 no action.

Round 2: the revised plan and cards go to a narrow confirmation of the
affected parts after the user's answers, before PR-1 implementation.

## Round 2 (narrow confirmation, DR2)

Dispatch: `dev-reviewer`, requested opus/high (role `review-routine`),
recorded `unknown`, case `not read back`. Result: every round-1 finding
applied, three partly (DR-S-01 card text, DR-S-04 card list, DR-D-16); new
findings below.

| ID | Severity | Triage | Disposition |
| --- | --- | --- | --- |
| DR2-01 | SHOULD-FIX | agent-error path: the DR-D-02 exclusion would stop every PR-3 review (PR-3 edits the body of `agents/dev-security-reviewer.md`) | Fixed in the plan by deletion: the exclusion covers only the `tools` and `disallowedTools` lines, the pins and D-032 (option 2 of the reviewer) |
| DR2-02 | SHOULD-FIX | REQ-013 (D-014 items 2, 3): the STE principle sentence is a user requirement | Fixed in the plan: the whole STE bullet stays; the loosening narrows (no new user answer: the card said the STE statement stays) |
| DR2-03 | NIT | false fact in card C1 (d) | Fixed: "PR-1 合併之後" |

Residual items: 1 (run the check at the top level of the worktree under
review) and 2 (a moved cite is no rule change) fixed in the plan; 3 PR-2
item 9 points at the (b) record; 4 delta type `tighten`, as DL-049; 6 wording
fixed; 7 PR-2 does not edit the `tools` lines (owned paths kept, noted); 8
REQ-009 and REQ-023 added to the graph. 5: recorded in D-032 "Not covered".
DR-S-01 and DR-S-04 partial card text: the card was answered; D-032 carries
the full lists.
