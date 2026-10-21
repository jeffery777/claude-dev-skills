# Review records (Issue #14)

Design-first (strict tier). Spec v2 and its threat model were reviewed before
any rule text, then approved by the user (Q1 (a), Q2 (a); REQ-021 sources).

## Design review round 1 (spec v1, no repository change)

- Reviewers: `dev-reviewer` (deep) and `dev-security-reviewer`.
- Findings: DR-001 MUST-FIX (`git show` cannot tell a missing file from a
  missing commit: false `NOT_CONFIGURED`), DR-002 to DR-006 SHOULD-FIX
  (allowed keys, schema, head re-read, no-profile path, policy-change
  definition), DR-007 SCOPE-CREEP (configurable path list), DR-008 NIT;
  ES0-001 to ES0-003 MUST-FIX (rules pagination, `filter=all` per suite,
  checker inside the repository), ES0-004 to ES0-007 SHOULD-FIX, ES0-008 NIT.
- Dispositions: all Fixed in spec v2 (necessary fix); DR-007 went to the user
  as card Q2, answered (a) (fixed path list).

## Implementation review round 1

- Identity: HEAD `97406d73ca3e36ed6311f2a8c8640cdb96a7b6b8`, uncommitted diff
  `git diff HEAD --binary` SHA-256
  `ce1112bad481cb402d02b63f7c93878bd5e050f00d8ef750afe64d4c25dd8e83`;
  unchanged before and after both reviews.
- Reviewers: `dev-reviewer` (deep) and `dev-security-reviewer` (Security
  Diff Scan; gitleaks `NOT_RUN`, capability `UNAVAILABLE` locally; CI runs it).
- No false `VERIFIED`, no injection and no write call was found; the profile
  matches the live ruleset.

| ID | Relation | Severity | Class | Finding | Disposition |
| --- | --- | --- | --- | --- | --- |
| R1-001 = ES1-001 | in-scope | MUST-FIX | necessary fix | `--repo-dir` in a subdirectory: `git ls-tree` path relative to it, false `NOT_CONFIGURED` | Fixed: the checker works from `git rev-parse --show-toplevel`; test `test_subdirectory_repo_dir_still_reads_the_profile` |
| R1-002 = ES1-003 | in-scope | SHOULD-FIX | necessary fix | The fake `gh` ignored flags; no negative case for host, GET only, all pages, `filter=all`, head re-read, blob binding | Fixed: the fake answers only the exact GET form for the bound repository; new tests; 8 mutations on a copy outside the repository all fail the tests |
| R1-003 | in-scope | SHOULD-FIX | necessary fix | Pack directory = repository root gave prefix `./`; pack files never listed | Fixed: the whole repository is listed; test added |
| R1-004 | in-scope | SHOULD-FIX | necessary fix | A `.dev/config.json` that is not UTF-8 crashed the checker | Fixed: `BLOCKED` "invalid JSON: not UTF-8"; test added |
| R1-005 = ES1-004 | gap | REQ-GAP | needs human decision | No rule for a checker failure or a missing result line | User decision Q6 (a): the gate result is `UNVERIFIED` (rule text only, no code) |
| R1-006 = ES1-002 | gap | REQ-GAP (security: Core blocker) | needs human decision | Without a profile, a stale bound base could give a false `NOT_CONFIGURED` | User decision Q5 (a): `baseRefOid` added to the one `gh pr view` read; another base is `UNVERIFIED` (rule text only) |
| ES1-005 | in-scope | NIT | necessary fix | Input patterns accepted a trailing newline, non-ASCII digits and `.`/`..` | Fixed: `fullmatch`, ASCII digits, dot segments refused; tests added |
| ES1-006 | gap | NIT | worth improving | Run the base copy with `python3 -I`; case-insensitive paths can bypass the self-location check | `python3 -I` added to the rule text (spec property: base copy). Case-insensitive bypass: residual risk, a changed checker could remove the check anyway |

- Stop rule (R-VER-2): the design review and implementation review round 1
  both found new blockers in this mechanism. The fix loop stopped; the user
  decided "Q4 a；Q5 a；Q6 a" (one bounded fix round). If the next round finds
  new blockers in this mechanism, the work stops and the PR is split.
- Residual risk: the newest run in a suite is chosen by run id; `CHANGELOG`
  lists the feature under `Changed`; whether an open PR's `baseRefOid`
  follows the base branch is not verified (a mismatch fails closed as
  `UNVERIFIED`).

## Narrow confirmation round 2

- Identity: HEAD `97406d73ca3e36ed6311f2a8c8640cdb96a7b6b8`, diff SHA-256
  `9bb595b38a830f5e85b2b6195f9b99cf6933bb444da45873e45f50648dd1e3cf`;
  unchanged before and after both reviews.
- Both reviewers confirmed every round-1 disposition; mutations on copies
  outside the repository fail the tests; no new false `VERIFIED` or false
  `NOT_CONFIGURED` in the checker; the diff has no secrets or private data.

| ID | Relation | Severity | Class | Finding | Disposition |
| --- | --- | --- | --- | --- | --- |
| R2-001 = ES2-002 | in-scope | MUST-FIX | necessary fix | `dev-core` R-EXH-4 did not state the Q5 base check and the Q6 checker failure, so it contradicted `dev-gate` step 6 | Fixed: the sentence names the bound base, another base or head, and a checker failure |
| ES2-001 | in-scope | NIT | necessary fix | The fallback `git ls-tree` (checker missing at base) did not run from the top level | Fixed: `git cat-file -e` plus `git ls-tree --full-tree` |
| ES2-003 | gap | REQ-GAP | needs human decision | The no-profile `gh pr view` did not pin the host | User decision Q8 (a): `--repo github.com/<owner/name>` |

- Stop rule: R2-001 was a new blocker in this mechanism (a restated rule
  copy that missed the Q5/Q6 change, the FU-006 pattern). The user decided
  "Q7 a；Q8 a": fix the text and continue.
- Residual risk: if an open PR's `baseRefOid` and the bound base are equally
  stale, they match (GitHub behaviour not verified); `GIT_DIR` and
  `GIT_WORK_TREE` in the environment are passed to git; a file name that is
  not UTF-8 can crash the checker (Q6: `UNVERIFIED`).

## Narrow confirmation round 3

- Identity: HEAD `97406d73ca3e36ed6311f2a8c8640cdb96a7b6b8`, diff SHA-256
  `62995b2588bfb17374acb43d7d505d8395f07b3bed1dbdf39f243eda5a034085`
  (text-only changes after round 2); unchanged before and after.
- `dev-reviewer` confirmed R2-001, ES2-001 and ES2-003 (Q8 (a)); every
  restated `NOT_CONFIGURED` / `UNVERIFIED` statement in `skills/`, README,
  REQ-021 and D-018 matches `dev-gate` step 6. No findings; no new blocker.

Written per ASD-STE100 principles; full conformance not verified.
