# Issue #96 PR-1 plan: model configuration file and read-back classification (`Part of #96`)

- Objective: GitHub Issue #96 (body and comments 1 to 3), PR-1 of two:
  one configuration file, `skills/dev-core/model-config.json`, holds the
  model families with tiers, the observed model IDs and the roles; the
  read-back script classifies a recorded model ID through it, so that a
  newer model version counts with a warning instead of stopping every
  review and scan; the rule and record files only get added sentences.
- Rigor `strict`. Reason (R-RIG-1, re-assessed at Discover as R-RIG-2
  says): a change to a security rule (R-DEL-2, the read-back gate), to
  pack rule text, and to an executable that gates commits; the R-DEL-2
  floor applies to every node.
- Base: `main` `b51848bb27f943783c5eeb28aaebe7b4d0803ae9`, branch
  `issue-96-model-config`.
- Spec: design rev 9 of 2026-11-02, which gives the differences against
  the full PR-1 design rev 8 (where they differ, rev 9 wins), with the gate
  dry run. The design files are in the session notes, which are not in the
  repository; Issue #96 comment 3 states the scope that they settle.
- Method (card I96-R5-C1 (a)): no word of a rule or record file in scope
  that exists at the base is removed; superseded sentences stay and get a
  sentence that they no longer apply from Issue #96 on. A deterministic
  gate checks part of it; the reviewers checked the rest with a
  character-level diff, and the tree-identity checks keep that tree (see
  Gate).

## Source trace (dev-plan step 2)

Sources: the Issue #96 body; comment 1 (scope and threat model); comment 2
(items handed over by the PR #97 merge); comment 3 (scope update with the
design decisions); D-028 and its residual risks 2, 3 and 8; DL-042 and
DL-043; REQ-009; FU-020, FU-021, FU-049, FU-056 and FU-057; and these
user answers (Claude Code session, the user's words in the orchestrator
session, relayed):

- Issue #96 body (2026-10-31): 「我的想法是，claude是固定的。Opus/sonnet/Haiku 版、次版這些都可以換。因為模型名稱本來就會變、版號也會變。最好是有個文件做設定，負責任務編排、審查、程式設計、文件撰寫、…等agent或任務的模型是什麼，推理程度允許範圍。以後模型名稱變了、改版，只要來改這個設定檔就行了，剩下的就是代位詞來查表套用。」
  and 「只要是在這裡透過正式流程實際驗證過、並釋出配置都有依據對吧？但如果用戶自己改了，那就自己負責」:
  one configuration file; the released file rests on the pack's own
  process, and a user who edits it owns the result.
- Comment 1 (2026-10-31):
  「我覺得這樣的想法邏輯上沒錯，但實務上有問題，這有點像是要追求bug free一樣，想防止所有的例外。但這是不可能的，模型、版本這些本來就是可以替換的，我們在設計這個技能包的當下依照規格設計了所有的流程，驗證也都做過了。新版模型出來也經過驗證，但釋出後其實無法防止有人惡搞，故意把模型換掉。如果有人故意把sonnet拿來當Opus用，那也是他個人的問題，他得為他的行為負責」
  and
  「對，你身為任務編排的責任盡到了、子session的任務盡到了就行，用戶惡搞，那就是用戶自己要負責。如果用戶在無法確認的狀況下，其實可以要求Agent先確認再修改配置，而不是自己亂搞」:
  the gate guards against agent and host errors; item 2 let an
  unrecognized model ID count with a warning (narrowed below).
- Comment 2 (2026-11-01): 「MR97-C2 b，在 dev-gate 改好前每次 merge 都照 b；FU-057 併入 #96」
  and 「MR97-C3 a」: the `dev-gate` wording part of FU-057 is in this Issue.
- 「I96-C1 c，C2 b，C3 a，C4 a，C5 a，C6 a，C7 a，C8 b，C9 a，C10 a」
  (2026-11-01): C2 (b) the warning is shown without waiting; C3 (a) it
  also covers the R-REV-9 scans; C5 (a) the `check` mode; C6 (a) the merge
  readiness text; C7 (a) the `light` exception ends; C10 (a) a D-005
  follow-up for a new generation or family; C1 (c) is replaced by R2-C1
  (a); C8 and C9 go to PR-2.
