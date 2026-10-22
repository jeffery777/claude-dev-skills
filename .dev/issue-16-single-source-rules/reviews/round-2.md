# Review round 2 (narrow confirmation, R-REV-4) — issue-16-single-source-rules

- Target: working tree at HEAD 1386a69 (+ uncommitted, intent-to-add)
- Diff identity: sha256 of `git diff HEAD --binary` = c1179f1baf1775115b506caf86c8cd0499b63c47d71a6601b5de6f87fcbacc34 (same before and after; HEAD and status unchanged)
- Mode: narrow confirmation of round 1 fixes
- Reviewer: dev-reviewer (requested model/effort: opus/xhigh; effective: unknown)
- Scope: the round 1 fixes (dev-gate step 4 and merge row, dev-docs step 3, dev-implement, dev-review step 3, dev-continue, tests/test_rule_citations.py, tests/test_core_checks.py docstring, FU-005, FU-010, CHANGELOG, graph.json)  Requirements: REQ-022  DoD: each round 1 fix correct and complete, no new problem
- Writing: written per ASD-STE100 principles; full conformance not verified (R-WRT-1)

## Findings

| ID | Relation | Severity | Location | Finding | Evidence | Impact | Class | Disposition |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| FR2-001 | in-scope | MUST-FIX | skills/dev-implement/SKILL.md:47-48 | The FR1-005 fix says "R-EXH-3 says where the scan and gate records go", but the rule for records before a PR exists (never in the commit they cover; a later commit or an authorized PR comment) is in R-REV-9; R-EXH-3 covers only the time after a PR exists | dev-core R-REV-9 last-but-one bullet; R-EXH-3; HEAD dev-implement:49-52 | Citation points to the wrong rule; REQ-022 acceptance 1 not met for this sentence | necessary fix | Needs Human Decision, then Fixed by the user's card 6 answer (a) (「6a，FU-006 合併後 FU-010 列為下一項並做完整盤點」): the HEAD text is restored word for word with (R-REV-9), (R-EXH-3) and (CB-4) added (re-review: rounds 3 and 4; kept in the card 7a rebuild) |

Round 1 fixes FR1-001 to FR1-006 and residual items R1, R2, R9, R10: confirmed correct, no new problem except FR2-001.

## Stop rule (R-VER-2)

Round 1 and round 2 both reported new blockers, and FR2-001 came from the fix of the same mechanism (rewriting restated rule text into new citation sentences) that produced FR1-001, FR1-002 and FR1-005. The fix loop stops; the approach goes to the user as a decision card.

## Verification evidence

Reviewer: `bash scripts/validate.sh` exit 0 (131 tests OK); `python3 -m unittest tests.test_rule_citations -v` 4 OK; `graph.py validate` ok; the section patterns applied in memory to `git show HEAD:<file>` flag all 7 old citations in 6 files and give no false positive on the tree; HEAD, diff hash and status count unchanged before and after. Not run: Security Diff Scan (not this mode); GateRuleText review (outside the boundary).

## Residual risk

R2-a: CORE_SECTION_RE misses "§ 8" with a space and plural "sections"; SECTION_RE misses some other phrasings (none present). R2-b: tests/test_core_checks.py:197 finds the section by its heading (fails loudly at a split). R2-c: FU-010 lists only part of the R-WRT-1 gaps (its verification plan covers items 1 to 6). R2-d: FU-005 row overstates that review-report IDs resolve through agent copies (R-REV-4, R-WRT-1 have no agent copy). R2-e: CHANGELOG and REQ-022 mention "section 8" descriptively. R2-f: round 1 says six citations; it is seven in six files. R2-g: only *.md under skills/ is scanned. R2-h: line width in dev-continue.

## Decision card 6 and the bounded fix round

User answer: (a). Criterion applied: an old text that restates exactly one dev-core rule becomes a pure pointer to that rule; an old text that combines several rules in one statement, or carries a condition or detail that the replacement would drop, is restored word for word from HEAD with the rule IDs added. Restored: dev-deliver D1, D4, D6 (first sentence), D7; dev-implement I5 (FR2-001); dev-review mode paragraph, native-option sentence, step 5 cards; dev-gate G1, G4, G6 (first item, scan item, header IDs). A whitespace-normalized check confirms each restored passage is in HEAD. Residual R2-a (CORE_SECTION_RE: "§ 8", plural "sections") and R2-d (FU-005 wording) fixed; FU-010 priority recorded.
