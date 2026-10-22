# Review round 4 (full deep review after card 7a) — issue-16-single-source-rules

- Target: working tree at HEAD 1386a69 (+ uncommitted, intent-to-add)
- Diff identity: sha256 of `git diff HEAD --binary` = c89fa43724cabe2f38665b0cc3103749dd07e50bdb384ff79a0544537edc7542 (same before and after; HEAD and status unchanged)
- Mode: deep
- Reviewer: dev-reviewer (requested model/effort: opus/xhigh; effective: unknown)
- Scope: the 26 files of `git diff HEAD`  Requirements: REQ-022 (acceptance narrowed by card 7a)  DoD: card 7a method, the user's location check, dev-core changes, tests, records
- Writing: written per ASD-STE100 principles; full conformance not verified (R-WRT-1)

## Findings

| ID | Relation | Severity | Location | Finding | Evidence | Impact | Class | Disposition |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| FR4-001 | in-scope | NIT | .dev/followups.md FU-005 | Agent copy list incomplete and inconsistent (R-AUTH-1 in both reviewers, R-REV-7 applicability, R-REV-2, R-RIG-3, R-REV-1 read-only missing) | agents/*.md | FU-005 could miss copies | necessary fix | Fixed: list extended (re-review: round 5, which found it still incomplete: FR5-001) |
| FR4-002 | in-scope | SHOULD-FIX | reviews/round-2.md, round-3.md | Scope, DoD and verification evidence missing (R-REV-8) | round-1.md has them | Gate evidence incomplete | necessary fix | Fixed: fields and evidence added from the reviewer reports (re-review: round 5) |
| FR4-003 | in-scope | NIT | reviews/round-3.md | FR3-005/006 dispositions said "word for word from main"; `Fixed` rows had no re-review round | round-3.md | Record did not match the work | necessary fix | Fixed: one disposition per row, re-review rounds added in rounds 1 to 3 (re-review: round 5) |
| FR4-004 | in-scope | NIT | tests/test_platform_profile.py GateRuleText docstring | Said Q8 is written in R-EXH-4; the host pin stays in dev-gate and its reference | dev-core R-EXH-4; dev-gate step 6 | False docstring | necessary fix | Fixed: docstring names Q5/Q6 in R-EXH-4 and Q8 in dev-gate (re-review: round 5) |

No MUST-FIX: the R-VER-2 stop rule does not apply.

## The user's location check (card 7a)

R-EXH-3, R-VER-2 and R-EXH-4 appear only in main-session files (dev-continue, dev-deliver, dev-gate and its platform-profile.md reference, dev-implement, dev-plan graph-schema.md (unchanged), dev-review SKILL.md, dev-core). They do not appear in agents/*.md, review-report.md, decision-card.md or task-brief.md. Passed.

## Residual items handled

R4-d (C1-001 was a NIT: REQ-022 says "findings"), R4-e (graph T1 title and DoD), R4-h (CF-008 lesson quotes the user and marks the reason as an inference): fixed. Kept as residual risk:
- R4-a: platform-profile.md:5 pointer; without a PR (local base..head) R-EXH-4 gives `NOT_CONFIGURED` only after a read-back; the unchanged dev-gate label "No profile (`NOT_CONFIGURED`)" covers that case (the ambiguity exists on main).
- R4-b: the GateRuleText negative test checks two phrases only.
- R4-c: no test keeps the three pointers out of subagent references (not required by the acceptance).
- R4-f: some changed lines are longer than 79 characters.
- R4-g: CHANGELOG and REQ-022 mention "`dev-core` section 8" as a description, not a citation.
- R4-i: the ID test scans Markdown files only. Python files do cite rule IDs (corrected after round 6, FR6-001): `skills/dev-gate/scripts/platform_profile.py:281` R-AUTH-2, `skills/dev-plan/scripts/graph.py:703` R-AUTH-7, `tests/test_platform_profile.py` R-EXH-4, `tests/test_core_checks.py` R-AUTH-7, R-WRT-1 and CB-4. All of them exist in `dev-core` today; a later rename would not be caught by the test.
- R4-j: acceptance 1 says copies "name their rule IDs"; some paragraphs have the ID at paragraph level only (for example dev-deliver step 5).

Not run in round 4: Security Diff Scan (not applicable); the R-REV-9 scan (separate); GitNexus (docs and tests only).

## Reviewer side effect

The reviewer ran `python3 -I`, which wrote a byte-code cache under the gitignored `tests/__pycache__/`. Diff hash and status were unchanged. The file was not deleted (a deletion needs the user's approval).

## Verification evidence

Reviewer: `bash scripts/validate.sh` passed (131 tests); 8 targeted tests OK; `graph.py validate` ok; `git diff HEAD --check` clean; in-memory comparison of every changed skill line with `git show HEAD:<file>` after removing added ID groups; ID sequence comparison; test patterns applied to HEAD content; tree-wide `git grep` for the three rule IDs.
