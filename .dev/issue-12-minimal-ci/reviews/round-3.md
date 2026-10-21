# Round 3: narrow confirmation after Q5 (a) (Issue #12)

- Candidate: uncommitted tree on base `98878365c6d541c7efdd54af43960679bb3fb42a`,
  branch `12-minimal-ci`, diff sha256 `36eedd10…` (unchanged during both
  reviews).
- Reviewers: `dev-skills:dev-reviewer` (narrow, opus) and
  `dev-skills:dev-security-reviewer` (narrow plus a content scan of the whole
  diff, opus). Both read-only.
- Input: the user's decision Q5 (a) (REQ-020 source): the provider-profile
  setting leaves this PR and is designed in FU-009 together with FU-008.
- Commands: `scripts/validate.sh` (pass); `graph.py validate` (ok); greps for
  leftover profile text; content scan of all added lines (no secrets,
  private paths, hostnames, emails or real names).

## Confirmed

- `dev-gate` step 6 follows Core exact-dimensions: `NOT_CONFIGURED` without a
  profile; a failed read or another head gives `UNVERIFIED`; no VERIFIED or
  BLOCKED path; no repository file can influence the result.
- R2-001, R2-002 and R2-003 are fixed. ES2-001 to ES2-003 and R2-004 no longer
  apply. ES-003 (gitleaks flags and stated limits) is intact.
- FU-009 records every ES2 design point.

## Findings and dispositions

| ID | Relation | Severity | Class | Finding | Disposition |
| --- | --- | --- | --- | --- | --- |
| R3-001 | in-scope | NIT | necessary fix | REQ-020 Need said `platform_enforcement` can be read back, which this PR no longer delivers | Fixed: "(after FU-009)" |
| R3-002 = ES3-001 | in-scope | NIT | necessary fix | round-1 and round-2 records still described the removed profile path as fixed | Fixed: supersession notes in round-1 (three rows) and round-2; ES-001 and ES-002 lessons added to the FU-009 source |

## Residual risk

- While `platform_enforcement` is `NOT_CONFIGURED`, a failed PR check is
  listed but not named as a step-4 blocker; GitHub blocks it once the
  maintainer makes the checks required; FU-009 closes it.
- `gh pr view` uses gh's own repository resolution (FU-009).
- Round-1 residuals stay.

Written per ASD-STE100 principles; full conformance not verified.
