# Reviewer write channel: the user's one-time acceptance

Written per ASD-STE100 principles; full conformance not verified.

This file is part of R-REV-1. Read it in full before the first required
review or scan of a session. Core: v0.5.0 `review-and-security.md#review-required-read-only`
(tag object `374124ac6bc88efe73b27a4f7875fffd0dc669e2`), paragraphs 5 to 8.
Decision: D-032 (`docs/design-proposal.md` of the pack repository).

## Why

A required reviewer must have no effective write channel, or run under a
one-time acceptance of the user for a specific environment (Core). The pack
reviewers `dev-reviewer` and `dev-security-reviewer` keep Bash: they run
tests and the Git and read-back commands of the scans, and they search the
repository. A plugin cannot give one subagent a read-only sandbox. So they
count only under the user's acceptance record. Reading of Core :21-31
(inference): "路徑" is the reviewer path, which R-REV-1 limits to the two
named reviewers with pinned tool lines; the environment is the clone of the
record; the resources are the protected resources below and the cases where
the record does not apply.

## Accepted text (version 3)

- Write channels: Bash in `dev-reviewer` and `dev-security-reviewer`. Bash
  can write in the worktree, in `.git`, outside the repository and to the
  network (for example `gh` with the user's token: merge a PR, close an
  Issue, delete a branch, create a Release). Also any tool that the host
  gives a subagent beyond its agent file: runtime enforcement of `tools` and
  `disallowedTools` is not tested (FU-004). The agent files have
  `tools: Read, Grep, Glob, Bash` and `disallowedTools: Edit, Write, NotebookEdit`.
