# Review round 4 — Issue #1, Phase 1 (pre-commit, narrow confirmation)

- Target: working tree at HEAD `5229478` after the round 3 fixes.
- Reviewer: `R4`, a fresh opus subagent that did not write the change. It confirmed the round 3 fixes by reproducing the original failure scenarios, and compared the new `dev-core` wording with Core (zh-TW).
- Result: 25 of 27 round 3 items confirmed fixed. No MUST-FIX. Three SHOULD-FIX and one NIT, handled below.

| ID | Sev | Finding | Disposition |
| --- | --- | --- | --- |
| R4-01 | SHOULD-FIX | `ls-files --debug` stat data made the reviewer's own read-only `git diff` or `git status` change the fingerprint (false positive, a regression from R3-01) | Fixed: `--debug` removed; flags and staged content are still covered by `ls-files -s -v` and `diff --cached`; test with a stat-only change followed by `git diff HEAD` and `git status` |
| R4-02 | SHOULD-FIX | R-RIG-4 "required fix" class was narrower than Core (missed broken required compatibility and unacceptable regressions) | Fixed: wording now matches Core `wf-assumptions-and-options` |
| R4-03 | SHOULD-FIX | Edits to files already flagged assume-unchanged or skip-worktree were invisible, and §8 did not say so | Fixed: the fingerprint hashes the working-tree content of every flagged file; §8 and the script docstring say so; test |
| R4-04 | NIT | STATUS_DEP row in graph-schema.md not updated for R3-09 | Fixed |
| R3-21 (reopened) | NIT | Flow lists lost a quoted comma when a space came before the quote | Fixed: regex allows leading whitespace; test `[x, "b, c", y]` |

## Verification

`./scripts/validate.sh`: all checks passed (68 tests, also run with `-W error::ResourceWarning`).

## Result of round 4

- No MUST-FIX is open, and every finding has a disposition.
- A narrow independent check of these five fixes (round 5) runs before the commit gate.

## Round 5 (narrow independent check of the round 4 fixes)

Reviewer: a fresh opus subagent. No MUST-FIX or SHOULD-FIX, and no regressions. It reproduced every fix in scratch repositories, including sparse checkout, flagged paths with spaces, and deleted flagged files. `validate.sh` passed in a copy.

| ID | Sev | Note below the reporting bar | Disposition |
| --- | --- | --- | --- |
| R5-01 | NIT | A reviewer's own `git status` can clear a skip-worktree flag on a path that already exists on disk, so the fingerprint changes and the review is discarded | Rejected as a defect: it fails safe (the review is rerun, never wrongly accepted). Recorded here as a known false-positive case |
| R5-02 | NIT | `#` inside a quoted flow-list item was cut by `strip_comment` | Fixed: a flow list ends at its `]`; test |
| R5-03 | NIT | The R-RIG-4 "required fix" text did not repeat "within authority and dependency limits" | Fixed |
