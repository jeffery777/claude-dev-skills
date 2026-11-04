# Issue #96 PR-3 plan: role names in the routing tables and rules, the family-name lint, and the repository check of the read-back script (`Closes #96`)

- Objective: GitHub Issue #96 (body and comments 1 to 5), PR-3 of three:
  the routing tables and the rule sentences name roles of the
  configuration file `skills/dev-core/model-config.json` only (card
  I96-C8 as changed); `check_pack` gets a family-name lint and a check of
  the role names of the tables; the record of the tested host behavior
  moves from R-DEL-2 to REQ-009; the README gets a section on the
  configuration file; and, by card I96-IR-P2-C3 (b), the read-back script
  run by its path stops with `IN_REPO` when its copy lies in a worktree of
  the same Git repository as the current working directory (residual risk
  23 of the D-029 PR-2 supplement). The inputs that the PR #99 merge gate
  record moved to PR-3 (MR99-S-02, S-03, S-04, D-01 and M-01) and the
  items of FU-061 are done here.
- Rigor `strict`. Reason (R-RIG-1): a change to a security rule (R-DEL-2,
  the read-back gate), to pack rule text, and to an executable that gates
  commits; the R-DEL-2 floor applies to every node.
- Base: `main` `c78d53c7da11c18178ca32bf1855200b7f5b7101` (`c78d53c`, the
  merge of PR #99), branch `claude/issue-96-pr3-796c75`.
- Spec: the PR-3 designs d1 to d5 of 2026-11-03 (each later one wins; d5
  is the final one for the implementation), with the decision cards
  I96-P3-C1, I96-P3-C2, I96-P3-R2-C1 and I96-P3-R2-C2, and the
  implementation review stop cards I96-P3-IR1-C1, I96-P3-IR1-C2 and
  I96-P3-IR2-C1. The
  design files are in the session notes, which are not in the repository;
  the D-029 PR-3 supplement records what they settle.
- Method (cards I96-P2-C1 (a) and I96-P2-C2 (a), still in force): only the
  sentences of a closed list change (P3-R1 to P3-R18 below). One scripted
  run of `apply_pr3.py` (SHA-256
  `64dc996252556e81c7b036a8521a3a09900e139970d636ca0162d4824486f178`; not
  committed) made all 22 edits in 6 files; it asserts that each base text
  occurs exactly once and writes nothing otherwise. Every other rule
  sentence stays word for word. The reviewers compare each changed
  sentence with this table (see Review procedure).

## Source trace (dev-plan step 2)

Sources: the Issue #96 body and comments 1 to 5 (comment 4 has the PR-3
scope); D-029 with its PR-2 supplement and residual risks 4, 5, 22, 23
and 24; DL-040, DL-042, DL-044 and DL-045; REQ-009 and REQ-026; FU-045,
FU-046, FU-060 to FU-063; the PR #99 merge gate record (MR99-S-02,
MR99-S-03, MR99-S-04, MR99-D-01 and MR99-M-01) and the PR-2 inputs
IR3-P2-S-01, O-1 and O-4; and these user answers (Claude Code session, the
user's words in the orchestrator session, relayed):

- 「開始 PR-3」: start PR-3.
- 「C1 b，C2 a」: card I96-P3-C1 (b), run by its path the script gives
  `STOP REPO_CHECK` when its copy lies in a Git repository and the working
  directory lies in none, and a copy in no repository does not stop; card
  I96-P3-C2 (a), the repository check reads no environment variable and
  `git` gets the environment of the caller.
- 「R2-C1 a，R2-C2 a」: card I96-P3-R2-C1 (a), design d5 makes the fixes of
  design review round 2, with no third design review round, and the
  implementation review checks them and every hit of the Record sweep
  below; card I96-P3-R2-C2 (a), C2 (a) stays, and a relative
  `GIT_COMMON_DIR` is an exception to the inference of card C2, a sub-item
  of residual risk 23, with a test that uses a real `git` and expects
  `REPO_CHECK`; residual risk 23 stays unauthorized, and the user decides
  at merge.
- 「C1 a，C2 a，接受」 (2026-11-04): card I96-P3-IR1-C1 (a), a relative
  `GIT_DIR` and a relative `GIT_COMMON_DIR` together are the exception to
  the inference of card C2, a sub-item of residual risk 23, still an
  unauthorized residual risk that the user decides at merge; card
  I96-P3-IR1-C2 (a), one fix round (P3-T3), then a scoped implementation
  review; 「接受」, the user explicitly accepts the two sentences that T2
  added next to the unified superseding sentence of the D-029 PR-3
  supplement.
- 「IR2-C1 a」 (2026-11-04): card I96-P3-IR2-C1 (a), one fix round of the
  records only (P3-T4), then a scoped review (a deep review and a Security
  Diff Scan of the fix only).
- From PR-2 and earlier, still in force: 「I96-IR-P2-C1 a，C2 a，C3 b，C4 a」
  (C3 (b): the deterministic check of the path form in PR-3),
  「I96-IR2-P2-C1 a，C2 b，C3 a」 (C2 (b): residual risk 24 goes to FU-063,
  not to PR-3; C3 (a): the two premises of the PR-3 check),
  「MR99-M1 a，確認 (1)、(i)、23、24，S-02 歸 D-027」,
  「照更正後的做法，只加進 D-027 風險清單」,
  「C8 改為：設定檔是唯一來源，路由表只標角色名、不寫數值；I96-C12 a＋停用規則；不加技能」,
  「I96-P2-C1 a，P2-C2 a，P2-C3 a」 and
  「為什麼是依值找角色？而是不是依任務找角色？如果值是依任務複雜度給定的，那依值找角色等同於依任務找角色」
  (the role of a node comes from its task type, never from equal values).
- The user's meaning, relayed by the orchestrator (a summary, not the
  user's words): a ban such as "an agent never edits the installed
  configuration file" is not practical, because nobody can tell who made
  an edit, and the user may ask an agent to make one. PR-3 adds no such
  ban.

From the PR-3 design reviews of rounds 1 and 2, not from the user's words:
the other wording of the rule sentences (finding IDs in the table below).

## PR-3 files

| Status | Path | Task |
| --- | --- | --- |
| M | `skills/dev-core/scripts/model_effort_readback.py` | T1 |
| M | `scripts/check_pack.py` | T1 |
| M | `tests/test_model_effort_readback.py` | T1 |
| M | `tests/test_core_checks.py` | T1 |
| M | `skills/dev-core/SKILL.md` | T2 |
| M | `skills/dev-deliver/SKILL.md` | T2 |
| M | `skills/dev-deliver/references/task-brief.md` | T2 |
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
| M | `README.md` | T2 |
| M | `.dev/followups.md` | T2 |
| M | `.dev/issue-96-pr2/plan.md` | T2 |
| A | `.dev/issue-96-pr3/plan.md` | T2 |

## Rule sentences (P3-R1 to P3-R18; d1 section 2, d4 section 5, d5 section 1)

The base text of each row is the text at `c78d53c`; the new text is in
`apply_pr3.py`, word for word. The one scripted run makes 22 edits: P3-R1
and P3-R2 are one edit, P3-R8 is three, P3-R12, P3-R14 and P3-R15 are two
each, and every other row is one.

| ID | File and place | Base text (start) | Change | Cards and findings |
| --- | --- | --- | --- | --- |
| P3-R1 | `skills/dev-deliver/SKILL.md`, routing table | "\| Node \| Agent \| Model / effort \|" and its six rows | replaced: the column `Role`; each row names roles of the configuration file and no value; the explore row says "at least the work floor"; "a higher effort only when the user asks" for the security review | I96-C8 as changed; d1 |
| P3-R2 | same, after the table | (insertion) | added: the table names a role for each node and no value; the row value is the family and the lowest effort of that role, read as the configuration read of R-DEL-2 says | I96-C8 as changed |
| P3-R3 | `skills/dev-review/SKILL.md`, mode table, third column | "`dev-reviewer`, model `opus`, effort `high`; …" (four rows) | replaced: roles `review-routine`, `review-routine-light`, `review-deep`, `review-security` and `scan` | I96-C8 as changed |
| P3-R4 | same, routine review | "the routine review uses model `opus`, effort `high`:" | replaced: "uses the role `review-routine`:" | I96-C8 as changed |
| P3-R5 | same, escalation paragraph | "A trigger found after the review re-runs the review at `opus`/`high` …" | replaced: the roles `review-routine` and `review-routine-light`, same meaning | I96-C8 as changed; I73-R2-C2 (a), I73-R3-C1 (a) |
| P3-R6 | `skills/dev-core/SKILL.md`, R-DEL-2, the bullet on tested host behavior | "Tested host behavior (Issue #77, 2026-10-29; …" (the whole bullet) | replaced: the record is in REQ-009 (moved there by Issue #96 PR-3); in the shipped pack the agent file values are the family and the lowest effort of the `agent_default` role, pinned by `check_pack` | I96-P2-C3 (a); d2 A; deep R14; d5 |
| P3-R7 | R-DEL-2, escalation bullet | "every later review round of that node uses `opus`/`high`, never `sonnet`/`medium` again (Issue #73, C4)." | replaced: the roles | I96-C8 as changed |
| P3-R8 | R-DEL-2, read-back bullet, three places | "A `light` routine review at `sonnet`/`medium` is read back …"; "only the review at `opus`/`high` whose read-back passes does."; "The re-run at `opus`/`high` that `dev-review` makes" | replaced: the roles | I96-C8 as changed |
| P3-R9 | same, path-form template | "… `model_effort_readback.py subagent --projects-dir <DIR>` …" | `--floor <floor>` inserted | MR99-S-03 |
| P3-R10 | same, D-027 sentence | "… change a copy of the script, or add a replace ref" | "or of the configuration file" inserted; a recorded risk, no ban | MR99-S-02 |
| P3-R11 | same, after "… and `--config-base` is then a wrong call." | (insertion) | added: the repository check of the path form (`STOP REPO_CHECK`, `STOP IN_REPO`), no environment variable read, the working directory as the repository of the change, the copy in a worktree without a `.git` entry (residual risk 23) | I96-IR-P2-C3 (b), I96-P3-C1 (b), I96-P3-C2 (a), I96-P3-R2-C2 (a); d4 D-09, S-08, deep R9; d5 S-06, deep R3 |
| P3-R12 | same, two places | "and every `STOP` token except `BAD_ARGS`, are …"; "`BAD_ARGS` is a wrong call: …" | "and `IN_REPO`" inserted; replaced: `BAD_ARGS` and `IN_REPO` are wrong calls with one correction that keeps the `--floor` value, and after `IN_REPO` a new configuration read at the bound base | I96-IR-P2-C3 (b); d4 D-08, S-08 |
| P3-R13 | R-DEL-2 main text, after "never a row or role found by equal values." | (insertion) | added: the tables name roles and no values; the row value is the family and the lowest effort of the role | I96-C8 as changed |
| P3-R14 | `skills/dev-retro/SKILL.md`, step 5, two places | "Dispatch `dev-skills:dev-reviewer` with model `opus` and effort `xhigh` (R-DEL-2), and a brief (R-DEL-1)."; "names `opus`; which version the alias resolves to is not verified" | replaced: the role `review-deep`, a deep review of the `dev-review` mode table (R-REV-6); "names the family alias of that role" | I96-C8 as changed; d4 D-02 (task type, not values); d5 deep |
| P3-R15 | `skills/dev-deliver/references/task-brief.md`, escalation triggers line, two places | "(`light` routine review at `sonnet`/`medium` only)"; "re-runs the review at `opus`/`high`, as for trigger 5" | replaced: the roles | I96-C8 as changed |
| P3-R16 | `skills/dev-review/references/review-report.md`, header list | "`light` routine review at `sonnet`/`medium` only" | replaced: the role `review-routine-light` | I96-C8 as changed |
| P3-R17 | R-DEL-2 main text | "from the … record below" (the record of the tested host) | replaced: "(REQ-009)" | d4 D-04 |
| P3-R18 | `skills/dev-deliver/references/task-brief.md`, recorded-value paragraph | "the … record of R-DEL-2" (the record of the tested host) | replaced: "(REQ-009)" | d4 D-04 |

Not in this table, and so unchanged in PR-3: the `Role:` field of
`task-brief.md` (deep R10: a field name whose value is an agent kind, not a
role of the configuration file) and `agents/*.md`.

## Task graph (d5 section 5)

| Task | Agent | Paths | Requested | Recorded | Effective |
| --- | --- | --- | --- | --- | --- |
| P3-T1: the repository check of the read-back script, the family-name lint and the table check of `check_pack`, tests | `dev-implementer` | the T1 rows above | role `implement` (`opus`/`high`) | main agent fills in (R-DEL-2) | `unknown` |
| P3-T2: rule sentences P3-R1 to P3-R18 (one scripted run), the reference, records, the README, the two plans | `dev-implementer` | the T2 rows above | role `implement` (`opus`/`high`) | main agent fills in (R-DEL-2) | `unknown` |
| P3-T3: the fixes of implementation review round 1 (card I96-P3-IR1-C2 (a)) | `dev-implementer` | `docs/design-proposal.md`, REQ-009, the reference, `skills/dev-core/deltas.md`, `README.md`, this plan, `tests/test_model_effort_readback.py` | role `implement` (`opus`/`high`) | main agent fills in (R-DEL-2) | `unknown` |
| P3-T4: the record fixes of implementation review round 2 (card I96-P3-IR2-C1 (a)) | `dev-implementer` | `docs/design-proposal.md`, REQ-009, `docs/requirements/log.md`, `CHANGELOG.md`, the reference, `skills/dev-core/deltas.md`, this plan | role `implement` (`opus`/`high`) | main agent fills in (R-DEL-2) | `unknown` |

Why role `implement`: the implement and docs row at the `strict` tier; the
R-DEL-2 floor applies (security-rule and public-contract text, and their
records). The read-backs pass `--floor work` and use the stdin form at
the bound base `c78d53c`. By "Never run two writers at once" of
`dev-deliver`, the two nodes run one after the other in one worktree, T1
first. Before T2, the family-name lint and the table check of T1 fail on
the base rules only; after T2 they pass. After both:
`scripts/validate.sh`, the unit tests and `scripts/check_pack.py`; the
implementation review; the commit scan, the commit, the push scan with the
PR text, the push, the PR (`Closes #96`) and the ready-for-Merge-Review
card.

## Review procedure

1. Compare `git --no-replace-objects diff --raw --no-abbrev --no-renames
   --ignore-submodules=none --no-relative -z <base> <head>` with the file
   list above, mode changes, symlinks and removals included.
2. Read `git --no-replace-objects diff --no-ext-diff --no-textconv --text
   --ignore-submodules=none --no-relative` once, without `-w`, for
   indentation, blank lines and the levels of lists.
3. Compare each changed rule sentence with a row P3-R1 to P3-R18. A change
   of a rule sentence outside the table is a finding.
4. Check every row of the Record sweep below against the diff (card
   I96-P3-R2-C1 (a)).

No helper script that lists the sentences is part of this plan. When a
reviewer uses one, the review record names it by its file name and SHA-256
only and states what it really does, as the corrected PR-2 plan does for
`issue96-pr2-sentences.py` (MR99-D-01).

The diff hash uses `git --no-replace-objects diff --no-relative --binary
--no-textconv --no-ext-diff --ignore-submodules=none --submodule=short`.
Commit and merge: the commit's tree and the merged tree equal the reviewed
tree, and the parent commit is checked.

The implementation review (card I96-P3-R2-C1 (a)) is a deep review (role
`review-deep`) and a Security Diff Scan (role `review-security`), both
`opus`/`xhigh` and read back with `--floor review-scan`, on the staged
diff. It checks by name: each test of d5 section 3 (the portable inode
test with a mock `os.stat`, the real test on a file system that ignores
case, the relative `GIT_COMMON_DIR` test with a real `git`, the dangling
`.git` symlink, the different folder depths, the static pins); every row
of the Record sweep; the record of card I96-P3-R2-C2 (a); and that
`FORBIDDEN` and `FORBIDDEN_TEXT` of the static test do not change. A new
problem in the repository check, in P3-R11 or in P3-R12 stops the work
with a decision card (R-VER-2).

## Design review

Before round 1: the decision cards I96-P3-C1 (d1) and I96-P3-C2 (d2);
the user's answer 「C1 b，C2 a」 (d3).

Round 1 (2026-11-03), on d1 to d3: a deep review and a security review,
both `opus`/`xhigh`, both read back with `PASS` and `floor=review-scan`.

- Deep review: 0 MUST-FIX, 3 SHOULD-FIX, 6 NIT and one concern (D-10,
  `--path-format` needs `git` 2.31). SHOULD-FIX: D-01 (the reference),
  D-02 (P3-R14 found its role by values; residual risk 22 and REQ-026),
  D-03 (the status of residual risk 23). No R-VER-2 candidate.
- Security review: 0 MUST-FIX, 1 SHOULD-FIX (S-01, the reference and the
  premise 2 records) and 8 NIT. It measured the inference of card C2 (a)
  with `git` 2.54.0 on macOS: 30 settings of the environment or the Git
  configuration, none of which gave `PASS` for the same repository, with
  the correction S-03 for relative values. The installed copies on the
  test machine (the official marketplace and the cache) lie in no Git
  clone. No R-VER-2 candidate.
- Design d4 fixes all of them: the argv without `--path-format` and the
  join of a relative value (D-10); the `os.stat` step and the
  `(st_dev, st_ino)` comparison (S-02); the tests (S-03, S-05, deep R6);
  P3-R11 and P3-R12 as final (D-08, D-09, S-08); P3-R14 by the task type
  (D-02); P3-R17 and P3-R18 (D-04); the record list (D-01, D-03, D-05 to
  D-07, S-01, S-06, S-07, S-09).

Round 2 (2026-11-03), scoped to d4: a deep review and a security review,
both `opus`/`xhigh`, both read back with `PASS` and `floor=review-scan`.

- Deep review: 0 MUST-FIX, 0 SHOULD-FIX, 3 NIT (D-01 to D-03, all "the
  record list of d4 is not complete").
- Security review: 0 MUST-FIX, 3 SHOULD-FIX (S-01: the inode branch holds
  the macOS cases, and the planned symlink test does not reach it; S-02:
  a relative `GIT_COMMON_DIR` that `git` joins wrongly in a subfolder;
  S-03: four more places that state premise 2) and 4 NIT. The script
  design does not change.
- Stopped by R-VER-2: the record list and the inode test needed fixes in
  two rounds in a row, and S-02 touches the inference that card C2 rests
  on. Stop cards I96-P3-R2-C1 and I96-P3-R2-C2; the user's answer:
  「R2-C1 a，R2-C2 a」. Design d5 makes the fixes: the deterministic pattern
  list of the Record sweep, the portable and the macOS inode tests, the
  relative `GIT_COMMON_DIR` test and record, and the other NITs. No third
  design review round.

## Implementation review

Round 1 (2026-11-04), on the staged diff, the diff hash the same before
and after each review: a deep review (role `review-deep`) and a Security
Diff Scan (role `review-security`), both `opus`/`xhigh`, both read back
with `PASS` and `floor=review-scan`.

- Deep review: 0 MUST-FIX, 1 SHOULD-FIX, 2 NIT and 1 SCOPE-CREEP.
  SHOULD-FIX IR-P3-D-01: the sub-items of residual risk 23 leave out a
  relative `GIT_DIR` (design d4 had it under D-027; d5 changed the class
  of `GIT_COMMON_DIR` only). NIT D-02: the dotfiles stop case needs "when
  the working directory is not in a repository of its own"; NIT D-03: the
  reason of the `CHANGELOG.md` row of the Record sweep is not true.
  SCOPE-CREEP D-04: a whitespace change of the `FAMILY` line in
  `tests/test_model_effort_readback.py`. No problem of correctness in the
  script, `check_pack`, the tests or the rule sentences.
- Security Diff Scan: 0 MUST-FIX, 0 SHOULD-FIX, 6 NIT: S-01 (as D-01),
  S-02 (the scopes of `safe.directory`), S-03 (the `IN_REPO` condition
  holds by the answer of `git` only; the dotfiles case), S-04 (the limits
  of the family-name lint), S-05 (as D-04), S-06 (no test fails when the
  final-newline check is removed). No new path that passes and no
  unrecorded loosening. Mutation: 13 of 14 behavior mutants of the
  repository check caught, and all 7 static mutants; the survivor was the
  removal of `not out.endswith(b"\n")`. The new subtest "one newline, not
  the final byte" of `RepoCheckInProcess.test_output_rules` now catches
  it: P3-T3 ran that test on a mutated copy in a scratch folder outside
  the repository, and the subtest fails (the script is unchanged). An
  output with no newline at all, such as `/x/.git`, does not catch the
  mutant, because the line count check stops it first.
- Both reviews: 166 hits of the Record sweep and 166 rows. The three format
  checks that T1 added to the table check are needed to fail closed (not
  scope creep); the changed count of `test_role_values_are_pinned` is
  right; leaving out the optional `S_ISDIR` check is acceptable; "Fixed by
  Issue #96 PR-3" on FU-061 before the merge is acceptable.
- Stopped by R-VER-2: D-01 is the mechanism of card I96-P3-R2-C1 (an
  incomplete record list) in a second round, and its class touches card
  I96-P3-R2-C2 (a). Stop card I96-P3-IR1 (cards I96-P3-IR1-C1 and
  I96-P3-IR1-C2); the user's answer: 「C1 a，C2 a，接受」. 「接受」 is the
  user's explicit acceptance of the two sentences that T2 added next to
  the unified superseding sentence (the second and the third sentence of
  the "Superseding" item of the D-029 PR-3 supplement), which the deep
  review asked for. P3-T3 makes the fixes; round 2 is a scoped deep review
  and Security Diff Scan of the fix diff, with G1 to G16 run again.
- Not verified: the session scratch folder that held `apply_pr3.py` was
  cleared on 2026-11-04, so the content of that script cannot be checked
  again; its 22 edits are in the diff, and both round 1 reviews checked
  them sentence by sentence.

Round 2 (2026-11-04), scoped to the fix diff of P3-T3 (7 files), the diff
hash the same before and after each review: a deep review (role
`review-deep`) and a Security Diff Scan (role `review-security`), both
`opus`/`xhigh`, both read back with `PASS` and `floor=review-scan`.

- Deep review: of the 10 items of round 1, 9 resolved and 1 (IR-P3-S-01)
  partly resolved; new: 0 MUST-FIX, 1 SHOULD-FIX, 3 NIT and 1 concern.
  SHOULD-FIX IR2-P3-D-01: `docs/requirements/log.md` had no row for the
  REQ-009 changes of round 1 (the list of card I96-P3-IR1-C2 and the
  owned paths of P3-T3 did not name the log). NIT D-02: the PR-3 entry of
  `CHANGELOG.md` left out 「C1 a，C2 a，接受」; NIT D-03: the sentence of
  this plan that the D-029 PR-3 supplement gives the two lint limits in
  both languages was not true (they were in DL-046 and this plan only);
  NIT D-04: as S-02 below. Concern SUS-01 (an inference, the same as the
  test of S-01): the condition on `GIT_WORK_TREE` is too narrow. Below
  the threshold: a line range of this plan off by one, "T2" not defined
  in `docs/design-proposal.md` and REQ-009, and the docstring of the
  script without "by the answer of git" (left for the ready card).
- Security Diff Scan: 0 MUST-FIX, 1 SHOULD-FIX, 1 NIT; no change of the
  behavior of the script, no new path that passes, no private data.
  SHOULD-FIX IR2-P3-S-01: "a relative `GIT_DIR` only when no
  `GIT_WORK_TREE` is set" is not true; a read-only test with `git` 2.54.0
  on macOS in six cases gave a relative `GIT_DIR` resolved from the folder
  of each call, whether or not `GIT_WORK_TREE` is set. The condition came
  from a parenthesis of the round 1 security summary, through the facts of
  card I96-P3-IR1-C1 and the brief of P3-T3. NIT IR2-P3-S-02: the command
  scope holds only `git -c` and `GIT_CONFIG_COUNT`, `GIT_CONFIG_KEY_<n>`
  and `GIT_CONFIG_VALUE_<n>`; `GIT_CONFIG_GLOBAL`, `GIT_CONFIG_SYSTEM` and
  `GIT_CONFIG_NOSYSTEM` choose or turn off the files of the global and
  system scopes.
- Both reviews: 186 hits of the Record sweep and 186 rows; the mutant that
  removes the final-newline check is caught by the new subtest (both
  reviewers ran it again in memory).
- Stopped by R-VER-2: records that were not complete or not exact needed
  fixes in design review round 2 (card I96-P3-R2-C1), implementation
  review round 1 (card I96-P3-IR1-C1) and this round. Stop card
  I96-P3-IR2-C1; the user's answer: 「IR2-C1 a」. P3-T4 makes the fixes in
  records only (items 1 to 5 of the card and the two small items of its
  notice), with two deterministic checks: every change of REQ-009 gets a
  log row and the quote list of `CHANGELOG.md` is updated, and every new
  sentence that states a fact gives its test or source or says that it is
  an inference. Then a scoped deep review and Security Diff Scan of the
  fix, with G1 to G16 run again.

## Residual risks

The D-029 PR-3 supplement gives them in both languages:

1. Residual risk 23, narrowed (a working directory in another repository
   or a submodule; a copy in no repository; a worktree without a `.git`
   entry; a bare layout, a fake `git` or a relative `PATH` entry; a
   relative `GIT_DIR` or `GIT_COMMON_DIR` when both `git` calls succeed and
   the two joined paths are two different existing paths, the exception to
   the inference of card C2 (cards I96-P3-R2-C2 (a) and I96-P3-IR1-C1 (a);
   a relative `GIT_DIR` resolves from the folder of each call, whether or
   not `GIT_WORK_TREE` is set (tested: read-only
   `git rev-parse --git-common-dir`, `git` 2.54.0, macOS, six cases,
   implementation review round 2, IR2-P3-S-01); the full pass of a
   relative `GIT_DIR` (two different existing git directories) is not
   tested)). Unauthorized; the user decides at merge. For a relative value, the
   scope of the inference of card C2 is this item.
2. Residual risk 24 of the PR-2 supplement: FU-063, not in PR-3.
3. The cost of card C1 (b): a project outside Git while the pack loads
   from a Git clone stops every read-back by path; whether a third-party
   marketplace install lies in a Git clone is not known.
4. Other cases that stop, fail closed: a dotfiles home folder when the
   working directory is not in a repository of its own, dubious
   ownership, a file system boundary, a sandbox that refuses the `lstat`
   (not tested), `git` before 2.13 (not tested).
5. A pack in a plain subfolder of the project repository gives `IN_REPO`,
   then usually `unknown`.
6. The new read after `IN_REPO` repeats the comparisons of that one
   dispatch only.
7. The family-name lint covers the listed scope only; the exception of
   the `model:` line applies to the front matter of every `agents/*.md`
   file, and the glob does not read a file or folder whose name starts
   with a dot (IR-P3-S-04; DL-046, REQ-009 and item 7 of the D-029 PR-3
   supplement).
8. FU-063 gets a trigger note only; the user's answer did not address it
   separately, and the ready card lists it again.
9. A session that has not reloaded the pack after the merge uses the old
   rule text and script (inference).

## Record sweep (card I96-P3-R2-C1 (a); d5 section 4)

P3-T2 ran each pattern below with `git grep -n -F '<pattern>'` over all
tracked files of the working tree after its edits, and the same fixed
string search over this plan, which `git grep` does not see until it is
staged. P3-T3 ran them again after its fixes (card I96-P3-IR1-C2 (a)),
with `git grep -n -F` only, because this plan is now in the index, and
P3-T4 ran them again after its fixes (card I96-P3-IR2-C1 (a)) the same
way; the line numbers below are those of the working tree after P3-T4. Each
hit is one row (a line with two hits of one pattern is one row). Dispositions:

- `changed`: the text at that place is new or edited by PR-3 (a new
  record, a new note, a pointer fix).
- `noted`: the old text stays; either a PR-3 note at the same place (the
  same line, row or list item) qualifies it, or the reason says why it
  is still true after PR-3, or the hit is not about the PR-3 check.
- `historical`: the text describes a PR-2 or earlier rule or decision,
  and the D-029 PR-3 supplement has a unified superseding sentence for it
  ("Superseding" item, both languages).

Patterns:

```
G1  tested-host record
G2  records the tested host
G3  until PR-3
G4  到 PR-3
G5  PR-3 adds
G6  PR-3 加
G7  variables like
G8  GIT_DIR
G9  in no Git repository
G10 不在任何
G11 reads the file of the change
G12 讀到的是變更自己的設定檔
G13 PR-3 makes
G14 item (i) of the PR-2 supplement
G15 補充的第 (i) 項
G16 fails closed
```

The places that design review round 2 named (d5 section 4; line numbers
at the base `c78d53c`, then at the working tree after P3-T4):

| Place at `c78d53c` | Now | Disposition |
| --- | --- | --- |
| `.dev/followups.md:57` (FU-045) | `:57` | `noted`: a PR-3 note in the Status column |
| `.dev/followups.md:58` (FU-046) | `:58` | `changed`: the Remaining risk column points to REQ-009; a PR-3 note |
| `.dev/followups.md:73` (FU-061) | `:73` | `changed`: Fixed, with the PR-3 note (the three moved items, premise 2) |
| REQ-009 `:231` | `:243` | `changed`: a PR-3 note |
| REQ-009 `:255` | `:267` | `changed`: pointer fix to this file |
| REQ-009 `:336` | `:348` | `noted`: a PR-3 note on the path form, with the qualifiers of d5 section 4 |
| REQ-009 `:352` | `:364` | `noted`: a PR-3 note on premise 2 |
| REQ-009 `:354` | `:366` | `noted`: a PR-3 note on residual risk 23 and on a wrong `--floor` value |
| `docs/design-proposal.md:803` | `:803` | `changed`: a PR-3 correction of premise 2 |
| `docs/design-proposal.md:809` | `:809` | `changed`: the pointer names residual risk 23 (MR99-S-04); a PR-3 correction |
| `docs/design-proposal.md:810` | `:810` | `changed`: a PR-3 correction of residual risk 5 |
| `docs/design-proposal.md:900` (residual risk 22) | `:900` | `changed`: a PR-3 note |
| `docs/design-proposal.md:901` | `:901` | `changed`: a PR-3 note |
| `docs/design-proposal.md:3576` to `:3580` | `:3641` to `:3651` | `noted`: a PR-3 correction follows |
| `docs/design-proposal.md:3624` to `:3627` | `:3695` to `:3706` | `changed`: the pointer names residual risk 23 (MR99-S-04); a PR-3 correction |
| `docs/design-proposal.md:3631` (residual risk 5) | `:3707` to `:3738` | `noted`: a PR-3 correction follows |
| `docs/design-proposal.md:4087` to `:4094` (residual risk 22) | `:4178` to `:4190` | `noted`: a PR-3 note follows |
| `docs/design-proposal.md:4095` to `:4101` | `:4191` to `:4201` | `noted`: a PR-3 note follows |
| `skills/dev-core/deltas.md:63` (DL-040) | `:63` | `changed`: a PR-3 note |
| `skills/dev-core/deltas.md:65` (DL-042) | `:65` | `changed`: a PR-3 note |
| `skills/dev-core/deltas.md:68` (DL-045) | `:68` | `changed`: a PR-3 note |
| `.dev/issue-96-pr2/plan.md:219` | `:226` | `noted`: a PR-3 note follows |
| `.dev/issue-96-pr2/plan.md:318` | `:340` | `noted`: a PR-3 note follows |
| `.dev/issue-96-pr2/plan.md:379` | `:404` | `noted`: a PR-3 note follows |
| `.dev/issue-96-pr2/plan.md:402` to `:405` | `:430` to `:433` | `noted`: a PR-3 note follows (line 437) |

Also checked, with no hit of a pattern: the record of the test in D-024
(`docs/design-proposal.md:578`, Chinese, and `:2646`, English, `:2582` at
the base) describes the Issue #77 rule of its time and stays as it is.

| Pattern | Place | Disposition | Reason |
| --- | --- | --- | --- |
| G1 | `.dev/followups.md:57` | `noted` | FU-045: the old place of the record in the Remaining risk column; a PR-3 note in the Status column says that the record moved to REQ-009 (d5 section 4) |
| G1 | `.dev/followups.md:58` | `changed` | FU-046: the Remaining risk column now names a strict change of the record in REQ-009; a PR-3 note in the Status column |
| G1 | `.dev/followups.md:73` | `changed` | FU-061: the Item column lists the move as PR-3 work; the new PR-3 note in the Status column says that it is done |
| G1 | `.dev/issue-77-effort-readback/plan.md:18` | `historical` | plan of an earlier Issue; it describes the rule of its time, when the record was in R-DEL-2 (Superseding item, last sentence) |
| G1 | `.dev/issue-77-effort-readback/plan.md:84` | `historical` | plan of an earlier Issue; it describes the rule of its time, when the record was in R-DEL-2 (Superseding item, last sentence) |
| G1 | `.dev/issue-85-retest-values/plan.md:148` | `historical` | plan of an earlier Issue; it describes the rule of its time, when the record was in R-DEL-2 (Superseding item, last sentence) |
| G1 | `.dev/issue-96-pr2/plan.md:425` | `noted` | PR-2 Non-goals list the move as PR-3 work; the PR-3 note after the paragraph (line 437) |
| G1 | `CHANGELOG.md:401` | `historical` | Issue #85 entry of the change log; it describes the rule of its time, when the record was in R-DEL-2 (Superseding item, last sentence; IR-P3-D-03) |
| G1 | `docs/design-proposal.md:927` | `changed` | new text of the D-029 PR-3 supplement (Chinese) |
| G1 | `docs/design-proposal.md:3637` | `noted` | English PR-2 split note; the PR-3 correction follows (lines 3646 to 3651) |
| G1 | `docs/design-proposal.md:4314` | `changed` | new text of the D-029 PR-3 supplement (English) |
| G1 | `docs/design-proposal.md:4315` | `changed` | new text of the D-029 PR-3 supplement (English) |
| G1 | `docs/design-proposal.md:4451` | `changed` | the Superseding item of the D-029 PR-3 supplement (English) |
| G1 | `docs/requirements/REQ-009-subagent-model-effort.md:243` | `changed` | Issue #77 group; a PR-3 note on the same line says that the record moved into REQ-009 |
| G1 | `docs/requirements/REQ-009-subagent-model-effort.md:265` | `noted` | Issue #79 slice A group; still true, because the name names the same record, now in this file |
| G1 | `docs/requirements/REQ-009-subagent-model-effort.md:267` | `changed` | pointer fix: the trigger now names the record in this file (d4 D-04) |
| G1 | `docs/requirements/REQ-009-subagent-model-effort.md:271` | `noted` | Issue #79 slice A group; still true, the same record |
| G1 | `docs/requirements/REQ-009-subagent-model-effort.md:364` | `noted` | PR-2 split item lists the move as PR-3 work; a PR-3 note on the same line points to the PR-3 group |
| G1 | `docs/requirements/REQ-009-subagent-model-effort.md:373` | `changed` | new Issue #96 PR-3 group: the moved record, word for word |
| G1 | `docs/requirements/REQ-009-subagent-model-effort.md:380` | `changed` | new Issue #96 PR-3 group (implementation review decisions): the third accepted sentence of the Superseding item, named by card I96-P3-IR2-C1 (a) |
| G1 | `docs/requirements/log.md:137` | `changed` | new log entry of PR-3 |
| G1 | `skills/dev-core/SKILL.md:181` | `changed` | rule sentence P3-R17 |
| G1 | `skills/dev-core/SKILL.md:183` | `changed` | rule sentence P3-R6 |
| G1 | `skills/dev-core/SKILL.md:185` | `noted` | rule sentence outside the closed list; still true, because the name names the same record and P3-R6 says where it is |
| G1 | `skills/dev-core/deltas.md:63` | `changed` | DL-040: a PR-3 note in the same row says that the record moved to REQ-009 |
| G1 | `skills/dev-core/deltas.md:69` | `changed` | new row DL-046 |
| G1 | `skills/dev-deliver/references/task-brief.md:46` | `changed` | rule sentence P3-R18 |
| G1 | `.dev/issue-96-pr3/plan.md:402` | `changed` | new text of this plan (the pattern list) |
| G2 | `docs/requirements/REQ-009-subagent-model-effort.md:243` | `noted` | the Issue #77 sentence stays; the PR-3 note on the same line says where the record is now |
| G2 | `skills/dev-core/deltas.md:63` | `noted` | the DL-040 sentence stays; the PR-3 note in the same row says where the record is now |
| G2 | `.dev/issue-96-pr3/plan.md:403` | `changed` | new text of this plan (the pattern list) |
| G3 | `.dev/followups.md:73` | `changed` | FU-061: the new PR-3 note quotes the phrase and says that the D-029 PR-3 supplement supersedes it |
| G3 | `.dev/issue-96-pr2/plan.md:226` | `noted` | PR-2 finding S-01 and D-02; the PR-3 note follows (lines 227 to 229) |
| G3 | `.dev/issue-96-pr2/plan.md:340` | `noted` | PR-2 merge card item; the PR-3 note follows (lines 341 to 343) |
| G3 | `.dev/issue-96-pr2/plan.md:404` | `noted` | PR-2 residual risk 23; the PR-3 note follows (lines 407 to 409) |
| G3 | `docs/design-proposal.md:3697` | `noted` | English residual risk 4 correction; the pointer on the next line is fixed and the PR-3 correction follows (lines 3703 to 3706) |
| G3 | `docs/design-proposal.md:4100` | `historical` | item (j) of the English PR-2 supplement; still true, because `check_pack` keeps the role values pinned after PR-3; Superseding item |
| G3 | `docs/design-proposal.md:4195` | `noted` | English PR-2 residual risk 23; the PR-3 note follows (lines 4198 to 4201) |
| G3 | `docs/design-proposal.md:4447` | `changed` | the Superseding item of the D-029 PR-3 supplement (English) |
| G3 | `docs/requirements/REQ-009-subagent-model-effort.md:178` | `historical` | source locator that describes the PR-2 card answer I96-IR-P2-C3 (b); Superseding item |
| G3 | `docs/requirements/REQ-009-subagent-model-effort.md:366` | `noted` | PR-2 residual risks; a PR-3 note on the same line |
| G3 | `docs/requirements/log.md:135` | `historical` | append-only log: earlier lines are never rewritten; the PR-3 entry is line 137; Superseding item |
| G3 | `skills/dev-core/deltas.md:68` | `changed` | DL-045: the new PR-3 note in the same row says that DL-046 and the D-029 PR-3 supplement supersede these sentences |
| G3 | `skills/dev-core/references/model-effort-readback.md:614` | `noted` | the PR-2 limit bullet; the PR-3 note in the same bullet (lines 625 to 634) |
| G3 | `.dev/issue-96-pr3/plan.md:404` | `changed` | new text of this plan (the pattern list) |
| G4 | `docs/design-proposal.md:809` | `changed` | Chinese residual risk 4 correction: the pointer now names residual risk 23 (MR99-S-04), and a PR-3 correction on the same line |
| G4 | `docs/design-proposal.md:877` | `historical` | the PR-2 decision not to change the README; PR-3 writes the README section (Superseding item, second sentence) |
| G4 | `docs/design-proposal.md:901` | `noted` | Chinese PR-2 residual risk 23; a PR-3 note on the same line |
| G4 | `docs/design-proposal.md:952` | `changed` | the Superseding item of the D-029 PR-3 supplement (Chinese) |
| G4 | `.dev/issue-96-pr3/plan.md:405` | `changed` | new text of this plan (the pattern list) |
| G5 | `.dev/issue-96-pr2/plan.md:227` | `changed` | new PR-3 note |
| G5 | `.dev/issue-96-pr2/plan.md:340` | `noted` | PR-2 merge card item; the PR-3 note follows (lines 341 to 343) |
| G5 | `.dev/issue-96-pr2/plan.md:341` | `changed` | new PR-3 note |
| G5 | `.dev/issue-96-pr2/plan.md:404` | `noted` | PR-2 residual risk 23; the PR-3 note follows (lines 407 to 409) |
| G5 | `.dev/issue-96-pr2/plan.md:407` | `changed` | new PR-3 note |
| G5 | `docs/design-proposal.md:3704` | `changed` | new PR-3 correction of residual risk 4 (English) |
| G5 | `docs/design-proposal.md:3855` | `historical` | item 12 of the English PR-2 supplement, the decision of card I96-IR-P2-C3 (b); Superseding item |
| G5 | `docs/design-proposal.md:4095` | `historical` | item (i) of the English PR-2 supplement; it gives the plan of PR-2 for the check; Superseding item |
| G5 | `docs/design-proposal.md:4195` | `noted` | English PR-2 residual risk 23; the PR-3 note follows (lines 4198 to 4201) |
| G5 | `docs/design-proposal.md:4198` | `changed` | new PR-3 note |
| G5 | `docs/design-proposal.md:4244` | `changed` | new text of the D-029 PR-3 supplement (English) |
| G5 | `docs/design-proposal.md:4251` | `changed` | new text of the D-029 PR-3 supplement (English), the user's words: the second accepted sentence of the Superseding item, named by card I96-P3-IR2-C1 (a) |
| G5 | `docs/design-proposal.md:4449` | `changed` | the Superseding item of the D-029 PR-3 supplement (English) |
| G5 | `docs/requirements/REQ-009-subagent-model-effort.md:178` | `historical` | source locator that describes the PR-2 card answer I96-IR-P2-C3 (b); Superseding item |
| G5 | `docs/requirements/REQ-009-subagent-model-effort.md:366` | `changed` | the new PR-3 note on the same line |
| G5 | `docs/requirements/REQ-009-subagent-model-effort.md:380` | `changed` | new Issue #96 PR-3 group (implementation review decisions): the second accepted sentence of the Superseding item, named by card I96-P3-IR2-C1 (a) |
| G5 | `docs/requirements/log.md:135` | `historical` | append-only log: earlier lines are never rewritten; Superseding item |
| G5 | `skills/dev-core/references/model-effort-readback.md:614` | `noted` | the PR-2 limit bullet; the PR-3 note in the same bullet (lines 625 to 634) |
| G5 | `.dev/issue-96-pr3/plan.md:84` | `changed` | new text of this plan |
| G5 | `.dev/issue-96-pr3/plan.md:406` | `changed` | new text of this plan (the pattern list) |
| G6 | `docs/design-proposal.md:809` | `changed` | Chinese residual risk 4 correction: the pointer fix and the new PR-3 correction on the same line |
| G6 | `docs/design-proposal.md:847` | `historical` | item 12 of the Chinese PR-2 supplement, the decision of card I96-IR-P2-C3 (b); Superseding item |
| G6 | `docs/design-proposal.md:870` | `historical` | item (i) of the Chinese PR-2 supplement; it gives the plan of PR-2 for the check; Superseding item |
| G6 | `docs/design-proposal.md:901` | `changed` | the new PR-3 note on the same line |
| G6 | `.dev/issue-96-pr3/plan.md:407` | `changed` | new text of this plan (the pattern list) |
| G7 | `.dev/followups.md:73` | `noted` | FU-061 Item column states premise 2; the PR-3 note in the Status column says how it is narrowed |
| G7 | `.dev/issue-96-pr2/plan.md:433` | `noted` | PR-2 Non-goals state premise 2; the PR-3 note after the paragraph (line 437) |
| G7 | `docs/design-proposal.md:3645` | `noted` | English PR-2 split note states premise 2; the PR-3 correction follows (lines 3646 to 3651) |
| G7 | `docs/design-proposal.md:4291` | `changed` | new text of the D-029 PR-3 supplement (English) |
| G7 | `docs/design-proposal.md:4294` | `changed` | new text of the D-029 PR-3 supplement (English) |
| G7 | `docs/requirements/REQ-009-subagent-model-effort.md:364` | `noted` | PR-2 split item states premise 2; a PR-3 note on the same line |
| G7 | `skills/dev-core/deltas.md:69` | `changed` | new row DL-046 |
| G7 | `skills/dev-core/references/model-effort-readback.md:619` | `noted` | the PR-2 limit bullet states premise 2; the PR-3 note in the same bullet (lines 625 to 634) |
| G7 | `.dev/issue-96-pr3/plan.md:408` | `changed` | new text of this plan (the pattern list) |
| G8 | `.dev/followups.md:31` | `noted` | unrelated to the PR-3 check |
| G8 | `.dev/followups.md:73` | `changed` | FU-061: the new PR-3 note names the variables that the check does not detect |
| G8 | `.dev/issue-14-platform-profile/reviews/round-1.md:68` | `noted` | unrelated to the PR-3 check |
| G8 | `.dev/issue-96-pr2/plan.md:433` | `noted` | PR-2 Non-goals state premise 2; the PR-3 note after the paragraph (line 437) |
| G8 | `.dev/issue-96-pr2/plan.md:441` | `changed` | new PR-3 note |
| G8 | `CHANGELOG.md:801` | `noted` | unrelated to the PR-3 check |
| G8 | `CHANGELOG.md:802` | `noted` | unrelated to the PR-3 check |
| G8 | `docs/design-proposal.md:803` | `changed` | Chinese PR-2 split note; a PR-3 correction on the same line |
| G8 | `docs/design-proposal.md:810` | `changed` | Chinese residual risk 5; the PR-3 correction on the same line, with the condition of `IN_REPO` and the relative values (card I96-P3-IR1-C1 (a)) |
| G8 | `docs/design-proposal.md:920` | `changed` | new text of the D-029 PR-3 supplement (Chinese), the decision of card I96-P3-IR1-C1 (a) |
| G8 | `docs/design-proposal.md:923` | `changed` | new text of the D-029 PR-3 supplement (Chinese) |
| G8 | `docs/design-proposal.md:942` | `changed` | new text of the D-029 PR-3 supplement (Chinese) |
| G8 | `docs/design-proposal.md:945` | `changed` | new text of the D-029 PR-3 supplement (Chinese), item 6 of residual risk 23 |
| G8 | `docs/design-proposal.md:3645` | `noted` | English PR-2 split note states premise 2; the PR-3 correction follows (lines 3646 to 3651) |
| G8 | `docs/design-proposal.md:3650` | `changed` | new PR-3 correction |
| G8 | `docs/design-proposal.md:3728` | `changed` | the PR-3 correction of residual risk 5 (English), with the condition of `IN_REPO` |
| G8 | `docs/design-proposal.md:3733` | `changed` | the PR-3 correction of residual risk 5 (English), the relative values (card I96-P3-IR1-C1 (a)) |
| G8 | `docs/design-proposal.md:4280` | `changed` | new text of the D-029 PR-3 supplement (English), the decision of card I96-P3-IR1-C1 (a) |
| G8 | `docs/design-proposal.md:4291` | `changed` | new text of the D-029 PR-3 supplement (English) |
| G8 | `docs/design-proposal.md:4294` | `changed` | new text of the D-029 PR-3 supplement (English) |
| G8 | `docs/design-proposal.md:4398` | `changed` | new text of the D-029 PR-3 supplement (English) |
| G8 | `docs/design-proposal.md:4405` | `changed` | new text of the D-029 PR-3 supplement (English), item 6 of residual risk 23 |
| G8 | `docs/design-proposal.md:4410` | `changed` | new text of the D-029 PR-3 supplement (English), item 6 of residual risk 23 |
| G8 | `docs/design-proposal.md:4414` | `changed` | new text of the D-029 PR-3 supplement (English), item 6 of residual risk 23 |
| G8 | `docs/requirements/REQ-009-subagent-model-effort.md:190` | `changed` | new sources entry of the stop cards I96-P3-IR1-C1 and I96-P3-IR1-C2 |
| G8 | `docs/requirements/REQ-009-subagent-model-effort.md:348` | `changed` | Issue #96 PR-1 residual risks; the PR-3 note on the same line, with the condition of `IN_REPO` and the relative values |
| G8 | `docs/requirements/REQ-009-subagent-model-effort.md:364` | `noted` | PR-2 split item states premise 2; a PR-3 note on the same line |
| G8 | `docs/requirements/REQ-009-subagent-model-effort.md:378` | `changed` | new Issue #96 PR-3 group |
| G8 | `docs/requirements/REQ-009-subagent-model-effort.md:380` | `changed` | new Issue #96 PR-3 group (implementation review decisions) |
| G8 | `docs/requirements/REQ-009-subagent-model-effort.md:381` | `changed` | new Issue #96 PR-3 group (residual risks) |
| G8 | `docs/requirements/REQ-011-security-review-before-commit-push.md:223` | `noted` | unrelated to the PR-3 check |
| G8 | `docs/requirements/log.md:138` | `changed` | new log entry of the implementation review decisions of PR-3 (rounds 1 and 2) |
| G8 | `skills/dev-core/SKILL.md:155` | `noted` | unrelated to the PR-3 check |
| G8 | `skills/dev-core/SKILL.md:190` | `changed` | rule sentence P3-R11 |
| G8 | `skills/dev-core/deltas.md:69` | `changed` | new row DL-046 |
| G8 | `skills/dev-core/references/model-effort-readback.md:483` | `changed` | new PR-3 note on the repository check |
| G8 | `skills/dev-core/references/model-effort-readback.md:490` | `changed` | new PR-3 note on the repository check |
| G8 | `skills/dev-core/references/model-effort-readback.md:493` | `changed` | new PR-3 note on the repository check |
| G8 | `skills/dev-core/references/model-effort-readback.md:498` | `changed` | new PR-3 note on the repository check |
| G8 | `skills/dev-core/references/model-effort-readback.md:620` | `noted` | the PR-2 limit bullet states premise 2; the PR-3 note in the same bullet (lines 625 to 634) |
| G8 | `skills/dev-core/references/model-effort-readback.md:631` | `changed` | the new PR-3 note in the limit bullet |
| G8 | `tests/test_model_effort_readback.py:1581` | `noted` | P3-T1 code or test text (outside the T2 paths); it matches the PR-3 design |
| G8 | `tests/test_model_effort_readback.py:1589` | `noted` | P3-T1 code or test text (outside the T2 paths); it matches the PR-3 design |
| G8 | `tests/test_model_effort_readback.py:1613` | `noted` | P3-T1 code or test text (outside the T2 paths); it matches the PR-3 design |
| G8 | `tests/test_model_effort_readback.py:1619` | `noted` | P3-T1 code or test text (outside the T2 paths); it matches the PR-3 design |
| G8 | `.dev/issue-96-pr3/plan.md:61` | `changed` | new text of this plan (the answer to the stop cards I96-P3-IR1-C1 and I96-P3-IR1-C2) |
| G8 | `.dev/issue-96-pr3/plan.md:257` | `changed` | new text of this plan (implementation review round 1) |
| G8 | `.dev/issue-96-pr3/plan.md:316` | `changed` | new text of this plan (implementation review round 2) |
| G8 | `.dev/issue-96-pr3/plan.md:318` | `changed` | new text of this plan (implementation review round 2) |
| G8 | `.dev/issue-96-pr3/plan.md:347` | `changed` | new text of this plan (residual risk 23, card I96-P3-IR1-C1 (a)) |
| G8 | `.dev/issue-96-pr3/plan.md:350` | `changed` | new text of this plan (residual risk 23, cards I96-P3-IR1-C1 (a) and I96-P3-IR2-C1 (a)) |
| G8 | `.dev/issue-96-pr3/plan.md:354` | `changed` | new text of this plan (residual risk 23, cards I96-P3-IR1-C1 (a) and I96-P3-IR2-C1 (a)) |
| G8 | `.dev/issue-96-pr3/plan.md:409` | `changed` | new text of this plan (the pattern list) |
| G9 | `.dev/followups.md:73` | `changed` | FU-061: the new PR-3 note says how premise 2 is narrowed |
| G9 | `.dev/issue-96-pr2/plan.md:432` | `noted` | PR-2 Non-goals state premise 2; the PR-3 note after the paragraph (line 437) |
| G9 | `README.md:197` | `changed` | new README section (English) |
| G9 | `docs/design-proposal.md:3644` | `noted` | English PR-2 split note states premise 2; the PR-3 correction follows (lines 3646 to 3651) |
| G9 | `docs/design-proposal.md:4472` | `changed` | new text of the D-029 PR-3 supplement (English) |
| G9 | `docs/requirements/REQ-009-subagent-model-effort.md:364` | `noted` | PR-2 split item states premise 2; a PR-3 note on the same line |
| G9 | `docs/requirements/REQ-009-subagent-model-effort.md:375` | `changed` | new Issue #96 PR-3 group |
| G9 | `docs/requirements/REQ-009-subagent-model-effort.md:378` | `changed` | new Issue #96 PR-3 group |
| G9 | `skills/dev-core/SKILL.md:190` | `changed` | rule sentence P3-R11 |
| G9 | `skills/dev-core/deltas.md:69` | `changed` | new row DL-046 |
| G9 | `skills/dev-core/references/model-effort-readback.md:447` | `changed` | new PR-3 note on the repository check |
| G9 | `skills/dev-core/references/model-effort-readback.md:653` | `changed` | new PR-3 limit bullet |
| G9 | `skills/dev-core/references/model-effort-readback.md:663` | `changed` | new PR-3 limit bullet |
| G9 | `skills/dev-core/scripts/model_effort_readback.py:370` | `noted` | P3-T1 code or test text (outside the T2 paths); it matches the PR-3 design |
| G9 | `.dev/issue-96-pr3/plan.md:410` | `changed` | new text of this plan (the pattern list) |
| G10 | `README.md:66` | `changed` | new README section (Chinese) |
| G10 | `docs/design-proposal.md:803` | `changed` | Chinese PR-2 split note states premise 2; a PR-3 correction on the same line |
| G10 | `docs/design-proposal.md:915` | `changed` | new text of the D-029 PR-3 supplement (Chinese) |
| G10 | `docs/design-proposal.md:923` | `changed` | new text of the D-029 PR-3 supplement (Chinese) |
| G10 | `docs/design-proposal.md:941` | `changed` | new text of the D-029 PR-3 supplement (Chinese) |
| G10 | `docs/design-proposal.md:957` | `changed` | new text of the D-029 PR-3 supplement (Chinese) |
| G10 | `.dev/issue-96-pr3/plan.md:411` | `changed` | new text of this plan (the pattern list) |
| G11 | `skills/dev-core/references/model-effort-readback.md:436` | `noted` | the PR-1 sentence on the path form; the PR-3 note follows (lines 438 to 499) and says when it still holds |
| G11 | `skills/dev-core/references/model-effort-readback.md:486` | `changed` | new PR-3 note |
| G11 | `.dev/issue-96-pr3/plan.md:412` | `changed` | new text of this plan (the pattern list) |
| G12 | `docs/design-proposal.md:810` | `changed` | Chinese residual risk 5; a PR-3 correction on the same line (d4 D-06, d5 section 4) |
| G12 | `docs/design-proposal.md:949` | `changed` | new text of the D-029 PR-3 supplement (Chinese) |
| G12 | `.dev/issue-96-pr3/plan.md:413` | `changed` | new text of this plan (the pattern list) |
| G13 | `docs/design-proposal.md:1093` | `noted` | English section 4 note of PR-2; the PR-3 note follows (lines 1097 to 1100) |
| G13 | `.dev/issue-96-pr3/plan.md:414` | `changed` | new text of this plan (the pattern list) |
| G14 | `.dev/issue-96-pr3/plan.md:415` | `changed` | new text of this plan (the pattern list) |
| G15 | `.dev/issue-96-pr3/plan.md:416` | `changed` | new text of this plan (the pattern list) |
| G16 | `.dev/followups.md:21` | `noted` | unrelated to the PR-3 check |
| G16 | `.dev/followups.md:43` | `noted` | unrelated to the PR-3 check |
| G16 | `.dev/followups.md:44` | `noted` | unrelated to the PR-3 check |
| G16 | `.dev/followups.md:73` | `noted` | FU-061 Item column states premise 2; the PR-3 note in the Status column says how it is narrowed |
| G16 | `.dev/issue-14-platform-profile/reviews/round-1.md:46` | `noted` | unrelated to the PR-3 check |
| G16 | `.dev/issue-66-user-level-install/plan.md:47` | `noted` | unrelated to the PR-3 check |
| G16 | `.dev/issue-69-readonly-tools-check/plan.md:38` | `noted` | unrelated to the PR-3 check |
| G16 | `.dev/issue-96-pr2/plan.md:431` | `noted` | PR-2 Non-goals state premise 2; the PR-3 note after the paragraph (line 437) |
| G16 | `CHANGELOG.md:481` | `noted` | unrelated to the PR-3 check |
| G16 | `docs/design-proposal.md:1949` | `noted` | unrelated to the PR-3 check |
| G16 | `docs/design-proposal.md:3605` | `noted` | unrelated to the PR-3 check |
| G16 | `docs/design-proposal.md:3643` | `noted` | English PR-2 split note states premise 2; the PR-3 correction follows (lines 3646 to 3651) |
| G16 | `docs/design-proposal.md:4108` | `noted` | unrelated to the PR-3 check |
| G16 | `docs/design-proposal.md:4290` | `changed` | new text of the D-029 PR-3 supplement (English) |
| G16 | `docs/requirements/REQ-009-subagent-model-effort.md:354` | `noted` | unrelated to the PR-3 check |
| G16 | `docs/requirements/REQ-009-subagent-model-effort.md:364` | `noted` | PR-2 split item states premise 2; a PR-3 note on the same line |
| G16 | `docs/requirements/REQ-021-platform-profile.md:23` | `noted` | unrelated to the PR-3 check |
| G16 | `docs/requirements/REQ-028-user-level-read-grant.md:154` | `noted` | unrelated to the PR-3 check |
| G16 | `skills/dev-core/deltas.md:38` | `noted` | unrelated to the PR-3 check |
| G16 | `skills/dev-core/deltas.md:67` | `noted` | unrelated to the PR-3 check |
| G16 | `skills/dev-core/deltas.md:68` | `noted` | unrelated to the PR-3 check |
| G16 | `skills/dev-core/deltas.md:69` | `changed` | new row DL-046 |
| G16 | `skills/dev-core/references/model-effort-readback.md:618` | `noted` | the PR-2 limit bullet states premise 2; the PR-3 note in the same bullet (lines 625 to 634) |
| G16 | `tests/test_model_effort_readback.py:1341` | `noted` | P3-T1 test file; a PR-2 test comment, unrelated to the PR-3 check |
| G16 | `.dev/issue-96-pr3/plan.md:417` | `changed` | new text of this plan (the pattern list) |

## Read-back records

The read-back result lines of the nodes, reviews and scans of this plan
are in the PR gate record comment, not in this file: they carry agent IDs.

## Non-goals

FU-063 (a deterministic check of the bound base literal, residual risk 24;
card I96-IR2-P2-C2 (b)), FU-062, FU-050 and FU-053 to FU-057,
provider-specific model IDs, a wider ID character set, `agents/*.md`, the
`Role:` field of `task-brief.md`, and any ban on edits of an installed
configuration file.