- 「C4 a＋條件，C9 a＋Fable 等級 4 ，這是你之前建議的2點嗎？是的話我同意」
  (2026-11-01), with the orchestrator's relayed answer 「是」: the two
  points that the orchestrator had proposed, as design rev 3 and design
  cards rev 3 record them (relayed, not the user's words): the required
  reviews and R-REV-9 scans keep a floor at tier 3 / `xhigh` that the
  configuration cannot lower; Fable is at tier 4 from the official
  documentation, after `max` at Opus in the ladder, and Issue #96
  supersedes FU-020. D-029 records this source (R5-S-14).
- 「I96-C11 a」 (2026-11-01): that floor covers every R-REV-9 scan, deep
  review and security review; routine and `light` reviews keep today's
  values (PR-2 writes the tier rules; in PR-1 `check_pack` pins the roles
  at today's values).
- 「C8 改為：設定檔是唯一來源，路由表只標角色名、不寫數值；I96-C12 a＋停用規則；不加技能」
  (2026-11-01): C8 is PR-2; C12 (a) `check_pack` pins each family tier
  (its pin or null); no new skill.
- 「I96-R2-C1 a，R2-C2 a，R2-C3 a，R2-C4 a，R2-C5 a」 (2026-11-01): the
  classification with the `version` class; the main session's own floor
  check unchanged; the `orchestration` role stays; only the observed Opus
  ID is listed; two PRs.
- 「I96-R3-C1 a，R3-C2 a；不支援 Bedrock 等 provider 專屬 ID，列為 non-goal（需要的人自行 fork），ID 字元集不放寬」
  (2026-11-01): the effort order stays fixed; a mechanical check; provider
  IDs are a non-goal, and the ID character set is not widened. This
  reverses "another provider's ID … counts" of comment 1 item 2.
- 「I96-R4-C1 a」 (2026-11-02): the R-DEL-2 change of PR-1 is kept to a
  minimum, and the rewrite in tier numbers moves to PR-2.
- 「I96-R5-C1 a，R5-C2 a（實作審查若在 gate 或附加句找到新問題，照 R-VER-2 停）」
  (2026-11-02): no word is removed in PR-1 (this changes how C7 (a) is
  done: the removal moves to PR-2); no sixth design review round.
- 「I96-IR1-C1 b」 (2026-11-02): the gate script and its SHA-256 do not
  change; this plan states what the gate proves and what it does not; the
  commit and the merge keep the reviewed tree by tree identity (see Gate
  and Implementation review round 1).

From the design reviews of rounds 1 to 5, not from the user's words: the
other wording of the rule sentences of design rev 9 section 1 (finding IDs
in rev 9).

## PR-1 files

The gate's `--files` list has one `<status><TAB><path>` line for each row.
It must equal the actual change of the branch; when an implementer does not
change a listed file, the main agent corrects the list before the gate run
and records why.

| Status | Path | Task | Content checked by the gate |
| --- | --- | --- | --- |
| A | `skills/dev-core/model-config.json` | T1 | no |
| M | `skills/dev-core/scripts/model_effort_readback.py` | T1 | no |
| M | `scripts/check_pack.py` | T1 | no |
| M | `tests/test_model_effort_readback.py` | T1 | no |
| M | `tests/test_core_checks.py` | T1 | no |
| M | `skills/dev-core/SKILL.md` | T2 | yes |
| M | `skills/dev-core/references/model-effort-readback.md` | T2 | yes |
| M | `skills/dev-core/deltas.md` | T2 | yes |
| M | `skills/dev-gate/SKILL.md` | T2 | yes |
| M | `skills/dev-review/SKILL.md` | T2 | yes |
| M | `skills/dev-review/references/review-report.md` | T2 | yes |
| M | `docs/design-proposal.md` | T2 | yes |
| M | `docs/requirements/REQ-009-subagent-model-effort.md` | T2 | yes |
| M | `docs/requirements/log.md` | T2 | yes |
| M | `CHANGELOG.md` | T2 | yes |
| M | `.dev/followups.md` | T2 | yes |
| A | `.dev/issue-96-model-config/plan.md` | T2 | no |

## Rule sentences (design rev 9 section 1)

One scripted run inserts each sentence at its anchor, word for word, and
asserts each anchor; each sentence then appears exactly once.

| ID | File | Anchor (base) | Next sentence (back reference checked by hand) |
| --- | --- | --- | --- |
| S1 | `skills/dev-core/SKILL.md`, R-DEL-2 read-back bullet | after "`git --no-replace-objects cat-file blob <full base ID>:skills/dev-core/scripts/model_effort_readback.py \| python3 -I - subagent …`." | "The main agent writes the full base ID in this command as a literal …": "this command" now follows the S1 command as well; both forms need the literal, so the reading does not loosen |
| S2 | same bullet | after "The `recorded` field is the alias and the level of that `OK`, `PASS` or `BELOW` line." | "Every other outcome is `unknown` …": "other" now also excludes a `WARN` line, as S2 says |
| N1 | same bullet | after "… is data and can only end the exception." | "Once a trigger applies, …": no back reference to N1 |
| N2, S5 | same bullet | after "Every project that installs the pack stops at the same time." | "A host whose dispatch tool has no model or effort parameter …": no back reference |
| S6 | `skills/dev-gate/SKILL.md`, merge readiness row | before the final ` \|` of the row | end of the row |
| N3 | `skills/dev-gate/SKILL.md`, blocker list | end of the line "… while R-DEL-2 lets it skip the gate;" | next blocker bullet |
| S7 | `skills/dev-gate/SKILL.md`, Output | end of the Read-back line | next Output line |
| N4 | `skills/dev-review/SKILL.md` | end of the line "… R-DEL-2 says when that exception holds." | next paragraph |
| N5 | `skills/dev-review/references/review-report.md` | end of the Read-back template line | next template line |
| FU-049 note | `.dev/followups.md` | before the final ` \|` of the FU-049 row | end of the row |

Change after design review round 5 that the implementation review checks
by name: S2 has "where `<digits>` is one or more groups of digits joined by
hyphens" (from the pre-post scan of Issue comment 3, I96-C3-S-01).

## Task graph

| Task | Agent | Paths | Requested | Recorded | Effective |
| --- | --- | --- | --- | --- | --- |
| T1: configuration file, validator, classification, `--config-base`, `check`, `check_pack` pins, tests | `dev-implementer` | the T1 rows above | `opus`/`high` | main agent fills in (R-DEL-2); not filled in here: see the PR #98 merge gate record (MR98-M-02) | `unknown` |
| T2: rule sentences (one scripted run), reference notes, records, this plan | `dev-implementer` | the T2 rows above | `opus`/`high` | main agent fills in (R-DEL-2); not filled in here: see the PR #98 merge gate record (MR98-M-02) | `unknown` |

Why `opus`/`high`: the implement and docs role at the `strict` tier; the
R-DEL-2 floor applies (security-rule and public-contract text). T1 and T2
run at the same time in one worktree with disjoint paths. After both:
`scripts/check_pack.py`, `scripts/verify_core.py`,
`scripts/check_core_coverage.py` and the unit tests; the gate on the
working tree; the implementation review; the commit scan, the commit, the
gate on the committed head, the push scan with the PR text, the push, the
PR (`Part of #96`) and the ready-for-Merge-Review card.

## Gate

- Script: outside the branch and outside the pack, SHA-256
  `8e1bdbd442ca302d9c072711a819d485bf1ba33890a98127df2cdcc084091a9a`,
  checked before each run. The SHA-256 is also in the Issue #96 scope
  comment. The implementation review gets its full text.
- Inputs: `--base` (the bound base, found with `git merge-base`, a full
  ID), `--head <full ID>` after the commit (the deciding run) or
  `--worktree` before it (new files added with `git add -N` first), and
  `--files` (the list above).
- Checks, with `LC_ALL=C` and `git --no-replace-objects -c
  core.quotePath=false -c diff.relative=false`:
  1. The `--name-status -z --no-renames --no-relative` file list equals
     the `--files` list, statuses included; a deletion or an unexpected
     path fails.
  2. The rows above marked "no" are not content-checked.
  3. Every other file: every base line maps, in order, to its own head
     line with the same leading whitespace, and the tokens of the base line
     (`[A-Za-z0-9_]+` or one other non-space character) are a subsequence
     of the tokens of the head line; a blank base line maps only to an
     equal line.
  4. The head has more tokens than the base, and no NUL.
- What the gate proves (design rev 9 section 8, after card I96-IR1-C1
  (b); facts, from the probes of implementation review round 1):
  - no alphanumeric token of a file in scope is removed;
  - every base line maps, in order, to its own head line with the same
    leading whitespace;
  - a split or joined line, a changed indent and a removed blank line
    fail;
  - the file list equals the `--files` list, statuses included.
- What the gate does not catch (IR1-D-01, IR1-D-02, IR1-S-01, IR1-S-03):
  - an insertion glued to a word, for example `opus` → `opus-mini` or
    `R-DEL-2` → `R-DEL-2.1`: a space-separated word of the base is gone,
    but each of its tokens is still there;
  - a space inserted at a word boundary;
  - an inserted blank line, or an inserted marker at the start of a line;
  - a change of whitespace only inside a line, for example `- ` → `-`,
    LF → CRLF, or a space → NBSP;
  - an old sentence wrapped in `<!-- -->` or in a code fence.
- Why these cases are accepted as residual risk (residual risk 13; this
  list of what the gate does not catch comes from card I96-IR1-C1 (b), not
  from D-029, whose item 13 only says "the limits of the gate"): they
  are mostly deliberate tampering, which is outside the threat model of
  Issue #96 comment 1 (the gates guard against agent and host errors, not
  against deliberate misuse). The errors that an agent realistically
  makes fail the gate: a dropped clause, or a changed word such as `high`
  → `higher`.
- Other safeguards (card I96-IR1-C1 (b), the user's words in the
  orchestrator session, relayed: 「I96-IR1-C1 b」):
  - Fact: two implementation reviewers (the deep review and the Security
    Diff Scan of implementation review round 1) checked the tree of
    implementation review round 1 (diff SHA-256
    `602b53e3ea4fd91a3364a957fce17319df534f82a50fbd17d37bb4be3d47e8b2`)
    with a character-level diff. Every change in the 11 gated files is a
    pure insertion, and the 4 rule files equal the base plus the 10
    sentences of design rev 9 section 1 (IR2-D-02).
  - Tree identity (design rev 9 section 9, IR2-D-01, which corrects
    section 8): the earlier form, the SHA-256 of `git diff <base> --binary`
    before and after the commit, compares the base with the working tree,
    not with the commit, so it is not a check of the commit. The steps:
    1. Before the commit: the main agent stages the 17 files by explicit
       path; the SHA-256 of `git diff --cached <base> --binary` must equal
       the hash of the last reviewed working tree, and
       `git diff --binary` (the working tree against the index) must be
       empty.
    2. After the commit: the SHA-256 of
       `git diff <base> <commit> --binary` (the two-commit form) must
       equal that hash, and `git status --porcelain --untracked-files=no`
       must be empty; the main agent records the tree ID,
       `git rev-parse <commit>^{tree}`.
    3. Gate: the gate runs again with `--head <commit>` (the deciding
       run).
    4. Merge: the merging session checks that
       `<Merge Review head>^{tree}` equals the recorded tree ID.
  - Any later fix round that changes a gated file needs a reviewer's
    character-level pure-insertion check, written in the review brief; the
    gate alone is not enough. This holds for the round that corrects this
    plan, because it adds a note to the FU-061 row of `.dev/followups.md`.
    That round was fix round T3: the review of that round (IR2) checked
    its FU-061 note (1047 characters inserted in a gated file) character
    by character (IR2-D-02).
- Output: one `PASS` or `FAIL` line for each file with its path in the
  repository, then `GATE PASS` (exit 0) or `GATE FAIL` (exit 1); exit 2 on
  an error. No git stderr and no content.
- Runs: after the implementers hand in (`--worktree`), before each
  implementation review round, after the commit (`--head`, the deciding
  run), and in the merging session on the Merge Review head.
- Dry run before the implementation, on a scratch clone at the base with
  the rev 9 section 1 insertions:

  | Case | Expected | Result |
  | --- | --- | --- |
  | 1. insertions only, `--worktree` | PASS | `GATE PASS`, exit 0 |
  | 2. as 1, with `post,` removed from "No commit, push, post or merge proceeds" | FAIL | `GATE FAIL`, exit 1 |
  | 3. as 1, with line 190 split before "Required reviews and scans (Issue #95):" and a blank line between | FAIL | `GATE FAIL`, exit 1 |
  | 4. as 1, committed, `--head <40 digits>` | PASS | `GATE PASS`, exit 0 |
  | 5. `--head` with a 12-digit abbreviation | ERROR | `GATE ERROR not a full object ID`, exit 2 |

  A second dry run after the S2 `<digits>` change gave the same results
  for cases 1 to 3; the script did not change.
- Adjustment found by the dry run: the git word diff reported removed
  segments for case 1, a pure insertion inside a long line (also with
  `--minimal`, patience and histogram), so the gate does not use it; the
  line-by-line token subsequence check (3) takes its place. That check is
  weaker than the word diff, not stricter: the word diff of C0 to C2 finds
  an insertion glued to a word, and check (3) does not (IR1-D-01). The
  implementation review checks this adjustment by name.
- Limits: the gate proves only what "What the gate proves" lists. It does
  not show that an added sentence does not loosen a rule or that it sits
  in the right place; the reviews cover both. Code, tests, `check_pack`,
  the configuration file and this plan are covered by tests and reviews.

## Design review round 6

Skipped by the user's decision R5-C2 (a). The implementation review (a
deep review and a Security Diff Scan, `opus`/`xhigh`, both read back)
covers it: the added sentences (S2 by name), the gate script in full and
its dry run, and the code of the script and the validator. A new problem
in the gate or in an added sentence stops the work with a decision card
(R-VER-2); other findings go through the usual fix rounds.

