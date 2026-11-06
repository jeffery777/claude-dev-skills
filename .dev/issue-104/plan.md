# Issue #104 plan: rule slimming

Written per ASD-STE100 principles; full conformance not verified.

## Objective and scope

- Objective: GitHub Issue #104 (body read 2026-11-06, no comments). It absorbs
  Issue #102 and its comment (body and comment read 2026-11-06).
- Base: `6f7a817933c5f680a32d01ed0e6d6fe6eb3834c5` (`git merge-base HEAD origin/main`).
  Branch: `issue-104-rule-slimming`.
- Rigor: `strict`. Reason: it changes published rule text, a stop rule and the
  read-back gate (R-RIG-1). The Issue proposes the same tier.
- Requirements: REQ-009, REQ-011, REQ-012, REQ-022, REQ-029.
- Out (Issue #104): the review roles, floors and efforts; the Core update;
  Issue #79 C3 and D. Not changed: `model_effort_readback.py`,
  `model-config.json`, `push_precheck.py`.

## Model and effort of this session

The transcript of this session records `claude-opus-5-5`. Its first 28 records
give effort `medium`, and that floor check did not pass: the session stopped
before any write and told the orchestrator. From the orchestrator's relay on,
records give `high`, and the check passes (`opus` is tier 3 in
`skills/dev-core/model-config.json` at the base; the ID is listed). The main
session implements. Implement row: role `implement`.

## Decisions (source: Issue #104 body, relayed by the orchestrator session)

The user's word 「同意」 (2026-11-05), to the recommended options Q1 (a), Q2 (a),
Q3 (a) and Q4 (a). Q1 to Q3 narrow project tightenings, so only the user decides
them (`deltas.md`). This session read them in the Issue; it did not see the
user's own message. The Scope of the Issue also holds three items that are not
under that word: the R-REV-4 order, "accepted residual risk is not raised again",
and the merge-signature record. Cards I104-C1 and I104-C2 (`cards-1.md`) asked the
user to confirm in this session (DR-D-01, DR-D-06). The user's own message in this
session: 「C1 a，C2 a」 (2026-11-06). Q4 is an order, so it has no
rule; D-031 records it.

## Finding triage in this work

Before a fix, judge in this order (Issue #104; the same text goes to each brief):

1. Is it in the threat model? Agent or host errors and program or
   config-parsing bugs: yes. Deliberate runtime tampering: no; record as not
   handled.
2. Does a requirement cover it? If not, it is a `REQ-GAP` for the user. Do not
   fix it because a reviewer raised it.
3. Only then fix, and prefer deletion over a new sentence.

A wording edge that no realistic agent error reaches is residual risk. Use
"keep as is", `Rejected` and `Deferred` with a reason. R-REV-9 scans and the
commit and push checks stay as they are. Core blockers stay `MUST-FIX`.
Until this PR merges, the current rules apply to this work, with the R-VER-2
stop and the read-back of every required review and scan.

## Design

### U1, mechanical move (text only)

New files, both rule text, under `skills/dev-core/references/`:

- `readback-gate.md`: the long bullet of R-DEL-2 that starts "The main agent
  fills in the receipt's `recorded` field" (`SKILL.md:190` at the base),
  word for word, except the sentences that are not a manual of the read-back.
  These stay in `SKILL.md` as their own bullets, word for word (DR-D-02,
  DR-S-02): "A review or scan counts only in the session ..." to "... never
  counts (FU-057).", and the three sentences on who may change
  `model-config.json` and what its change needs.
- `push-scan.md`: the "Before a push" steps 1 to 9 and the "Not covered" bullet
  of R-REV-9 (`SKILL.md:142-152` and `:155` at the base), word for word.

Each file has a short heading and a first paragraph that says it is part of
the rule. Paragraph breaks may go between sentences. `SKILL.md` keeps a pointer
bullet in place of each moved part: the command, "use its result", the file
path and "read it in full". `tests/test_push_precheck.py` reads the commands
from `SKILL.md` and `push-scan.md`.

Check: a script normalizes white space and shows that (a) the moved text at the
base equals the text of the new files without their heading and first paragraph,
and (b) `SKILL.md` at the base equals `SKILL.md` at U1 except the moved parts and
the pointer bullets. No sentence review (Issue #104, Process). The security scan
and the commit gate run as usual.

### U2, decisions

R-VER-2 (Q1). The sentence that starts "When two consecutive review rounds"
becomes:

> When two consecutive review rounds still report new blockers, or the same
> mechanism needed fixes and produced new problems in two consecutive rounds,
> the main agent re-evaluates the spec, the acceptance criteria and the approach
> (R-RIG-4) and reports the result. It stops for the user, with a decision card
> (R-AUTH-6), only on a `MUST-FIX`, a requirement change or a loosening;
> otherwise the work continues.

Co-changes: "stop rule" becomes "re-evaluation" in R-DEL-2 (escalation bullet),
R-VER-5, `dev-deliver` step 5, `dev-review` step 6, `review-report.md`,
`source-map.md`, REQ-012. The wording of `graph-schema.md:73` already fits.

Read-back (Q2). Read back: the Merge Review (`dev-gate` step 3), each security
review that the head needs at the merge (R-REV-7) and the merge readiness scan.
The Issue says "the Merge Review and the scans before a merge"; that the security
review of the head is one of these scans is an inference. It is the narrower
loosening, and the merging session runs these three today (`dev-gate` step 3).
No other dispatch is read back: its `recorded` value is `unknown` with the case
`not read back`. The floor check of the main session stays. The dispatch choice
of R-DEL-2 (pass both values, floors, tables) stays.

- `readback-gate.md`: the first paragraph gives this scope; no redefinition of
  words (DR-D-02). Narrow the file sentence by sentence (DR-D-03). Delete the
  sentences that only serve other dispatches: the `work`, `none`,
  `review-routine`, `review-light` and narrow-confirmation cases of `--floor`;
  the gate for a dispatch of work under the floor and its approval sentences;
  the `light` routine review sentences. `--floor` is `review-scan`.
- `SKILL.md`, `dev-deliver`, `dev-review`, `dev-implement`, `dev-continue`,
  `dev-gate`, `task-brief.md`, `review-report.md`: delete or narrow the sentences
  that read back a commit, push or post scan, an implementation review or an
  implementer. The rule that a review or scan counts only in the session that
  dispatched it stays for every review and scan; only its "read it back" part is
  limited to the three dispatches. `cat-file commit HEAD` is another read back and
  stays.
- The script keeps its `--floor` values; no code change.

R-REV-9 text scan (Q3). The bullet "Before posting" becomes:

> Before posting a PR or MR title, body or comment, an Issue title, body or
> comment, or a review record, the main agent saves the exact text to a file and
> runs `<check>`, which prints the numbers of the lines to look at. A
> `dev-security-reviewer` then scans the exact text, those lines first, for
> private data only: the list of the "Look for" bullet below and what R-AUTH-7
> forbids. It does not judge whether a fact is precise; that is the work of the
> review. Text that exists before a push scan may be scanned with it.

`<check>` is one `LC_ALL=C awk '/.../{print NR}' <text file>` command with paths
of user folders, email addresses, and common key and token forms (`grep` cannot
print only line numbers and stops at a NUL byte: DR-S-01, DR-D-08; REQ-011
already uses `awk` for that reason). A value does not reach a record. A line is
not a finding by itself; an exit code other than 0 means the check did not run.
`agents/dev-security-reviewer.md` gets the target of a text scan, because
subagents do not load `dev-core` (DR-D-07).
The text scan keeps the agent and the role `scan`: the Issue says that roles and
efforts are out. "Lighter" is the narrower target and no read-back. Inference:
the user may have meant a lower effort too; the ready card says so.

R-REV-4 gets the order of "Finding triage" above in one sentence group, with
"This order does not lower a Core blocker (R-REV-3)". The threat-model words
apply to the gates and checks of this pack; a product has its own threat model
(DR-S-03).

R-REV-3: "A residual risk that the user has accepted is not raised again in
later PRs of the same work; when a review raises it, the main agent records it as
`Rejected` with the acceptance as the source."

R-REV-9 signature: "A signature on a merge or squash commit that the hosting
platform created (committer `GitHub <noreply@github.com>`) is recorded only: it
is no blocking finding and no question for the user. A signature on the user's
own commits before a push still goes to the user (push step 5)." The same
exception goes to `push-scan.md` steps 5 and 8, the merge readiness bullet,
`dev-implement` step 4 and `agents/dev-security-reviewer.md` (DR-D-05, DR-S-04).

Records: DL-012 note and new rows DL-048 (`compress`, the move) and DL-049
(`tighten`, narrowed by the user: Q1 to Q3 and the three Scope items, with the
reading of Core `workflow.md:56`); DL-049 supersedes the affected parts of
DL-010, DL-035, DL-042, DL-043 and DL-045; REQ-009, REQ-011, REQ-012 and REQ-026
(source, Need or Acceptance, note); `docs/requirements/log.md`; D-031 and the
notes on D-013, D-027 and D-028 (both languages); CF-001 items 2, 4 and 5 (both
languages); `source-map.md`; CHANGELOG. `model-effort-readback.md` gets one note.

Issue #102 items: U3B-D-02 is answered by the comment on Issue #102 (no text
change; the exception text is withdrawn for good, so items 1 to 6 are moot).
U3B-NC-01: add the three files to "What ships (U3b)" of D-030 (both languages).
U3B-NC-02: delete the clause from the `cards-15.md` row of
`.dev/issue-101/plan.md`. MR103-D-01: class of U3B-NC-04 becomes "worth
improving". Card I101-U3R1-C2 and findings U3R1-S-01 to S-03, D-01, D-02 are moot:
Q1 replaces the exception, so their text never ships.

Tests: `tests/test_rule_slimming.py`: the pointers exist and the files resolve;
each decision pins its sentence; the check command finds samples, prints only
numbers and passes clean text. Sample tokens are built by concatenation, so that
gitleaks has nothing to report. No word-count test (DR-D-09); DoD 1 is measured
once in the gate record.

Search list (`dev-plan` step 6), run before each commit, rows in the U2 section
below: K1 `stop rule`, K2 `stop the fix loop`, K3 `停止規則`, K4 `R-VER-2`,
K5 `does not count by R-DEL-2`, K6 `reads back`, K7 `read back`, K8 `DL-012`.

## DoD

1. `skills/dev-core/SKILL.md` is under 11,000 words (base 15,754).
2. The moved text is reachable from the rule and equals the source at U1.
3. Each decision of the Issue has a rule change and a test; Q4 has its record.
4. `scripts/validate.sh` and CI pass. The four record items of Issue #102 are done.
5. PR with `Closes #104` and `Closes #102`; gate record posted and read back;
   ready card written. No merge in this session.

## Trace

| Issue item | Unit | Test or example |
| --- | --- | --- |
| Move | U1 | move check, `test_rule_slimming.py` |
| R-REV-4 order | U2 | `test_rule_slimming.py` |
| Q1 | U2 | `test_rule_slimming.py` |
| Q2 | U2 | `test_rule_slimming.py` |
| Q3 | U2 | `test_rule_slimming.py`, command run on samples |
| Accepted residual risk | U2 | `test_rule_slimming.py` |
| Merge signature | U2 | `test_rule_slimming.py` |
| Issue #102 items | U2 | Merge Review reads them |

## Review plan

Design: `dev-reviewer` deep and `dev-security-reviewer` security, one round, on
this file (`reviews/design-round-1.md`). U1: move check. U2: deep and security
implementation review of base..head, pointers included, then the narrow
confirmation. Each at opus/xhigh with read-back, `--floor review-scan`.

## U1 record

Move check (script outside the repository, compares with the base by
`git cat-file`): `MOVE CHECK PASS moved words: 5549 core words: 10685`. The
check shows that `SKILL.md` equals the base except the moved parts, the two kept
bullets and the pointers, and that the two files hold the moved text. The
pointers are new text: the U2 review reads them.
Tests: `python3 -I -m unittest discover -s tests`: 383 tests, OK (3 skipped).
`scripts/check_pack.py` and `scripts/check_core_coverage.py`: OK.

U1 search list (command of `dev-plan` step 6 on the index, exit 0 for each; the
step numbers and the name "Not covered" do not change, so every place stays
true; `noted`, one row per string to keep the list short):

| String | Files with hits | Disposition |
| --- | --- | --- |
| `Not covered` | `CHANGELOG.md` 1, `docs/design-proposal.md` 1, REQ-011 4, REQ-026 1, `docs/requirements/log.md` 1, `skills/dev-core/SKILL.md` 1, `references/push-scan.md` 1 | `noted`: the list keeps its name under R-REV-9 |
| `R-REV-9 step` | `agents/dev-security-reviewer.md` 1, REQ-011 1, `log.md` 1, `push_precheck.py` 1, `skills/dev-implement/SKILL.md` 2, `tests/test_push_precheck.py` 2 | `noted`: the numbers are the same |
| `push step` | `CHANGELOG.md` 2, `docs/core-feedback.md` 1, `docs/design-proposal.md` 8, REQ-009 1, REQ-011 4, `SKILL.md` 1, `deltas.md` 1, `references/readback-gate.md` 1, `push_precheck.py` 1 | `noted`: the numbers are the same |

U1 changes no requirement file, so co-change rule 1 does not apply.

## U2 record

Search list (command of `dev-plan` step 6 on the index). One row per string and
group, not per file: `.dev/` of other objectives and dated records hold hundreds
of hits for K4 and K7, and rows per file would add no check (class: keep as is).
Counts are in the run of 2026-11-06 before the U2 commit.

| String | Place | Disposition |
| --- | --- | --- |
| K1 `stop rule`, K2 `stop the fix loop`, K3 `停止規則` | `.dev/` of other objectives; dated rows of `log.md`; REQ-009 source locator; REQ-020 to REQ-028 sources and notes; D-0xx entries; DL-015, DL-017, DL-035, DL-045 | `historical`: they record what ran then; D-031 and DL-049 supersede them |
| K1 to K3 | `skills/dev-core/SKILL.md`, `dev-deliver`, `dev-review`, `review-report.md`, `source-map.md`, REQ-009 Acceptance, REQ-012, REQ-026 line of the trigger, CF-001 items 2, 4, 5 | `changed` |
| K4 `R-VER-2` | `SKILL.md`, `readback-gate.md` (failure class), `graph-schema.md`, `dev-deliver`, `dev-review`, `review-report.md` | `noted`: the rule keeps its ID; the re-evaluation stays |
| K5 `does not count by R-DEL-2` | `SKILL.md` (merge readiness scan), `dev-deliver` step 7 and `dev-gate` step 2 (merge) | `noted`: all three speak of the dispatches that are read back |
| K5 | `deltas.md`, REQ-009, `log.md` | `historical`: DL-049 supersedes |
| K6 `reads back`, K7 `read back` | `SKILL.md`, `readback-gate.md`, `dev-deliver`, `dev-gate`, `dev-review`, `task-brief.md`, `review-report.md` | `changed` or `noted`: narrowed to the three dispatches |
| K6, K7 | `dev-implement` (`cat-file commit HEAD`), `dev-retro`, `platform_profile.py`, script, REQ-020, REQ-021 and REQ-026 | `noted`: another read-back |
| K6, K7 | `docs/design-proposal.md`, REQ-009, REQ-011, `deltas.md` DL-040 to DL-046, `log.md`, CHANGELOG | `historical`: D-031 and DL-049 supersede, with notes at D-027, D-028, REQ-009, REQ-011 |
| K8 `DL-012` | `deltas.md`, `source-map.md`, `core-feedback.md`, `design-proposal.md` | `noted`: DL-012 keeps R-REV-4 and has a note |

Co-change rule 1: REQ-009, REQ-011, REQ-012 and REQ-026 change, and `log.md` has
one new row for each. The records quote the user's own answer to cards I104-C1 and I104-C2 in this
session: 「C1 a，C2 a」 (2026-11-06).

Issue #102 items: U3B-NC-01 (D-030, both languages), U3B-NC-02 and MR103-D-01
(`.dev/issue-101/plan.md`) are `Fixed` in this unit; U3B-D-02 is answered by the
comment on Issue #102.
