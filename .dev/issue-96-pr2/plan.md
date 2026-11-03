# Issue #96 PR-2 plan: tier-number rules, review and scan floors, and `--floor` (`Part of #96`)

- Objective: GitHub Issue #96 (body and comments 1 to 4), PR-2 of three:
  the model rules of R-DEL-2 use the tiers of the configuration file
  `skills/dev-core/model-config.json` (card I96-C9 (a) with Fable at tier
  4); the review and scan floors are in the rule (card I96-C11 (a)); the
  read-back script checks the floor of each dispatch with a required
  `--floor`; the sentences that PR-1 declared superseded are removed
  (FU-061); the records give the `fable` loosening and the narrow
  loosening (i). PR-3 (`Closes #96`) makes the routing tables and the
  rule sentences name roles only.
- Rigor `strict`. Reason (R-RIG-1): a change to a security rule (R-DEL-2,
  the read-back gate, the floors), to pack rule text, and to an
  executable that gates commits; the R-DEL-2 floor applies to every node.
- Base: `main` `1eb28de2ca96dbd87107fbdb2974e41e5f2d5137` (`1eb28de`, the
  merge of PR #98), branch `issue-96-pr2`.
- Spec: the PR-2 design d4 of 2026-11-03 (the full design) and the PR-2
  design d5 of 2026-11-03 (the differences against d4; where they differ,
  d5 wins), with the decision cards of the PR-2 design rounds 1 to 3. The
  design files are in the session notes, which are not in the repository;
  Issue #96 comment 4 states the scope that they settle. The earlier
  drafts d1 to d3 are history only.
- Method (cards I96-P2-C1 (a) and I96-P2-C2 (a)): only the sentences of a
  closed list change (R1 to R23 below). One scripted run, which asserts
  that each base text occurs exactly once, applied R1 to R22. R23 and the
  amendments of R2 and R10 were applied as hand edits by an implementer in
  the fix round after implementation review round 1, not by the apply
  script. Every other rule sentence stays word for word. The reviewers
  compare each changed sentence with this table (see Review procedure).

## Source trace (dev-plan step 2)

Sources: the Issue #96 body and comments 1 to 4; D-029 and its residual
risks; DL-005, DL-034, DL-038 and DL-042 to DL-044; REQ-009 and REQ-026;
FU-020, FU-021, FU-049, FU-061 and FU-062; the PR #98 merge gate record
(MR98-M-02, MR98-M-03 and MR98-S-01); and these user answers (Claude Code
session, the user's words in the orchestrator session, relayed):

- 「I96-P2-C1 a，P2-C2 a，P2-C3 a」: the reviewers compare the removals
  and rewrites sentence by sentence with a helper script that lists them
  and gives no PASS or FAIL, and the commit and the merge check tree
  identity (C1); only a closed list of sentences changes (C2); PR-2
  (`Part of #96`) and PR-3 (`Closes #96`) (C3).
- 「I96-P2R1-C1 a，P2R1-C2 a（較高等級的家族只經由升級階梯或使用者要求使用）」:
  the main agent reads the configuration file at the base that it finds
  itself (C1; the comparison after the dispatch then moved to `--floor` by
  P2R2-C1 (a)); the scope (a) to (h) of the `fable` loosening, with the
  user's condition on families of a higher tier (C2).
- 「I96-P2R2-C1 a，P2R2-C2 a，P2R2-C3 a，P2R2-C4 a」: the read-back script
  checks the floor with a required `--floor` (C1); a higher tier only from
  the user's own message in the session that dispatches, and item (d) of
  card P2R1-C2 for the effort only (C2); "first `max`, then the next tier"
  only from tier 3 up (C3); the narrow loosening (i) (C4).
- 「為什麼是依值找角色？而是不是依任務找角色？如果值是依任務複雜度給定的，那依值找角色等同於依任務找角色」:
  the role of a node comes from its task type, never from equal values.
- 「I96-P2R3-C1 b」: no fourth design review round; the implementation
  review covers it (see Design review round 4).
- 「I96-IR-P2-C1 a，C2 a，C3 b，C4 a」: the stop cards of implementation review round 1
  (see Implementation review); with C3 (b) the user also approves the
  wider scope of PR-3.
- 「I96-IR2-P2-C1 a，C2 b，C3 a」: the stop cards of implementation review
  round 2 (see Implementation review); with C2 (b) the same wrong base
  literal in both reads leaves the loosening (i) and goes to FU-063.
- From PR-1, still in force: 「C4 a＋條件，C9 a＋Fable 等級 4 ，這是你之前建議的2點嗎？是的話我同意」
  (with the relayed answer 「是」; D-029 records the two points),
  「I96-C11 a」, 「I96-R2-C1 a，R2-C2 a，R2-C3 a，R2-C4 a，R2-C5 a」 and
  「C8 改為：設定檔是唯一來源，路由表只標角色名、不寫數值；I96-C12 a＋停用規則；不加技能」.

From the PR-2 design reviews of rounds 1 to 3, not from the user's words:
the other wording of the rule sentences of d4 section 2 and d5 section 1
(finding IDs in d4 section 7 and d5).

## PR-2 files

| Status | Path | Task |
| --- | --- | --- |
| M | `skills/dev-core/scripts/model_effort_readback.py` | T1 |
| M | `skills/dev-core/model-config.json` | T1 |
| M | `scripts/check_pack.py` | T1 |
| M | `tests/test_model_effort_readback.py` | T1 |
| M | `tests/test_core_checks.py` | T1 |
| M | `skills/dev-core/SKILL.md` | T2 |
| M | `skills/dev-deliver/SKILL.md` | T2 |
| M | `skills/dev-deliver/references/task-brief.md` | T2 |
| M | `skills/dev-gate/SKILL.md` | T2 |
| M | `skills/dev-review/SKILL.md` | T2 |
| M | `skills/dev-review/references/review-report.md` | T2 |
| M | `skills/dev-retro/SKILL.md` | T2 |
| M | `skills/dev-core/references/model-effort-readback.md` | T2 |
| M | `skills/dev-core/deltas.md` | T2 |
| M | `docs/design-proposal.md` | T2 |
| M | `docs/requirements/REQ-009-subagent-model-effort.md` | T2 |
| M | `docs/requirements/REQ-026-lessons-skill.md` | T2 |
| M | `docs/requirements/log.md` | T2 |
| M | `CHANGELOG.md` | T2 |
| M | `.dev/followups.md` | T2 |
| M | `.dev/issue-96-model-config/plan.md` | T2 |
| A | `.dev/issue-96-pr2/plan.md` | T2 |

## Rule sentences (d4 section 2 and d5 section 1)

The base text of each row is the text at `1eb28de`; the new text is in
the design, word for word. One scripted run makes 25 edits (R11 removes
four sentences; every other row is one edit). The fix round after
implementation review round 1 makes three more edits: the amendments of
R2 and R10 (card I96-IR-P2-C1 (a)) and R23 (card I96-IR-P2-C2 (a)).

| ID | File and place | Base text (start) | Change | Cards and findings |
| --- | --- | --- | --- | --- |
| R1 | `skills/dev-core/SKILL.md`, R-DEL-2 main text | "Use aliases (`haiku`, `sonnet`, `opus`), never pinned IDs." | replaced: family names of the configuration file; "The configuration read" | I96-C9 (a), I96-P2R1-C1 (a); S-17, D-09 |
| R2 | same | "For security, data, migration and public-contract work the floor is `opus` with effort `high`." | replaced (d5 text): the work floor, the review and scan floors, roles by task type, higher values, each floor that applies; amended by IR-P2-C1 (a): ", a trigger of an earlier round of the node included" after "at the time of its dispatch" | I96-C9 (a), I96-C11 (a), I96-C4 (a), I96-P2R1-C2 (a), I96-P2R2-C2 (a), the user's note on roles; I96-IR-P2-C1 (a), S-02 |
| R3 | R-DEL-2, main-session bullet | "For work under the floor, when that model is not `opus`, …" | replaced: a listed model ID of tier 3 or higher; `WARN` never applies | I96-C9 (a), I96-R2-C2 (a); MR98-S-01 |
| R4 | same bullet | "an explore node under the floor goes to `dev-explorer` at `opus`/`high` …" | replaced: at least at the floor | I96-C9 (a) |
| R5 | R-DEL-2, start bullet | "For a session, it uses the highest row … at least `opus`/`high` …" | replaced (d5 text): the family and the lowest effort of `orchestration` and the floor | I96-R2-C3 (a) |
| R6 | R-DEL-2, Relayed answers bullet | "A setting is at or above the reference value only when … (`haiku`, `sonnet`, `opus`; …)." | replaced: the tiers of the configuration read | I96-C9 (a) |
| R7 | same bullet | "A value outside these orders, for example `fable` (not evaluated), …" | replaced: null tier, unknown name, effort outside the order, `unknown`; a reference value outside the orders stops | I96-C9 (a); S-11 |
| R8 | R-DEL-2, escalation bullet | "raise the effort first (`low` → `medium` → `high`); …" | replaced: next tier of the file; from tier 3 up only at `max` | I96-C9 (a), I96-P2R2-C3 (a) |
| R9 | same bullet | "`fable` is not in this order until it is evaluated (D-007 rule 4)." | removed | I96-C9 (a) |
| R10 | R-DEL-2, read-back bullet, after "… and `--config-base` is then a wrong call." | (insertion) | added (d5 text): `--floor` by the mode of the dispatch, fixed before it; `floor=`; amended by IR-P2-C1 (a): ", a trigger of an earlier round of the node included" after "at the time of its dispatch" | I96-P2R2-C1 (a); d5 fixes 1, 4, 5; I96-IR-P2-C1 (a), S-02 |
| R11 | same bullet | the four `light` exception sentences ("Until the allowlist …", "The exception holds only while …", "The exception holds only for …", "From Issue #96 on, the exception …") | removed | I96-C7 (a); FU-061 (N1) |
| R12 | same bullet, dead end | "The allowlist of the script holds only the Opus ID: when `opus` names a newer model, every review and scan stops," | replaced; the rest of the sentence is unchanged | I96-R2-C1 (a); IR1-S-04, S-04, D-10, S-11 |
| R13 | same bullet, dead end | "From Issue #96 on, the allowlist is the configuration file …" | replaced: the `version` form warns; other dispatches; the mixed-record dead end | I96-R2-C1 (a); IR1-S-04 (N2), D-07, D-10 |
| R14 | `skills/dev-deliver/SKILL.md`, step 2 | "When the model is not `opus`, the effort is below `high`, …" | replaced: the check of R-DEL-2; at least the floor, the row value and any escalated setting | S-12 |
| R15 | `skills/dev-gate/SKILL.md`, blocker list | ", except a `light` routine review at `sonnet`/`medium` while R-DEL-2 lets it skip the gate; …;" | removed (the line ends with ";") | I96-C7 (a) |
| R16 | `skills/dev-review/SKILL.md`, mode section | "A `light` routine review at `sonnet`/`medium` is read back by R-DEL-2 and skips that gate …" (two sentences) | removed | I96-C7 (a) |
| R17 | `skills/dev-review/references/review-report.md`, Read-back line | " (a `light` routine review at `sonnet`/`medium`: `MODEL_NOT_ALLOWED` …) — … (card I96-C7 (a))" | removed | I96-C7 (a) |
| R18 | `skills/dev-retro/SKILL.md`, step 5 | "Do not use `fable` before its evaluation (D-007 rule 4)." | removed | I96-C9 (a) |
| R19 | `skills/dev-core/SKILL.md`, read-back bullet | "… this rule compares aliases and levels only." | replaced: "aliases, levels and the `floor=` value only" | d5 fix 7 (D-08, S-09) |
| R20 | `skills/dev-review/references/review-report.md`, Read-back line | "… values as well (Issue #96)" | "and its `floor=` value" inserted | d5 fix 5 |
| R21 | `skills/dev-gate/SKILL.md`, Output, Read-back line | "… the call form without `<DIR>` or `<ID>` (Issue #96)" | "; the `--floor` value of the call and the `floor=` value of the line" added | d5 fix 5 |
| R22 | `skills/dev-deliver/references/task-brief.md`, "Why this model/effort" line | "… escalation step and the quality failure it answers>" | "; the `--floor` value of its read-back (R-DEL-2)" added | d5 fixes 1, 5 |
| R23 | `skills/dev-core/SKILL.md`, read-back bullet | "`BELOW` and every `STOP` token except `BAD_ARGS` are environment, permission or data failures (R-VER-2): a higher effort does not fix them." | replaced: "A `BELOW` line whose expected values meet the floor of the call, and every `STOP` token except `BAD_ARGS`, are environment, permission or data failures (R-VER-2): a higher effort does not fix them." (a clarification, not a loosening; DL-045 (o)) | I96-IR-P2-C2 (a); D-04 |

Not in this table, and so unchanged in PR-2: the routing tables and the
sentences that only rename a family (PR-3), the README (PR-3) and
`agents/*.md`.

## Task graph

| Task | Agent | Paths | Requested | Recorded | Effective |
| --- | --- | --- | --- | --- | --- |
| T1: `--floor`, the check order, `floor=`, realpath, the static test, the role ranges, the `check_pack` pins and the `FLOORS` check, tests | `dev-implementer` | the T1 rows above | `opus`/`high` | main agent fills in (R-DEL-2) | `unknown` |
| T2: rule sentences R1 to R22 (one scripted run), the reference, records, this plan | `dev-implementer` | the T2 rows above | `opus`/`high` | main agent fills in (R-DEL-2) | `unknown` |
| T3: fix round 1 (cards I96-IR-P2-C1 to C4): R2 and R10 amended and R23 by hand edits, the reference, records, this plan | `dev-implementer` | `skills/dev-core/SKILL.md`, the reference, `deltas.md`, `docs/design-proposal.md`, REQ-009, the log, the CHANGELOG, `.dev/followups.md`, this plan | `opus`/`high` | main agent fills in (R-DEL-2) | `unknown` |
| T4: fix round 2 (cards I96-IR2-P2-C1 to C3), records only | `dev-implementer` | the reference, `deltas.md`, `docs/design-proposal.md`, REQ-009, the log, the CHANGELOG, `.dev/followups.md`, this plan | `opus`/`high` | main agent fills in (R-DEL-2) | `unknown` |

Why `opus`/`high`: the implement and docs role at the `strict` tier; the
R-DEL-2 floor applies (security-rule and public-contract text, and their
records). By the new rule the `--floor` value of their read-backs would be
`work`; the copy of the script at the base `1eb28de` has no `--floor`, so
the read-backs of this PR use the call form of the base rule (with
`--config-base`, without `--floor`; d5). T1 and T2 run at the same time in
one worktree with disjoint paths. After both: `scripts/validate.sh`, the
unit tests and `scripts/check_pack.py`; the implementation review; the
commit scan, the commit, the push scan with the PR text, the push, the PR
(`Part of #96`) and the ready-for-Merge-Review card.

## Review procedure (card I96-P2-C1 (a); d4 section 5)

1. Compare `git --no-replace-objects diff --raw --no-abbrev --no-renames
   --ignore-submodules=none --no-relative -z <base> <head>` with the file
   list above, mode changes, symlinks and removals included.
2. Read `git --no-replace-objects diff --no-ext-diff --no-textconv --text
   --ignore-submodules=none --no-relative` once, without `-w`, for
   indentation, blank lines and the levels of lists.
3. With the output of the helper script, compare each changed sentence
   with a row R1 to R23. A change of a rule sentence outside the table is a
   finding.

The helper script lists the removed, replaced and added sentences between
base and head; it never gives PASS or FAIL and is not a gate. It refuses a
file that is not a regular file (lstat or `O_NOFOLLOW`); it takes a rev
only as a full ID of 40 or 64 hexadecimal digits; its `--worktree` mode
takes only relative paths inside the repository without `..`; it reports a
file missing at the base or at the head separately; on its own error it
prints one fixed line and, at the end, the count of errors (not a PASS or
FAIL of the content); it marks control and format characters (Cc, Cf); it
opens files with `newline=""`. Records name it only by `<notes>` or its
SHA-256; it is not committed.

Commit and merge: as for PR-1, the commit's tree and the merged tree equal
the reviewed tree, checked with the hardened commands, and the parent
commit is checked.

The implementation review (a deep review and a Security Diff Scan,
`opus`/`xhigh`, both read back) checks by name the fixes of d5 and the
final text of R2 and R10.

## Design review round 4

Skipped by the user's decision P2R3-C1 (b). The implementation review
covers it. A new problem that the implementation review finds in R2, R10
or the `--floor` mapping stops the work with a decision card (R-VER-2) and
is not fixed in that round; other findings go through the usual fix
rounds.

## Implementation review

Round 1 (2026-11-03), on the staged change with the index tree
`2b286ec8cb2c7c6f03e8bf45a916c07ca4625e60`:

- A deep review and a Security Diff Scan, both `opus`/`xhigh`, both read
  back with `PASS`; the start and end diff hash of both is
  `30e752ab5013b4a9aa465846c9026f89bcf93d3d7e94e9af8cc29a40bd2a9305`.
  Neither has a MUST-FIX. A first dispatch of the deep review with a wrong
  isolation setting was stopped at once and does not count.
- Stopped by R-VER-2 (card I96-P2R3-C1 (b)): findings S-02 and D-04 are
  new problems in R2 and R10, so the round did not fix them and gave stop
  cards.
- Findings and dispositions:
  - S-02 (R2 and R10 lost "an earlier round" of the trigger): card
    I96-IR-P2-C1 (a); R2 and R10 amended.
  - D-04 (the old sentence that every `BELOW` is an environment,
    permission or data failure, against the floor `BELOW` of R10): card
    I96-IR-P2-C2 (a); row R23.
  - S-01 and D-02 (the third case of (i) was left for the orchestrator to
    confirm, while the reference and the corrections of D-029 residual
    risk 4 wrote it as authorized): card I96-IR-P2-C3 (b); not part of
    (i), an unauthorized residual risk until PR-3 (residual risk 23).
  - D-01 and S-03 (the reason of residual risk 22): card I96-IR-P2-C4 (a);
    rewritten.
  - D-03, S-04 and S-05 (FU-050, FU-054 and FU-062): card I96-IR-P2-C4
    (a); notes added, the rows stay Open.
  - D-05 (the CHANGELOG lacked the branch outside the repository): card
    I96-IR-P2-C4 (a); added.
  - S-06 ("gets `BAD_ARGS` (fail closed)" says too much): card
    I96-IR-P2-C4 (a); residual risk 13 rewritten.
  - S-07 (`FLOORS` is compared with `==`, so `3.0` passes too; no security
    effect): kept as is.
- The security reviewer reported that its `python3 -I` debugging rewrote
  an ignored `__pycache__` file of the read-back script; this does not
  change the index or the diff, and the file is not deleted (the user
  decides).
- Cards I96-IR-P2-C1 to I96-IR-P2-C4. The user's answer (the user's words
  in the orchestrator session, relayed): 「I96-IR-P2-C1 a，C2 a，C3 b，C4 a」. With C3 (b) the
  user also approves the wider scope of PR-3. The orchestrator states that
  the read-backs in this repository always use the stdin form; no
  mechanism checks this before PR-3 (the gap of residual risk 23).
- Next (card I96-IR-P2-C4 (a)): a scoped implementation review round 2 of
  this fix round, a deep review and a Security Diff Scan at `opus`/`xhigh`.
- The fix-round-1 implementer (T3) reported that it ran one `git
  write-tree`, against its brief. The tree already existed, and the staged
  content was unchanged.

Round 2 (2026-11-03), on the staged change with the index tree
`fd53147c4306b863140c2d6c951cdf52566f36c8`:

- A deep review and a Security Diff Scan, both `opus`/`xhigh`, both read
  back with `PASS`; the start and end hashes of both are the same. The
  hash of the fix diff is
  `f0ea4653d49cba680ce53b90c276282203518b05dfc4e9b1e5444b65ae1834a6`, and
  the hash of the full diff is
  `08d89b8905d874f0678190d91181856c2ec85fa3609377cc4659abe23f2b176d`.
  The deep review has no MUST-FIX, one SHOULD-FIX and no R-VER-2
  candidate; the Security Diff Scan has no MUST-FIX, one SHOULD-FIX, three
  NITs and no R-VER-2 candidate. Both confirm that card IR-P2-C1 (a)
  closes the gap of round 1 and only tightens; that after card IR-P2-C2
  (a) every floor `BELOW` still stops and asks the user; and that the
  records write the PR-3 check as the answered card does ("under a
  worktree of the same Git repository"). The round finds no new problem in
  R2, R10, R23 or the `--floor` mapping. Both reviewers report that they
  stayed read-only.
- Stopped by R-VER-2 ("the same mechanism needed fixes and produced new
  problems in two consecutive rounds"): the records of the scope of (i)
  needed fixes in round 1 (S-01 and D-02) and gave new SHOULD-FIX findings
  in round 2 (D-01 and S-02), so the round did not fix them and gave stop
  cards.
- Findings and dispositions:
  - D-01 (SHOULD-FIX) and S-01 (NIT) (summary sentences that count "both
    reads use the same wrong copy" as (i), and so the case of residual
    risk 23 as well): card I96-IR2-P2-C1 (a); residual risk 3, the D-029
    residual risk 5 correction and the FU-062 note list only the case that
    (i) still accepts.
  - S-02 (SHOULD-FIX) (the second case of (i), the same wrong base literal
    in both reads, is an agent error as well): card I96-IR2-P2-C2 (b);
    withdrawn from (i), an unauthorized residual risk (residual risk 24),
    FU-063, not in PR-3.
  - S-03 (NIT) (the premises of the PR-3 check): card I96-IR2-P2-C3 (a);
    written at the PR-3 scope.
  - S-04 (NIT) ("not exercised between the merges" says more than any
    mechanism shows): card I96-IR2-P2-C3 (a); reworded.
  - Notes of the deep report (the grammar of the Method item, the
    exceptions of the `_` ban in the FU-050 note, the T3 row of the task
    graph, the `git write-tree` of T3, the earlier-round clause in the
    CHANGELOG): card I96-IR2-P2-C3 (a); fixed.
- The deep reviewer also gave an inference that it did not list as a
  finding: R23 says "expected values meet the floor of the call", so for a
  `--floor none` dispatch an ordinary `BELOW` may read as not classified;
  this affects the cost only, and the work still stops and asks the user.
  The main agent does not list it as a finding either; listed, it would be
  an R-VER-2 candidate for R2 and R10.
- Cards I96-IR2-P2-C1 to I96-IR2-P2-C3. The user's answer (the user's
  words in the orchestrator session, relayed): 「I96-IR2-P2-C1 a，C2 b，C3 a」.
  The orchestrator recommended (b) over the main agent's (c) for C2, for
  these reasons: a check that the base is an ancestor of
  `origin/<default>` would stop forever in a local-only repository without
  a remote or with a stale origin, which recreates the dead end that #96
  removes, so the check needs its own design; PR-3 was already widened
  once (card I96-IR-P2-C3 (b)); the case is unlikely, because both
  literals must be wrong, and wrong to a commit of the change itself.
- Next (card I96-IR2-P2-C1 (a)): a scoped implementation review round 3
  of the fix diff of this round only, a deep review and a Security Diff
  Scan, both at `opus`/`xhigh`.

## Merge card items (d5 section 4)

- The scope (a) to (h) of the `fable` loosening (DL-045 item (1)).
- The narrow loosening (i), one case only, outside the pack repository:
  the main agent and the script read the same installed copy, which the
  user edited. Not part of (i):
  - the same wrong base literal in both reads: by card I96-IR2-P2-C2 (b),
    the user's decision relayed by the orchestrator, an agent error and an
    unauthorized residual risk (residual risk 24), tracked by FU-063 and
    not in PR-3;
  - a main agent that wrongly judges that the skill path lies outside the
    repository of the change: by card I96-IR-P2-C3 (b), the user's
    decision relayed by the orchestrator, an unauthorized residual risk
    until PR-3 adds a deterministic check (residual risk 23).

## Residual risks

D-029 (PR-2 supplement) gives them in both languages:

1. Between PR-2 and PR-3 the routing tables and the sentences that only
   rename still name families and values; `check_pack` pins them exactly.
2. `fable` is not evaluated by this pack, is the most expensive family,
   is not verified on the host and has no listed ID.
3. The narrow loosening (i): both reads of the main agent use the
   installed copy outside the pack repository that the user edited. Items
   23 and 24 are not part of it. FU-062 is the case of two different base
   literals.
4. A wrong `--floor` value is not caught by the script; whether the higher
   one is passed when unsure rests on review.
5. The condition on families of a higher tier rests on the agent's choice
   only.
6. The main-session comparison is the agent's own until Issue #79 slice D.
7. A main session on a newer, unlisted Opus waits for the ID to be listed
   before every write of work under the floor, or the user acts.
8. The main agent's configuration read is not checked by `validate_config`;
   this affects the conversion to a floor and the session value.
9. Realpath: the Read tool may resolve `..` literally; a real file name
   other than the expected one gives `BAD_ARGS`; a race.
10. With role ranges up to `max`, one failed fix round after the main
    agent chose `max` escalates to the next tier, from tier 3 to
    `fable`/`max`.
11. Whether a meaning changed rests on the reviewers; the helper script is
    not committed, so others cannot check its SHA-256.
12. Whether a merge requires CI is not verified.
13. After the merge and before a session reloads the pack, a call of the
    old rule without `--floor` gets `BAD_ARGS`. A session that has not
    reloaded the pack may still, under the old rule, add a `--floor` in its
    one allowed correction; the remedy is item 15 (reload the pack or start
    a new session).
14. A branch whose bound base is before PR-2 gets `unknown` for every
    read-back by the new rule; a rebase comes first.
15. The remedy for item 13: reload the plugin or start a new session
    before a dispatch on a base after PR-2; the main agent owns this.
16. No independent review checks a wrong `--floor` value; only the brief
    record and the reviewers' reading show it.
17. An older-generation `version` ID of a tier 3 family meets every floor
    with `WARN` (D-029 residual risk 1).
18. A copy without a family whose tier equals a floor uses the next tier
    up, today `fable`; this adds cost.
19. The configuration read and the read of the script are separate reads
    and can use different bases after a rebase.
20. `--floor` is verified only on synthetic fixtures before the merge.
21. `work` and `review-routine` have the same floor, so "the higher one"
    can tie; this affects later audits only.
22. The review of `dev-retro` step 5 passes `review-scan`. Step 5 names
    no `dev-review` mode, so `review-scan` comes from R10 ("when this
    session's own reading cannot tell, … the higher floor"), not from the
    `opus`/`xhigh` values of the step, which would be a role found by equal
    values, which R2 forbids. The remaining risk: a session that reads it
    as "every other dispatch" passes `none`, and the script then makes no
    floor check; the expected values still come from the dispatch.
23. A main agent that wrongly judges that the skill path lies outside the
    repository of the change: both reads use the copy on the skill path,
    and nothing stops a wrong tier. Not part of (i): by card I96-IR-P2-C3
    (b) an unauthorized residual risk until PR-3 adds a deterministic
    check. The orchestrator states that the read-backs in this repository
    always use the stdin form; no mechanism checks this before PR-3.
24. The same wrong base literal in both reads of the main agent (for
    example the head of the change): both reads use the configuration file
    of that commit, and nothing stops a wrong tier; the path-form check of
    PR-3 does not catch it, because the call then uses the stdin form. Not
    part of (i): by card I96-IR2-P2-C2 (b) an agent error and an
    unauthorized residual risk. FU-063 tracks a deterministic check of the
    bound base literal that works with no remote or a stale origin; it is
    not part of PR-3.

## Read-back records

## Non-goals

PR-3 work (the routing tables and the rule sentences that name roles
only, the check of the role names of the tables, the family-name lint,
the move of the tested-host record to REQ-009, the README section on the
configuration file, and, by card I96-IR-P2-C3 (b), a deterministic check
of the read-back script: when it runs by path, and the realpath of its own
file is under a worktree of the same Git repository as the current working
directory, it gives a STOP and asks for the `--config-base` stdin form;
the PR-3 design rests on two premises: the check takes the current working
directory as the repository of the change, and it fails closed when the
working directory is in no Git repository, when a git query fails, and
when variables like `GIT_DIR` are set), `agents/*.md`, provider-specific
model IDs, a wider ID character set, and the work of FU-059, FU-060,
FU-062 and FU-063.
