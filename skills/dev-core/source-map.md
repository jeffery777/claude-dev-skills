# dev-core source map

This file maps every anchor in the vendored Core v0.1.1 contracts to `dev-core`
rules. `scripts/check_core_coverage.py` fails when an anchor has no row, a row
names a missing anchor or rule, a rule cites a different anchor, or a
`not-applicable` row has no reason.

Status values: `covered`, `not-applicable`.

The script checks structure only: that every anchor is mapped and every rule
cites an anchor. It cannot detect a rule that relaxes Core. Each change to
`dev-core` therefore needs an independent rule-by-rule comparison against the
cited Core section (see review round 1, DR-001 to DR-008, in
`.dev/issue-1-phase1/reviews/round-1.md`).

| Core anchor | dev-core rules | Status | Note |
| --- | --- | --- | --- |
| `workflow.md#wf-stages` | R-STG-1, R-STG-2, R-STG-3, R-STG-4, R-STG-5 | covered | Stage table compressed into five rules |
| `workflow.md#wf-writing` | R-WRT-1 | covered | Traditional Chinese plain-writing rules spelled out; every review and gate report carries the ASD-STE100 note (DL-014) |
| `workflow.md#wf-capability` | R-CAP-1, R-CAP-2, R-CAP-3 | covered | Native Claude Code capabilities named explicitly |
| `workflow.md#wf-delegation` | R-DEL-1, R-DEL-2 | covered | Model/effort floor tightened (D-007) |
| `workflow.md#wf-verification` | R-VER-1, R-VER-2, R-VER-3 | covered | R-VER-2 adds the stop rule for the fix loop (DL-012) |
| `workflow.md#wf-assumptions-and-options` | R-RIG-3, R-RIG-4 | covered | R-RIG-3 adds requirement tracing and SCOPE-CREEP (D-003); R-RIG-4 carries the premise and option rules |
| `workflow.md#wf-evidence-lifecycle` | R-EVD-1, R-EVD-2 | covered | Illustrative scenario table not copied; read Core for cases |
| `authorization-and-stops.md#auth-scope` | R-AUTH-1, R-AUTH-2 | covered | |
| `authorization-and-stops.md#auth-destructive` | R-AUTH-3, R-AUTH-4 | covered | |
| `authorization-and-stops.md#auth-stops` | R-AUTH-5, R-AUTH-6 | covered | R-AUTH-6 uses the decision card (DL-014) |
| `authorization-and-stops.md#auth-data` | R-AUTH-7 | covered | |
| `review-and-security.md#review-independent` | R-REV-1, R-REV-2 | covered | Edit/Write removed by the tool allowlist; read-only Bash use is by instruction (DL-004) |
| `review-and-security.md#review-findings` | R-RIG-2, R-REV-3, R-REV-4, R-REV-5 | covered | Adds SCOPE-CREEP severity; severity thresholds, `requirement_relation` and `REQ-GAP` (DL-011); classification before fixing and narrow confirmation before a push (DL-012) |
| `review-and-security.md#review-risk-timing` | R-RIG-1, R-RIG-2, R-REV-6 | covered | Rigor tiers map Core risk timing (D-004) |
| `review-and-security.md#review-security` | R-REV-7, R-REV-9 | covered | R-REV-9 tightens: a scan before every commit, push, PR post and Issue post, including commit identity and message (DL-010); once a PR exists, scan and gate records never go into a commit on the PR branch (DL-013) |
| `review-and-security.md#review-evidence` | R-REV-8 | covered | R-REV-8 adds the masking rule for review and gate records (DL-016) |
| `exact-head-and-evidence.md#exact-identity` | R-EXH-1 | covered | |
| `exact-head-and-evidence.md#exact-coherence` | R-EXH-2 | covered | |
| `exact-head-and-evidence.md#exact-transition` | R-EXH-3 | covered | Records of a PR head are never committed to the PR branch; a PR comment only with the user's authority, otherwise uncommitted in the report; evidence reuse only for provably unaffected parts, with reason and coverage (DL-013) |
| `exact-head-and-evidence.md#exact-dimensions` | R-EXH-4 | covered | |
| `exact-head-and-evidence.md#exact-pinning` | R-EXH-5 | covered | Lock records source, consumer, assembler, layout, environment, sections used and closure; `scripts/verify_core.py` checks digests and, with `--upstream`, the tag |
