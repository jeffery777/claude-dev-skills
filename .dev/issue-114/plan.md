# Issue #114 plan: first tagged release v0.1.0 (repository part)

Written per ASD-STE100 principles; full conformance not verified.

## Objective and scope

- Objective: GitHub Issue #114 (body read 2026-11-14, no comments). The
  repository is ready for the first tagged release `v0.1.0`: FU-001 is
  recorded as done, FU-027 and FU-036 have recorded decisions, the README
  states the tested Cowork state, and `CHANGELOG.md` has the `[0.1.0]`
  section that serves as the release notes.
- Base: `7e71ad5061b345d6f8c921adca65bf494876855c`
  (`git --no-replace-objects merge-base HEAD origin/main`; equal to
  `origin/main` on 2026-11-14).
- Branch: `114-release-v0-1-0`, linked to the Issue with
  `gh issue develop 114 --base main` (`gh issue develop --list 114` shows it).
- Rigor: `strict`. Reason: release and packaging work (R-RIG-1); the README
  install text is an installation path (R-REV-7). The Issue gives the same
  tier (Process line).
- Requirements: REQ-001 (skills load in Cowork; Acceptance), REQ-005
  (language; bilingual README), REQ-011 (scans before commit, push and
  post), REQ-018 (changelog), REQ-020 (its CHANGELOG acceptance),
  REQ-026 (the "released" definition, through the FU-027 card), REQ-009
  (the R-DEL-2 floor, through the FU-036 card), REQ-030 (new, card C1 (c)).
