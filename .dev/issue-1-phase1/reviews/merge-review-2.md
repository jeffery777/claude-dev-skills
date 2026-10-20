# Exact-head Merge Review 2 — PR #2 (closes #1)

- Identity:
  - base and merge-base: `5229478aead42cc2d70b7843dd5db3548c08c562`
  - head: `c72c64d42c2072b19ffe2a25a8ce9fd1e8319fa1`
  - diff: sha256 = `d93ad672c67aca371873b13c9a9d845945256e8008557ac1cd8abf3e0b1d5515` (84 files)
- Reviewer: a fresh opus subagent. It ran a complete base-to-head review with native `/code-review` (high, all findings) and native `/security-review` on the full range, focused on the changes since `9f38f06`.
  - Security: after the false-positive filter (threshold 8), there were no reportable vulnerabilities.
  - Merge Review 1 dispositions: confirmed one by one.
- Result:
  - `content_review: BLOCKED`. 17 new findings had no disposition; none was MUST-FIX.
  - `platform_enforcement: NOT_CONFIGURED`.
  - Neither result authorizes a merge.
- Deterministic checks at the head:
  - `validate.sh`: passed (73 tests).
  - `verify_core.py --upstream` against a fresh upstream clone: matched.
  - The markdown digest equals the codex-dev-skills lock.

## Findings and dispositions

The fixes form a new head, which needs Merge Review 3.

| ID | Sev | Finding | Disposition |
| --- | --- | --- | --- |
| MR2-01 | SHOULD-FIX | dev-core §8 fingerprint path still used `${CLAUDE_SKILL_DIR}/scripts` (MR-03 was incomplete) | Fixed: `${CLAUDE_SKILL_DIR}/../dev-core/scripts/tree_fingerprint.py`; MR-03 row annotated |
| MR2-02 | SHOULD-FIX | After MR-04, `validate` passed with a parked writer on a conflicting REQ, contradicting REQ-008, the design and the wiki guide | Fixed in code, without changing the user's requirement: `validate` again fails with `REQUIREMENT_CONFLICT` for every open writer. Only `ready` lists the other nodes when the sole such errors sit on writers parked as `planned` or `blocked`, and it reports those writers under `waiting_on_conflict`. REQ-008, the design and the wiki guide are true again; tests |
| MR2-03 | SHOULD-FIX | PR body was stale (test count, validations, Deferred and Rejected lists, missing records) | Fixed: PR body updated after the new head is pushed |
| MR2-04 | NIT | A comment line inside a block list broke the list (regression from MR-10) | Fixed: comment-only lines are skipped; test |
| MR2-05 | NIT | MR-13 containment bypassed when the symlink target held `.git` or `.dev` | Fixed: transition refuses any symlinked folder between the graph and its `.dev` folder; test with a symlinked objective pointing to another repository |
| MR2-06 | NIT | A bare `*.pyc` anywhere was excluded from the fingerprint, although `.pyc` files are importable code | Fixed: only the named cache folders are excluded; test that a bare `.pyc` is detected |
| MR2-07 | NIT | Submodules were neither covered nor listed as a limit | Fixed (documentation): the script docstring and dev-core §8 state that submodules are not covered and say to fingerprint them separately |
| MR2-08 | NIT | check_pack could not catch MR2-01 | Fixed: in dev-core, every `${CLAUDE_SKILL_DIR}` reference must start with `../dev-core/` or `../../vendor/` |
| MR2-09 | NIT | REQ relation errors in unrelated REQ files block every graph | Rejected: deliberately fail-closed. The requirements wiki is shared by every objective in the project, and a broken relation means a requirement no one can trust; fixing the wiki is the intended next step |
| MR2-10 | NIT | ILLEGAL_REOPEN advice was impossible for accepted dependents | Fixed: the message says to move unfinished dependents back, and to add a new node for done or accepted ones |
| MR2-11 | NIT | Ownership overlap was case-sensitive | Fixed: compared case-folded (more conservative on case-insensitive file systems); test |
| MR2-12 | NIT | The `''` escape inside single quotes was cut short | Fixed; test |
| MR2-13 | NIT | check_pack and graph.py used different REQ filename rules | Fixed: shared `graph.REQ_FILE_RE` |
| MR2-14 | NIT | The MR-20 row held two dispositions | Fixed: the row now has a single Fixed disposition with context |
| MR2-15 | NIT | Redundant second `rev-parse --show-toplevel` | Fixed |
| MR2-16 | NIT | Each REQ file is parsed three times in check_pack | Rejected: about ten small files; the cost is negligible, and merging the passes would couple the schema check to graph internals |
| MR2-17 | NIT | Rename records in `status -z` were mis-sliced | Fixed: rename and copy entries keep their original-path record; test with a staged rename |

## Verification after the fixes

- `./scripts/validate.sh`: all checks passed.
  - 79 tests, also run with `-W error::ResourceWarning`.
  - Both manifests validate.
