# Round 1: deep review and R-REV-7 security scan (Issue #32, SR21B-001)

- Revision: base `33ba87cbb67b5217565ba87e6e764e0cbb424479` plus uncommitted changes; `git diff HEAD --binary` SHA-256 `9242e5c364cd52017fce1fbaa803686fd04778563a0ee16fee7ba4b90c972852`. HEAD, status and diff hashes were the same before and after both reviews (CB-4).
- Scope: `agents/dev-security-reviewer.md` (allow-list sentence, lines 13-15), `docs/requirements/REQ-024-agent-write-and-delete.md`, `docs/requirements/log.md`, `CHANGELOG.md`, `.dev/issue-32-sr21b-001/`.
- Requirements: REQ-024; also REQ-008, REQ-011, REQ-018; REQ-025 checklist row C-24.
- DoD: the agent sentence equals the text the user approved in this session; no other agent rule text changes; REQ-024 records the user's answers and one acceptance line; one log row; no open MUST-FIX.
- Reviewers: `dev-skills:dev-reviewer` (deep, opus, xhigh requested) and `dev-skills:dev-security-reviewer` (R-REV-7 scan, opus, xhigh requested). Effective settings: unknown (not read back).
- Commands (both reviewers): `git diff HEAD --text --no-textconv --no-ext-diff`, `--word-diff`, `--check` (exit 0); `PYTHONDONTWRITEBYTECODE=1 bash scripts/validate.sh` (exit 0, 131 tests OK, existing ICON_MISSING warning); `graph.py validate` (ok); `gh issue view 32`; pattern scan for secrets, paths, emails and hostnames (0 true hits). No scanner named, none run.

## Security scan (R-REV-7)

Applicable: yes (agent tool and permission policy; indirect: executables, packaging). Status: FINDINGS, 1 NIT (SR32-001), 0 MUST-FIX, 0 SHOULD-FIX. The new words widen the allow-list only to tests named in the brief; the no-install, no-external-service, no-modify and no-write rules and the frontmatter do not change. The reviewer agrees with the PR-3 view that the added risk is low.

## Findings

| ID | Relation | Severity | Location | Finding | Class | Disposition |
| --- | --- | --- | --- | --- | --- | --- |
| R1-001 (= SR32-001) | in-scope (REQ-024) | NIT | `docs/requirements/REQ-024-agent-write-and-delete.md:64` against the new acceptance line | "The read-only rules stay as they are." contradicts the new line, which changes the allow-list in the read-only rule | necessary fix | Fixed: the new acceptance line ends with "This is the only change to the read-only rules." Re-review: round 2 |
| R1-002 | gap | REQ-GAP | `.dev/followups.md:13`, FU-005 row, Status | "SR21B-001 (... names scanners, not tests) is deferred to Issue #32" becomes stale with this change; no source assigns this update | needs human decision | Fixed: user decision card R1-002 (a) (「選a，本 PR 一起改；只寫 Issue #32，不要預寫 PR 編號。」): the FU-005 row clause now says SR21B-001 is fixed by Issue #32, with no PR number. Re-review: round 2 |

## Residual risk

- RR-1: the sentence does not require the security reviewer to read the diff of the test code or runner before it runs them.
- RR-2: tests named in an R-REV-9 commit or push scan brief have side effects after the scan; the CB-4 check does not see ignored files, `.git` or effects outside the repository.
- RR-3: "test commands" is not defined; the reviewer cannot always know before a run whether a command writes or uses the network (same as `dev-reviewer`).
- The security reviewer now runs code from the tree under review without technical isolation (accepted by the user, card 1 (a)); the main agent and `dev-reviewer` already do.
- Not verified: whether `claude plugin validate` (in `validate.sh`) contacts an external service; runtime enforcement of `tools` and `disallowedTools` (FU-004).
- Stale but frozen: `.dev/issue-22-fu005-records/fu005-checklist.md:69` (C-24 note; approved record, REQ-025 keeps it unchanged): unrelated.
- No test checks that both reviewer allow-lists stay aligned.

## Writing spot-check

Scope: agent sentence, CHANGELOG entry, REQ-024 lines, log row. The agent sentence is the approved wording. The CHANGELOG third sentence is long (28 words); observation only. Written per ASD-STE100 principles; full conformance not verified.