## Implementation review round 1

A deep review and a Security Diff Scan, `opus`/`xhigh`, both read back
with `PASS`, on a working tree with a diff SHA-256 of `602b53e3…47e8b2`
(17 files). The deep review found 0 MUST-FIX, 1 SHOULD-FIX and 1 NIT; the
scan found 0 MUST-FIX, 1 SHOULD-FIX and 6 NIT. The gate findings stopped
the work (R-VER-2); the user answered 「I96-IR1-C1 b」.

| ID | Finding | Disposition |
| --- | --- | --- |
| IR1-D-01 | An insertion glued to a word passes the gate (`opus` → `opus-mini`, `R-DEL-2` → `R-DEL-2.1`) | Accepted as residual risk for PR-1 (see Gate); a stronger gate is Deferred to FU-061 |
| IR1-D-02 | An inserted blank line passes the gate; the plan said otherwise | Accepted as residual risk for PR-1, and the plan corrected; a stronger gate is Deferred to FU-061 |
| IR1-S-01 | An inserted blank line in a table or a list item, or a whitespace-only change inside a line, passes the gate | Accepted as residual risk for PR-1; a stronger gate is Deferred to FU-061 |
| IR1-S-02 | An error line of the gate can print the text of an operating system error, which can hold a private path | Accepted as residual risk: the gate script does not change under card I96-IR1-C1 (b). Conditions: a raw `GATE ERROR` line is never pasted into a posted record, and the pre-post scans back this up; the PR-2 gate design takes over "print fixed error text, never exception text" |
| IR1-S-03 | An old sentence wrapped in `<!-- -->` or in a code fence passes the gate | Accepted as residual risk for PR-1; a stronger gate is Deferred to FU-061 |
| IR1-S-04 | The N2 wording is wider than the code: a `version`-form Fable ID and a record that mixes two families still stop the reviews (fail closed) | Deferred to FU-061; the added sentence does not change in PR-1 |
| IR1-S-05 | The path form uses the literal normalized path, so with a symlinked skill directory it can read another copy of the configuration file (inference) | Deferred to FU-061, and accepted as residual risk for PR-1; the code does not change |
| IR1-S-06 | The static test does not catch an aliased call such as `P = subprocess.Popen` | Deferred to FU-061 |
| IR1-S-07 | The DL-042 and DL-043 notes "a `WARN` line counts like a `PASS` here" lack the conditions; R-DEL-2 and DL-044 state them | Deferred to FU-061 |
| Deep review residual items | The N1 wording, the FU-060 wording, the form of `WARN` in short summaries, and the Owner column ("maintainer", which both reviewers accept) | Deferred to FU-061 |
| Implementation review round 2 (IR2) | D-01 (MUST-FIX): the tree-identity check compared the working tree, not the commit; D-02 (NIT): which tree the character-level check covers, and the check of the FU-061 note of fix round T3; D-03 (NIT): the widened text of residual risk 13 is not from D-029 | D-01 Fixed by T4; D-02 Fixed by T4; D-03 Fixed by T4 |

