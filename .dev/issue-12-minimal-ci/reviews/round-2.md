# Round 2: deep review and security review (Issue #12)

- Candidate: uncommitted tree on base `98878365c6d541c7efdd54af43960679bb3fb42a`,
  branch `12-minimal-ci`, diff sha256 `cc6f8aad…` at start. The deep review saw
  no change during its run. The security review saw the R2 fixes land during
  its run (end diff `3735c32d…`) and checked its findings against the end
  candidate.
- Reviewers: `dev-skills:dev-reviewer` (deep, opus) and
  `dev-skills:dev-security-reviewer` (opus). Both read-only.
- Inputs: round 1, the user's decisions Q1 to Q4 (REQ-011 and REQ-020
  sources), Issue #12.
- Commands: `scripts/validate.sh` (pass); `graph.py validate` (ok); pattern
  scans of the diff (no secrets, private paths, hostnames or emails).
- Round-1 fixes confirmed: R1-001/ES-001, ES-002, ES-003, R1-003. After this
  round, Q5 (a) removed the profile path, so the R1-001/ES-001, ES-002 and
  R1-002 mechanisms no longer exist in the candidate (round 3).

## Findings and dispositions

| ID | Relation | Severity | Class | Finding | Disposition |
| --- | --- | --- | --- | --- | --- |
| R2-001 | in-scope | SHOULD-FIX | necessary fix | No profile and a failed read gave `NOT_CONFIGURED`, against R-EXH-4 | Fixed: a failed read or another head gives `UNVERIFIED` |
| R2-002 | in-scope | NIT | necessary fix | Restated R-REV-9 copies lacked Issue text (agent description, source map, CF-002, D-015) | Fixed |
| R2-003 | in-scope | NIT | necessary fix | FU-007 row cells contradicted the split | Fixed: row rewritten |
| R2-004 | gap | REQ-GAP | needs human decision | Which revision of the profile setting the gate reads | Superseded by ES2-001; moved to FU-009 (Q5 (a)) |
| ES2-001 | in-scope | MUST-FIX | needs human decision | A PR or a local edit can choose the profile that judges it | Stop rule R-VER-2 (second round with new blockers in the same mechanism). User decision Q5 (a): the profile setting is removed from this PR and designed in FU-009 with FU-008. The finding no longer applies to this candidate: no profile setting exists |
| ES2-002 | in-scope | SHOULD-FIX | needs human decision | VERIFIED and BLOCKED can both apply; "passed" undefined | Same as ES2-001: no VERIFIED or BLOCKED path remains in this PR; the rule goes into FU-009 |
| ES2-003 | in-scope | SHOULD-FIX | needs human decision | Unclear settings fail open | Same as ES2-001; fail-closed parsing goes into FU-009 |

## Residual risk

- Round-1 residuals stay (npm `postinstall` without a lockfile; gitleaks
  checksum from the same release; `node-version: "22"` range; a green check
  can be older than the base).
- `platform_enforcement` stays `NOT_CONFIGURED` until FU-009.

The narrowed `dev-gate` text needs a narrow independent confirmation before a
push (R-REV-4).

Written per ASD-STE100 principles; full conformance not verified.
