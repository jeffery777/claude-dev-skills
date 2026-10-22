# Review round 1 — issue-22-fu005-records (FU-005 PR-1)

- Target: working tree at 0fc4e5f (+ uncommitted; new files intent-to-add)
- Diff identity: sha256 of `git diff HEAD --binary` 8d14faae49f54a86a9a9a4ae4b7f7a46b08b44f7828c4ab8708d6bf5a91f7a0e (review); e32cdc70a43f380a9a1eb9a6904ea0120d69c0cae9262b52298fc5489f45f878 (narrow confirmation after fixes); bb9a08ef4698163b1c63ce43c66a1702e3a67a4f27a5b45a3bf3ac4f3431ea51 (confirmation of the PR1-006 fix); 5185e64cad645977d04f5f5806a0c0efab0673ae2f7e382623c90c658d06212d (confirmation of the PR1D-001 fix; this record line was edited afterwards). HEAD, `git status --porcelain=v1 --untracked-files=all` and the hash were the same before and after each review (CB-4).
- Mode: deep (strict tier); then a narrow confirmation (R-REV-4)
- Reviewer: `dev-skills:dev-reviewer` (requested model/effort: opus/xhigh; effective: unknown)
- Scope: `skills/dev-core/SKILL.md`, `skills/dev-core/deltas.md`, `docs/requirements/` (REQ-025, index, log), `docs/design-proposal.md`, `docs/core-feedback.md`, `.dev/followups.md`, `CHANGELOG.md`, `.dev/issue-22-fu005-records/`. Requirements: REQ-025, REQ-007, REQ-022, REQ-023, REQ-024, REQ-018, REQ-005. DoD: the PR-1 acceptance of REQ-025 and the approved FU-005 spec (sections 1.1 (D), 1.3, 5, 7.2 PR-1).
- Writing: written per ASD-STE100 principles; full conformance not verified (R-WRT-1)

## Findings

| ID | Relation | Severity | Location | Finding | Evidence | Impact | Class | Disposition |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PR1-001 | in-scope | SHOULD-FIX | `deltas.md` DL-019, DL-022, DL-023, DL-024; `.dev/followups.md` FU-012 | Empty Evidence cells, while design card 6b closes FU-012 on "reasons in the Reason and Evidence columns" | per-row parse of `deltas.md` | FU-012 closure partly unsupported | necessary fix | Fixed: "None recorded yet"; FU-012 lists the seven rows without evidence (DL-005, DL-006, DL-007, DL-019, DL-022, DL-023, DL-024); confirmed |
| PR1-002 | in-scope | NIT | `docs/design-proposal.md` D-001 note and D-020 (zh/EN); REQ-025 acceptance | D-001 marked "refined"; the approved spec says "superseded"; present tense for behavior that starts in PR-2 | spec 1.3; checklist table E | Record differs from the approved spec | necessary fix | Fixed: "superseded by D-020, in effect from PR-2" in all places; confirmed |
| PR1-003 | in-scope | NIT | `deltas.md` DL-018, DL-023, DL-025 | `commit_state` is D-008, not only D-010; the CF-009 item 1 and dry-run link and two "Core-feedback candidate" notes have no item in `docs/core-feedback.md` | `docs/design-proposal.md:286`; `docs/core-feedback.md` CF-009 | Citations cannot be followed | necessary fix | Fixed: (D-008, D-010); "a Core-feedback candidate in the FU-005 design, not yet in `docs/core-feedback.md`"; confirmed |
| PR1-004 | in-scope | NIT | `.dev/followups.md` FU-011 | The scope list leaves out R-CAP-1 (DL-006, rephrase), which design card 6a includes | card 6a: tables A, B and C | FU-011 narrower than decided | necessary fix | Fixed: scope names checklist tables A, B and C; confirmed |
| PR1-005 | no-requirement | SCOPE-CREEP | D-020 (zh/EN), REQ-025, FU-005 | "Each PR starts after the previous one merges and the user says to continue" is in no source and no spec prerequisite | spec 7.2 prerequisites | An unsourced human gate attributed to the user | necessary fix (the text named a gate that no source states) | Fixed: each PR starts after the previous one merges (PR-2 also waits for the FU-004 baseline run); the user decides each merge; confirmed |
| PR1-006 | gap | REQ-GAP | new DL rows, REQ-025, FU-011 | The citations "FU-005 checklist item C-n" and "FU-005 design review R1-001, R2-004" point to the approved design record, which is outside the repository; no requirement says where it is kept | `grep`: no checklist in the repository | Repo readers cannot check the citations (R-EVD-2); PR-4 needs checklist table D | needs human decision | Resolved by the user (「PR1-006 選 a」): the approved spec and checklist are in `.dev/issue-22-fu005-records/` word for word (masking only, recorded in its `README.md`); REQ-025 names the location |

Narrow confirmation of the PR1-006 fix (diff sha256 bb9a08ef4698163b1c63ce43c66a1702e3a67a4f27a5b45a3bf3ac4f3431ea51):

| ID | Relation | Severity | Location | Finding | Evidence | Impact | Class | Disposition |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PR1D-001 | unrelated | MUST-FIX | `.dev/issue-22-fu005-records/README.md` | The README gave the SHA-256 of the unmasked original spec; the original differs from the copy in one masked path, so a reader can guess the masked account name offline against the hash | difflib comparison: one line differs | The masking fails (private identifier; R-AUTH-7, R-REV-8; same class as FU-003) | necessary fix (Core blocker: private data) | Fixed: only the hash of the masked copy is recorded; the original's hash stays outside the repository |

Limit from the same check, also fixed: DL-021, DL-025, DL-026 and DL-027 cited the FU-005 design review records, which stay outside the repository; their Evidence now points to the checklist items C-5, C-20, C-21 and C-22 in `fu005-checklist.md`, which record those findings.

## Requirement trace

| REQ | Covered by | Verified by |
| --- | --- | --- |
| REQ-025 | all changes | the two readings match the approved spec text (substring check); the quotes match the existing REQ quotes and the design record; graph check 0 errors, 0 warnings |
| REQ-007, REQ-023 | `SKILL.md` adds only the two readings and five origin sentences; DL-001 to DL-017 unchanged | `git diff HEAD` line by line |
| REQ-022 | rule IDs and bold definitions unchanged | `check_core_coverage.py`, `test_rule_citations.py` patterns read; `validate.sh` passed (main agent) |
| REQ-024 | agent files and `task-brief.md` unchanged | not in the diff |
| REQ-018 | CHANGELOG entry | content checked |
| REQ-005 | D-020, D-001 note and core-feedback in zh and EN | point by point |

## Security scan

Applicable: no Security Diff Scan (documents and rule text; the R-AUTH-5 reading is only stricter; no permission, tool, installation or executable change). Baseline pattern check of the added lines: no private path, email, token or key. The R-REV-9 commit and push scans run separately.

## Verification evidence

- Main agent: `bash scripts/validate.sh` → all checks passed (before and after the fixes).
- Reviewer: read-only `git`, `grep`, `sed`, `shasum` and printing `python3 -I -B -c` (including a read-only call of the `graph.py` check function); no test run, no file written.

## Residual risk and limits

- Until PR-4, R-AUTH-5 has both its old text ("…, and no safe fallback exists") and the stricter project reading; DL-028 and the header give the stricter reading.
- The CB-4 general-purpose implementer substitute is not a Core-named fallback; CB-4 itself, kept word for word, covers it (design card 9b).
- The user's quotes were compared with existing repository quotes and the design record, not with the original conversations.
- Zero findings in the narrow confirmation do not prove there are no defects.