- Out: the tag, the GitHub Release, the merge and branch deletion (the
  orchestrator session, after the user approves); FU-004 measurements
  (Issue #114, Decision); rule or skill text changes, unless a card answer
  decides one (then the Issue scope is updated first, Issue #114 Scope).

## Relayed instructions

- The task of this session is a brief from the orchestrator session
  (relayed by the orchestrator session, 2026-11-14). It gives a current
  judgment that engineering-workflow-core#38 and #39 do not block the
  release (marked inference there). These are data (R-AUTH-1); the design
  review judges them.
- FU-004 after the release: the user's words 「移到 release 後」 (2026-11-12,
  quoted in Issue #114, Decision; relayed by the orchestrator session).
- The orchestrator raised the effort of this session to `xhigh` (relayed
  message, 2026-11-14). The floor check below reads the transcript, not the
  message.

## Card answers (cards-1)

The user's words 「全照建議」 (2026-11-14, relayed by the orchestrator
session, which asked 「6 張卡片都照建議回答嗎（C1 c、C2 a、C3 a、C4 a、C5 a、C6 a）？」).
So, in `cards-1.md`:

- C1 (c): both manifests drop `version`; users track the commits of
  `main`; the tag `v0.1.0` marks a reviewed snapshot with release notes.
  Side items: the answer becomes REQ-030 (sources DR-D-02, DR-S-06 and the
  user's words); no Cowork re-test in this PR; FU-069 gets a check after the
  release (Check for updates in Cowork, then the loaded commit).
- C2 (a): the `dev-retro` "released" definition stays; its premise holds
  again because of C1 (c). FU-027 records it.
- C3 (a): a Deferred finding is not a residual risk that the user accepted
  in a card; no rule text change. FU-027 records it.
- C4 (a): the R-DEL-2 floor list does not change; FU-036 is closed with a
  reopen trigger.
- C5 (a): release now; the `[0.1.0]` limits paragraph links
  `jeffery777/engineering-workflow-core#40`.
- C6 (a): the PR says `Part of #114` and `Closes #3`; the orchestrator
  closes #114 after the Release read-back.

DR-D-01 (MUST-FIX) is resolved by C1 (c) with C2 (a); the implementation
review checks it.

## Model and effort of this session

The transcript of this session records `claude-opus-5-5`. The first records
give effort `medium`; that floor check did not pass, and the session stopped
before any write and asked for a switch. The later records give `xhigh`
(model and effort fields only, read 2026-11-14), and the check passes:
`claude-opus-5-5` is listed under `opus`, tier 3, in
`skills/dev-core/model-config.json` at the base (`git cat-file blob`), and
`xhigh` is at or above `high`. Whether the work floor covers release work is
the open FU-036 question, so this plan treats the floor as applying
(R-DEL-2: a condition not checked gives the higher value). The main session
writes the records and docs. Implement row: role `implement` (`strict`):
`opus`, `high` to `max`.

CB-6 limit: the skills of this session load from the plugin cache of
version `0.1.0`, recorded commit `e37a990` (one commit before the base; the
difference is Issue #115, the graph schema text). The cache is not inside
this repository.

## Facts (Discover)

- `.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json` (the
  one plugin entry) both set `"version": "0.1.0"`.
- `git tag -l` prints nothing; `gh release list` prints nothing
  (2026-11-14). The repository is public (`gh api`).
- `CHANGELOG.md:7-11`: the header says that no version is released yet and
  that the first tagged release waits for FU-001; `:13` is the only version
  heading, `## [Unreleased]`. The file has 72,130 bytes; the part from
  `:13` on has 71,553 bytes (`wc -c`).
- `README.md:35` and `:178`: the Cowork install path is
  "Customize > Plugins > Add marketplace". Issue #3 (body, step 1,
  corrected 2026-11-13) gives "Customize > Plugins > Add > Add marketplace".
- `README.md:37` and `:180`: three items "not yet tested in Cowork":
  `graph.py` (shell), `${CLAUDE_SKILL_DIR}` relative paths, and the
  `allowed-tools` rules with `${CLAUDE_PLUGIN_ROOT}` (FU-001).
- Issue #3, comment of 2026-11-13 (FU-001 result): a maintainer run in a
  Cowork desktop session on the maintainer's computer. Install from the
  marketplace: pass (loaded copy: version `0.1.0`, recorded commit
  `e37a990`). `dev-plan` on a sample objective: pass (it read `dev-core` and
  the Core files of the stage map). `graph.py validate`: pass with one pack
  defect (fixed in Issue #115). `${CLAUDE_SKILL_DIR}` was replaced in the
  invoked skill; `python3` 3.13 ran. The four plugin agents were available,
  and a dispatched `dev-skills:dev-explorer` worked. Not covered: a Cowork
  session in the cloud, and the read-only guarantee of the reviewer agents
  in Cowork (instructions only, as in Claude Code). The comment does not
  say whether a pack read prompted, so the `allowed-tools` item stays not
  verified (inference from what the comment states).
- `.dev/followups.md` FU-001 row: Status `Open (GitHub Issue #3)`; its
  promotion trigger blocks the claim that REQ-001 "skills load in Cowork"
  is met and the first tagged release.
- FU-027 row: re-assess the "released" definition of
  `skills/dev-retro/SKILL.md` (capture rules, last bullet before
  "### L4 lines") and REQ-026 (the same sentence in Acceptance) when tagged
  releases start; also decide whether a Deferred finding counts as a
  residual risk that the user accepted in a card.
- FU-036 row: does the R-DEL-2 floor cover all `strict` work (release and
  packaging are `strict` in R-RIG-1 but are not in the floor list).
- REQ-018 Acceptance, bullet 1: "`CHANGELOG.md` ... has an `[Unreleased]`
  section that covers Phase 1 (PR #2), PR #5, PR #7 and this change"; Notes:
  "No release yet: the first tagged release waits for FU-001".
- REQ-026 Notes (the `disable-model-invocation` paragraph): "Whether Cowork
  supports them is not known (the FU-001 Cowork test is not done)". The
  FU-001 run did not test `dev-retro` (Issue #3 comment).
- engineering-workflow-core#38, #39 and #40 are open, with no comments
  (`gh issue view`, 2026-11-14). DL-049 (2) reads Core `workflow.md:57` as
  "a duty of the interface, not of each dispatch" and marks it inference;
  #40 asks whether Reading A (each dispatch) is intended.
- The Claude Code install of this machine has `dev-skills` at version
  `0.1.0`, recorded commit `e37a990`; `main` is now `7e71ad5` (the
  installed-plugins record, fields version and commit only). The Issue #3
  comment gives the same version and commit for the Cowork install. Other
  installs are not known.
- With `version` set, an installed copy stays at its cached version until
  the string changes (official docs, D5 card 1). So the FU-027 premise "the
  definition holds until the first tagged release" is false already: a fix
  merged to `main` does not reach an installed `0.1.0` copy (design review
  DR-D-01, DR-S-05).
- `vendor/engineering-workflow-core.lock.json` (`consumer.version`) says
  `"0.1.0 (.claude-plugin/plugin.json)"`. `scripts/check_pack.py`
  (`MANIFEST_KEYS`) allows the `version` key in both manifests and does not
  require it.
- REQ-020 Acceptance bullet 3 names "`CHANGELOG.md` `[Unreleased]`".

## Design

### D1. FU-001 row (records; closes Issue #3)

Status becomes `Done for a Cowork desktop session (Issue #114); items not
covered moved to FU-069`, with the result from the Issue #3 comment only:
the date, "a Cowork desktop session on the maintainer's computer", version
`0.1.0` at commit `e37a990`, the four steps and their results, the defect
and its fix (Issue #115). No local path, no user name, no folder name. The
row stays (the header: never delete).

New row FU-069 (Open; design review DR-D-06): the Cowork items that FU-001
did not cover: a Cowork session in the cloud; a required review or scan in
Cowork (no review ran there; reviewer read-only rests on instructions, as in
Claude Code); whether the `allowed-tools` Read rules keep pack reads free of
prompts (the run does not report it); `dev-retro` in Cowork; the content of
the release (the run used `e37a990`); plus what card 1 decides about
updates in Cowork.

### D2. README (zh and EN, the same content)

- Install line (`:35`, `:178`): the path "Customize > Plugins > Add > Add
  marketplace", then `jeffery777/claude-dev-skills`, then install
  `dev-skills`.
- Paragraph (`:37`, `:180`; design review DR-D-05, DR-S-03): tested on
  2026-11-13 in a Cowork desktop session on the maintainer's computer, with
  version `0.1.0` at commit `e37a990` (FU-001, Issue #3): the plugin
  installs from the marketplace; `dev-plan` runs, with `${CLAUDE_SKILL_DIR}`
  replaced in the invoked skill, and reads `dev-core` and the Core files;
  `python3` and `graph.py` run; the four plugin agents are available, and
  `dev-explorer` ran. Not tested: a Cowork session in the cloud; a required
  review or scan in Cowork (reviewer read-only rests on instructions, as in
  Claude Code). Not verified: whether the `allowed-tools` rules with
  `${CLAUDE_PLUGIN_ROOT}` keep pack reads free of prompts in Cowork (the run
  does not report it). Open items: FU-069. The two existing safety
  sentences stay (without a shell, the written procedures; a path that does
  not resolve stops the skill, CB-6).
- What an unpinned install gets, and any update text: by card 1.
- The `dev-retro` row ("only Claude Code") does not change.

### D3. CHANGELOG

- Header (`:7-11`): the sentence about the first release says that `0.1.0`
  is the first tagged release (Issue #114), after FU-001 passed (Issue #3),
  and that its section serves as the release notes.
- `## [Unreleased]` becomes `## [0.1.0] - <date>`. `<date>` is the planned
  release date in UTC, written when the content is final (DR-D-08). Before
  the tag, the orchestrator compares it with the tag date (UTC); when they
  differ, the user decides: a fix PR or accept.
- Under the new heading, before `### Added`: one short limits paragraph
  (DR-D-07, DR-D-09, DR-S-03): the first tagged release; the Core pin
  (v0.5.0, `vendor/engineering-workflow-core.lock.json`); the entries of
  this section are grouped by kind, and the entry of the later merged
  change supersedes an earlier one (as changed by IR1-D-01); the DL-049 read-back scope is a reading of Core `workflow.md:57`
  marked inference, with the open question
  `jeffery777/engineering-workflow-core#40` (a Reading A answer would make
  that part stricter in Core than in this release); Cowork tested only in a
  desktop session at `e37a990`, no review or scan there (FU-069); runtime
  enforcement of the reviewer tool lists is not tested (FU-004); what card 1
  decides about install and update.
- One entry for this change (`### Changed`): README Cowork state and
  install path; FU-001 done, FU-069; plus what the cards decide.
- No empty `## [Unreleased]` heading is added now; the header says that the
  next change adds it back.
- Earlier entries that say "not tested in Cowork (FU-001)" (`:162-163`)
  stay: they record the state of their change (historical; the limits
  paragraph and the new entry supersede them). `:897-898` (a skill stops
  when a path does not resolve) is still true.

### D4. Requirement files (docs sync)

- REQ-018: Acceptance bullet 1 names the `[0.1.0]` section (first release,
  Issue #114) instead of `[Unreleased]`; the Notes sentence "No release
  yet" says that the first tagged release is `0.1.0` (Issue #114, after
  FU-001). The non-goal "A release or a tag before FU-001" stays true and
  stays. One `log.md` row (co-change rule 1).
- REQ-026: the Notes sentence says that the FU-001 Cowork run of
  2026-11-13 did not test `dev-retro` (Issue #3), so Cowork support of the
  fields is still not known. One `log.md` row. Plus the FU-027 outcome.
- REQ-020 (DR-D-04): Acceptance bullet 3 keeps its words and adds that the
  section is `[0.1.0]` since Issue #114. One `log.md` row.
- REQ-001: no change; the FU-001 row records that its Cowork acceptance is
  met for a Cowork desktop session (inference from the Issue #3 comment).

### D5. Decision cards (after this design review)

Cards in `.dev/issue-114/cards-1.md` (Traditional Chinese), each with a
recommendation; this session does not decide them:

1. Version policy: `plugin.json` and `marketplace.json` pin `0.1.0`. The
   `0.1.0` string already names `e37a990` in existing caches (fact above).
   Official docs (fetched 2026-11-14; `curl` of the `.md` pages, lines
   found with `grep`): code.claude.com/docs/en/plugins/host-marketplace.md,
   "Release a new version": "Bump `version` on each release: users stay on
   their cached copy until the string changes", "Omit `version`: users
   track your commits instead", and "Don't set `version` in both
   `plugin.json` and the marketplace entry"; .../plugins/loading.md: for a
   relative path inside a Git-hosted marketplace the computed version
   without `version` is "The commit SHA of the installed directory".
   claude.com/docs/cowork/guide/plugins.md names "Check for updates" and
   "Sync automatically" and does not say how Cowork compares versions
   (no `version` text on the page; `grep`). A docs subagent (claude-code-guide,
   not a pack reviewer) found the same and more (for example `#ref` on
   `marketplace add`); only the quotes above were read back here.
   Card 1 also carries the REQ-GAP questions DR-D-02 (a version policy
   requirement) and DR-S-06 (what an unpinned install gets; how to pin),
   the duplicate `version` (DR-S-07), and whether Cowork is tested again
   after a manifest change. The pin syntax `owner/repo#ref` is in
   code.claude.com/docs/en/plugins/install.md ("Add `#ref` to pin a branch
   or tag", read 2026-11-14 with `curl`); it is not tested here.
2. FU-027 (DR-D-01, DR-S-05): the "released" definition is false today
   with a pinned `version`; its options follow card 1.
3. FU-027, second question: does a Deferred finding count as a residual
   risk that the user accepted in a card; independent of card 1.
4. FU-036: the floor for release and packaging work, with the cost of each
   option; independent of cards 1 to 3 (this Issue already applies the
   floor).
5. engineering-workflow-core#40: release now with the disclosure of D3, or
   wait for the Core answer.
6. The PR keywords (DR-D-03): the brief asks for `Closes #114` and
   `Closes #3`; `Closes #114` closes the Issue at the merge, before the tag
   and the Release of its Done-when exist.

The cards are in `cards-1.md` as C1 to C6, in this order. DR-D-01 is a
`MUST-FIX` that stays open until the user answers card C2
(R-REV-3). Each answer that changes rule text, a manifest or a requirement
updates the Issue #114 scope first, then becomes a write node of its own
(`strict`: each slice a review unit; R-REV-6) with a deep review and a
Security Diff Scan; a rule change of `dev-retro` or R-DEL-2 is also work
under the floor.

### D6. Release title and notes (draft files, not published)

The task brief (step 5) asks for draft files; DR-D-10 is `Rejected` with
that source. After the content is final, this session writes the draft
title (`dev-skills v0.1.0`) and the notes to files in the notes folder of
this session group, outside the repository, with the PR head, its tree
and the SHA-256 of the notes. The path of that folder holds an account
name: it goes into no commit, post, record or Release (DR-S-09); the merge
card names the files by role only.

Extraction rule (one rule for both sides): from the line after
`## [0.1.0] - <date>` to the end of `CHANGELOG.md` (the heading line is
not part of the notes; the title carries the version).

Handover in the merge card (DR-S-01, DR-S-02); the orchestrator does these
steps after the user approves the merge, and the tag and the Release each
need their own approval (Issue #114 Scope):

- `M`: the full 40-hex merge commit, read back from the PR
  (`gh pr view <n> --repo jeffery777/claude-dev-skills --json state,mergeCommit,headRefOid`):
  `state` is `MERGED`, `headRefOid` is the reviewed head, tree(`M`) equals
  tree(reviewed head), and the parent of `M` is the base that the Merge
  Review bound.
- Before the notes and the create (IR1-S-04; order per IR-U1-R2): `git fetch` so that `M` is local;
  `gh api repos/jeffery777/claude-dev-skills/git/ref/tags/v0.1.0` must
  answer 404 (no tag yet), else stop. The parent check assumes a squash
  merge.
- Notes: `git --no-replace-objects cat-file blob <M>:CHANGELOG.md`, then
  the extraction rule; its SHA-256 equals that of the draft; the scan reads
  the whole file (else `NOT_RUN`).
- Scan inputs (R-REV-9, DL-050): the title file, the notes file, one text
  file with the tag name and `M`; no attached file.
- Command form: `gh release create v0.1.0 --repo jeffery777/claude-dev-skills --target <M> --title '<scanned title>' --notes-file <scanned file>`
  (a lightweight tag that GitHub makes: no tagger, message or signature;
  inference from the security review). Never `--generate-notes`,
  `--notes-from-tag` or `--notes`. An annotated tag instead needs its own
  scan of the tag object (push-scan steps 1 to 9) and a user decision on
  the tagger time zone (security review answer 3 (a)).
- Read-back: `gh release view v0.1.0 --repo jeffery777/claude-dev-skills --json tagName,name,body,isDraft,assets,url`
  (name = title; body SHA-256 = notes, or report any difference; no assets)
  and `gh api repos/jeffery777/claude-dev-skills/git/ref/tags/v0.1.0`
  (type `commit`, SHA `M`). One tag, one Release.
- Failure: when the effect is unknown, read back first and never resend
  blindly (R-AUTH-4); moving or deleting a tag or a Release is destructive
  and needs the user's confirmation at the time.
- The GitHub Release body limit and any normalization of the body are not
  verified here (the notes are about 72,000 bytes; inference).

### D7. After the cards: REQ-030, FU rows, manifests

- U1 adds REQ-030 (plugin version policy, from card C1 (c)), its
  `index.md` row and a `log.md` row; FU-027 Done (C2 (a), C3 (a)); FU-036
  Done (C4 (a), reopen trigger); FU-069 with the Cowork check after the
  release; README zh and EN: one sentence on what an install follows (no
  pin command: not tested); the CHANGELOG entry names the manifest change.
- U2 (packaging): remove `"version"` from `.claude-plugin/plugin.json` and
  from the plugin entry of `.claude-plugin/marketplace.json`; set
  `consumer.version` of `vendor/engineering-workflow-core.lock.json` to a
  text that says the commit SHA is the version (no manifest `version` since
  Issue #114). Verification: `python3 scripts/verify_core.py` (stage-map
  trigger for a change under `vendor/`), `./scripts/validate.sh`
  (`claude plugin validate` of both manifests).

## Slices, graph and review units

Graph: `.dev/issue-114/graph.json`.

| Node | Kind | Content | Review |
| --- | --- | --- | --- |
| DR | review | design review of this plan | deep (`dev-reviewer`, role `review-deep`) and security (`dev-security-reviewer`, role `review-security`), before any write node (R-RIG-1, R-REV-6) |
| C | human_gate | decision cards C1 to C6 (`cards-1.md`) | the user (relayed by the orchestrator session) |
| U1 | docs | D1 to D4 and D7: FU-001, FU-027, FU-036 and FU-069 rows, README, CHANGELOG, REQ-018, REQ-020, REQ-026, REQ-030, `index.md`, `log.md` | deep; Security Diff Scan (installation text, R-REV-7) |
| U2 | implement | D7: manifests and lock file (packaging, REQ-030) | deep; Security Diff Scan (installation and packaging, R-REV-7) |
| IR | review | implementation reviews: U1 and U2 as separate review units (separate reviewer runs, parallel, read-only) | deep and security for each |
| G | gate | commit and push gate, PR, release-note drafts | `dev-gate`; R-REV-9 scans |
| H | human_gate | merge, tag, Release | the orchestrator session and the user |

Card C1 (c) adds the write node `U2` after `U1`, with its own review unit.
`graph.py validate` warns `UNUSED_REQUIREMENT` for REQ-011 (the scans
belong to the gate `G`, which has no requirement list); this is expected.
Since the IR1-D-04 fix, U1 lists REQ-009 (the FU-036 row), so REQ-009 gives
no warning (IR2-01).

Dispatch values (R-DEL-2, `skills/dev-core/model-config.json` at the base):
`review-deep`, `review-security` and `scan`: `opus`/`xhigh`. Both values are
passed in each dispatch. These reviews are not read back by this session
(R-DEL-2 Read-back: only the Merge Review, the security reviews that the
head needs at the merge and the merge readiness scan, which the merging
session dispatches); their `recorded` value is `unknown` with the case
`not read back`.

Before each review and scan: `reviewer_acceptance.py check` and the CB-4
commands in the same Bash command, at the top level of the worktree; the
CB-4 commands again after the review.

## Completeness checks (before the commit)

Search list (fixed strings; rows filled before the commit): K1 `FU-001`,
K2 `tagged release`, K3 `first release`, K4 `Unreleased`, K5
`Add marketplace`, K6 `not yet tested in Cowork`, K7 `尚未實測`, K8
`0.1.0`, K9 `FU-027`, K10 `FU-036`, K11 `is released`, K12 `Cowork`
(design review: `docs/design-proposal.md` and `skills/dev-retro/SKILL.md`
hold Cowork claims that K1 to K11 miss). Co-change rule 1:
the two commands on `docs/requirements`. Co-change rule 2: the records that
list the decisions of this change are this plan and the cards file.

## DoD

- FU-001 row Done with the Issue #3 result and no private data; FU-027 and
  FU-036 rows carry the card decisions with the user's words.
- README zh and EN state the tested Cowork state, the corrected install
  path and the items not covered, with the same content.
- `CHANGELOG.md` has `## [0.1.0] - <date>` and the updated header sentence.
- REQ-018, REQ-020 and REQ-026 match; REQ-030 added; `index.md` and `log.md` rows.
- Manifests without `version`; lock `consumer.version` updated (U2).
- `./scripts/validate.sh` and `python3 -I -B -m unittest discover -s tests`
  pass; the graph validates.
- Draft release title and notes exist as files for the orchestrator.
- Reviews, scans and the gate as the pack requires; PR with `Part of #114`
  and `Closes #3` (card C6 (a)); stop at the merge card.

## Implementation and verification (U1, U2)

- U1 and U2 were written in this order by the main session (floor check
  before each write batch: `claude-opus-5-5`, `xhigh`). U2 was written
  before the U1 review, which departs from "units go one at a time"
  (`dev-plan` step 6); `graph.py transition U2 ready` refused it
  (`STATUS_DEP`, U1 not done). So the graph keeps U2 `planned` until U1 is
  done, the U1 review covers the U1 paths only, and U2 gets its own review
  after that. Recorded here and in the Lesson candidates of the final
  report.
- Issue #114 body updated after an R-REV-9 text scan (PASSED, `opus`/`xhigh`
  passed, recorded `unknown`, case `not read back`); posted with
  `--body-file`; the stored body equals the scanned file byte for byte
  (SHA-256 `99096cf7b49170fc52aba5cc9e3f7c0e1fb6b88fe54316e2dfd4fc07070fe7ea`).
- `./scripts/validate.sh` -> exit 0, "all checks passed" (it runs
  `verify_core.py`, `check_core_coverage.py`, `check_pack.py`, the unit
  tests and `claude plugin validate` of both manifests with Claude Code
  2.1.312). Correction (IRU2-D-01; the first record read only the last 15
  lines of the output): `claude plugin validate .` prints two warnings
  `version: No version specified. Consider adding a version following
  semver` and `ICON_MISSING`; `claude plugin validate .claude-plugin/plugin.json`
  prints one `version` warning and `ICON_MISSING`; both exit 0 (main agent,
  2026-11-14; the U2 deep reviewer saw the same with 2.1.310 and 2.1.311).
  The `version` warning is expected: REQ-030 and the official docs omit
  `version` on purpose, so it is not acted on. Whether the base gives
  `ICON_MISSING` too was not checked. CI pins 2.1.304; its result comes
  with the PR run (unverified).
- `graph.py validate` -> ok; at that time warnings `UNUSED_REQUIREMENT` for
  REQ-009 and REQ-011. After the IR1-D-04 fix: REQ-011 only (IR2-01).

## Implementation review U1, round 1

Record: `reviews/impl-u1-round-1.md`. Corrections to the design review
record `reviews/design-round-1.md` (IR1-D-08; that file is not edited,
because `events.jsonl` holds its SHA-256): DR-D-03 was answered by card C6,
not card 5; the #40 question is card C5, not card 4; the
Needs Human Decision findings got these answers (the user's words
「全照建議」, relayed): DR-S-04, DR-S-06, DR-S-07 and DR-D-02 by C1 (c)
(both manifests drop `version`; REQ-030; no pin instructions); DR-S-05 and
DR-D-01 by C1 (c) with C2 (a); DR-D-03 by C6 (a). `cards-1.md` C3 cites
"設計審查 DR-D 回答 3"; the fact itself is Core
`review-and-security.md:41` (the Deferred fields have no "accepted").

## Card C7 (cards-2) and node U3

The user's words 「C7 a」 (2026-11-14, relayed by the orchestrator session;
`cards-2.md`): `scripts/check_pack.py` fails when a manifest has `version`.
U3 (implement, `strict`, after U2): remove `"version"` from both sets of
`MANIFEST_KEYS`; add two `version` cases to
`test_manifest_key_outside_the_allowlist_fails` in
`tests/test_core_checks.py`; REQ-030 Acceptance gets the check; REQ-028
drops `version` from its key list; one CHANGELOG sentence; `log.md` rows
for REQ-028 and REQ-030. This resolves IRU2-D-02, IRU2-S-01 and IRU2-D-03.
The Issue #114 scope is updated first (text scan before the post). Review:
deep and Security Diff Scan. NITs that touch only this session's own record
wording get no new review round (orchestrator relay of 2026-11-14).

U3 verification (2026-11-14): the Issue #114 body was updated first
(text scan T2 PASSED, `opus`/`xhigh` passed, recorded `unknown`, case `not
read back`; the stored body equals the scanned file byte for byte, SHA-256
`e3e9ae159d2c05271849627410d46c8816c384735b5ef79aebad7dcc7ae0d732`).
`./scripts/validate.sh` -> exit 0 ("pack structure: OK"; 424 tests OK, 3
skipped; `claude plugin validate` gives the expected `version` warnings and
passes). `test_manifest_key_outside_the_allowlist_fails` -> OK with the two
new `version` cases. A load of `scripts/check_pack.py` without `-B` wrote an
ignored `scripts/__pycache__/` file; it is not staged and was not deleted
(deletion asks the user).

U3 review round 1 (`reviews/impl-u3-round-1.md`): two NITs fixed (CHANGELOG
sentence, REQ-028 note) and one SCOPE-CREEP fixed by deletion (the REQ-030
note on the `claude plugin validate` warning; the observation stays in this
plan, section "Implementation and verification", IRU2-D-01 correction).
The fix round adds its own `log.md` rows for REQ-028 and REQ-030. A narrow
confirmation follows on the fix-only diff.

U3 narrow confirmation (IR-U3-R2; `dev-skills:dev-reviewer`, role
`review-deep`, `opus`/`xhigh` passed, recorded `unknown`, case `not read
back`): IRU3-D-01, IRU3-D-02 and IRU3-D-03 confirmed on the fix-only diff
(SHA-256 `ad482cbf01bfd8b2f54900397677a36b989a1fa6a1e39997683d24ade0eb9413`);
co-change rule 1 passed; no new finding. Notes below the thresholds, kept
as residual: the CHANGELOG says "card C7" without the option letter; the
CHANGELOG entry does not list REQ-028. Acceptance check `PASS` and CB-4
equal before and after.

## Completeness checks before the commit (2026-11-14)

Run by the main agent after staging, from the top of the worktree
(`git rev-parse --show-prefix` printed an empty line), before the R-REV-9
commit scan. Each search command ran alone
(`git --no-replace-objects --literal-pathspecs -c core.quotePath=false grep --cached -c -F -i -e '<string>' --`)
in one loop; the loop output was filtered afterwards to drop the rows of
`.dev/issue-114/` (the list itself). Every search exited 0 (hits).
Strings K1 to K12 passed the value rule (printable, no `'`, `\` or line
break). Dispositions: `changed`, `noted`, `historical`.

| K | Path | Count | Disposition | Reason |
| --- | --- | --- | --- | --- |
| K1 FU-001 | `.dev/followups.md` | 3 | changed | FU-001 Status Done; FU-069 and FU-027 rows name it |
| K1 | `.dev/handoff/pr-2-checkpoint.md` | 5 | historical | Phase 1 handoff; the FU-001 row supersedes it |
| K1 | `.dev/issue-1-phase1/reviews/merge-review-1.md`, `round-1.md` | 1, 1 | historical | records of DR-022b; the FU-001 row supersedes |
| K1 | `.dev/issue-115/plan.md`, `.dev/issue-4-commit-security/reviews/round-2.md`, `.dev/issue-64-fu025-skill-paths/plan.md`, `.dev/issue-8-decisions-changelog-core-feedback/reviews/round-1.md` | 1 each | historical | records of earlier changes; the FU-001 row supersedes |
| K1 | `CHANGELOG.md` | 6 | changed | header, limits and the new entry; older entries record their change (the section says the later entry supersedes) |
| K1 | `README.md` | 2 | changed | Cowork paragraphs zh and EN |
| K1 | `docs/design-proposal.md` | 2 | historical | D-011 text ("Cowork waits for FU-001"); the FU-001 row supersedes |
| K1 | `docs/requirements/REQ-016-deploy-and-measure.md` | 3 | noted | source quote and non-goal "Cowork use before FU-001 is verified" stay true as written |
| K1 | `docs/requirements/REQ-018-changelog.md` | 2 | changed | note on the first release; the non-goal stays true |
| K1 | `docs/requirements/REQ-026-lessons-skill.md` | 3 | changed | Cowork note; other mentions are earlier sources (noted) |
| K1 | `docs/requirements/log.md` | 2 | historical | earlier rows; the new rows of this change supersede |
| K2 tagged release | `.dev/followups.md` | 3 | changed | FU-027, FU-036 and FU-001 rows; their old trigger text records the trigger |
| K2 | `.dev/issue-8-decisions-changelog-core-feedback/reviews/round-1.md` | 1 | historical | B1-007 record |
| K2 | `CHANGELOG.md` | 3 | changed | header and the new entry |
| K2 | `docs/requirements/REQ-018-changelog.md` | 2 | changed | acceptance and note |
| K2 | `docs/requirements/REQ-026-lessons-skill.md` | 1 | noted | earlier source locator of FU-027; the new FU-027 note supersedes |
| K2 | `docs/requirements/log.md` | 2 | historical | earlier rows and one new row |
| K3 first release | `.dev/issue-4-commit-security/reviews/round-2.md` | 1 | noted | "release notes and tags come with the first release": still true (Release notes get the text scan, DL-050) |
| K3 | `docs/requirements/log.md` | 1 | changed | the new REQ-018 row |
| K3 | `vendor/engineering-workflow-core/README.md` | 1 | noted | Core's own text, unrelated |
| K4 Unreleased | `.dev/issue-106/plan.md`, `.dev/issue-115/plan.md`, `.dev/issue-8-decisions-changelog-core-feedback/graph.json` | 1 each | historical | records of earlier changes that wrote into `[Unreleased]` |
| K4 | `CHANGELOG.md` | 2 | changed | header: the next change adds `[Unreleased]` |
| K4 | `docs/requirements/REQ-018-changelog.md`, `REQ-020-minimal-ci.md` | 1, 1 | changed | acceptance names `[0.1.0]` since Issue #114 |
| K4 | `docs/requirements/log.md` | 2 | changed | the new REQ-018 and REQ-020 rows |
| K4 | `vendor/engineering-workflow-core/CHANGELOG.md`, `README.md` | 3, 1 | noted | Core's own changelog, unrelated |
| K5 Add marketplace | `CHANGELOG.md`, `README.md` | 1, 2 | changed | corrected Cowork path |
| K6 not yet tested in Cowork | (no file outside `.dev/issue-114/`) | 0 | — | the README sentence is gone |
| K7 尚未實測 | `docs/design-proposal.md` | 1 | noted | about Fable, unrelated |
| K7 | `vendor/engineering-workflow-core/docs/architecture/project-split.md` | 1 | noted | Core's own text, unrelated |
| K8 0.1.0 | `.dev/followups.md` | 2 | changed | FU-001 and FU-069: the tested version `0.1.0` at `e37a990` (true) |
| K8 | `CHANGELOG.md` | 5 | changed | `[0.1.0]`, tag `v0.1.0`; the Phase 1 entry "Plugin `dev-skills` 0.1.0" is historical |
| K8 | `README.md` | 4 | changed | tested version and the tag |
| K8 | `docs/requirements/REQ-018-changelog.md`, `REQ-020-minimal-ci.md`, `REQ-030-plugin-version-policy.md`, `log.md` | 2, 1, 3, 2 | changed | the release and the version policy |
| K8 | `vendor/engineering-workflow-core.lock.json` | 1 | noted | the path of Core's `docs/releases/v0.1.0.md`, unrelated |
| K8 | `vendor/engineering-workflow-core/CHANGELOG.md`, `README.md`, `docs/provenance/source-map.md`, `docs/releases/v0.1.0.md`, `docs/releases/v0.1.1.md` | 8, 2, 6, 7, 6 | noted | Core's own versions, unrelated |
| K9 FU-027 | `.dev/followups.md` | 2 | changed | FU-027 Done; FU-069 item 5 |
| K9 | `.dev/issue-57-d019-pr4/events.jsonl` | 1 | historical | event of D-019 PR-4 |
| K9 | `CHANGELOG.md` | 2 | changed | new entry; an older entry records its creation (historical) |
| K9 | `docs/requirements/REQ-026-lessons-skill.md`, `log.md` | 3, 3 | changed | FU-027 note and source; rows |
| K10 FU-036 | `.dev/followups.md` | 1 | changed | FU-036 Done |
| K10 | `.dev/issue-75-issue73-followup/graph.json`, `plan.md` | 1, 3 | historical | Issue #75 records |
| K10 | `CHANGELOG.md` | 2 | changed | new entry; an older entry is historical |
| K10 | `docs/design-proposal.md` | 6 | historical | D-023 text says FU-036 evaluates the floor; the FU-036 row (Done, card C4 (a)) supersedes |
| K10 | `docs/requirements/REQ-009-subagent-model-effort.md` | 2 | historical | Issue #75 source and note; the FU-036 row supersedes |
| K10 | `docs/requirements/log.md` | 1 | historical | Issue #75 row |
| K10 | `skills/dev-core/deltas.md` | 1 | historical | DL-039 says FU-036 evaluates; rule text outside this Issue's scope; the FU-036 row supersedes (U1 review residual) |
| K11 is released | `docs/design-proposal.md`, `docs/requirements/REQ-026-lessons-skill.md`, `skills/dev-retro/SKILL.md` | 1, 1, 2 | noted | the definition stays (card C2 (a)); its premise holds again (REQ-030) |
| K12 Cowork | `.claude-plugin/marketplace.json`, `plugin.json` | 1, 1 | noted | descriptions "for Claude Code and Cowork": still true |
| K12 | `.dev/followups.md` | 3 | changed | FU-001, FU-069 |
| K12 | `.dev/handoff/pr-2-checkpoint.md`, `.dev/issue-1-phase1/gate-commit.md`, `.dev/issue-1-phase1/reviews/round-1.md`, `.dev/issue-115/plan.md`, `.dev/issue-64-fu025-skill-paths/plan.md`, `.dev/issue-66-user-level-install/plan.md` | 4, 3, 3, 1, 1, 1 | historical | records of earlier changes |
| K12 | `CHANGELOG.md` | 11 | changed | limits and new entry; older entries historical |
| K12 | `README.md` | 8 | changed | install, Cowork and version paragraphs; the intro and the `dev-retro` row stay true (noted) |
| K12 | `docs/design-proposal.md` | 9 | historical | design and decision text of earlier changes |
| K12 | `docs/requirements/REQ-001-claude-skill-pack.md` | 4 | noted | need and acceptance; the FU-001 row records that the Cowork acceptance holds for a desktop session (inference) |
| K12 | `docs/requirements/REQ-016-deploy-and-measure.md` | 3 | noted | as K1 |
| K12 | `docs/requirements/REQ-026-lessons-skill.md`, `REQ-030-plugin-version-policy.md`, `index.md`, `log.md` | 7, 6, 1, 5 | changed | Cowork notes, the new requirement and rows |
| K12 | `scripts/check_pack.py` | 1 | noted | the Cowork description length limit, unrelated |
| K12 | `skills/dev-plan/references/graph-schema.md` | 1 | noted | a session without code execution; still true |
| K12 | `skills/dev-retro/SKILL.md` | 1 | noted | `dev-retro` fields in Cowork not known: still true (FU-069 item 4) |

Co-change rule 1 (both commands exit 0): staged requirement files
REQ-018, REQ-020, REQ-026, REQ-028, REQ-030 (plus `index.md`, `log.md`);
`log.md` staged diff has 10 lines that start with `+|` (REQ column: REQ-018
1, REQ-020 1, REQ-026 2, REQ-028 2, REQ-030 4) and 0 lines that start with
`-|`. Every listed requirement file has its ID in a `+|` row. Co-change
rule 2: the card answers are quoted in `cards-1.md`, `cards-2.md`, this
plan, the FU-027, FU-036 and FU-069 rows, REQ-026, REQ-028 (by its log
row), REQ-030 and the `log.md` rows.
