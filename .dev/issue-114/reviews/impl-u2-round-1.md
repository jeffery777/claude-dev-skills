# Issue #114 implementation review of U2, round 1

Written per ASD-STE100 principles; full conformance not verified.

## Binding

- Target: `git diff HEAD --binary -- .claude-plugin/plugin.json .claude-plugin/marketplace.json vendor/engineering-workflow-core.lock.json`
  (SHA-256 `622672b0c1b0de7636a3e8867e2ef8b2ba7dc5ae02e5220f01be10b7afd7e389`,
  deep reviewer), uncommitted, HEAD = base
  `7e71ad5061b345d6f8c921adca65bf494876855c`; tree diff hash before and
  after (CB-4): `5592907a30901cc89ca6856c087fc493b75f08d303cedb2a96228231257d375d`.
- Reviews, in parallel with the U1 round 2 confirmation: deep
  (`dev-skills:dev-reviewer`, role `review-deep`) and Security Diff Scan
  (`dev-skills:dev-security-reviewer`, role `review-security`), each
  `opus`/`xhigh` passed; recorded `unknown`, case `not read back`;
  effective `unknown`. The graph still had U1 in `reviewing` and refused U2
  (`STATUS_DEP`); the U2 reviews ran before U1 was `done` (plan, order
  deviation).
- `reviewer_acceptance.py check` `PASS` and CB-4 as in
  `impl-u1-round-2.md` (one Bash command before the three dispatches; the
  same values after).
- Reported commands: `check_pack.py`, `verify_core.py`,
  `check_core_coverage.py` (all exit 0), unit tests (424, OK, 3 skipped),
  `git diff --check`, JSON structure compare against `HEAD`, `claude plugin
  validate` with 2.1.310, 2.1.311 and 2.1.312 (exit 0, warnings), `curl` of
  the official docs, read-only `git grep`. The deep reviewer also listed the
  local CLI version folders to look for 2.1.304 (not found). No write
  reported.
- Security Diff Scan verdict: PASSED (bounded). Only `/version` of
  `plugin.json`, `/plugins/0/version` of `marketplace.json` and
  `/consumer/version` of the lock changed; `verify_core.py` does not read
  `consumer`; no new component, key, hook or executable.

## Findings and dispositions

| ID | Relation | Severity | Summary | Class | Disposition |
| --- | --- | --- | --- | --- | --- |
| IRU2-D-01 | in-scope | NIT | The plan said that `claude plugin validate` names no `version`; it prints `version: No version specified ...` (exit 0) | necessary fix | Fixed in the plan (correction, with the reason that the warning is expected) |
| IRU2-D-02 | gap | REQ-GAP | `check_pack.py` (`MANIFEST_KEYS`) still allows `version` in both manifests; nothing fails when it comes back, and the validator suggests adding it | needs human decision | Needs Human Decision: card C7 (`cards-2.md`) |
| IRU2-S-01 | gap | REQ-GAP | Same as IRU2-D-02 | needs human decision | Needs Human Decision: card C7, with IRU2-D-02 |
| IRU2-D-03 | in-scope | NIT | REQ-028, the `check_pack.py` comment, CB-7 and DL-037 call the manifest allowlist "the keys in use"; no manifest uses `version` now | needs human decision | Needs Human Decision through card C7: option (a) makes the text true again with one REQ-028 edit; option (b) adds one sentence |

Design findings now settled by card C1 (c) and this diff: DR-S-04 and
DR-S-07 Fixed (no `version` in either manifest); DR-S-06 answered by REQ-030
(no pin instructions).

## Residual risk and limits

- Release channel (deep reviewer, for the user's awareness): every merge
  to `main` reaches each unpinned Claude Code install at its next update,
  with no release gate between them; card C1 (c) accepted "no stable
  channel". Who can push to `main` was not checked in this review.
- After an update, the cache folder named `0.1.0` is marked orphaned and is
  removed 14 days later (official docs, `loading.md`; inference for this
  plugin): briefs that name files by that cache path stop resolving.
- CI pins Claude Code 2.1.304; its `claude plugin validate` result without
  `version` comes with the PR run (unverified).
