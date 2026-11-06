# Design review round 1, Issue #104

- Target: `.dev/issue-104/plan.md`, SHA-256 `55fdc33c75760331be1a73b16cbbaf4d65596633da30f184e6f80264a64e9b91`, uncommitted, base `6f7a817933c5f680a32d01ed0e6d6fe6eb3834c5`.
- Tree check: HEAD, status and diff hash are the same before and after both reviews.
- Deep: `dev-reviewer`, requested opus/xhigh. Read-back: `git --no-replace-objects cat-file blob 6f7a817933c5f680a32d01ed0e6d6fe6eb3834c5:skills/dev-core/scripts/model_effort_readback.py | python3 -I - subagent --config-base 6f7a817933c5f680a32d01ed0e6d6fe6eb3834c5 --floor review-scan …`: `PASS model=opus tier=3 effort=xhigh expected=opus/xhigh expected_tier=3 floor=review-scan`, exit 0.
- Security: `dev-security-reviewer`, requested opus/xhigh. Same call form, same line, exit 0, after its task notification.
- Effective setting: `unknown`.
- Writing: written per ASD-STE100 principles; full conformance not verified.

## Findings and dispositions

The IDs are the reviewers' IDs with a prefix (DR-D deep, DR-S security).

| ID | Severity | Finding | Class | Disposition |
| --- | --- | --- | --- | --- |
| DR-D-01 | MUST-FIX (unclear Core blocker) | After Q2 most dispatches are not checked; Core `workflow.md:56` says each interface checks the effective model and effort | needs human decision | `Fixed` by the user's answer to card I104-C1 (a): the reading is recorded in DL-049 and D-031, marked as an inference |
| DR-D-02, DR-S-02 | SHOULD-FIX | Redefining "a review" narrows rules that are not read-back (session binding, handoff, native pass) | necessary fix | `Fixed` in the design: these sentences stay in `SKILL.md`; no redefinition |
| DR-D-03 | SHOULD-FIX | The delete list leaves sentences that name other dispatches | necessary fix | `Fixed` in the design: sentence by sentence |
| DR-D-04 | SHOULD-FIX | No search list; co-changes missed (REQ-026, DL-035, DL-045, CF-001 items 2 and 5) | necessary fix | `Fixed` in the design |
| DR-D-05, DR-S-04 | SHOULD-FIX, NIT | The signature exception misses `dev-implement` and push step 5 | necessary fix | `Fixed` in the design |
| DR-D-06 | SHOULD-FIX | Three Scope items have no recorded authority | necessary fix | `Fixed` in the design (DL-049) and card I104-C2 |
| DR-D-07 | SHOULD-FIX | "Private data only" does not reach the scanning subagent | necessary fix | `Fixed` in the design: agent file |
| DR-D-08, DR-S-01 | SHOULD-FIX | One `grep` cannot print only line numbers | necessary fix | `Fixed` in the design: `awk` |
| DR-D-09 | SCOPE-CREEP | A standing word-count test has no requirement | keep as is | `Fixed`: test removed from the design |
| DR-S-03 | SHOULD-FIX | R-REV-4 would write the threat model of this pack's gates into a rule that also reviews products | necessary fix | `Fixed` in the design: scope words |

Fixes get their re-review in the implementation review. Each fix deletes text or
changes words; DR-D-07 adds one clause.

## Residual risk and not handled

- Not handled (deliberate tampering): a forged GitHub committer on a local commit with a personal signature; a rewritten transcript.
- Reading a reference in a later turn can prompt or be refused (CB-7): fail-closed, the same as other references.
- "the same work" of R-REV-3 is not defined; a specific rule such as push step 5 ("covers only") stays as written.
- R-VER-2 has no round limit; Core `workflow.md:72` and `:99` and R-RIG-4 cover endless rework.

## Lesson candidates

none