## Residual risks

D-029 gives them in both languages; the wider wording of item 13 here
comes from card I96-IR1-C1 (b), and D-029 item 13 only says "the limits of
the gate":

1. The `version` class counts with a warning, older generations (for
   example `claude-opus-4-8` for `opus`) and Claude-style names that are
   not the real model included; it infers the family from the ID, while
   the official documentation advises reading `line`, which a transcript
   does not have.
2. Provider IDs are a non-goal: on a provider host every review, scan and
   floor dispatch stops; only a fork helps.
3. A new first-party ID without the `version` form also stops (the dead
   end).
4. A user can change the tiers of their own copy; in this repository
   `check_pack` pins them, and the alias order and same-family checks keep
   a wrong tier from making a lower alias count when the script that runs
   is the copy at the bound base.
5. An agent with Bash or another process can change what lies outside the
   base (D-027); the two base literals are checked by the main agent only;
   a wrong literal trusts the file of that commit (a wrong tier is
   stopped, a wrong ID list is not); a run by path inside the repository
   of the change reads the change's own file.
6. The Sonnet, Haiku and Fable IDs are not observed, so `light` reviews
   and explores carry a warning, and a Sonnet ID without the `version`
   form stops the `light` review (FU-060).
7. The script starts `git`: `PATH`, the environment, the Git
   configuration and a lazy fetch are the trust surface of the outer
   command.
