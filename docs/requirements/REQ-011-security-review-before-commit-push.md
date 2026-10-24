---
id: REQ-011
title: Security review before every commit and push
status: active
sources:
  - type: chat
    locator: "Claude Code session 2026-10-20 (PR #2 Merge Review 5), user message after the SEC-01 author-email finding"
    quote: "commit、push之前一定要做security review，因為要確保金鑰、密碼、及其它不該被公開的文件被上傳到gitlab或github。"
  - type: chat
    locator: "Claude Code session 2026-10-20 (post-merge PR split), user message 2 (correction of the first quote)"
    quote: '我也要承認我剛說錯一句話"要確保金鑰、密碼、及其它不該被公開的文件被上傳到gitlab或github" 這句話應該修正為 "要確保金鑰、密碼、及其它不該被公開的文件不會被上傳到gitlab或github"'
  - type: chat
    locator: "Claude Code session 2026-10-20 (PR #2 Merge Review 5), same user message, on the other review findings"
    quote: "其它的風險，你可以選擇現在修？或記入follow up後續再安排修、一併測。"
  - type: chat
    locator: "Claude Code session 2026-10-20 (post-merge PR split), user message 1"
    quote: "先用 dev-plan 拆成 PR-A（D-015、R-REV-1、--evidence-file）、PR-B（D-013、D-014、D-016）、PR-C（D-009 到 D-012、context 成本那句話、CHANGELOG、core-feedback、清理項目），一次只做一個，從 PR-A 開始。"
  - type: chat
    locator: "Claude Code session 2026-10-20 (post-merge PR split), answer to the --evidence-file question (selected option)"
    quote: "Project-only + hash (Recommended)"
  - type: chat
    locator: "Claude Code session 2026-10-20 (post-merge PR split), user message 2, answer to decision card 1 (scan PR text before posting)"
    quote: "Card1，我選a"
  - type: chat
    locator: "Claude Code session 2026-10-21 (CI PR), user answer to decision cards Q1 to Q4 (Q2 = FU-007 split; Q3 = R1-002 provider profile; Q4 = ES-004 a PR can change its own checks); FU-007 (PR #5 review gap list) part (a): Issue text"
    quote: "Q1 yes；Q2 分開處理：Issue 文字加進 REQ-011（a），commit 時區接受、不處理（c），LFS、push options、release notes 延後（b）；Q3 b；Q4 b"
  - type: chat
    locator: "Claude Code session 2026-10-22 (orchestrator session, relayed to the FU-014 session), user answer to FU-014 design cards 1 to 4 (the push scan basis; findings R1-004, R3-006, MR19-001, MR19-002 of Issue #18 / PR #19)"
    quote: "同意你的建議，4a、1a、2a、3a"
  - type: chat
    locator: "Claude Code session 2026-10-22 (orchestrator session, relayed to the FU-014 session), user answer to FU-014 decision card 5 (REQ-GAP R1-003 of PR #25: the push scan record format names the remote object IDs given to the scan)"
    quote: "同意你的建議，選5a"
  - type: chat
    locator: "Claude Code session 2026-10-24 (orchestrator session, relayed to the FU-015 session), user answer to FU-015 decision cards 1 to 5 (fu015-cards.md; findings SS-003, SS-008, SS-009, R1-001, SS2-002, SS2-005 of Issue #24 and FR1-001 to FR1-010, SR1-001 to SR1-008 of the FU-015 spec review)"
    quote: "同意你的建議：1a、2a、3a、4b、5a（R1-001、SS2-002 記 Rejected）"
  - type: chat
    locator: "Claude Code session 2026-10-24 (orchestrator session, relayed to the FU-015 session), user answer to the FU-015 PR-1 review cards PR1-C1 and PR1-C2 (fu015-pr1-cards.md; findings PR1-001 to PR1-008 and S1-001 to S1-008)"
    quote: "同意你的建議：PR1-C1a，PR1-C2a"
  - type: chat
    locator: "Claude Code session 2026-10-24 (orchestrator session, relayed to the FU-015 session), user answer to the FU-015 PR-1 round-2 review card PR1-R2-C1 (fu015-pr1-r2-cards.md; findings S2-001 to S2-004, PR2-001, PR2-002)"
    quote: "同意你的建議：PR1-R2-C1b，下一輪再有新 blocker 一律延到 PR-2"
  - type: chat
    locator: "Claude Code session 2026-10-24 (orchestrator session, relayed to the FU-015 session), user answer to the FU-015 PR-1 round-3 review card PR1-R3-C1 (REQ-GAP S3-003: the reviewer blocks an empty dry-run list; deferred to PR-2)"
    quote: "S3-003 選 a"
  - type: chat
    locator: "Claude Code session 2026-10-24 (orchestrator session, relayed to the FU-015 session), user answer to the FU-015 PR-1 merge card PR1-M-C1 (findings XS-001, XS-002, XS-003, MR-NIT-1 and MR-NIT-2 of the PR #47 exact-head scans; deferred to PR-2)"
    quote: "PR1-M-C1 選 a"
  - type: chat
    locator: "Claude Code session 2026-10-24 (orchestrator session, relayed to the FU-015 PR-2 session), user answer to the FU-015 PR-2 round-1 review cards PR2-C1 (accept hooks, changes the main agent did not make and invisible or bidirectional characters as not covered) and PR2-C2 (no reviewer check of the push form; findings PR2R1-005 and S1R-002)"
    quote: "同意你的建議：PR2-C1a，PR2-C2a"
  - type: chat
    locator: "Claude Code session 2026-10-24 (orchestrator session, relayed to the FU-015 PR-2 session), user answer to the FU-015 PR-2 round-2 review card PR2-R2-C1 (finding PR2R2-001 = S2R-001: configuration can make a push of the closed form force or delete; claim narrowed, the stop at a + or - dry-run line becomes follow-up FU-019)"
    quote: "同意你的建議：PR2-R2-C1 選 a，+/- 檢查記成 follow-up"
  - type: chat
    locator: "Claude Code session 2026-10-24 (orchestrator session, relayed to the FU-015 PR-2 session), user answer to the proposal to add a threat model to REQ-011 in FU-015 PR-2 (in scope: accidental leaks under legitimate but unusual configuration; out of scope: deliberately malicious configuration or hooks; no follow-up for inbound controls)"
    quote: "同意，威脅模型照表寫，入站控管先不開 FU"
