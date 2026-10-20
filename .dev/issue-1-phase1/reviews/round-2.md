# Review round 2 — Issue #1, Phase 1 (pre-commit)

- Target: the working tree at HEAD `5229478` after the round 1 fixes.
- Reviewers, each in a fresh subagent context, none of which wrote the change:
  - `R2C`: native `/code-review` (high, all findings), plus a check that each round 1 "Fixed" item really was fixed. 22 findings, 8 round 1 items reopened.
  - `R2S`: native `/security-review` with scratch reproductions of the round 1 security fixes, plus a rule-by-rule comparison of `dev-core` with Core. 12 findings. None reached the exploitability threshold, and no MUST-FIX.
- Re-assessment after two review rounds (R-VER-2): severity dropped from 2 MUST-FIX to none, and the open items are edge cases in the same files. The approach, model and context stay; this round fixes the items one by one.

## Round 1 items reopened by R2C

| Round 1 ID | What was incomplete | Disposition |
| --- | --- | --- |
| CR-002 | Cancelling a node could break the ordering between writers, with no re-validation | Fixed: transition re-validates the resulting graph (`TRANSITION_BREAKS_GRAPH`); `STRANDED` warning; test |
| CR-003 | The reopen guard ignored dependents that had moved to `blocked` | Fixed: any dependent past `ready` blocks the reopen; test |
| CR-007 | A failed restore was not handled; a torn event line corrupted later appends | Fixed: `GRAPH_EVENT_MISMATCH`; `EVENTS_CORRUPT` check before append; tests |
| SR-004 | An explicit `--requirements-dir` skipped the containment check | Fixed: an explicit directory must also stay inside the project root; test |
| DR-015 | `max_rounds` remained in 13 fixtures | Fixed: removed from every fixture |
| DR-003 | dev-plan step 5 cited R-RIG-3 instead of R-RIG-4 | Fixed |
| CR-016 | Front matter was parsed again on an ID mismatch | Fixed: `load_requirements` returns the IDs it found |
| CR-017 | check_pack kept duplicate parsers; `sources()` did not strip comments, so files made from the REQ template failed | Fixed: uses `graph.frontmatter_lines`, `graph.REQ_RE`, `graph.REQ_STATUSES` and `graph.strip_comment`; template parse test |

## New findings