8. The strict open by path can stop every read-back in a managed
   installation (not verified).
9. A plugin update can replace an edited file or keep one of an older
   schema (`STOP CONFIG`; not verified).
10. This repository trusts the file at the base when the base passed
    `check_pack`; whether a merge requires CI is not verified.
11. One PR can change the file, the validator and the pins together; the
    guard rests on review.
12. After the merge and before a session reloads the pack, a call of the
    old rule gets `BAD_ARGS` (fail closed).
13. The limits of the gate (above: what the gate does not catch, and the
    limits). The part "what the gate does not catch" comes from card
    I96-IR1-C1 (b), not from D-029 (IR2-D-03).
14. The internal time limit is 20 seconds; with a shorter outer limit,
    `git` can be left running (fail closed).
15. Between PR-1 and PR-2 the rules still name families.
16. The rules keep the sentences that are declared superseded until PR-2;
    a reader has to take the added sentence (FU-061).
17. A `STOP CONFIG` merged on a base stops every read-back until the user
    fixes it outside the agent's work.
18. The gate script is outside the branch, so the merging session needs
    it, or a script with the same SHA-256.
19. The content of new files is checked by review only.
20. The script does not compare its own code with the copy at
    `--config-base` (FU-062); that the two literals are the same is
    checked by the main agent only.