- Reason: the reviewers run tests and the Git and read-back commands of the
  scans, and they search the repository. On some hosts a subagent has no
  separate Grep or Glob tool (a subagent's own report), so without Bash it
  keeps only Read.
- Protected resources: the content under review in the repository of the
  change (worktree, index, refs, objects), the scan input files, and the PRs
  and Issues of that repository.
- The record does not apply when the task, the brief or a project policy
  names another protected resource or requires technical isolation. It
  covers only `dev-reviewer` and `dev-security-reviewer`. An agent with
  write tools never counts.
- Substitute detection: CB-4 (HEAD, the status hash and the diff hash before
  and after each review and scan, with the exit-status check of the
  `dev-retro` read-back; a failed or missing command is `NOT_RUN`, and the
  review or scan does not count; a detected change voids the review).
- Not covered by the detection: everything outside the worktree and the
  index: `.git` refs and objects (the content of the push and merge
  readiness scans), untracked and ignored files and edits inside an
  untracked file (the content of text scans), other worktrees, the checkout
  from which the plugin is loaded (CB-6 Limit), effects outside the
  repository, network and platform writes, a change that is undone before
  the after-check, the time outside the review, and changes of the host
  permission settings (owner: the user; not checked each time). Equal values
  before and after do not prove that nothing changed.
- Not exempted: independence of author and reviewer, the real review, the
  required scans, exact-head, data protection, operation authority and
  higher requirements. The acceptance gives no reviewer the right to change
  the content under review. It is never recorded as technical read-only.

## The record

One JSON file per clone, outside every repository:
`~/.claude/dev-skills/reviewer-acceptance/<id>.json`. `<id>` is the SHA-256
of the real path and `st_ino` of the clone's common Git directory
(`git rev-parse --path-format=absolute --git-common-dir`), so all worktrees
of one clone share it; another clone or another user has none, nor has
another machine, a re-clone at the same path or a restored home folder where
the file system gives a new inode number (unverified on file systems that
reuse inode numbers). The device number (`st_dev`) is not used: it can change
at a reboot (card I106-C10). Residual: the same path on another disk with the
same inode number reuses the record. Keys,
exactly: `version` (integer, equal to `ACCEPTANCE_VERSION` of the script),
`decision` (the user's own words), `date`. No account, repository name or
path is stored.

Only the user creates it, in their own terminal, at the top level of the
clone:

```bash
python3 -I <pack root>/skills/dev-core/scripts/reviewer_acceptance.py accept
```

`accept` runs only when stdin and stdout are a terminal (else `STOP NO_TTY`
and no write). When the clone already has a record, it first prints that
record's date and words (or one line saying that the record is missing or
unreadable), so the user sees what the new record replaces. It prints the
"Accepted text" section of this file, reads the
user's own words, and writes the record atomically only after the exact
answer `yes` (else `STOP DECLINED`). It prints no clone path and no file
name. The gate stops an agent that runs `accept` in a tool without a
terminal. It does not stop a pseudo-terminal, another tool that writes the
file, or a host where the agent's shell keeps a terminal (unverified); the
rules below forbid all of them.

## The check

Before each required review or scan, the main agent runs at the top level
of the worktree under review, in the same Bash command as the CB-4 commands
that run before the review:

```bash
python3 -I ${CLAUDE_SKILL_DIR}/../dev-core/scripts/reviewer_acceptance.py check
```

It prints exactly one line on stdout and nothing on stderr: `PASS` (exit 0),
or `STOP GIT`, `STOP NO_RECORD`, `STOP BAD_RECORD`, `STOP VERSION` or
`STOP INTERNAL` (exit 1), or `STOP BAD_ARGS` (exit 2). Only `PASS` with exit
0 counts. Anything else, no output, a check that did not run, or a case where
the record does not apply (above) keeps the review incomplete and the
dependent gate stopped; safe independent work may go on. `dev-reviewer` and
`dev-security-reviewer` keep Bash, so they count only under the record.
`accept` prints `ACCEPTED` (exit 0) or `STOP NO_TTY`, `STOP GIT`,
`STOP NO_REFERENCE`, `STOP DECLINED`, `STOP INTERNAL` (exit 1). The main agent then tells the
user how to run `accept` (`NO_RECORD`, `VERSION`), with the resolved pack
root (`${CLAUDE_SKILL_DIR}/../dev-core/../..`) in the chat only, or what failed. A review
record gives only the result line. The CB-6 Limit applies to the copy of the
script that runs; the setup-change rule covers a change that edits it.

## Rules for the agent

- The agent never creates, edits, moves or deletes the user's record, by any
  tool or command, and never runs `accept`. (Tests that use a temporary home
  folder are not the user's record.)
- The agent reads the record only through `check`. The record folder, the
  file name and the record content never go into a record, a brief or a
  post.

## Setup change (card I106-C3 (a); card I106-C5 (b))

"The change" is all work from the bound base to the candidate, staged and
working tree included. When it edits a reviewer agent file,
`READ_ONLY_AGENTS` in `scripts/check_pack.py`, `reviewer_acceptance.py`,
this file, a pinned digest of `tests/test_reviewer_acceptance.py`, D-032 or
a rule that the record covers (the sentences of R-REV-1 that apply it, CB-4,
CB-5, the `dev-retro` read-back), its reviews and scans count only with
`PASS` and a new decision of the user for this change: the user's own
message in the session that dispatches the review, quoted with its date and
the change it was given for, and recorded in this change. The decision also says whether the version is raised. An added
or moved cite or line number is no change.

## Version

A test pins the SHA-256 of this file, of CB-4 and CB-5 in
`skills/dev-core/SKILL.md`, of the `## Read-back` section of
`skills/dev-retro/SKILL.md`, and of the `tools` and `disallowedTools` lines
of both reviewer agent files to `ACCEPTANCE_VERSION`. A change of the
meaning of a pinned text, or of any tool line, raises the version; every
record then gives `STOP VERSION` until its user runs `accept` again. A change
that keeps the meaning (a cite, a line number, a typo) updates the pinned
digest only, with the reason below. Both need the setup-change decision.

| Version | Change |
| --- | --- |
| 1 | First version (Issue #106 PR-1, head `92492bf`); never in a merged pack. |
| 2 | The setup-change rule records the change that the decision was given for (Merge Review finding MR107B-01; card I106-C5 (b) has these words). The Accepted text did not change. |
| 3 | The record key drops `st_dev`, which changed at a reboot (card I106-C10 (a)); the Accepted text did not change. |
