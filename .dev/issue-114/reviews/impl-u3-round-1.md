# Issue #114 implementation review of U3, round 1

Written per ASD-STE100 principles; full conformance not verified.

## Binding

- Target: the U3-only diff (SHA-256 `434a8fbe0ee3a07a7e7f4031b3bd124df1e6c384759d1e0dd84eb135d55b8bcd`,
  a file outside the repository: CHANGELOG, REQ-030 and `log.md` against a
  snapshot taken after the U1 fixes, plus `git diff HEAD` of
  `scripts/check_pack.py`, `tests/test_core_checks.py` and REQ-028),
  uncommitted, HEAD = base `7e71ad5061b345d6f8c921adca65bf494876855c`;
  tree diff hash before and after (CB-4):
  `7c669d7aa4cae94463e146acb1b2ca08b7b9f17f9a82f5d82f56b41519bce49b`.
- Reviews, in parallel: deep (`dev-skills:dev-reviewer`, role
  `review-deep`) and Security Diff Scan (`dev-skills:dev-security-reviewer`,
  role `review-security`), each `opus`/`xhigh` passed; recorded `unknown`,
  case `not read back`; effective `unknown`.
- `reviewer_acceptance.py check` printed `PASS` (exit 0) in the same Bash
  command as the CB-4 values before the dispatch; after both reviews the
  values were the same (exit 0).
- Reported commands: the targeted test (OK, 8 subtests with the two new
  `version` cases), `check_pack.py` (exit 0), `git diff --check`,
  `git diff --no-index` against the snapshot (U3 changed only the six paths
  of node U3), read-only `git grep`, `shasum`, `awk`. No write reported.
- Security Diff Scan verdict: PASSED (bounded). The change only narrows the
  allowlist; `MANIFEST_KEYS` has one user (`check_pack.py`, the manifest
  check); no new key, import or execution path.

## Findings and dispositions

| ID | Relation | Severity | Summary | Class | Disposition |
| --- | --- | --- | --- | --- | --- |
| IRU3-D-01 | in-scope | NIT | The inserted CHANGELOG clause made "`consumer.version` ... says the same" refer to the check, and it cited cards-1 for C7 | necessary fix | Fixed: the check is its own sentence after the lock clause, citing `cards-2.md` |
| IRU3-D-02 | in-scope | NIT | REQ-028 note "the sets in use on 2026-10-27" no longer holds for the manifest allowlists | necessary fix | Fixed: the note adds that the manifest allowlists have no `version` since Issue #114 |
| IRU3-D-03 | no-requirement | SCOPE-CREEP | The REQ-030 note on the `claude plugin validate` warning has no requirement source (card C7 did not list it) | keep as is (deletion) | Fixed by deletion: the note is removed; the plan keeps the observation (U2 correction IRU2-D-01); a fix-round `log.md` row records the removal |
| IRU3-S-01 | unrelated | NIT | Two ignored bytecode files under `scripts/__pycache__/` and `skills/dev-plan/scripts/__pycache__/` from a run without `-B` | keep as is | Rejected as a change of this node: the files are ignored and not staged; the main agent made them (plan, U3 verification); deletion asks the user |

IRU2-D-02, IRU2-S-01 and IRU2-D-03 of the U2 review are Fixed by U3 (card
C7 (a)).

## Residual risk and limits

- The check runs in `validate.sh` and CI, not when Claude Code loads the
  plugin (CB-7 limit); a PR can change the allowlist and the manifests
  together, so review and REQ-030 remain the guard for that case.
- The test proof that the two cases fail with the old allowlist is by
  reading the code; no mutation run.
