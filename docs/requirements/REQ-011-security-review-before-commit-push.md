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
  - type: chat
    locator: "Claude Code session 2026-10-25 (orchestrator session, relayed to the R-REV-9 backlog session, Issue #52), user decision on the FU-019 priority"
    quote: "FU-019 恢復一般優先，和 FU-017 同列 backlog"
  - type: chat
    locator: "Claude Code session 2026-10-25, D-019 design card C6 (orchestrator relay): the R-REV-9 backlog PR (Issue #52) comes before the D-019 spec"
    quote: "C7 選 a；C1a C2a C3a C4a C5a；C6 先做 R-REV-9 backlog PR"
  - type: chat
    locator: "Claude Code session 2026-10-25 (orchestrator session, relayed to the R-REV-9 backlog session, Issue #52), user answer to cards RB-C1 (FU-017 in a separate PR after this one) and RB-C2 (finding S1-001: a configuration check before the dry-run)"
    quote: "RB-C1 選 b，RB-C2 選 b"
  - type: chat
    locator: "Claude Code session 2026-10-25 (orchestrator session, relayed to the R-REV-9 backlog session, Issue #52), user answer to card RB-C3 (findings S2-001 to S2-003: the configuration check does not cover `GIT_CONFIG`, legacy remotes and branches files or Git before 2.18; claims narrowed) and to the proposed rule for the next round"
    quote: "RB-C3 選 a，也同意下一輪的約定"
  - type: chat
    locator: "Claude Code session 2026-10-25 (orchestrator session, relayed to the FU-017 session, Issue #54), user answer to card FU017-C1 (commit and tag signatures: stop condition)"
    quote: "C1 選 b"
  - type: chat
    locator: "Claude Code session 2026-10-25 (orchestrator session, relayed to the FU-017 session, Issue #54), user answer to card FU017-R1-C1 (finding S1-002: an encoding that is not ASCII-compatible; claim narrowed)"
    quote: "R1-C1 選 a"
  - type: chat
    locator: "Claude Code session 2026-10-25 (orchestrator session, relayed to the FU-017 session, Issue #54), user answer to round-2 cards FU017-R2-C2 (finding S2-001: tag signature inside the last message line; check changed) and FU017-R2-C3 (findings R2-001, R2-002, S2-003: an allowed signature finding is Rejected for this push) and extras 1 to 4 (R2-003, S2-002, S2-004, round-3 convention)"
    quote: "R2-C2 選 a，R2-C3 選 a，附帶 1–4 同意"
  - type: issue
    locator: "GitHub Issue #68 body, Goal (user decisions of 2026-10-27 on cards E1 and E2 and item 4 of the cost proposal)"
    quote: "E1 選 A，E2 同意"
  - type: chat
    locator: "Claude Code session 2026-10-27 (orchestrator relay), user answer to the Issue #68 design cards I68-C1 to I68-C7"
    quote: "I68-C1a、C2a、C3a、C4a、C5b、C6a、C7a"
  - type: chat
    locator: "Claude Code session 2026-10-27 (orchestrator relay), user answer to the Issue #68 review round 1 cards I68-R1-C1 (finding R1-009: the log -p views without --ignore-submodules=none) and I68-R1-C2 (finding S1-003: which copy of scan_records.py runs)"
    quote: "R1-C1a、R1-C2c 加 b（檢查寫在 script 外）"
  - type: chat
    locator: "Claude Code session 2026-10-27 (orchestrator relay), user answer to the Issue #68 review round 2 card I68-R2-C1 (R-VER-2 stop: a bounded round 3 in which the reviewer computes every input of the binding itself; if round 3 shows a new blocker in the binding mechanism, fallback (c))"
    quote: "R2-C1a，.pyc 可刪"
  - type: chat
    locator: "Claude Code session 2026-10-28 (orchestrator relay), user answer after Issue #68 review round 3 (finding R3-001, a new blocker in the binding mechanism): fallback (c) with option (c1), the record and binding subcommands removed with their tests"
    quote: "繼續，c1"
  - type: chat
    locator: "Claude Code session 2026-10-28 (orchestrator relay), user answer to the Issue #68 review round 4 REQ-GAP S4-002 (the commit-scan hash command has no --ignore-submodules=none)"
    quote: "commit 掃描也加，這個 PR 修"
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
  before a force or delete that it can cause, the main agent stops the push
  for the user's decision (the configuration check before the dry-run and
  the `+`/`-` dry-run check; FU-019, card RB-C2b, Issue #52), within the
  coverage that R-REV-9 states (its "Not covered" list, card RB-C3a).
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
  output is data). They are not a commit-time or push-time scan. Apart from
  R-AUTH-1, this pack does not implement these inbound controls.
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
  this form force or delete; since Issue #52 the main agent stops such a
  push within the coverage that R-REV-9 states: a configuration check
  before the dry-run and a `+` or `-` dry-run line, FU-019), and any change
  restarts the checks; the main
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
- Issue #52 (FU-019, MS49-001, MS49-002, MS49-003, MR49-001; cards
  PR2-R2-C1a, RB-C2b and RB-C3a and the FU-019 priority decision): the URL check sends the
  error output of `git remote get-url` to `/dev/null`, counts the fetch and
  the push URL lines and prints only PASS or STOP; the error output of
  `ls-remote`, the dry-run and the push goes into no brief, record or post;
  before the dry-run, the main agent stops at a configuration check
  (`remote.<remote>.mirror` true, or a `remote.<remote>.push` value that
  starts with `+` or is `:<dst>`), and it stops at a `+` or `-` dry-run ref
  line (R-REV-9 step 5), both also in `dev-implement`. R-REV-9 lists what
  the configuration check does not cover (the `GIT_CONFIG` environment
  variable, legacy `$GIT_DIR/remotes/` and `$GIT_DIR/branches/` files, Git
  before 2.18), which the user accepted (card RB-C3a). Temporary-repository tests show
  `transfer.credentialsInUrl=warn` (only PASS on stdout), a fetch URL with a
  trailing newline (STOP), a missing remote (STOP), and
  `git remote add --mirror=push`, `remote.<name>.push=+…` and
  `remote.<name>.push=:…` stopped while an ordinary push is not. For the
  configuration check they show a push mirror (`git remote add --mirror=push`),
  `+refs/heads/*:refs/heads/*`, `+refs/tags/*` and `:refs/heads/<name>`
  stopping, and an ordinary remote and `:` (matching) passing; and a race
  case with `+refs/heads/*:refs/heads/*` and with a push mirror, where the
  configuration check stops the push before any dry-run, while without the
  check (control) a dry-run shows no `+` or `-` line and the real push, after
  another clone changed a remote ref, force-updates or deletes it. The
  reviewer agent
  file does not repeat the new checks; this is an author decision that
  follows card PR2-C2a (the push form).
