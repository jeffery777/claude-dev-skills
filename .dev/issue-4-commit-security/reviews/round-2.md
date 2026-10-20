# Review round 2 — issue-4-commit-security (PR-A)

- Target: working tree at 4b75360afc9a722defbc743f9a237e550cd8ae82 (+ uncommitted, intent-to-add, 22 status entries)
- Diff identity: sha256 of `git diff HEAD --binary` = af5bcb713550ed85e899aaf8ea1bfa6691e2242036dd1020a7693d5d800515cf (both reviewers matched it before and after)
- Reviewers: `dev-skills:dev-reviewer` deep re-review (R2-A-*), `dev-skills:dev-security-reviewer` Security Diff Scan (SR2-A-*); requested model opus; effective: unknown
- Thresholds: MUST-FIX only Core relaxation, security, data loss, integrity or an unmet REQ-011 acceptance item; SHOULD-FIX needs a reproducible failure; NIT only regressions of this round or false documentation
- Round-1 dispositions: verified Fixed by the reviewers except where listed below
- Result: 1 MUST-FIX, 2 SHOULD-FIX, 3 NIT (R2-A-001 and SR2-A-003 are the same defect)
- Reviewer side effects (no tracked change, diff hash unchanged): an ignored `__pycache__` file, and unreferenced loose blobs from a scratch index copy (`git gc` removes them)

## Findings and dispositions

| ID | Severity | Finding | Disposition |
| --- | --- | --- | --- |
| R2-A-001, SR2-A-003 | MUST-FIX | The `.git` refusal in `evidence_file_ref` is case-sensitive; on case-insensitive APFS `.GIT/config` was accepted (path + hash only) | Fixed: case-insensitive part comparison; test (skipped on case-sensitive filesystems); docs say "any letter case" — superseded, see "Re-evaluation after round 2" below |
| R2-A-002 | NIT | SR-A-005 had two dispositions (R-REV-3) | Fixed: split into SR-A-005a (Fixed) and SR-A-005b (Rejected) in round-1.md |
| SR2-A-001 | SHOULD-FIX | `--binary` shows binary or `-diff` files only as encoded data, so a secret in them passes the scan | Fixed: every R-REV-9 scan command uses `--text --no-textconv --no-ext-diff`; binary and LFS-tracked paths are listed and inspected, or the work stops for the user — superseded, see "Re-evaluation after round 2" below |
| SR2-A-002 | SHOULD-FIX | The push dry-run is not tied to the real push arguments (`--tags`, `--follow-tags`, `--all`) | Fixed: the main agent runs the dry-run with exactly the real push arguments and pushes with exactly those; the gate binds the push command; the reviewer never runs fetch or push |
| SR2-A-004 | NIT | A parent folder swapped between `realpath` and `lstat` records an outside file's hash; docs claimed this was fixed | Fixed in code and docs: `realpath` is re-checked after the open (test); the remaining short race window is documented as residual risk in FU-003, graph-schema.md and D-015 — superseded, see "Re-evaluation after round 2" below |

## Residual risk (recorded, not findings)

- Record placement has no explicit end: the last record (for example the Merge Review comment) lives in the PR and is scanned as PR text before posting.
- An R-REV-9 scan does not replace an R-REV-7 Security Diff Scan for trust-boundary changes.
- The platform's squash author email cannot be shown by git before the merge; set subject, body and author explicitly at merge and read the commit back.
- Not named in R-REV-9: push options (`-o`), issue comments, release notes, submodule pushes, timestamps and UTC offset. Release notes and tags come with the first release (after FU-001).
- `fetch --prune` prunes only inside the fetch refspec. Windows is untested. gitleaks: NOT_RUN (capability UNAVAILABLE, installing needs approval).

## Verification evidence

80 unit tests OK; `check_core_coverage.py` OK (21 anchors, 41 rules); `check_pack.py` OK. The reviewers ran the named git commands in scratch repos (git 2.54.0).

