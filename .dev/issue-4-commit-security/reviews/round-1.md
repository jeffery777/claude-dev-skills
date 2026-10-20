# Review round 1 — issue-4-commit-security (PR-A)

- Target: working tree at 4b75360afc9a722defbc743f9a237e550cd8ae82 (+ uncommitted, intent-to-add)
- Diff identity: sha256 of `git diff HEAD --binary` = a616b89f60cfe6b240ac8575e5ff72dbc4eef1851b235753a60a9a480c737f32 (both reviewers matched it before and after; tree unchanged)
- Reviewers: `dev-skills:dev-reviewer` deep (DR-A-*), `dev-skills:dev-security-reviewer` Security Diff Scan (SR-A-*); requested model opus, effort from the agent definitions; effective: unknown
- Scope: all 18 changed paths. Requirement: REQ-011. DoD: REQ-011 Acceptance and graph nodes T1–T5
- Result: 0 MUST-FIX, 10 SHOULD-FIX, 12 NIT, 0 SCOPE-CREEP (overlapping findings are listed together; SR-A-005 split into a and b in round 2 per R2-A-002)

## Findings and dispositions

| ID | Severity | Finding | Disposition |
| --- | --- | --- | --- |
| DR-A-001, SR-A-003 | SHOULD-FIX | `--evidence-file` on a FIFO blocks in `os.open` before the regular-file check | Fixed: `lstat` check before opening, `O_NONBLOCK`, FIFO test — superseded, see "Re-evaluation after round 2" in round-2.md |
| DR-A-002, SR-A-002 | SHOULD-FIX | R-REV-9 does not cover the platform merge/squash commit (author, message, `Co-authored-by:`), annotated tags or PR text | Fixed: R-REV-9 covers tags before push, PR text before posting, and the merge or squash commit at merge; dev-gate merge row |
| DR-A-003 | SHOULD-FIX | Committing scan and gate records after the scan causes an endless rescan loop | Fixed: records go into a later commit or the PR, never into the commit they cover |
| DR-A-004, SR-A-001 | SHOULD-FIX | `git log -p` hides merge-resolution content and binary files | Fixed: `git log --format=fuller -p --cc --binary <ref> --not --remotes=<remote>` |
| DR-A-005 | SHOULD-FIX | The commit gate binds the working tree, the scan binds the staged diff | Fixed: dev-gate step 1 binds the staged-diff hash, identity and message (push: refs and range) |
| DR-A-006 | SHOULD-FIX | Report template has no field for the commit/push scan and still allows "not applicable" | Fixed: template mode, scan identity fields, "always applicable", masking rules |
| DR-A-007 | SHOULD-FIX | dev-implement has no gate before the push | Fixed: step 5 "Pass the `dev-gate` push gate, then push" |
| DR-A-008, SR-A-006 | NIT | No deterministic way to read the identity a commit will carry | Fixed: `git var GIT_AUTHOR_IDENT` / `GIT_COMMITTER_IDENT`, no override after the scan, read-back with `git log -1 --format=fuller`; `user.useConfigOnly` recommended with user approval |
| DR-A-009, SR-A-004 | NIT | Race between the containment check and the open can record a `../` path and an outside file's hash | Fixed: resolve once, refuse `..`/absolute relative paths, compare `lstat` and `fstat` (`st_dev`, `st_ino`); test with a mocked swap — superseded, see "Re-evaluation after round 2" in round-2.md |
| DR-A-010 | NIT | FU-003 overstated the fix and was marked Fixed before review | Fixed: FU-003 reworded (residual risks listed; set to Fixed with the merge commit after merge) |
| DR-A-011 | NIT | Stale "commit, PR or merge" text and agent descriptions | Fixed: dev-gate description, dev-deliver routing row, README (zh and EN), dev-security-reviewer description, design-proposal agent tables (zh and EN) |
| DR-A-012 | NIT | dev-review native-option paragraph ambiguous about the security reviewer | Fixed: "(`dev-security-reviewer` for a security review or scan)" |
| DR-A-013 | NIT | T1, T3, T4 moved to `done` before the independent review | Rejected: `graph.py` allows no `done -> reviewing` transition and reopening is refused while dependents have started. Correction recorded here: these nodes' review evidence is this round and its re-review. T5 stays in `reviewing` until the re-review passes. The graph is coordination data, not completion evidence |
| DR-A-014 | NIT | Exit codes and the no-root case for `--evidence-file` are undocumented | Fixed: the docstring and graph-schema.md document exit 2, `EVIDENCE_FILE_REFUSED` for a missing file, and the project-root requirement |
| SR-A-005a | NIT | Accepts `.git/*` and hardlinks to outside files | Fixed: `.git/` paths and hardlinks are refused (tests). Round 2 found the `.git` check was case-sensitive (R2-A-001) — superseded, see "Re-evaluation after round 2" in round-2.md |
| SR-A-005b | NIT | Accepts gitignored secret files inside the project; FU-003 understated the residual risk | Rejected: the user chose "Project-only + hash" (REQ-011 source); content never leaks; the hash of a short, guessable file is a recorded residual risk (FU-003, graph-schema.md, D-015), and the R-REV-9 scan shows any `file:.env` entry before a commit |
| SR-A-007 | NIT | Push range relies on HEAD and a possibly stale tracking ref | Fixed: `git fetch --prune`, `git push --dry-run --porcelain` lists the refs, each scanned with `--not --remotes=<remote>` |
| SR-A-008 | NIT | Masking only in the R-REV-9 bullet and loosely defined | Fixed: standing masking rule with a fixed format in both reviewer agents and the report template |

## Requirement trace

| REQ-011 acceptance | Covered by | Verified by |
| --- | --- | --- |
| Scan before commit, push, PR post and at merge | dev-core R-REV-9, DL-010, source-map | Reading; re-review round 2 |
| R-REV-1 names `dev-security-reviewer` | dev-core R-REV-1, dev-review | Reading; re-review round 2 |
| Skills apply the rule | dev-review, dev-gate, dev-implement, dev-deliver, both reviewer agents | Reading; re-review round 2 |
| `--evidence-file` project-only, path + hash | graph.py `evidence_file_ref`, tests, graph-schema.md, FU-003 | Unit tests; old-code failure check |

## Security scan

Applicable: yes (persistent committed data, untrusted path input, executables, commit identity, agent policy).
Status: FINDINGS in round 1 (above); the diff itself contained no secrets or private data; configured identity is a GitHub noreply address, `user.useConfigOnly` is true, no `GIT_*` identity variables.

## Verification evidence

Round 1: 75 tests OK; `check_core_coverage.py` OK (21 anchors, 41 rules); `check_pack.py` OK; the six new evidence-file cases fail on the old `graph.py`. Not run: gitleaks (not installed; installing needs approval).

## Residual risk and limits

R-REV-9 and the reviewers' read-only Bash use are enforced by instructions only (no hook). Windows was not tested. The verbatim REQ-011 quotes could not be checked by the reviewers. English text: written per ASD-STE100 principles; full conformance not verified.