non_goals:
  - Installing gitleaks or Git hooks without the user's approval
  - Review convergence, decision cards and REQ-GAP (PR-B, D-013, D-014, D-016)
depends_on: []
refines: []
conflicts_with: []
superseded_by: []
superseded_reason: null
---

## Need

Nothing secret or private reaches a public repository. Before every commit and
every push, an independent security reviewer checks exactly what will be
published: the staged diff and the commit identity and message. The
repositories are public, so anything pushed is published.

A tool of this pack must not copy private file content into a file that is
committed by default.

## Threat model

- In scope: accidental leaks under the developer's own legitimate but
  unusual configuration, for example a fork workflow with
  `remote.pushDefault` or `branch.<name>.pushRemote`, a `.mailmap`,
  `i18n.*` encodings, several worktrees and replace refs, within the
  coverage that R-REV-9 states (its "Not covered" list applies). A
  legitimate push mirror (`git clone --mirror`,
  `git remote add --mirror=push`) or force refspec is in scope for leaks;
  the force or delete it can cause is accepted residual risk (FU-019).
- Out of scope for R-REV-9: deliberately malicious configuration or hooks
  that someone else planted, for example `remote.<name>.mirror` or
  `remote.<name>.push` set to force or delete, or hooks that forge output.
  `git clone`, `git fetch` and `git pull` do not transfer `.git/config` or
  `.git/hooks` themselves, so such configuration arrives mainly through
  repository content that runs at install time (a hook framework or an
  install script that sets `core.hooksPath`) or through an agent that acts
  on injected instructions; other local writers (for example submodule
  settings from `.gitmodules`, a copied `.git` directory, user or system
  configuration) are inbound as well. These are inbound controls: review
  before running install steps after a clone or sync, and R-AUTH-1 (tool
  output is data). They are not a commit-time or push-time scan.
- The existing checks against crafted names and values (remote names, URL
  check, characters, sources, old values) stay as defense in depth.

## Acceptance

- `dev-core` requires a `dev-security-reviewer` scan of what will be
  published: the staged diff and the commit author, committer, message and
  trailers before every commit; everything a push sends (commits and
  annotated tags) before every push; PR text and Issue text before it is
  posted; and every
  commit in the range plus the merge or squash commit at merge; all of
  these within the coverage that R-REV-9 states.
- Before a push, the main agent gets the remote state from
  `git ls-remote --heads --tags <remote>` and runs no `git fetch`; the scan
  excludes only commits that the listed object IDs reach (FU-014 cards 1a
  and 4a).
