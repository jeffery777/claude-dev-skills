# Review round 5 (narrow confirmation, R-REV-4) — issue-16-single-source-rules

- Target: working tree at HEAD 1386a69 (+ uncommitted, intent-to-add)
- Diff identity: sha256 of `git diff HEAD --binary` = 9e65caef1634cb38b51f712576c72bbbbf1c8a738afe1a43a348b6cc24f045a7 (same before and after; HEAD and status unchanged)
- Mode: narrow confirmation of the round 4 fixes
- Reviewer: dev-reviewer (requested model/effort: opus/high; effective: unknown)
- Scope: FU-005 row, GateRuleText docstring, REQ-022, CF-008 zh and EN, graph.json, reviews/round-1 to round-4  Requirements: REQ-022  DoD: each round 4 fix correct and complete, no new problem
- Writing: written per ASD-STE100 principles; full conformance not verified (R-WRT-1)

## Findings

| ID | Relation | Severity | Location | Finding | Evidence | Impact | Class | Disposition |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| FR5-001 | in-scope | NIT | .dev/followups.md FU-005 | Agent copy list still incomplete (R-REV-6 in both reviewers; R-DEL-1 "one final receipt" in the explorer and both reviewers); fourth time this list is flagged | agents/*.md; dev-core R-REV-6, R-DEL-1 | FU-005 could miss copies | necessary fix (management measure) | Fixed: the two items added; the list is marked as a minimum, and the FU-005 verification plan requires a sentence-by-sentence comparison of each agent file and task-brief.md with dev-core before a split or a change to a copied rule, with an owner and a stop when it cannot be done (re-review: round 6) |
| FR5-002 | in-scope | SHOULD-FIX | reviews/round-4.md, round-1.md | Residual items listed by number only; round 4 had no "not run" list (R-REV-8) | round-2.md and round-3.md list them | Gate cannot read the residual risk | necessary fix | Fixed: contents of R3 to R8, R11 and R4-a to R4-j written out; round 4 "not run" added (re-review: round 6) |
| FR5-003 | in-scope | NIT | docs/core-feedback.md CF-008 EN | "in their words" gave only a translation | REQ-022 sources | Translation read as a quote | necessary fix | Fixed: the original Chinese quote plus a marked translation (re-review: round 6) |

No MUST-FIX: the R-VER-2 stop rule does not apply.

## Verification evidence

Reviewer: `bash scripts/validate.sh` passed (131 tests); 8 targeted tests OK; `graph.py validate` ok; `git diff HEAD --check` clean; agents/*.md and task-brief.md compared with dev-core rules by hand; CF-008 quotes compared with REQ-022 sources. Not run: full deep review (not this mode); R-REV-9 scan (separate). No file written (Python with `-B`).

## Residual risk

R5-a: round-2 FR2-001 disposition text describes a change of state (final disposition: Fixed). R5-b: `Fixed` rows name the re-review round but not a fix revision (no commits yet; the next round's diff identity identifies the fix). R5-c: task-brief.md model/effort template fields (R-DEL-2) not in FU-005. R5-d: dev-reviewer "recommend a security review" (R-REV-7) not in FU-005. R5-e: FU-006 status says "Done in Issue #16" before the merge. R5-f: the round 4 byte-code side effect was not re-checked.
