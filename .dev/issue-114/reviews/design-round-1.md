# Issue #114 design review, round 1

Written per ASD-STE100 principles; full conformance not verified.

## Binding

- Target: `.dev/issue-114/plan.md` (SHA-256 `e41692c5d6feba391ecb3880eec69294db2eeb3cd3597bbf97f9d9208d371a77`)
  and `.dev/issue-114/graph.json` (SHA-256 `e527bc9fa0c0af5aabfef3193e11848ae23606187f1d3d3b36c0c440c141c328`),
  both untracked; HEAD = base `7e71ad5061b345d6f8c921adca65bf494876855c`.
- Reviews: deep (`dev-skills:dev-reviewer`, role `review-deep`) and
  security (`dev-skills:dev-security-reviewer`, role `review-security`),
  dispatched in parallel, each with `opus`/`xhigh` passed. Recorded value:
  `unknown`, case `not read back` (R-DEL-2 Read-back). Effective: `unknown`.
- Before the dispatch, in one Bash command: `reviewer_acceptance.py check`
  printed `PASS` (exit 0), and the CB-4 values (HEAD, status hash, diff
  hash, plus the SHA-256 of the three files of this folder). After both
  reviews: the same values (exit 0). Limit (CB-4): edits inside untracked
  files are seen here only through the extra file hashes; `.git`, ignored
  files and effects outside the repository are not seen.
- Core review criteria: the contracts of the loaded pack (plugin cache,
  version `0.1.0`); the deep reviewer reports them byte-identical with the
  vendored copies (`cmp`), the security reviewer the same (`shasum`).
- Commands that the reviewers report: read-only `git`, `gh issue view`,
  `gh api` (GET), `gh release create --help`, `curl` of three official docs
  pages (deep reviewer), `shasum`, `grep`, `awk`, `perl` counts. No test
  run (no code change). No reviewer reports a write.

## Findings and dispositions

Classification before fixing (R-REV-4): threat model, then requirement,
then fix.

| ID | Relation | Severity | Summary | Class | Disposition |
| --- | --- | --- | --- | --- | --- |
| DR-S-01 | in-scope | MUST-FIX | The tag target and the notes are not bound to the exact merge commit; `gh release create` makes a missing tag from the latest default branch (`gh` 2.88.1 help, reviewer) | necessary fix | Fixed in design: D6 and the merge-card handover bind the tag and the notes to the full ID of the merge commit `M` read back from the PR, with tree(`M`) = tree(reviewed head) |
| DR-S-02 | in-scope | SHOULD-FIX | No handover for the scan inputs, tag kind, command form, read-back and failure handling of node H | necessary fix | Fixed in design: handover list in D6 |
| DR-S-03 | in-scope | SHOULD-FIX | README and release limits omit that no review or scan ran in Cowork and that reviewer read-only rests on instructions | necessary fix | Fixed in design (D2, D3); same root as DR-D-05 |
| DR-S-04 | in-scope | SHOULD-FIX | The string `0.1.0` names more than one content; existing installs do not get later commits | needs human decision | Needs Human Decision: card 1 |
| DR-S-05 | in-scope | SHOULD-FIX | The "released" definition is false today with a pinned `version` | needs human decision | Needs Human Decision: card 2; same root as DR-D-01 |
| DR-S-06 | gap | REQ-GAP | No requirement says what an unpinned install gets or how to pin a release | needs human decision | Needs Human Decision: card 1 (sub-question) |
| DR-S-07 | in-scope | NIT | `version` is set in both manifests; the docs say not to | needs human decision | Needs Human Decision: card 1 option |
| DR-S-08 | in-scope | NIT | The plan records the last-update date of the local install (runtime state) | necessary fix | Fixed: the date is removed from the plan |
| DR-S-09 | in-scope | NIT | The notes folder path holds an account name | necessary fix | Fixed in design: D6 says that the path goes into no commit, post or Release |
| DR-D-01 | in-scope | MUST-FIX | FU-027 premise ("holds until the first tagged release") is false: with `version` pinned, a merge does not reach installed users; the rule decides when a security lesson may be published | needs human decision | Needs Human Decision: card 2 (the rule text needs the user's answer; the blocker stays open until then, R-REV-3). Plan facts corrected |
| DR-D-02 | gap | REQ-GAP | No requirement sets the plugin version policy | needs human decision | Needs Human Decision: card 1 (add a requirement, defer or reject) |
| DR-D-03 | in-scope | SHOULD-FIX | `Closes #114` closes the Issue at the merge, before the tag and the Release of its Done-when exist | needs human decision | Needs Human Decision: card 5 (the brief asks for `Closes #114`) |
| DR-D-04 | in-scope | SHOULD-FIX | REQ-020 Acceptance names `CHANGELOG.md` `[Unreleased]` | necessary fix | Fixed in design: D4 adds REQ-020 (same handling as REQ-018), with a `log.md` row |
| DR-D-05 | in-scope | SHOULD-FIX | README "the skills load" is wider than the evidence; reviewer read-only and the tested version and commit are missing | necessary fix | Fixed in design (D2) |
| DR-D-06 | in-scope | SHOULD-FIX | FU-001 `Done` leaves the items not covered without a durable target | necessary fix | Fixed in design: new row FU-069 (Open) for the Cowork items not covered |
| DR-D-07 | in-scope | SHOULD-FIX | "the Core version it follows" without the DL-049 qualification is an unqualified conformance claim | necessary fix | Fixed in design (D3 limits paragraph) |
| DR-D-08 | in-scope | NIT | The date rule is unclear and has no time zone | necessary fix | Fixed in design: planned release date (UTC); the orchestrator compares it with the tag date |
| DR-D-09 | in-scope | NIT | Older entries in the same section say "not tested in Cowork"; the plan cites `CHANGELOG.md:898` wrongly | necessary fix | Fixed in design: one sentence on entry order; citation corrected |
| DR-D-10 | no-requirement | SCOPE-CREEP | Draft notes files outside the repository have no requirement | keep as is | Rejected: source is the task brief from the orchestrator session, step 5 ("Draft the GitHub Release title and notes ... as files for the orchestrator"); the draft carries the extraction rule and SHA-256, so it is a check value for the orchestrator, not a second source |

## Answers that the plan takes over

- engineering-workflow-core#40: conditionally not blocking (deep review:
  the same rule is already on `main`; the tag does not change what users
  run; FU-067 covers a Reading A answer; condition: a qualified disclosure
  in the release notes and a user decision before the tag); no security
  reason to block (security review). #38 and #39: not blocking (both
  reviews; #38 "adds no new obligation", #39 collects comments only).
  These are inferences of the reviewers. Card 4 asks the user.
- Security Diff Scan of U1 and of any U2: required (security review,
  R-REV-7: installation text and security claims in the release notes).

## Residual risk and limits

- Both reviews read the plan, not text; the README, CHANGELOG and record
  text is checked in the implementation review and the scans.
- Unverified (reviewers): the GitHub Release body limit, whether GitHub
  normalizes the body, how Cowork compares versions, whether a reinstall
  replaces an existing `0.1.0` cache folder, how many other caches exist.
- The deep reviewer did not read `authorization-and-stops.md` and
  `exact-head-and-evidence.md` (not in its criteria list).