- Issue #54 (FU-017; card FU017-C1b): when the push scan view (R-REV-9
  step 8) has a line that starts with `gpgsig `, `gpgsig-sha256 ` or
  `mergetag ` (a commit header; the view indents message lines), or a
  scanned tag has a line that starts with `gpgsig` or `-----END ` or
  contains `-----BEGIN ` (card FU017-R2-C2a: a message without a trailing
  newline puts the signature block inside the last message line), the
  reviewer reports a blocking finding with the disposition Needs Human
  Decision. It lists each such commit or tag and the kind of signature, and
  it does not decode the signature. The checks use `awk`, not `grep`,
  because `grep` can treat the view as binary when it has a NUL byte and
  then print no line. The main agent stops at step 5, and the user decides
  whether the identity of the signing key may be published. When the user
  allows it, the main agent records the signature finding with the
  disposition `Rejected`, with the user's answer as the source and the
  reason (card FU017-R2-C3a). The answer covers only the commits and tags
  of that scan and push. When the scan has no other open finding, the
  R-REV-9 scan counts as passed, and the main agent continues at step 9.
  After any change, the main agent starts again at step 1. A signature
  finding blocks the push until the user allows it. The merge-readiness
  range scan reports signatures in the same way. The user decides as in
  step 5 whether the identity of the signing key may be published; an
  allowing answer is recorded the same way and covers that range.
  The reviewer agent file carries the step-8 detection sentences and the
  range sentence (not step 5), and `dev-implement` step 4 says that a
  signed commit or tag stops the push. The commit scan shows no signature:
  Git adds it when it creates the commit, and the push scan reports it
  (with `commit.gpgsign=true`, the staged view has no signature line and
  the commit object has one; security reviewer check). R-REV-9 lists what
  the scans do not cover: the decoded content of signatures and signatures
  that the platform adds when it creates a merge or squash commit.
  R-REV-9 also lists an `encoding` header that names an encoding that is
  not ASCII-compatible (for example UTF-16 or EBCDIC), for which the view
  can show no readable identity or signature header; the user accepted this
  case (card FU017-R1-C1a).
  Temporary-repository tests show these cases reported: OpenPGP with
  `user.signingkey` set to a fingerprint, unset, and set to an email; SSH;
  x509 with a self-signed and with a CA-issued certificate (gpgsm); a
  SHA-256 repository (`gpgsig-sha256`); a signed tag; a signed tag whose
  message has no trailing newline (`--cleanup=verbatim`); a `mergetag`
  merge; a signed commit in the range scan; and a signed commit followed by a
  commit that adds a binary file (a NUL byte in the view), in the Claude
  Code Bash shell and in bash. They show these cases not
  reported: an unsigned commit, a commit message with a `gpgsig` line, an
  unsigned tag, and a signed commit that the remote already has. A tag
  message that contains `-----BEGIN ` anywhere is reported (a false
  positive on the safe side). gitsign and smimesign were not tested (not
  installed). This acceptance replaces item 3 of the Issue #54 acceptance
  on the commit scan: by finding R1-004, the commit-scan note is a fact
  sentence in the "Before a commit" bullet, not a Not-covered item.
