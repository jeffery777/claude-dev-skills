# dev-core source map

This file maps every anchor in the vendored Core v0.5.0 contracts to `dev-core`
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
| `workflow.md#wf-stages` | R-STG-1, R-STG-2, R-STG-3, R-STG-4, R-STG-5 | covered | R-STG-2 and R-STG-4 keep their text; R-STG-1, R-STG-3 and R-STG-5 are index lines (FU-005 PR-4) |
| `workflow.md#wf-writing` | R-WRT-1, R-WRT-2 | covered | R-WRT-1: the three items of the Core minimum, plus the Traditional Chinese plain-writing rules and the ASD-STE100 note in every review and gate report (DL-014, DL-051); R-WRT-2: the two-layer trigger for `writing.md` and the spot-check |
| `workflow.md#wf-capability` | R-CAP-1, R-CAP-2, R-CAP-3 | covered | Native Claude Code capabilities named explicitly |
| `workflow.md#wf-delegation` | R-DEL-1, R-DEL-2 | covered | Model/effort floor tightened (D-007) |
| `workflow.md#wf-verification` | R-VER-1, R-VER-2, R-VER-3, R-VER-5 | covered | R-VER-2 says when the re-evaluation stops for the user (DL-049); R-VER-5 adds the Lesson candidates section of the `dev-deliver` and `dev-review` reports (DL-035) |
| `workflow.md#wf-assumptions-and-options` | R-RIG-3, R-RIG-4 | covered | R-RIG-3 adds requirement tracing and SCOPE-CREEP (D-003); R-RIG-4 is an index line (FU-005 PR-4) |
| `workflow.md#wf-evidence-lifecycle` | R-EVD-1, R-EVD-2, R-EVD-3 | covered | Illustrative scenario table not copied; read Core for cases |
| `authorization-and-stops.md#auth-scope` | R-AUTH-1, R-AUTH-2 | covered | |
| `authorization-and-stops.md#auth-destructive` | R-AUTH-3, R-AUTH-4 | covered | |
| `authorization-and-stops.md#auth-stops` | R-AUTH-5, R-AUTH-6 | covered | R-AUTH-6 uses the decision card (DL-014) |
| `authorization-and-stops.md#auth-data` | R-AUTH-7 | covered | |
| `review-and-security.md#review-independent` | R-REV-1, R-REV-2 | covered | Edit/Write removed by the tool allowlist; read-only Bash use is by instruction (DL-004) |
| `review-and-security.md#review-required-read-only` | R-REV-1 | covered | The user's acceptance record on the user's machine and its check (D-032, DL-004, `references/reviewer-acceptance.md`) |
| `review-and-security.md#review-findings` | R-RIG-2, R-REV-3, R-REV-4, R-REV-5 | covered | Adds SCOPE-CREEP severity; severity thresholds, `requirement_relation` and `REQ-GAP` (DL-011); classification before fixing and narrow confirmation before a push (DL-012) |
| `review-and-security.md#review-risk-timing` | R-RIG-1, R-RIG-2, R-REV-6 | covered | Rigor tiers map Core risk timing (D-004) |
| `review-and-security.md#review-security` | R-REV-7, R-REV-9 | covered | R-REV-9 tightens: a scan before every commit, push, PR post and Issue post, including commit identity and message (DL-010); once a PR exists, scan and gate records never go into a commit on the PR branch (DL-013) |
| `review-and-security.md#review-publication-data` | R-REV-9 | covered | Sentence by sentence in DL-050; push options and Git LFS objects stop the push (card I106-C12 (a)) |
| `review-and-security.md#review-evidence` | R-REV-8 | covered | R-REV-8 adds the masking rule for review and gate records (DL-016) |
| `exact-head-and-evidence.md#exact-identity` | R-EXH-1 | covered | |
| `exact-head-and-evidence.md#exact-coherence` | R-EXH-2 | covered | |
| `exact-head-and-evidence.md#exact-transition` | R-EXH-3 | covered | Records of a PR head are never committed to the PR branch; a PR comment only with the user's authority, otherwise uncommitted in the report; evidence reuse only for provably unaffected parts, with reason and coverage; reusable content evidence is bound to the tree and the diff, and the new review binds the exact base, head and merge-base (Issue #68 E2, DL-013) |
| `exact-head-and-evidence.md#exact-dimensions` | R-EXH-4 | covered | |
| `exact-head-and-evidence.md#exact-pinning` | R-EXH-5 | covered | Lock records source, consumer, assembler, layout, environment, sections used and closure; `scripts/verify_core.py` checks digests and, with `--upstream`, the tag |
| `writing.md#writing-scope` | R-WRT-2 | covered | Read in full only for a document task (the two layers of `wf-writing`) |
| `writing.md#writing-principles` | R-WRT-2 | covered | Index: read Core for a document task |
| `writing.md#writing-genres` | R-WRT-2 | covered | Index: read Core for a document task |
| `writing.md#writing-sources` | R-WRT-2 | covered | Index: read Core for a document task |
| `writing.md#writing-language` | R-WRT-2 | covered | Index; the fixed ASD-STE100 statement of R-WRT-1 stays (a downstream stricter rule that this section keeps) |
| `writing.md#writing-process` | R-WRT-2 | covered | The spot-check of R-WRT-2 in the existing review report |