## Re-evaluation after round 2 (stop rule, user decision 2026-10-20)

The user asked to stop before the commit and re-evaluate: fix only what a
requirement covers, and turn gaps into decisions (D-013.2, D-013.3, D-016,
applied ahead of PR-B). The D-013.5 stop rule was treated as triggered: the
`--evidence-file` checks needed fixes and produced new findings in two rounds
in a row. Round 3 was stopped before it reported.

| Finding | requirement_relation | Classification | New mechanism | Final disposition |
| --- | --- | --- | --- | --- |
| DR-A-001, SR-A-003 FIFO hang | in-scope (chosen option: regular file) | necessary fix | no | Fixed (lstat regular-file check before open) |
| DR-A-002, SR-A-002 merge/squash commit, tags | in-scope (published commits; push sends tags) | necessary fix | no | Fixed |
| DR-A-002, SR-A-002 PR text | gap | needs human decision → user chose "add" (card 1 a) | no (instruction) | Fixed; REQ-011 source added |
| DR-A-003 rescan loop | in-scope | necessary fix | no | Fixed |
| DR-A-004, SR-A-001, SR2-A-001 merge content, encoded binaries | in-scope | necessary fix | no | Fixed (`--cc`, `--text --no-textconv --no-ext-diff`); the binary/LFS inspection clause was removed (no requirement) |
| DR-A-005, -006, -007, -010, -011, -012, -014 | in-scope (rules disagreed or docs were false) | necessary fix | no | Fixed |
| DR-A-008, SR-A-006 identity read | in-scope (SEC-01 cause) | worth improving | no | Fixed |
| SR-A-007, SR2-A-002 exact push arguments | in-scope | necessary fix | no | Fixed |
| SR-A-008 masking | in-scope (records are committed or posted) | worth improving | no | Fixed |
| DR-A-009, SR-A-004, SR2-A-004 check/open race | no-requirement (hash only) | SCOPE-CREEP | yes | Rejected; the inode and re-resolve checks and their tests were removed (user decision) |
| SR-A-005a, R2-A-001, SR2-A-003 `.git` (any case) and hardlink refusal | no-requirement (hash only) | SCOPE-CREEP | yes | Rejected; checks and tests removed (user decision); the round-2 MUST-FIX no longer applies |
| SR-A-005b gitignored files | in-scope, accepted risk | keep as is | no | Rejected (residual risk) |
| Signed-commit headers, ref names (added in round 2) | no-requirement | SCOPE-CREEP | no | Removed |

`evidence_file_ref` now keeps: a project root, no symlink, no path outside the
project, regular files only. REQ-011 records the user's correction of the
first quote ("不會被上傳").

## Narrow confirmation and pre-commit scan (C-A)

- Reviewer: `dev-skills:dev-security-reviewer`; bound to staged diff sha256 a15326d3e7036d40f5a8929dc775425c67f89535bf2e26f50092091206aa1543
- Job A confirmed the simplified `evidence_file_ref` (no content, absolute or `../` path recorded; refusals work; FIFO does not hang) and the R-REV-9 wiring
- R-REV-9 pre-commit scan of that candidate: PASSED (noreply identity, `user.useConfigOnly` true, no hooks, message clean)

| ID | Severity | requirement_relation | Finding | Disposition |
| --- | --- | --- | --- | --- |
| C-A-001 | SHOULD-FIX | in-scope | The correction quote in REQ-011 used `\"` escapes, which the pack's front-matter parser cuts at 13 characters | Fixed: single-quoted scalar; parses to the full 102 characters |
| C-A-002 | NIT | no-requirement | Review-record cells still said "Fixed" for removed checks | Fixed: those cells are marked superseded |
| C-A-003 | question | gap | "Tests cover each refusal": missing-file and no-root refusals had no test | Fixed: two short tests for existing behavior (the acceptance text was written by the agent, not the user; no new mechanism) |

The fixes make a new candidate; it gets its own pre-commit scan.
