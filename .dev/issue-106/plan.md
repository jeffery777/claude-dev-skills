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
