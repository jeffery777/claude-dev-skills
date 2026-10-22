# Review round 6 (narrow confirmation, R-REV-4) — issue-16-single-source-rules

- Target: working tree at HEAD 1386a69 (+ uncommitted, intent-to-add)
- Diff identity: sha256 of `git diff HEAD --binary` = 08fe36b566ede31cb4e5580a807d632c180e444f8986952e3fedb96b1d306b16 (same before and after; HEAD and status unchanged)
- Mode: narrow confirmation of the round 5 fixes
- Reviewer: dev-reviewer (requested model/effort: opus/high; effective: unknown)
- Scope: FU-005 row, reviews/round-1.md, round-4.md, round-5.md, CF-008 zh and EN; agents/ has no diff  Requirements: REQ-022  DoD: each round 5 fix correct and complete, no new problem
- Writing: written per ASD-STE100 principles; full conformance not verified (R-WRT-1)

## Findings

| ID | Relation | Severity | Location | Finding | Evidence | Impact | Class | Disposition |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| FR6-001 | in-scope | NIT | reviews/round-4.md R4-i | "no `.py` file cites a rule ID today" is false | `grep` of rule IDs in `*.py`: platform_profile.py:281, graph.py:703, test_platform_profile.py, test_core_checks.py | Residual risk recorded as "no effect" | necessary fix | Fixed: R4-i lists the Python citations and states that the test does not cover them (re-review: round 7, narrow) |

FR5-001, FR5-002 and FR5-003 confirmed correct. No MUST-FIX: the R-VER-2 stop rule does not apply.

## Verification evidence

Reviewer: `bash scripts/validate.sh` passed; `python3 -B -m unittest discover -s tests -q` 131 OK; `git diff HEAD --check` clean; FU-005 items checked against agents/*.md line by line; CF-008 quotes compared byte by byte with REQ-022 sources. Not run: full deep review; GitNexus; R-REV-9 scan (separate).

## Residual risk

RR6-a: the FU-005 measure lives in followups.md only, and no skill points a rule-changing session to it. RR6-b: round records 1 to 6 have no separate "Requirement trace" and "Security scan" sections. RR6-c: `Fixed` rows name no fix revision (no commits yet). RR6-d: further reviewer sentences copy rules (R-REV-7 "recommend a security review", "keep verified findings apart"); the FU-005 list is a minimum. RR6-e: gitignored `__pycache__` folders exist in the tree (origin unknown; not created or deleted by the reviewer). RR6-f: long line in core-feedback.md EN.
