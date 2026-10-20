# Review round 3 — Issue #1, Phase 1 (pre-commit)

- Target: working tree at HEAD `5229478` after the round 2 fixes.
- Reviewer: `R3`, a fresh opus subagent that did not write the change. It ran native `/code-review` (high) on the files round 2 changed, re-checked every round 2 "Fixed" item, broke `tree_fingerprint.py` and the transition paths in scratch repositories, and compared the changed `dev-core` rules with Core (zh-TW). It reported 27 findings: no MUST-FIX and no MUST-level Core relaxation.
- Round 2 items reopened: R2S-01 (fingerprint gaps), CR-002 (the conflict precondition was too broad), CR-007 (short write and fsync), R2C-09 (multi-line plain scalars). Each is handled below.

| ID | Sev | Finding | Disposition |
| --- | --- | --- | --- |
| R3-01 | SHOULD-FIX | Fingerprint missed staged content and assume-unchanged/skip-worktree flags | Fixed: hashes `ls-files -s -v --debug` and `diff --cached`; tests |
| R3-02 | SHOULD-FIX | Linked worktree: shared config and hooks not covered | Fixed: `--git-common-dir`, plus `config.worktree`; test |
| R3-03 | SHOULD-FIX | Refs, stash, symbolic HEAD, info/, hook subfolders, nested repositories and modes not covered | Fixed: all now hashed; tests for branch, info/attributes, hook subfolder, nested repository and mode. External effects (push, forge comments, writes outside the repository) cannot be seen locally; this limit is stated in the script and in dev-core §8, with `git ls-remote` comparison where a remote matters |
| R3-04 | SHOULD-FIX | §8 claimed more coverage than the script had | Fixed: §8 lists exactly what is and is not covered |
| R3-05 | NIT | No `--no-ext-diff`/`--no-textconv`; crashed in a repository with no commits | Fixed; test |
| R3-06 | NIT | Tests used the global git config | Fixed: `GIT_CONFIG_GLOBAL=/dev/null`, `GIT_CONFIG_NOSYSTEM`, `commit.gpgsign=false` |
| R3-07 | SHOULD-FIX | REQUIREMENT_CONFLICT blocked every transition | Fixed: structural errors block all transitions; other errors block only forward moves of the affected node, or of any node for graph-level errors; parking moves (planned, blocked, cancelled) stay allowed; a transition is refused only when it adds errors; tests |
| R3-08 | SHOULD-FIX | Short write reported as success; after an fsync failure the event line stayed | Fixed: writes in a loop, truncates the log back to its original size on any failure, restores the graph; tests for both paths |
| R3-09 | NIT | `ready` nodes with unsatisfied dependencies passed validate | Fixed: STATUS_DEP covers `ready`; reopening now needs dependents moved back first (`TRANSITION_BREAKS_GRAPH`); test |
| R3-10 | SHOULD-FIX | check_pack accepted duplicate REQ ids | Fixed; test |
| R3-11 | NIT | Multi-line plain scalars were truncated | Fixed: continuation lines are joined; test |
| R3-12 | NIT | `owns` accepted paths outside the repository | Fixed: SCHEMA error for absolute paths and `..`; test |
| R3-13 | NIT | Recursion overflow on very long chains | Fixed: `GRAPH_TOO_DEEP` with exit 2 instead of a traceback |
| R3-14 | NIT | Exit codes and streams were inconsistent for unreadable input | Fixed: missing or non-object graphs give `UNREADABLE` on stderr with exit 2 for every command |
| R3-15 | NIT | File descriptor leak in `_atomic_write` | Fixed: `fchmod` runs inside the `fdopen` block |
| R3-16 | NIT | Write kinds were hard-coded | Fixed: uses `WRITE_KINDS` with a type guard |
| R3-17 | NIT | Schema doc row for REQUIREMENTS_DIR_OUTSIDE was stale | Fixed; the `owns` rule is documented too |
| R3-18 | NIT | `--upstream=path` and unknown arguments were ignored | Fixed: argparse; unknown arguments exit 2 |
| R3-19 | NIT | The tag was never resolved to the locked revision | Fixed: `--upstream` checks that the tag object and the tag's commit match the lock. Re-run 2026-10-20: match |
| R3-20 | NIT | Duplicate source-map rows overwrote each other silently | Fixed: reported as an error |
| R3-21 | NIT | Tool and path checks were narrow | Fixed: permission specifiers and `MultiEdit` are detected, flow lists keep quoted commas, and `${CLAUDE_SKILL_DIR}` references are checked in every Markdown file under each skill; tests |
| R3-22 | NIT | The fingerprint script and its test were untracked | Fixed: they are included in the commit (intent-to-add before the gate) |
| R3-23 | NIT | R-REV-1 dropped reviewer capability and qualification | Fixed |
| R3-24 | NIT | R-REV-7 omitted Core limits | Fixed: examine the boundary first; no Passed for incomplete or failed scans; result record; widen on trust-boundary change; a new candidate erases nothing |
| R3-25 | NIT | R-REV-8 omitted record fields | Fixed: source assumptions; coverage and evidence location for pending checks |
| R3-26 | NIT | R-RIG-4 omitted items | Fixed: why existing mechanisms are not enough, the later-inventory limit, research bounds, the four-way outcome classification |
| R3-27 | NIT | R-STG-4 dropped "with authorized capability" | Fixed |

## Verification

`./scripts/validate.sh`: all checks passed (21 anchors, 40 rules; 66 tests, also run with `-W error::ResourceWarning`; `claude plugin validate .` passed). `verify_core.py --upstream <clone>`: tag object, tag commit and all 14 files match.

## Result of round 3

- No MUST-FIX is open, and every finding has a disposition.
- Severity trend: round 1 had 2 MUST-FIX; rounds 2 and 3 had none, and the remaining items are edge cases.
- Round 4 is a narrow, independent confirmation of the round 3 fixes only. A review of the whole change follows as the exact-head Merge Review on the PR.
