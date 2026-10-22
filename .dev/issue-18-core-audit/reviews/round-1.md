# Review round 1 (deep), Issue #18

- Target: working tree against HEAD `a1d42a6`, `git diff HEAD --binary` sha256 `324aed7b…` (untracked files
  intent-to-add). Reviewer: `dev-skills:dev-reviewer` (opus, xhigh), read-only.
- Scope: `skills/dev-core/**`, `.dev/issue-18-core-audit/**`, records (REQ-023, index, log, followups,
  CF-009, CHANGELOG). DoD and acceptance: REQ-023.
- Commands (reviewer): `PYTHONDONTWRITEBYTECODE=1 bash scripts/validate.sh` exit 0 (14 vendored files, 21
  anchors, 131 tests, both plugin manifests valid). CB-4 before and after: HEAD, status hash, diff hash and the
  hash of the ignored-file list unchanged. Skipped: GitNexus (docs only, no call paths).

## Findings and dispositions

Classification before the fix (R-REV-4) is given for each finding.

| ID | Relation | Severity | Finding | Class | Disposition in that round (superseded: the final disposition is in `round-3.md`) |
| --- | --- | --- | --- | --- | --- |
| R1-001 | in-scope | MUST-FIX | Rules rated equal still miss Core words: wf:62 (no lower DoD, no invented qualification), rev:47 (code review includes a baseline security check), wf:13/wf:46 (check public capabilities, schemas, permissions), auth:46 (verification of memory operations), auth:21/23 (checked preview; explicit confirmation) | necessary fix | Fixed: words added to R-DEL-2, R-REV-7, R-STG-2, R-AUTH-7, R-AUTH-3; audit rows corrected |
| R1-002 | in-scope | MUST-FIX | The added R-EXH-5 sentence is weaker than exh:58 (old receipts; the interface's own verification of every affected part) | necessary fix | Fixed |
| R1-003 | in-scope | MUST-FIX | The R-WRT-1 literal bullet lost Core's condition "for the writing rules" and conflicts with R-REV-8 masking | necessary fix | Fixed: "The writing rules never change machine literals (… and the like) …; masking under R-REV-8 still applies" |
| R1-004 | in-scope | MUST-FIX | The restored destructive-action list (prune) conflicts with `git fetch --prune` in R-REV-9 and `dev-implement` step 4 | needs human decision | Fixed by user decision card 4 (a), 「同意你的建議，選a。」: R-REV-9 records the `--prune` of that fetch as a project policy that covers no other prune (REQ-023 sources) |
| R1-005 | in-scope | NIT | `audit.md`: "dictionary" was not new in item 4; the list of copied rules missed R-REV-8 | necessary fix | Fixed |

Suspicions S1 to S8 (the reviewer's inferences, not rated), all classified as necessary fixes because each
names a Core obligation missing in `dev-core`: S1 R-AUTH-5 joined "no safe fallback" with "and" (now a
separate condition, the stricter reading); S2 R-STG-5 checkpoint content; S3 R-RIG-4 independent sources and
the human-decision triggers; S4 R-STG-2 repository identity and R-AUTH-1 environment; S5 R-REV-5 result
contents; S6 R-EVD-1 reason and readable evidence, R-VER-3 exception; S7 recorded as residual risk in
`audit.md` (no text conflict); S8 unmapped Core lines now listed with their rules in `audit.md`. Residual items
fixed as well: R-STG-6 actor, R-CAP-1 wording, wf:56 moved from "kept out" into R-DEL-2, "not proposed" in
REQ-023. Fixes verified with `bash scripts/validate.sh` (all checks passed).

## Residual risk

- R-VER-2 "widen or rerun them only for …" could be read as a reason to skip a required rerun; "Never skip
  required checks" in the same rule limits it.
- R-AUTH-1 "user's instructions take priority over skill defaults" does not say which tightenings are skill
  defaults; the sentence follows Core auth:9.
- DL-017 has the type `compress` but also records two new rules and one rephrase.
- The reviewer agents do not get the added R-REV-1 and R-EXH-2 items (FU-005).

Writing spot-check (reviewer): scope the changed rules, `audit.md`, CF-009, CHANGELOG, REQ-023; results: two
wording items, fixed; limits: no full ASD-STE100 check. Written per ASD-STE100 principles; full conformance not
verified.

## Superseded by user decision card 5 (after round 2)

PR-A was narrowed (see `round-2.md`). The R1-001 additions and the R1-002 sentence were omissions and are
removed from `dev-core`; they stay listed in `audit.md` and are Deferred to FU-005 (input for the on-demand
loading design). Kept: the R1-001 R-AUTH-3 conditions (checked preview, explicit confirmation; a looser
sentence), R1-003 (R-WRT-1), R1-004 (card 4), R1-005, and S1 (R-AUTH-5). The S2 to S6 additions are removed
as omissions (FU-005).
