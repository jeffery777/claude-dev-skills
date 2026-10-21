# Round 1: early deep review and early security review (Issue #12)

- Candidate: uncommitted tree on base `98878365c6d541c7efdd54af43960679bb3fb42a`,
  sha256 of `git diff HEAD --binary` = `834012cc…` (deep review; the tree did
  not change during it). The security review started on the same candidate;
  the R1-001 fix landed during it (end hash `89662cba…`), and the reviewer
  read both versions of the changed parts.
- Reviewers: `dev-skills:dev-reviewer` (deep, opus) and
  `dev-skills:dev-security-reviewer` (opus). Both read-only.
- Scope: REQ-020 acceptance, `.github/workflows/ci.yml`, `dev-gate` step 6,
  `dev-core` R-EXH-4, README CI section, D-017, CHANGELOG.
- Commands: `scripts/validate.sh` (pass, 83 tests); `claude plugin validate`
  with an empty HOME and no login (pass); pin checks with `gh api` and
  `git ls-remote`; gitleaks 8.30.1 source read with `gh api`; no binary run.

## Findings and dispositions

| ID | Relation | Severity | Class | Finding | Disposition |
| --- | --- | --- | --- | --- | --- |
| R1-001 = ES-001 | in-scope | MUST-FIX | necessary fix | The branch-protection endpoint returns 404 to non-admins, so a protected branch read as "no rule" | Fixed: read `branches/<base>` (`protection.required_status_checks`), readable with read access; a failed read is `UNVERIFIED`. Superseded by Q5 (a): the profile path was removed; see round-2.md ES2-001 and FU-009. |
| ES-002 | in-scope | MUST-FIX | necessary fix | A required check that never reported, or an empty required set, could give `VERIFIED`; head and checks were read in two calls | Fixed: required names come from the profile and are confirmed in the platform rules; one `gh pr view --json headRefOid,statusCheckRollup` read; an empty list is never `VERIFIED`. Superseded by Q5 (a): the profile path was removed; see round-2.md ES2-001 and FU-009. |
| ES-003 | in-scope | SHOULD-FIX | necessary fix | gitleaks coverage was overstated: binary diffs skipped, `gitleaks:allow` honored, merge patches not scanned, tree files can change the scan, CI runs after publication | Fixed: `--log-opts="--text HEAD"` and `--ignore-gitleaks-allow`; limits stated in `ci.yml`, README (zh, EN) and D-017 (zh, EN) |
| R1-003 | in-scope | NIT | necessary fix | The zh text of D-017 misquoted Core (dropped "current successful") | Fixed: Core sentence quoted verbatim |
| R1-002 | gap | REQ-GAP | needs human decision | No requirement says how a project selects the GitHub profile, what it covers, or whether it blocks | User decision Q3 (b): a profile is selected only with `platform_profile` in `.dev/config.json` (REQ-020 source). Implemented in `dev-gate` step 6. Superseded by Q5 (a): the profile path was removed; see round-2.md ES2-001 and FU-009. |
| ES-004 | gap | REQ-GAP | needs human decision | A PR can change its own checks (workflow, scripts, tests, gitleaks files) | User decision Q4 (b): Deferred as FU-008 (`.dev/followups.md`) |

FU-007 reached its promotion trigger in this plan. User decision Q2: Issue
text added to R-REV-9 and REQ-011 (a); commit timestamps rejected, risk
accepted (c); Git LFS, push options and release notes deferred (b).

## Residual risk (below the thresholds)

- The npm package of the Claude CLI runs a `postinstall` script; the version
  is exact, but there is no lockfile. The job token is read-only and the job
  has no secrets.
- The gitleaks checksum comes from the same release as the binary.
- `node-version: "22"` is a range.
- Without "require branches to be up to date", a green check can be older
  than the latest base.

The fixes above need a narrow independent confirmation before a push (R-REV-4).

Written per ASD-STE100 principles; full conformance not verified.