| ID | Sev | Finding | Disposition |
| --- | --- | --- | --- |
| R2C-01 | SHOULD-FIX | = CR-002 reopened | Fixed (see above) |
| R2C-02 | SHOULD-FIX | Dependents of a cancelled node were stranded silently | Fixed: `STRANDED` warning; dev-deliver says to re-plan; the schema doc states that a cancelled dependency is never satisfied (Completed under MR4-01: `ready` now passes the warning on.) |
| R2C-03 | SHOULD-FIX | = CR-003 reopened | Fixed |
| R2C-04 | SHOULD-FIX | = SR-004 reopened | Fixed |
| R2C-05 | SHOULD-FIX | Unhashable enum values crashed validate | Fixed: type guards; test |
| R2C-06 | SHOULD-FIX | A non-object JSON root crashed transition | Fixed: `UNREADABLE`; test |
| R2C-07 | SHOULD-FIX | Block-list items with the dash in column 0 were dropped | Fixed; test |
| R2C-08 | NIT | `#` inside values was cut | Fixed: `strip_comment` keeps quoted text whole and needs whitespace before `#`; test |
| R2C-09 | NIT | Block-scalar descriptions bypassed the length check | Fixed: `>` and `\|` values are joined before measuring; test |
| R2C-10 | SHOULD-FIX | = CR-017 reopened (template sources) | Fixed |
| R2C-11 | NIT | Status case not validated in user projects | Fixed: `BAD_REQUIREMENT_STATUS`; test |
| R2C-12 | NIT | = CR-007 reopened | Fixed |
| R2C-13 | NIT | `ready` lists planned nodes, but planned → in_progress is illegal | Fixed: documented in graph.py, the schema doc, dev-implement and dev-deliver (planned → ready first) |
| R2C-14 | SHOULD-FIX | = DR-003 reopened | Fixed |
| R2C-15 | NIT | The source map cites an untracked `.dev` review file | Rejected: `.dev/` is committed by default (DR-020). This review record is committed with the change, so the link resolves |
| R2C-16 | NIT | = DR-015 reopened | Fixed |
| R2C-17 | NIT | `ls-tree` output was not NUL-separated | Fixed: `-z` |
| R2C-18 | NIT | `--upstream` with no value raised IndexError | Fixed: usage message, exit 2; test |
| R2C-19 | NIT | A rule block ended at any `#` line | Fixed: ends only at a Markdown heading |
| R2C-20 | NIT | = CR-016 reopened | Fixed |
| R2C-21 | NIT | check_pack duplicated `REQ_ID` and the delimiter logic | Fixed |
| R2C-22 | NIT | Test helpers were duplicated; `rewrite` did not assert the target was present | Fixed |
| R2S-01 | SHOULD-FIX | The substitute-reviewer tree check missed untracked, ignored and `.git` changes | Fixed: `skills/dev-core/scripts/tree_fingerprint.py` covers untracked and ignored contents, `.git/config` and `.git/hooks`; without a shell, no substitute for a required review; tests |
| R2S-02 | SHOULD-FIX | Formal-exception limits dropped | Fixed: R-REV-8 (policy must allow it, recorded basis, no override of non-waivable rules), R-REV-7 (full non-waivable list) |
| R2S-03 | SHOULD-FIX | Gate blockers listed only a `NOT_RUN` scan | Fixed: dev-gate step 4 lists incomplete, failed and insufficient-coverage checks, missing reviews and unresolved security risk |
| R2S-04 | SHOULD-FIX | Gate review reuse checked only revision and scope | Fixed: dev-gate cites the full R-CAP-3 list |
| R2S-05 | SHOULD-FIX | Light work left uncommitted could end with no independent review | Fixed: R-RIG-2 says such work is "implemented, not independently reviewed", not engineering-accepted, and never reported as done |
| R2S-06 | NIT | R-RIG-4 omitted three limits | Fixed |
| R2S-07 | NIT | Smaller review-record obligations dropped | Fixed: R-REV-4 (fix safe extras, record reuse reason), R-REV-7 (policy not-applicable record), R-REV-8 (outside-evidence read-back), R-STG-4 (protected tests) |
| R2S-08 | NIT | R-REV-1 conflicted with the section 8 fallback | Fixed: R-REV-1 accepts a substitute only with the tree check |
| R2S-09 | NIT | The atomic write reset `graph.json` to 0600 | Fixed: the original mode is kept; test |
| R2S-10 | NIT | = R2C-06 | Fixed |
| R2S-11 | NIT | Race between the event-log symlink check and the open | Fixed: `os.open` with `O_APPEND \| O_NOFOLLOW` |
| R2S-12 | NIT | verify_core argument parsing; vendor directory itself a symlink | Fixed: usage message; the vendor dir and its parent are rejected when they are symlinks |

## Verification

- `./scripts/validate.sh`: all checks passed (21 anchors, 40 rules; 51 tests, also run with `-W error::ResourceWarning`; `claude plugin validate .` passed).
- The fingerprint script detected an untracked edit in this repository (manual check) and in tests.

## Result of round 2

- No MUST-FIX is open, and every finding has a disposition.
- Round 3 re-reviews independently, scoped to what round 2 changed: graph.py, check_pack.py, verify_core.py, check_core_coverage.py, tree_fingerprint.py, the changed dev-core rules (R-STG-4, R-RIG-2, R-RIG-4, R-REV-1, R-REV-4, R-REV-7, R-REV-8, section 8), and dev-gate, dev-plan, dev-implement, dev-deliver and graph-schema.md.