- Issue #68, fallback (c) (option (c1); D-021): the commit-scan view of
  R-REV-9 has `--ignore-submodules=none --submodule=short`, so that a
  gitlink change stays visible as its object IDs, and the `log -p` commands
  of push step 8 and of the merge-readiness range scan have
  `--ignore-submodules=none`, in `dev-core` and in
  `agents/dev-security-reviewer.md` (card I68-R1-C1a). The commit-scan
  hash command of `dev-gate` step 1 and `review-report.md` also has
  `--ignore-submodules=none --submodule=short`, and the agent file says so
  for the staged diff (finding S4-002; user answer
  「commit 掃描也加，這個 PR 修」). Push step 4a runs
  `skills/dev-gate/scripts/push_precheck.py verify --dry-run <file> --remote-ids <file>`
  in the worktree of the dry-run. It runs the source checks of step 7 (at
  least one ref line; one `:` per refspec; no `+`, `-` or `!` ref line; a
  known flag; names of `[A-Za-z0-9._/-]`; a source that starts with
  `refs/heads/` or `refs/tags/` or is a full object ID; an old value that is
  the start of a remote ID; a source that is a commit or a tag whose target
  is a commit) with `git --no-replace-objects`, no shell and an exit-code
  check for every Git call. It exits 0 (the checks passed) or 2
  (`STOP <reason>`, also for a Git error or an unexpected error, without a
  traceback); its output carries no identity and no path; it keeps no
  record and writes no file. Any result other than exit 0 stops the push;
  exit 0 replaces no scan, and steps 6 to 8 always run.
  Temporary-repository tests (`tests/test_push_precheck.py`, subprocesses
  with `-B`) show a passing push (new commits, a new branch and an
  annotated tag, in a SHA-1 and a SHA-256 repository; an up-to-date push)
  and each STOP case: a bad source or destination name, a source of the
  wrong kind, a tree or a tag of a tree as the source, a source that does
  not exist, a `+`, `-` or `!` ref line, an old value that is not in the
  remote IDs, bad remote IDs, bad ref lines, a missing, symlinked,
  directory or non-UTF-8 input file, a directory that is not a repository
  and an unexpected error (no bytecode written). They also show that the
  step-8 and range commands taken from `dev-core` show a gitlink change
  under `diff.ignoreSubmodules=all`, which the same command without the
  option hides. Not enabled (fallback (c)): commit-time scan records, the
  binding of the commit scan report, and a push without a reviewer scan
  (E1 A).
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
records: D-015 and, since Issue #68, D-021 in `docs/design-proposal.md`. Related: [[REQ-003]], [[REQ-007]].
