# Review round 1 — issue-16-single-source-rules (FU-006, REQ-022)

- Target: working tree at HEAD 1386a69 (+ uncommitted, intent-to-add)
- Diff identity: sha256 of `git diff HEAD --binary` = aa613b8f0c58f10be04e359a12ece02fc12e758bc8a6a9a9b7ce1799bd4d14c9 (same before and after the review; HEAD and status unchanged)
- Mode: deep
- Reviewer: dev-reviewer (requested model/effort: opus/xhigh; effective: unknown)
- Scope: 23 files of `git diff HEAD`  Requirements: REQ-022  DoD: brief items 1 to 7
- Writing: written per ASD-STE100 principles; full conformance not verified (R-WRT-1)

## Findings

| ID | Relation | Severity | Location | Finding | Evidence | Impact | Class | Disposition |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| FR1-001 | in-scope | MUST-FIX | skills/dev-gate/SKILL.md step 4 | The blocker "a required review, verification or scan that is missing, incomplete, failed, has insufficient coverage, or is `NOT_RUN`" became "that R-AUTH-5 or R-REV-7 says blocks"; R-AUTH-5 adds "no safe fallback exists" and R-REV-7 says only "never Passed" | HEAD dev-gate:52-53; dev-core R-AUTH-5, R-REV-7 | Relaxed gate blocker | necessary fix | Fixed (re-review: round 2): old list restored with the IDs as sources (card 5a extra) |
| FR1-002 | in-scope | MUST-FIX | skills/dev-docs/SKILL.md step 3 | "Keep the prerequisites, the safety notes and the limits" and "license text" say more than R-WRT-1 ("for brevity", "quoted license text") | HEAD dev-docs:18-20; dev-core R-WRT-1 | Relaxed docs step | necessary fix | Fixed (re-review: round 2): old text restored with (R-WRT-1) |
| FR1-003 | in-scope | MUST-FIX | tests/test_rule_citations.py | The section-number pattern missed DL-009 "section 8" in deltas.md and other phrasings; CHANGELOG overstated the test | grep of the pattern on HEAD | REQ-022 acceptance 5 partly met | necessary fix | Fixed (re-review: round 2): dev-core folder flags any section number; other phrasings added; tests/ scanned; negative check flags all 6 old citations at HEAD; CHANGELOG reworded |
| FR1-004 | in-scope | MUST-FIX | tests/test_core_checks.py:191 | Docstring "dev-core section 8" | file text | Citation breaks at a split | necessary fix | Fixed (re-review: round 2): "dev-core CB-4"; tests/ now in the scan |
| FR1-005 | in-scope | MUST-FIX | dev-implement, dev-review step 3, dev-continue | Three citation sentences had no clear actor or changed the brief contract ("classify findings by R-REV-3"; "Scan its text" without `dev-security-reviewer`) | file text; agents/dev-reviewer.md "Rate severity by the thresholds in the brief" | Wrong actor or field | necessary fix | Fixed (re-review: round 2): one sentence per rule; dev-review brief sentence and dev-continue scanner sentence restored |
| FR1-006 | in-scope | NIT | .dev/followups.md FU-005 | List of agent copies incomplete | agents/dev-implementer.md, dev-explorer.md, task-brief.md | FU-005 could miss copies | necessary fix | Fixed (re-review: round 2): full list incl. task-brief.md and review-report.md |

## Residual items handled

- R1 (dev-gate "incomplete disposition"), R2 (merge row "identities and messages"), R9 (CHANGELOG "moves" vs new gate-record scope): worth improving, fixed with the round.
- R10 (R-WRT-1 lists fewer machine literals than Core wf-writing item 6, and omits items 2 and 3): verified against `vendor/.../workflow.md` items 2, 3 and 6. Relation `unrelated` (since 4b75360), not a security, data-loss, authorization or integrity blocker; REQ-022 forbids rule changes. Deferred to FU-010.
- Kept as residual risk (no requirement or DoD failure):
  - R3: review-report.md is also given to the reviewer subagent; its new pointers resolve only through the agent copies (later FR3-001; solved by card 7a).
  - R4: dev-deliver "may run in parallel (R-CAP-2)" without its condition (restored word for word by card 6a).
  - R5: "Decide the mode by R-REV-7", although R-REV-7's impact rule is about the Security Diff Scan (restored by card 6a).
  - R6: "gives the result of R-EXH-4" no longer names `UNVERIFIED` (readability; kept, the rule is in R-EXH-4).
  - R7: "the gate is void" removed in dev-gate step 7 (restored by card 7a).
  - R8: the GateRuleText negative test checks two fixed phrases; `DEFINED_RE` treats any bold `**R-…**` in dev-core as a definition.
  - R11: tests/test_core_checks.py finds section 8 by its heading text; a split makes it fail loudly.

## Verification evidence

Reviewer: validate.sh passed, 131 tests OK, graph validate ok. After fixes: validate.sh passed; patterns flag all six old section citations at HEAD.
