# Review round 1 — issue-6-review-convergence (PR-B)

- Target: working tree at 1debfabebd6d1620e49b5d385cbf72b05f06fb19 (+ uncommitted, intent-to-add, 20 status entries)
- Diff identity: sha256 of `git diff HEAD --binary` = f2a999937d66ba2c6d61f92b4c13a4a878d125cd469969d576c5e61ba42497c2 (both reviewers matched it before and after)
- Reviewers: `dev-skills:dev-reviewer` deep (B1-*), `dev-skills:dev-security-reviewer` Security Diff Scan (S1-*); requested model opus; effective: unknown
- Scope: all 20 changed paths. Requirements: REQ-012, REQ-013, REQ-014. DoD: their Acceptance lists and graph node T6
- Thresholds: the rules of this PR (R-REV-3 as changed here)
- Result: 3 MUST-FIX (reported by both reviewers), 1 SCOPE-CREEP
- Writing: written per ASD-STE100 principles; full conformance not verified

## Findings and dispositions

Each finding was classified before any fix (R-REV-4).

| ID | Relation | Severity | Finding | Class | New mechanism | Disposition |
| --- | --- | --- | --- | --- | --- | --- |
| B1-001, S1-001 | in-scope (REQ-014 item 5) | MUST-FIX | A Core blocker with relation `gap`, `no-requirement` or `unrelated` got the severity `REQ-GAP`, `SCOPE-CREEP` or none, so the gate did not block on it | necessary fix | no | Fixed: R-REV-3 makes a Core blocker `MUST-FIX` for every relation and overrides the other handling; R-REV-4 fixes a Core blocker first; DL-011, DL-012 and D-013 item 2 (zh, EN) updated. The optional extra gate line (S1-001) was not added: R-REV-5 already blocks a `MUST-FIX` |
| B1-002, S1-002 | in-scope (REQ-012 item 4) | MUST-FIX | Evidence reuse in the Merge Review used "untouched" instead of the user's "unaffected" (「未受影響」) | necessary fix | no | Fixed: "provably unaffected" / 「可證未受影響」 in R-EXH-3, dev-gate step 3, DL-013 and D-013 item 4 (zh, EN) |
| B1-003, S1-003 | in-scope (REQ-012 item 6) | MUST-FIX | Records were to be posted as a PR comment without the user's authority (R-AUTH-2), and a comment was the only allowed place | necessary fix | no | Fixed: never commit them to the PR branch; post a comment only when the user has authorized it, otherwise keep them uncommitted and give them in the report (R-EXH-3, R-REV-9, dev-gate step 8, dev-review step 5, DL-013, D-013 item 6 zh and EN) |
| B1-004 | no-requirement | SCOPE-CREEP | A second stop-rule trigger ("the same mechanism needed fixes and produced new problems in two consecutive rounds") is not in the user's words; it came from relayed advice | needs human decision | no | Fixed: removed from R-VER-2, DL-012, dev-review, dev-deliver and D-013 (zh, EN). Decision card 1 (`REQ-GAP` G-001: add it as a requirement, defer, or reject) went to the user. The user chose (a) add; REQ-012 records the answer, and the trigger is back in all five places |

## Requirement trace

| REQ | Covered by | Verified by |
| --- | --- | --- |
| REQ-012 | R-REV-3, R-REV-4, R-VER-2, R-EXH-3, R-REV-9; DL-011 to DL-013; dev-review, dev-gate, dev-deliver; D-013 | Deep review round 1; narrow confirmation pending |
| REQ-013 | decision-card.md, R-AUTH-6, R-WRT-1, DL-014; dev-review, dev-gate, dev-deliver; D-014 | Deep review round 1 (all acceptance items met) |
| REQ-014 | R-REV-3, review-report.md, both reviewer agents, dev-plan, DL-011; D-016 | Deep review round 1; B1-001 fix pending confirmation |

## Security scan

Applicable: yes (agent policy, review and gate rules, external writes, published content). Status: FINDINGS (S1-001 to S1-003, above). No secrets, private paths, hostnames, emails or real names in the 20 files. This is not the R-REV-9 pre-commit scan.

## Verification evidence

`bash scripts/validate.sh`: all checks passed before and after the fixes (core vendor, coverage 21 anchors and 41 rules, pack structure, 78 tests, plugin manifests). Two tests use the `wf-writing` source-map row as a fixture, so that row stays unchanged; DL-014 records R-WRT-1.

## Residual risk and limits

- The positive example's "If you do not decide" line is a long sentence split by "/".
- `gap` and `no-requirement` can overlap; the choice needs judgment.
- It is not stated whether an `unrelated` item gets an ID and a disposition.
- Uncommitted review records kept after a PR exists can be committed by accident with a later `git add -A`; the R-REV-9 scan still covers them.
- "Delta" in the user's NIT rule is read as "the change under review".
- The `source-map.md` rows for `wf-writing` and `review-security` do not name DL-014 and DL-013.
- Graph nodes T1 to T5 went to `done` on a self-check; their independent review is node T6 (the same pattern as PR-A, DR-A-013).
- The reviewers could not check the REQ quotes against the session transcript; the main agent checked all 22 quotes by script.

## Narrow confirmation C1 (before the commit)

- Candidate: staged diff sha256 320d4e5bc0e126c8440f7394b87638f91e94784e21f4ee63b310dc388ed3e1b3 (21 paths; both reviewers matched it before and after)
- Reviewers: `dev-skills:dev-reviewer` narrow confirmation (C1-*), `dev-skills:dev-security-reviewer` confirmation of S1-001 to S1-003 (C1S-*)
- B1-001, B1-002, B1-003, B1-004 with decision card 1, S1-001, S1-002, S1-003: CONFIRMED

| ID | Relation | Severity | Finding | Class | New mechanism | Disposition |
| --- | --- | --- | --- | --- | --- | --- |
| C1-001, C1S-001 | in-scope (REQ-012 items 4 and 6) | NIT | The `exact-transition` note in `source-map.md` still stated the rule before the B1-002 and B1-003 fixes | necessary fix (false documentation caused by this change) | no | Fixed: the note now says "never committed to the PR branch; a PR comment only with the user's authority, otherwise uncommitted in the report; evidence reuse only for provably unaffected parts" |

Residual risk (below the thresholds): the bracket "(security, data loss, authorization, integrity)" in R-REV-3 can be read as the full list of Core blockers, while the `MUST-FIX` line gives the full list; the R-REV-9 sentence keeps "or into the PR" without the authority condition, which R-EXH-3 and R-AUTH-2 supply; the REQ-012 Acceptance text says "evidence reuse … with reason and coverage" without "unaffected" (the quote and the rules say it); the positive example describes PR-A posting review records as comments without naming authority.

The C1-001 fix makes a new candidate. Its own R-REV-9 pre-commit scan is recorded outside this commit (R-REV-9).