## Changeover after the merge of PR-1

1. Each session that reads back reloads the pack or starts again; until
   then, a call of the old rule gets `BAD_ARGS` (fail closed).
2. For each open branch whose base does not hold the configuration file,
   the read-back outcome is `unknown`; the main agent stops and asks the
   user and proposes a rebase or merge onto a base that holds the file
   (R-AUTH-3); the reviews of the new head are new dispatches.
3. Smoke test: one `dev-explorer` dispatch at `opus`, read back with the
   new call form (`--config-base` with the literal base ID). When it does
   not pass, the main agent stops and asks the user with the facts.
4. Then the PR-2 design (FU-061).

## Read-back records

Not copied into this plan (MR98-M-02, deferred to Issue #96 PR-2 by the
PR #98 merge). The PR #98 merge gate record comment,
https://github.com/jeffery777/claude-dev-skills/pull/98#issuecomment-6570747634,
gives the read-backs of the merging session (the Merge Review, the
Security Diff Scan of the head and the R-REV-9 merge readiness scan) with
their call form, result lines and exit codes; the Recorded column of the
task graph points here.

## Non-goals

PR-2 work (the tier-number rules, role-only tables, the removal of the
superseded sentences, the FU-020 status and the FU-049 status word),
`dev-deliver`, the routing tables, `agents/*.md`, the README, `dev-retro`,
REQ-026, provider-specific model IDs, a wider ID character set, and the
work of FU-059 to FU-062.
