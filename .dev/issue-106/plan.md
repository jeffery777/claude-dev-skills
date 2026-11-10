# Issue #106 plan: vendored Core update to v0.5.0

Written per ASD-STE100 principles; full conformance not verified.

## Objective and scope

- Objective: GitHub Issue #106 (body read 2026-11-09, no comments). Scope
  items 1 to 9 and "Done when" of the Issue; nothing more.
- Base: `23ed6dd352dba41e76d878655239c22465092f49`
  (`git --no-replace-objects merge-base HEAD origin/main`).
- Rigor: `strict`. Reason: Core authority, published rule text, review and
  scan rules (R-RIG-1). The Issue gives the same tier.
- Requirements: REQ-005 (language and writing), REQ-007 (Core authority),
  REQ-009 (model and effort; MR105-D-03 and SEC105B-01), REQ-011 (scans
  before commit and push), REQ-012 (review convergence), REQ-018
  (changelog), REQ-019 (Core feedback), REQ-022 (single source), REQ-023
  (dev-core not weaker than Core).
- Out (Issue #106): the review roles, floors and efforts; Issue #79 C3 and D;
  the release; any change in the Core repository. Not changed:
  `model_effort_readback.py`, `model-config.json`, `push_precheck.py`.
- Core source: only the tags of the local clone of
  `engineering-workflow-core`, read with `git show <tag>:<path>` or
  `git archive <tag>`, plus a read-only `git ls-remote` of the published tag
  (DR-D-11). The clone is not changed.

## Model and effort of this session

The transcript of this session records `claude-opus-5-5`. The first records
give effort `medium`; that floor check did not pass, and the session stopped
before any write and told the orchestrator. From the orchestrator's change on,
the records give `high`, and the check passes: `opus` is tier 3 in
`skills/dev-core/model-config.json` at the base, and the ID is listed. The
main session implements. Implement row: role `implement` (`strict`).

## Facts from Core (tags of the local clone)

- `v0.1.1` = commit `7b66978a76597d09be1b55ad199a969b4ee59c0f`; `v0.5.0` = tag
  object `374124ac6bc88efe73b27a4f7875fffd0dc669e2`, commit
  `0edcbad3d126cb8a7c0b64e9ad95283e2cca635e` (`git rev-parse`).
- `git diff --stat v0.1.1 v0.5.0`: 23 files, +1781, -9. No file is deleted.
  `git ls-tree -r v0.5.0`: 31 files (14 now). Only three of them are
  contracts; the other 20 changed files are companion, maintenance, release
  and provenance documents, which change no contract or consumer obligation
  (Core `README.md` at v0.5.0, reading guide; `writing.md:72` says the
  examples are not authority). Line numbers below are at v0.5.0.
- Contract changes (`git diff v0.1.1 v0.5.0 -- contracts`):
  - C1 `review-and-security.md:17-35`: new anchor `review-required-read-only`
    (effective read-only condition for a required reviewer, and the
    one-time per-environment acceptance).
  - C2 `review-and-security.md#review-findings` `:43-51`:
    `requirement_relation` with a source or a note that the source is
    missing; "a blocker does not authorize a fix outside the scope, a new
    requirement or an external write" (`:47`); "the other safe fixes are
    limited to the authorized scope" (`:51`).
  - C3 `review-and-security.md:87-101`: new anchor `review-publication-data`.
  - C4 `workflow.md#wf-writing`: a short minimum (three items) and the full
    contract `writing.md` on demand (`:30-40`).
  - C5 `workflow.md#wf-verification` `:75`: implementation defect, premise
    problem or mixed; no model switch, effort raise or repeated patch
    replaces the re-assessment.
  - C6 `workflow.md#wf-assumptions-and-options` `:91`: each new mechanism
    records its unique effect and its requirement source.
  - C7 new `contracts/writing.md`, anchors `writing-scope`,
    `writing-principles`, `writing-genres`, `writing-sources`,
    `writing-language`, `writing-process`.
- `wf-delegation` and the contracts `authorization-and-stops.md` and
  `exact-head-and-evidence.md` have no change from `v0.1.1` to `v0.5.0`.

## Finding triage in this work

Before a fix, judge in this order (R-REV-4; the same text goes to each brief):

1. Is it in the threat model? Agent or host errors and program or
   config-parsing bugs: yes. Deliberate runtime tampering: no; record it as
   not handled.
2. Does a requirement cover it? A Core obligation is a requirement. If not,
   it is a `REQ-GAP` for the user. Do not fix it because a reviewer raised it.
3. Only then fix, and prefer deletion over a new sentence.

A wording edge or a single command flag that no recorded agent error reaches
is "keep as is" or an option on a user card, not a new rule (the
orchestrator's note, 2026-11-09; the user does not want over-protection).
Core blockers stay `MUST-FIX`.

## Slices

| PR | Content | Risk |
| --- | --- | --- |
| PR-1 | Scope 2: the #23 acceptance record (D-032) and the reviewer rules R-REV-1, CB-4, CB-5, DL-004 | high |
| PR-2 | Scope 1, 4, 5, 6, 7, 9 and MR105-D-03: vendor bump, lock, pins, citations, source-map rows, deltas, R-REV-3 and R-REV-4 scope limit, R-VER-2 mixed class, writing layers, DL-049 re-check, the test | high (vendor and lock, authorization text; DR-D-04) |
| PR-3 | Scope 3 and SEC105B-01: R-REV-9 against `review-publication-data` | high |

PR-2 needs PR-1 merged: the record lands before the bump. DR-D-10: between a
PR-2 merge and a PR-3 merge, vendored Core would ask for checks that the pack
text does not name yet. The order PR-1 → PR-3 → PR-2 removes that window (PR-3
then cites Core v0.5.0 by tag and commit, as PR-1 does, and PR-2 adds the
cite). The orchestrator agreed (its message to this session, 2026-11-09):
the order is PR-1 → PR-3 → PR-2, and PR-2 is the last PR and says
`Closes #106`.

Branch plan (orchestrator's message to this session, 2026-11-09): PR-1 on
`issue-106-vendored-core-v050`, body `Part of #106`; PR-2 on
`issue-106-pr2-vendor-bump`; PR-3 on `issue-106-pr3-publication-data`. The
last PR to merge closes #106. The orchestrator creates each later branch from
main after the previous merge (`gh issue develop 106`) and names it; this
session creates no branch.

## Design

### PR-1: #23 acceptance record

Facts: both reviewer agent files have `tools: Read, Grep, Glob, Bash` and
`disallowedTools: Edit, Write, NotebookEdit` (`agents/dev-reviewer.md:6-7`,
`agents/dev-security-reviewer.md:6-7`), pinned by `scripts/check_pack.py:85-86`.
Runtime enforcement of these lines is not tested (`skills/dev-core/deltas.md:27`,
FU-004). CB-4 records HEAD, status and a diff hash before and after each
review; its commands do not check exit codes, and a failed `git diff` gives
the empty-input hash, the same as a clean tree (DR-D-07: exit code 129 outside
a repository; `skills/dev-retro/SKILL.md` "Read-back" already handles this).

1. A new decision `D-032` in `docs/design-proposal.md` (Traditional Chinese
   and English parts) is the acceptance record (Core :29-35). Fields:
   - Decision: the user's own words in this session to card I106-C1, quoted,
     with the date. The agent never accepts or presumes acceptance. Only a new
     quoted decision of the user changes D-032; a change made to pass a test
     voids it (DR-S-05, DR-D-02).
   - Bound environment: the option of card I106-C1, with the check command.
   - Protected resources (DR-S-01, DR-D-02): the content under review in the
     repository of the change (worktree, index, refs, objects), the scan input
     files, and the PRs and Issues of that repository. When a task, a brief
     or a project policy names another protected resource or requires
     technical isolation, D-032 does not apply.
   - Rules covered (DR-D-06): Core v0.5.0 `review-required-read-only` (tag and
     commit above), the sentence of R-REV-1 that applies it, the CB-4
     detection and CB-5. Applies to every required independent review and
     every R-REV-9 scan that `dev-reviewer` or `dev-security-reviewer` runs.
     A later change of R-REV-9 is not a change of these rules.
   - Write channels (DR-S-06, DR-D-14): Bash in both agents, which can write
     in the worktree, in `.git`, outside the repository and to the network
     (for example `gh` with the user's token: merge, close, delete, release);
     and any tool that the host gives beyond the agent file (runtime
     enforcement of `tools` and `disallowedTools` not tested, FU-004).
   - Reason: the reviewers run tests and the Git and read-back commands of
     the scans.
   - Substitute detection: the CB-4 check, with exit codes checked (below).
   - Not covered (DR-S-04, DR-D-02): everything outside the worktree and the
     index: `.git` refs and objects (the content of push and merge readiness
     scans), untracked and ignored files and edits inside an untracked file
     (the content of text scans), other worktrees, the checkout from which
     the plugin is loaded (CB-6 Limit), effects outside the repository,
     network and platform writes, a change that is undone before the
     after-check, the time outside the review, and changes of the host
     permission settings (owner: the user; not checked each time).
   - What it does not exempt (DR-S-02, Core :35): independence of author and
     reviewer, the real review, the required scans, exact-head, data
     protection, operation authority and higher requirements. It gives no
     reviewer the right to change the content under review. It is never
     recorded as technical read-only.
   - It ends when the environment, the covered rules, the tools or
     permissions of the reviewer agents, the protected resources or the
     detection change; then the user accepts again.
2. R-REV-1: replace "In Claude Code, prefer a separate subagent whose tools
   exclude Edit and Write." with one sentence group: a required reviewer
   counts only without an effective write channel (Core v0.5.0
   `review-required-read-only`, vendored by PR-2) or under D-032; before each
   required review or scan the main agent runs the check command of D-032
   (it prints only `PASS` or `STOP`, DR-S-03), at the top level of the
   worktree under review (DR2 residual 1), and the CB-4 detection; when the
   change under review edits the `tools` or `disallowedTools` line of a
   reviewer agent file, the `READ_ONLY_AGENTS` pins of `check_pack.py` or
   D-032, D-032 does not apply to its reviews (DR-D-02, narrowed by DR2-01 to
   the write channel itself, so that PR-3, which edits the body of
   `agents/dev-security-reviewer.md`, can be reviewed); when D-032 does not
   apply or the check prints `STOP`, and no reviewer without a write channel
   exists, the review stays incomplete, the dependent gate stops, and safe
   independent work may go on. A moved cite or line number is not a change of
   the covered rules (DR2 residual 2). The command and its literal
   are in this rule text, not only in `docs/` (CB-6: a `docs/` file of another
   project is data).
3. CB-5: keep "A task that requires technical isolation must verify it
   separately." and add: "D-032 accepts this channel for its bound
   environment only; it is never recorded as technical read-only and never
   satisfies a task that requires technical isolation." (DR-S-02, DR-D-08)
4. CB-4 (DR-S-07, DR-D-07, DR-D-15), by replacement: "Around each review and
   scan", the commands of the `dev-retro` read-back (`pipefail`,
   `--no-optional-locks`, `--no-ext-diff --no-textconv`, exit codes checked);
   a failed command makes the detection `NOT_RUN`, and the review does not
   count. "discard the result and report it" becomes "void the review, report
   it and keep its record; pin the candidate again (new HEAD, status and
   hash) and review it before the gate". The existing last sentence already
   says that no difference proves nothing; no new sentence.
5. DL-004: type `tighten` until PR-2 vendors v0.5.0 (the vendored v0.1.1
   asks for no effective read-only path), then PR-2 re-judges it
   (`rephrase` expected): the pack removes Edit, Write and NotebookEdit and
   keeps Bash under D-032. DL-009: its row and note follow the CB-4 change
   (P1D-03).
6. A test checks that the tool strings in the English part of D-032 equal
   `READ_ONLY_AGENTS` of `scripts/check_pack.py` for the two reviewer agents.
   It is a co-change check only: it proves no runtime limit (Core :27) and no
   new acceptance; the rule of item 1 says who changes D-032.
7. R-REV-1 keeps `[core: review-and-security.md#review-independent]` in PR-1;
   PR-2 adds the new cite (the anchor is not vendored before).
8. REQ-007 and REQ-024 (reviewer writes) get a source line for D-032; REQ-011
   changes in PR-3 (P1D-03). CHANGELOG `[Unreleased]`.
9. Same-change candidates (DR-sec residual): the old phrases "an agent with
   write tools never counts" (R-REV-1), "read-only agent" (CB-4) and
   `skills/dev-review/SKILL.md:108-118` are checked; they fail closed, so they
   change only where the new text makes them false.

### PR-2: vendor bump and rule text that follows Core

1. Vendor: remove `vendor/engineering-workflow-core/`, then
   `git -C <clone> archive v0.5.0 | tar -x -C vendor/engineering-workflow-core/`.
2. Lock: version `0.5.0`, tag `v0.5.0`, the tag object and the commit above,
   31 files with SHA-256 and sizes, both set digests (`set_digest` of
   `scripts/verify_core.py`), `sections_used` adds `contracts/writing.md`,
   `dependency_closure` and `upstream_verification` rewritten: date,
   `git ls-remote <upstream> refs/tags/v0.5.0` gives tag object `374124ac…`
   and `^{}` gives `0edcbad3…` (DR-D-11), `verify_core.py --upstream`; the
   Codex parity line says "not checked at v0.5.0" unless it is checked.
3. Pin text: `skills/dev-core/SKILL.md:12` and R-EXH-5,
   `skills/dev-core/source-map.md:3`, `skills/dev-core/deltas.md:1`,
   `docs/design-proposal.md` Core vendor rows (both languages),
   `docs/requirements/REQ-018-changelog.md:33` (the acceptance names the
   current pin; the v0.1.1 fact moves to a note), `docs/core-feedback.md` (a
   note that the pin moved; line numbers there stay at v0.1.1). Historical
   records (`.dev/`, CHANGELOG entries) keep their text.
4. Line citations: every `<contract>.md:<line>` in live rule and requirement
   text (`skills/`, `agents/`, `docs/requirements/`, `deltas.md`,
   `source-map.md`, the stage map) is checked against `v0.5.0` and moved; the
   search command and its counts go into this plan (dev-plan step 6).
5. Source map: rows `review-and-security.md#review-required-read-only` →
   R-REV-1 (D-032); `review-and-security.md#review-publication-data` →
   R-REV-9; six `writing.md#writing-*` rows → R-WRT-2. R-REV-1 and R-REV-9 add
   the cites.
6. R-REV-3 and R-REV-4 (DR-D-01), by rewriting the existing sentences: a Core
   blocker blocks readiness for every relation; it is fixed in this round only
   inside the authorized scope; a fix outside it, a new requirement or an
   external write goes to a decision card (R-AUTH-6). R-REV-4 "unless it is a
   Core blocker: fix a Core blocker first" and "Fix the other findings that
   can be fixed safely" get the same limit.
7. R-VER-2: "Classify a failure that points at the spec, the acceptance or a
   design premise as an implementation defect, a premise problem or mixed;
   a model switch, an effort raise or a repeated patch never replaces that
   re-assessment." The R-DEL-2 escalation bullet: "a spec or design failure"
   gets "or a mixed one" (DR-deep residual 1).
8. Deltas (DR-D-17): DL-003: the requirement source of R-RIG-3 is stricter;
   its list of mechanisms is narrower, and Core C6 governs the rest. DL-011:
   `compress`; Core now has `requirement_relation` and asks for a source or a
   note for each finding, which Core governs. DL-004 (PR-1). DL-010 reason:
   Core now asks for a bounded data check before each public commit, push,
   merge, tag and post; the pack is still stricter (an independent scan by
   `dev-security-reviewer`, never `not applicable`).
9. Writing (C4, C7), by the answer I106-C2 (b) (see "Decision cards"):
   R-WRT-1 is the minimum for delivery summaries and ordinary records. A new R-WRT-2
   cites the six `writing.md` anchors: when the document is the deliverable or
   the review target (substantive writing, editing, translation or document
   review; a task to write or review a summary document is a document task),
   read `contracts/writing.md` in full; judge by impact, not by word count or
   file type, after checking the context; a typo or format fix that does not
   change the meaning needs only R-WRT-1. The pack's STE statement in every
   review and gate report stays (a downstream fixed statement, which
   `writing-language` keeps). The spot-check bullet moves under R-WRT-2. The
   stage map: `dev-implement`, `dev-docs` and `dev-review` add `writing.md`
   "when the document is the deliverable or the review target" (DR-D-12); the
   review-criteria table for `dev-reviewer` likewise; the task brief names
   `writing.md` for a document deliverable.
10. DL-049 and D-031 re-check (DR-D-13): `wf-delegation` did not change. The
    new reviewer text (`review-and-security.md:21`, `:23`: "在當次介面中",
    "接口須以當次支援且可核實的控制與生效證據") supports "a duty of the
    interface" but its "當次" (for each run) does not support, and may weaken,
    "not of each dispatch". The DL-049 note says this; the reading stays an
    inference; the final report tells the user, who may ask for core feedback
    (REQ-019) or a new Issue. No read-back rule changes (Issue Out).
11. MR105-D-03: a test in `tests/test_rule_slimming.py` that pins the three
    dispatches that keep the read-back (Merge Review, each security review the
    head needs at merge, merge readiness scan) in R-DEL-2 and
    `references/readback-gate.md`.
12. Optional, only when it is one line: the old label at
    `docs/requirements/REQ-022-single-source-rules.md:55`. Not done: the
    R-REV-3 sentence on accepted residual risk that grows (a requirement
    question; listed as a follow-up), `dev-plan` step 6 (card MR105-C2 was for
    PR #105 only).
13. Rejected: `verify_core.py` reads the clone without `--no-replace-objects`
    (DR-deep residual 12): only deliberate tampering reaches it.

### PR-3: R-REV-9 against `review-publication-data` (#22) and SEC105B-01

Only what Core `review-publication-data` (`:87-101`) asks for. Copies of the
scan lists in `agents/dev-security-reviewer.md` and `skills/dev-implement/SKILL.md`
change with R-REV-9 (DR-D-09, REQ-022).

| Core sentence | Pack now | Plan |
| --- | --- | --- |
| scope: commit, push, merge, tag, PR or Issue text and attached data | commit, push, merge readiness, PR and Issue text and comments, review records | add a Release title and notes, the tag name and target of a Release, and each attached file; a scan that cannot read a whole attachment or asset is `NOT_RUN` and stops for the user (DR-S-11, Core :99) |
| the actual destination of each public action | push step 2 only | push: the push URL names the repository of the task (from the user's instruction or the task), tested without printing it; a post names its repository (`--repo`), as `dev-retro` already does (DR-S-09, DR-D-05) |
| the actual payload of a non-Git post | the text is saved to a file and scanned | post that scanned file itself (`--body-file` or `--notes-file`); no text that the tool generates after the scan (DR-S-10, DR-S-11) |
| look for: certificates, confidential files, hosts and accounts, unneeded execution logs; keep an approved public identity with a source and full license notices | keys, passwords, tokens, private files and paths, hostnames, private email, real names | add certificates, hosts and addresses, accounts and unneeded execution logs; add "an approved public identity with a source and license notices are kept"; awk pattern `-----BEGIN ` instead of `-----BEGIN [A-Z ]*PRIVATE KEY` (DR-S-13) |
| before a commit: signer information and signing settings, without reading signing secrets | "the staged diff shows no signature; the push scan reports it" | the commit scan input says whether Git will sign (`commit.gpgsign`, a `-S` option) and the `gpg.format`; a signature that Git will make is a finding for the user, as push step 5; `user.signingkey` by class only, never its value; no private key or passphrase is read (DR-S-08) |
| after creation: the raw object before the dependent public action | read-back of `cat-file commit HEAD`; push step 8 | covered |
| push and merge: full range, raw identity, message, trailer, signature; merge result | push steps 6 to 8; merge readiness bullet | covered |
| tag: tag object, signature and certificate public information | push step 8 scans the tag; signatures go to the user without decoding (FU017-C1b) | substitute: recorded with the source card |
| raw data, not mailmap, replace refs or pretty views | `--no-replace-objects`, `--no-mailmap`, `--format=raw` | covered |
| every URL and refspec actually sent and the rewrites | step 2 (`get-url` and `get-url --push` print the URL after `insteadOf` and `pushInsteadOf`: tested 2026-11-09 with git 2.54.0 in a scratch repository), steps 3 and 4 | covered with the destination row above |
| drift, unknown, failed read: stop, not clean | "any change … new candidate"; exit code check | covered |
| public records: safe categories only, no private value or guessable hash | R-REV-8 masking | covered |
| LFS objects, push options, push certificates, commit time zone | accepted residual risk (FU-007 (b) and (c)) | recorded with the source cards; FU-007 (b) release notes are now covered by the first row |

Keep as is (no recorded agent error reaches them; orchestrator's note):
`--head` for `gh pr create`, fixed URL forms beyond the https form, a listing
of `gh` fill, editor, web and template options (the "payload" row already
forbids generated text).

SEC105B-01 (DR-S-12): one clause in R-REV-9: "Each scan (commit, push, text
and merge readiness) that does not count by R-DEL-2 and R-REV-1 counts as no
scan, also when push step 5 counts it as passed." Both notes in REQ-011
(Issue #95 and Issue #104) say: the session binding and R-REV-1 apply to each
scan; the read-back applies to the merge readiness scan only.

Each "covered" or "substitute" row gets a delta or source-map note, so "Done
when" item 3 holds. The CHANGELOG gets an entry per PR.

## Decision cards (Traditional Chinese, for the user)

`cards-1.md`: I106-C1 (the scope of "environment" for D-032), I106-C2 (the
detailed R-WRT-1 bullets).

The user's own message in this session (2026-11-09): 「C1 a，C2 b」.

- I106-C1 (a): D-032 binds the account `jeffery777` and the repository
  `jeffery777/claude-dev-skills` only. Check command (one line, prints only
  `PASS` or `STOP`):
  `test "$(gh api user --jq .login 2>/dev/null)" = jeffery777 && test "$(gh repo view --json nameWithOwner --jq .nameWithOwner 2>/dev/null)" = jeffery777/claude-dev-skills && echo PASS || echo STOP`.
  Work in another repository stops at each required review until the user
  accepts that repository too. Tested 2026-11-09: `PASS` in this worktree,
  `STOP` with the working directory `/`.
- I106-C2 (b): a loosening that the user typed in this session. R-WRT-1
  becomes the three Core v0.5.0 minimum items plus the project tightenings:
  the Traditional Chinese plain-writing bullet (DL-014), and the whole STE
  bullet: English technical text follows the ASD-STE100 principles, the
  statement in every review and gate report, and no conformance claim
  (REQ-013, D-014 items 2 and 3; DR2-02: the principle sentence is a user
  requirement, not only a restatement of Core, so it stays; this keeps more
  than the card text and narrows the loosening). The bullets that restate
  Core v0.1.1 `wf-writing` items 1, 2, 3, 5 and 6 are deleted where Core
  v0.5.0 does not keep them in the minimum, and `writing.md` covers them for a
  document task (R-WRT-2). Record: a `deltas.md` row, type `tighten` (what
  stays is still at or above Core, as DL-049), whose text names the loosening
  with the source (this answer), the quote, the authority (the user), the
  reason (Issue #106 Scope 7) and the scope (the restated bullets only). This
  is in PR-2.

## Verification

- `scripts/validate.sh` (includes `check_pack.py`, `check_core_coverage.py`,
  `verify_core.py`, unit tests).
- PR-2: `python3 -I scripts/verify_core.py --upstream <clone>` passes (tag
  object, commit, 31 files), and the `git ls-remote` check of the lock.
- dev-plan step 6 search list and co-change rule 1 before each commit; counts
  and exit codes in this plan.
- Reviews per PR: a deep review of the diff, and a security review for each
  PR (R-REV-7: reviewer and scan rules in PR-1 and PR-3; vendor, lock and
  authorization text in PR-2, DR-D-04); R-REV-9 scans before each commit and
  push; a text scan before each post.

## Design review

Round 1: deep (`dev-reviewer`) and security (`dev-security-reviewer`), both
opus/xhigh, on the first version of this plan and `cards-1.md`. Findings and
triage: `reviews/design-round-1.md`. This version applies them.

## PR-1 completeness checks (2026-11-09, on the index, before the reviews)

Commands from the top of the worktree (`git rev-parse --show-prefix` prints an
empty line); `git --no-replace-objects --literal-pathspecs -c core.quotePath=false grep --cached -c -F -i -e '<string>' --`.
Files under `.dev/issue-106/` get no rows.

| ID | String | Exit | Rows (path: count, disposition, reason) |
| --- | --- | --- | --- |
| K1 | `DL-004` | 0 | `skills/dev-core/deltas.md`: 2, changed (DL-004 row; DL-009 note keeps its link); `skills/dev-core/SKILL.md`: 1, changed (CB-5 origin); `skills/dev-core/source-map.md`: 1, noted (read-only Bash use is still by instruction); `docs/design-proposal.md`: 2, changed (D-032 both languages); `docs/requirements/REQ-007-core-authority.md`: 1, changed; `docs/requirements/REQ-024-agent-write-and-delete.md`: 1, changed; `CHANGELOG.md`: 1, changed; `tests/test_reviewer_acceptance.py`: 1, changed; `docs/core-feedback.md`: 2, historical (feedback at v0.1.1); `.dev/issue-1-phase1/reviews/round-1.md`, `.dev/issue-22-fu005-records/fu005-checklist.md` (2), `.dev/issue-22-fu005-records/fu005-spec.md`, `.dev/issue-31-fu005-pr3/reviews/round-0-security-design.md`, `.dev/issue-31-fu005-pr3/reviews/round-1-deep.md`: 1 each unless shown, historical (records of earlier work; D-032 supersedes) |
| K2 | `D-032` | 0 | `CHANGELOG.md`: 5, `docs/design-proposal.md`: 6, `docs/requirements/REQ-007-core-authority.md`: 2, `docs/requirements/REQ-024-agent-write-and-delete.md`: 2, `docs/requirements/log.md`: 2, `skills/dev-core/SKILL.md`: 2, `skills/dev-core/deltas.md`: 2, `tests/test_reviewer_acceptance.py`: 6; all changed (new in this change) |
| K3 | `CB-5` | 0 | `skills/dev-core/SKILL.md`: 2, changed; `skills/dev-core/deltas.md`: 3, changed (DL-004) or noted; `agents/dev-reviewer.md`: 1 and `agents/dev-security-reviewer.md`: 1, noted ("read-only Bash use is enforced by instructions only" stays true); `skills/dev-gate/references/platform-profile.md`: 1, noted (not technical isolation, still true); `scripts/check_pack.py`: 6, noted (the pins; unchanged); `tests/test_core_checks.py`: 2, noted; `docs/requirements/REQ-022-single-source-rules.md`: 2, `REQ-023-core-audit.md`: 2, `REQ-025-on-demand-core-loading.md`: 4, noted (they name the ID range CB-1 to CB-5); `docs/requirements/REQ-024-agent-write-and-delete.md`: 1, historical (its non-goal scopes the FU-013 work; the new note says Issue #106 changed CB-5); `docs/design-proposal.md`: 4, noted or changed (D-032); `CHANGELOG.md`: 6, historical or changed; `.dev/followups.md`: 3, noted (FU-004 still open); `.dev/issue-16-…`, `.dev/issue-18-…` (3), `.dev/issue-22-…` (7), `.dev/issue-31-…` (2), `.dev/issue-69-…` (6): historical |
| K4 | `prefer a separate subagent` | 0 | hits only under `.dev/issue-106/`; the R-REV-1 sentence is gone |
| K5 | `technical isolation` | 0 | `skills/dev-core/SKILL.md`: 2, changed (CB-5, R-REV-1); `docs/design-proposal.md`: 2, noted (principle 3: Bash still makes it no isolation) and changed (D-032); `README.md`: 1, noted (still true); `skills/dev-gate/references/platform-profile.md`: 1, noted; `vendor/…/migration-plan.md`: 1 and `vendor/…/project-split.md`: 4, noted (Core text); `.dev/issue-31-…`, `.dev/issue-32-…`: historical |
| K6 | `review-required-read-only` | 0 | `CHANGELOG.md`: 1, `docs/design-proposal.md`: 6, `docs/requirements/REQ-007-core-authority.md`: 1, `docs/requirements/log.md`: 1, `skills/dev-core/SKILL.md`: 1, `skills/dev-core/deltas.md`: 1; all changed (new) |
| K7 | `engineering-workflow-core#23` | 0 | `CHANGELOG.md`: 1, `docs/design-proposal.md`: 4, changed or historical (D-031 item 6 named the record; D-032 is it); `docs/core-feedback.md`: 4, noted (CF entry for #23; its status line moves in PR-2 with the pin) |
| K8 | `discard the result` | 0 | hits only under `.dev/issue-106/` |
| K9 | `Around each review` | 0 | hits only under `.dev/issue-106/` |

Co-change rule 1: `--name-only` lists `REQ-007-core-authority.md`,
`REQ-024-agent-write-and-delete.md` and `log.md` (exit 0); the `-U0` diff of
`log.md` has `+|` rows for REQ-007 and REQ-024 and no `-|` row (exit 0).

`scripts/validate.sh`: exit 0, "all checks passed" (399 tests before the
test fix; the new test file and `test_core_checks` pass).

PR-1 reviews run under the rules at the base (the plugin loads from `main`):
D-032 and the new R-REV-1 check apply from the merge of PR-1 on.

## Card I106-C3

The user's own message in this session (2026-11-09): 「C3 a」. R-REV-1 and
D-032: a change that edits a reviewer agent file, the pins, D-032 or a rule
that D-032 covers counts under D-032 only with a new, quoted decision of the
user for that change, recorded in it. This replaces the narrowed exclusion of
DR2-01 (`reviews/design-round-1.md`). PR-3 asks the user for that decision before
its first review.

Re-run before the PR-1 commit (2026-11-09, after the fix rounds and
staging): K1 to K9 exit 0. Changed counts only: K2 `D-032`: CHANGELOG 6,
design-proposal 8, REQ-024 3, `log.md` 3, test 7; K3 `CB-5`: REQ-024 2 (its
note names CB-5); dispositions unchanged. A tenth string `C3 a` was tried and
dropped: with `-i` it matches unrelated text. Co-change rule 1: the
`--name-only` list is REQ-007, REQ-024 and `log.md` (exit 0); `log.md` has
three `+|` rows (REQ-007, REQ-024, REQ-024 fix round) and no `-|` row.

## PR-1 redesign: a generic acceptance record (2026-11-09, design v2)

Source: the orchestrator's message to this session, 2026-11-09, which
quotes the user: 「同意，照你的建議改走第2條」. An earlier message of the same
day ("remove Bash", 「同意，那就拿掉bash。…」) is void; its survey was
stopped. The Issue #106 body was updated at 2026-11-09T05:36:28Z (`gh issue
view 106 --json updatedAt`); its "Scope change (2026-11-09)" section has both
decisions and the new Scope item 2. A later orchestrator message adds the
user's request: 「README裡是否也要寫上原因？…畢竟這是因為原生功能的一種妥協，
不是你和我不願意做。」 (relayed). Design v1 had a design review (DR3, both
lanes); v2 applies its findings (`reviews/design-round-3.md`).

Why (the official pages `code.claude.com/docs/en/sandboxing.md` and
`…/sub-agents.md`, relayed by the orchestrator; this session reads both
pages before the README text is written): a sandbox is a setting of the
whole session, off by default; a subagent inherits the main session's
setting and its front matter has no sandbox key; a plugin agent ignores
`permissionMode`, `hooks` and `mcpServers`. Without Bash the reviewers would
keep only Read: the subagents of this host list `Bash` and `Read` and no
separate `Grep` or `Glob` (`.dev/issue-69-readonly-tools-check/plan.md:99-112`).

### Design v2

1. Record: its own file `.dev/reviewer-acceptance.json`, read only at the
   bound base, never in the working tree or at the head (the base read of
   `platform_profile`; a separate file leaves `platform_profile.py` and its
   key list unchanged, DR3-D-02, DR3-S-07). Exactly these keys:
   - `version`: integer, equal to `ACCEPTANCE_VERSION` of the check script.
   - `account`: the GitHub login of the user (compared without case).
   - `repository`: `owner/name` (compared without case).
   - `decision`: the user's own words, the date, and a public place or
     "Claude Code session" (no path, session ID or host name; DR3-S-08).
   The texts that Core :29 asks for (write channels, reason, detection, what
   it misses, protected resources, rules, what it does not exempt) are the
   pack's text of that version, in one reference file (item 3). The record
   accepts that text by its version (inference: a versioned pointer meets
   "記錄"; card I106-C4 shows it to the user). One account per record
   (card I106-C6).
2. Check: `skills/dev-core/scripts/reviewer_acceptance.py`.
   - `check --base <full base ID>`: reads the record from the base with
     `git --no-replace-objects cat-file blob <base>:.dev/reviewer-acceptance.json`;
     the base contract of the read-back script (40 or 64 lowercase hex, and
     `git rev-parse --verify <base>^{commit}` equals the literal, else
     `STOP BAD_ARGS`); the parse contract of `platform_profile.py` (no
     duplicate keys, exactly the keys above, types); compares `account` with
     `gh api --hostname github.com user --jq .login` and `repository` with
     `gh repo view --json nameWithOwner --jq .nameWithOwner` run at the top
     level of the worktree under review; `version` with the constant.
   - `validate --file <path>`: format and version of a record file only, for
     the head record before its merge; prints `VALID` or `INVALID <CODE>`; it
     never qualifies a reviewer (DR3-D-01).
   - Output: exactly one line on stdout (`PASS`, `STOP <CODE>` with
     `BAD_ARGS`, `GIT`, `NO_RECORD`, `BAD_RECORD`, `VERSION`, `ACCOUNT`,
     `REPOSITORY`, `GH`, `INTERNAL`); stderr stays empty; every exception and
     subprocess failure becomes a code; subprocesses get `stdin=DEVNULL` and
     a time limit; no value read is printed (DR3-S-03, DR3-S-04). Exit 0 only
     for `PASS` or `VALID`.
   - In the repository of the pack, the main agent runs the base copy
     (`git --no-replace-objects cat-file blob <full base ID>:skills/dev-core/scripts/reviewer_acceptance.py | python3 -I - check --base <same full base ID>`),
     as `references/readback-gate.md` says for the read-back script (the
     base found with `git merge-base`, the literal checked in the command
     text). Elsewhere it runs the copy on the skill path.
3. Rule text in one place: `skills/dev-core/references/reviewer-acceptance.md`
   (read in full, part of R-REV-1): the record format and template, the
   check and its outcomes, the protected resources, the write channels, the
   reason, the detection (CB-4), what it misses, what it does not exempt,
   the setup-change rule (item 5), and the version history. A test pins the
   SHA-256 of this file, of the CB-4 and CB-5 bullets and of the `tools` and
   `disallowedTools` lines of both reviewer agent files to
   `ACCEPTANCE_VERSION` (DR3-S-01, DR3-D-03). A change of any of them fails
   the test until the version is raised or the pinned digest is updated;
   both need the user's decision for that change (item 5). A raised version
   makes every record stop with `STOP VERSION` until its owner accepts again.
4. R-REV-1 (no account or repository name, DR3-D-05): a required reviewer
   counts only without an effective write channel, or under the project's
   acceptance record when the check prints `PASS` (read the reference in
   full). The pack reviewers keep Bash, so they count only under the record.
   The record does not apply when the task, the brief or a project policy
   names another protected resource or requires technical isolation; it
   covers only `dev-reviewer` and `dev-security-reviewer`; an agent with
   write tools never counts (DR3-S-02, DR3-D-04). Anything but `PASS`: the
   review stays incomplete, the dependent gate stops, safe independent work
   may go on, and the main agent gives the user a decision card; it never
   adds or edits a record on its own (DR3-D-04). CB-4 runs around each
   review and scan.
5. Setup change (card I106-C3 (a), generalized). "The change" is all work
   from the bound base to the candidate, staged and working tree included.
   - When it adds or edits `.dev/reviewer-acceptance.json` and nothing else
     (`git --no-replace-objects diff --name-only <base>` plus the index and
     the working tree list only that file), the user's new decision for this
     change replaces a base `STOP NO_RECORD`, `BAD_RECORD`, `VERSION`,
     `ACCOUNT` or `REPOSITORY`; never `BAD_ARGS`, `GIT`, `GH` or `INTERNAL`.
     Before its merge, `validate` on the head file prints `VALID`. This is
     the path of the first record and of each re-acceptance (DR3-D-01,
     DR3-S-05, DR3-S-06).
   - When it edits a reviewer agent file, `READ_ONLY_AGENTS` of
     `scripts/check_pack.py`, the check script, the reference or a pinned
     digest, its reviews and scans need the check's `PASS` and the user's new
     decision for this change.
   - The decision is quoted and recorded in that change, with the change it
     is for (branch or PR). Card I106-C5 decides whether it must be the
     user's own message in the dispatching session.
6. This repository's record: `.dev/reviewer-acceptance.json` with version 1,
   `jeffery777`, `jeffery777/claude-dev-skills` and the user's words to
   card I106-C4. D-032 becomes "this repository's record by the generic
   mechanism" (the decision, the binding, the pointer); its field texts move
   to the reference. PR-1's own reviews run under the base rules (the
   record is not at the base yet).
7. README (one section, both languages; the template is only in the
   reference, the README points to it, REQ-022): why the reviewers keep Bash
   (tests, Git commands, search; no separate Grep or Glob on some hosts);
   why no read-only sandbox (session-wide setting, subagents inherit it, no
   front matter key; links to the two pages); the residual risk and what
   CB-4 sees and misses; optional user hardening that the pages document
   (a session sandbox, `permissions.deny`), at the user's own risk; how to
   create the record, the prerequisites (GitHub, `gh` logged in, network,
   card I106-C6), what `STOP` means; that a narrowing of the record on main
   reaches a branch only after a rebase (DR3-S-10); that the design is
   re-assessed when Claude Code offers a read-only mode for one subagent.
8. Kept from PR #107: CB-4 (exit-status check, `NOT_RUN`, void and keep the
   record), CB-5 (isolation sentence) with "the project's acceptance record
   (R-REV-1)" instead of D-032, DL-004 (`tighten` until the vendor bump,
   names no account or repository), DL-009 row and note.
9. Removed: the account check with its literals in R-REV-1, the literal
   names in DL-004, CB-5, the REQ-007 and REQ-024 notes, and the PR #107
   test assertions on the literal check; `tests/test_reviewer_acceptance.py`
   pins the script outputs, the digest-to-version tie and this
   repository's record instead; `check_pack` pins stay.
10. "No account or repository name in the shared rules" (Issue Done when):
    read as "no account or repository that a record binds". At the base,
    `skills/dev-retro/SKILL.md:140`, `:141` and `:191` name the Core
    repository as the destination of feedback, and the vendored Core names
    its owner; they stay (DR3-D-06; the orchestrator confirms the reading).
    A deterministic `git grep -n -F` over `skills agents scripts` for the
    login lists only those lines after PR-1.
11. Records: REQ-024 and REQ-007 get sources for the new decision (relayed,
    with the Issue body as source) and for the card answers; `log.md`
    appends rows; CHANGELOG entry rewritten; search list K rows for
    `D-032`, the login, `reviewer_acceptance`, `bound environment`, `this
    account` (DR3-D-05).
12. Not done: a sandbox for the reviewers (not possible for a plugin);
    FU-004 stays open: Bash is accepted as a write channel; non-GitHub hosts
    and several accounts per repository (card I106-C6; follow-up when
    chosen).

### What a new installer does

Create `.dev/reviewer-acceptance.json` from the template in the reference,
with the user's own words, in a change that touches only that file; its
reviews count with the user's decision for that change; `validate` passes
before the merge. After the merge, the check prints `PASS` for that account
and repository until the pack raises the version.

### Cards (`cards-3.md`)

- I106-C4: accept this repository's record (version 1 texts).
- I106-C5: whether the decision for one change must be the user's own
  message in the dispatching session.
- I106-C6: the limits of version 1 (GitHub with `gh` only; one account per
  repository).

### Design v3: amendments from round 4 (DR4)

These amendments replace the named parts of design v2. Triage:
`reviews/design-round-3.md`, section "Round 4".

- Item 2: `validate` is deleted (over-design 1). A wrong record that merges
  fails closed (`STOP BAD_RECORD`) and is fixed by a record-only change;
  this repository's record is pinned by a test. `check` is the only mode;
  exit 0 only for `PASS`.
- Item 3: the sentences that apply the record (item 4) live in the
  reference; R-REV-1 keeps one sentence and a pointer, so the digest covers
  them (DR4-02). The pinned ranges: the whole reference file; the lines
  from `- **CB-4**` to the line before `- **CB-6**` of `skills/dev-core/SKILL.md`
  as LF bytes; the raw `tools` and `disallowedTools` lines that
  `check_pack.py` reads (DR4-09). Version rule in the reference: a change of
  the meaning of a pinned text, or of any tool line, raises the version; only
  a change that keeps the meaning (a cite, a line number, a typo) updates the
  digest, with the reason in the version history (DR4-02).
- Item 4: the main agent runs `check` before each required review or scan;
  only one stdout line `PASS` with exit 0 counts (DR4-11).
- Item 5, one list (DR4-01; card I106-C3 (a)): when the change adds or edits
  the record, a reviewer agent file, `READ_ONLY_AGENTS`, the check script,
  the reference, a pinned digest or a rule that the record covers (the
  apply sentences, CB-4, CB-5), its reviews and scans count only with a new
  decision of the user for this change; a change that is not record-only
  also needs `PASS`. For a record-only change, that decision also replaces a
  base `STOP NO_RECORD`, `BAD_RECORD`, `VERSION`, `ACCOUNT` or `REPOSITORY`,
  never `BAD_ARGS`, `GIT`, `GH` or `INTERNAL`. An added or moved cite or line
  number is no change. "Record-only" (DR4-03): the three lists
  `git --no-replace-objects -c core.quotePath=false diff --name-only --no-renames --no-relative --ignore-submodules=none -z <base>`,
  the same with `--cached`, and `git ls-files --others --exclude-standard -z`
  together hold exactly `.dev/reviewer-acceptance.json`. The record's
  `decision` field is the record of the decision for a record-only change;
  the commit message names the branch or PR; that change commits no other
  file, state files included; the decision covers only the record content
  shown on the card, and a later edit needs a new decision (DR4-04).
- Item 7, README: the "what CB-4 sees and misses" part points to the
  reference instead of repeating it (over-design 2). The optional hardening
  stays short (the user asked for the reasons; the orchestrator's note) and
  says: it acts on the whole session, the main agent included; it does not
  replace the record; a sandbox that blocks the network makes the check
  `STOP GH`. "No separate Grep or Glob" keeps its mark: a subagent's own
  report, not a harness list (DR4-10).
- Item 10 (DR4-08): correction: `skills/dev-retro/SKILL.md:140`, `:141` and
  `:191` name this pack's repository (the feedback destination), not the
  Core repository (`git grep -n -F` at the base). Reading of the Done-when
  line: "no account or repository name that binds or checks an acceptance".
  The orchestrator confirms the reading.
- Residual (DR4-05): a full commit ID of the change passed as the base lets
  a change qualify itself; outside the pack repository there is one literal
  only. It goes to card I106-C4 (fact), the reference ("what it misses") and
  the scope of FU-063; the user decides by the card.
- "What a new installer does": no `validate` step.

Orchestrator's answers (its message to this session, 2026-11-09): (1) the
Done-when reading "no name that binds or checks an acceptance" is right;
the dev-retro feedback destination is outside it. (2) The cards are not
shown yet: the orchestrator relays them and offers the user another
direction for C6 (C6 (a) would block commits off GitHub or offline, behind
the current main, DL-045). No implementation until the user decides C6;
then the user answers C4 and C5 in this session.

## PR-1 design v4: the acceptance record on the user's own machine (2026-11-09)

Source: the orchestrator's message to this session, 2026-11-09, with the
user's words (relayed): 「技能本身本來就不應該綁帳號和repo，這是我的認知，否則
會造成其它問題對嗎？」; on the base risk of card C4: 「這應該無論是AI Agent或是人
都有可能犯錯，所以能以工作流程加以規範，將可能性降到最低嗎？」; on a record on
the user's machine: 「同意，如果是上游的engineering-workflow-core有問題，那麼要開一個
Issue回饋給上游，我讓codex修改」. Design v4 replaces design v2 and its v3
amendments where they differ; their findings stay as history.

Core check (Core v0.5.0 `review-and-security.md:29-35`, read from the tag of
the local clone): the record must be traceable to the user's explicit
decision, bind the environment and the rules, and record the write
channels, the reason, the detection and what it misses; each review checks
that the record applies and runs the detection; a change of the
environment or the rules needs a new acceptance; the acceptance of another
environment or consumer never applies. Core does not say where the record
lives, and does not ask that it is in the repository or visible in a PR
(`:29-35`; `review-evidence` asks only that the review lists the commands
run and their results). So a record on the user's machine meets Core; no
upstream Issue is needed (inference from the text; no Core sentence names a
place).

Facts tested in this session (2026-11-09): the Bash tool of the agent has
no terminal: `sys.stdin.isatty()` and `sys.stdout.isatty()` are `False`, and
opening `/dev/tty` fails with errno 6 (ENXIO).

### Design v4

1. Record: one JSON file per clone, outside every repository, at
   `~/.claude/dev-skills/reviewer-acceptance/<id>.json`. `<id>` is the
   SHA-256 of the real path of `git rev-parse --path-format=absolute
   --git-common-dir`, so all worktrees of one clone share it, and another
   clone, another machine or another user has none. Keys, exactly:
   `version` (integer, equal to `ACCEPTANCE_VERSION`), `decision` (the
   user's own words), `date`. No account, repository name or path is
   stored or printed. Works offline, on any Git host, without a remote, and
   for each user of a shared repository (each has their own home folder).
2. Create: only the user, in their own terminal:
   `python3 <pack root>/skills/dev-core/scripts/reviewer_acceptance.py accept`
   at the top level of the clone. It prints the version text summary (the
   reference, item 4), reads the user's words from `/dev/tty`, and writes
   the file. Without a terminal (`/dev/tty` cannot be opened) it prints
   `STOP NO_TTY` and writes nothing, so an agent's Bash cannot run it. The
   agent never creates, edits or deletes the record by any means
   (R-REV-1). Residual: an agent error that writes the file with another
   tool is not stopped by the script; R-REV-1 forbids it, and the user sees
   the file's date and words when they run `accept` again or open it.
3. Check: `reviewer_acceptance.py check`, run by the main agent at the top
   level of the worktree under review before each required review or scan.
   It finds the record by the same `<id>`, checks the keys and the version,
   and prints exactly one stdout line: `PASS`, or `STOP <CODE>` with `GIT`,
   `NO_RECORD`, `BAD_RECORD`, `VERSION` or `INTERNAL`; stderr stays empty;
   exit 0 only for `PASS`. No `--base`, no `gh`, no network. The main agent
   runs the copy on the skill path (CB-6); in the pack's own repository the
   plugin loads from `main`, so a change under review does not run its own
   script (CB-6 Limit stays as residual risk).
4. Reference `skills/dev-core/references/reviewer-acceptance.md` (read in
   full; part of R-REV-1): the Core :29 texts (write channels, reason,
   detection CB-4, what it misses, protected resources, what it does not
   exempt), the record, `accept` and `check`, and the version history. The
   digest test of design v3 stays: the reference, the CB-4 and CB-5 lines
   and both reviewer tool lines are pinned to `ACCEPTANCE_VERSION`; a change
   of meaning or of a tool line raises the version, and every record then
   gives `STOP VERSION` until its user runs `accept` again.
5. R-REV-1 (one sentence and a pointer; no account or repository name): a
   required reviewer counts only without an effective write channel, or when
   `check` prints `PASS`; the record does not apply when the task, the brief
   or a project policy names another protected resource or requires
   technical isolation; it covers only `dev-reviewer` and
   `dev-security-reviewer`; an agent with write tools never counts; anything
   but `PASS` keeps the review incomplete and the dependent gate stopped,
   and the main agent tells the user how to run `accept`. CB-4 runs around
   each review and scan.
6. Setup change (card I106-C3 (a)): when the change under review edits a
   reviewer agent file, `READ_ONLY_AGENTS`, the script, the reference, a
   pinned digest or a rule that the record covers, its reviews and scans
   need `PASS` and a new decision of the user for this change; card I106-C5
   decides where that decision must be given. An added or moved cite or line
   number is no change. The record-only path of v2 and v3 is gone (the
   record is not in the repository).
7. Removed from v2 and v3: `.dev/reviewer-acceptance.json`, the base read and
   `--base`, the `gh` comparisons, the account and repository fields, the
   DR4-05 residual, the DR4-03 name-only commands, card I106-C6. If a later
   step needs a base, it gets it with a fixed command, never a typed ID.
8. This repository: D-032 records the user's decision to use the generic
   mechanism and to accept the residual risk on their own machine (the
   user's words to card I106-C4); the record itself is the user's local
   file, made by `accept` after PR-1 merges. D-032 names no account,
   repository or path.
9. README (both languages, one short section): why the reviewers keep Bash;
   why no read-only sandbox for one subagent (the two official pages, read
   by this session before writing); the residual risk with a pointer to the
   reference; optional user hardening that the pages document, at the
   user's own risk, acting on the whole session; how to run `accept` and
   what each `STOP` means; that moving or re-cloning a repository needs a
   new `accept`; re-assessment when Claude Code offers a read-only mode for
   one subagent.
10. Kept from PR #107 and v3: CB-4 (exit-status check, `NOT_RUN`, void and
    keep the record), CB-5 (isolation sentence, "the user's acceptance
    record (R-REV-1)"), DL-004 (`tighten` until the vendor bump, no names),
    DL-009, the digest test, the search list rows.
11. Tests: `accept` refuses without a terminal; `check` outputs for a
    missing, malformed or old-version record and for `PASS`, with a
    temporary home folder and temporary repositories; the digest-to-version
    tie; `check_pack` pins.

### Cards (`cards-3.md`, rewritten)

- I106-C4: accept the residual risk of the reviewer write channel on your
  machine (version 1 text), and run `accept` yourself after PR-1 merges.
- I106-C5: whether the decision for a setup change must be the user's own
  message in the dispatching session.
- I106-C6: deleted (no GitHub or account limit remains).

### Design v4.1: amendments from round 5 (DR5)

These amendments replace the named parts of design v4. Triage:
`reviews/design-round-3.md`, section "Round 5".

- Item 1, key (DR5-05 (a)): `<id>` is the SHA-256 of the real path of the
  common Git directory together with its `st_dev` and `st_ino`; a re-clone at
  the same path, a restored home folder or another machine gives
  `NO_RECORD` (fails closed). A file system with unstable inode numbers can
  give a false `STOP` (unverified).
- Item 2, `accept` (DR5-03, DR5-04, DR5-08, DR5-11): it runs only when
  `sys.stdin.isatty()` and `sys.stdout.isatty()` are both true, else
  `STOP NO_TTY` and no write; it prints the pinned acceptance section of the
  reference word for word (`STOP` if the reference is missing); it reads the
  user's words from stdin, then asks for the exact answer `yes`; anything
  else, an empty line, end of input or an interrupt writes nothing
  (`STOP DECLINED`); it writes the file atomically; it prints no clone path
  and no file name. What the gate stops: an agent that runs `accept`
  directly in a tool without a terminal. What it does not stop: a
  pseudo-terminal, another tool that writes the file, or a host where the
  agent's shell keeps a terminal (unverified); the rules forbid all of them.
  The README says: run `accept` in a separate terminal, not through Claude
  Code.
- Item 3, `check` (DR5-10, DR5-12, DR5-14): the parse contract of v2 stays
  (no duplicate keys, exactly the three keys, `type(version) is int`, a
  non-empty `decision`, every failure a code, `stdin=DEVNULL`, a time limit,
  no value printed); it runs as `python3 -I`; the main agent runs it in the
  same Bash command as the CB-4 commands before the review, so the recorded
  HEAD shows the tree it ran in. The sentence "the plugin loads from main"
  is replaced by "the CB-6 Limit applies; item 6 covers a change that edits
  the script".
- Item 4, pinned ranges (DR5-01): add the `## Read-back` section of
  `skills/dev-retro/SKILL.md` (from that heading to the line before
  `## capture`, LF bytes), which holds the exit-status rule of CB-4. The
  reference gets one mapping sentence (DR5-13): in Core :21-31 "路徑" is the
  reviewer path (R-REV-1 covers only the two named reviewers, and the tool
  lines are pinned); the environment is the clone key; the resources are the
  reference list and the cases where the record does not apply (inference).
  The reference also says (DR5-11): the main agent reads the record only
  through `check`; the folder, the file name and the content never go into a
  record or a post.
- Item 6, setup change (DR5-02, restores card C3 (a)): when the change under
  review (all work from the bound base to the candidate, staged and working
  tree included) edits a reviewer agent file, `READ_ONLY_AGENTS`, the
  script, the reference, a pinned digest, D-032 or a rule that the record
  covers, its reviews and scans need `PASS` and a new decision of the user
  for this change, quoted and recorded in this change. The decision also
  says whether the version is raised (a change of the reviewer body text,
  for example the no-write instructions, raises no version by itself; open
  note of DR5). Card I106-C5 decides only where the decision is given.
- Item 7: the sentence on "a later step needs a base" is deleted
  (over-design 1).
- Cards: C4 gets the facts of DR5-04, DR5-05, DR5-06 and DR5-07; C5 (b) gets
  the recording sentence.
- Issue body (DR5-09): Scope item 2 says "in their own project" and "D-032
  becomes the record of this repository only"; v4 keeps the record on the
  user's machine and D-032 as the decision entry. The orchestrator updates
  the Issue body before the implementation.

Orchestrator (its message to this session, 2026-11-09): it withdrew its
idea of dropping `st_dev` and `st_ino` from `<id>`; the key of v4.1 and card
C4 stay as they are. It updated the Issue #106 body for DR5-09 and relayed
cards C4 and C5 to the user; the user answers them in this session.

The user's own message in this session (2026-11-09): 「C4 a，C5 b」. C4 (a):
the user accepts the residual risk of the reviewer write channel (version 1
text) and runs `accept` in this clone after PR-1 merges. C5 (b): the
decision for a setup change counts only as the user's own message in the
session that dispatches the review, quoted with its date and the change it
was given for, and recorded in the change (MR107B-01).

## PR-1 redesign completeness checks (2026-11-09, on the index, before the reviews)

Same command form as above. Files under `.dev/` get no rows.

| ID | String | Exit | Rows (path: count, disposition, reason) |
| --- | --- | --- | --- |
| K10 | `D-032` | 0 | `skills/dev-core/SKILL.md`: 1, `skills/dev-core/deltas.md`: 2, `skills/dev-core/references/reviewer-acceptance.md`: 2, `skills/dev-core/scripts/reviewer_acceptance.py`: 1, changed (the decision entry, no binding); `docs/design-proposal.md`: 4, changed (D-032 rewritten); `docs/requirements/REQ-007-core-authority.md`: 2, `REQ-024-agent-write-and-delete.md`: 3, `log.md`: 3, `CHANGELOG.md`: 1, `tests/test_reviewer_acceptance.py`: 1, changed |
| K11 | the owner login | 0 | `skills/dev-retro/SKILL.md`: 3, noted (feedback destination; outside the Done-when reading, confirmed by the orchestrator); `README.md`: 6, `.claude-plugin/*.json`: 4, `LICENSE`: 1, `CHANGELOG.md`: 2, `docs/design-proposal.md`: 4, `REQ-009`: 1, `REQ-026`: 3, noted (links and authorship, not a binding); `REQ-007`: 1, `REQ-024`: 1, historical (the C1 (a) source locator; the REQ-007 note says that C4 (a) supersedes it, and the REQ-024 note and locator say so since MR107B-02); `tests/test_reviewer_acceptance.py`: 1, changed (asserts the login is absent from the rule files); `vendor/…`: noted (Core text) |
| K12 | `reviewer_acceptance` | 0 | `README.md`: 2, `CHANGELOG.md`: 2, `docs/design-proposal.md`: 4, `REQ-024`: 1, `log.md`: 1, `skills/dev-core/deltas.md`: 1, `references/reviewer-acceptance.md`: 4, test: 5; changed (new) |
| K13 | `bound environment` | 0 | hits only under `.dev/` |
| K14 | `this account` | 1 | no hit |
| K15 | `gh api user` | 0 | `tests/test_reviewer_acceptance.py`: 1, changed (asserts absence in the rule files) |
| K16 | `reviewer-acceptance.json` | 0 | `tests/test_reviewer_acceptance.py`: 1, changed (asserts absence) |

Co-change rule 1: REQ-007, REQ-024 and `log.md` change; `log.md` gets `+|`
rows for REQ-007 and REQ-024 (run again before the commit).
`scripts/validate.sh`: exit 0, 409 tests OK (3 skipped).

## Open notes (follow-up candidates, not fixed in PR-1)

From the Merge Review of head `92492bf` (relayed by the orchestrator,
2026-11-09), below the merge threshold:

- A repository without a commit fails CB-4 (`git rev-parse HEAD`), so its
  reviews never count until the first commit.
- `check` needs Git 2.31 or later (`--path-format`); an older Git gives
  `STOP GIT` (fail closed).
- README says that the design is assessed again when Claude Code offers a
  read-only mode for one subagent; no follow-up names that trigger yet.

## PR-3 implementation (2026-11-09)

Later changes (2026-11-10): cards I106-C8 (d), C9 (a), C10 (a) and C11 (a)
replace parts of this section: push step 2 and step 5 keep the base text (no
destination test of URL forms, no allow path), PR and Issue metadata and ref
names are read, and the acceptance version is 3 (record key without `st_dev`).
The review record `reviews/pr3-round-1.md` has the details.

Branch `issue-106-pr3-publication-data` from main `1ae24b5` (PR #107 merged).
Setup change: PR-3 edits the body of `agents/dev-security-reviewer.md` (not
its tool lines); the user's own message in this session to card I106-C7
(`cards-4.md`): 「C7 a」 (agree; the acceptance version stays 2). The rules
of the merged base apply: `reviewer_acceptance.py check` prints `PASS` in
this clone before each required review and scan.

Changes: R-REV-9 (scope, payload, destination, signing settings, look-for
list, SEC105B-01 clause, `-----BEGIN ` pattern), push step 2 (destination
test), `skills/dev-implement/SKILL.md` and `agents/dev-security-reviewer.md`
copies, REQ-011 notes, DL-050, CHANGELOG, `tests/test_publication_data.py`,
README version wording (MR107C-02, SEC107C-01), ID rename P1DR-01
(MR107C-01).

Completeness checks (index): K20 `SEC105B-01` (exit 0): all hits changed;
K21 `machine hostnames` (exit 0): `docs/design-proposal.md` 1, historical;
K22 `PRIVATE KEY` (exit 0): `skills/dev-core/SKILL.md` 1 (the signing
sentence, "no private key"), noted; `tests/test_rule_slimming.py` 1, noted
(the sample still matches `-----BEGIN `); K23 `stays for it alone` (exit 0):
only the new test that asserts its absence; K24 `review-publication-data`
(exit 0): all changed; K25 `Look for keys` (exit 0): SKILL.md and the agent
file, changed; K26 `counts as no scan` (exit 0): `docs/design-proposal.md` 1
and REQ-009 1, historical (they state the Issue #95 rule; the REQ-011 note
now says it holds for each scan). Co-change rule 1: REQ-011 changes; the
`log.md` row for REQ-011 is in this change. `scripts/validate.sh`: exit 0,
416 tests.

## PR-3 completeness checks before the commit (2026-11-10, index)

Command form as above, from the top of the worktree; files under
`.dev/issue-106/` and `vendor/` get no rows.

| ID | String | Exit | Rows (path: count, disposition, reason) |
| --- | --- | --- | --- |
| K20 | `SEC105B-01` | 0 | `CHANGELOG.md`: 1, `REQ-011`: 1, `log.md`: 1, `skills/dev-core/SKILL.md`: 1, `skills/dev-core/deltas.md`: 1, `tests/test_publication_data.py`: 1; all changed |
| K21 | `machine hostnames` | 0 | `docs/design-proposal.md`: 1, historical (an earlier decision text) |
| K22 | `PRIVATE KEY` | 0 | `skills/dev-core/SKILL.md`: 1, noted ("no private key … is read"); `tests/test_rule_slimming.py`: 1, noted (sample matched by `-----BEGIN `); `.dev/issue-1-phase1/…`: 1, historical |
| K23 | `stays for it alone` | 0 | `tests/test_publication_data.py`: 1, changed (asserts absence) |
| K24 | `review-publication-data` | 0 | `CHANGELOG.md`, `REQ-011`, `log.md`, `skills/dev-core/SKILL.md`, `skills/dev-core/deltas.md`, `tests/test_publication_data.py`: 1 each, changed |
| K25 | `Look for keys` | 0 | `agents/dev-security-reviewer.md`: 1, `skills/dev-core/SKILL.md`: 1, changed |
| K26 | `counts as no scan` | 0 | `REQ-011`: 2 (one changed note, one unchanged Issue #95 note, noted: the Issue #104 note now says it holds for each scan); `docs/design-proposal.md`: 1, `REQ-009`: 1, historical; `CHANGELOG.md`, `log.md`, `SKILL.md`, `deltas.md`, test: 1 each, changed |
| K27 | `st_dev` | 0 | `reviewer-acceptance.md`: 2, `reviewer_acceptance.py`: 1, `tests/test_reviewer_acceptance.py`: 1, changed (C10); `model_effort_readback.py`: 3, `references/model-effort-readback.md`: 1, `deltas.md`: 1 (DL-046), `docs/design-proposal.md`: 2, `REQ-009`: 1, `tests/test_platform_profile.py`: 1, `tests/test_review_loop_rules.py`: 1, noted (the read-back repository check, unrelated); `.dev/issue-4-…`, `.dev/issue-96-pr3/…`: historical |
| K28 | `STOP VERSION` | 0 | `reviewer-acceptance.md`: 2, `tests/test_reviewer_acceptance.py`: 1, noted (true for a version raise without a key change) |
| K29 | `names the repository of the task` | 0 | `tests/test_publication_data.py`: 1, changed (asserts absence) |

Co-change rule 1: `--name-only` lists REQ-011 and `log.md` (exit 0); the
`-U0` diff of `log.md` has three `+|` rows for REQ-011 (one per round) and no
`-|` row. `scripts/validate.sh`: exit 0.

## PR-2 implementation (2026-11-10)

Branch `issue-106-pr2-vendor-bump` (local `issue-106-pr2`) from main
`9d17e9c` (PR #108 merged). Not a setup change: no reviewer agent file,
`READ_ONLY_AGENTS`, script, reference `reviewer-acceptance.md`, pinned
digest, D-032 or covered rule changes; R-REV-1 gets an added cite only.
`reviewer_acceptance.py check`: `PASS` (the user ran `accept` again after the
merge). Floor check: transcript effort `high`, `opus` tier 3 at the base.

Cards: `cards-8.md`, I106-C12 (a) and I106-C13 (a), the user's own messages
in this session (2026-11-10): 「C12 a」, 「C13 a」. Design of C12, MR108-02 and
MR108-03: `pr2-c12-design.md` (v2); design review round 1:
`reviews/pr2-design-round-1.md` (P2D-01 to P2D-08).

Deferred from PR #108 by the user (「merge，全部延到 PR-2」, relayed):
MR108-01 (cards C12, C13), MR108-02, MR108-03, MR108-04 (DL-050, CHANGELOG,
REQ-011 sources), MR108-05 (FU-007 Trigger), MR108-06 (below), SEC108-01
(`cards-6.md`: the device numbers and the date are gone), SEC108-02
(`test_old_version` also tests an older version), the README sentence on a
disk copy or an image restore.

MR108-06, correction of the PR #108 body (a merged PR body is not edited):
the body says "three narrow confirmations and one narrow review of the last
NIT fixes". The record (`reviews/pr3-round-1.md`) has the deep and the
security review of round 1 and two narrow confirmations (P3-R2, P3-R3); the
fixes of the two P3R3 NITs had no narrow review before the commit. The commit
scan and the merge-time reviews of PR #108 covered the head.

Vendor: `git -C <clone> archive v0.5.0`, extracted into a new empty folder,
then copied into `vendor/engineering-workflow-core/` (31 files, no symlink).
Lock rewritten; `git ls-remote origin 'refs/tags/v0.5.0*'` in the clone gave
tag object `374124ac…` and `^{}` commit `0edcbad3…` (exit 0);
`verify_core.py --upstream <clone>`: OK, 31 files.

Line citations (step 4): `git grep -lE 'workflow\.md:[0-9]' -- skills agents
docs/requirements`, then a replacement by a map that `difflib` built from the
equal lines of `contracts/workflow.md` at both tags: 56→57, 60→61, 62→63,
64→65, 72→73, 74→77, 76→79, 88→93, 90-97→95-102, 99→104, 117→122; 34
replacements in `REQ-025`, `REQ-026`, `skills/dev-core/SKILL.md`,
`deltas.md`, `dev-retro/SKILL.md`, `review-report.md`. The
`authorization-and-stops.md` lines cited (3, 21, 35, 52) did not move. The
stage map lines of `review-and-security.md` 33 and 37 moved to 61 and 65.
Cites that already named v0.5.0 (DL-004, DL-050, R-REV-1, R-REV-9) were not
changed.

Not done: step 12 (`REQ-022:55`): the line is an acceptance item of a closed
requirement; changing it would rewrite a past acceptance, so it stays.
REQ-023 gets a note instead of an acceptance change (Core v0.5.0 has three
`wf-writing` items).

Completeness checks (working tree, `git grep -c -F`, without `vendor/`,
`.dev/` and `CHANGELOG.md`; all exit 0):

| String | Rows (path: count, disposition) |
| --- | --- |
| `v0.1.1` | `docs/core-feedback.md`: 11, noted (its items stay at v0.1.1; a note says the pin moved); `docs/design-proposal.md`: 2, changed (the parity note); `REQ-018`: 1, changed (moved to a note); `log.md`: 1, historical; `deltas.md`: 1, changed (DL-051 names the old items) |
| `--dry-run --porcelain` | `push-scan.md`: 2, changed; `dev-implement/SKILL.md`: 1, changed; `docs/design-proposal.md`: 2, historical (D-015 text); `push_precheck.py`: 1, noted (docstring; the script reads the saved output only, Issue Out); tests: 4, noted or changed |
| `spot-check` | `SKILL.md`: 2, `deltas.md`: 2, `source-map.md`: 2, changed or noted; `REQ-023`: 1, noted (a note added) |
| `R-WRT-2` | `SKILL.md`, `deltas.md`, `source-map.md`, `task-brief.md`, `dev-docs/SKILL.md`: changed |
| `push.pushOption`, `oid sha256` | `push-scan.md`, `deltas.md`, `REQ-011`, the test: changed |

Co-change rule 1: REQ-011, REQ-018, REQ-023, REQ-025 and REQ-026 change; each
has a new `log.md` row. `scripts/validate.sh`: exit 0, 421 tests (3 skipped),
before the reviews.
