# Exact-head Merge Review 3 — PR #2 (closes #1)

- Identity:
  - base and merge-base: `5229478aead42cc2d70b7843dd5db3548c08c562`
  - head: `c934a29126c82f7565d85e1bf2f18ee5ebcb0ca4`
  - diff: sha256 = `63e4fd710c614d8778a6ad06a2c1cfbe6b09176d7db860d3db95d9267e34fed3` (85 files)
- Reviewer: a fresh opus subagent. It ran a complete base-to-head review with native `/code-review` (high, all findings) and a proportionate manual Security Diff Scan of the delta since `c72c64d`, with reproductions. It reused Merge Review 2's native `/security-review` for paths that did not change. It confirmed every Merge Review 2 disposition except MR2-17 (partly done).
- Result:
  - `content_review: BLOCKED`. 2 new findings had no disposition; neither is a MUST-FIX.
  - `platform_enforcement: NOT_CONFIGURED`.
  - Neither result authorizes a merge.
- Disposition audit: 173 rows across 6 records, each with exactly one disposition.

| ID | Sev | Finding | Disposition |
| --- | --- | --- | --- |
| MR3-01 | SHOULD-FIX | `TRANSITION_BREAKS_GRAPH` compared error text, so a transition that reduced a STATUS_DEP's pending list was refused | Fixed: a STATUS_DEP counts as new only when its pending set grows; other errors are still compared by code, node and message; regression test with the reviewer's scenario |
| MR3-02 | NIT | MR2-17 handled only index-side renames | Fixed: R or C in either status column marks a two-record entry; test with `git add -N` after a move; MR2-17 row annotated (Test strengthened under MR4-04.) Superseded: `tree_fingerprint.py` was removed in ed3f66c (PR #2, user decision 3); a required review now stops at the gate without a read-only plugin reviewer. |

Records also annotated: merge-review-1.md MR-04 (superseded by MR2-02) and MR-05 (narrowed by MR2-06).

## Verification after the fixes

- `./scripts/validate.sh`: all checks passed (81 tests, also run with `-W error::ResourceWarning`).
