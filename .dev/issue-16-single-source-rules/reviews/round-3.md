# Review round 3 (full deep review after card 6a) — issue-16-single-source-rules

- Target: working tree at HEAD 1386a69 (+ uncommitted, intent-to-add)
- Diff identity: sha256 of `git diff HEAD --binary` = 7d5b40cdc12e2d7285c6aba22d81104d6df7e24c11b66ab9ca038348bf5ea391 (same before and after; HEAD and status unchanged)
- Mode: deep
- Reviewer: dev-reviewer (requested model/effort: opus/xhigh; effective: unknown)
- Scope: the 26 files of `git diff HEAD`  Requirements: REQ-022  DoD: card 6a method for every changed sentence; records consistent
- Writing: written per ASD-STE100 principles; full conformance not verified (R-WRT-1)

## Findings

| ID | Relation | Severity | Location | Finding | Evidence | Impact | Class | Disposition |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| FR3-001 | in-scope | MUST-FIX | skills/dev-review/references/review-report.md severity and REQ-GAP paragraphs | The thresholds were replaced by an R-REV-3 pointer, but this file is given to the reviewer agents, and `dev-security-reviewer` does not load dev-core and has no copy of the thresholds | dev-review step 3; agents/dev-security-reviewer.md:44-48 (verified: no threshold text) | Security review loses its severity thresholds | necessary fix | Fixed by card 7a: review-report.md is main text word for word, with (R-REV-3), (R-RIG-3), (R-REV-8) added (re-review: round 4) |
| FR3-002 | in-scope | MUST-FIX | skills/dev-gate/SKILL.md step 6 | "A failed or unrun check follows R-EXH-2", but R-EXH-2 says only "A missing or unrun CI is not Passed" | dev-core R-EXH-2 (verified); HEAD dev-gate:80 | "failed" loses its rule | necessary fix | Fixed by card 7a: "A failed or unrun check is never Passed (R-EXH-2)" is main text again (re-review: round 4) |
| FR3-003 | in-scope | MUST-FIX | dev-continue comment scan; dev-gate merge row, step 6 first line, step 7 "void"; dev-review line 10, step 3; review-report dispositions | Seven partial rewrites: neither a pure pointer nor a verbatim restoration (card 6a) | HEAD vs current, phrase by phrase | Same mechanism as FR1-001/002/005 and FR2-001 | necessary fix | Fixed by card 7a: all seven places are main text word for word, with rule IDs added (re-review: round 4) |
| FR3-004 | in-scope | MUST-FIX | dev-review step 6; dev-deliver step 7; dev-review mode paragraph | Pointer sentences dropped the actor (independent reviewer, `dev-security-reviewer`, reviewer agents) | HEAD text | R-WRT-1 explicit actor; same kind as FR1-005 | necessary fix | Fixed by card 7a: the three sentences are main text word for word, with their actors (re-review: round 4) |
| FR3-005 | in-scope | NIT | .dev/followups.md FU-005 | Says `dev-security-reviewer` keeps the R-REV-3 thresholds; it keeps only the names | agents/dev-security-reviewer.md:44-48 | False record | necessary fix | Fixed: FU-005 row rewritten (re-review: round 4, which found it still incomplete: FR4-001) |
| FR3-006 | in-scope | NIT | CHANGELOG, CF-008 zh/EN, REQ-022 acceptance 1 and sources, log.md | Records do not reflect card 6a (restored text with IDs) | final diff | Records inconsistent with the diff | necessary fix | Fixed: CHANGELOG, CF-008 zh and EN, REQ-022 need, acceptance and sources, and log.md rewritten for card 7a (re-review: round 4) |

## Stop rule (R-VER-2) and the user's condition

The user's card 6 answer said: if round 3 finds a new blocker of the same kind, stop and report. FR3-001 to FR3-004 are of the same kind (rewritten rule text that loses a condition, an actor, a reader or names the wrong rule). The main session also missed partial rewrites (FR3-003, FR3-004) when it applied card 6a. Fix loop stopped; next step goes to the user as a decision card.

## Verification evidence

Reviewer: `bash scripts/validate.sh` all checks passed (21 anchors, 41 rules, 131 tests OK); `python3 -m unittest tests.test_rule_citations tests.test_platform_profile.GateRuleText -v` 8 OK; test patterns applied in memory to `git show HEAD:<file>`; phrase-by-phrase comparison of HEAD and the tree; `git grep` for rule IDs in non-Markdown files. HEAD, diff hash and status unchanged. Not run: Security Diff Scan (not applicable to rule text); the R-REV-9 scan (separate).

## Residual risk

R3-a GateRuleText negative test checks two phrases only; R3-b `(section N)` flagged in any file, ID scan covers *.md only; R3-c stale-base rationale only in platform-profile.md; R3-d decision-card cites R-REV-3 for any requirement-adding answer; R3-e dev-implement no longer names `dev-review` for light work; R3-f DL-016 "Core does not ask for masking" vs Core auth-data (public records keep only safe information); R3-g round-2 FR2-001 marked Fixed before confirmation; R3-h graph T4 still `planned`.

## Card 7a fix pass

User answer 7a (verbatim quote in REQ-022 sources). Before the pass, the full diff was saved as a patch outside the repository (sha256 equals the round-3 diff identity, `git apply --check -R` OK). Each skill and reference file was rebuilt from main (HEAD 1386a69) with only: the R-EXH-3 pointers (dev-review step 5, dev-gate step 8), the R-VER-2 pointers (dev-deliver step 5, dev-review step 6), the R-EXH-4 pointers (dev-gate step 6, platform-profile.md three places), CB-1/CB-4 in place of section numbers, and rule IDs added to word-for-word text. FR3-001 to FR3-004 are removed with the rewritten text. FR3-005: FU-005 row corrected. FR3-006: CHANGELOG, CF-008 (zh, EN, with the card 7a lesson), REQ-022 (need, acceptance, sources) and log.md updated. R3-f: DL-016 reason corrected (Core auth-data asks for safe public records, no masking format).
