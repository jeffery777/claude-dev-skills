# Issue #106 PR-2: design of card I106-C12 (a), MR108-02 and MR108-03

Written per ASD-STE100 principles; full conformance not verified.

Source: card I106-C12 (`cards-8.md`), the user's own message in this session
(2026-11-10): 「C12 a」. Merge Review findings of PR #108 MR108-01, MR108-02,
MR108-03 (relayed by the orchestrator; the user deferred them to PR-2).
Core v0.5.0 `contracts/review-and-security.md:81` (a required scan that did
not run or has not enough coverage never counts as passed), `:91`, `:97`,
`:99`.

No setup change: no reviewer agent file, script, reference
`reviewer-acceptance.md`, pinned digest or covered rule changes.

## C12 (a): push options and Git LFS objects

Facts:

- Push step 3 already allows no option other than four, so `-o` and
  `--push-option` on the command line stop the push.
- Git sends each configured `push.pushOption` value with a push. Tested with
  git 2.54.0 (2026-11-10, scratch repository): unset gives no output and
  exit 1; set prints the value with exit 0.
- The Git LFS pre-push hook uploads the objects that the LFS pointer files of
  the pushed commits name. The first line of a pointer file is
  `version https://git-lfs.github.com/spec/v1` (older clients:
  `https://hawser.github.com/spec/v1`). From the LFS specification; git-lfs is
  not installed here, so not tested.

Design v2 (after review round 1, `reviews/pr2-design-round-1.md`).

Proposed text, `skills/dev-core/references/push-scan.md`:

1. Step 3, after the configuration check of `<remote>`: "Git sends each
   configured `push.pushOption` value with the push, and no scan reads it, so
   the main agent also checks, without printing the values, that none is set:
   `git config --get-all push.pushOption >/dev/null 2>&1; test $? -eq 1 && echo PASS || echo STOP`
   prints `PASS` (exit 1: the key is not set; card I106-C12 (a))."
2. Step 3, the dry-run: "the real push command with
   `--dry-run --porcelain --no-verify` added after `push`" (P2D-01: no hook
   runs in the dry-run, so a Git LFS pre-push hook sends nothing before the
   scan). Step 9: "without `--dry-run --porcelain --no-verify`" (the hooks of
   the real push still run). `skills/dev-implement/SKILL.md:61` likewise.
   "Not covered", the hook item: the hook runs during the push only.
3. New step 6a: "The main agent runs the `log` command of step 8 for each
   `<source>` in the worktree of the dry-run, saves the output to a file and
   checks that the command exits 0. Then
   `LC_ALL=C grep -Ec 'oid sha256:[0-9a-f]{64}' <file>` prints `0` and exits
   1. A match is a line of a Git LFS pointer file (P2D-02: added, changed or
   deleted; any diff prefix or color): the Git LFS pre-push hook of the real
   push sends the object that a new pointer names, and no scan reads that
   object. Another count or exit code stops the push (step 5)."
   The step 8 command is not copied (one source; `tests/test_push_precheck.py`
   `rule_command` requires one copy).
4. Step 5: "or step 6a stops" joins the stop list, and one sentence: "A stop
   of step 3 for push options or of step 6a leaves the push scan `NOT_RUN`
   (Core v0.5.0 `review-and-security.md:81`): no answer counts it as passed,
   and the main agent does not push."
5. "Not covered": "push options and Git LFS objects (FU-007)" is replaced by
   the narrower item of card I106-C13 (P2D-05).
6. `skills/dev-core/deltas.md` DL-050: "Accepted residual risk: LFS objects
   and push options (FU-007 (b))" moves to "Added": the stops of step 3 and
   step 6a, and the narrower residual item. `.dev/followups.md` FU-007: (b)
   closed by card I106-C12 (a); the Trigger column drops release notes
   (MR108-05). REQ-011: a note that card I106-C12 (a) handles LFS and push
   options (P2D-08).
7. Tests in `tests/test_publication_data.py`, with an isolated Git
   environment (`GIT_CONFIG_GLOBAL=/dev/null`, `GIT_CONFIG_NOSYSTEM=1`, no
   other `GIT_*`): the push-option command from the rule text stops with
   `push.pushOption` set and passes without it; the step 6a `grep` counts a
   pointer line in an added and in a changed pointer (the sample text is
   built at run time, so that no committed line matches; P2D-07); the dry-run
   form has `--no-verify`; the old metadata sentence at line 49 changes with
   MR108-02 (P2D-08).

Residual risk for the user (card I106-C13): an LFS object that a commit
already on the remote names and that the LFS server does not have yet (step
6a reads only the commits that the remote does not have); a pointer that
the diff does not show (for example only renamed). A hook other than LFS that
sends data during the push stays in "Not covered" (hooks).

## MR108-02: metadata through the same `awk`

`skills/dev-core/SKILL.md` R-REV-9, text-scan bullet. Now: "The scan also
reads the labels, milestone and assignees that a post sets, and a push scan
reads the ref names that the push sends (card I106-C9 (a); …)". Proposed
(v2, P2D-04): "The labels, milestone and assignees that a post sets, and the
ref names that a push sends (both sides of each tab-separated ref line of the
dry-run), go into a separate text file; the same `awk` runs on it, and the
reviewer scans it (card I106-C9 (a); …)."

## MR108-03: commit-time signature exception

`skills/dev-core/SKILL.md:147`, now: "A finding blocks the commit, push or
post until it is fixed and re-scanned, or, for a signature finding (step 8),
until the user allows it (step 5)." Proposed: "… or, for a signature finding
(push step 8, or a signature that Git will make at a commit), until the user
allows it (push step 5)."