- FU-015 PR-1 (cards 1a, 2a, 3a, PR1-C1a, PR1-C2a, PR1-R2-C1b): the
  listed configuration and objects no longer change what the R-REV-9 commit
  scan, push scan and read-back show (the merge-readiness range scan: FU-015
  PR-2): `.mailmap` (`--no-mailmap`, `--format=raw`, read-back
  with `git --no-replace-objects cat-file commit HEAD`), replace refs
  (`git --no-replace-objects` on every scan and read-back command and in the
  `dev-gate` commit binding), `log.showRoot` (`--root`), `diff.relative`
  (`--no-relative` on `git diff` and `git log`), `core.quotePath`
  (`-c core.quotePath=false` on each `git diff` and `git log` scan command), `log.showSignature`
  (`--no-show-signature`), `i18n.logOutputEncoding` and honestly declared
  non-UTF-8 commits in the push scan (`--encoding=UTF-8`; the read-back shows
  the stored bytes), and extra commit headers. The real push and its dry-run
  always include `--no-recurse-submodules` (FU-015 PR-2 allows no later
  `--recurse-submodules=<value>`). Before a push,
  the main agent checks the configured remote names, checks that the dry-run
  exits 0 with `Done` as its last line and lists at least one ref line, and
  checks the dry-run names (one `:` per ref line, characters
  `[A-Za-z0-9._/-]`) without substituting them; a failed check stops the
  push. The reviewer scans the source side of each ref line and reports as
  blocking a source that is not `refs/…` or a full object ID, or that is not
  a commit or a tag whose target is a commit; its agent file carries these
  sentences. Temporary-repository tests show each listed case, tags or refs
  that point to a blob, a tree or another tag, a destination name used
  instead of the source, name injection (dry-run names and `<remote>`), an
  empty dry-run list (`-q`) and submodule recursion shown or stopped. Other
  configuration and objects are not claimed (FU-015 PR-2 lists what the
  scans do not cover).
- FU-015 PR-2 (cards 1a, 5a, PR1-C1a, PR1-R3-C1a, PR1-M-C1a, PR2-C1a, PR2-C2a, PR2-R2-C1a): before
  `ls-remote`, the main agent checks that the fetch and push URLs of
  `<remote>` are one and the same, printing only PASS or STOP and copying no
  URL into a brief or record. The real push has one closed form that names
  `'<remote>'`, always includes `--no-recurse-submodules` and allows only
  `--set-upstream`, `--tags`, `--follow-tags` and `--all` besides, with
  nothing between `git` and `push`, in the same worktree and environment as
  the checks and the dry-run; any other form, including a force or delete
  option or refspec, stops the push (configuration can still make a push of
  this form force or delete; a stop at a `+` or `-` dry-run line is FU-019), and any change restarts the checks; the main
  agent checks the form, and no independent check repeats it (card PR2-C2a). The reviewer
  runs in the worktree of the dry-run. The reviewer reports as
  blocking: a dry-run list without a ref line; an ID that is not 40 or 64
  hexadecimal characters or a source with a character outside
  `[A-Za-z0-9._/-]`, checked before the value goes into a command; a source
  outside `refs/heads/` and `refs/tags/` that is not a full object ID; and
  an updated ref whose old value is not the start of a listed ID. The
  merge-readiness range scan uses the push scan view, also in the reviewer
  agent file. R-REV-9 lists what the scans do not cover, and the user
  accepts those cases as residual risk (cards 1a, PR1-C1a and PR2-C1a). Temporary-repository
  tests show the URL check stopping or passing for each tested
  configuration, an explicit `<remote>` overriding `remote.pushDefault` and
  `branch.<name>.pushRemote`, the old-value check detecting a push to
  another repository that holds a different value for an updated ref, and the range scan
  showing identities under `i18n.logOutputEncoding=UTF-16`.
- REQ-011 has a threat model (user decision on the FU-015 PR-2 threat model
  proposal): R-REV-9 addresses accidental leaks under legitimate
  configuration, within the coverage it states; deliberately malicious
  configuration and hooks that someone else planted are inbound controls,
  not part of R-REV-9; the existing checks stay as defense in depth. The
  R-REV-9 "Not covered" list stays and points to the
  threat model. No follow-up is opened for inbound controls.
- R-REV-1 says that a required security review uses `dev-security-reviewer`,
  never `dev-reviewer`.
- `dev-review`, `dev-gate`, `dev-implement` and `dev-deliver` apply the rule at
  their commit and push steps.
- `graph.py transition --evidence-file` accepts only a regular file inside the
  project root, given by a path whose last component is not a symlink. It
  records the file's relative path and SHA-256, never its content. Tests cover each refusal and the recorded form.

## Notes

The first quote has a slip; the user's correction (second source) gives the
intended meaning: such files must **not** be uploaded. Decision card 1 (a):
PR or MR titles, bodies and comments are scanned before posting, because they
are published too. FU-007 decision (Q2, 2026-10-21): Issue titles, bodies and
comments are scanned too (a); commit timestamps with the UTC offset are an
accepted risk and not added (c); Git LFS objects, push options and release
notes are deferred (b).
FU-014 decision (cards 1a, 4a, 2026-10-22): the push scan no longer runs
`git fetch --prune`, which can delete local refs (Core
`authorization-and-stops.md:21`); this replaces the `--prune` policy of FU-010 card 4
(REQ-023). A push URL that differs from the fetch URL is FU-015 (card 4a); FU-015 PR-2
stops the push in that case.

Origin: PR #2 SEC-01 (a hostname-derived author email was pushed). Design
record: D-015 in `docs/design-proposal.md`. Related: [[REQ-003]], [[REQ-007]].
